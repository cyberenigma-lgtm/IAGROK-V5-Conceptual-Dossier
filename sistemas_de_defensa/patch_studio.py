import os

path = r'C:\NeuroOSDEFINITIVO\capa_cognitiva\neuro_audio_studio.py'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('print(f"\u26a0\ufe0f Error cargando motores de audio: {e}")', 'print(f"[WARN] Error cargando motores de audio: {e}")')
    content = content.replace('print(f"⚠️ Error cargando motores de audio: {e}")', 'print(f"[WARN] Error cargando motores de audio: {e}")')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] neuro_audio_studio.py patched successfully.")
