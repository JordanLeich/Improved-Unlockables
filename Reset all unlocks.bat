@echo off
setlocal

REM Reset Marvel Ultimate Alliance saved unlocks.
REM Check the expected path and a OneDrive Documents alternative.

set "FilePath=%USERPROFILE%\Documents\Activision\Marvel Ultimate Alliance\Save\settings.dat"
set "OneDriveFilePath=%OneDrive%\Documents\Activision\Marvel Ultimate Alliance\Save\settings.dat"

echo.
echo Checking for settings.dat...
echo User profile: "%USERPROFILE%"
echo Expected path: "%FilePath%"
echo.

if exist "%FilePath%" (
    call :ResetFile "%FilePath%"
    goto :End
)

if defined OneDrive if exist "%OneDriveFilePath%" (
    echo Found settings.dat in the OneDrive Documents folder.
    call :ResetFile "%OneDriveFilePath%"
    goto :End
)

echo ERROR: settings.dat was not found at either checked location.
echo.
echo Please confirm the actual location of settings.dat in File Explorer.
echo If Documents is redirected, use the full path shown in File Explorer.
echo No files were deleted.

:End
echo.
pause
endlocal
exit /b

:ResetFile
echo Found file: "%~1"
echo.
choice /M "Delete this file to reset saved unlocks"
if errorlevel 2 (
    echo Cancelled. No files were deleted.
    exit /b
)
del /f /q "%~1"
if exist "%~1" (
    echo ERROR: The file could not be deleted.
) else (
    echo settings.dat deleted successfully. Saved unlocks have been reset.
)
exit /b
