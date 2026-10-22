/* ============================================================================ */
/* IAGROK NATIVE C99 - TEXT EMBEDDING & VECTOR ENCODING ENGINE                  */
/* High-performance deterministic semantic vectorization in microseconds        */
/* ============================================================================ */

#ifndef IAGROK_EMBED_H
#define IAGROK_EMBED_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define IAGROK_DEFAULT_EMBED_DIM 1536

/* Convert arbitrary UTF-8 text into a normalized float embedding vector */
/* out_vec must be pre-allocated to hold (dim * sizeof(float)) bytes */
bool iagrok_text_to_vector(const char *text, float *out_vec, size_t dim);

/* Batch vectorization of multiple document strings into a contiguous matrix */
/* out_matrix must be allocated for (num_docs * dim * sizeof(float)) */
bool iagrok_batch_texts_to_matrix(const char *const *texts,
                                  size_t num_docs,
                                  float *out_matrix,
                                  size_t dim);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_EMBED_H */
