# -*- coding: utf-8 -*-
"""
===============================================================================
🥊 NEUROSHIELD - DEFENDEDOR STREET FIGHTER "ROUND 1... FIGHT! INSERT COIN! 🪙"
===============================================================================
Autor: José Manuel Moreno (JMM) (Cyberenigma / Noxferion)
SafeCreative IDs: 2609046909131 | 2609036897950

Módulo de Trampa y Contramedida Estilo Street Fighter para:
1. Inundación de Recursos (CPU / RAM / Socket Exhaustion).
2. Escalado de Privilegios o Inyección Admin no autorizados.
3. Banner Arcade Street Fighter "ROUND 1... FIGHT! -> YOU LOSE! INSERT COIN! 🪙".
"""

import sys
import time
from dataclasses import dataclass
from typing import Tuple, Dict

if sys.platform == "win32":
    getattr(sys.stdout, "reconfigure", lambda **kw: None)(encoding="utf-8")


PANTALLA_STREET_FIGHTER_INSERT_COIN = """
===============================================================================
🥊  S T R E E T   F I G H T E R  -  N E U R O S H I E L D   E D I T I O N
===============================================================================

       ATTACKER  [--------------------] HP: 0%   ---> YOU LOSE! 💀
       IAGROK    [████████████████████] HP: 100% ---> PERFECT KO! 🏆

            ┌───────────────────────────────────────────────┐
            │                                               │
            │             🔔  ROUND 1... FIGHT!             │
            │                                               │
            │   💥 ATTACK NEUTRALIZED BY RING-0 C++ KERNEL │
            │   🛡️ SOBERANÍA SILICIO: PERFECT KO!          │
            │                                               │
            │  💬 "SIGUE INTENTÁNDOLO... ¡INSERT COIN! 🪙"  │
            │                                               │
            └───────────────────────────────────────────────┘

                 [ CREDIT: 0 / 1 COIN REQUIRED TO CONTINUE ]
                    CONTINUE? 9... 8... 7... INSERT COIN!
===============================================================================
"""


@dataclass
class RespuestaDefensaArcade:
    bloqueado: bool
    pantalla_arcade: str
    log_auditoria: str


class DefensaArcadeInsertCoin:
    def __init__(self, umbral_memoria_mb: float = 500.0, max_intentos_privilegio: int = 3):
        self.umbral_memoria_mb = umbral_memoria_mb
        self.max_intentos_privilegio = max_intentos_privilegio
        self.intentos_por_ip: Dict[str, int] = {}

    def detectar_ataque_y_responder(self, ip_origen: str, intentando_escalado_admin: bool, bytes_solicitados: int) -> RespuestaDefensaArcade:
        """
        Analiza si el cliente está intentando un ataque de inundación de recursos o privilegios.
        En caso afirmativo, despliega la pantalla Arcade Street Fighter 'ROUND 1... FIGHT! INSERT COIN!'.
        """
        ahora = time.time()
        intentos = self.intentos_por_ip.get(ip_origen, 0)

        es_ataque = False
        razon = ""

        if intentando_escalado_admin:
            intentos += 1
            self.intentos_por_ip[ip_origen] = intentos
            if intentos >= self.max_intentos_privilegio:
                es_ataque = True
                razon = f"Inundación de Privilegios ({intentos} intentos)"

        if bytes_solicitados > 50 * 1024 * 1024:  # > 50 MB
            es_ataque = True
            razon = f"Ataque de Agotamiento de Recursos (RAM Flood {bytes_solicitados / (1024*1024):.1f} MB)"

        if es_ataque:
            log_msg = f"🥊 KO TÉCNICO [{ip_origen}] - {razon} | STREET FIGHTER DEFENSE TRIGGERED"
            return RespuestaDefensaArcade(
                bloqueado=True,
                pantalla_arcade=PANTALLA_STREET_FIGHTER_INSERT_COIN,
                log_auditoria=log_msg
            )

        return RespuestaDefensaArcade(
            bloqueado=False,
            pantalla_arcade="",
            log_auditoria=f"Petición Legítima [{ip_origen}] OK"
        )


defensor_arcade = DefensaArcadeInsertCoin()


if __name__ == "__main__":
    print("=" * 80)
    print("🥊 NEUROSHIELD - PRUEBA DE DEFENSAS STREET FIGHTER 'ROUND 1... FIGHT!'")
    print("=" * 80)

    ip_atacante = "192.168.1.66"

    print("\nIniciando combate contra ataque de privilegios...")
    for i in range(1, 4):
        resp = defensor_arcade.detectar_ataque_y_responder(
            ip_origen=ip_atacante,
            intentando_escalado_admin=True,
            bytes_solicitados=1024
        )
        if resp.bloqueado:
            print(resp.log_auditoria)
            print(resp.pantalla_arcade)
        else:
            print(f"Intento {i}: {resp.log_auditoria}")

    print("=" * 80)
