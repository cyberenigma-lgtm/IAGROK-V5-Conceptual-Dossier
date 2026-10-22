/* ============================================================================ */
/* IAGROK NATIVE C99 - FILE SYSTEM & PROGRAMMING ENVIRONMENT EXECUTION ENGINE    */
/* 100% ANSI C99 - Real Win32 File Tree, Source I/O, Compilers & Runners        */
/* ============================================================================ */

#ifndef IAGROK_FS_H
#define IAGROK_FS_H

#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Build recursive JSON file tree of workspace */
bool iagrok_fs_tree_json(const char *root_path, int max_depth, char *out_json, size_t max_out);

/* Read source file contents into heap buffer (caller must free *out_content) */
bool iagrok_fs_read(const char *filepath, char **out_content, size_t *out_len);

/* Write or create source file with automatic parent directory creation */
bool iagrok_fs_write(const char *filepath, const char *content);

/* Compile and execute source files (.c, .cpp, .rs, .bat, .ps1, .py, .js) */
bool iagrok_fs_execute(const char *filepath,
                       char *out_stdout, size_t max_out,
                       char *out_stderr, size_t max_err,
                       int *out_exit_code);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_FS_H */
