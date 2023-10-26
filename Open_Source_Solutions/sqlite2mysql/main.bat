@echo off
if not exist env (
    echo Creating virtual environment...
    python -m venv env
    echo.

    echo Activating virtual environment...
    call env\Scripts\activate

    echo Updating pip...
    python -m pip install --upgrade pip

    call env\Scripts\deactivate
)
call env\Scripts\activate
pip install -r requirements.txt | find /V "already satisfied"

python main.py %*