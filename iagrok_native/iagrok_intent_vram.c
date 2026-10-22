/* ============================================================================ */
/* IAGROK NATIVE C99 - INTENT ARBITER & MULTI-CHANNEL HYBRID VRAM (GXNOX)     */
/* Co-Diseño de Jerarquía de Memoria: RAM Física Inmediata + VRAM en SSD      */
/* con Rotación Anti-Desgaste de Silicio (Software Wear-Leveling Ring)         */
/* Author: José Manuel Moreno (JMM) (JMMC)                                       */
/* ============================================================================ */

#define _WIN32_WINNT 0x0600
#include <windows.h>
#include <psapi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "iagrok_intent_vram.h"

static HANDLE g_vram_file = INVALID_HANDLE_VALUE;
static char g_container_path[MAX_PATH] = {0};
static uint64_t g_vram_capacity_bytes = 0;
static uint64_t g_vram_total_blocks = 0;
static uint64_t g_ring_head_offset = 4096; /* Offset inicial después de cabecera LBA */
static uint32_t g_wear_cycles = 0;
static uint64_t g_stat_immediate_ram = 0;
static uint64_t g_stat_extended_vram = 0;
static CRITICAL_SECTION g_vram_lock;
static bool g_initialized = false;

/* Inicializar contenedor VRAM GXNOX con rotación de silicio */
bool iagrok_vram_init(const char *container_path, uint64_t size_gb) {
    if (g_initialized) return true;
    InitializeCriticalSection(&g_vram_lock);

    if (container_path && strlen(container_path) > 0) {
        strncpy(g_container_path, container_path, sizeof(g_container_path) - 1);
    } else {
        strncpy(g_container_path, DEFAULT_VRAM_CONTAINER, sizeof(g_container_path) - 1);
    }

    if (size_gb == 0) size_gb = 4; /* Default 4 GB de VRAM de procesamiento */
    g_vram_capacity_bytes = size_gb * 1024ULL * 1024ULL * 1024ULL;
    g_vram_total_blocks = g_vram_capacity_bytes / GXNOX_VRAM_BLOCK_SIZE;

    /* Asegurar que existe directorio padre */
    char dir_buf[MAX_PATH];
    strncpy(dir_buf, g_container_path, sizeof(dir_buf) - 1);
    char *last_slash = strrchr(dir_buf, '\\');
    if (last_slash) {
        *last_slash = '\0';
        CreateDirectoryA(dir_buf, NULL);
    }

    /* Abrir o crear contenedor contiguo con acceso directo a disco */
    g_vram_file = CreateFileA(
        g_container_path,
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ,
        NULL,
        OPEN_ALWAYS,
        FILE_ATTRIBUTE_NORMAL | FILE_FLAG_RANDOM_ACCESS,
        NULL
    );

    if (g_vram_file == INVALID_HANDLE_VALUE) {
        return false;
    }

    /* Pre-reserva contigua de tamaño si es nuevo */
    LARGE_INTEGER cur_sz;
    GetFileSizeEx(g_vram_file, &cur_sz);
    if ((uint64_t)cur_sz.QuadPart < g_vram_capacity_bytes) {
        LARGE_INTEGER li;
        li.QuadPart = (LONGLONG)g_vram_capacity_bytes;
        SetFilePointerEx(g_vram_file, li, NULL, FILE_BEGIN);
        SetEndOfFile(g_vram_file);

        /* Escribir cabecera mágica Sector 0 */
        SetFilePointer(g_vram_file, 0, NULL, FILE_BEGIN);
        uint8_t sector0[4096];
        memset(sector0, 0, sizeof(sector0));
        *(uint32_t*)(sector0 + 0) = GXNOX_VRAM_MAGIC; /* "GXNX" */
        *(uint32_t*)(sector0 + 4) = 3;                /* Versión 3 */
        *(uint64_t*)(sector0 + 8) = (uint64_t)time(NULL);
        *(uint64_t*)(sector0 + 16) = g_vram_capacity_bytes;
        *(uint32_t*)(sector0 + 24) = 0x434D4D4A;     /* "JMMC" */
        DWORD written;
        WriteFile(g_vram_file, sector0, sizeof(sector0), &written, NULL);
    }

    g_ring_head_offset = 4096;
    g_wear_cycles = 0;
    g_initialized = true;
    return true;
}

