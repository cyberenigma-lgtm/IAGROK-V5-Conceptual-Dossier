# -*- coding: utf-8 -*-
"""
Generador de Huellas Criptográficas SHA-256 para Sellado Temporal
Obra: Arquitectura Computacional Cognitiva Soberana IAGROK V5
Autor Exclusivo: José Manuel Moreno (JMM)
"""

import hashlib
import os
from pathlib import Path
from datetime import datetime

DIR_DOSSIER = Path(__file__).parent

def calcular_hash_sha256(filepath: Path) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def generar_reporte_hashes():
    print("=================================================================")
    print("=== GENERANDO FIRMAS SHA-256 PARA REGISTRO DE PROPIEDAD INTELECTUAL ===")
    print("   Autor Exclusivo: José Manuel Moreno (JMM)")
    print(f"   Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=================================================================\n")

    archivos_md = sorted(list(DIR_DOSSIER.glob("*.md")))
    hashes_dict = {}

    for f in archivos_md:
        h = calcular_hash_sha256(f)
        hashes_dict[f.name] = h
        print(f"  * {f.name}\n    SHA-256: {h}\n")

    index_path = DIR_DOSSIER / "06_INDEX_Y_CERTIFICADO_ESTRUCTURA_PROCESOS.md"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as file_in:
            content = file_in.read()

        seccion_hashes = "\n\n### 🛡️ Firmas SHA-256 Calculadas:\n```txt\n"
        for name, h in hashes_dict.items():
            seccion_hashes += f"{name}: {h}\n"
        seccion_hashes += "```\n"

        if "### 🛡️ Firmas SHA-256 Calculadas:" in content:
            content = content.split("### 🛡️ Firmas SHA-256 Calculadas:")[0] + seccion_hashes.strip()
        else:
            content += seccion_hashes

        with open(index_path, "w", encoding="utf-8") as file_out:
            file_out.write(content)
        print("[OK] Certificado 06_INDEX_Y_CERTIFICADO_ESTRUCTURA_PROCESOS.md actualizado con las firmas SHA-256.")

if __name__ == "__main__":
    generar_reporte_hashes()
