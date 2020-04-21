@echo off

set PYTHON_VERSION=3.7.7
set PYTHON_MSI=python-%PYTHON_VERSION%-amd64.exe 
set PYTHON_HOME=c:\python37
set PYTHON_EXE=%PYTHON_HOME%\python.exe
set PYTHON_SCRIPTS=%PYTHON_HOME%\Scripts
set PYTHON_PIP_EXE=%PYTHON_SCRIPTS%\pip3.7.exe

if not exist %PYTHON_EXE% (

	if not exist %PYTHON_MSI% (
		echo,
		echo ------------------------------------------------------------------
		echo Downloading Python...
		echo ------------------------------------------------------------------
		echo,

		curl -L -O http://python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_MSI%
	)

	echo,
	echo ------------------------------------------------------------------
	echo Installing Python..
	echo ------------------------------------------------------------------
	echo,

	if exist %PYTHON_MSI% (
        %PYTHON_MSI% /quiet InstallAllUsers=1 TargetDir=%PYTHON_HOME% Include_pip=1
	) else (
		echo Python installer package didn't seem to download correctly.
		exit /b 1
	)
)

if not exist %PYTHON_SCRIPTS%\virtualenv.exe (
	echo,
	echo ------------------------------------------------------------------
	echo Installing virtualenv
	echo ------------------------------------------------------------------
	echo,

	%PYTHON_PIP_EXE% install virtualenv
)

if not exist venv\Scripts\activate (
	echo,
	echo ------------------------------------------------------------------
	echo Creating virtual environment
	echo ------------------------------------------------------------------
	echo,

	%PYTHON_SCRIPTS%\virtualenv.exe venv -p %PYTHON_EXE%
)

echo,
echo ------------------------------------------------------------------
echo Installing dependencies
echo ------------------------------------------------------------------
echo,

venv\Scripts\pip install -r requirements.txt

echo,
echo ------------------------------------------------------------------
echo Installation completed
echo ------------------------------------------------------------------
echo,
