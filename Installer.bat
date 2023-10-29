@echo off

:: Variable to track if the notice was displayed
set "noticeDisplayed="

:: Check if a marker file exists
if exist "installed.marker" (
    echo Requirements are already installed.
    echo.
    echo Running the Python script...
    echo.
    py "NDI Centerer.py"
    echo.
    pause
    exit /b
)

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed on your system.
    echo.
    echo Please install Python 3.11 from the Microsoft Store:
    echo.
    start ms-windows-store://pdp/?ProductId=9NRWMJP3717K
    echo.
    echo After installing Python, re-run this installer.bat script.
    echo.
    pause
    exit /b
)

:: Define package names
set "packages=PyGetWindow pyautogui Pillow opencv-python numpy"

:: Clear the screen
cls

:: Set the text color to green
color 0A

:: Install each package without a delay
for %%i in (%packages%) do (
    echo Installing %%i...
    python.exe -m pip install %%i >nul 2>&1

    :: Check if the notice is displayed and mark it as displayed
    python.exe -m pip install --no-warn-script-location pip >nul 2>&1
    set "noticeDisplayed=true"
)

:: Check if the notice was displayed and mark it as displayed
if not defined noticeDisplayed (
    python.exe -m pip install --no-warn-script-location pip >nul 2>&1
    set "noticeDisplayed=true"
)

:: Create a marker file to indicate that requirements are installed
if defined noticeDisplayed (
    echo. > "installed.marker"
    echo Python packages installed successfully.
    echo.
    echo Running the Python script...
    echo.
    python "NDI Centerer.py"
    echo.
)

:: Reset the text color to the default
color 07
