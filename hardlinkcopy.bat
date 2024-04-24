@echo off
TITLE Python Hard Link Copier v 1.1
setlocal enabledelayedexpansion

set scriptdir=%~dp0
set pythonpath="%scriptdir%\Python37\python.exe"
set hardlink="%scriptdir%\program.py"

if exist %pythonpath% (
    rem Use embedded python
) else (
    rem Use Python install
    set pythonpath="python"
)

if "%~1" == "" (
    color 04
    echo Drag ^& Drop folders or loose files over this script to make copy using hardlinks
    timeout 5
    exit /b
)

:loop
if "%~1" neq "" (
    if exist "%~f1\" (
        %pythonpath% %hardlink% "%~f1"
    ) else (
        %pythonpath% %hardlink% "%~f1"
    )
    shift
    goto loop
)
timeout 5
