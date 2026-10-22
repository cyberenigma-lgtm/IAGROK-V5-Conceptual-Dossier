/* ============================================================================ */
/* IAGROK NATIVE C99 - CHAT & SOVEREIGN REASONING ENGINE                        */
/* 100% ANSI C99 - Real RAG Semantic Search & Tool Execution Dispatcher        */
/* ============================================================================ */

#ifndef IAGROK_CHAT_H
#define IAGROK_CHAT_H

#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Initialize the chat and knowledge corpus */
void iagrok_chat_init(void);

/* Process user chat query and generate JSON response */
/* out_json receives the formatted JSON payload for the UI */
bool iagrok_chat_process(const char *prompt, char *out_json, size_t max_out);

/* Process user chat query and generate Prometheus IDE compatible JSON response */
bool iagrok_chat_process_prometheus(const char *prompt, char *out_json, size_t max_out);

/* Read the chat history from chat_history.json */
bool iagrok_chat_get_history(char **out_json, size_t *out_len);

/* Clear the chat history */
bool iagrok_chat_clear_history(void);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_CHAT_H */
