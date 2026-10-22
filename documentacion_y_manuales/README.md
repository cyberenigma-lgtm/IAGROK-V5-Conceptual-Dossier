# 🧠 NeuroOS 1.1.0-DEF — AI-Native Sovereign Operating System

> **El primer Sistema Operativo Soberano con Inteligencia Artificial Nativa como Kernel Controller (IAGROK).**

---

## 🌟 Visión General

**NeuroOS 1.1.0-DEF** redefinió la arquitectura de los sistemas operativos al integrar **IAGROK** no como una extensión de chat externa, sino como el **Intelligence Kernel Controller** residente en el núcleo (`c:\IAGROK`). 

NeuroOS proporciona autocuración en tiempo real (Zero-Crash), seguridad 360° perimetral, gobernanza inteligente de recursos, arquitectura redundante Dual-Bank A/B con pruebas de paridad de memoria, permisos granulares por aplicación (`app.json`), comunicación inter-proceso por bus de eventos (Neuro-IPC) y un gestor de ventanas nativo ES6 (`NeuroWindowManager`).

---

## 🏛️ Las 7 Garantías Estructurales del Kernel Soberano

```
 +-------------------------------------------------------------------------+
 |                      NEURO-OS 1.1.0-DEF ARCHITECTURE                    |
 +-------------------------------------------------------------------------+
 |  [1. Zero-Crash]    [2. Security 360°]      [3. Resource Governance]    |
 |  [4. Dual-Bank A/B] [5. Granular Perms]     [6. Neuro-IPC Bus]          |
 |  ------------------ [7. NeuroWindowManager ES6] ----------------------  |
 +-------------------------------------------------------------------------+
```

1. **Zero-Crash Architecture (Recovery Shield)**: Intercepción automática de excepciones no capturadas y promesas asíncronas (`window.onerror`, `window.onunhandledrejection`, `safe_execute`).
2. **Seguridad Perimetral 360°**: Autenticación por roles (**ROOT**, **OPERADOR**, **SISTEMA**), tokens de sesión `neuro_session_token`, registro inmutable de auditoría y verificación de firmas hash SHA-256.
3. **Gobernanza de Recursos (`SovereignResourceGovernor`)**: Monitoreo dinámico de CPU, RAM, GPU y latencias con limitación de tasa (rate-limiting) y límite estricto de 5000ms para DSL.
4. **Dual-Bank A/B + Paridad Par/Impar (`verificar_arquitectura_par_impar`)**: Sistema redundante de arranque en dos bancos (`BankA`/`BankB`) con prueba de paridad en anillo-0 y rollback instantáneo.
5. **Permisos Granulares por Aplicación (`SovereignAppPermissions`)**: Manifiesto estándar `app.json` por aplicación con validación estricta (`audio`, `network`, `display`, `storage`, `terminal`).
6. **Bus Neuro-IPC (Neuro-Bus Event Stream)**: Canal de comunicación inter-proceso pub/sub para streaming de telemetría y eventos.
7. **Gestor de Ventanas ES6 (`NeuroWindowManager`)**: Multinstancia nativa, apilamiento dinámico de capas Z-Index con iluminación de enfoque, anclaje en 8 posiciones y atajos de teclado globales (`Alt+Tab`, `Alt+F4`, `Super+D`, `Super+Flechas`).

---

## 🤝 El Contrato Soberano (Humano - Sistema)

| Tipo de Acción | Responsable | Ejemplos |
| :--- | :--- | :--- |
| **🤖 Autónomas** | **IAGROK (IA)** | Autocuración de UI, balanceo de CPU/RAM, sondeos de paridad, mitigación de caos |
| **👤 Confirmación Obligatoria** | **Operador Humano** | Elevar a ROOT, conceder permisos `app.json`, updates/rollback A/B, exportar perfil, apagar equipo |
| **⛔ Invariantes Inviolables** | **Prohibido Siempre** | Ignorar denegaciones de permisos del usuario, borrado no autorizado de auditoría/claves, comandos destructivos (`format`) |

---

## 📦 Encapsulados y Formatos Compatibles (Sin Mocks)

NeuroOS instala y ejecuta de forma nativa cinco estándares de encapsulación:
- **`*.gx`**: Paquetes binarios soberanos encapsulados para NeuroOS.
- **`*.exe` / `*.msi`**: Aplicaciones nativas de Windows / Subsistema WinApps.
- **`*.apk`**: Aplicaciones de Android (vía ADB / LXC).
- **`*.deb` / `*.AppImage`**: Binarios nativos de Linux.
- **`*.app` / `*.dmg`**: Paquetes nativos de macOS.

---

## 🚀 Inicio Rápido y Ejecución de Pruebas

### 1. Requisitos
- Python 3.8+
- Entorno Windows / Linux / macOS

### 2. Ejecutar Servidor Backend e Interfaz
```bash
python app.py
```
Abre la interfaz en el navegador o visor GXHTML: `http://localhost:5000`

### 3. Ejecutar Suites de Verificación Integrales
```bash
# Test de Integridad de la Plataforma (5/5 OK)
python test_platform_integrity.py

# Test de Integridad de Hero App Quantum Sentinel (4/4 OK)
python test_hero_app_integrity.py
```

---

## 📂 Estructura del Repositorio

```
c:\IAGROK\
├── system_controller.py             # Kernel Controller principal (IAGROK)
├── app.py                           # API REST Flask de enlace
├── sovereign_kernel_manifest.md     # Especificación canónica y Contrato Soberano
├── test_platform_integrity.py       # Suite de pruebas automatizadas de plataforma
├── test_hero_app_integrity.py       # Suite de pruebas automatizadas para Hero App
├── installed_apps/                  # Directorio de apps instaladas (app.json)
│   └── quantum_sentinel/            # Hero App (Quantum Sentinel .gx)
└── NeuroOSDEFINITIVO/
    └── interfaz_gxhtml/
        └── sovereign_face_es5_FINAL.html # Interfaz GXHTML principal con NeuroWindowManager
```

---

## 📜 Licencia y Manifiesto
Consulte el [Manifiesto del Kernel Soberano](file:///c:/IAGROK/sovereign_kernel_manifest.md) para conocer la especificación formal del contrato humano-sistema y las garantías del kernel.
