#ifndef IAGROK_OPS_H
#define IAGROK_OPS_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Executes a 100% ANSI C99 / Win32 native cleanup and pruning of residual files,
 * eliminating auto-generated junk, duplicate staging files, and Python cache remnants.
 * 
 * @param out_files_removed Pointer to receive the count of removed files (optional).
 * @param out_bytes_freed Pointer to receive the total bytes freed (optional).
 * @return true on success, false on failure.
 */
bool iagrok_ops_clean_system(uint64_t *out_files_removed, uint64_t *out_bytes_freed);

/**
 * Creates a high-speed native sovereign backup of critical IAGROK core assets,
 * generating a verified directory snapshot and integrity manifest in milliseconds.
 * 
 * @param backup_root Base directory where backups are stored (e.g. "backups").
 * @param out_target_path Buffer to receive the created backup destination path.
 * @param max_path_len Maximum capacity of out_target_path buffer.
 * @return true on success, false on failure.
 */
bool iagrok_ops_backup_system(const char *backup_root, char *out_target_path, size_t max_path_len);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_OPS_H */
