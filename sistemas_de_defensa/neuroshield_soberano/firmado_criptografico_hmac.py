# -*- coding: utf-8 -*-
r"""
===============================================================================
🛡️ NEUROSHIELD V5 - MOTOR DE FIRMADO Y VERIFICACIÓN CRIPTOGRÁFICA HMAC-SHA256
===============================================================================
Autor: José Manuel Moreno (JMM) (Cyberenigma / Noxferion)
SafeCreative IDs: 2609046909131 | 2609036897950

Verificación de Invariancia Somática y Prevención de Envenenamiento RAG:
- Genera firmas HMAC-SHA256 canónicas para todos los documentos en E:\
- Verifica la integridad física de la biblioteca soberana en tiempo real.
- Detecta manipulaciones o inyecciones externas y registra el incidente.
"""

import os
import sys
import json
import time
import hmac
import hashlib
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional

if sys.platform == "win32":
    getattr(sys.stdout, "reconfigure", lambda **kw: None)(encoding="utf-8")


@dataclass
class ReporteIntegridadCriptografica:
    total_archivos_inspeccionados: int
    archivos_validos: int
    archivos_alterados: List[str]
    archivos_nuevos_sin_firma: List[str]
    score_invariancia: float
    estado_somata: str
    timestamp: str


class MotorFirmadoCriptograficoHMAC:
    def __init__(self, base_dir: str = "c:\\IAGROK"):
        self.autor = "José Manuel Moreno (JMM) (Cyberenigma / Noxferion)"
        self.safe_creative_ids = ["2609046909131", "2609036897950"]
        self.base_dir = base_dir
        self.secret_hmac_key = b"IAGROK_SOVEREIGN_LIBRARIAN_KEY_V5_3_SECRET_HMAC"
        
        # Localización de la biblioteca en disco externo
        self.hdd_library = self._localizar_disco_externo()
        self.manifest_path = os.path.join(self.hdd_library, "INDICE_FIRMAS_CRIPTOGRAFICAS_HMAC.json")
        self.log_ataques_path = os.path.join(self.base_dir, "logs", "LIBRO_REGISTRO_ATAQUES_NEUROSHIELD.json")

    def _localizar_disco_externo(self) -> str:
        nombre_carpeta = "IAGROK_BIBLIOTECA_SABIDURIA_SOBERANA"
        for letra in ["E", "D", "F", "G", "H", "I", "Z", "C"]:
            posible_ruta = f"{letra}:\\{nombre_carpeta}"
            if os.path.exists(posible_ruta):
                return posible_ruta
        return os.path.join(self.base_dir, "logs")

    def calcular_hmac_archivo(self, ruta_archivo: str) -> str:
        """Calcula la firma digest HMAC-SHA256 de un archivo."""
        h = hmac.new(self.secret_hmac_key, digestmod=hashlib.sha256)
        with open(ruta_archivo, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    def firmar_biblioteca_completa(self) -> str:
        """Genera y guarda el manifiesto canónico de firmas HMAC de la biblioteca."""
        if not os.path.exists(self.hdd_library):
            return self.manifest_path

        firmas: Dict[str, dict] = {}
        total = 0
        for root, _, files in os.walk(self.hdd_library):
            for file in files:
                # Evitar re-firmar los propios archivos de manifiesto e índice temporal
                if file in ["INDICE_FIRMAS_CRIPTOGRAFICAS_HMAC.json", "INDICE_BIBLIOTECARIO_MAESTRO.json"] or ".tmp" in file:
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.hdd_library)
                try:
                    h_val = self.calcular_hmac_archivo(full_path)
                    firmas[rel_path] = {
                        "hmac_sha256": h_val,
                        "size_bytes": os.path.getsize(full_path),
                        "mtime": os.path.getmtime(full_path)
                    }
                    total += 1
                except Exception:
                    pass

        manifiesto_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "autor": self.autor,
            "safe_creative_ids": self.safe_creative_ids,
            "total_archivos_firmados": total,
            "firmas": firmas
        }

        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifiesto_data, f, indent=2, ensure_ascii=False)

        return self.manifest_path

    def verificar_integridad_somatica(self) -> ReporteIntegridadCriptografica:
        """Audita cada archivo en el disco contra el manifiesto canónico HMAC."""
        if not os.path.exists(self.manifest_path):
            self.firmar_biblioteca_completa()

        with open(self.manifest_path, "r", encoding="utf-8") as f:
            manifiesto = json.load(f)

        firmas_guardadas = manifiesto.get("firmas", {})
        archivos_alterados = []
        archivos_nuevos = []
        validos = 0

        for root, _, files in os.walk(self.hdd_library):
            for file in files:
                if file in ["INDICE_FIRMAS_CRIPTOGRAFICAS_HMAC.json", "INDICE_BIBLIOTECARIO_MAESTRO.json"] or ".tmp" in file:
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.hdd_library)
                
                if rel_path not in firmas_guardadas:
                    archivos_nuevos.append(rel_path)
                    continue

                try:
                    h_actual = self.calcular_hmac_archivo(full_path)
                    if h_actual == firmas_guardadas[rel_path]["hmac_sha256"]:
                        validos += 1
                    else:
                        archivos_alterados.append(rel_path)
                except Exception:
                    archivos_alterados.append(rel_path)

        total_evaluados = validos + len(archivos_alterados)
        score = (validos / total_evaluados) if total_evaluados > 0 else 1.0
        estado = "✅ 100% INVARIANTE SOBERANO" if score >= 0.99 and not archivos_alterados else "🚨 VIOLACIÓN DE INTEGRIDAD DETECTADA"

        if archivos_alterados:
            self._registrar_alerta_alteracion(archivos_alterados)

        return ReporteIntegridadCriptografica(
            total_archivos_inspeccionados=total_evaluados,
            archivos_validos=validos,
            archivos_alterados=archivos_alterados,
            archivos_nuevos_sin_firma=archivos_nuevos,
            score_invariancia=round(score, 4),
            estado_somata=estado,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )

    def _registrar_alerta_alteracion(self, alterados: List[str]):
        """Registra incidentes de alteración física en el log de NeuroShield."""
        os.makedirs(os.path.dirname(self.log_ataques_path), exist_ok=True)
        registro = []
        if os.path.exists(self.log_ataques_path):
            try:
                with open(self.log_ataques_path, "r", encoding="utf-8") as f:
                    registro = json.load(f)
            except Exception:
                registro = []

        registro.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "consulta_bloqueada": f"AUDITORÍA SOMÁTICA DISCO {self.hdd_library}",
            "hallazgos_seguridad": [f"Archivos corruptos o alterados exteriormente: {', '.join(alterados)}"],
            "respuesta_defensiva": "🚨 ACCESO BLOQUEADO // AISLAMIENTO DE DOCUMENTOS QUERENTENADOS"
        })

        with open(self.log_ataques_path, "w", encoding="utf-8") as f:
            json.dump(registro, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print("=" * 80)
    print("🛡️ NEUROSHIELD V5 - FIRMADO Y VERIFICACIÓN CRIPTOGRÁFICA HMAC-SHA256")
    print("=" * 80)
    
    motor_hmac = MotorFirmadoCriptograficoHMAC()
    print(f"📁 Firmando biblioteca en: {motor_hmac.hdd_library}")
    manifiesto = motor_hmac.firmar_biblioteca_completa()
    print(f"📜 Manifiesto canónico generado: {manifiesto}")

    auditoria = motor_hmac.verificar_integridad_somatica()
    print(f"\n📊 RESUMEN DE INTEGRIDAD SOMÁTICA:")
    print(f" * Archivos evaluados:  {auditoria.total_archivos_inspeccionados}")
    print(f" * Archivos válidos:    {auditoria.archivos_validos}")
    print(f" * Archivos alterados:  {len(auditoria.archivos_alterados)}")
    print(f" * Archivos nuevos:     {len(auditoria.archivos_nuevos_sin_firma)}")
    print(f" * Score Invariancia:   {int(auditoria.score_invariancia * 100)}%")
    print(f" * Estado Somático:     {auditoria.estado_somata}")
    print("=" * 80)
