@echo off
title Dhan Disha launcher
set "DEST=C:\dd"
set "DL=%USERPROFILE%\Downloads"

if not exist "%DEST%" mkdir "%DEST%"
if not exist "%DEST%\.streamlit" mkdir "%DEST%\.streamlit"

rem Find the NEWEST app*.py in Downloads (browsers rename repeats to "app (1).py", "app (2).py", ...)
set "FOUND="
for /f "delims=" %%F in ('dir /b /o-d "%DL%\app*.py" 2^>nul') do (
  if not defined FOUND set "FOUND=%%F"
)
if not defined FOUND (
  echo.
  echo Could not find an app file in your Downloads folder:
  echo %DL%
  echo Download the newest app.py again, then double-click this file again.
  echo.
  pause
  exit /b 1
)

copy /y "%DL%\%FOUND%" "%DEST%\app.py" >nul
echo.
echo Using this file from Downloads: %FOUND%
echo Copied to: %DEST%\app.py
echo.

rem Theme settings, if you downloaded config.toml
if exist "%DL%\config.toml" copy /y "%DL%\config.toml" "%DEST%\.streamlit\config.toml" >nul

rem Reuse your AI key file from the old folder, if it is not already here
if not exist "%DEST%\.streamlit\secrets.toml" (
  for %%S in ("%USERPROFILE%\OneDrive\Desktop\finance app\.streamlit\secrets.toml" "%USERPROFILE%\Desktop\finance app\.streamlit\secrets.toml") do (
    if exist %%S copy /y %%S "%DEST%\.streamlit\secrets.toml" >nul
  )
)

rem Stop any old copy of the app that is still running, so you do not look at a stale page
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":8501 :8502 :8510" ^| findstr LISTENING') do taskkill /f /pid %%P >nul 2>&1

cd /d "%DEST%"
echo Installing or updating the tools. Please wait a minute...
py -m pip install --quiet --upgrade streamlit requests pandas pillow
echo.
echo Starting Dhan Disha. When it opens, the left panel should say Version 14.
echo Keep this window open while you use the app. Press Ctrl+C to stop it.
echo.
py -m streamlit run app.py --server.port 8510
echo.
pause
