# 🛠️ Manual de Troubleshooting y Resolución de Problemas — IAGROK v1.0

## 📌 Guía de Diagnóstico Rápido
Este documento detalla la resolución de los escenarios excepcionales más comunes en el despliegue de IAGROK.

---

## 🚨 Scenario 1: Error al Iniciar el Servidor (Puerto 5000 Ocupado)
**SÍNTOMA**: El servidor no arranca e indica `OSError: [Errno 10048] Address already in use`.
**SOLUCIÓN**:
1. Ejecute en consola: `netstat -ano | findstr :5000` para localizar el proceso previo.
2. Cierre el proceso previo con: `taskkill /F /PID <PID_NUMERO>` o ejecute el script `RESTAURAR_IAGROK_EN_1_CLIC.bat`.

---

## 🚨 Scenario 2: Error de Sintaxis durante la Auto-Mutación
**SÍNTOMA**: Se intentó aplicar un cambio de código fallido.
**SOLUCIÓN**: No requiere intervención manual. El módulo **Transactional Auto-Mutation** de IAGROK detecta automáticamente la falla mediante `py_compile` y realiza un **Auto-Rollback Instantáneo** al snapshot previo.

---

## 🚨 Scenario 3: Bloqueo de Emergencia (Lockdown / Freeze Mode)
**SÍNTOMA**: El sistema indica `MUTATION_FREEZE_MODE: True`.
**SOLUCIÓN**:
1. En la interfaz gráfica, abra el menú de Seguridad y pulse **Descongelar**.
2. O realice una petición POST a `http://localhost:5000/api/sovereign/freeze` con JSON `{"freeze": false}`.

---

## 🚨 Scenario 4: Sobrecarga Térmica o Estrés de Hardware
**SÍNTOMA**: La consola muestra `[NEUROSHIELD ACTIVADO]`.
**SOLUCIÓN**: El sistema ha activado autónomamente el modo defensivo para prevenir corrupción de datos. Una vez que la CPU/RAM se estabilicen por debajo del 85%, NeuroShield se desactivará solo de forma automática.

---
*Soporte Técnico Oficial*: José Manuel Moreno (JMM) (Noxferion)
