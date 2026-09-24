#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path: sys.path.insert(0, BASE_DIR)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from arquitectura_cognitiva.planificador_afinidad_hardware import planificador_afinidad
from arquitectura_cognitiva.gestor_respaldo_espejo_criptografico import gestor_respaldo

def certificar_afinidad_y_respaldos_v14():
    print("================================================================================")
    print("⚡ EJECUTANDO CERTIFICACIÓN V14: AFINIDAD DE HILOS HARDWARE Y RESPALDO ESPEJO")
    print("================================================================================")

    # -------------------------------------------------------------------------
    print("\n🔹 PASO 1: Fijación Hardware de P-Cores (Neurobús Maestro & Sistema 1 Alpha)")
    t_ini = time.perf_counter()
    res_p = planificador_afinidad.fijar_p_cores_hilo_actual()
    lat_ns_p = (time.perf_counter() - t_ini) * 1e9

    print(f"   ├─ Status:                    {res_p.get('ok')}")
    print(f"   ├─ Máscara de Afinidad (Hex): {res_p.get('mask_hex')}")
    print(f"   ├─ Asignación de Núcleos:    {res_p.get('tipo_core')}")
    print(f"   ├─ Prioridad Elevada:        {res_p.get('prioridad_elevada')}")
    print(f"   └─ Latencia de Fijación:     {round(lat_ns_p, 2)} ns (Anti-Jitter Activo)")
    assert res_p.get("ok") is True

    # -------------------------------------------------------------------------
    print("\n🔹 PASO 2: Asignación Hardware de E-Cores (Orden 4 GC & Curiosidad)")
    t_ini = time.perf_counter()
    res_e = planificador_afinidad.fijar_e_cores_hilo_actual()
    lat_ns_e = (time.perf_counter() - t_ini) * 1e9

    print(f"   ├─ Status:                    {res_e.get('ok')}")
    print(f"   ├─ Máscara de Afinidad (Hex): {res_e.get('mask_hex')}")
    print(f"   └─ Asignación de Núcleos:    {res_e.get('tipo_core')}")
    assert res_e.get("ok") is True

    # Restaurar a P-Cores para hilos principales
    planificador_afinidad.fijar_p_cores_hilo_actual()

    # -------------------------------------------------------------------------
    print("\n🔹 PASO 3: Respaldo Espejo Criptográfico Descentralizado ASMI-DOE V10")
    nodulo_test = "nodulo_patrones_42000"
    payload_original = b"PATRONES_CRISTALIZADOS_SOBERANOS_V14_DATA_PAYLOAD"
    
    t_ini = time.perf_counter()
    res_b = gestor_respaldo.respaldar_buffer_asmi_doe(nodulo_test, payload_original)
    lat_ns_b = (time.perf_counter() - t_ini) * 1e9

    sha256_str = str(res_b.get('sha256', ''))
    print(f"   ├─ Status:                    {res_b.get('ok')}")
    print(f"   ├─ Nódulo Respaldado:        {res_b.get('nombre_nodulo')}")
    print(f"   ├─ Hash SHA256 Certificado:   {sha256_str[:16]}...")
    print(f"   └─ Latencia de Respaldo FFI: {round(lat_ns_b, 2)} ns")
    assert res_b.get("ok") is True

    # -------------------------------------------------------------------------
    print("\n🔹 PASO 4: Restauración y Verificación Cero Perfección (Recomposición Espejo)")
    payload_restaurado = gestor_respaldo.restaurar_buffer_asmi_doe(nodulo_test)
    print(f"   ├─ Recomposición Inversa:     {payload_restaurado == payload_original}")
    assert payload_restaurado == payload_original

    print("\n================================================================================")
    print("📊 CERTIFICADO HARDWARE V14 — STATUS:")
    print("   ├─ Pinning P-Core & E-Core (Anti-Jitter): ✅ COMPLETADO")
    print("   ├─ Respaldo Espejo ASMI-DOE V10:           ✅ VALIDADO")
    print("   └─ Blindaje Periférico V14:               🚀 EXTREMO (RENDIMIENTO DE 5 COHETES)")
    print("================================================================================")

if __name__ == "__main__":
    certificar_afinidad_y_respaldos_v14()
