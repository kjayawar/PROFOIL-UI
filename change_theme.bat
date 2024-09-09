@echo off
set /p filename=Enter the selected theme to apply:
copy ".\themes\%filename%" "preferences.py"
if %errorlevel%==0 (
    echo File copied successfully.
) else (
    echo Error: Unable to copy the file.
)
pause