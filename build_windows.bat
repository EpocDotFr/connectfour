@ECHO off
REM Batch script to build the Connect Four Windows executable.
REM The resulting "connectfour_windows.exe" executable will be available in the "dist" directory.

pyinstaller ^
    --clean --noconfirm --onefile --windowed ^
    --log-level=WARN ^
    --name="connectfour_windows" ^
    --icon="resources/images/icon.ico" ^
    --add-data="resources;resources" ^
    run.py