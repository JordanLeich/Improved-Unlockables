#!/usr/bin/env python3
"""Safely update Improved Unlockables from its latest GitHub release.

Uses only the Python standard library. The updater installs into the folder
containing this script and only records a version after the update succeeds.
"""

import json
import os
import re
import shutil
import stat
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath, PureWindowsPath

REPO_OWNER = "JordanLeich"
REPO_NAME = "Improved-Unlockables"
REPO_URL = "https://api.github.com/repos/{}/{}/releases/latest".format(
    REPO_OWNER, REPO_NAME
)
USER_AGENT = "Improved-Unlockables-Updater/2.0"
SAVED_VERSION_NAME = "saved_version.txt"
REQUEST_TIMEOUT_SECONDS = 30
DOWNLOAD_TIMEOUT_SECONDS = 90
MAX_DOWNLOAD_BYTES = 1024 * 1024 * 1024  # 1 GiB safety limit
MAX_ARCHIVE_FILES = 50000
MAX_UNCOMPRESSED_BYTES = 1024 * 1024 * 1024  # 1 GiB safety limit

# Supports common tags such as v18.0, 18.1.2, v19.0-beta.1, and build metadata.
VERSION_PATTERN = re.compile(
    r"^[vV]?(\d+(?:\.\d+)*)(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?$"
)


def say(message):
    print(message, flush=True)


def make_request(url, accept=None):
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    request = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS)


def parse_version(version_text):
    """Return a comparable version tuple or raise ValueError for unsupported tags."""
    match = VERSION_PATTERN.fullmatch(version_text.strip())
    if not match:
        raise ValueError("Unsupported version tag: {!r}".format(version_text))

    numbers = tuple(int(part) for part in match.group(1).split("."))
    prerelease_text = match.group(2)
    if prerelease_text is None:
        prerelease = None
    else:
        prerelease = tuple(
            (0, int(part)) if part.isdigit() else (1, part.lower())
            for part in prerelease_text.split(".")
        )
    return numbers, prerelease


def compare_versions(left_text, right_text):
    """Return -1, 0, or 1 according to semantic version ordering."""
    left_numbers, left_pre = parse_version(left_text)
    right_numbers, right_pre = parse_version(right_text)

    width = max(len(left_numbers), len(right_numbers))
    left_numbers += (0,) * (width - len(left_numbers))
    right_numbers += (0,) * (width - len(right_numbers))

    if left_numbers < right_numbers:
        return -1
    if left_numbers > right_numbers:
        return 1

    # A stable version is newer than a prerelease with the same numeric version.
    if left_pre is None and right_pre is not None:
        return 1
    if left_pre is not None and right_pre is None:
        return -1
    if left_pre is None and right_pre is None:
        return 0

    for left_part, right_part in zip(left_pre, right_pre):
        if left_part < right_part:
            return -1
        if left_part > right_part:
            return 1
    if len(left_pre) < len(right_pre):
        return -1
    if len(left_pre) > len(right_pre):
        return 1
    return 0


def get_latest_release():
    say("Checking GitHub for the latest Improved Unlockables release...")
    try:
        with make_request(REPO_URL, "application/vnd.github+json") as response:
            release = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise RuntimeError(
                "GitHub could not find a published 'latest' release for this repository. "
                "The updater needs a published GitHub Release, not only a source-code commit."
            ) from exc
        if exc.code == 403:
            raise RuntimeError(
                "GitHub denied the request (possibly an API rate limit). Try again later."
            ) from exc
        raise RuntimeError("GitHub returned HTTP {} while checking for updates.".format(exc.code)) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise RuntimeError("Could not reach GitHub: {}".format(exc)) from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RuntimeError("GitHub returned an invalid release response.") from exc

    tag_name = release.get("tag_name")
    if not isinstance(tag_name, str) or not tag_name.strip():
        raise RuntimeError("The GitHub release response did not contain a valid tag name.")

    # Validate the tag before using it in any update logic.
    try:
        parse_version(tag_name)
    except ValueError as exc:
        raise RuntimeError(
            "The latest GitHub tag {!r} is not a supported numeric version. "
            "Use tags such as v18.0 or v18.1.0. No files were changed.".format(tag_name)
        ) from exc

    zip_url = release.get("zipball_url")
    if not isinstance(zip_url, str) or not zip_url.startswith("https://github.com/"):
        # Fallback for a normal GitHub source archive.
        safe_tag = urllib.parse.quote(tag_name, safe="")
        zip_url = "https://github.com/{}/{}/archive/refs/tags/{}.zip".format(
            REPO_OWNER, REPO_NAME, safe_tag
        )

    say("Latest release: {}".format(tag_name))
    return tag_name, zip_url


