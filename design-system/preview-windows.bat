@echo off
REM SuperCat Design System — local preview launcher (Windows)
REM Double-click this file to start a local server and open the system in your browser.

cd /d "%~dp0"
set PORT=8765

echo.
echo  +----------------------------------------------+
echo  ^|  SuperCat Design System -- Preview           ^|
echo  ^|  Serving at http://localhost:%PORT%/            ^|
echo  ^|  Press Ctrl+C to stop.                       ^|
echo  +----------------------------------------------+
echo.

REM Open the browser shortly after the server starts.
start "" "http://localhost:%PORT%/index.html"

REM Try Python 3 first, then Python 2 (rare).
where python >nul 2>&1
if %errorlevel%==0 (
  python -m http.server %PORT% --bind 127.0.0.1
  goto :eof
)
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 -m http.server %PORT% --bind 127.0.0.1
  goto :eof
)

echo Python is required to run the local server.
echo Install Python from https://python.org, or just open index.html directly.
pause
