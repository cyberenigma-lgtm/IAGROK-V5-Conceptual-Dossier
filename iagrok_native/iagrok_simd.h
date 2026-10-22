/* ============================================================================ */
/* IAGROK NATIVE C99 - HARDWARE-ACCELERATED SIMD VECTOR ENGINE (AVX2/FMA)       */
/* Real Hardware Vector Operations - High Throughput Cosine k-NN Search         */
/* ============================================================================ */

#ifndef IAGROK_SIMD_H
#define IAGROK_SIMD_H

#include "iagrok_types.h"
#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Real CPU feature detection */
bool iagrok_cpu_has_avx2(void);
bool iagrok_cpu_has_fma(void);

/* Real AVX2/FMA vector dot product */
float iagrok_simd_dot_product_avx2(const float *a, const float *b, size_t dim);

/* Scalar fallback vector dot product (for testing, benchmarks and CPU fallback) */
float iagrok_simd_dot_product_scalar(const float *a, const float *b, size_t dim);

/* L2 Euclidean vector norm */
float iagrok_simd_l2_norm(const float *a, size_t dim);

/* Normalizes a vector in-place such that ||v||_2 = 1.0 */
void iagrok_simd_normalize(float *v, size_t dim);

/* Real Cosine Similarity calculation */
float iagrok_simd_cosine_similarity(const float *a, const float *b, size_t dim);

/* High-performance k-NN search across document vector matrix */
/* matrix contains (num_docs * dim) floats. */
/* Results array must have space for at least top_k elements. */
/* elapsed_us receives the real execution time measured with QueryPerformanceCounter */
void iagrok_simd_knn_search(const float *query,
                            const float *matrix,
                            size_t num_docs,
                            size_t dim,
                            size_t top_k,
                            IagrokKnnResult *results,
                            double *elapsed_us);

/* Real performance benchmark comparing AVX2 SIMD against Scalar loop */
void iagrok_simd_benchmark(size_t num_vectors,
                           size_t dim,
                           double *avx2_time_ms,
                           double *scalar_time_ms,
                           double *speedup);

/* ============================================================================ */
/* NEW TRANSFORMER & SELF-CORRECTIVE OPERATORS (META MUSE + OPENAI ASTRA)       */
/* ============================================================================ */

/* Fast Hardware-Accelerated RMSNorm with AVX2 (Meta Muse / OpenAI Astra) */
void iagrok_simd_rmsnorm(const float *x, const float *weight, float *out, size_t dim, float eps);

/* SwiGLU Fused Activation with AVX2: out[i] = x[i] * SiLU(gate[i]) */
void iagrok_simd_swiglu(const float *x, const float *gate, float *out, size_t dim);

/* Looped Transformer Recurrent Step (OpenAI Astra Weight-Sharing Architecture) */
/* Executes weight-sharing recurrent depth with adaptive early stopping */
int iagrok_simd_looped_transformer_step(float *state, const float *weights, size_t dim, int max_loops, float convergence_threshold);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_SIMD_H */