def get_saved_version(version_file):
    try:
        value = version_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        say("No saved version file was found; treating this as a first update check.")
        return None
    except OSError as exc:
        raise RuntimeError("Could not read {}: {}".format(version_file.name, exc)) from exc

    if not value:
        say("The saved version file is empty; treating this as a first update check.")
        return None

    try:
        parse_version(value)
    except ValueError:
        say("Warning: saved version {!r} is not recognized; a full update will be attempted.".format(value))
        return None

    say("Installed version: {}".format(value))
    return value


def download_archive(zip_url, destination):
    say("Downloading update archive...")
    request = urllib.request.Request(zip_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT_SECONDS) as response:
            content_length = response.headers.get("Content-Length")
            if content_length:
                try:
                    if int(content_length) > MAX_DOWNLOAD_BYTES:
                        raise RuntimeError("The update archive exceeds the 1 GiB download safety limit.")
                except ValueError:
                    pass

            downloaded = 0
            with open(destination, "wb") as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    downloaded += len(chunk)
                    if downloaded > MAX_DOWNLOAD_BYTES:
                        raise RuntimeError("The update archive exceeded the 1 GiB download safety limit.")
                    output.write(chunk)
    except urllib.error.HTTPError as exc:
        raise RuntimeError("GitHub returned HTTP {} while downloading the update.".format(exc.code)) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise RuntimeError("The update download failed: {}".format(exc)) from exc

    if downloaded == 0:
        raise RuntimeError("GitHub returned an empty update archive.")
    say("Downloaded {:.1f} MB.".format(downloaded / (1024 * 1024)))


def safe_archive_path(member_name):
    """Validate a ZIP member path against absolute and traversal paths."""
    normalized = member_name.replace("\\", "/")
    posix_path = PurePosixPath(normalized)
    windows_path = PureWindowsPath(normalized)
    if not normalized or posix_path.is_absolute() or windows_path.is_absolute() or windows_path.drive:
        raise RuntimeError("The update archive contains an unsafe path: {!r}".format(member_name))
    if any(part in ("", ".", "..") for part in posix_path.parts):
        raise RuntimeError("The update archive contains an unsafe path: {!r}".format(member_name))
    return posix_path


