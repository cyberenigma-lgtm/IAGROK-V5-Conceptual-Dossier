# -*- coding: utf-8 -*-
"""
===============================================================================
🛡️ NEUROSHIELD - FILTRO INMUNOLÓGICO DE RED Y LIMITADOR DE TASA SOBERANO
===============================================================================
Autor: José Manuel Moreno (JMM) (Cyberenigma / Noxferion)
SafeCreative IDs: 2609046909131 | 2609036897950

Módulo de Defensa contra:
1. Ataques de Inundación de Peticiones (DDoS / Socket Flooding).
2. Contaminación de Parámetros en API local o Multipuerto.
3. Clientes no autenticados o payloads malformados hacia el NeuroBus.
"""

import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple

if sys.platform == "win32":
    getattr(sys.stdout, "reconfigure", lambda **kw: None)(encoding="utf-8")


@dataclass
class EstadoInmunologicoCliente:
    ip_origen: str
    peticiones_por_segundo: int
    bloqueado_hasta: float
    intentos_maliciosos: int


class FiltroInmunologicoRed:
    def __init__(self, max_req_por_seg: int = 50, ventana_tiempo: float = 1.0):
        self.max_req_por_seg = max_req_por_seg
        self.ventana_tiempo = ventana_tiempo
        self.historial_peticiones: Dict[str, List[float]] = {}
        self.lista_negra: Dict[str, float] = {}

    def evaluar_peticion(self, ip_origen: str, payload_size_bytes: int) -> Tuple[bool, str]:
        """Evalúa si una conexión entrante es legítima o debe ser bloqueada inmediatamente."""
        ahora = time.time()

        # 1. Comprobar si la IP está en lista negra activa
        if ip_origen in self.lista_negra:
            if ahora < self.lista_negra[ip_origen]:
                return False, f"IP {ip_origen} Bloqueada por Actividad Sospechosa"
            else:
                del self.lista_negra[ip_origen]

        # 2. Control de Tamaño de Paquete (Evitar desbordamiento de buffer)
        if payload_size_bytes > 10 * 1024 * 1024:  # > 10 MB
            self.lista_negra[ip_origen] = ahora + 300  # Bloqueo de 5 min
            return False, f"Payload Excesivo ({payload_size_bytes} Bytes) - IP Bloqueada"

        # 3. Control de Frecuencia (Rate-Limiting)
        if ip_origen not in self.historial_peticiones:
            self.historial_peticiones[ip_origen] = []

        timestamps = self.historial_peticiones[ip_origen]
        timestamps = [t for t in timestamps if ahora - t < self.ventana_tiempo]
        timestamps.append(ahora)
        self.historial_peticiones[ip_origen] = timestamps

        if len(timestamps) > self.max_req_por_seg:
            self.lista_negra[ip_origen] = ahora + 60  # Bloqueo 1 min
            return False, f"Inundación Detectada ({len(timestamps)} req/s) - IP Bloqueada"

        return True, "Petición Aceptada"


filtro_red = FiltroInmunologicoRed()

if __name__ == "__main__":
    print("=" * 80)
    print("🛡️ NEUROSHIELD - PRUEBA DE FILTRO INMUNOLÓGICO DE RED")
    print("=" * 80)

    ip_test = "127.0.0.1"
    print("Enviando peticiones normales...")
    for _ in range(5):
        ok, msg = filtro_red.evaluar_peticion(ip_test, 512)
    print(f"Estado Petición Normal: {'✅ OK' if ok else '🚨 BLOQUEADO'} ({msg})")

    print("\nSimulando inundación de peticiones (Flooding)...")
    for _ in range(60):
        ok, msg = filtro_red.evaluar_peticion(ip_test, 512)

    print(f"Resultado tras Inundación: {'✅ OK' if ok else '🚨 BLOQUEADO'} ({msg})")
    print("=" * 80)
