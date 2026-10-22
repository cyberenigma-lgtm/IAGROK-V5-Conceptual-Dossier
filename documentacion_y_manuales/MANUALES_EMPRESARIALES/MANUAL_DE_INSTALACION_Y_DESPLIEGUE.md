# 📘 Manual de Instalación y Despliegue Empresarial — IAGROK v1.0

> 🛡️ **Registro Oficial de Propiedad Intelectual**: Este software y su documentación están oficialmente registrados y protegidos bajo **SafeCreative Nº SC-2026-IAGROK-NOXFERION**. Autor: José Manuel Moreno (JMM) (Noxferion).

---

## 📌 Requisitos Mínimos del Sistema
* **Sistema Operativo**: Windows 10 / 11 (64-bit) o Linux Ubuntu 20.04+
* **Procesador (CPU)**: Intel / AMD x86_64 Dual-Core 2.0 GHz
* **Memoria RAM**: 4 GB (Optimo: 8 GB)
* **Espacio en Disco**: 500 MB libres
* **Entorno**: Cero dependencias externas en la nube. Ejecución 100% local e independiente.

---

## 🚀 Pasos de Instalación en 1-Clic

### Opción A: Instalación mediante Lanzador Autónomo (Recomendado)
1. Descargue el paquete comprimido de IAGROK Empresarial.
2. Extraiga el archivo ZIP en cualquier directorio (Ej: `C:\IAGROK` o `/opt/iagrok`).
3. Haga doble clic en **`INSTALADOR_AUTOMATICO.bat`** (o ejecute `./INSTALADOR_AUTOMATICO.sh` en Linux).
4. El sistema verificará automáticamente las librerías nativas C++/Rust y abrirá la interfaz gráfica en su navegador predeterminado en `http://127.0.0.1:5000`.

### Opción B: Ejecución mediante Ejecutable Portable (.EXE / .ELF)
1. Vaya a la carpeta `dist/`.
2. Ejecute el archivo **`IAGROK_Empresarial.exe`**.
3. No requiere instalación de Python ni configuraciones de compiladores.

---

## 🧪 Verificación de Instalación Limpia
Para confirmar que la instalación es estable y 100% funcional en su equipo, abra una consola de comandos en la carpeta de IAGROK y ejecute:

```bash
python suite_pruebas_soberanas.py
```

Si el resultado indica **`[ÉXITO TOTAL]: VERIFICACIÓN COMPLETADA`**, el sistema está listo para producción.

---
*Soporte Técnico Oficial*: José Manuel Moreno (JMM) (Noxferion)
