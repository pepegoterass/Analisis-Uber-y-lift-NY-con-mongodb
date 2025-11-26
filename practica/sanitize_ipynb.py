# -*- coding: utf-8 -*-
"""
Sanitize Jupyter Notebooks by removing invalid Unicode surrogate code points
that cause: UnicodeEncodeError: 'utf-8' ... surrogates not allowed

Usage (PowerShell):
  python sanitize_ipynb.py "HVFHV_MongoDB_Analysis.ipynb" "HVFHV_MongoDB_Analysis - copia.ipynb"
"""
import json
import sys
import os
from typing import Any

SURROGATE_MIN = 0xD800
SURROGATE_MAX = 0xDFFF


def strip_surrogates(s: str) -> str:
    # Remove any code point in surrogate range
    return "".join(ch for ch in s if not (SURROGATE_MIN <= ord(ch) <= SURROGATE_MAX))


def cleanse(obj: Any) -> Any:
    if isinstance(obj, str):
        return strip_surrogates(obj)
    if isinstance(obj, list):
        return [cleanse(x) for x in obj]
    if isinstance(obj, dict):
        return {k: cleanse(v) for k, v in obj.items()}
    return obj


def sanitize_file(path: str) -> None:
    if not os.path.exists(path):
        print(f"⚠️  No existe: {path}")
        return
    backup = path.replace('.ipynb', '_BACKUP_before_sanitize.ipynb')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ No se pudo leer JSON de {path}: {e}")
        return

    cleaned = cleanse(data)
    # Guardar backup (usar ensure_ascii=True para evitar error por surrogates)
    try:
        with open(backup, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=True, indent=1)
        print(f"🗄️  Backup creado: {backup}")
    except Exception as e:
        print(f"❌ No se pudo crear backup de {path}: {e}")
        return

    # Guardar limpio
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=1)
        print(f"✅ Sanitizado OK: {path}")
    except Exception as e:
        print(f"❌ Error al escribir {path}: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python sanitize_ipynb.py <notebook1.ipynb> [<notebook2.ipynb> ...]")
        sys.exit(1)
    for nb in sys.argv[1:]:
        sanitize_file(nb)