def extract_to_staging(archive_path, staging_dir):
    """Safely extract a GitHub source ZIP to staging, stripping its root folder."""
    try:
        archive = zipfile.ZipFile(archive_path, "r")
    except (zipfile.BadZipFile, OSError) as exc:
        raise RuntimeError("The downloaded file is not a valid ZIP archive.") from exc

    with archive:
        infos = archive.infolist()
        if not infos:
            raise RuntimeError("The update archive is empty.")
        if len(infos) > MAX_ARCHIVE_FILES:
            raise RuntimeError("The update archive contains too many files; refusing to install it.")

        roots = set()
        total_uncompressed = 0
        validated = []
        for info in infos:
            member_path = safe_archive_path(info.filename.rstrip("/"))
            if not member_path.parts:
                continue
            roots.add(member_path.parts[0])
            mode = (info.external_attr >> 16) & 0xFFFF
            file_type = stat.S_IFMT(mode)
            if stat.S_ISLNK(mode):
                raise RuntimeError("The update archive contains a symbolic link; refusing to install it.")
            # Some ZIP producers store permission bits without a Unix file-type bit.
            # Accept those normal entries, but reject known non-regular special files.
            if not info.is_dir() and file_type not in (0, stat.S_IFREG):
                raise RuntimeError("The update archive contains a special file; refusing to install it.")
            if not info.is_dir():
                total_uncompressed += info.file_size
                if total_uncompressed > MAX_UNCOMPRESSED_BYTES:
                    raise RuntimeError("The extracted archive would exceed the 1 GiB safety limit.")
            validated.append((info, member_path))

        if len(roots) != 1:
            raise RuntimeError("Expected a GitHub source archive with one top-level folder; no files were changed.")
        root_name = next(iter(roots))
        top_level_items = set()
        for _, member_path in validated:
            if len(member_path.parts) >= 2:
                top_level_items.add(member_path.parts[1])

        missing = {"data", "dialogs", "scripts"} - top_level_items
        if missing:
            raise RuntimeError(
                "The downloaded archive does not look like an Improved Unlockables source archive "
                "(missing: {}). No files were changed.".format(", ".join(sorted(missing)))
            )

        extracted_count = 0
        for info, member_path in validated:
            if len(member_path.parts) < 2:
                continue
            relative = PurePosixPath(*member_path.parts[1:])
            # Never install repository metadata or the version marker directly from the archive.
            if relative.parts[0] == ".git" or relative.name.lower() == SAVED_VERSION_NAME.lower():
                continue
            target = staging_dir.joinpath(*relative.parts)

            # Resolve parents and ensure the target remains inside the staging directory.
            staging_resolved = staging_dir.resolve()
            target_resolved = target.resolve()
            if target_resolved != staging_resolved and staging_resolved not in target_resolved.parents:
                raise RuntimeError("An archive entry resolved outside the staging folder.")

            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue

            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info, "r") as source, open(target, "wb") as output:
                shutil.copyfileobj(source, output, length=1024 * 1024)
            extracted_count += 1

        if extracted_count == 0:
            raise RuntimeError("No installable files were found in the update archive.")
        say("Validated {} update files.".format(extracted_count))


def files_are_equal(source, target):
    if not target.is_file() or source.stat().st_size != target.stat().st_size:
        return False
    with open(source, "rb") as source_file, open(target, "rb") as target_file:
        while True:
            source_chunk = source_file.read(1024 * 1024)
            target_chunk = target_file.read(1024 * 1024)
            if source_chunk != target_chunk:
                return False
            if not source_chunk:
                return True


def atomic_copy(source, target):
    """Copy to a sibling temporary file, then replace the destination atomically."""
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_target = None
    try:
        fd, temp_name = tempfile.mkstemp(prefix=".iu-update-", suffix=".tmp", dir=str(target.parent))
        temporary_target = Path(temp_name)
        with os.fdopen(fd, "wb") as output, open(source, "rb") as input_file:
            shutil.copyfileobj(input_file, output, length=1024 * 1024)
            output.flush()
            os.fsync(output.fileno())
        try:
            shutil.copystat(source, temporary_target)
        except OSError:
            pass
        os.replace(str(temporary_target), str(target))
        temporary_target = None
    finally:
        if temporary_target is not None:
            try:
                temporary_target.unlink()
            except OSError:
                pass


