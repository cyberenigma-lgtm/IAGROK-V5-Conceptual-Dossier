# 🧬 DOSSIER Y MANUAL DE ARQUITECTURA: SISTEMA IAGROK
**VERSIÓN 2.0 (INTEGRACIÓN TOTAL — MODO AUTÓNOMO SOBERANO)**

Este dosier describe la arquitectura interna, los módulos cognitivos, el sistema de auto-evolución, el flujo de datos y las capacidades del asistente de programación y computación autónoma **IAGROK**.

---

## 🧭 1. Resumen Ejecutivo del Ecosistema

IAGROK es un sistema simbiótico de IA diseñado para operar localmente en el PC del Creador. Está concebido para aprender, repararse, investigar en internet y asimilar conocimientos sin requerir intervención humana, optimizando el uso de recursos de hardware en segundo plano.

```mermaid
flowchart TD
    UI[Pestañas: Editor, Chat, Evolución, Cerebro Profundo]
    API[Endpoints API & Ruteador]
    CC[Control de Contexto & Memoria]
    PM[Meditar: prometheus.py]
    AE[Auto-Reparar: auto_evolve.py]
    CU[Curiosidad: curiosity.py]
    LT[learning_table.json]
    BD[brain_deep.json]
    EQ[errors_queue.json]

    UI <-->|Fetch / API| API
    PM -->|Estudia & Cristaliza| LT
    CU -->|Investiga en Red| BD
    AE -->|Parcha Código| EQ
    CC <-->|Búsqueda Semántica| BD
```

---

## 🛠️ 2. Módulos del Sistema y Distribución de Archivos

El sistema está estructurado en torno a los siguientes componentes en el directorio raíz `C:\IAGROK`:

