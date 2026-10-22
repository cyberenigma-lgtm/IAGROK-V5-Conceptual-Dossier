@echo off
setlocal
title BENCHMARK SIMD AVX2 C99 NATIVO
echo ================================================================================
echo   BENCHMARK EN SILICIO REAL: AVX2/FMA SIMD (100,000 Vectores x 1536 Dims)
echo   (0%% Python / 100%% C99 / Medicion por QueryPerformanceCounter)
echo ================================================================================

cd /d "%~dp0"

if not exist "iagrok_server.exe" (
    call "iagrok_native\build.bat"
)

"iagrok_server.exe" --bench-simd 100000 1536

echo.
pause
