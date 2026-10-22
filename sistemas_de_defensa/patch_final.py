import os
import re

files_to_patch = [
    r'C:\NeuroOSDEFINITIVO\capa_cognitiva\NEURO_OS_FINAL.py',
    r'C:\NeuroOSDEFINITIVO\capa_cognitiva\NEURO_OS_MASTER.py',
    r'C:\NeuroOSDEFINITIVO\capa_cognitiva\sovereign_desktop_v4.py'
]

for path in files_to_patch:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if 'print(' in line:
                # Replace non-ascii characters in print statements
                line = re.sub(r'[\u0080-\uffff\U00010000-\U0010ffff]', '*', line)
            new_lines.append(line)
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"[OK] Cleaned print statements in {os.path.basename(path)}")
