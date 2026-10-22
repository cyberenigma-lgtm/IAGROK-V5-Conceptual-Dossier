# 🛡️ ARQUITECTURA SOBERANA DE ENCAPSULAMIENTO ABI POR PLATAFORMA

**Versión:** 2.0-SOVEREIGN-FINAL  
**Principio de Aislamiento:** Zero-Cross Execution Isolation  

---

## 🏛️ Matriz de Encapsulamiento por Subsistema

En **Neuro-OS**, cada aplicación o binario se ejecuta estrictamente dentro de su cápsula y subsistema de Sandbox asignado:

| Plataforma | Extensión | Subsistema ABI | Sandbox Aislado | Motor de Ejecución |
| :--- | :--- | :--- | :--- | :--- |
| **🪟 Windows NT** | `.exe`, `.bat`, `.cmd` | `Win32 / PE` | `sandbox_vault/neuro_native` | Kernel NT Native Subsystem |
| **🍏 macOS Darwin** | `.app`, `.dmg`, `.pkg` | `Mach-O Darwin` | `sandbox_vault/macos` | `mac_player_engine.py` + `mac_abi_extractor.py` |
| **🐧 Linux POSIX** | `.deb`, `.rpm`, `.AppImage` | `POSIX / GLIBC` | `sandbox_vault/linux` | `abi_native_dispatcher.py` (WSL / POSIX) |
| **🤖 Android ART** | `.apk` | `Dalvik / ART` | `sandbox_vault/android` | `neuro_abi_sandbox_manager.py` (Dalvik JIT) |
| **⚛️ Nativos GX** | `.gx`, `.gxp`, `.bin` | `Sovereign DVTRGA` | `SOVEREIGN_BUNKER.gx` | Core Génesis C / DVTRGAS-30 |

---

## 🔒 Reglas de Seguridad y Cero Cruzado

1. **Prohibición de Fallback Cruzado**: Una aplicación `.app` o `.apk` **jamás** debe invocar o abrir ejecutables Win32 `.exe` de Windows para emular funcionalidad.
2. **Aislamiento en Vault**: Cada paquete se copia y registra en su carpeta física `sandbox_vault/<plataforma>/apps/`.
3. **Homeostasis de Recursos**: Si una aplicación de un subsistema intenta acceder a la memoria de otro subsistema sin pasar por el `NeuroBus`, el guardián de homeostasis bloquea la operación instantáneamente.

---

*Especificación oficial de encapsulamiento por ABI de Neuro-OS.*
