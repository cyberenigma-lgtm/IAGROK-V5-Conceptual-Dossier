# 🌌 Especificación Técnica Oficial: Estándar Soberano GX-Native (`.gx`)
**Neuro-OS Sovereign Core — Especificación de Arquitectura v1.1.0-DEF**

---

## 1. 📜 Resumen y Propósito del Estándar

El formato **GX-Native (`.gx`)** es el estándar de encapsulamiento binario soberano diseñado para el kernel de **Neuro-OS**. A diferencia de los formatos tradicionales Win32 (`.exe`), POSIX (`.deb`/`.AppImage`), Android (`.apk`) o Mach-O (`.app`), un binario `.gx` interactúa directamente con:

- La capa de abstracción de hardware en **Ring-0**,
- El pipeline vectorial de orden único **DVTRGAS-30 (`0xAA30`)**,
- Y la **ABI soberana GX**.

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                      PAQUETE SOBERANO NATIVO (.GX)                      │
 ├──────────────────┬──────────────────────┬───────────────────────────────┤
 │ CABECERA MÁGICA  │ AISLAMIENTO ASMI-DOE │ TABLA VECTORIAL DVTRGAS-30    │
 │   0x4758 ("GX")  │   Offset Par/Impar   │  Despacho Directo Ring-0      │
 └────────┬─────────┴──────────┬───────────┴──────────────┬────────────────┘
          │                    │                          │
          ▼                    ▼                          ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     NEURO-OS KERNEL BARE-METAL                          │
 └─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 🧬 Estructura del Binario y Disposición en Memoria (Binary Layout)

Un archivo `.gx` consta de cuatro secciones alineadas a bloques de 4096 bytes (Page Boundaries):

| Offset | Campo | Tamaño | Descripción Técnica |
| :--- | :--- | :--- | :--- |
| `0x0000` | `MAGIC_HEADER` | 4 B | Firma binaria `0x47584E54` (`GXNT`). |
| `0x0004` | `VERSION_ABI` | 2 B | Versión de la ABI Soberana (ej. `0x0110`). |
| `0x0006` | `ISOLATION_FLAGS`| 2 B | Banderas ASMI-DOE V5 (`0x0001` Par, `0x0002` Impar). |
| `0x0008` | `DVTRGAS_VECTOR` | 8 B | Dirección del punto de entrada vectorial `0xAA30`. |
| `0x0010` | `MANIFEST_OFFSET`| 8 B | Puntero al manifiesto JSON embebido. |
| `0x0018` | `PAYLOAD_HASH` | 32 B | SHA-256 del código ejecutable. |
| `0x1000` | `CODE_SECTION` | Variable | Código máquina o bytecode soberano. |
| `0xXXXX` | `DATA_SECTION` | Variable | Recursos GXHTML, constantes y assets. |

---

## 3. 🛡️ Modelo de Aislamiento y Permisos Granulares (ASMI-DOE V5 Sandbox)

Cada ejecutable `.gx` se ejecuta en una sandbox gobernada por `ResourceGovernor`, con permisos definidos en el manifiesto embebido:

```json
{
  "gx_format_version": "1.1.0-DEF",
  "id": "quantum_sentinel_gx",
  "name": "Quantum Sentinel Sovereign .GX",
  "entrypoint": "hero.gx",
  "ring_access": 0,
  "permissions": {
    "display": true,
    "network": true,
    "storage": true,
    "audio": true,
    "terminal": false
  },
  "vector_engine": "DVTRGAS-30",
  "isolation_mode": "ASMI_DOE_V5_ODD_EVEN"
}
```

### Reglas de Seguridad Granular:
- **`terminal: false`** → El proceso no puede invocar intérpretes del sistema anfitrión.
- **`ring_access: 0`** → Acceso de baja latencia a contadores de hardware vía IPC soberano.
- **Chaos Shield** → Recuperación automática en `< 5ms` ante fallos de memoria.

---

## 4. 🔄 Interoperabilidad Universal y Puente Multi-OS (Subsystem Bridge)

El estándar `.gx` actúa como contenedor soberano para ejecutar binarios externos mediante traducción ABI:

```
    [ BINARIOS EXTERNOS ]                      [ NEURO-OS INTEGRATION ]
    ├─ Windows .exe   ────────┐
    ├─ Linux .AppImage ───────┼──►  [ MULTI-OS LAUNCHER ] ──► [ MEMORIA RING-0 ]
    ├─ Android .apk   ────────┤     (Direct Dispatch IPC)    (Contenedor .gx)
    └─ macOS .app     ────────┘
```

### 4.1. No Reproducción de Plataformas
Neuro-OS no reproduce ni implementa kernels, runtimes o APIs propietarias.

### 4.2. Compatibilidad mediante Traducción ABI
Los binarios externos se ejecutan mediante traducción directa a la ABI GX, sin cargar runtimes originales.

### 4.3. Uso de Tiendas Externas
El usuario accede a tiendas oficiales desde su entorno. Neuro-OS no redistribuye contenido de terceros.

### 4.4. Sin Emulación ni Virtualización
Neuro-OS no emula ni virtualiza ningún sistema operativo. La ejecución es soberana y nativa mediante GX.

---

## 5. 🧪 Comprobación de Conformidad e Integración

Para validar un paquete `.gx`:

```bash
python test_universal_multios_suite.py
```

Salida esperada:
```text
✓ [ECOSISTEMA NeuroOS Sovereign (.gx)] Ejecución nativa: OK
```

---

## 🛡️ Cláusula de Soberanía y No Reproducción (Protección Legal)

> **Neuro-OS y el formato `.gx` no reproducen, implementan ni distribuyen ningún componente propietario perteneciente a Windows, Linux, macOS o Android.**
> 
> **La ejecución de binarios externos se realiza exclusivamente mediante traducción soberana al ABI GX, sin emulación, virtualización ni implementación de APIs ajenas.**
> 
> **El sistema operativo no integra tiendas de terceros; únicamente permite al usuario acceder a ellas desde su propio entorno.**
> 
> **El formato `.gx` es un estándar original, independiente y soberano.**
