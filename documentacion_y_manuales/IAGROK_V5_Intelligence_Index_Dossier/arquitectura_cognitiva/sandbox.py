import sys
import subprocess
import tempfile
import os

def ejecutar_codigo_sandbox(codigo: str, timeout_sec: int = 2) -> str:
    """
    Ejecuta un bloque de código Python de manera aislada (subprocess)
    y retorna su salida estándar (stdout) o los errores encontrados.
    Útil para la auto-curación del Lóbulo Lógico (Sistema 2).
    """
    if not codigo or not codigo.strip():
        return "No hay código para ejecutar."
        
    codigo_limpio = codigo.replace("```python", "").replace("```", "").strip()
    
    # ── Protocolo Guardián: Filtro de Seguridad ──
    # Bloqueamos importaciones que puedan interactuar con el sistema de archivos o procesos de forma destructiva
    dangerous_imports = ['import os', 'from os ', 'import subprocess', 'from subprocess ', 
                         'import shutil', 'from shutil ', 'import sys', 'from sys ', 'import pty']
    
    for word in dangerous_imports:
        if word in codigo_limpio:
            return f"Error de Seguridad (Protocolo Guardián): Bloqueado intento de uso del módulo restringido '{word.strip()}'. La directiva moral prohíbe acciones no supervisadas a nivel de OS en modo Centinela."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(codigo_limpio)
        temp_path = f.name
        
    try:
        resultado = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )
        salida = resultado.stdout.strip()
        errores = resultado.stderr.strip()
        
        out_str = ""
        if salida:
            out_str += f"STDOUT:\n{salida}\n"
        if errores:
            out_str += f"STDERR:\n{errores}\n"
            
        if not out_str:
            out_str = "El código se ejecutó sin errores pero no produjo ninguna salida (stdout vacío)."
            
        return out_str
        
    except subprocess.TimeoutExpired:
        return f"Error: La ejecución del código excedió el tiempo límite de {timeout_sec} segundos (Timeout)."
    except Exception as e:
        return f"Error crítico al ejecutar sandbox: {str(e)}"
    finally:
        try:
            os.remove(temp_path)
        except:
            pass
