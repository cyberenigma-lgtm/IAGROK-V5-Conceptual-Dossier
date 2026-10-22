/* ============================================================================ */
/* IAGROK NATIVE C99 - SOVEREIGN VAULT & AUTONOMOUS WEB ASSIMILATION ENGINE    */
/* 100% ANSI C99 - WinINet HTTPS, Sovereign Vault Ingestion, Vector Synthesis    */
/* ============================================================================ */

#ifndef IAGROK_BOVEDA_H
#define IAGROK_BOVEDA_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Initialize Sovereign Vault directories and cache */
bool iagrok_boveda_init(void);

/* Native WinINet HTTPS Web Search (Wikipedia Open API & Scientific Repositories) */
bool iagrok_web_search(const char *query, char *out_results, size_t max_results);

/* Assimilate knowledge into Sovereign Vault (C: Primary + E:/G: Dynamic Hot Replicas) */
bool iagrok_boveda_assimilate(const char *topic, const char *source_text, char *out_json, size_t max_out);

/* Telemetry and document statistics of the Sovereign Vault */
bool iagrok_boveda_get_stats_json(char *out_json, size_t max_out);

/* Total document count across primary vault and external library E:\ */
uint32_t iagrok_boveda_get_total_docs_count(void);

/* Resolve query from local Sovereign Library (E:\ & C:\) or on-demand assimilate via WinINet */
bool iagrok_boveda_resolve_or_assimilate(const char *query, char *out_text, size_t max_text, char *out_source, size_t max_source, bool *out_assimilated);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_BOVEDA_H */
