/* ============================================================================ */
/* IAGROK NATIVE C99 - HARDWARE TELEMETRY & MEMORY OPTIMIZATION IMPLEMENTATION */
/* ============================================================================ */

#define _WIN32_WINNT 0x0600
#include <windows.h>
#include <psapi.h>
#include <tlhelp32.h>
#include <stdio.h>
#include "iagrok_hardware.h"

/* Static variables to calculate delta CPU usage across calls */
static ULARGE_INTEGER prev_idle_time = {0};
static ULARGE_INTEGER prev_kernel_time = {0};
static ULARGE_INTEGER prev_user_time = {0};
static bool cpu_initialized = false;

static double calculate_cpu_load(void) {
    FILETIME idle, kernel, user;
    if (!GetSystemTimes(&idle, &kernel, &user)) {
        return 0.0;
    }

    ULARGE_INTEGER current_idle, current_kernel, current_user;
    current_idle.LowPart = idle.dwLowDateTime;
    current_idle.HighPart = idle.dwHighDateTime;
    current_kernel.LowPart = kernel.dwLowDateTime;
    current_kernel.HighPart = kernel.dwHighDateTime;
    current_user.LowPart = user.dwLowDateTime;
    current_user.HighPart = user.dwHighDateTime;

    if (!cpu_initialized) {
        prev_idle_time = current_idle;
        prev_kernel_time = current_kernel;
        prev_user_time = current_user;
        cpu_initialized = true;
        return 5.0; /* Initial baseline estimate */
    }

    ULONGLONG delta_idle = current_idle.QuadPart - prev_idle_time.QuadPart;
    ULONGLONG delta_kernel = current_kernel.QuadPart - prev_kernel_time.QuadPart;
    ULONGLONG delta_user = current_user.QuadPart - prev_user_time.QuadPart;
    ULONGLONG total_sys = delta_kernel + delta_user;

    prev_idle_time = current_idle;
    prev_kernel_time = current_kernel;
    prev_user_time = current_user;

    if (total_sys == 0) return 0.0;

    double load = 100.0 - ((double)delta_idle * 100.0 / (double)total_sys);
    if (load < 0.0) load = 0.0;
    if (load > 100.0) load = 100.0;
    return load;
}

bool iagrok_get_hardware_stats(IagrokHardwareStats *stats) {
    if (!stats) return false;
    memset(stats, 0, sizeof(IagrokHardwareStats));

    /* 1. Global RAM Status */
    MEMORYSTATUSEX mem_status;
    mem_status.dwLength = sizeof(mem_status);
    if (GlobalMemoryStatusEx(&mem_status)) {
        stats->total_ram_gb = (double)mem_status.ullTotalPhys / (1024.0 * 1024.0 * 1024.0);
        stats->free_ram_gb = (double)mem_status.ullAvailPhys / (1024.0 * 1024.0 * 1024.0);
        stats->used_ram_gb = stats->total_ram_gb - stats->free_ram_gb;
        stats->ram_usage_percent = (uint32_t)mem_status.dwMemoryLoad;
    }

    /* 2. Process Working Set */
    PROCESS_MEMORY_COUNTERS pmc;
    if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
        stats->process_working_set_mb = (double)pmc.WorkingSetSize / (1024.0 * 1024.0);
        stats->process_peak_working_set_mb = (double)pmc.PeakWorkingSetSize / (1024.0 * 1024.0);
    }

    /* 3. Real CPU Usage Percentage */
    stats->cpu_usage_percent = calculate_cpu_load();

    /* 4. Disk Storage Telemetry */
    ULARGE_INTEGER free_bytes_avail, total_bytes, total_free_bytes;
    if (GetDiskFreeSpaceExA("C:\\", &free_bytes_avail, &total_bytes, &total_free_bytes)) {
        stats->total_disk_gb = (double)total_bytes.QuadPart / (1024.0 * 1024.0 * 1024.0);
        stats->free_disk_gb = (double)total_free_bytes.QuadPart / (1024.0 * 1024.0 * 1024.0);
    }

    return true;
}

double iagrok_purge_working_set(void) {
    HANDLE process = GetCurrentProcess();
    PROCESS_MEMORY_COUNTERS before;
    PROCESS_MEMORY_COUNTERS after;

    memset(&before, 0, sizeof(before));
    memset(&after, 0, sizeof(after));

    GetProcessMemoryInfo(process, &before, sizeof(before));

    /* Physically trim memory working set */
    EmptyWorkingSet(process);
    SetProcessWorkingSetSize(process, (SIZE_T)-1, (SIZE_T)-1);

    GetProcessMemoryInfo(process, &after, sizeof(after));

    double mb_before = (double)before.WorkingSetSize / (1024.0 * 1024.0);
    double mb_after = (double)after.WorkingSetSize / (1024.0 * 1024.0);
    double freed = mb_before - mb_after;
    return (freed > 0.0) ? freed : 0.0;
}

size_t iagrok_purge_all_processes_working_set(void) {
    HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snap == INVALID_HANDLE_VALUE) return 0;

    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(pe);
    size_t count = 0;

    if (Process32First(snap, &pe)) {
        do {
            if (pe.th32ProcessID <= 4) continue;
            HANDLE h = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_SET_QUOTA, FALSE, pe.th32ProcessID);
            if (h) {
                if (EmptyWorkingSet(h)) {
                    count++;
                }
                CloseHandle(h);
            }
        } while (Process32Next(snap, &pe));
    }
    CloseHandle(snap);
    return count;
}
