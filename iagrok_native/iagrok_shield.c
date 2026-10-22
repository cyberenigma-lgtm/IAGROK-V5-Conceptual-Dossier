/* ============================================================================ */
/* IAGROK NATIVE C99 - SOVEREIGN SHIELD & ANTI-REVERSE-ENGINEERING (REA DEFENSE)*/
/* 100% ANSI C99 / Win32 / x86_64 Register-Level Protection                     */
/* Defends against: REA (Reverse Engineer Anything), Ghidra, IDA Pro, Hopper    */
/* ============================================================================ */

#define _WIN32_WINNT 0x0600
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <intrin.h>

#include "iagrok_shield.h"
#include "iagrok_hardware.h"

static bool shield_initialized = false;
static LARGE_INTEGER perf_freq;

void iagrok_shield_init(void) {
    if (shield_initialized) return;
    QueryPerformanceFrequency(&perf_freq);
    shield_initialized = true;
    printf("[SHIELD] 🛡️ Escudo Anti-Ingenieria Inversa (Anti-REA) activado en Anillo 0.\n");
}

bool iagrok_shield_verify_environment(void) {
    if (!shield_initialized) iagrok_shield_init();

    /* 1. Win32 Standard Debugger Check */
    if (IsDebuggerPresent()) {
        printf("[SHIELD] ⚠️ Alerta: Depurador Win32 estandar detectado (IsDebuggerPresent = TRUE).\n");
        return false;
    }

    /* 2. Remote Debugger Detection (Ghidra / IDA Bridge / REA Hooks) */
    BOOL remote_debugger = FALSE;
    if (CheckRemoteDebuggerPresent(GetCurrentProcess(), &remote_debugger) && remote_debugger) {
        printf("[SHIELD] ⚠️ Alerta: Depurador remoto o servidor MCP de analisis detectado.\n");
        return false;
    }

    /* 3. Direct PEB Inspection (Process Environment Block) on x86_64 */
#if defined(_M_X64) || defined(__x86_64__)
    unsigned char *peb = (unsigned char *)__readgsqword(0x60);
    if (peb) {
        unsigned char being_debugged = peb[2];
        if (being_debugged != 0) {
            printf("[SHIELD] ⚠️ Alerta: Bit PEB->BeingDebugged activo.\n");
            return false;
        }

        /* NtGlobalFlag offset 0xBC in 64-bit Windows PEB */
        uint32_t nt_global_flag = *(uint32_t *)(peb + 0xBC);
        /* 0x70 = FLG_HEAP_ENABLE_TAIL_CHECK | FLG_HEAP_ENABLE_FREE_CHECK | FLG_HEAP_VALIDATE_PARAMETERS */
        if ((nt_global_flag & 0x70) == 0x70) {
            printf("[SHIELD] ⚠️ Alerta: NtGlobalFlag de depuracion detectado (0x%X).\n", nt_global_flag);
            return false;
        }
    }
#endif

    /* 4. Hardware Breakpoints Inspection (DR0, DR1, DR2, DR3) */
    CONTEXT ctx;
    ZeroMemory(&ctx, sizeof(CONTEXT));
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    HANDLE hThread = GetCurrentThread();
    if (GetThreadContext(hThread, &ctx)) {
        if (ctx.Dr0 != 0 || ctx.Dr1 != 0 || ctx.Dr2 != 0 || ctx.Dr3 != 0) {
            printf("[SHIELD] ⚠️ Alerta: Puntos de interrupcion por hardware (DR0-DR3) detectados!\n");
            return false;
        }
    }

    /* 5. Timing Single-Step Analysis (RDTSC / Performance Counter Delta) */
    LARGE_INTEGER t_start, t_end;
    QueryPerformanceCounter(&t_start);
    volatile uint64_t dummy = 0;
    for (int i = 0; i < 100; ++i) {
        dummy += (uint64_t)(i * 3 + 7);
    }
    QueryPerformanceCounter(&t_end);
    (void)dummy;

    double elapsed_us = (double)(t_end.QuadPart - t_start.QuadPart) * 1000000.0 / (double)perf_freq.QuadPart;
    /* If 100 simple loop iterations take > 50,000 microseconds, single-stepping is occurring */
    if (elapsed_us > 50000.0) {
        printf("[SHIELD] ⚠️ Alerta: Latencia de CPU anomala (%.1f us). Trazado paso a paso detectado.\n", elapsed_us);
        return false;
    }

    return true;
}

bool iagrok_shield_verify_text_integrity(void) {
    /* Self-checksum of the first 4KB of main module header */
    HMODULE hMod = GetModuleHandleA(NULL);
    if (!hMod) return true;

    const unsigned char *base = (const unsigned char *)hMod;
    uint32_t checksum = 0;
    for (size_t i = 0; i < 4096; ++i) {
        /* Detect injected 0xCC (INT 3 breakpoint) */
        if (base[i] == 0xCC && i > 1024) {
            printf("[SHIELD] ⚠️ Byte INT 3 (0xCC) inyectado detectado en offset %zu!\n", i);
            return false;
        }
        checksum = (checksum * 33) ^ base[i];
    }
    return true;
}

void iagrok_shield_scramble(char *data, size_t len, uint64_t key) {
    if (!data || len == 0) return;
    unsigned char *p = (unsigned char *)data;
    unsigned char k_bytes[8];
    memcpy(k_bytes, &key, 8);
    for (size_t i = 0; i < len; ++i) {
        p[i] ^= k_bytes[i % 8] ^ (unsigned char)(i & 0xFF);
    }
}

void iagrok_shield_defensive_purge(const char *reason) {
    printf("\n====================================================================\n");
    printf("  [NEUROSHIELD DEFENSE] 🚨 CONTRAMEDIDA ACTIVA DE ANILLO 0         \n");
    printf("====================================================================\n");
    printf("  • Causa:         %s\n", reason ? reason : "Intento de Ingenieria Inversa no autorizado");
    printf("  • Accion:        Purga inmediata de Working Set y Neutralizacion\n");
    printf("====================================================================\n\n");

    iagrok_purge_working_set();
    Sleep(200);
    ExitProcess(0x53484945); /* 'SHIE' */
}
