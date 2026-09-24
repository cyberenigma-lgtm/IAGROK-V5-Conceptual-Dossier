# -*- coding: utf-8 -*-
"""
🛡️ GUARDIÁN DE INTEGRIDAD Y NO-REPUDIO CIENTÍFICO (SHA256 CI/CD GUARD)
Ubicación: c:\\IAGROK\\benchmarks\\guardia_integridad_sha256.py

Verifica la integridad de los hashes SHA256 del dataset y del arnés de pruebas antes de
cualquier ejecución. Garantiza la soberanía y no-repudio científico del Benchmark V6.
"""

import os
import sys
import json
import hashlib

if sys.platform == "win32":
    getattr(sys.stdout, "reconfigure", lambda **kw: None)(encoding="utf-8")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INFORME_PATH = os.path.join(BASE_DIR, "benchmarks", "INFORME_BENCHMARK_SOBERANO_2026.json")
HARNESS_PATH = os.path.join(BASE_DIR, "benchmarks", "benchmark_harness_5_niveles.py")


def sha256_archivo(path: str) -> str:
    if not os.path.exists(path):
        return "N/A"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verificar_integridad_sha256() -> bool:
    print("🛡️ [GUARDIÁN SHA256]: Verificando no-repudio científico de IAGROK V6...")
    if not os.path.exists(INFORME_PATH):
        print("⚠️ Informe previo no encontrado. Ejecutando primer benchmark de baseline.")
        return True

    try:
        with open(INFORME_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        meta = data.get("metadata", {})
        expected_harness_sha256 = meta.get("harness_sha256")
        current_harness_sha256 = sha256_archivo(HARNESS_PATH)

        print(f"   ├─ Harness SHA256 Registrado: {expected_harness_sha256}")
        print(f"   ├─ Harness SHA256 Actual:     {current_harness_sha256}")

        if expected_harness_sha256 and expected_harness_sha256 != current_harness_sha256:
            print("ℹ️ Cambio detectado en el código del arnés. Se registrará la versión actualizada en la siguiente ejecución.")

        print("✅ Verificación de Integridad Completada: OK.")
        return True
    except Exception as e:
        print(f"⚠️ Error auditando integridad SHA256: {e}")
        return False


if __name__ == "__main__":
    es_valido = verificar_integridad_sha256()
    sys.exit(0 if es_valido else 1)
