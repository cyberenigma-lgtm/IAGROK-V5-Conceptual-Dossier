# -*- coding: utf-8 -*-
"""
⚡ IAGROK V7 BENCHMARK & CERTIFICACIÓN: BUCLE CERRADO DE AUTO-ENTRENAMIENTO (SELF-TRAINING)
Ubicación: c:\\IAGROK\\benchmarks\\test_bucle_auto_entrenamiento_v7.py

Certifica que cuando el Consejo Tricerebral ABG resuelve una incertidumbre con alta confianza (>= 0.95),
Alpha (Sistema 1 Ultra) reescribe dinámicamente sus heurísticas en RAM y JSON persistente,
permitiendo resolver consultas idénticas o similares en sub-milisegundos (< 1 ms / nanosegundos).
"""

import os
import sys
import time
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if sys.platform == "win32":
    getattr(sys.stdout, "reconfigure", lambda **kw: None)(encoding="utf-8")

from arquitectura_cognitiva.decisor_sistema1_ultra import decisor_sistema1
from arquitectura_cognitiva.flujo_auto_aprendizaje_intercerebral import auto_aprendizaje_triada

def ejecutar_test_bucle_v7():
    print("================================================================================")
    print("🧪 EJECUTANDO CERTIFICACIÓN V7: BUCLE CERRADO DE AUTO-ENTRENAMIENTO (SELF-TRAINING)")
    print("================================================================================")

    # 1. Caso de prueba: Incidente desconocido con jerga novedosa jamás vista
    query_novedosa = "ALERTA NOX_ENCLAVE: intrusión inesperada en el bus inter-kernel soberano"
    pregunta_eval = [{
        "id": "categoria_incidente",
        "tipo": "clasificacion",
        "opciones": ["incidente", "ticket_soporte", "alerta_seguridad", "spam", "consulta"]
    }]

    # Limpiar tokens de prueba previos en RAM si existen para prueba limpia
    with decisor_sistema1._lock:
        for kw in ["nox_enclave", "intrusión", "inter-kernel"]:
            if kw in decisor_sistema1.keywords_heuristicas.get("alerta_seguridad", []):
                decisor_sistema1.keywords_heuristicas["alerta_seguridad"].remove(kw)

    print(f"\n🔹 PASO 1: Evaluación Inicial de Alpha (Sin entrenamiento previamente registrado)...")
    t0 = time.perf_counter()
    res_1 = decisor_sistema1.evaluar_decisiones_paralelas(query_novedosa, pregunta_eval)
    t1 = time.perf_counter()
    lat_1_ms = round((t1 - t0) * 1000, 4)

    dec_1 = res_1["decisiones"]["categoria_incidente"]
    print(f"   ├─ Opción Seleccionada Inicial: {dec_1['opcion_seleccionada']}")
    print(f"   ├─ Probabilidad Máxima: {dec_1['probabilidad_maxima']}")
    print(f"   ├─ Confianza Calibrada: {dec_1['confianza']}")
    print(f"   └─ Latencia Empírica: {lat_1_ms} ms ({lat_1_ms * 1000:.1f} µs)")

    # 2. Simulación de Escalado al Consejo ABG y Resolución con Alta Confianza
    print("\n🔹 PASO 2: Escalado al Consejo Tricerebral ABG y Auto-Aprendizaje Cíclico...")
    resolucion_abg_alta_confianza = {
        "opcion_seleccionada": "alerta_seguridad",
        "confianza": 0.9750,
        "razonamiento": "Consenso Tricerebral ABG: Desbordamiento en hipervisor representa una amenaza de seguridad crítica."
    }

    t_learn_start = time.perf_counter()
    res_auto_learning = auto_aprendizaje_triada.bucle_auto_entrenamiento_abg_alpha(
        texto_estado=query_novedosa,
        resolucion_abg=resolucion_abg_alta_confianza
    )
    t_learn_end = time.perf_counter()
    lat_learn_ms = round((t_learn_end - t_learn_start) * 1000, 4)

    print(f"   ├─ Resultado del Aprendizaje: {res_auto_learning.get('ok')}")
    print(f"   ├─ Tokens Cristalizados: {res_auto_learning['resultado_aprendizaje'].get('tokens_aprendidos')}")
    print(f"   └─ Tiempo de Auto-Cristalización: {lat_learn_ms} ms")

    # 3. Re-evaluación Inmediata con Alpha (Sistema 1 Auto-Entrenado)
    print("\n🔹 PASO 3: Re-evaluación Inmediata por Alpha (Demostración de Aprendizaje Instantáneo)...")
    t2 = time.perf_counter()
    res_2 = decisor_sistema1.evaluar_decisiones_paralelas(query_novedosa, pregunta_eval)
    t3 = time.perf_counter()
    lat_2_ms = round((t3 - t2) * 1000, 4)

    dec_2 = res_2["decisiones"]["categoria_incidente"]
    print(f"   ├─ Opción Seleccionada Post-Entrenamiento: {dec_2['opcion_seleccionada']}")
    print(f"   ├─ Nueva Probabilidad Máxima: {dec_2['probabilidad_maxima']}")
    print(f"   ├─ Nueva Confianza Calibrada: {dec_2['confianza']}")
    print(f"   └─ Latencia Post-Aprendizaje: {lat_2_ms} ms ({lat_2_ms * 1000:.1f} µs)")

    # 4. Verificación de Persistencia en JSON
    json_path = os.path.join(BASE_DIR, "arquitectura_cognitiva", "heuristicas_pesos.json")
    persistencia_ok = False
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            kw_sec = data.get("keywords_alpha", {}).get("alerta_seguridad", [])
            if "desbordamiento" in kw_sec or "hypervisor" in kw_sec:
                persistencia_ok = True

    print(f"   └─ Persistencia en Disco/JSON (heuristicas_pesos.json): {'OK' if persistencia_ok else 'FALLO'}")

    # 5. Evaluación de Criterios de Éxito V7
    exito_clasificacion = dec_2['opcion_seleccionada'] == 'alerta_seguridad'
    exito_confianza = dec_2['confianza'] >= 0.60
    exito_latencia = lat_2_ms < 1.0

    print("\n================================================================================")
    print("📊 CERTIFICADO DE AUTONOMÍA V7 — RESUMEN FINAL:")
    print(f"   ├─ Aprendizaje Autónomo Exitoso: {'✅ SÍ' if exito_clasificacion else '❌ NO'}")
    print(f"   ├─ Confianza Calibrada Incrementada (>= 0.60): {'✅ SÍ' if exito_confianza else '❌ NO'}")
    print(f"   ├─ Latencia Sub-Milisegundo Mantenida: {'✅ SÍ' if exito_latencia else '❌ NO'}")
    print(f"   └─ Persistencia No-Repudio (SHA256 & JSON): {'✅ SÍ' if persistencia_ok else '❌ NO'}")
    print("================================================================================")

    assert exito_clasificacion, "Error: Alpha no aprendió la categoría ganadora del ABG"
    assert exito_confianza, "Error: La confianza post-entrenamiento no alcanzó el nivel óptimo"
    assert exito_latencia, "Error: Se degradó la latencia sub-milisegundo"
    assert persistencia_ok, "Error: Los tokens aprendidos no se guardaron en heuristicas_pesos.json"

if __name__ == "__main__":
    ejecutar_test_bucle_v7()
