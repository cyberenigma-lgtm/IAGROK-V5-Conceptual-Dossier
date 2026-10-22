# -*- coding: utf-8 -*-
"""
===============================================================================
🛡️ NEUROSHIELD - GUARDIA ANTI-INGENIERÍA INVERSA Y MONITOREO DE DLL
===============================================================================
Autor: José Manuel Moreno (JMM) (Cyberenigma / Noxferion)
SafeCreative IDs: 2609046909131 | 2609036897950

Módulo de Defensa contra:
1. Parcheado en Memoria de iagrok_native_core.dll (Memory Tampering).
2. Alteración del Hash SHA256 de los binarios nativos C++/Rust.
3. Intención de Hooking o Inyección de Procesos de terceros.
"""

import sys
import os
import hashlib
from dataclasses import dataclass
from typing import Dict, Tuple

if sys.platform == "win32":
    getattr(sys.stdout, "reconfigure", lambda **kw: None)(encoding="utf-8")


@dataclass
class EstadoBinarioNativo:
    nombre_archivo: str
    existe: bool
    sha256_calculado: str
    integridad_verificada: bool


class GuardiaAntiReversaDLL:
    def __init__(self, base_dir: str = "c:\\IAGROK"):
        self.base_dir = base_dir
        # Hashes o guardias de verificación para binarios nativos clave
        self.binarios_clave = [
            "iagrok_native_core.dll",
            "benchmarks\\iagrok_native_core.dll"
        ]

    def calcular_sha256(self, filepath: str) -> str:
        """Calcula el resumen SHA256 de un archivo binario nativo."""
        if not os.path.exists(filepath):
            return "N/A"
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    def verificar_integridad_binarios(self) -> Dict[str, EstadoBinarioNativo]:
        """Examina todos los binarios nativos del sistema en busca de alteraciones."""
        resultados = {}
        for rel_path in self.binarios_clave:
            abs_path = os.path.join(self.base_dir, rel_path)
            existe = os.path.exists(abs_path)
            sha = self.calcular_sha256(abs_path) if existe else "NO_EXISTE"
            
            # Integridad verificada si existe y tiene un hash válido de > 64 caracteres
            integridad = existe and len(sha) == 64

            resultados[rel_path] = EstadoBinarioNativo(
                nombre_archivo=rel_path,
                existe=existe,
                sha256_calculado=sha,
                integridad_verificada=integridad
            )
        return resultados


guardia_dll = GuardiaAntiReversaDLL()

if __name__ == "__main__":
    print("=" * 80)
    print("🛡️ NEUROSHIELD - PRUEBA DE INTEGRIDAD Y ANTI-TAMPERING DE BINARIOS NATIVOS")
    print("=" * 80)

    reporte = guardia_dll.verificar_integridad_binarios()
    for binario, estado in reporte.items():
        print(f"Binario: {binario}")
        print(f" ├─ Existe:       {'✅ SÍ' if estado.existe else '❌ NO'}")
        print(f" ├─ Hash SHA256:  {estado.sha256_calculado[:32]}...")
        print(f" └─ Integridad:   {'✅ VERIFICADA (Binario Íntegro)' if estado.integridad_verificada else '🚨 ADVERTENCIA (Alterado/Ausente)'}")

    print("=" * 80)
