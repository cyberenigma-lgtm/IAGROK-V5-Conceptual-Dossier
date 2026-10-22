/* ============================================================================ */
/* IAGROK NATIVE C99 - HARDWARE TELEMETRY & MEMORY OPTIMIZATION               */
/* ============================================================================ */

#ifndef IAGROK_HARDWARE_H
#define IAGROK_HARDWARE_H

#include "iagrok_types.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Retrieve exact real-time hardware telemetry from Windows Win32 API */
bool iagrok_get_hardware_stats(IagrokHardwareStats *stats);

/* Physically purge and trim working set RAM of the current process */
/* Returns the amount of megabytes trimmed from working set */
double iagrok_purge_working_set(void);

/* Physically purge working sets across all accessible system processes (Win32 Toolhelp) */
/* Returns the number of processes successfully trimmed */
size_t iagrok_purge_all_processes_working_set(void);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_HARDWARE_H */
