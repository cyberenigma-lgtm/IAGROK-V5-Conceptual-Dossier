# -*- coding: utf-8 -*-
"""
Benchmark Test Harness - V28: Memory Tiering & Swap Burst GC Isolation
Verifica asignación multinivel L1/L2/L3 y ciclo de purga aislada con respaldo ASMI-DOE V10.
"""

import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arquitectura_cognitiva.memory_tiering_gc_v28 import GestorJerarquiaMemoriaV28
from arquitectura_cognitiva.gestor_respaldo_espejo_criptografico import GestorRespaldoEspejoCriptografico


def test_memory_tiering_v28():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("======================================================================")
    print("⚡ [BENCHMARK V28] INICIANDO PRUEBA DE TIERING DE MEMORIA Y GC AISLADO")
    print("======================================================================")

    # 1. Copia de seguridad PRE-TEST
    backup = GestorRespaldoEspejoCriptografico()
    res_pre = backup.respaldar_buffer_asmi_doe("PRE_BENCHMARK_V28", b"PAYLOAD_BENCHMARK_PRE_V28")
    assert res_pre.get("ok"), "FALLO: Copia de seguridad PRE-V28 invalida"
    print(f"🔒 [ASMI-DOE V10] Backup PRE-V28 completado. Hash: {res_pre['sha256'][:16]}...")

    gestor = GestorJerarquiaMemoriaV28()

    # 2. Prueba L1 (RAM Ultra-Rapida)
    payload_hot = b"\xAB" * 1024 * 10 # 10 KB
    res_l1 = gestor.clasificar_y_almacenar("hot_vector_01", payload_hot, "L1")
    assert res_l1["capa_asignada"] == "L1", "Fallo asignación L1"
    print(f"✅ [L1 CACHE] Asignado en {res_l1['latencia_ms']:.4f} ms | Tamaño: {res_l1['tamaño_bytes']} B")

    # 3. Prueba L2 (RAM Sistema)
    payload_sys = b"\xCD" * 1024 * 50 # 50 KB
    res_l2 = gestor.clasificar_y_almacenar("sys_matrix_01", payload_sys, "L2")
    assert res_l2["capa_asignada"] == "L2", "Fallo asignación L2"
    print(f"✅ [L2 RAM]   Asignado en {res_l2['latencia_ms']:.4f} ms | Tamaño: {res_l2['tamaño_bytes']} B")

    # 4. Prueba L3 (Swap Burst)
    payload_burst = b"\xEF" * 1024 * 100 # 100 KB
    res_l3 = gestor.clasificar_y_almacenar("swap_burst_01", payload_burst, "L3")
    print(f"✅ [L3 SWAP]  Asignado a Capa: {res_l3['capa_asignada']} | Latencia: {res_l3['latencia_ms']:.4f} ms")

    # 5. Generar basura en memoria y forzar Purga Aislada
    dummy_garbage = [b"X" * 100000 for _ in range(500)]
    del dummy_garbage

    res_gc = gestor.purgar_memoria_aislada()
    assert res_gc["estado"] == "ISOLATED_PURGE_SUCCESS", "Fallo recolección GC"
    print(f"🧹 [GC PURGE] Completo en {res_gc['duracion_ms']:.3f} ms | Objetos recolectados: {res_gc['objetos_recolectados']}")

    # 6. Copia de seguridad POST-TEST
    res_post = backup.respaldar_buffer_asmi_doe("POST_BENCHMARK_V28", b"PAYLOAD_BENCHMARK_POST_V28")
    assert res_post.get("ok"), "FALLO: Copia de seguridad POST-V28 invalida"
    print(f"🔒 [ASMI-DOE V10] Backup POST-V28 completado. Hash: {res_post['sha256'][:16]}...")

    print("======================================================================")
    print("🏆 PRUEBA V28 (MEMORY TIERING & GC ISOLATION) COMPLETADA CON ÉXITO [EXIT CODE 0]")
    print("======================================================================")


if __name__ == "__main__":
    test_memory_tiering_v28()
