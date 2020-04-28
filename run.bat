@echo off

set WINPYTHON_HOME=WPy64-3770
set PYTHON_HOME=%WINPYTHON_HOME%\python-3.7.7.amd64
set PYTHON=%PYTHON_HOME%\python.exe

if exist %WINPYTHON_HOME% (
    call %WINPYTHON_HOME%\scripts\env.bat 
    python flaskInterface.py
)
