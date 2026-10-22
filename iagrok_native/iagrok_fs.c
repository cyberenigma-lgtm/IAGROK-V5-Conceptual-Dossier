/* ============================================================================ */
/* IAGROK NATIVE C99 - FILE SYSTEM & PROGRAMMING ENVIRONMENT EXECUTION ENGINE    */
/* 100% ANSI C99 - Real Win32 File Tree, Source I/O, Compilers & Runners        */
/* ============================================================================ */

#define _WIN32_WINNT 0x0600
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "iagrok_fs.h"

static bool should_ignore_dir(const char *name) {
    if (!name || name[0] == '.') return true;
    const char *ignored[] = {
        "__pycache__", ".git", "node_modules", "target",
        ".venv", "venv", "target_run", "backups", "backups_geneticos"
    };
    for (size_t i = 0; i < sizeof(ignored) / sizeof(ignored[0]); ++i) {
        if (_stricmp(name, ignored[i]) == 0) return true;
    }
    return false;
}

/* Helper to escape backslashes for JSON */
static void json_escape_path(const char *in, char *out, size_t max_out) {
    size_t o = 0;
    for (size_t i = 0; in[i] && o < max_out - 2; ++i) {
        if (in[i] == '\\') {
            out[o++] = '\\';
            out[o++] = '\\';
        } else if (in[i] == '"') {
            out[o++] = '\\';
            out[o++] = '"';
        } else {
            out[o++] = in[i];
        }
    }
    out[o] = '\0';
}

static int build_tree_recursive(const char *abs_path, int max_depth, int depth, char *out, size_t max_out, size_t offset) {
    char search_pattern[1024];
    snprintf(search_pattern, sizeof(search_pattern), "%s\\*", abs_path);

    WIN32_FIND_DATAA fd;
    HANDLE hFind = FindFirstFileA(search_pattern, &fd);

    const char *basename = strrchr(abs_path, '\\');
    basename = basename ? basename + 1 : abs_path;

    char escaped_path[MAX_PATH * 2];
    json_escape_path(abs_path, escaped_path, sizeof(escaped_path));

    offset += snprintf(out + offset, max_out - offset,
        "{\"name\":\"%s\",\"path\":\"%s\",\"is_dir\":true,\"children\":[",
        basename, escaped_path);

    if (hFind != INVALID_HANDLE_VALUE) {
        bool first = true;
        do {
            if (strcmp(fd.cFileName, ".") == 0 || strcmp(fd.cFileName, "..") == 0) {
                continue;
            }

            char child_path[1024];
            snprintf(child_path, sizeof(child_path), "%s\\%s", abs_path, fd.cFileName);

            bool is_dir = (fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0;

            if (is_dir) {
                if (should_ignore_dir(fd.cFileName)) continue;
                if (depth < max_depth) {
                    if (!first) offset += snprintf(out + offset, max_out - offset, ",");
                    first = false;
                    offset = build_tree_recursive(child_path, max_depth, depth + 1, out, max_out, offset);
                }
            } else {
                if (!first) offset += snprintf(out + offset, max_out - offset, ",");
                first = false;
                char esc_child[MAX_PATH * 2];
                json_escape_path(child_path, esc_child, sizeof(esc_child));
                offset += snprintf(out + offset, max_out - offset,
                    "{\"name\":\"%s\",\"path\":\"%s\",\"is_dir\":false}",
                    fd.cFileName, esc_child);
            }

            if (offset >= max_out - 256) break; /* Guard buffer limit */
        } while (FindNextFileA(hFind, &fd));
        FindClose(hFind);
    }

    offset += snprintf(out + offset, max_out - offset, "]}");
    return (int)offset;
}

bool iagrok_fs_tree_json(const char *root_path, int max_depth, char *out_json, size_t max_out) {
    if (!root_path || !out_json || max_out == 0) return false;
    char abs_root[MAX_PATH];
    if (!GetFullPathNameA(root_path, MAX_PATH, abs_root, NULL)) {
        strncpy(abs_root, root_path, sizeof(abs_root) - 1);
    }
    int len = build_tree_recursive(abs_root, max_depth, 0, out_json, max_out, 0);
    return len > 0;
}

bool iagrok_fs_read(const char *filepath, char **out_content, size_t *out_len) {
    if (!filepath || !out_content) return false;

    FILE *f = fopen(filepath, "rb");
    if (!f) return false;

    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);

    if (sz < 0) {
        fclose(f);
        return false;
    }

    char *buf = (char*)malloc(sz + 1);
    if (!buf) {
        fclose(f);
        return false;
    }

    size_t read_bytes = fread(buf, 1, sz, f);
    buf[read_bytes] = '\0';
    fclose(f);

    *out_content = buf;
    if (out_len) *out_len = read_bytes;
    return true;
}