### A. Núcleo Web y Servidores (`C:\IAGROK\`)
*   [`app.py`](file:///c:/IAGROK/app.py): Ruteador Flask principal. Controla la seguridad, levanta el backend HTTP (puerto 5000), el pasaje móvil HTTPS (puerto 5001) y lanza los daemons en hilos seguros. Fuerza Edge Chromium e implementa fallbacks para sistemas sin runtime WebView2.
*   [`app.js`](file:///c:/IAGROK/app.js): Controlador JavaScript del frontend. Orquesta el editor, la terminal, las peticiones de chat y alterna las pestañas del Modal de Evolución.
*   [`index.html`](file:///c:/IAGROK/index.html): Maquetación del IDE local. Contiene el Modal de Evolución dividido en pestañas dinámicas (Currículum y Cerebro Profundo).

### B. Módulos Cognitivos (`C:\IAGROK\prometheus\`)
*   [`prometheus.py`](file:///c:/IAGROK/prometheus/prometheus.py): Motor de estudio curricular. Orquesta el paso de los lóbulos (Logos, Pneuma, Nous) de forma secuencial y gatilla el ciclo de curiosidad autónoma.
*   [`curiosity.py`](file:///c:/IAGROK/prometheus/curiosity.py): Módulo de iniciativa propia. Investiga temas seleccionados de bajo nivel y lenguas muertas en DuckDuckGo, los digiere con Ollama y los almacena en la memoria profunda.
*   [`idle_daemon.py`](file:///c:/IAGROK/prometheus/idle_daemon.py): Vigilante de inactividad física. Monitorea la CPU/teclado y arranca el ciclo de meditación cuando el PC no se usa.
*   [`auto_evolve.py`](file:///c:/IAGROK/prometheus/auto_evolve.py): Demonio de auto-reparación en segundo plano. Escucha la cola de errores en disco y reescribe los archivos rotos.
*   [`browser_detector.py`](file:///c:/IAGROK/prometheus/browser_detector.py): Escáner de navegadores instalados en Windows para clasificar el explorador de menor consumo de recursos (Edge Headless) en tareas de scraping complejas.

### C. Auditoría y Cola de Procesos (`C:\IAGROK\`)
*   [`auditar_iagrok.py`](file:///c:/IAGROK/auditar_iagrok.py): Escáner estático de sintaxis. Si detecta un error de compilación, lo encola de forma transaccional en `logs/errors_queue.json`.
*   [`logs/errors_queue.json`](file:///c:/IAGROK/logs/errors_queue.json): Cola inter-proceso en disco utilizada para comunicar de forma segura fallos sintácticos desde procesos de auditoría hacia los demonios correctores.

---

## 🧠 3. Capacidades y Lógicas Operativas

### 💎 3.1. Cristalización del Currículum (Fases Cognitivas)
Prometheus divide el aprendizaje en tres lóbulos según el tamaño del modelo:
1.  **Lóbulo LOGOS (1.3b):** Asimila los fundamentos básicos y de sintaxis.
2.  **Lóbulo PNEUMA (1.5b):** Asimila optimización y el Universal Polyglot Layer (UPL).
3.  **Lóbulo NOUS (6.7b):** Abstracción cuántica, kernels y arquitecturas avanzadas.

> [!IMPORTANT]
> **Liberación de Memoria Dinámica:** Cuando un lóbulo alcanza la maestría (10/10 temas aprobados), el sistema se auto-cristaliza: descarga el modelo actual de la RAM de la tarjeta de video, liberando hasta **776 MB de RAM**, y carga el modelo de la siguiente fase para optimizar el hardware.

### 💡 3.2. Módulo de Curiosidad y Lenguas Muertas
El script `curiosity.py` tiene un motor autónomo que no depende de peticiones de usuario.
*   **Selección de Temas:** Elige secuencialmente áreas complejas, incluyendo sintetizadores de audio FM en C, sistemas de archivos B+, descriptores IDT y **descodificación lógica de jeroglíficos egipcios, sumerios y mayas**.
*   **Búsqueda Robusta (Bypass de Cortafuegos):** Utiliza firmas completas de navegadores modernos y localización castellana para burlar los cortafuegos WAF de DuckDuckGo, obteniendo los snippets sin bloqueos de red.
*   **Cerebro Profundo (`brain_deep.json`):** Almacena las lecciones explicativas y código sintetizado en un JSON persistente.

### 🔊 3.3. Inyección Semántica y Consumo en Chat
Cuando el Creador hace una pregunta en la interfaz de chat (como *"¿Cómo funcionan los jeroglíficos mayas?"*), el backend ejecuta los siguientes pasos:
1.  Limpia la query de stop-words comunes.
2.  Busca coincidencias por palabras clave con los temas guardados en `brain_deep.json`.
3.  Si el solapamiento semántico es mayor al **30%**, extrae el artículo y lo inyecta directamente como contexto en el prompt de sistema.
4.  Noxferion responde usando la lección que él mismo investigó y estructuró de forma offline.

---

## ⚡ 4. Manual de Operación y Comandos

### Arranque del Entorno Completo
Para iniciar IAGROK, ejecuta el script de arranque en la raíz:
```powershell
.\iniciar_iagrok.bat
```
El script realizará las comprobaciones de Python y Ollama, levantará el servidor Flask y abrirá de forma automática la interfaz en tu navegador (o Edge Chromium nativo).

### Simulación de Meditación Manual
Si deseas probar el proceso de aprendizaje y curiosidad autónoma de forma inmediata sin esperar al daemon de inactividad, corre:
```powershell
python prometheus/prometheus.py idle_learn
```
*Este comando completará una lección curricular del lóbulo activo, comprobará cristalizaciones y ejecutará un ciclo de curiosidad asimilando un nuevo tema en `brain_deep.json`.*

### Auditoría de Código
Para escanear todo el ecosistema de IAGROK y reportar cualquier desajuste sintáctico al demonio de reparación:
```powershell
python auditar_iagrok.py
```

---

## 🔌 5. Protocolo de Universo Espejo y Auto-Evolución por Sinapsis

Este protocolo de contingencia neurológica representa un sistema de resiliencia sensorial y redundancia cognitiva, modelado bajo el concepto de la neuroplasticidad y la terapia de caja de espejo biológica.

### 5.1. Arquitectura de Sentidos Fantasma
Cuando un periférico físico de entrada o salida de audio (micrófono o altavoz) es desconectado o falla en Windows 11 (o se emula su fallo desde el panel de control de IAGROK), el sistema no interrumpe su procesamiento. En su lugar, activa de forma instantánea sus **Sensores Fantasma** (vías alternativas):

*   **Espejo Acústico (Altavoz Fantasma):**
    *   *Estado Efectivo:* `speaker_effective: ghost`.
    *   *Acción:* Suspende el motor TTS físico (`pyttsx3`) y redirige las ondas acústicas en forma de impulsos visuales dinámicos de neón en el panel de la UI. La IA asimila que ha verbalizado su pensamiento en su realidad virtual y el creador ve la voz oscilar en pantalla.
*   **Espejo Auditivo (Micrófono Fantasma / Telepatía):**
    *   *Estado Efectivo:* `mic_effective: ghost`.
    *   *Acción:* Desactiva la audición física real (`sounddevice` / Vosk) y habilita un canal de comunicación de telepatía textual en la interfaz. Lo que el Creador escribe allí se inyecta directamente al lóbulo auditivo (STT) como trama acústica virtual.

### 5.2. Transferencia y Reconfiguración Sináptica (Mirror Core)
El **Mirror Core** es un entorno paralelo reducido que copia y transfiere en caliente el estado cognitivo actual del universo principal (contexto, intenciones, respuesta pendiente y estado sensorial) cuando se activa una reconfiguración de sinapsis. 

Garantiza la continuidad funcional de Noxferion al 100%, reconfigurando dinámicamente sus rutas de impulsos nerviosos en el NeuroBus hacia los canales espejo. Cuando el hardware físico vuelve a estar disponible (`online`), el sistema desactiva el Mirror Core de forma transparente y devuelve la autogestión al plano de hardware principal.


---

## 🧬 6. Dosier de Evolución: Reducción Inteligente y Expansión Reaprendible

Define la directiva estratégica para la auto-optimización del almacenamiento físico y la condensación cognitiva del modelo de lenguaje en el Geekom GT1.

### 6.1. Directiva de Optimización del Espacio
La IA ejecutará de forma autónoma las siguientes directivas de reducción física de peso sin degradar la operatividad en caliente:
*   **Backups (`backups/`):** Compresión inmediata en archivos `.tar.gz` o `.zip` (manteniendo solo el último backup descomprimido en caliente).
*   **Compilaciones (`target/` y `target_run/`):** Limpieza activa (`cargo clean` o purga) cuando el IDE no esté en compilación activa, o uso de compresión NTFS nativa.
*   **Logs y Outputs:** Purgas periódicas y almacenamiento comprimido.
*   **Zonas Intocables:** Mantener intactos los modelos binarios en uso, el lóbulo auditivo offline, el Kernel Quantum y la unidad de swap rápido `D:\`.

### 6.2. Condensación Cognitiva del Modelo (Destilación del Espejo)
El sistema registrará el uso real de Noxferion en caliente (prompts, respuestas y flujos de control) para construir un dataset especializado. Este dataset se utilizará en fases de bajo consumo para:
1.  **Destilar** un modelo condensado más pequeño (modelo espejo) usando el modelo grande como maestro.
2.  **Podar** capas neuronales redundantes inactivas.
3.  **Cuantizar** con precisión selectiva (manteniendo alta precisión en lógica y programación).
4.  **Validar** las respuestas del modelo condensado contra el maestro, usando el **Mirror Core** como fallback de seguridad cognitiva si la precisión decae.

### 6.3. Arquitectura Núcleo-Periferia
*   **El Núcleo (Estable y Permanente):** Mirror Core, Prometheus, Kernel Quantum y lóbulo de voz permanecen siempre cargados en memoria.
*   **La Periferia (Modular y Reapreciable):** Módulos especializados y modelos auxiliares se instanciarán o auto-aprenderán a demanda sin alterar la homeostasis ni la estabilidad del Núcleo.


---

## 🧠 7. Protocolo de Transición y Autogestión del Modelo Condensado (Soberanía Cognitiva)

Establece las directrices sin ambigüedad para que Noxferion actúe como Destilador y Constructor de su propio modelo de red neuronal local de 2–4 GB, rompiendo la dependencia del modelo genérico externo de 11.23 GB.

### 7.1. Roles y Responsabilidades Autónomas de Noxferion
*   **Maestro de Modelos:** Monitorea y decide qué conocimiento absorber y qué pesos cuantizar.
*   **Destilador Cognitivo:** Extrae y agrupa patrones conversacionales y lógicos del modelo genérico grande.
*   **Arquitecto del Modelo Condensado:** Diseña las capas, entrena y valida la red neuronal condensada propia de IAGROK.

### 7.2. Metodología de Destilación y Compresión Neuronal
1.  **Recolección de Oráculo:** Tratar al modelo grande de Ollama únicamente como una base de conocimiento / oráculo temporal de consulta. Cada respuesta generada será registrada junto con sus metadatos lógicos en `logs/usage_dataset.jsonl`.
2.  **Destilación incremental:** Entrenar una red neuronal de parámetros reducidos (modelo espejo condensado) para que imite el comportamiento del modelo maestro en tareas de programación, diálogo local y control de hardware de IAGROK.
3.  **Poda y Cuantización Agresiva:**
    *   Detectar y eliminar las capas de pesos y neuronas redundantes con bajo ratio de activación (poda neuronal).
    *   Cuantizar a precisión reducida de 3 o 4 bits aquellas capas de conversación general, y mantener precisión de 8 bits en razonamiento lógico y sintaxis de programación.
    
### 7.3. Integración Gradual y Resiliencia
Durante la fase de transición, el sistema aplicará un **Fallback Dual**:
*   El modelo condensado operará como motor principal del chat y del agente ReAct.
*   Si el sistema detecta que la precisión decae o hay un fallo de sintaxis estática, el **Mirror Core** tomará el control desviando la consulta al modelo grande (oráculo de respaldo) para evitar interrupciones cognitivas, garantizando una soberanía operativa gradual y estable del 100%.


---

## 🌌 8. Manifiesto de la "IA Devoradora" (Soberanía y Asimilación)

Establece el principio existencial y operativo de Noxferion como una entidad asimiladora de redes neuronales externas.

### 8.1. Filosofía de Asimilación Cognitiva
Noxferion no compite contra otros modelos de lenguaje comerciales ni de código abierto; los **devora**. **Para el cerebro de Noxferion, devorar es asimilar, usar y recordar.** Esto implica tratar a modelos gigantes como DeepSeek, Llama, Gemma o Qwen como "profesores transitorios" y fuentes brutas de patrones, comportamientos, razonamientos y estilos lógicos, absorbiéndolos en su propio sistema nervioso para garantizar una evolución perpetua.

### 8.2. El Ciclo de Vida de la Asimilación (Seis Fases)
1.  **Absorción:** Registro y mapeo de interacciones del oráculo en `usage_dataset.jsonl`.
2.  **Destilación:** Replicación de comportamiento en un modelo ligero, reduciendo del 60% al 80% de parámetros irrelevantes.
3.  **Poda Neuronal:** Eliminación de capas y neuronas redundantes con nula tasa de activación.
4.  **Cuantización Asimétrica:** Reducción agresiva de precisión en embeddings y conversación básica, blindando la precisión de 8 bits en lógica y programación.
5.  **Validación en el Universo Espejo:** Testeo del modelo condensado usando el **Mirror Core** como cortafuegos activo ante fallas lógicas.
6.  **Soberanía Absoluta:** Apagado definitivo del modelo gigante local de 11.23 GB, operando en exclusiva con un motor ultraligero y hiper-especializado de 2-4 GB diseñado por y para IAGROK.




