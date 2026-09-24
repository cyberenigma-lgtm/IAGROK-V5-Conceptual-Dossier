# -*- coding: utf-8 -*-
"""
Benchmark Test Harness - V30: Master Sovereign Hypervisor Kernel Unification
Certificación final de unificación total del sistema IAGROK hasta la V30.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arquitectura_cognitiva.hypervisor_master_v30 import HypervisorMasterKernelV30
from arquitectura_cognitiva.gestor_respaldo_espejo_criptografico import GestorRespaldoEspejoCriptografico


def test_hypervisor_master_v30():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("======================================================================")
    print("👑 [BENCHMARK V30] INICIANDO PRUEBA DEL HIPERVISOR SOBERANO MAESTRO V30")
    print("======================================================================")

    # 1. Copia de seguridad PRE-TEST MAESTRO
    backup = GestorRespaldoEspejoCriptografico()
    res_pre = backup.respaldar_buffer_asmi_doe("PRE_BENCHMARK_MASTER_V30", b"PAYLOAD_PRE_MASTER_V30")
    assert res_pre.get("ok"), "Fallo backup PRE V30"
    print(f"🔒 [ASMI-DOE V10] Backup PRE-MASTER-V30 completado. Hash: {res_pre['sha256'][:16]}...")

    # 2. Inicializar Hipervisor V30
    kernel = HypervisorMasterKernelV30()
    res_boot = kernel.inicializar_hipervisor_v30()

    assert res_boot["estado_general"] == "HYPERVISOR_V30_ONLINE_MASTER_CERTIFIED", "Fallo arranque Hipervisor V30"
    assert res_boot["backup_pre"] and res_boot["backup_post"], "Fallo de respaldos en arranque de hipervisor"

    print(f"🚀 [ARRANQUE HIPERVISOR V30] Versión: {res_boot['version']}")
    print(f"⏱️ [LATENCIA ARRANQUE]      {res_boot['latencia_arranque_ms']:.3f} ms")
    print(f"📌 [AFINIDAD HARDWARE]      {res_boot['afinidad_hardware']}")
    print(f"⚡ [JIT NWC OPCODES]        {res_boot['jit_opcodes_bytes']} Bytes generados")
    print(f"💾 [JERARQUÍA MEMORIA]      {res_boot['memoria_status']}")
    print(f"🩺 [SALUD SOMÁTICA]         {res_boot['somatic_health']}")

    # 3. Copia de seguridad POST-TEST MAESTRO
    res_post = backup.respaldar_buffer_asmi_doe("POST_BENCHMARK_MASTER_V30", b"PAYLOAD_POST_MASTER_V30")
    assert res_post.get("ok"), "Fallo backup POST V30"
    print(f"🔒 [ASMI-DOE V10] Backup POST-MASTER-V30 completado. Hash: {res_post['sha256'][:16]}...")

    print("======================================================================")
    print("🏆 PRUEBA V30 (MASTER HYPERVISOR KERNEL UNIFICATION) COMPLETADA CON ÉXITO [EXIT CODE 0]")
    print("======================================================================")


if __name__ == "__main__":
    test_hypervisor_master_v30()
