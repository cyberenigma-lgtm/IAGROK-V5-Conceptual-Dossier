# 🔑 Manual de Gestión de Licencias Cifradas y Usuarios — IAGROK v1.0

## 📌 Administración de Licencias para el Administrador
IAGROK incluye un centro de control de licencias cifradas accesible directamente desde el panel de control gráfico (UI) mediante el botón **`🔑 Gestor de Licencias`** o vía la API REST.

---

## 🔑 Emisión de Nuevas Licencias en 1-Clic
Para emitir una nueva licencia a un cliente o usuario:
1. Abra la interfaz web en `http://localhost:5000`.
2. En la barra lateral, pulse el botón amarillo **`🔑 Gestor de Licencias`**.
3. Rellene los campos:
   * **Usuario / Cliente**: Nombre del usuario o identificador.
   * **Empresa**: Nombre de la organización cliente.
   * **Tipo de Licencia**:
     * `Trial (15 días)`
     * `Trial (30 días)`
     * `1 Año (Anual)`
     * `5 Años (Empresarial)`
     * `Vitalicia (Sin Expiración)`
4. Haga clic en **`⚡ GENERAR LICENCIA`**. El token encriptado `HMAC-SHA256` se guardará automáticamente en el registro soberano.

---

## ⚡ Prolongación y Revocación de Licencias
* **Prolongar 30 días**: En la tabla de licencias emitidas, pulse el botón azul **`+30d`** en la fila del usuario correspondiente.
* **Revocar Acceso**: Si una empresa incumple las condiciones, pulse el botón rojo **`Revocar`**. El acceso se cancelará inmediatamente.

---
*Soporte Técnico Oficial*: José Manuel Moreno (JMM) (Noxferion)
