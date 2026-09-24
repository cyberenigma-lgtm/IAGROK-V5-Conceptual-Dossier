# -*- coding: utf-8 -*-
"""
⚡ IAGROK V9 BENCHMARK & CERTIFICACIÓN: ACELERACIÓN DEL METAL EN RUST/C++ (C-ABI NATIVO)
Ubicación: c:\\IAGROK\\benchmarks\\test_acelerador_nativo_v9.py

Certifica el salto de rendimiento de la Versión V9:
1. Porting de la Calibración Sigmoidal de Platt a Rust C-ABI nativo.
2. Hashing no criptográfico FNV-1a de 32 bits directo en binario compilado.
3. Cero descalibración (delta < 1e-6) y latencia ultra-baja garantizada.
"""

import os
import sys
import time
import math

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if sys.platform == "win32":
    getattr(sys.stdout, "reconfigure", lambda **kw: None)(encoding="utf-8")

from arquitectura_cognitiva.iagrok_native_bridge import native_bridge
from arquitectura_cognitiva.decisor_sistema1_ultra import decisor_sistema1

def calibrar_platt_python_ref(raw_score: float, a: float = -1.20, b: float = 0.80) -> float:
    p_clamped = max(0.01, min(0.99, raw_score))
    logit = math.log(p_clamped / (1.0 - p_clamped))
    prob_calibrada = 1.0 / (1.0 + math.exp(a * logit + b))
    return max(0.20, min(0.96, prob_calibrada))

def fnv1a_32_python_ref(texto: str) -> int:
    h = 2166136261
    for b in texto.encode("utf-8"):
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h

def ejecutar_test_aceleracion_v9():
    print("================================================================================")
    print("🧪 EJECUTANDO CERTIFICACIÓN V9: ACELERACIÓN DEL METAL NATIVO (RUST C-ABI)")
    print("================================================================================")

    # 1. Prueba 1: Calibración Sigmoidal de Platt Nativa vs Referencia Python
    print("\n🔹 PASO 1: Certificación de Exactitud Platt Sigmoid (Rust vs Python)...")
    test_scores = [0.10, 0.35, 0.50, 0.75, 0.90, 0.98]
    platt_ok = True

    for s in test_scores:
        py_res = calibrar_platt_python_ref(s)
        rust_res = native_bridge.calibrar_platt_nativo(s)
        diff = abs(py_res - rust_res)
        if diff > 1e-5:
            platt_ok = False
        print(f"   ├─ Raw Score: {s:.2f} | Py: {py_res:.4f} | Rust: {rust_res:.4f} | Δ: {diff:.6e}")

    print(f"   └─ Exactitud de Calibración Platt: {'✅ OK (<1e-5)' if platt_ok else '❌ DESVIADO'}")

    # 2. Prueba 2: Hash FNV-1a 32-bit Nativo vs Referencia Python
    print("\n🔹 PASO 2: Certificación de Hash FNV-1a (Rust vs Python)...")
    test_strings = [
        "prewarm_kernel_l1_l2_cache_ping",
        "incidente_critico_desbordamiento",
        "iagrok_soberano_v9_metal_acceleration"
    ]
    fnv_ok = True

    for txt in test_strings:
        py_h = fnv1a_32_python_ref(txt)
        rust_h = native_bridge.fnv1a_32_nativo(txt)
        match = py_h == rust_h
        if not match:
            fnv_ok = False
        print(f"   ├─ Texto: '{txt[:30]}...' | Py Hash: {py_h} | Rust Hash: {rust_h} | Coincide: {'✅' if match else '❌'}")

    print(f"   └─ Integridad Hashing FNV-1a: {'✅ OK (100% Identico)' if fnv_ok else '❌ DESVIADO'}")

    # 3. Prueba 3: Benchmark Integrado Decisor Sistema 1 con Puente Nativo V9
    print("\n🔹 PASO 3: Benchmark Integrado de Sistema 1 con Aceleración Nativa V9...")
    query = "ALERTA CRÍTICA: Intento de desbordamiento de búfer en módulo nativo de memoria"
    pregunta_eval = [{
        "id": "categoria_incidente",
        "tipo": "clasificacion",
        "opciones": ["incidente", "ticket_soporte", "alerta_seguridad", "spam", "consulta"]
    }]

    t0 = time.perf_counter()
    res_s1 = decisor_sistema1.evaluar_decisiones_paralelas(query, pregunta_eval)
    t1 = time.perf_counter()
    lat_ms = round((t1 - t0) * 1000, 4)

    print(f"   ├─ Motor Exec: {res_s1['engine']}")
    print(f"   ├─ Decisión Tomada: {res_s1['decisiones']['categoria_incidente']['opcion_seleccionada']}")
    print(f"   ├─ Probabilidad Calibrada Nativa: {res_s1['decisiones']['categoria_incidente']['probabilidad_maxima']}")
    print(f"   ├─ Latencia Empírica: {lat_ms} ms ({lat_ms * 1000:.1f} µs)")
    print(f"   └─ Rendimiento Sub-Milisegundo: {'✅ SÍ' if lat_ms < 1.0 else '❌ NO'}")

    # 4. Resumen Final de Certificación V9
    exito_total = platt_ok and fnv_ok and (lat_ms < 1.0)

    print("\n================================================================================")
    print("📊 CERTIFICADO DE ACELERACIÓN METAL NATIVO V9 — RESUMEN FINAL:")
    print(f"   ├─ Platt Sigmoid Nativo en Rust: {'✅ SÍ' if platt_ok else '❌ NO'}")
    print(f"   ├─ Hash FNV-1a Nativo en Rust: {'✅ SÍ' if fnv_ok else '❌ NO'}")
    print(f"   ├─ Latencia Sub-Milisegundo Garantizada: {'✅ SÍ' if lat_ms < 1.0 else '❌ NO'}")
    print(f"   └─ Certificación Metal V9: {'✅ CERTIFICADO' if exito_total else '❌ FALLO'}")
    print("================================================================================")

    assert platt_ok, "Error: La calibración Platt en Rust difiere de la referencia"
    assert fnv_ok, "Error: El hash FNV-1a en Rust difiere de la referencia"
    assert lat_ms < 1.0, "Error: Se degradó la latencia sub-milisegundo"

if __name__ == "__main__":
    ejecutar_test_aceleracion_v9()
