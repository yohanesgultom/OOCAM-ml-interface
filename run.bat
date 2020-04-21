@echo off

if exist venv\Scripts\python.exe (
	echo,
	echo ------------------------------------------------------------------
	echo Running with virtual environment
	echo ------------------------------------------------------------------
	echo,

	venv\Scripts\python.exe flaskInterface.py
) else (
    echo No virtual environment found. Please run installer.bat first
)
