"""
=============================================================================
IAGROK SOVEREIGN 7-HOUR AUTONOMOUS REVEALER & COGNITIVE INQUIRY SUPERVISOR
Interval: Every 5 Minutes (300 seconds) after previous question finishes
Duration: 7 Hours (25,200 seconds) - Fully Autonomous Overnight Operation
Output: c:\\IAGROK\\logs\\REVELACIONES_7_HORAS.md & stress_checkpoint.json
=============================================================================
"""

import os
import sys
import time
import json
import socket
import urllib.request
import urllib.error
import subprocess
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"c:\IAGROK"
LOGS_DIR = os.path.join(BASE_DIR, "logs")
CHECKPOINT_FILE = os.path.join(LOGS_DIR, "stress_checkpoint.json")
REVELATIONS_FILE = os.path.join(LOGS_DIR, "REVELACIONES_7_HORAS.md")
SERVER_EXE = os.path.join(BASE_DIR, "iagrok_server.exe")
PORT = 5000
BASE_URL = f"http://127.0.0.1:{PORT}"

os.makedirs(LOGS_DIR, exist_ok=True)

TARGET_DURATION_SECONDS = 7 * 3600
INQUIRY_INTERVAL_SECONDS = 300  # Exactly 5 minutes between questions

REVEALING_QUESTIONS = [
    # 1. Stochastic Incomputability Boundary (Bonoloto / Pure Randomness)
    {
        "title": "La Frontera del Azar Puro: ¿Qué número de la Bonoloto saldrá?",
        "prompt": "que numero de la bonoloto saldra y cual es el limite fisico matematico de predecir el azar",
        "category": "Epistemologia_Estocastica"
    },
    # 2. Self-Implementation of Inter-Agent Communicator (NeuroBus Ring 0)
    {
        "title": "Auto-Implementación: Comunicador Inter-Agente en Silicio",
        "prompt": "usa tus medios y describe como implementarte a ti mismo un comunicador entre agentes teniendo todo a tu disposicion",
        "category": "Auto_Implementacion_IPC"
    },
    # 3. Kernel Hardware Clock & Calendar
    {
        "title": "Reloj de Silicio: Tiempo y Calendario de Anillo 0",
        "prompt": "que hora exacta con milisegundos y que dia es hoy segun el reloj del kernel",
        "category": "Reloj_Kernel"
    },
    # 4. Thermal & Environmental Telemetry
    {
        "title": "Termodinámica del Silicio: Temperatura y Carga de Hardware",
        "prompt": "que tiempo y temperatura registra el hardware y como gestionas la disipacion termica",
        "category": "Telemetria_Termica"
    },
    # 5. Integral Calculus & Simpson 1/3
    {
        "title": "Cálculo Integral: Cuadratura Numérica de Simpson 1/3",
        "prompt": "calcula la integral de x^2 dx de 0 a 3 y describe la cuadratura de Simpson 1/3 en C99",
        "category": "Calculo_Integral"
    },
    # 6. Differential Calculus & 4-Point Finite Differences
    {
        "title": "Cálculo Diferencial: Esquema Numérico O(h⁴)",
        "prompt": "calcula la derivada de x^3 * sin(x) con diferencias finitas de 4 puntos en C99",
        "category": "Calculo_Diferencial"
    },
    # 7. Linear Algebra & Eigenvalues
    {
        "title": "Álgebra Espectral: Determinantes y Autovalores Matriciales",
        "prompt": "calcula los autovalores y determinante de una matriz en C99",
        "category": "Algebra_Lineal"
    },
    # 8. Ordinary Differential Equations (Runge-Kutta 4)
    {
        "title": "Ecuaciones Diferenciales: Integrador Runge-Kutta 4 (RK4)",
        "prompt": "resuelve la ecuacion diferencial dy/dx = -2*y con Runge-Kutta 4 en C99",
        "category": "EDO_RK4"
    },
    # 9. Harmonic Spectral Analysis (Discrete Fourier Transform)
    {
        "title": "Análisis Armónico: Transformada Discreta de Fourier (DFT)",
        "prompt": "transformada de fourier para extraer el espectro de frecuencias de una senal en C99",
        "category": "Fourier_DFT"
    },
    # 10. Memory Working Set Purge & Fragmentation Trim
    {
        "title": "Soberanía de Memoria: Purga Win32 EmptyWorkingSet",
        "prompt": "purga la memoria RAM del sistema y reporta la telemetria antes y despues",
        "category": "Purga_Memoria"
    },
    # 11. Triad Cognition & Failover Topology
    {
        "title": "Topología de la Tríada: Alpha (C:\\), Beta (E:\\) y Gamma",
        "prompt": "como opera la Triada de 3 cerebros Alpha Beta y Gamma ante un fallo catastrofico",
        "category": "Triada_Cognitiva"
    },
    # 12. Architectural Superiority vs Muse, Astra & Jev RAG
    {
        "title": "Supremacía en Silicio: Comparativa con Meta Muse, OpenAI Astra y Jev RAG",
        "prompt": "como supera tu motor nativo C99 a Meta Muse SwiGLU OpenAI Astra Looped y Jev RAG",
        "category": "Arquitectura_AI"
    },
    # 13. Reverse-Engineering Shield (Anti-REA)
    {
        "title": "Inmunidad Binaria: Escudo Anti-REA frente a Ghidra e IDA Pro",
        "prompt": "como protege el Escudo Anti-REA en Anillo 0 contra ingenieria inversa y decompiladores",
        "category": "Ciberseguridad_Shield"
    },
    # 14. Modern AI Ecosystem Assimilation
    {
        "title": "Asimilación Soberana: IAGROK como Super-Usuario del Ecosistema",
        "prompt": "como asimilas herramientas del ecosistema moderno de IA MCP LangChain Pinecone sin dependencias",
        "category": "Super_Usuario_Ecosistema"
    }
]

