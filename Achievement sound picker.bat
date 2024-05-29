@echo off
setlocal

REM Set the source folder and file paths
set "SourceFolder=sounds\eng\x\_"
set "SourceFile360=%SourceFolder%\x_common 360.zsm"
set "SourceFileXB1=%SourceFolder%\x_common XB1.zsm"
set "SourceFilePS3=%SourceFolder%\x_common PS3.zsm"
set "SourceFileHint=%SourceFolder%\x_common Hint Sound.zsm"
set "SourceFileLevel=%SourceFolder%\x_common Level Up Rep Sound.zsm"
set "SourceFileSecret=%SourceFolder%\x_common Secret Sound.zsm"
set "SourceFileTreasure=%SourceFolder%\x_common Treasure Sound.zsm"

REM Prompt the user for their selection
echo Select the achievement sound you want:
echo [1] Xbox 360
echo [2] Xbox One 
echo [3] PS3
echo [4] Hint Sound
echo [5] Level Up Rep Sound
echo [6] Secret Sound (default sound)
echo [7] Treasure Sound

set /p "Selection=Enter your choice (1, 2, 3, 4, 5, 6, or 7): "

REM Copy and rename the selected file
if "%Selection%"=="1" (
    echo Copying Xbox 360 file...
    copy "%SourceFile360%" "%SourceFolder%\x_common.zsm" >nul || (
        echo Error: Failed to copy Xbox 360 file.
        goto :EOF
    )
    echo File copied and renamed to x_common.zsm.
    echo Now using the Xbox 360 achievement sound!
) else if "%Selection%"=="2" (
    echo Copying Xbox One file...
    copy "%SourceFileXB1%" "%SourceFolder%\x_common.zsm" >nul || (
        echo Error: Failed to copy Xbox One file.
        goto :EOF
    )
    echo File copied and renamed to x_common.zsm.
    echo Now using the Xbox One achievement sound!
) else if "%Selection%"=="3" (
    echo Copying PS3 file...
    copy "%SourceFilePS3%" "%SourceFolder%\x_common.zsm" >nul || (
        echo Error: Failed to copy PS3 file.
        goto :EOF
    )
    echo File copied and renamed to x_common.zsm.
    echo Now using the PS3 achievement sound!
) else if "%Selection%"=="4" (
    echo Copying Hint Sound file...
    copy "%SourceFileHint%" "%SourceFolder%\x_common.zsm" >nul || (
        echo Error: Failed to copy Hint Sound file.
        goto :EOF
    )
    echo File copied and renamed to x_common.zsm.
    echo Now using the Hint achievement sound!
) else if "%Selection%"=="5" (
    echo Copying Level Up Rep Sound file...
    copy "%SourceFileLevel%" "%SourceFolder%\x_common.zsm" >nul || (
        echo Error: Failed to copy Level Up Rep Sound file.
        goto :EOF
    )
    echo File copied and renamed to x_common.zsm.
    echo Now using the Level Up Rep achievement sound!
) else if "%Selection%"=="6" (
    echo Copying Secret Sound file...
    copy "%SourceFileSecret%" "%SourceFolder%\x_common.zsm" >nul || (
        echo Error: Failed to copy Secret Sound file.
        goto :EOF
    )
    echo File copied and renamed to x_common.zsm.
    echo Now using the Secret achievement sound!
) else if "%Selection%"=="7" (
    echo Copying Treasure Sound file...
    copy "%SourceFileTreasure%" "%SourceFolder%\x_common.zsm" >nul || (
        echo Error: Failed to copy Treasure Sound file.
        goto :EOF
    )
    echo File copied and renamed to x_common.zsm.
    echo Now using the Treasure achievement sound!
) else (
    echo Invalid selection!
)

endlocal
pause
