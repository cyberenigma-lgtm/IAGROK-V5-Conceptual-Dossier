@echo off
setlocal
title TEST DE VERIFICACION 100% REAL - IAGROK C99
echo ================================================================================
echo   EJECUTANDO SUITE DE VERIFICACION 100%% REAL (ZERO MOCKS / ZERO FANTASIA)
echo ================================================================================

cd /d "%~dp0"

if not exist "iagrok_server.exe" (
    call "iagrok_native\build.bat"
)

"iagrok_server.exe" --test

echo.
pause
