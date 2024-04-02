@echo off
setlocal

REM Set the folder path
set "FolderPath=%USERPROFILE%\Documents\Activision\Marvel Ultimate Alliance\Save"

REM Set the file path to delete
set "FilePath=%FolderPath%\settings.dat"

REM Check if the file exists
if exist "%FilePath%" (
    echo Deleting file: %FilePath%
    del "%FilePath%"
    echo File deleted successfully. All unlocks have been reset!
) else (
    echo File not found: %FilePath%
    echo This means no current unlocks are saved and your unlocks are already reset.
)

endlocal

pause