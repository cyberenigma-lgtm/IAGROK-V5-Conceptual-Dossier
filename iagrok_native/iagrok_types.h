/* ============================================================================ */
/* IAGROK NATIVE C99 SYSTEMS ENGINE - CORE TYPES & SPECIFICATIONS              */
/* 100% ANSI C99 - Zero Python Runtime - High-Performance Local Architecture   */
/* Author: cyberenigma-lgtm (Noxferion) -- Systems Architect                   */
/* ============================================================================ */

#ifndef IAGROK_TYPES_H
#define IAGROK_TYPES_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define IAGROK_VERSION_STRING "5.5.0-C99-NATIVE"
#define IAGROK_DEFAULT_PORT 5000
#define IAGROK_MAX_CLIENTS 64
#define IAGROK_BUFFER_SIZE 65536
#define IAGROK_MAX_PATH_LEN 512
#define IAGROK_AUTHORITY_SEAL "0x4359454E"

/* HTTP Request Methods */
typedef enum {
    HTTP_METHOD_UNKNOWN = 0,
    HTTP_METHOD_GET,
    HTTP_METHOD_POST,
    HTTP_METHOD_OPTIONS,
    HTTP_METHOD_HEAD
} HttpMethod;

/* HTTP Request Parsed Structure */
typedef struct {
    HttpMethod method;
    char path[IAGROK_MAX_PATH_LEN];
    char query[IAGROK_MAX_PATH_LEN];
    char content_type[128];
    size_t content_length;
    char *body;
} HttpRequest;

/* Hardware Telemetry Structure */
typedef struct {
    double total_ram_gb;
    double free_ram_gb;
    double used_ram_gb;
    uint32_t ram_usage_percent;
    double process_working_set_mb;
    double process_peak_working_set_mb;
    double cpu_usage_percent;
    double total_disk_gb;
    double free_disk_gb;
} IagrokHardwareStats;

/* Vector Embedding and Search Structures */
typedef struct {
    uint32_t id;
    float score; /* Cosine similarity score [-1.0, 1.0] */
} IagrokKnnResult;

typedef struct {
    size_t dimension;
    size_t count;
    float *data; /* Continuous array of floats (count * dimension) */
} IagrokVectorDatabase;

#endif /* IAGROK_TYPES_H */
