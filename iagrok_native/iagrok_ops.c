/* ============================================================================ */
/* IAGROK NATIVE C99 - SYSTEM OPERATIONS (PRUNING & SOVEREIGN BACKUPS)         */
/* 100% ANSI C99 / Win32 Systems Code - Zero Python Dependencies                */
/* ============================================================================ */

#define _WIN32_WINNT 0x0600
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "iagrok_ops.h"
#include "iagrok_hardware.h"

/* Helper: recursively delete a directory and its contents */
static bool delete_directory_recursive(const char *dir_path, uint64_t *out_files, uint64_t *out_bytes) {
    char search_pattern[1024];
    snprintf(search_pattern, sizeof(search_pattern), "%s\\*", dir_path);

    WIN32_FIND_DATAA fd;
    HANDLE hFind = FindFirstFileA(search_pattern, &fd);
    if (hFind == INVALID_HANDLE_VALUE) return false;

    do {
        if (strcmp(fd.cFileName, ".") == 0 || strcmp(fd.cFileName, "..") == 0) {
            continue;
        }

        char full_path[1024];
        snprintf(full_path, sizeof(full_path), "%s\\%s", dir_path, fd.cFileName);

        if (fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
            delete_directory_recursive(full_path, out_files, out_bytes);
            RemoveDirectoryA(full_path);
        } else {
            uint64_t file_size = ((uint64_t)fd.nFileSizeHigh << 32) | fd.nFileSizeLow;
            if (DeleteFileA(full_path)) {
                if (out_files) (*out_files)++;
                if (out_bytes) (*out_bytes) += file_size;
            }
        }
    } while (FindNextFileA(hFind, &fd));

    FindClose(hFind);
    return RemoveDirectoryA(dir_path) != 0;
}

/* Helper: create directory tree recursively */
static bool create_dir_recursive(const char *path) {
    char temp[1024];
    snprintf(temp, sizeof(temp), "%s", path);
    size_t len = strlen(temp);

    for (size_t i = 1; i < len; ++i) {
        if (temp[i] == '\\' || temp[i] == '/') {
            char slash = temp[i];
            temp[i] = '\0';
            CreateDirectoryA(temp, NULL);
            temp[i] = slash;
        }
    }
    return CreateDirectoryA(temp, NULL) || GetLastError() == ERROR_ALREADY_EXISTS;
}

/* Helper: recursively copy directory */
static bool copy_directory_recursive(const char *src_dir, const char *dst_dir, FILE *manifest, uint64_t *out_files, uint64_t *out_bytes) {
    create_dir_recursive(dst_dir);

    char search_pattern[1024];
    snprintf(search_pattern, sizeof(search_pattern), "%s\\*", src_dir);

    WIN32_FIND_DATAA fd;
    HANDLE hFind = FindFirstFileA(search_pattern, &fd);
    if (hFind == INVALID_HANDLE_VALUE) return false;

    do {
        if (strcmp(fd.cFileName, ".") == 0 || strcmp(fd.cFileName, "..") == 0) {
            continue;
        }

        /* Skip git and temporary caches */
        if (_stricmp(fd.cFileName, ".git") == 0 || _stricmp(fd.cFileName, "__pycache__") == 0) {
            continue;
        }

        char src_path[1024];
        char dst_path[1024];
        snprintf(src_path, sizeof(src_path), "%s\\%s", src_dir, fd.cFileName);
        snprintf(dst_path, sizeof(dst_path), "%s\\%s", dst_dir, fd.cFileName);

        if (fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
            copy_directory_recursive(src_path, dst_path, manifest, out_files, out_bytes);
        } else {
            if (CopyFileA(src_path, dst_path, FALSE)) {
                uint64_t file_size = ((uint64_t)fd.nFileSizeHigh << 32) | fd.nFileSizeLow;
                if (out_files) (*out_files)++;
                if (out_bytes) (*out_bytes) += file_size;
                if (manifest) {
                    fprintf(manifest, "%s | %llu bytes\n", src_path, (unsigned long long)file_size);
                }
            }
        }
    } while (FindNextFileA(hFind, &fd));

    FindClose(hFind);
    return true;
}

