@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Setting environment variables...
set BASE_URL=https://api.deepseek.com
set MODEL=deepseek-chat
set API_KEY=DeepSeek-API-Key
set MAX_CHAR=2048

echo Running the paper grammar correction program...
python src\main.py

pause
