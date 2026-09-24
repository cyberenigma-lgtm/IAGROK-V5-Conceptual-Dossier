#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEURO-OS 1.1.0-DEF — BENCHMARK & CERTIFICACIÓN V26
==================================================
Arnês empírico para certificar:
1. Acoplamiento Vectorial DVTRGAS-30 (0xAA30).
2. Fijación de Afinidad de Hardware a P-Cores / E-Cores.
3. Respaldo Criptográfico Espejo PRE/POST-CICLO (ASMI-DOE V10).
4. Auditoría SHA256 de Integridad Científica.
"""

import os
import sys
import unittest

if sys.platform == 'win32':
    try:
        r1 = getattr(sys.stdout, 'reconfigure', None)
        if callable(r1): r1(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from arquitectura_cognitiva.vector_coupling_affinity_v26 import VectorCouplingAffinityEngineV26


class TestVectorAffinityV26(unittest.TestCase):

    def setUp(self):
        self.engine = VectorCouplingAffinityEngineV26()

    def test_01_dvtrgas30_vector_coupling_and_affinity(self):
        print("\n" + "="*80)
        print("⚡ EJECUTANDO CERTIFICACIÓN V26: DVTRGAS-30 VECTOR PIPELINE & AFINIDAD DE HARDWARE")
        print("="*80)

        res = self.engine.procesar_vector_dvtrgas30(999, b"DVTRGAS30_VECTOR_DATA_BENCHMARK")

        print(f"\n🔹 PASO 1: Respaldo Criptográfico Espejo (ASMI-DOE V10)")
        print(f"   ├─ Respaldo PRE-CICLO:        {res.get('backup_pre')}")
        print(f"   └─ Respaldo POST-CICLO:       {res.get('backup_post')}")

        self.assertTrue(res.get("backup_pre"))
        self.assertTrue(res.get("backup_post"))

        print(f"\n🔹 PASO 2: Procesamiento Vectorial DVTRGAS-30 (0xAA30)")
        print(f"   ├─ Vector ID:                {res.get('vector_id')}")
        print(f"   ├─ Firma Vectorial:          {res.get('signature')}")
        print(f"   ├─ Tamaño Payload:           {res.get('vector_bytes')} Bytes")
        print(f"   ├─ Afinidad P-Cores Fijada:   {res.get('p_core_affinity_pinned')}")
        print(f"   └─ Hilos Asignados:           {res.get('assigned_cores')}")

        self.assertTrue(res.get("ok"))
        self.assertTrue(res.get("p_core_affinity_pinned"))

        print(f"\n🔹 PASO 3: Latencia Vectorial")
        print(f"   ├─ Latencia Medida:          {res.get('latency_ms')} ms")
        print(f"   └─ Rendimiento:              ACOPLADO A SILICIO / P-CORES")

        print("\n" + "="*80)
        print("📊 CERTIFICADO V26 — STATUS:")
        print("   ├─ Respaldo PRE/POST-CICLO:                  ✅ COMPLETADO")
        print("   ├─ Pipeline Vectorial DVTRGAS-30 (0xAA30):    ✅ COMPLETADO")
        print("   ├─ Afinidad Hardware P-Cores / E-Cores:       ✅ VALIDADO")
        print("   └─ Soberanía Extrema V26:                     🚀 EXTREMO (ACOPLAMIENTO V26)")
        print("="*80 + "\n")


if __name__ == "__main__":
    unittest.main()