bool iagrok_ops_clean_system(uint64_t *out_files_removed, uint64_t *out_bytes_freed) {
    uint64_t files_cnt = 0;
    uint64_t bytes_cnt = 0;

    printf("[CLEAN] Iniciando Poda y Limpieza Nativa ANSI C99 (Zero Python)...\n");

    /* 1. Clean root junk files */
    WIN32_FIND_DATAA fd;
    HANDLE hFind = FindFirstFileA(".\\*", &fd);
    if (hFind != INVALID_HANDLE_VALUE) {
        do {
            if (fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
                if (_stricmp(fd.cFileName, "__pycache__") == 0) {
                    printf("  [CLEAN] Eliminando cache python: %s\n", fd.cFileName);
                    delete_directory_recursive(fd.cFileName, &files_cnt, &bytes_cnt);
                }
                continue;
            }

            bool should_delete = false;
            if (strncmp(fd.cFileName, "auto_gen_", 9) == 0) should_delete = true;
            if (strcmp(fd.cFileName, "127.0.0.1)") == 0) should_delete = true;
            if (strcmp(fd.cFileName, "captura_paquetes_cliente.log") == 0) should_delete = true;
            if (strstr(fd.cFileName, ".bak_") != NULL) should_delete = true;

            const char *ext = strrchr(fd.cFileName, '.');
            if (ext && _stricmp(ext, ".pyc") == 0) should_delete = true;

            if (should_delete) {
                uint64_t sz = ((uint64_t)fd.nFileSizeHigh << 32) | fd.nFileSizeLow;
                if (DeleteFileA(fd.cFileName)) {
                    files_cnt++;
                    bytes_cnt += sz;
                    printf("  [CLEAN] Archivo residual eliminado: %s (%.1f KB)\n", fd.cFileName, (double)sz / 1024.0);
                }
            }
        } while (FindNextFileA(hFind, &fd));
        FindClose(hFind);
    }

    /* 2. Clean ISO staging if exists */
    const char *iso_staging = "kernels\\NeuroOSDEFINITIVO\\iso_staging_dir";
    if (GetFileAttributesA(iso_staging) != INVALID_FILE_ATTRIBUTES) {
        printf("  [CLEAN] Purgando staging ISO duplicado: %s\n", iso_staging);
        delete_directory_recursive(iso_staging, &files_cnt, &bytes_cnt);
    }

    /* 3. Empty system working set for IAGROK process */
    double freed_mb = iagrok_purge_working_set();
    printf("  [CLEAN] Memoria RAM del proceso purgada (EmptyWorkingSet): %.2f MB liberados.\n", freed_mb);

    if (out_files_removed) *out_files_removed = files_cnt;
    if (out_bytes_freed) *out_bytes_freed = bytes_cnt;

    printf("[CLEAN] Limpieza completada: %llu archivos eliminados, %.2f MB de almacenamiento liberado.\n\n",
           (unsigned long long)files_cnt, (double)bytes_cnt / (1024.0 * 1024.0));
    return true;
}

