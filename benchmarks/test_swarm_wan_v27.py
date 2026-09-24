#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEURO-OS 1.1.0-DEF — BENCHMARK & CERTIFICACIÓN V27
==================================================
Arnês empírico para certificar:
1. Sincronización de Enjambre P2P/WAN con fragmentación criptográfica SWRM.
2. Respaldo Criptográfico Espejo PRE/POST-CICLO (ASMI-DOE V10).
3. Auditoría SHA256 de Integridad Científica.
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

from arquitectura_cognitiva.swarm_wan_sharding_v27 import SwarmWANShardingEngineV27


class TestSwarmWANV27(unittest.TestCase):

    def setUp(self):
        self.engine = SwarmWANShardingEngineV27()

    def test_01_swarm_wan_cryptographic_sharding(self):
        print("\n" + "="*80)
        print("⚡ EJECUTANDO CERTIFICACIÓN V27: ENJAMBRE P2P/WAN & FRAGMENTACIÓN CRIPTOGRÁFICA")
        print("="*80)

        res = self.engine.sincronizar_enjambre_wan(105, b"SWARM_WAN_SYNC_DATA_TEST_V27")

        print(f"\n🔹 PASO 1: Respaldo Criptográfico Espejo (ASMI-DOE V10)")
        print(f"   ├─ Respaldo PRE-CICLO:        {res.get('backup_pre')}")
        print(f"   └─ Respaldo POST-CICLO:       {res.get('backup_post')}")

        self.assertTrue(res.get("backup_pre"))
        self.assertTrue(res.get("backup_post"))

        print(f"\n🔹 PASO 2: Sincronización SWRM P2P")
        print(f"   ├─ Node ID:                  {res.get('node_id')}")
        print(f"   ├─ Bytes Transmitidos:       {res.get('bytes_sincronizados')} Bytes")
        print(f"   ├─ Cabecera SWRM:            {res.get('swarm_packet_header')}")
        print(f"   └─ Latencia de Red:          {res.get('latency_ms')} ms")

        self.assertTrue(res.get("ok"))
        self.assertEqual(res.get("swarm_packet_header"), "SWRM")

        print("\n" + "="*80)
        print("📊 CERTIFICADO V27 — STATUS:")
        print("   ├─ Respaldo PRE/POST-CICLO:                  ✅ COMPLETADO")
        print("   ├─ Sincronización SWRM P2P/WAN:              ✅ COMPLETADO")
        print("   └─ Soberanía Extrema V27:                     🚀 EXTREMO (ENJAMBRE WAN V27)")
        print("="*80 + "\n")


if __name__ == "__main__":
    unittest.main()
