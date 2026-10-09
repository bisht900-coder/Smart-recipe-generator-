@echo off
title Smart Recipe Generator
echo ========================================================
echo   Starting Smart Recipe Generator...
echo ========================================================
echo.

:: 1. Try py launcher
py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Found Python launcher (py). Starting application...
    echo.
    py run.py
    goto end
)

:: 2. Try standard python command
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Found python command. Starting application...
    echo.
    python run.py
    goto end
)

:: 3. Check common User AppData Python installation paths
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        echo [INFO] Found Python at: %%D\python.exe
        echo.
        "%%D\python.exe" run.py
        goto end
    )
)

:: 4. Check common Program Files Python installation paths
for /d %%D in ("C:\Program Files\Python*") do (
    if exist "%%D\python.exe" (
        echo [INFO] Found Python at: %%D\python.exe
        echo.
        "%%D\python.exe" run.py
        goto end
    )
)

for /d %%D in ("C:\Program Files (x86)\Python*") do (
    if exist "%%D\python.exe" (
        echo [INFO] Found Python at: %%D\python.exe
        echo.
        "%%D\python.exe" run.py
        goto end
    )
)

:: If Python was not located
echo ========================================================
echo  [ERROR] Python was not found on your system!
echo ========================================================
echo.
echo Please follow these quick steps:
echo.
echo 1. Disable Windows App Execution Aliases:
echo    - Open Windows Start Menu and type: "App execution aliases"
echo    - Turn OFF the switches for "App Installer: python.exe" and "python3.exe"
echo.
echo 2. If Python is not yet installed:
echo    - Download Python from: https://www.python.org/downloads/
echo    - IMPORTANT: Check the box "Add python.exe to PATH" during installation.
echo.
pause

:end
