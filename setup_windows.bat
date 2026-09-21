@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3.14 -m venv .venv 2>nul || py -m venv .venv
) else (
  python -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup complete.
echo Set OPENAI_API_KEY in Windows, then run start_windows.bat.
pause