void iagrok_vram_shutdown(void) {
    if (!g_initialized) return;
    EnterCriticalSection(&g_vram_lock);
    if (g_vram_file != INVALID_HANDLE_VALUE) {
        CloseHandle(g_vram_file);
        g_vram_file = INVALID_HANDLE_VALUE;
    }
    g_initialized = false;
    LeaveCriticalSection(&g_vram_lock);
    DeleteCriticalSection(&g_vram_lock);
}

/* Evaluador de Intenciones en Tiempo Constante O(1) */
IagrokIntentAnalysis iagrok_evaluate_intent(const char *query_or_task, size_t payload_len) {
    IagrokIntentAnalysis result;
    memset(&result, 0, sizeof(result));
    result.estimated_payload_bytes = payload_len;

    if (!query_or_task) {
        result.target = INTENT_DISPATCH_IMMEDIATE_RAM;
        result.estimated_compute_ms = 0.5;
        snprintf(result.reason, sizeof(result.reason), "Consulta nula: bypass directo a RAM");
        return result;
    }

    size_t qlen = strlen(query_or_task);

    /* Heurística 1: Tareas interactivas inmediatas de baja carga */
    /* Comandos de estado, hora, preguntas cortas, comprobaciones de hardware */
    bool is_interactive_command = (qlen < 160) && 
        (strstr(query_or_task, "hora") || strstr(query_or_task, "status") || 
         strstr(query_or_task, "ping") || strstr(query_or_task, "azar") ||
         strstr(query_or_task, "bonoloto") || strstr(query_or_task, "ram") ||
         strstr(query_or_task, "hardware") || strstr(query_or_task, "version"));

    /* Heurística 2: Tareas pesadas que saturan RAM en el SO */
    /* Ingesta de documentos, código masivo, asimilación web, RAG profundo, multi-paso */
    bool is_heavy_compute = (payload_len > 16384) || (qlen > 600) ||
        (strstr(query_or_task, "asimil") || strstr(query_or_task, "document") ||
         strstr(query_or_task, "repositorio") || strstr(query_or_task, "benchmark") ||
         strstr(query_or_task, "vector") || strstr(query_or_task, "codigo completo") ||
         strstr(query_or_task, "7 horas") || strstr(query_or_task, "estres"));

    if (is_interactive_command && !is_heavy_compute) {
        result.target = INTENT_DISPATCH_IMMEDIATE_RAM;
        result.estimated_compute_ms = 1.2;
        snprintf(result.reason, sizeof(result.reason), "Interaccion inmediata (DRAM caliente, latencia < 2ms)");
        InterlockedIncrement64((LONG64*)&g_stat_immediate_ram);
    } else {
        result.target = INTENT_DISPATCH_EXTENDED_VRAM;
        result.estimated_compute_ms = 25.0 + ((double)payload_len / 5000.0);
        snprintf(result.reason, sizeof(result.reason), "Carga pesada / extendida: offload a VRAM GXNOX en SSD");
        InterlockedIncrement64((LONG64*)&g_stat_extended_vram);
    }

    return result;
}

