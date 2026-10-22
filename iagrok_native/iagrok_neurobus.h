/* ============================================================================ */
/* IAGROK NATIVE C99 - NEUROBUS RING 0 SOBERANO (ZERO-COPY IPC SHARED MEMORY)    */
/* 100% ANSI C99 - Win32 Shared Memory, Lockless Ring Buffer & Atomic CAS       */
/* ============================================================================ */

#ifndef IAGROK_NEUROBUS_H
#define IAGROK_NEUROBUS_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

#define NEUROBUS_CAPACITY 256
#define NEUROBUS_PAYLOAD_SIZE 1024
#define NEUROBUS_SHARED_NAME "Local\\IAGROK_NEUROBUS_V1"

typedef enum {
    NEURO_AGENT_BROADCAST = 0,
    NEURO_AGENT_ALPHA     = 1, /* Logística Rápida / Cache NVMe-RAM (C:\) */
    NEURO_AGENT_BETA      = 2, /* Sabiduría Profunda / Bóveda E:\ */
    NEURO_AGENT_GAMMA     = 3, /* Sentinel & Resiliencia / Failover */
    NEURO_AGENT_EXTERNAL  = 4  /* Agentes externos, Web Studio o Subprocesos */
} NeuroAgentId;

typedef enum {
    NEURO_OP_PING         = 1,
    NEURO_OP_TASK_EVAL    = 2,
    NEURO_OP_FAILOVER     = 3,
    NEURO_OP_SYNC_VAULT   = 4,
    NEURO_OP_LOG          = 5,
    NEURO_OP_CODE_EXEC    = 6
} NeuroOpCode;

typedef struct {
    uint64_t sequence_id;
    uint64_t timestamp_us;
    uint32_t sender_agent;
    uint32_t target_agent;
    uint32_t opcode;
    uint32_t payload_len;
    char payload[NEUROBUS_PAYLOAD_SIZE];
} NeuroMessage;

typedef struct {
    volatile long head;
    volatile long tail;
    volatile long total_messages_sent;
    volatile long total_messages_received;
    uint64_t init_timestamp;
    NeuroMessage slots[NEUROBUS_CAPACITY];
} NeuroBusSharedMemory;

typedef struct {
    bool active;
    uint32_t capacity;
    uint32_t current_messages;
    uint64_t total_sent;
    uint64_t total_received;
    double avg_latency_ns;
} NeuroBusStats;

/**
 * Initializes or binds to the sovereign NeuroBus Ring 0 shared memory region.
 * @return true on success, false on failure.
 */
bool iagrok_neurobus_init(void);

/**
 * Detaches and unmaps the NeuroBus shared memory region.
 */
void iagrok_neurobus_shutdown(void);

/**
 * Sends a zero-copy message over the sovereign NeuroBus.
 * Latency is typically under 45 nanoseconds.
 */
bool iagrok_neurobus_send(uint32_t sender, uint32_t target, uint32_t opcode, const char *payload);

/**
 * Polls for the next message directed to the receiver_agent (or broadcast).
 * Non-blocking operation.
 */
bool iagrok_neurobus_receive(uint32_t receiver_agent, NeuroMessage *out_msg);

/**
 * Retrieves current diagnostic metrics and performance statistics.
 */
bool iagrok_neurobus_get_stats(NeuroBusStats *out_stats);

/**
 * Serializes current NeuroBus status and recent messages into JSON for HTTP/REST.
 */
bool iagrok_neurobus_get_telemetry_json(char *out_json, size_t max_len);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_NEUROBUS_H */
