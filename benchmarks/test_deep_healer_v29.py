# -*- coding: utf-8 -*-
"""
Benchmark Test Harness - V29: Deep Somatic Hardware Healer & Autonomous Mesh
Verifica autocuración profunda y respaldos PRE/POST ciclo ASMI-DOE V10.
"""

import os
import sys
import hashlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arquitectura_cognitiva.deep_somatic_healer_v29 import DeepSomaticHealerV29
from arquitectura_cognitiva.gestor_respaldo_espejo_criptografico import GestorRespaldoEspejoCriptografico


def test_deep_healer_v29():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("======================================================================")
    print("⚡ [BENCHMARK V29] INICIANDO PRUEBA DE AUTOCURACIÓN hardware SOMÁTICA")
    print("======================================================================")

    # 1. Backup PRE-TEST
    backup = GestorRespaldoEspejoCriptografico()
    res_pre = backup.respaldar_buffer_asmi_doe("PRE_BENCHMARK_V29", b"PAYLOAD_PRE_V29")
    assert res_pre.get("ok"), "Fallo backup PRE V29"
    print(f"🔒 [ASMI-DOE V10] Backup PRE-V29 completado. Hash: {res_pre['sha256'][:16]}...")

    healer = DeepSomaticHealerV29()

    # 2. Prueba Diagnóstico Saludable
    payload_sano = b"SOMATIC_STABLE_PATTERN_" * 10
    hash_sano = hashlib.sha256(payload_sano).hexdigest()

    res1 = healer.diagnosticar_y_reparar_buffer("nodo_p_core_0", payload_sano, hash_sano)
    assert not res1["corrupcion_detectada"], "Se detectó corrupción errónea en buffer sano"
    assert res1["estado"] == "HEALTHY_INTEGRITY", "Estado de salud incorrecto"
    print(f"✅ [NODO SALUDABLE] Verificado en {res1['latencia_curacion_ms']:.4f} ms | Hash: {res1['hash_reparado'][:16]}...")

    # 3. Prueba Diagnóstico y Curación de Corrupción
    payload_alterado = b"SOMATIC_MUTATED_PATTERN_" * 10
    res2 = healer.diagnosticar_y_reparar_buffer("nodo_e_core_3", payload_alterado, hash_sano)
    assert res2["corrupcion_detectada"], "No se detectó la corrupción simulada"
    assert res2["estado"] == "AUTONOMICALLY_RESTORED", "No se autocuro el buffer"
    print(f"🛠️ [NODO AUTOCURADO] Restaurado en {res2['latencia_curacion_ms']:.4f} ms | Hash: {res2['hash_reparado'][:16]}...")

    # 4. Backup POST-TEST
    res_post = backup.respaldar_buffer_asmi_doe("POST_BENCHMARK_V29", b"PAYLOAD_POST_V29")
    assert res_post.get("ok"), "Fallo backup POST V29"
    print(f"🔒 [ASMI-DOE V10] Backup POST-V29 completado. Hash: {res_post['sha256'][:16]}...")

    print("======================================================================")
    print("🏆 PRUEBA V29 (DEEP SOMATIC HEALER) COMPLETADA CON ÉXITO [EXIT CODE 0]")
    print("======================================================================")


if __name__ == "__main__":
    test_deep_healer_v29()
