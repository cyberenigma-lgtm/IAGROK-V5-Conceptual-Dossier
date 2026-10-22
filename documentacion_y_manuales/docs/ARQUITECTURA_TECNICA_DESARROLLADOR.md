# ⚙️ ARQUITECTURA TÉCNICA Y ESPECIFICACIÓN DE INGENIERÍA — IAGROK / NOXFERION 👑🛡️

Documentación técnica de bajo nivel para desarrolladores, arquitectura de módulos, algoritmos de procesamiento de señal (DSP), modelos neuronales y endpoints de la API.

---

## 🏛️ 1. Estructura de Directorios del Ecosistema

```text
C:\IAGROK\
├── cerebro_soberano\          # Inferencia LLM in-process nativa (llama_cpp / GGUF)
│   └── cerebro_nativo.py      # Gestor de memoria RAM y streaming soberano
├── memoria_vectorial\         # Base de datos semántica de 128 dimensiones
│   └── memoria_vectorial_rag.py
├── modelos_locales\           # Checkpoints y pesos neuronales descargados
├── noxferion_audio_engine\    # Suite completa de producción acústica y DSP
│   ├── music_synth_core.py    # Generador instrumental Meta MusicGen
│   ├── suno_bark_vocal_engine.py # Motor vocal y canto neuronal Suno Bark
│   ├── separador_stems_soberano.py # Separador 4-stems HPSS offline
│   ├── dynamic_song_arranger.py # Compositor multi-sección (Intro->Verso->Estribillo)
│   ├── convolutive_reverb_dsp.py # Reverb cálida Schroeder-Moorer & EQ analógico
│   └── mix_dsp_engine.py      # Masterizador a -14 LUFS con limitador soft-knee
├── noxferion_video_engine\    # Suite de vídeo cinemático 3D y renderizado
│   ├── optical_flow_interpolator.py # Interpolación de movimiento a 60 FPS
│   └── pipeline_video_maestro.py # Shaders GLSL, cámara 3D y timeline
├── neuroshield_soberano\      # Guardián de recursos y autorreparación
│   └── neuroshield_autoheal.py
├── noxferion_web_studio\      # Servidor web independiente y UI (Port 8080)
│   ├── server.py              # Backend Flask asíncrono
│   └── index.html             # Frontend moderno con diseño de cristal oscuro
├── pipeline\                  # Orquestador maestro de punta a punta
│   └── pipeline_maestro_total.py
├── outputs\                   # Directorio de renderizados maestros (MP3, MP4, PNG)
└── app.py                     # Servidor central y controlador PyWebView IDE
```

---

## 🔬 2. Especificación Matemática y Algoritmos DSP

### 🎛️ A. Separación de Stems Soberana (HPSS + Spatial Masking):
Dado un espectrograma complejo $X(t, f) = \text{STFT}(x)$, la separación armónica-percusiva se calcula mediante filtros de mediana bidireccionales:
$$H(t, f) = \text{Mediana}_t(|X(t, f)|, L_{\text{arm}})$$
$$P(t, f) = \text{Mediana}_f(|X(t, f)|, L_{\text{perc}})$$
- **Vocales y Melodía:** Filtro pasabanda $250\text{ Hz} \le f \le 4500\text{ Hz}$ sobre la componente armónica con máscara espectral suave.
- **Bajo:** Filtro pasabajos $f \le 220\text{ Hz}$ sobre la componente armónica.
- **Batería:** Componente percusiva $P(t, f)$ con reconstrucción por $\text{ISTFT}$.

### 🎚️ B. Reverberación Cálida Analógica (Schroeder-Moorer):
Elimina las resonancias metálicas mediante 4 líneas de retardo desacopladas con absorción pasabajos de Butterworth a $3.2\text{ kHz}$:
$$y[n] = x[n] + \sum_{k=1}^{4} g_k \cdot \text{LPF}(x[n - d_k])$$
Donde $d_k \in \{29, 47, 68, 93\}\text{ ms}$ y $g_k \in [0.10, 0.42]$.

### 🧬 C. Memoria Vectorial RAG Densa (128 Dimensiones):
Los conceptos textuales se proyectan a un espacio euclidiano continuo mediante hashing ortogonal con dispersión de caracteres:
$$\vec{v}_i = \frac{1}{\sqrt{D}} \sum_{c \in \text{tokens}} \sin\left(\frac{2\pi \cdot \text{hash}(c) \cdot i}{D}\right)$$
La similitud semántica se calcula mediante producto escalar coseno:
$$\text{Sim}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}$$

---

## 🌐 3. Referencia de Endpoints de la API Central

| Método | Endpoint | Parámetros Principales | Respuesta |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/prometheus/query` | `query`, `model`, `system_prompt` | `{"ok": true, "result": {"answer": str, "source": str}}` |
| `POST` | `/api/web/search` | `query` | `{"ok": true, "results": str}` |
| `POST` | `/api/master/pipeline` | `idea`, `titulo`, `estilo_musica`, `voz`, `duracion` | Objeto completo de canción, vídeo y miniatura |
| `POST` | `/api/audio/stems` | `audio_path` | `{"vocals": path, "drums": path, "bass": path, "other": path}` |
| `GET` | `/api/system/telemetry` | — | CPU, RAM, temperatura y estado de NeuroShield |
