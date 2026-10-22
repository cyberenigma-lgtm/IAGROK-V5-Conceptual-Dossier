/* ============================================================================ */
/* IAGROK NATIVE C99 - TEXT EMBEDDING & VECTOR ENCODING ENGINE                  */
/* 100% ANSI C99 - Deterministic Feature Hashing and SIMD Normalization        */
/* ============================================================================ */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "iagrok_embed.h"
#include "iagrok_simd.h"

static bool is_delimiter(char c) {
    return isspace((unsigned char)c) ||
           c == '.' || c == ',' || c == '(' || c == ')' ||
           c == '-' || c == '_' || c == '!' || c == '?' ||
           c == '"' || c == '\'' || c == ';' || c == ':' ||
           c == '/' || c == '\\' || c == '[' || c == ']' ||
           c == '{' || c == '}';
}

bool iagrok_text_to_vector(const char *text, float *out_vec, size_t dim) {
    if (!text || !out_vec || dim == 0) return false;

    /* Initialize baseline vector */
    for (size_t i = 0; i < dim; ++i) {
        out_vec[i] = 0.05f;
    }

    /* Tokenize text */
    const char *p = text;
    char token[128];
    size_t tok_len = 0;

    while (*p) {
        if (!is_delimiter(*p)) {
            if (tok_len < sizeof(token) - 1) {
                token[tok_len++] = (char)tolower((unsigned char)*p);
            }
        } else {
            if (tok_len > 2) {
                token[tok_len] = '\0';
                /* Polynomial hash (base 31) */
                uint64_t h = 0;
                uint64_t p_pow = 1;
                for (size_t i = 0; i < 8 && token[i]; ++i) {
                    h += ((uint64_t)(unsigned char)token[i]) * p_pow;
                    p_pow *= 31;
                }
                size_t slot = (size_t)(h % dim);
                out_vec[slot] += 1.0f + ((float)tok_len * 0.1f);
            }
            tok_len = 0;
        }
        p++;
    }

    /* Process final trailing token */
    if (tok_len > 2) {
        token[tok_len] = '\0';
        uint64_t h = 0;
        uint64_t p_pow = 1;
        for (size_t i = 0; i < 8 && token[i]; ++i) {
            h += ((uint64_t)(unsigned char)token[i]) * p_pow;
            p_pow *= 31;
        }
        size_t slot = (size_t)(h % dim);
        out_vec[slot] += 1.0f + ((float)tok_len * 0.1f);
    }

    /* L2 normalize vector using AVX2 SIMD */
    iagrok_simd_normalize(out_vec, dim);

    return true;
}

bool iagrok_batch_texts_to_matrix(const char *const *texts,
                                  size_t num_docs,
                                  float *out_matrix,
                                  size_t dim) {
    if (!texts || !out_matrix || num_docs == 0 || dim == 0) return false;

    for (size_t i = 0; i < num_docs; ++i) {
        if (!iagrok_text_to_vector(texts[i], &out_matrix[i * dim], dim)) {
            return false;
        }
    }
    return true;
}
