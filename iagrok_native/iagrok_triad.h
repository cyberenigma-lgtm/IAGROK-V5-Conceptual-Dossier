/* ============================================================================ */
/* IAGROK NATIVE C99 - COGNITIVE TRIAD ENGINE (3 CEREBROS: ALPHA, BETA, GAMMA)   */
/* 100% ANSI C99 - Real Systems Telemetry & Resilient Automated Failover        */
/* ============================================================================ */

#ifndef IAGROK_TRIAD_H
#define IAGROK_TRIAD_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "iagrok_types.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    char id[32];
    char nombre[64];
    char disco[64];
    char tier[64];
    char estado[32];     /* "ONLINE", "DEGRADED", "STANDBY_ACTIVE", "FAILOVER_TAKING_OVER" */
    char salud[32];      /* "OPTIMO", "OVERLOADED" */
    uint32_t ops_sec;
    double latencia_ms;
    double cpu_pct;
    double ram_mb;
    bool failover_activo;
    uint64_t last_heartbeat;
} IagrokBrainNode;

typedef struct {
    char timestamp[16];
    uint32_t alpha_ops;
    uint32_t beta_ops;
    uint32_t gamma_ops;
    uint32_t total_flujo;
} IagrokFlowSnapshot;

/* Initialize the 3 Cerebros subsystem */
void iagrok_triad_init(void);

/* Pre-warm and leave all 3 Cerebros in semi-active ready state */
void iagrok_triad_warmup(void);

/* Update internal node metrics from real Win32 hardware telemetry */
void iagrok_triad_update(void);

/* Generate full JSON telemetry matching dashboard expectations */
bool iagrok_triad_get_telemetry_json(char *out_json, size_t max_len);

/* Toggle failover simulation for testing Cerebro Gamma */
bool iagrok_triad_toggle_failover(bool *out_new_state, char *out_msg, size_t max_msg);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_TRIAD_H */
