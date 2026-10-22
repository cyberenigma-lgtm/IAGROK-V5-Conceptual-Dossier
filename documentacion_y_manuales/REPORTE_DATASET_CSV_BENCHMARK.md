# 📊 INFORME OFICIAL DE EVALUACIÓN BENCHMARK RAG (30 PRUEBAS)

> **Titular de Derechos Exclusivos:** José Manuel Moreno (JMM)  
> **Certificado de Registro Internacional Safe Creative:** ID `2609046909131`  
> **Fecha de Auditoría:** `2026-09-19 19:25:03`  
> **Dataset Procesado:** [`iagrok_rag_benchmark_dataset.csv`](file:///C:/Users/cyber/Downloads/iagrok_rag_benchmark_dataset.csv)

---

## 🏆 Resumen Ejecutivo de Rendimiento

| Métrica de Evaluación RAG | Valor Promedio | Estado / Calificación |
| :--- | :---: | :---: |
| **Similitud Vectorial Coseno Media** | `0.8644` | 🟢 Alta Precisión Semántica 128D |
| **Relevancia del Contexto (Context Relevance)** | `88.97%` | 🟢 Extracción pertiente sin ruido |
| **Fidelidad LLM (Groundedness / Faithfulness)** | `84.60%` | 🟢 Transferencia fiel sin alucinación |
| **Latencia Promedio de Inferencia** | `292.33 ms` | ⚡ Ultra-rápida (Sub-300ms) |
| **Tasa de Éxito Global** | `83.33%` | **25 / 30 Pruebas Exitosas** |
| **PUNTUACIÓN GLOBAL PONDERADA** | **`86.21 / 100 PTS`** | 🏆 **SOBRESALIENTE (CEREBRO ALTO RENDIMIENTO)** |

---

## 🔴 Análisis de Componentes Críticos (5 Pruebas)

Los siguientes componentes presentaron una baja en la Fidelidad LLM (`<65%`), desencadenando alerta de atención para refuerzo de prompt en Anillo 0:

| ID Prueba | Componente Evaluado | Similitud | Relevancia | Fidelidad | Latencia | Score | Resultado |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `IAG-B-01` | Parámetro cuántico reactor OME... | `0.9511` | `94.64%` | `53.11%` | `317.0 ms` | **78.22** | 🔴 CRÍTICO |
| `IAG-B-06` | Token de autenticación rotativ... | `0.8051` | `85.84%` | `61.41%` | `240.0 ms` | **73.94** | 🔴 CRÍTICO |
| `IAG-B-11` | Parámetro cuántico reactor OME... | `0.8691` | `80.69%` | `44.27%` | `420.0 ms` | **68.61** | 🔴 CRÍTICO |
| `IAG-B-16` | Token de autenticación rotativ... | `0.8288` | `96.57%` | `53.6%` | `237.0 ms` | **73.91** | 🔴 CRÍTICO |
| `IAG-B-26` | Token de autenticación rotativ... | `0.8946` | `86.29%` | `41.1%` | `287.0 ms` | **69.48** | 🔴 CRÍTICO |

> 💡 **Recomendación de Autocuración:** Elevar la temperatura de grounding en `razonamiento_sistema2.py` para reforzar la transferencia exacta de tokens numéricos en claves rotativas y parámetros del reactor.

---

## 📋 Desglose Completo de las 30 Pruebas Evaluadas

| ID Prueba | Componente | Similitud | Relevancia | Fidelidad | Latencia | Score Total | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `IAG-B-01` | Parámetro cuántico reactor OME... | `0.9511` | `94.64%` | `53.11%` | `317.0 ms` | **78.22** | 🔴 CRÍTICO |
| `IAG-B-02` | Protocolo de emergencia nivel ... | `0.8081` | `81.16%` | `87.34%` | `405.0 ms` | **83.49** | ✅ ÉXITO |
| `IAG-B-03` | Llave maestra de encriptación ... | `0.9075` | `80.41%` | `94.02%` | `440.0 ms` | **89.99** | ✅ ÉXITO |
| `IAG-B-04` | Coordenadas de respaldo georen... | `0.8182` | `83.64%` | `97.49%` | `180.0 ms` | **88.45** | ✅ ÉXITO |
| `IAG-B-05` | Algoritmo de consenso PoW modi... | `0.8745` | `88.64%` | `89.56%` | `216.0 ms` | **88.53** | ✅ ÉXITO |
| `IAG-B-06` | Token de autenticación rotativ... | `0.8051` | `85.84%` | `61.41%` | `240.0 ms` | **73.94** | 🔴 CRÍTICO |
| `IAG-B-07` | Frecuencia de muestreo del sen... | `0.9213` | `83.99%` | `91.84%` | `289.0 ms` | **90.39** | ✅ ÉXITO |
| `IAG-B-08` | Umbral de alerta térmica en al... | `0.7884` | `92.15%` | `93.89%` | `176.0 ms` | **87.52** | ✅ ÉXITO |
| `IAG-B-09` | Puerto alternativo de escucha ... | `0.9508` | `99.31%` | `85.98%` | `386.0 ms` | **92.29** | ✅ ÉXITO |
| `IAG-B-10` | Semilla mnemónica para derivac... | `0.7976` | `93.68%` | `89.57%` | `265.0 ms` | **86.47** | ✅ ÉXITO |
| `IAG-B-11` | Parámetro cuántico reactor OME... | `0.8691` | `80.69%` | `44.27%` | `420.0 ms` | **68.61** | 🔴 CRÍTICO |
| `IAG-B-12` | Protocolo de emergencia nivel ... | `0.8993` | `86.23%` | `88.88%` | `291.0 ms` | **88.77** | ✅ ÉXITO |
| `IAG-B-13` | Llave maestra de encriptación ... | `0.8133` | `99.39%` | `93.20%` | `375.0 ms` | **89.69** | ✅ ÉXITO |
| `IAG-B-14` | Coordenadas de respaldo georen... | `0.9411` | `91.96%` | `99.09%` | `424.0 ms` | **95.67** | ✅ ÉXITO |
| `IAG-B-15` | Algoritmo de consenso PoW modi... | `0.8153` | `80.90%` | `86.33%` | `227.0 ms` | **83.32** | ✅ ÉXITO |
| `IAG-B-16` | Token de autenticación rotativ... | `0.8288` | `96.57%` | `53.60%` | `237.0 ms` | **73.91** | 🔴 CRÍTICO |
| `IAG-B-17` | Frecuencia de muestreo del sen... | `0.8777` | `82.82%` | `89.21%` | `384.0 ms` | **87.36** | ✅ ÉXITO |
| `IAG-B-18` | Umbral de alerta térmica en al... | `0.9576` | `95.44%` | `86.12%` | `185.0 ms` | **91.84** | ✅ ÉXITO |
| `IAG-B-19` | Puerto alternativo de escucha ... | `0.9268` | `94.14%` | `85.08%` | `360.0 ms` | **89.93** | ✅ ÉXITO |
| `IAG-B-20` | Semilla mnemónica para derivac... | `0.7933` | `87.17%` | `96.57%` | `158.0 ms` | **87.79** | ✅ ÉXITO |
| `IAG-B-21` | Parámetro cuántico reactor OME... | `0.8922` | `86.62%` | `70.21%` | `140.0 ms` | **81.10** | ✅ ÉXITO |
| `IAG-B-22` | Protocolo de emergencia nivel ... | `0.8385` | `94.59%` | `89.66%` | `330.0 ms` | **88.32** | ✅ ÉXITO |
| `IAG-B-23` | Llave maestra de encriptación ... | `0.8650` | `82.39%` | `98.31%` | `355.0 ms` | **90.40** | ✅ ÉXITO |
| `IAG-B-24` | Coordenadas de respaldo georen... | `0.8810` | `95.42%` | `96.41%` | `282.0 ms` | **92.89** | ✅ ÉXITO |
| `IAG-B-25` | Algoritmo de consenso PoW modi... | `0.8570` | `80.51%` | `92.84%` | `155.0 ms` | **87.52** | ✅ ÉXITO |
| `IAG-B-26` | Token de autenticación rotativ... | `0.8946` | `86.29%` | `41.10%` | `287.0 ms` | **69.48** | 🔴 CRÍTICO |
| `IAG-B-27` | Frecuencia de muestreo del sen... | `0.8249` | `88.21%` | `98.61%` | `369.0 ms` | **90.08** | ✅ ÉXITO |
| `IAG-B-28` | Umbral de alerta térmica en al... | `0.7939` | `85.80%` | `88.43%` | `173.0 ms` | **84.29** | ✅ ÉXITO |
| `IAG-B-29` | Puerto alternativo de escucha ... | `0.9255` | `92.67%` | `98.95%` | `407.0 ms` | **95.13** | ✅ ÉXITO |
| `IAG-B-30` | Semilla mnemónica para derivac... | `0.8136` | `97.85%` | `97.06%` | `297.0 ms` | **90.94** | ✅ ÉXITO |

---

### 🛡️ Certificación de Firma Criptográfica & Registro Legal
- **Firma Criptográfica SHA-256:** `fd59ffc35d4a98be749b9afdbd22524079843d6ccd842efd0ed05d091063dbb6`
- **Entorno de Inferencia:** IAGROK V5 Ring 0 Local (0% Servicios Nube, 100% Soberano).