bool iagrok_ops_backup_system(const char *backup_root, char *out_target_path, size_t max_path_len) {
    const char *root = (backup_root && strlen(backup_root) > 0) ? backup_root : "backups";
    create_dir_recursive(root);

    time_t raw_time = time(NULL);
    struct tm *tm_info = localtime(&raw_time);
    char timestamp[32];
    strftime(timestamp, sizeof(timestamp), "%Y%m%d_%H%M%S", tm_info);

    char backup_dir[1024];
    snprintf(backup_dir, sizeof(backup_dir), "%s\\BACKUP_IAGROK_NATIVO_C99_%s", root, timestamp);
    create_dir_recursive(backup_dir);

    if (out_target_path && max_path_len > 0) {
        snprintf(out_target_path, max_path_len, "%s", backup_dir);
    }

    printf("====================================================================\n");
    printf("  IAGROK SOBERANO - GENERADOR DE RESPALDO NATIVO C99 (ZERO PYTHON)  \n");
    printf("====================================================================\n");
    printf("  Destino: %s\n\n", backup_dir);

    char manifest_path[1024];
    snprintf(manifest_path, sizeof(manifest_path), "%s\\MANIFEST_INTEGRIDAD.txt", backup_dir);
    FILE *manifest = fopen(manifest_path, "w");
    if (manifest) {
        fprintf(manifest, "IAGROK SOBERANO - MANIFIESTO DE INTEGRIDAD NATIVO C99\n");
        fprintf(manifest, "Generado: %s\n", timestamp);
        fprintf(manifest, "Estandar: 100%% ANSI C99 / UPL+ Respaldo Soberano\n");
        fprintf(manifest, "--------------------------------------------------------------------\n");
    }

    uint64_t total_files = 0;
    uint64_t total_bytes = 0;

    const char *dirs_to_backup[] = {
        "iagrok_native",
        "sistemas_de_defensa",
        "cerebro_soberano",
        "templates",
        "IAGROK_TYPESAFE_BENCHMARK_KIT"
    };
    size_t num_dirs = sizeof(dirs_to_backup) / sizeof(dirs_to_backup[0]);

    for (size_t i = 0; i < num_dirs; ++i) {
        if (GetFileAttributesA(dirs_to_backup[i]) != INVALID_FILE_ATTRIBUTES) {
            printf("  [BACKUP] Copiando modulo: %s ...\n", dirs_to_backup[i]);
            char dst_subdir[1024];
            snprintf(dst_subdir, sizeof(dst_subdir), "%s\\%s", backup_dir, dirs_to_backup[i]);
            copy_directory_recursive(dirs_to_backup[i], dst_subdir, manifest, &total_files, &total_bytes);
        }
    }

    /* Copy root critical markdown and configs */
    const char *root_files[] = {
        "README.md",
        "DECLARACION_OFICIAL_BENCHMARK_IAGROK_VS_TYPESAFE_JEV.md",
        "INFORME_BENCHMARK_SOBERANO_2026.json",
        "LANZAR_IAGROK_NATIVO.bat",
        "LANZAR_SERVIDOR_WEB_NEURO_STORE.bat",
        "PURGAR_RAM_NATIVO_C99.bat",
        "TEST_BENCHMARK_SIMD_C99.bat",
        "TEST_VERIFICACION_COMPLETA_C99.bat"
    };
    size_t num_files = sizeof(root_files) / sizeof(root_files[0]);

    for (size_t i = 0; i < num_files; ++i) {
        if (GetFileAttributesA(root_files[i]) != INVALID_FILE_ATTRIBUTES) {
            char dst_file[1024];
            snprintf(dst_file, sizeof(dst_file), "%s\\%s", backup_dir, root_files[i]);
            if (CopyFileA(root_files[i], dst_file, FALSE)) {
                total_files++;
                WIN32_FIND_DATAA fd;
                HANDLE h = FindFirstFileA(root_files[i], &fd);
                if (h != INVALID_HANDLE_VALUE) {
                    uint64_t sz = ((uint64_t)fd.nFileSizeHigh << 32) | fd.nFileSizeLow;
                    total_bytes += sz;
                    if (manifest) fprintf(manifest, "%s | %llu bytes\n", root_files[i], (unsigned long long)sz);
                    FindClose(h);
                }
            }
        }
    }

    if (manifest) {
        fprintf(manifest, "--------------------------------------------------------------------\n");
        fprintf(manifest, "Total archivos: %llu\n", (unsigned long long)total_files);
        fprintf(manifest, "Total bytes: %llu (%.2f MB)\n", (unsigned long long)total_bytes, (double)total_bytes / (1024.0 * 1024.0));
        fclose(manifest);
    }

    printf("\n[OK] Respaldo finalizado con exito.\n");
    printf("     Archivos respaldados: %llu\n", (unsigned long long)total_files);
    printf("     Tamano total:         %.2f MB\n", (double)total_bytes / (1024.0 * 1024.0));
    printf("     Manifiesto:           %s\n\n", manifest_path);

    return true;
}
