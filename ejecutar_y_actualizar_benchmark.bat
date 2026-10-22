@echo off
chcp 65001 > nul
title IAGROK DVTRGAS-30 — BENCHMARK NATIVO C99 (ZERO PYTHON)

echo ===========================================================================
echo 🚀 EJECUTANDO BENCHMARK NATIVO C99 AVX2/FMA SIMD (153.6 MFLOP)
echo ===========================================================================
echo.

cd /d "C:\IAGROK"

if not exist "iagrok_server.exe" (
    call "iagrok_native\build.bat"
)

iagrok_server.exe --bench-simd 100000 1536

echo.
echo ===========================================================================
echo 📊 PROCESO FINALIZADO CON ÉXITO (100%% ANSI C99 / 0%% PYTHON)
echo ===========================================================================
echo.
pause
