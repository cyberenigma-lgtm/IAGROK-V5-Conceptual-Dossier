/* ============================================================================ */
/* IAGROK NATIVE C99 - AUTONOMOUS AGENT (AUTO-IMPLEMENT & SELF-DEBUGGING)      */
/* 100% ANSI C99 - Real GCC Compilation, AST Patching & SSE Streaming Stream   */
/* ============================================================================ */

#ifndef IAGROK_AGENT_H
#define IAGROK_AGENT_H

#include <stdbool.h>
#include <stddef.h>
#include <winsock2.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Executes an autonomous Auto-Implementation and Self-Debugging task.
 * Synthesizes code, writes it to disk, compiles it with GCC, analyzes errors,
 * auto-debugs and auto-patches until clean exit, streaming real-time SSE.
 *
 * @param task_json The incoming JSON request (e.g. {"task": "crea un servidor UDP"})
 * @param client_sock Connected client socket for SSE event delivery.
 * @return true on success, false on failure.
 */
bool iagrok_agent_run_task(const char *task_json, SOCKET client_sock);

/**
 * Starts the autonomous background initiative thread (Iniciativa Propia).
 * Periodically verifies sandbox modules, scans for compilation errors,
 * auto-debugs in the background, and devours/crystallizes verified patterns.
 */
void iagrok_agent_start_initiative_loop(void);

/**
 * Stops the autonomous background initiative thread.
 */
void iagrok_agent_stop_initiative_loop(void);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_AGENT_H */
