# ⚙️ Manual de Configuración y Motor Nativo Híbrido — IAGROK v1.0

## 📌 Configuración de Puertos y Servidor Web
El servidor HTTP local de IAGROK se configura en `app.py`:
* **Puerto Predeterminado**: `5000`
* **Host**: `127.0.0.1` (Local) o `0.0.0.1` (Red Local / LAN)
* **Punto de Entrada Web**: `http://localhost:5000`

---

## 🦀⚡ Configuración del Motor Nativo Híbrido (C++ / Rust)
IAGROK utiliza un puente híbrido en tiempo de ejecución:
1. **`iagrok_native_core.dll` (C++ GCC -O3 SIMD)**: Procesa búsquedas de similitud de vectores a 0.0001 ms.
2. **`iagrok_rust_core.dll` (Rust Cargo Release)**: Garantiza la inmunidad de memoria y previene segfaults.

Para verificar el estado de los motores nativos desde cualquier navegador o software cliente, realice una petición HTTP GET a:
`http://localhost:5000/api/native/status`

---

## 🧠 Ajuste de Cristalizaciones por Lóbulo Cognitivo
Por defecto, la capacidad de cristalizaciones activas en memoria RAM por lóbulo es de **500 cristalizaciones**. Para modificar este valor según la memoria disponible en el servidor:
1. Abra `arquitectura_cognitiva/memoria_tripartita.py`.
2. Modifique la constante `NODULO_CAPACIDAD = 500` al valor deseado (ej: 1000).

---
*Soporte Técnico Oficial*: José Manuel Moreno (JMM) (Noxferion)
