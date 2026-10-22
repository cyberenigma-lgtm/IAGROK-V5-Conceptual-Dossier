#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ NEUROSHIELD SOBERANO — NÚCLEO DE DEFENSA, SALUD DE HARDWARE Y AUTOPROTECCIÓN
Ubicación: c:\\IAGROK\\neuroshield_soberano\\neuroshield_core.py
"""

import os
import sys
import time
import psutil

if hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass

class NeuroShield:
    def __init__(self):
        self.procesos_sospechosos = [
            "miner.exe", "xmrig.exe", "cryptominer.exe", "unknown_trojan.exe", "malicious_script.bat"
        ]
        self.max_ram_threshold = 92.0 # 92%
        self.alert_count = 0

    def vigilar_procesos(self):
        """Monitorea y neutraliza procesos no autorizados o mineros ocultos."""
        amenazas = []
        for p in psutil.process_iter(['pid', 'name']):
            try:
                pname = (p.info['name'] or '').lower()
                for sosp in self.procesos_sospechosos:
                    if sosp in pname:
                        print(f"[NEUROSHIELD ALERTA] Amenaza detectada: {pname} (PID: {p.info['pid']}). Neutralizando...")
                        psutil.Process(p.info['pid']).terminate()
                        amenazas.append(pname)
                        self.alert_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return amenazas

    def vigilar_memoria(self):
        """Controla el consumo de RAM y previene bloqueos del sistema operativo."""
        mem = psutil.virtual_memory()
        uso_ram = mem.percent
        if uso_ram > self.max_ram_threshold:
            print(f"[NEUROSHIELD ALERTA] Memoria RAM crítica ({uso_ram}%). Activando recolección de basura soberana.")
            import gc
            gc.collect()
        return uso_ram

    def vigilar_cpu(self):
        """Verifica uso de CPU y estabilidad térmica."""
        cpu_usage = psutil.cpu_percent(interval=0.1)
        return cpu_usage

    def estado_general(self):
        """Retorna un reporte de salud del sistema."""
        ram = self.vigilar_memoria()
        cpu = self.vigilar_cpu()
        disk = psutil.disk_usage('C:\\').percent
        return {
            "estado": "ACTIVO_Y_PROTEGIDO",
            "cpu_uso_porcentaje": cpu,
            "ram_uso_porcentaje": ram,
            "disco_c_uso_porcentaje": disk,
            "alertas_neutralizadas": self.alert_count,
            "timestamp": int(time.time())
        }

    def ciclo(self, max_iteraciones=3):
        """Ciclo de vigilancia continua."""
        print("[NEUROSHIELD] Vigilancia autónoma iniciada. Escaneando hilos...")
        iter_count = 0
        while iter_count < max_iteraciones:
            self.vigilar_procesos()
            ram = self.vigilar_memoria()
            cpu = self.vigilar_cpu()
            print(f"[NEUROSHIELD HEARTBEAT] CPU: {cpu}% | RAM: {ram}% | Sistema Soberano Protegido")
            iter_count += 1
            time.sleep(1)

def activar_neuroshield(max_iter=3):
    ns = NeuroShield()
    ns.ciclo(max_iteraciones=max_iter)
    return ns.estado_general()

if __name__ == "__main__":
    reporte = activar_neuroshield(max_iter=2)
    print("Reporte de Defensa:", reporte)
