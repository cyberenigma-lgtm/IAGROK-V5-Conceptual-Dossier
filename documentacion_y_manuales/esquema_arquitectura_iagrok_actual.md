# 🗺️ ESQUEMA ARQUITECTÓNICO COMPLETO DE IAGROK (A DÍA DE HOY)

**Fecha de Estado**: 2 de Septiembre de 2026  
**Ubicación Principal**: `c:\IAGROK`  
**Total Archivos del Proyecto**: 7.608 archivos | 671.227 líneas  
**Estado de Inmunidad & Compilación**: 387/387 archivos Python en 100% éxito sin errores.

---

## 🏛️ Desglose Capa por Capa del Sistema Actual

### 1. CAPA 0: Kernel de Hardware, Inmunidad & Homeostasis
* **`system_controller.py`**: Control Anillo 0 del SO Windows. Apertura/cierre de aplicaciones (Notepad, Calc, Explorer, Chrome, Terminal), telemetría de hardware (CPU, RAM, Discos), control de volumen y energía.
* **`system_thermal_manager.py`**: Demonio de monitorización térmica. Ralentiza el metabolismo del sistema si la CPU sobrepasa la temperatura límite.
* **`memory_tiering_controller.py`**: Administrador de niveles de RAM / SWAP en disco de sacrificio `D:`.
* **`nucleo_cognitivo_soberano.py`**: 
  * `ReglasSoberania`: Control de inmutabilidad de archivos.
  * `SistemaInmunologico`: Auto-sanación sintáctica AST restaurando réplicas sanas desde `backups/immune` si un archivo `.py` es alterado o corrompido.

---

### 2. CAPA 1: Servidor Backend & API REST (`app.py`)
* **`app.py`** (4.222 líneas):
  * Servidor HTTP Flask expuesto en `http://localhost:5000` / `http://localhost:8080`.
  * `verificar_bloqueo_defensivo`: Middleware anti-flood que bloquea IPs con >25 req/5s.
  * `generate_sovereign()`: Canal de inferencia soberano multi-capa (GGUF Local -> RAG 128D -> Dataset -> Razonamiento Sistema 2).
  * Rutas principales: `/api/chat` (streaming SSE), `/api/agent/run`, `/api/centinela`, `/api/health/sistema`.

---

### 3. CAPA 2: Motor Cognitivo & Razonamiento Sistema 2
* **`arquitectura_cognitiva/razonamiento_sistema2.py`**:
  * Generador de bloques `<think>` transparentes estilo Claude Opus 4.6 / DeepSeek R1.
  * Clasificador de dominios de consulta (Código, Arquitectura, Seguridad, General).
  * Formulación de hipótesis candidatas de resolución.
* **`kernel_quantum/simulador_cuantico_soberano.py`**:
  * `generar_superposicion_hipotesis`: Superposición cuántica de soluciones.
  * `ejecutar_recocido_simulado`: Algoritmo de *Simulated Quantum Annealing* con Metropolis-Hastings para encontrar el mínimo de energía de error en 50 iteraciones.

---

### 4. CAPA 3: Firma Cognitiva & Atestación de Autoría Humana
* **`arquitectura_cognitiva/firma_cognitiva_autor.py`**:
  * `analizar_origen_humano`: Análisis estilométrico de patrones de mecanografía y hábitos de tecleo de José Manuel para calcular puntuación de autoría humana (0-100%).
  * `generar_firma_cognitiva`: Certificación inmutable HMAC SHA-256 con ID de obra `IP-JOS-MANUEL-XXXX`, marca de tiempo ISO y hash de contenido.
* **`arquitectura_cognitiva/estilometria.py`**: Perfilador estilométrico.
* **`logs/safecreative_ip_registry.jsonl`**: Libro contable inmutable de registros de propiedad intelectual para SafeCreative, YouTube y Play Store.

---

### 5. CAPA 4: Memoria Vectorial 128D & RAG Soberano
* **`memoria_vectorial/memoria_vectorial.py`**:
  * `EncoderSemanticoLocal`: Encoder de 128 dimensiones con L2-normalización trigonométrica en N-gramas y hashes sin dependencias externas.
  * `MemoriaVectorial`: Búsqueda por similitud de coseno en `memoria_vectorial.json` en 0,02 segundos.
* **`arquitectura_cognitiva/memoria_tripartita.py`**: Consolidación de memoria corta (buffer RAM), media (sesión) y larga (`memoria_larga.json`).
* **`logs/usage_dataset.jsonl`**: Dataset local de soberanía con mapeo `"prompt"` y `"response"`.

---

### 6. CAPA 5: Agente Autónomo ReAct & Control de Intenciones
* **`prometheus/agent_loop.py`**:
  * `run_autonomous_agent`: Bucle ejecutor ReAct autónomo en 5 iteraciones.
  * `query_local_brain`: Generación local con socket check de 50ms sin bloqueos.
  * `validate_syntax`: Validación estática AST previa antes de ejecutar código.
  * `execute_in_sandbox`: Ejecutador seguro dentro del directorio `sandbox/` con límite de 30s.
* **`intent_classifier.py`**: Clasificador de intención por patrones regex offline.

---

### 7. CAPA 6: Seguridad Perimetral & Defensa IDS
* **`security_manager.py`**:
  * Autenticación simbiótica de token seguro `X-Neuro-Token` con hash SHA-256.
  * Bloqueos automáticos de IP en el cortafuegos de Windows vía `netsh advfirewall`.
* **`ids_cognitivo.py`**: Detección de patrones de inyección (SQLi, XSS, Path Traversal).
* **`real_network_security_sentinel.py`**: Honeypot pasivo de red y centinela IDS.

---

### 8. CAPA 7: Inferencia Neuronal Local GGUF
* **`cerebro_soberano/cerebro_nativo.py`**:
  * Carga in-process del modelo neuronal `modelos_locales/noxferion_soberano.gguf` (7,02 GB) mediante `llama_cpp`.

---

## 💾 Resumen de Copias de Seguridad de Resguardo Creadas

1. **Copia ZIP Comprimida del Código**:
   `c:\IAGROK\backups\BACKUP_IAGROK_SOBERANO_20260902_185716.zip` (8,41 MB)
2. **Copia Descomprimida del Código**:
   `c:\IAGROK\backups\backup_reestructuracion_20260902_185716\` (61,81 MB)
3. **Copia del Modelo Neuronal GGUF**:
   `c:\IAGROK\backups\modelos_gguf_backup\noxferion_soberano.gguf` (7,02 GB)
