@echo off
set /p filename=Enter the selected theme to apply:
copy "%filename%" "preferences.py"
if %errorlevel%==0 (
    echo File copied successfully.
) else (
    echo Error: Unable to copy the file.
)