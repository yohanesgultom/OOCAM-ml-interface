@echo off

rem Check if any existing python installed and configured in path
for /f "delims=" %%V in ('python --version') do SET EXISTING_PYTHON=%%V

if "%EXISTING_PYTHON:~0,8%" == "Python 3" (
	goto USE_EXISTING
) else (
	goto DOWNLOAD_INSTALL
)

rem ============================== DOWNLOAD_INSTALL ===============================

:DOWNLOAD_INSTALL

rem Try to download and install python in specific path

set PYTHON_VERSION=3.7.7
set PYTHON_MSI=python-%PYTHON_VERSION%-amd64.exe 
set PYTHON_HOME=c:\python37
set PYTHON_EXE=%PYTHON_HOME%\python.exe
set PYTHON_SCRIPTS=%PYTHON_HOME%\Scripts
set PYTHON_PIP_EXE=%PYTHON_SCRIPTS%\pip3.7.exe
set PYTHON_VIRTUALENV_EXE=%PYTHON_SCRIPTS%\virtualenv.exe

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
	echo Installing Python...
	echo ------------------------------------------------------------------
	echo,

	if exist %PYTHON_MSI% (
		rem if an exact version is installed, uninstall it quietly
		%PYTHON_MSI% /uninstall /quiet
		%PYTHON_MSI% /quiet InstallAllUsers=1 TargetDir=%PYTHON_HOME% Include_pip=1
	) else (
		echo Python installer package didn't seem to download correctly.
		exit /b 1
	)
)
goto SETUP_VIRTUALENV

rem ============================== USE_EXISTING ===============================

:USE_EXISTING

rem Try to use python in system PATH
echo %EXISTING_PYTHON% found in system PATH
set PYTHON_EXE=python.exe
set PYTHON_PIP_EXE=pip.exe
set PYTHON_VIRTUALENV_EXE=virtualenv.exe
goto SETUP_VIRTUALENV

rem ============================== SETUP_VIRTUALENV ===============================

:SETUP_VIRTUALENV

echo,
echo ------------------------------------------------------------------
echo Installing virtualenv...
echo ------------------------------------------------------------------
echo,
%PYTHON_PIP_EXE% install virtualenv

if not exist venv\Scripts\activate (
	echo,
	echo ------------------------------------------------------------------
	echo Creating virtual environment...
	echo ------------------------------------------------------------------
	echo,

	%PYTHON_VIRTUALENV_EXE% venv -p %PYTHON_EXE%
)

echo,
echo ------------------------------------------------------------------
echo Installing dependencies...
echo ------------------------------------------------------------------
echo,

venv\Scripts\pip install -r requirements.txt

echo Installation completed!