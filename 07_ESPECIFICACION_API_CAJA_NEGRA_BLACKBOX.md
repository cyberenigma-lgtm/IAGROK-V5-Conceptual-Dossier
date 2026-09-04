# 🌐 Especificación Oficial de la API de Caja Negra (Black-Box Endpoint)

> **Documentación del Endpoint Público para Auditorías Externas de la Arquitectura IAGROK V5**  
> **Autor y Titular de la Propiedad Intelectual:** José Manuel Moreno Cano  
> **Registro Internacional Safe Creative:** ID `2609046909131`

---

## 📡 Endpoint de Auditoría en Tiempo Real

### `POST /api/neurobus7/pensar`

Este endpoint permite a auditores externos, comités científicos y laboratorios evaluar el motor cognitivo de **IAGROK V5** mediante peticiones de caja negra (*Black-Box Testing*), sin exponer el código ejecutable privado ni las librerías nativas C/Rust.

#### 📥 Estructura de la Petición (Request Payload):

```json
{
  "prompt": "Generar un algoritmo soberano en Rust para sincronizar memoria de trabajo.",
  "contexto": {
    "auditor": "Comité Técnico Independiente",
    "modo_prueba": "BlackBox_ZeroKnowledge"
  }
}
```

---

#### 📤 Estructura de la Respuesta Cifrada / Telemétrica (Response Payload):

```json
{
  "ok": true,
  "resultado": {
    "estado": "OK",
    "tiempo_ms": 0.3235,
    "fase_1_logica": {
      "pipeline_activado": ["L30_COGNITIVE_AUDITOR"],
      "resumen": "Evaluación analítica completada",
      "valido": true
    },
    "fase_2_creativa": {
      "estilo": "Soberano Elegante",
      "pipeline_activado": ["R30_CREATIVE_ASSIMILATOR"]
    },
    "fase_3_resonancia": {
      "indice_coherencia": 1.0,
      "resumen_resonante": "Resonancia Armónica [100%]: Lógica (0 hallazgos) / Creatividad (0 IAs / Soberano Elegante)",
      "total_resonancias": 2
    },
    "fase_4_conciencia": {
      "foco_atencional": "Blindaje_Dimensional",
      "nivel_conciencia": "Vigilante_V5",
      "salud_cognitiva": 1.0
    },
    "estadisticas_bus": {
      "gestor_ram": "16GB_DDR5_OPTIMIZADO",
      "memoria_cristalizada": {
        "total_cristalizaciones": 1261,
        "cristalizaciones_ram_hot": 1261,
        "cristalizaciones_impar_blindadas": 635
      },
      "vram_virtual_swap_E": {
        "activo": true,
        "espacio_libre_gb": 536.83
      }
    }
  }
}
```

---

## 🔒 Garantía de Seguridad de Propiedad Intelectual
- **Cero Exposición de Código**: El cliente únicamente recibe la respuesta estructurada en JSON.
- **Procesamiento 100% Local / Soberano**: El motor ejecuta la malla de 60 sub-conciencias dentro del servidor cerrado del autor.
- **Verificabilidad Instantánea**: Comprobación en vivo de la velocidad sub-milisegundo (`0.32 ms`) y la resonancia armónica `100%`.