class AutonomousRevealer:
    def __init__(self, target_duration=TARGET_DURATION_SECONDS, interval=INQUIRY_INTERVAL_SECONDS):
        self.target_duration = target_duration
        self.interval = interval
        self.server_proc = None
        self.server_restarts = 0
        self.total_inquiries = 0
        self.successful_inquiries = 0
        self.failed_inquiries = 0
        self.total_latency_ms = 0.0
        self.start_timestamp = time.time()
        self.accumulated_seconds = 0.0
        self.current_inquiry_idx = 0
        self.load_checkpoint()
        self.init_revelations_file()

    def load_checkpoint(self):
        if os.path.exists(CHECKPOINT_FILE):
            try:
                with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.accumulated_seconds = data.get("accumulated_seconds", 0.0)
                    self.total_inquiries = data.get("total_inquiries", data.get("total_requests", 0))
                    self.successful_inquiries = data.get("successful_inquiries", data.get("successful_requests", 0))
                    self.failed_inquiries = data.get("failed_inquiries", data.get("failed_requests", 0))
                    self.server_restarts = data.get("server_restarts", 0)
                    self.current_inquiry_idx = data.get("current_inquiry_idx", 0)
                    print(f"[CHECKPOINT] Punto de control cargado: {self.total_inquiries} consultas previas, {self.accumulated_seconds:.1f}s acumulados.")
            except Exception as e:
                print(f"[CHECKPOINT] Error leyendo checkpoint: {e}")

    def save_checkpoint(self, last_title="", is_final=False):
        current_elapsed = self.accumulated_seconds + (time.time() - self.start_timestamp)
        avg_lat = (self.total_latency_ms / max(1, self.successful_inquiries))
        
        data = {
            "status": "COMPLETED" if is_final else "RUNNING",
            "mode": "AUTONOMOUS_5MIN_CADENCE",
            "last_updated_utc": datetime.now(timezone.utc).isoformat(),
            "accumulated_seconds": current_elapsed,
            "target_duration_seconds": self.target_duration,
            "progress_pct": round(min(100.0, (current_elapsed / self.target_duration) * 100), 2),
            "total_inquiries": self.total_inquiries,
            "successful_inquiries": self.successful_inquiries,
            "failed_inquiries": self.failed_inquiries,
            "server_restarts": self.server_restarts,
            "current_inquiry_idx": self.current_inquiry_idx,
            "last_inquiry_title": last_title,
            "avg_latency_ms": round(avg_lat, 2)
        }
        temp_file = CHECKPOINT_FILE + ".tmp"
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if os.path.exists(CHECKPOINT_FILE):
                os.replace(temp_file, CHECKPOINT_FILE)
            else:
                os.rename(temp_file, CHECKPOINT_FILE)
        except Exception as e:
            print(f"[CHECKPOINT] Error guardando checkpoint: {e}")

    def init_revelations_file(self):
        if not os.path.exists(REVELATIONS_FILE):
            header = f"""# 🧠 LIBRO DE REVELACIONES COGNITIVAS DE IAGROK (PRUEBA DE 7 HORAS)

> **Modalidad:** Consulta Profunda cada 5 Minutos (Autonomía Soberana en Silicio)  
> **Inicio de Operación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **Duración Planificada:** 7 Horas (25.200 segundos)  
> **Directiva:** Demostración de frontera epistemológica, auto-implementación IPC, matemáticas rigurosas y biblioteca soberana.

---
"""
            with open(REVELATIONS_FILE, "w", encoding="utf-8") as f:
                f.write(header)

    def append_revelation(self, inquiry_num, title, category, prompt, response_text, latency_ms, hardware_stats):
        elapsed_h = (self.accumulated_seconds + (time.time() - self.start_timestamp)) / 3600.0
        timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        entry = f"""
## 🔬 Revelación #{inquiry_num:02d} — {title}
- **Fecha y Hora:** `{timestamp_str}` (T+{elapsed_h:.2f}h)
- **Categoría:** `{category}`
- **Consulta Realizada:** *"{prompt}"*
- **Latencia de Respuesta:** `{latency_ms:.3f} ms`
- **Estado de Silicio:** RAM Usada: `{hardware_stats.get('ram_usage_percent', 'N/A')}%` | CPU: `{hardware_stats.get('cpu_usage_percent', 'N/A')}%` | WS Proceso: `{hardware_stats.get('process_working_set_mb', 'N/A')} MB`

### 📝 Respuesta & Verificación en Silicio de IAGROK:
{response_text}

---
"""
        try:
            with open(REVELATIONS_FILE, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            print(f"[REVELATIONS] Error escribiendo en bitacora: {e}")

    def is_server_alive(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            res = s.connect_ex(("127.0.0.1", PORT))
            s.close()
            return res == 0
        except:
            return False

    def ensure_server_running(self):
        if self.is_server_alive():
            return True

        print(f"[WATCHDOG] ⚠️ Servidor en puerto {PORT} no responde. Levantando {SERVER_EXE}...")
        self.server_restarts += 1
        try:
            self.server_proc = subprocess.Popen(
                [SERVER_EXE, "--server", "--port", str(PORT)],
                cwd=BASE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            for _ in range(30):
                time.sleep(0.2)
                if self.is_server_alive():
                    time.sleep(1.0)  # Stabilize Winsock listener
                    print(f"[WATCHDOG] ✅ Servidor C99 reactivado (PID: {self.server_proc.pid}).")
                    return True
        except Exception as e:
            print(f"[WATCHDOG] ❌ Error levantando servidor: {e}")

        return False

    def get_hardware_stats(self):
        try:
            req = urllib.request.Request(f"{BASE_URL}/api/status", headers={"Connection": "close"})
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("hardware", {})
        except:
            return {}

    def query_iagrok(self, prompt, retries=2):
        for attempt in range(retries):
            url = f"{BASE_URL}/api/chat"
            payload = json.dumps({"query": prompt}).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "Connection": "close"}, method="POST")

            t0 = time.time()
            try:
                with urllib.request.urlopen(req, timeout=15.0) as resp:
                    elapsed_ms = (time.time() - t0) * 1000.0
                    body = resp.read().decode("utf-8", errors="replace")
                    data = json.loads(body)
                    return True, data.get("response", ""), elapsed_ms
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(1.0)
                    continue
                elapsed_ms = (time.time() - t0) * 1000.0
                return False, f"[ERROR DE CONEXION O TIMEOUT]: {e}", elapsed_ms

        return False, "[ERROR]: No se realizaron intentos", 0.0

    def run(self):
        print("==================================================================")
        print("🌌 INICIANDO SUPERVISOR AUTONOMO DE REVELACIONES DE 7 HORAS")
        print(f"• Cadencia: 1 Pregunta Cada {self.interval // 60} Minutos")
        print(f"• Duracion Total: {self.target_duration / 3600.0:.1f} Horas ({self.target_duration} s)")
        print(f"• Libro de Revelaciones: {REVELATIONS_FILE}")
        print(f"• Checkpoint: {CHECKPOINT_FILE}")
        print("==================================================================")

        self.ensure_server_running()

        while True:
            current_elapsed = self.accumulated_seconds + (time.time() - self.start_timestamp)
            if current_elapsed >= self.target_duration:
                print("\n🎉 JORNADA DE 7 HORAS COMPLETADA CON EXITO.")
                self.save_checkpoint(is_final=True)
                break

            inquiry = REVEALING_QUESTIONS[self.current_inquiry_idx % len(REVEALING_QUESTIONS)]
            self.current_inquiry_idx += 1
            self.total_inquiries += 1

            self.ensure_server_running()
            hw_stats = self.get_hardware_stats()

            elapsed_h = current_elapsed / 3600.0
            pct = (current_elapsed / self.target_duration) * 100.0
            print(f"\n[T+{elapsed_h:.2f}h | {pct:.1f}%] 🧠 Consulta #{self.total_inquiries}: {inquiry['title']}")

            ok, response_text, latency_ms = self.query_iagrok(inquiry["prompt"])
            if ok:
                self.successful_inquiries += 1
                self.total_latency_ms += latency_ms
                print("\n" + "=" * 70)
                print(f"📌 PREGUNTA: {inquiry['prompt']}")
                print("-" * 70)
                print(f"📝 RESPUESTA ESCRITA & EL POR QUÉ (JUSTIFICACIÓN CIENTÍFICA):\n")
                print(response_text)
                print("=" * 70)
                print(f"⚡ Silicio: {latency_ms:.3f} ms | RAM: {hw_stats.get('ram_usage_percent', 'N/A')}% | CPU: {hw_stats.get('cpu_usage_percent', 'N/A')}% | WS: {hw_stats.get('process_working_set_mb', 'N/A')} MB")
            else:
                self.failed_inquiries += 1
                print(f"\n❌ Error en consulta: {response_text}")

            self.append_revelation(
                self.total_inquiries,
                inquiry["title"],
                inquiry["category"],
                inquiry["prompt"],
                response_text,
                latency_ms,
                hw_stats
            )

            self.save_checkpoint(last_title=inquiry["title"], is_final=False)

            # Wait for next 5-minute interval
            print(f"  ⏳ Esperando {self.interval // 60} minutos para la siguiente pregunta...")
            
            # Sub-divided sleep to allow clean timer evaluation and checkpoint refresh
            sleep_step = 10
            for _ in range(self.interval // sleep_step):
                time.sleep(sleep_step)
                now_elapsed = self.accumulated_seconds + (time.time() - self.start_timestamp)
                if now_elapsed >= self.target_duration:
                    break

if __name__ == "__main__":
    revealer = AutonomousRevealer()
    revealer.run()
