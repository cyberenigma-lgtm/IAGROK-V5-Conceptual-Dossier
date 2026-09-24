#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path: sys.path.insert(0, BASE_DIR)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from arquitectura_cognitiva.enjambre_soberano_p2p import enjambre_p2p, EnjambreSoberanoP2P
from arquitectura_cognitiva.auto_genesis_recompilador import auto_genesis

def certificar_v17_enjambre_y_autogenesis():
    print("================================================================================")
    print("⚡ EJECUTANDO CERTIFICACIÓN V17: ENJAMBRES P2P & AUTO-GÉNESIS HOT-RELOAD")
    print("================================================================================")

    # -------------------------------------------------------------------------
    print("\n🔹 PASO 1: Intercambio Criptográfico P2P entre Nodo Par (102) y Nodo Impar (103)")
    payload_original = b"BLOQUE_PATRONES_ENJAMBRE_SOBERANO_DATA_CELL_V17"
    
    # Nodo Par (ID: 102)
    nodo_par = EnjambreSoberanoP2P(local_node_id=102)
    pkt_par = nodo_par.crear_paquete_sincronizacion(payload_original)
    res_par = enjambre_p2p.recibir_y_descomprimir_paquete(pkt_par)

    print(f"   ├─ Status Nodo Par (102):     {res_par.get('ok')}")
    print(f"   ├─ Node ID Identificado:     {res_par.get('node_id')}")
    print(f"   ├─ Recomposición de Payload:  {res_par.get('payload') == payload_original}")
    assert res_par.get("ok") is True and res_par.get("payload") == payload_original

    # Nodo Impar (ID: 103) — Criptografía Espejo Inverso
    nodo_impar = EnjambreSoberanoP2P(local_node_id=103)
    pkt_impar = nodo_impar.crear_paquete_sincronizacion(payload_original)
    res_impar = enjambre_p2p.recibir_y_descomprimir_paquete(pkt_impar)

    print(f"   ├─ Status Nodo Impar (103):   {res_impar.get('ok')}")
    print(f"   ├─ Node ID Identificado:     {res_impar.get('node_id')}")
    print(f"   ├─ Descompresión Espejo OK:  {res_impar.get('payload') == payload_original}")
    assert res_impar.get("ok") is True and res_impar.get("payload") == payload_original

    # -------------------------------------------------------------------------
    print("\n🔹 PASO 2: Auto-Génesis Engine — Recompilación y Hot-Reload en Caliente")
    t_ini = time.perf_counter()
    res_ag = auto_genesis.evaluar_y_recompilar_en_caliente(forzar=True)
    lat_ns_ag = (time.perf_counter() - t_ini) * 1e9

    print(f"   ├─ Status Auto-Génesis:       {res_ag.get('ok')}")
    print(f"   ├─ Recompilación Cargo:       {res_ag.get('recompilado')}")
    print(f"   ├─ Recarga FFI en Caliente:   {res_ag.get('recargado_ffi')}")
    print(f"   ├─ Modo de Ejecución:        {res_ag.get('modo')}")
    print(f"   └─ Tiempo Total Reconstrucción: {round(lat_ns_ag / 1e6, 2)} ms")
    assert res_ag.get("ok") is True and res_ag.get("recargado_ffi") is True

    print("\n================================================================================")
    print("📊 CERTIFICADO V17 — STATUS:")
    print("   ├─ Protocolo P2P de Enjambres Soberanos:  ✅ COMPLETADO")
    print("   ├─ Auto-Génesis Hot-Reload en Caliente: ✅ VALIDADO")
    print("   └─ Soberanía Extrema V17:                 🚀 EXTREMO (RENDIMIENTO DE 5 COHETES)")
    print("================================================================================")

if __name__ == "__main__":
    certificar_v17_enjambre_y_autogenesis()
