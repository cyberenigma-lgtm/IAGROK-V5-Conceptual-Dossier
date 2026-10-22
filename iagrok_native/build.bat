@echo off
setlocal
echo ====================================================================
echo   COMPILANDO IAGROK NATIVO C99 (ZERO PYTHON / 100%% SISTEMAS)
echo ====================================================================

where gcc >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] No se encontro gcc en el PATH.
    exit /b 1
)

cd /d "%~dp0"

echo [1/8] Compilando iagrok_hardware.c...
gcc -std=c99 -O2 -Wall -Wextra -c iagrok_hardware.c -o iagrok_hardware.o -lpsapi
if %errorlevel% neq 0 goto error

echo [2/8] Compilando iagrok_simd.c (AVX2/FMA)...
gcc -std=c99 -O2 -Wall -Wextra -mavx2 -mfma -c iagrok_simd.c -o iagrok_simd.o
if %errorlevel% neq 0 goto error

echo [3/8] Compilando iagrok_embed.c...
gcc -std=c99 -O2 -Wall -Wextra -mavx2 -mfma -c iagrok_embed.c -o iagrok_embed.o
if %errorlevel% neq 0 goto error

echo [4/8] Compilando iagrok_triad.c (3 Cerebros: Alpha, Beta, Gamma)...
gcc -std=c99 -O2 -Wall -Wextra -c iagrok_triad.c -o iagrok_triad.o
if %errorlevel% neq 0 goto error

echo [5/8] Compilando iagrok_fs.c (File System ^& Code Execution Engine)...
gcc -std=c99 -O2 -Wall -Wextra -c iagrok_fs.c -o iagrok_fs.o
if %errorlevel% neq 0 goto error

echo [6/8] Compilando iagrok_chat.c (Chat ^& RAG Reasoning Engine)...
gcc -std=c99 -O2 -Wall -Wextra -c iagrok_chat.c -o iagrok_chat.o
if %errorlevel% neq 0 goto error

echo [7/9] Compilando iagrok_http.c (Winsock2 REST Server)...
gcc -std=c99 -O2 -Wall -Wextra -c iagrok_http.c -o iagrok_http.o -lws2_32
if %errorlevel% neq 0 goto error

echo [8/10] Compilando iagrok_ops.c (Native Pruning ^& Sovereign Backups)...
gcc -std=c99 -O2 -Wall -Wextra -c iagrok_ops.c -o iagrok_ops.o
if %errorlevel% neq 0 goto error

echo [9/11] Compilando iagrok_agent.c (Autonomous Agent ^& Self-Debugging)...
gcc -std=c99 -O2 -Wall -Wextra -c iagrok_agent.c -o iagrok_agent.o
if %errorlevel% neq 0 goto error

echo [10/12] Compilando iagrok_shield.c (Anti-REA / Anti-Reverse-Engineering Shield)...
gcc -std=c99 -O2 -Wall -Wextra -c iagrok_shield.c -o iagrok_shield.o
if %errorlevel% neq 0 goto error

echo [11/13] Compilando iagrok_neurobus.c (NeuroBus Ring 0 Shared Memory IPC)...
gcc -std=c99 -O2 -Wall -Wextra -c iagrok_neurobus.c -o iagrok_neurobus.o
if %errorlevel% neq 0 goto error

echo [12/13] Compilando iagrok_boveda.c (Sovereign Vault ^& Autonomous Web Assimilation Engine)...
gcc -std=c99 -O2 -Wall -Wextra -c iagrok_boveda.c -o iagrok_boveda.o -lwininet
if %errorlevel% neq 0 goto error

echo [13/13] Compilando y enlazando iagrok_server.exe (Stripped Symbols -s)...
gcc -std=c99 -O2 -Wall -Wextra -mavx2 -mfma -s -Wl,--strip-all iagrok_main.c iagrok_hardware.o iagrok_simd.o iagrok_embed.o iagrok_triad.o iagrok_fs.o iagrok_chat.o iagrok_http.o iagrok_ops.o iagrok_agent.o iagrok_shield.o iagrok_neurobus.o iagrok_boveda.o -o iagrok_server.exe -lws2_32 -lpsapi -lwininet -lm
if %errorlevel% neq 0 goto error

echo.
echo ====================================================================
echo   [OK] COMPILACION EXITOSA: iagrok_server.exe generado
echo ====================================================================
copy /y iagrok_server.exe ..\iagrok_server.exe >nul
echo [OK] Copiado a ..\iagrok_server.exe para ejecucion directa en raiz.
echo.
exit /b 0

:error
echo [ERROR] Fallo la compilacion.
exit /b 1
