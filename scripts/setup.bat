@echo off
echo Setting up Multi-Agent System with Hugging Face...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

REM Create necessary directories
if not exist logs mkdir logs
if not exist data mkdir data
if not exist temp mkdir temp
if not exist models mkdir models

REM Copy environment file
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo.
        echo ================================
        echo IMPORTANT: Configure your .env file
        echo Add your Hugging Face API token:
        echo HUGGINGFACE_API_KEY=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
        echo ================================
        echo.
    )
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Get your Hugging Face API token from https://huggingface.co/settings/tokens
echo 2. Add it to your .env file
echo 3. Run 'scripts\run.bat' to start the application
echo.
pause