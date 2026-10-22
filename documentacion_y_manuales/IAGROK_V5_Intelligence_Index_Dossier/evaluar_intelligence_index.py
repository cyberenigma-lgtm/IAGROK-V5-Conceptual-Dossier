#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 IAGROK V5 — EVALUADOR OFICIAL DEL INTELLIGENCE INDEX (VS QUASAR 43 PUNTOS)
Ubicación: c:\\IAGROK\\evaluar_intelligence_index.py

Punto de Entrada Principal para la Medición Telemétrica de la Arquitectura Soberana IAGROK V5.
"""

import os
import sys
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from arquitectura_cognitiva.intelligence_index_harness import IntelligenceIndexHarness

def main():
    parser = argparse.ArgumentParser(description="Evaluador del Intelligence Index para IAGROK V5")
    parser.add_argument("--modo", choices=["rapido", "completo"], default="completo", help="Modo de ejecución del benchmark (rapido o completo)")
    args = parser.parse_args()

    es_rapido = (args.modo == "rapido")
    harness = IntelligenceIndexHarness(modo_rapido=es_rapido)
    harness.ejecutar_evaluacion_completa()

if __name__ == "__main__":
    main()
