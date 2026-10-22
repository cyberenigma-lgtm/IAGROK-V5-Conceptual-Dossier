import re

with open('app.py', encoding='utf-8') as f:
    content = f.read()

# ── Parche 1: filtro busqueda web falsa ────────────────────────────────────
old = (
    "    # ── PASO 2: Buscar en internet (solo si es necesario y no es una acción de JARVIS) ──\n"
    "    query_lower = query.lower()\n"
    "    needs_web   = any(kw in query_lower for kw in REALTIME_KEYWORDS) if not is_jarvis_action else False\n"
    "\n"
    "    web_context = \"\"\n"
    "    web_data    = \"\"\n"
    "    if needs_web and not is_jarvis_action:\n"
    "        web_data = web_search_raw(query)\n"
    "        if web_data and \"Error\" not in web_data and \"Sin resultados\" not in web_data:\n"
)

new = (
    "    # ── PASO 2: Buscar en internet (solo si es necesario y no es una acción de JARVIS) ──\n"
    "    query_lower = query.lower()\n"
    "    needs_web   = any(kw in query_lower for kw in REALTIME_KEYWORDS) if not is_jarvis_action else False\n"
    "\n"
    "    # Evitar busquedas falsas para comandos de programacion local\n"
    "    _prog_kw = {\"crea\", \"programa\", \"archivo\", \"script\", \"escribe\", \"codigo\", \"código\", \"ejecuta\", \"run\", \"gcc\", \"python\"}\n"
    "    if any(pk in query_lower for pk in _prog_kw):\n"
    "        needs_web = False\n"
    "\n"
    "    web_context = \"\"\n"
    "    web_data    = \"\"\n"
    "    if needs_web and not is_jarvis_action:\n"
    "        web_data = web_search_raw(query)\n"
    "        if web_data and \"Error\" not in web_data and \"Sin resultados\" not in web_data and \"tráfico inusual\" not in web_data.lower() and \"captcha\" not in web_data.lower():\n"
)

if old in content:
    content = content.replace(old, new, 1)
    print("OK: filtro web aplicado")
elif "_prog_kw" in content:
    print("SKIP: filtro web ya estaba aplicado")
else:
    print("ERROR: bloque no encontrado — revisa manualmente")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# ── Parche 2: corregir SyntaxWarning en intent_classifier.py ──────────────
import ast, pathlib

ic_path = pathlib.Path('intent_classifier.py')
ic = ic_path.read_text(encoding='utf-8')
ic_fixed = ic.replace(r'"mejor\s+no"', r'"mejor\\s+no"')
if ic_fixed != ic:
    ic_path.write_text(ic_fixed, encoding='utf-8')
    print("OK: SyntaxWarning en intent_classifier.py corregido")
else:
    print("SKIP: intent_classifier.py ya correcto")

# ── Verificacion sintaxis app.py ──────────────────────────────────────────
try:
    with open('app.py', encoding='utf-8') as f:
        ast.parse(f.read())
    print("OK: app.py - sintaxis valida")
except SyntaxError as e:
    print(f"ERROR sintaxis app.py: {e}")

print("Parche completado.")
