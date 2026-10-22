# 🚩 HOJA DE RUTA SOBERANA: SUSTITUCIÓN Y REEMPLAZO DE SOFTWARE DE TERCEROS

**Objetivo**: Identificar todos los programas comerciales de terceros presentes en el sistema, diseñar sus sustitutos nativos dentro del ecosistema **IAGROK / Neuro-OS** y eliminarlos progresivamente para lograr **autonomía tecnológica total**.

---

## 📊 TABLA DE REEMPLAZO Y PLAN DE ACCIÓN

| # | Programa Comercial de Terceros | Función Comercial | Módulo Nativo IAGROK / Neuro-OS a Crear | Estado del Sustituto Nativo | Acción y Prioridad |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **7-Zip / WinRAR** | Compresión `.zip`, `.7z`, `.tar.gz` | `modulos/compresor_soberano.py` *(std `zipfile`, `tarfile`, `lzma`)* | 🟢 **100% Nativo Listo** | **Borrar 7-Zip** *(Usar script nativo)* |
| **2** | **VLC / Reproductor Multimedia** | Reproducción de audio y vídeo | `motores_y_estudios/noxferion_multimedia_engine.py` | 🟢 **Integrado en Noxferion DSP** | **Borrar reproductores externos** |
| **3** | **Postman / Insomnia / HTTP Clients** | Pruebas de APIs REST, JSON y WebSockets | `modulos/tester_api_soberano.py` *(Client HTTP/WS)* | 🟡 **Fase de Integración** | **Reemplazar por Web UI Studio** |
| **4** | **FileZilla / Clientes FTP/SFTP** | Transferencia remota de archivos | `arquitectura_cognitiva/cluster_distribuido.py` | 🟢 **Integrado en Red Malla P2P** | **Reemplazar por Red Malla P2P** |
| **5** | **Gitea (Servidor Git Self-Hosted)** | Servidor de repositorios Git, PRs e incidencias | Integrado como Servidor de Versiones en IAGROK | 🟢 **CONSERVADO 🛡️** | **CONSERVAR (Evita rehacer un servidor Git completo)** |
| **6** | **Notepad++ / VSCode** | Edición de texto y desarrollo | Web Studio IDE + Editor Nativo Python | 🟢 **Activo en Web Studio UI** | **Desplazar editores externos** |
| **7** | **Docker / Emuladores Pesados** | Aislamiento y ejecución en sandbox | `kernels/neuro_sandbox.c` + Python Micro-VM | 🟡 **Fase 2 (Kernel)** | **Sustituir contenedores Docker** |

---

## 🛠️ INSTRUCCIONES DE DESARROLLO PARA LOS SUSTITUTOS NATIVOS

### 1. Sustituto de Compresores (`modulos/compresor_soberano.py`)
IAGROK no requiere instaladores de 7-Zip o WinRAR. La biblioteca estándar de Python permite comprimir, descomprimir e inspeccionar archivos ZIP, TAR, GZ y BZ2 con cifrado nativo sin dependencias de terceros.

### 2. Sustituto de Reproductores (`noxferion_multimedia_engine.py`)
El motor Noxferion procesa audio digital en streaming, renderiza espectrogramas FFT en tiempo real y ejecuta vídeo directamente desde memoria o disco con soporte GPU/OpenCV.

### 3. Sustituto de Clientes API (Web Studio UI)
La interfaz web soberana de IAGROK (`motores_y_estudios/web_studio/`) incluye cliente WebSocket e inspector de endpoints REST de alta velocidad sin sobrecarga de memoria de Node/Electron.

---

## 📌 CRITERIO PERMANENTE DE CONSERVACIÓN vs ELIMINACIÓN
* **SE CONSERVA 🛡️**: Únicamente controladores físicos de hardware (Intel, Realtek, Nvidia), cliente de juegos Steam, binario nativo de Git y el servidor self-hosted **Gitea** *(para evitar rehacer un servidor Git completo desde cero)*.
* **SE ELIMINA Y REEMPLAZA ⚡**: Cualquier utilidad de software comercial (compresores, reproductores, DBs secundarias, proxies) que pueda ser escrita y controlada al 100% dentro del código fuente de **IAGROK**.