def save_version_atomically(version_file, version):
    version_file.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".iu-version-", suffix=".tmp", dir=str(version_file.parent))
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as output:
            output.write(version + "\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(str(temp_path), str(version_file))
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def install_update(staging_dir, install_dir, version_file, latest_version):
    """Install changed files with rollback if any replacement fails."""
    staged_files = sorted(path for path in staging_dir.rglob("*") if path.is_file())
    plan = []
    for source in staged_files:
        relative = source.relative_to(staging_dir)
        # Safety check again just before installing.
        if any(part in (".", "..") for part in relative.parts):
            raise RuntimeError("Unsafe staged path encountered; refusing to install.")
        target = install_dir / relative
        if target.exists() and target.is_dir():
            raise RuntimeError("Cannot update file because a directory exists at: {}".format(target))
        if not files_are_equal(source, target):
            plan.append((source, target, relative))

    if not plan:
        say("The downloaded files are identical to the local files.")
        # Still update the marker only once all checks have passed.
        save_version_atomically(version_file, latest_version)
        return 0

    say("Installing {} changed files...".format(len(plan)))
    changed = []
    with tempfile.TemporaryDirectory(prefix="improved-unlockables-rollback-") as backup_name:
        backup_root = Path(backup_name)
        try:
            for source, target, relative in plan:
                existed = target.is_file()
                backup = backup_root / relative
                if existed:
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target, backup)
                changed.append((target, backup, existed))
                atomic_copy(source, target)

            # The version marker is the commit point: never advance it until files are installed.
            save_version_atomically(version_file, latest_version)
        except Exception as exc:
            say("Installation failed; attempting to roll back changed files...")
            rollback_errors = []
            for target, backup, existed in reversed(changed):
                try:
                    if existed and backup.exists():
                        atomic_copy(backup, target)
                    elif not existed:
                        target.unlink(missing_ok=True)
                except Exception as rollback_exc:
                    rollback_errors.append("{}: {}".format(target, rollback_exc))
            if rollback_errors:
                raise RuntimeError(
                    "Installation failed ({}). Some files could not be rolled back: {}".format(
                        exc, "; ".join(rollback_errors)
                    )
                ) from exc
            raise RuntimeError("Installation failed and was rolled back: {}".format(exc)) from exc

    return len(plan)


def check_for_updates():
    script_dir = Path(__file__).resolve().parent
    version_file = script_dir / SAVED_VERSION_NAME

    say("=" * 58)
    say("Improved Unlockables Auto Updater")
    say("Install folder: {}".format(script_dir))
    say("=" * 58)

    latest_version, zip_url = get_latest_release()
    saved_version = get_saved_version(version_file)

    if saved_version is not None:
        comparison = compare_versions(latest_version, saved_version)
        if comparison == 0:
            say("You're already on the latest version ({}).".format(saved_version))
            return
        if comparison < 0:
            say(
                "The installed version ({}) is newer than the latest release ({}). "
                "No downgrade will be performed.".format(saved_version, latest_version)
            )
            return
        say("Update available: {} -> {}".format(saved_version, latest_version))
    else:
        say("Preparing to install the latest version: {}".format(latest_version))

    with tempfile.TemporaryDirectory(prefix="improved-unlockables-update-") as temp_name:
        temp_dir = Path(temp_name)
        archive_path = temp_dir / "release.zip"
        staging_dir = temp_dir / "staged"
        staging_dir.mkdir()
        download_archive(zip_url, archive_path)
        extract_to_staging(archive_path, staging_dir)
        changed_count = install_update(staging_dir, script_dir, version_file, latest_version)

    say("Update completed successfully. Installed version: {}".format(latest_version))
    say("Changed files: {}".format(changed_count))
    say("You can now close this window and launch the game.")


def main():
    try:
        check_for_updates()
    except KeyboardInterrupt:
        say("Update cancelled by user. No further actions were taken.")
    except Exception as exc:
        say("\nUPDATE FAILED: {}".format(exc))
        say("Your previous version should remain in place if installation did not complete.")
        say("If this continues, check your internet connection and the GitHub Releases page.")
    finally:
        try:
            input("\nPress Enter to exit...")
        except (EOFError, KeyboardInterrupt):
            pass


if __name__ == "__main__":
    main()
