/* ============================================================================ */
/* IAGROK NATIVE C99 - INTENT ARBITER & MULTI-CHANNEL HYBRID VRAM (GXNOX)     */
/* Co-Diseño de Jerarquía de Memoria: RAM Física Inmediata + VRAM en SSD      */
/* con Rotación Anti-Desgaste de Silicio (Software Wear-Leveling Ring)         */
/* Author: José Manuel Moreno (JMM) (JMMC)                                       */
/* ============================================================================ */

#ifndef IAGROK_INTENT_VRAM_H
#define IAGROK_INTENT_VRAM_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define GXNOX_VRAM_MAGIC 0x584E5847          /* "GXNX" Little-Endian */
#define GXNOX_VRAM_BLOCK_SIZE 65536          /* 64 KB por bloque contiguo */
#define DEFAULT_VRAM_CONTAINER "C:\\IAGROK\\datos_y_memoria\\gxnox_vram_scratchpad.gxnox"

/* Categorías de Despacho de Intención */
typedef enum {
    INTENT_DISPATCH_IMMEDIATE_RAM = 0, /* Despacho inmediato en DRAM (< 5 ms) */
    INTENT_DISPATCH_EXTENDED_VRAM = 1  /* Carga pesada / Procesamiento extendido en SSD GXNOX */
} IagrokDispatchTarget;

/* Estructura de Análisis de Intención */
typedef struct {
    IagrokDispatchTarget target;
    double estimated_compute_ms;
    size_t estimated_payload_bytes;
    char reason[128];
} IagrokIntentAnalysis;

/* Métricas de Telemetría de Memoria Híbrida */
typedef struct {
    double host_physical_ram_used_gb;
    double host_physical_ram_total_gb;
    uint32_t host_ram_percent;
    double process_ram_working_set_mb;
    
    /* VRAM GXNOX en SSD */
    double vram_container_size_gb;
    uint64_t vram_total_blocks;
    uint64_t vram_active_blocks;
    uint64_t vram_ring_write_offset_bytes;
    uint32_t wear_level_full_cycles;
    
    /* Estadísticas de despacho */
    uint64_t count_dispatches_immediate_ram;
    uint64_t count_dispatches_extended_vram;
} IagrokHybridMemoryStats;

/* Inicialización y Liberación del Subsistema de VRAM Híbrida */
bool iagrok_vram_init(const char *container_path, uint64_t size_gb);
void iagrok_vram_shutdown(void);

/* Evaluador de Intenciones Cognitivas */
IagrokIntentAnalysis iagrok_evaluate_intent(const char *query_or_task, size_t payload_len);

/* Operaciones de Silicio en VRAM GXNOX con Rotación Anti-Desgaste */
uint64_t iagrok_vram_write_scratchpad(const void *data, size_t size_bytes);
bool iagrok_vram_read_scratchpad(uint64_t vram_token_offset, void *dest_buffer, size_t size_bytes);

/* Telemetría */
bool iagrok_get_hybrid_memory_stats(IagrokHybridMemoryStats *stats);

#endif /* IAGROK_INTENT_VRAM_H */
