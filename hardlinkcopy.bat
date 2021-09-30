@echo off
set scriptdir=%~dp0
set pythonpath="%scriptdir%\Python37\python.exe"

if exist %pythonpath% (
	rem Use embedded python
) else (
	rem Use Python install
	set pythonpath="python"
)

:: Run script
%pythonpath% "%scriptdir%\program.py" %1

timeout 3
