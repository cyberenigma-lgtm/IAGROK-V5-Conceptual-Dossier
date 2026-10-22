/* ============================================================================ */
/* IAGROK NATIVE C99 - HIGH-PERFORMANCE WINSOCK2 HTTP 1.1 SERVER                */
/* Multithreaded REST API and Zero-Copy Static Asset Engine                     */
/* ============================================================================ */

#ifndef IAGROK_HTTP_H
#define IAGROK_HTTP_H

#include <stdint.h>
#include <stdbool.h>
#include "iagrok_types.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint16_t port;
    const char *web_root;
    bool verbose;
} IagrokServerConfig;

/* Initialize and start the HTTP server (blocking loop) */
int iagrok_http_server_start(const IagrokServerConfig *config);

/* Request server stop */
void iagrok_http_server_stop(void);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_HTTP_H */
