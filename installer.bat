@echo off

set CURL_EXE=curl\curl.exe
set WINPYTHON_INSTALLER=Winpython64-3.7.7.0dot.exe
set WINPYTHON_HOME=WPy64-3770
set PYTHON_HOME=%WINPYTHON_HOME%\python-3.7.7.amd64
set PYTHON=%PYTHON_HOME%\python.exe

if not exist %WINPYTHON_INSTALLER% (
    echo,
    echo ------------------------------------------------------------------
    echo Downloading WinPython...
    echo ------------------------------------------------------------------
    echo,

    %CURL_EXE% -L -O https://github.com/winpython/winpython/releases/download/2.3.20200319/%WINPYTHON_INSTALLER%
)

if not exist %WINPYTHON_HOME% (
    echo,
    echo ------------------------------------------------------------------
    echo Installing WinPython...
    echo ------------------------------------------------------------------
    echo,

    %WINPYTHON_INSTALLER% -o"." -y    
)

if exist %WINPYTHON_HOME% (
    echo,
    echo ------------------------------------------------------------------
    echo Installing dependencies...
    echo ------------------------------------------------------------------
    echo,

    call %WINPYTHON_HOME%\scripts\env.bat 
    pip3 install -r requirements.txt    
)
