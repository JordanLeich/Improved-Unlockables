@echo off
setlocal

REM Set the source folder and file paths
set "SourceFolder=sounds\eng\x\_"
set "SourceFile360=%SourceFolder%\x_common 360.zsm"
set "SourceFileXB1=%SourceFolder%\x_common XB1.zsm"
set "SourceFilePS3=%SourceFolder%\x_common PS3.zsm"

REM Prompt the user for their selection
echo Select the achievement sound you want:
echo [1] Xbox 360
echo [2] Xbox One (default sound)
echo [3] PS3

set /p "Selection=Enter your choice (1, 2, or 3): "

REM Copy and rename the selected file
if "%Selection%"=="1" (
    echo Copying Xbox 360 file...
    copy "%SourceFile360%" "%SourceFolder%\x_common.zsm" >nul
    echo File copied and renamed to x_common.zsm.
	echo Now using the Xbox 360 achievement sound!
) else if "%Selection%"=="2" (
    echo Copying Xbox One file...
    copy "%SourceFileXB1%" "%SourceFolder%\x_common.zsm" >nul
    echo File copied and renamed to x_common.zsm.
	echo Now using the Xbox One achievement sound!
) else if "%Selection%"=="3" (
    echo Copying PS3 file...
    copy "%SourceFilePS3%" "%SourceFolder%\x_common.zsm" >nul
    echo File copied and renamed to x_common.zsm.
	echo Now using the PS3 achievement sound!
) else (
    echo Invalid selection!
)

endlocal

pause