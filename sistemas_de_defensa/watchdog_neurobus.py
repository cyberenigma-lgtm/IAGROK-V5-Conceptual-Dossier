# -*- coding: utf-8 -*-
r"""
👑 NEURO-OS DEFINITIVO / IAGROK V5 — WATCHDOG DE SUPERVISIÓN NEUROBUS Y SERVIDORES API
Ubicación: c:\IAGROK\watchdog_neurobus.py

Propósito:
- Supervisa y mantiene en ejecución continua el servidor Backend Flask y la Red Hive P2P (app.py).
- Reinicia automáticamente el servidor si cae o deja de responder.
"""

import os
import sys
import time
import urllib.request
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_SCRIPT = os.path.join(BASE_DIR, "app.py")

def main():
    print("[WATCHDOG NEUROBUS]: Supervisión activa de Servidores Backend Flask & Hive.")
    
    while True:
        # Verificar si el endpoint de Hive / status responde en puerto 5000
        url_status = "http://127.0.0.1:5000/api/cluster/info"
        server_responsive = False
        try:
            with urllib.request.urlopen(url_status, timeout=3) as resp:
                if resp.status == 200:
                    server_responsive = True
        except Exception:
            server_responsive = False

        if not server_responsive:
            print("[WATCHDOG NEUROBUS]: Servidor Flask/Hive inactivo. Lanzando app.py --backend --api-only...")
            flags = getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0) | getattr(subprocess, 'DETACHED_PROCESS', 0) | getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000)
            subprocess.Popen([sys.executable, APP_SCRIPT, "--backend", "--api-only"], cwd=BASE_DIR, creationflags=flags)
            # Esperar a que arranque
            for _ in range(15):
                time.sleep(1)
                try:
                    with urllib.request.urlopen(url_status, timeout=2) as resp:
                        if resp.status == 200:
                            print("[WATCHDOG NEUROBUS]: Servidor activado y respondiendo en http://127.0.0.1:5000")
                            break
                except Exception:
                    pass
        time.sleep(15)

if __name__ == "__main__":
    main()
