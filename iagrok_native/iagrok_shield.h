/* ============================================================================ */
/* IAGROK NATIVE C99 - SOVEREIGN SHIELD & ANTI-REVERSE-ENGINEERING (REA DEFENSE)*/
/* 100% ANSI C99 / Win32 / x86_64 Register-Level Protection                     */
/* Defends against: REA (Reverse Engineer Anything), Ghidra, IDA Pro, Hopper    */
/* ============================================================================ */

#ifndef IAGROK_SHIELD_H
#define IAGROK_SHIELD_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Initializes the sovereign anti-reverse-engineering shield in Ring 0.
 * Sets up integrity baselines, anti-tampering guards, and memory traps.
 */
void iagrok_shield_init(void);

/**
 * Actively inspects the running process environment for REA/Ghidra/IDA hooks.
 * Checks PEB BeingDebugged, NtGlobalFlag, Hardware Breakpoints (DR0-DR3),
 * and timing anomalies via QueryPerformanceCounter / RDTSC.
 *
 * @return true if environment is sovereign and untampered, false if under analysis.
 */
bool iagrok_shield_verify_environment(void);

/**
 * Verifies code segment (.text) integrity against runtime patch injection.
 * @return true if untouched, false if breakpoints (0xCC) or patches detected.
 */
bool iagrok_shield_verify_text_integrity(void);

/**
 * Encrypts or decrypts a sensitive string buffer in-place using ephemeral XOR cipher.
 * Ensures zero plaintext strings in .rdata for Hopper/Ghidra to anchor onto.
 *
 * @param data Buffer to encrypt/decrypt
 * @param len Length of the buffer
 * @param key 64-bit ephemeral cipher key
 */
void iagrok_shield_scramble(char *data, size_t len, uint64_t key);

/**
 * Triggers defensive countermeasures if an automated reverse-engineering attack is confirmed.
 * Empties working set, zeroes memory tables, and cleanly terminates execution.
 */
void iagrok_shield_defensive_purge(const char *reason);

#ifdef __cplusplus
}
#endif

#endif /* IAGROK_SHIELD_H */