/* Escritura en VRAM GXNOX con Anillo de Desgaste Nivelado (Wear-Leveling Ring) */
uint64_t iagrok_vram_write_scratchpad(const void *data, size_t size_bytes) {
    if (!g_initialized || g_vram_file == INVALID_HANDLE_VALUE || !data || size_bytes == 0) {
        return 0;
    }

    EnterCriticalSection(&g_vram_lock);

    /* Alinear escritura a bloque contiguo de 64 bytes */
    size_t aligned_size = (size_bytes + 63ULL) & ~63ULL;

    /* Comprobar si cabe en el espacio restante del anillo o si debe dar la vuelta */
    if (g_ring_head_offset + aligned_size >= g_vram_capacity_bytes) {
        g_ring_head_offset = 4096; /* Reiniciar al inicio del anillo LBA */
        g_wear_cycles++;           /* Ciclo de desgaste nivelado completado */
    }

    uint64_t assigned_offset = g_ring_head_offset;

    LARGE_INTEGER li;
    li.QuadPart = (LONGLONG)assigned_offset;
    SetFilePointerEx(g_vram_file, li, NULL, FILE_BEGIN);

    DWORD bytes_written = 0;
    WriteFile(g_vram_file, data, (DWORD)size_bytes, &bytes_written, NULL);

    /* Avanzar la cabeza del anillo de silicio */
    g_ring_head_offset += aligned_size;

    LeaveCriticalSection(&g_vram_lock);
    return assigned_offset;
}

/* Lectura directa LBA desde la VRAM en SSD */
bool iagrok_vram_read_scratchpad(uint64_t vram_token_offset, void *dest_buffer, size_t size_bytes) {
    if (!g_initialized || g_vram_file == INVALID_HANDLE_VALUE || !dest_buffer || size_bytes == 0) {
        return false;
    }

    if (vram_token_offset < 4096 || vram_token_offset + size_bytes > g_vram_capacity_bytes) {
        return false;
    }

    EnterCriticalSection(&g_vram_lock);

    LARGE_INTEGER li;
    li.QuadPart = (LONGLONG)vram_token_offset;
    SetFilePointerEx(g_vram_file, li, NULL, FILE_BEGIN);

    DWORD bytes_read = 0;
    BOOL ok = ReadFile(g_vram_file, dest_buffer, (DWORD)size_bytes, &bytes_read, NULL);

    LeaveCriticalSection(&g_vram_lock);
    return (ok && bytes_read == (DWORD)size_bytes);
}

/* Telemetría Integrada de Memoria Híbrida */
bool iagrok_get_hybrid_memory_stats(IagrokHybridMemoryStats *stats) {
    if (!stats) return false;
    memset(stats, 0, sizeof(IagrokHybridMemoryStats));

    /* 1. Telemetría de RAM del host */
    MEMORYSTATUSEX mem;
    mem.dwLength = sizeof(mem);
    if (GlobalMemoryStatusEx(&mem)) {
        stats->host_physical_ram_total_gb = (double)mem.ullTotalPhys / (1024.0 * 1024.0 * 1024.0);
        stats->host_physical_ram_used_gb = (double)(mem.ullTotalPhys - mem.ullAvailPhys) / (1024.0 * 1024.0 * 1024.0);
        stats->host_ram_percent = (uint32_t)mem.dwMemoryLoad;
    }

    /* 2. Working set del proceso actual */
    PROCESS_MEMORY_COUNTERS pmc;
    if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
        stats->process_ram_working_set_mb = (double)pmc.WorkingSetSize / (1024.0 * 1024.0);
    }

    /* 3. Métricas de VRAM GXNOX */
    stats->vram_container_size_gb = (double)g_vram_capacity_bytes / (1024.0 * 1024.0 * 1024.0);
    stats->vram_total_blocks = g_vram_total_blocks;
    stats->vram_ring_write_offset_bytes = g_ring_head_offset;
    stats->vram_active_blocks = (g_ring_head_offset - 4096) / GXNOX_VRAM_BLOCK_SIZE;
    stats->wear_level_full_cycles = g_wear_cycles;

    /* 4. Contadores de Despacho */
    stats->count_dispatches_immediate_ram = g_stat_immediate_ram;
    stats->count_dispatches_extended_vram = g_stat_extended_vram;

    return true;
}
