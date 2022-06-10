@echo off
call %cd%\venv\Scripts\activate

python config.py %*

pause