/* Recursive directory creator */
static void ensure_parent_dirs(const char *filepath) {
    char dir[MAX_PATH];
    strncpy(dir, filepath, sizeof(dir) - 1);
    dir[sizeof(dir) - 1] = '\0';

    for (char *p = dir + 1; *p; ++p) {
        if (*p == '/' || *p == '\\') {
            char temp = *p;
            *p = '\0';
            CreateDirectoryA(dir, NULL);
            *p = temp;
        }
    }
}

bool iagrok_fs_write(const char *filepath, const char *content) {
    if (!filepath || !content) return false;
    ensure_parent_dirs(filepath);

    FILE *f = fopen(filepath, "wb");
    if (!f) return false;

    size_t len = strlen(content);
    size_t written = fwrite(content, 1, len, f);
    fclose(f);

    return written == len;
}

bool iagrok_fs_execute(const char *filepath,
                       char *out_stdout, size_t max_out,
                       char *out_stderr, size_t max_err,
                       int *out_exit_code) {
    if (!filepath || !out_stdout || max_out == 0) return false;

    out_stdout[0] = '\0';
    if (out_stderr && max_err > 0) out_stderr[0] = '\0';
    if (out_exit_code) *out_exit_code = -1;

    const char *ext = strrchr(filepath, '.');
    if (!ext) ext = "";

    char cmd[1024];
    char exe_temp[MAX_PATH];

    /* Prepare compilation/execution command */
    if (_stricmp(ext, ".c") == 0) {
        snprintf(exe_temp, sizeof(exe_temp), "%s.exe", filepath);
        snprintf(cmd, sizeof(cmd), "gcc -std=c99 -O2 \"%s\" -o \"%s\" -lm 2>&1 && \"%s\"", filepath, exe_temp, exe_temp);
    } else if (_stricmp(ext, ".cpp") == 0) {
        snprintf(exe_temp, sizeof(exe_temp), "%s.exe", filepath);
        snprintf(cmd, sizeof(cmd), "g++ -O2 \"%s\" -o \"%s\" -lm 2>&1 && \"%s\"", filepath, exe_temp, exe_temp);
    } else if (_stricmp(ext, ".rs") == 0) {
        snprintf(exe_temp, sizeof(exe_temp), "%s.exe", filepath);
        snprintf(cmd, sizeof(cmd), "rustc \"%s\" -o \"%s\" 2>&1 && \"%s\"", filepath, exe_temp, exe_temp);
    } else if (_stricmp(ext, ".bat") == 0) {
        snprintf(cmd, sizeof(cmd), "cmd.exe /c \"%s\" 2>&1", filepath);
    } else if (_stricmp(ext, ".ps1") == 0) {
        snprintf(cmd, sizeof(cmd), "powershell.exe -ExecutionPolicy Bypass -File \"%s\" 2>&1", filepath);
    } else if (_stricmp(ext, ".py") == 0) {
        snprintf(cmd, sizeof(cmd), "python.exe \"%s\" 2>&1", filepath);
    } else if (_stricmp(ext, ".js") == 0) {
        snprintf(cmd, sizeof(cmd), "node.exe \"%s\" 2>&1", filepath);
    } else if (_stricmp(ext, ".exe") == 0) {
        snprintf(cmd, sizeof(cmd), "\"%s\" 2>&1", filepath);
    } else {
        snprintf(out_stdout, max_out, "Unsupported executable file type: %s", ext);
        return false;
    }

    FILE *pipe = _popen(cmd, "r");
    if (!pipe) {
        snprintf(out_stdout, max_out, "Failed to launch process: %s", cmd);
        return false;
    }

    size_t total_read = 0;
    char buffer[512];
    while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
        size_t blen = strlen(buffer);
        if (total_read + blen < max_out - 1) {
            strcat(out_stdout, buffer);
            total_read += blen;
        } else {
            break;
        }
    }

    int ret = _pclose(pipe);
    if (out_exit_code) *out_exit_code = ret;

    return true;
}
