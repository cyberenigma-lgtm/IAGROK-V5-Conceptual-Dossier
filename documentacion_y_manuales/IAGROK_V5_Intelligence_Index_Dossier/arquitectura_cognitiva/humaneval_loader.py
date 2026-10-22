#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 IAGROK / NOXFERION — HUMANEVAL LOADER (164 PROBLEMAS OFICIALES)
Ubicación: c:\\IAGROK\\arquitectura_cognitiva\\humaneval_loader.py

Descarga y gestiona el dataset oficial HumanEval de OpenAI (164 problemas con aserciones).
"""

import os
import sys
import json
import gzip
import urllib.request
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "logs")
HUMANEVAL_PATH = os.path.join(DATA_DIR, "HumanEval.jsonl")
HUMANEVAL_URL = "https://raw.githubusercontent.com/openai/human-eval/master/data/HumanEval.jsonl.gz"

def descargar_humaneval_oficial() -> str:
    """Descarga e hidrata el dataset oficial HumanEval.jsonl."""
    os.makedirs(DATA_DIR, exist_ok=True)
    gz_path = os.path.join(DATA_DIR, "HumanEval.jsonl.gz")

    if not os.path.exists(HUMANEVAL_PATH):
        print(f"📥 Descargando HumanEval oficial desde OpenAI GitHub (master branch)...")
        try:
            req = urllib.request.Request(
                HUMANEVAL_URL, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req) as response, open(gz_path, 'wb') as out_file:
                out_file.write(response.read())

            with gzip.open(gz_path, 'rb') as f_in:
                with open(HUMANEVAL_PATH, 'wb') as f_out:
                    f_out.write(f_in.read())

            if os.path.exists(gz_path):
                os.remove(gz_path)
            print(f"✅ HumanEval descargado correctamente: {HUMANEVAL_PATH}")
        except Exception as e:
            print(f"⚠️ Error al descargar HumanEval: {e}.")
    return HUMANEVAL_PATH

def cargar_humaneval_problemas() -> List[Dict[str, Any]]:
    """Carga los 164 problemas del dataset HumanEval."""
    path = descargar_humaneval_oficial()
    problemas = []
    
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    problemas.append(json.loads(line))
    return problemas

if __name__ == "__main__":
    probs = cargar_humaneval_problemas()
    print(f"📊 Total de problemas cargados en HumanEval: {len(probs)}")
    if probs:
        print(f"Ejemplo Task 0: {probs[0]['task_id']} — Entry Point: {probs[0]['entry_point']}")
