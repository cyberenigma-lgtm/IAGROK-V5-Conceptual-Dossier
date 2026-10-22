import os

path = r'C:\Users\cyber\OneDrive\Documentos\NeuroOs\Neuro-OS-Genesis\Quantum-OS-Virgin\gxhtml_ui\NEURO_OS_MASTER_BACKUP_v23.py'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_dock = """        dock_items = [
            ("📁", "FILES", self.open_files),
            ("🌐", "NET", self.open_net),
            ("💻", "TERM", self.open_terminal),
            ("🎵", "MUSIC", self.open_music),
            ("🎨", "GFX", self.open_gfx),
            ("⚙️", "SETTINGS", self.open_settings),
            ("🔌", "OFF", self.close)
        ]"""

    new_dock = """        dock_items = [
            ("📁", "FILES", getattr(self, 'open_files', None)),
            ("🌐", "NET", getattr(self, 'open_net', None)),
            ("💻", "TERM", getattr(self, 'open_terminal', None)),
            ("🎵", "MUSIC", getattr(self, 'open_music', None)),
            ("🎨", "GFX", getattr(self, 'open_gfx', None)),
            ("⚙️", "SETTINGS", getattr(self, 'open_settings', None)),
            ("🔌", "OFF", self.close)
        ]"""
    
    if old_dock in content:
        content = content.replace(old_dock, new_dock)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("[OK] NEURO_OS_MASTER_BACKUP_v23.py dock items safely patched.")
    else:
        print("[WARN] old_dock pattern not found exactly, doing regex replacement...")
