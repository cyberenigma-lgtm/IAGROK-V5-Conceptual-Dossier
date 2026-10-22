# 📘 GUÍA OFICIAL DEL DESARROLLADOR SOBERANO (SOVEREIGN SDK)
## NeuroOS 1.1.0-DEF

---

## 1. Introducción
El **Sovereign Developer SDK** proporciona las herramientas, bibliotecas y CLI oficiales para construir aplicaciones nativas y soberanas (`.gx`, GXHTML, Python) en **NeuroOS 1.1.0-DEF**.

Las aplicaciones soberanas cumplen con las siguientes garantías:
1. **Manifiesto Estándar `app.json`**: Declaración explícita de permisos y punto de entrada.
2. **Gobernanza de Permisos**: Control estricto por `SovereignAppPermissions` (`display`, `storage`, `network`, `audio`, `terminal`).
3. **Gestor de Ventanas ES6**: Multinstancia nativa y snapping vía `NeuroWindowManager`.
4. **Bus Neuro-IPC**: Publicación y suscripción de eventos por `NeuroBus`.

---

## 2. Especificación del Manifiesto `app.json`

Cada aplicación soberana debe incluir en su raíz un archivo `app.json`:

```json
{
  "id": "mi_app_soberana",
  "name": "Mi Aplicación Soberana",
  "version": "1.1.0-DEF",
  "entry_point": "C:/IAGROK/installed_apps/mi_app_soberana/main.gx",
  "icon": "🌀",
  "permissions": {
    "audio": true,
    "network": true,
    "display": true,
    "storage": true,
    "terminal": false
  },
  "channel": "stable"
}
```

### Tabla de Permisos Granulares

| Permiso | Descripción | Acción si es Denegado |
| :--- | :--- | :--- |
| `display` | Control de resolución y composición gráfica | Renderizado estándar en ventana |
| `storage` | Lectura y escritura en NeuroFS / disco duro | Acceso en modo solo lectura |
| `network` | Conexión a red local e Internet | Aislamiento en sandbox local |
| `audio` | Emisión y captura de audio por hardware | Desactivación de salida de sonido |
| `terminal` | Ejecución de comandos del sistema maestro (ROOT) | Denegación inmediata (PERMISSION_DENIED) |

---

## 3. SovereignSDK CLI

Ubicación: `c:\IAGROK\sdk\sovereign_sdk_cli.py`

### Comandos de Desarrollo:

```bash
# 1. Crear nueva app soberana
python c:\IAGROK\sdk\sovereign_sdk_cli.py new mi_app

# 2. Validar y empaquetar la app
python c:\IAGROK\sdk\sovereign_sdk_cli.py build mi_app

# 3. Instalar app en NeuroOS
python c:\IAGROK\sdk\sovereign_sdk_cli.py install mi_app

# 4. Probar la app en el Sandbox
python c:\IAGROK\sdk\sovereign_sdk_cli.py test mi_app
```

---

## 4. API Frontend GXHTML (`sovereign_sdk.js`)

### Integración con Window Manager:
```javascript
// Crear nueva instancia de ventana
NeuroWindowManager.createInstance("mi_app_id", "Mi App", "<h1>Hola NeuroOS</h1>");

// Aplicar snapping
NeuroWindowManager.snapWindow("mi_app_id", "half-left");
```

### Publicación y Suscripción IPC:
```javascript
// Publicar métrica o evento
NeuroBus.publish("mi_app.event", { status: "ACTIVE", value: 100 });

// Suscribirse a eventos
NeuroBus.subscribe("system.events", function(event) {
  console.log("Evento de sistema recibido:", event);
});
```

---

## 5. API Backend Python (`neuro_sdk.py`)

```python
from sdk.neuro_sdk import NeuroSDK

# Inicializar cliente de app
client = NeuroSDK(app_id="mi_app_soberana")

# Verificar permisos
if client.check_permission("storage"):
    print("Permiso de almacenamiento verificado.")

# Publicar eventos sobre el Neuro-Bus
client.publish_ipc_event("mi_app.status", {"online": True})
```

---
*NeuroOS 1.1.0-DEF — Ecosistema de Desarrollo Soberano.*
