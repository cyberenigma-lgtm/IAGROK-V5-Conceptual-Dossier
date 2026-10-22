#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ NEUROSHIELD SOBERANO — WATCHDOG DE AUTORREPARACIÓN EN CALIENTE (Módulo 7 & 8)
Ubicación: c:\\IAGROK\\neuroshield_soberano\\neuroshield_autoheal.py
Funcionalidades:
1. Monitor de Recursos de Hardware en tiempo real (CPU, RAM, Disco).
2. Auto-Pausa y Auto-Reanudación inteligente de renders pesados.
3. Centinela de Autorreparación de scripts: Intercepta fallos, corrige dependencias y relanza procesos.
"""

import os
import sys
import time
import psutil
import subprocess
import traceback

if hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

class NeuroShieldAutoHeal:
    def __init__(self, cpu_limit_percent=90.0, mem_limit_percent=88.0):
        self.cpu_limit = cpu_limit_percent
        self.mem_limit = mem_limit_percent
        print("[NeuroShield AutoHeal] 🛡️ Centinela de Autorreparación y Monitor de Hardware Activo")

    def verificar_recursos(self):
        """Monitorea el estado de la máquina."""
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent
        disco = psutil.disk_usage('C:\\').percent
        
        estado = {
            "cpu_percent": cpu,
            "mem_percent": mem,
            "disk_percent": disco,
            "sobrecargado": cpu > self.cpu_limit or mem > self.mem_limit
        }
        return estado

    def auto_pausa_inteligente(self, timeout_secs=15):
        """Si la máquina está al límite, espera hasta que se estabilice."""
        est = self.verificar_recursos()
        if est["sobrecargado"]:
            print(f"[NeuroShield AutoHeal] ⚠️ Sobrecarga detectada (CPU: {est['cpu_percent']}%, RAM: {est['mem_percent']}%). Auto-pausando...")
            t0 = time.time()
            while self.verificar_recursos()["sobrecargado"] and (time.time() - t0 < timeout_secs):
                time.sleep(1.0)
            print("[NeuroShield AutoHeal] ✅ Recursos estabilizados. Reanudando ejecución...")

    def ejecutar_con_autorreparacion(self, comando_python, cwd=BASE_DIR, max_intentos=3):
        """
        Ejecuta un proceso; si falla, analiza el error, autorrepara el entorno y reintenta.
        """
        intento = 0
        while intento < max_intentos:
            intento += 1
            self.auto_pausa_inteligente()
            
            print(f"[NeuroShield AutoHeal] 🚀 Ejecutando (Intento {intento}/{max_intentos}): {comando_python}")
            res = subprocess.run(f"python {comando_python}", cwd=cwd, shell=True, capture_output=True, text=True)
            
            if res.returncode == 0:
                print(f"[NeuroShield AutoHeal] ✅ Comando finalizado con éxito en intento {intento}.")
                return True, res.stdout
            else:
                error_log = res.stderr
                print(f"[NeuroShield AutoHeal] ⚠️ Error detectado en script:\n{error_log[:300]}...")
                
                # Análisis de autorreparación
                if "ModuleNotFoundError" in error_log or "No module named" in error_log:
                    # Extraer módulo faltante y reparar
                    modulo = error_log.split("No module named")[-1].split("\n")[0].strip().strip("'").strip('"')
                    print(f"[NeuroShield AutoHeal] 🔧 Autorreparando: Instalando módulo faltante '{modulo}'...")
                    subprocess.run(f"pip install {modulo}", shell=True)
                elif "UnicodeEncodeError" in error_log:
                    print("[NeuroShield AutoHeal] 🔧 Autorreparando: Forzando codificación UTF-8 en entorno...")
                    os.environ["PYTHONIOENCODING"] = "utf-8"
                else:
                    time.sleep(0.5)

        return False, res.stderr

if __name__ == "__main__":
    shield = NeuroShieldAutoHeal()
    rec = shield.verificar_recursos()
    print(f"Estado de Hardware: CPU {rec['cpu_percent']}% | RAM {rec['mem_percent']}% | SSD {rec['disk_percent']}%")
