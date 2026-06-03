# -*- coding: utf-8 -*-
"""Generate ClimaPlots_<lang>.ts files from translations.py.

Run from this folder:  python make_ts.py
Then compile to .qm:    python ../compile_translations.py
"""
import os
from xml.sax.saxutils import escape

import translations as T

_LANG_ATTR = {"pt": "pt_BR", "zh": "zh_CN", "es": "es", "fr": "fr", "it": "it", "hi": "hi"}
_HERE = os.path.dirname(os.path.abspath(__file__))


def _ts(lang):
    rows = []
    table = T.TRANSLATIONS[lang]
    for src in T.SOURCES:
        tr = table.get(src, "")
        rows.append(
            "    <message>\n"
            f"        <source>{escape(src)}</source>\n"
            f"        <translation>{escape(tr)}</translation>\n"
            "    </message>"
        )
    body = "\n".join(rows)
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<!DOCTYPE TS>\n"
        f'<TS version="2.1" language="{_LANG_ATTR[lang]}">\n'
        "<context>\n"
        "    <name>ClimaPlots</name>\n"
        f"{body}\n"
        "</context>\n"
        "</TS>\n"
    )


def main():
    missing = []
    for lang in T.TRANSLATIONS:
        for src in T.SOURCES:
            if not T.TRANSLATIONS[lang].get(src):
                missing.append((lang, src))
        path = os.path.join(_HERE, f"ClimaPlots_{lang}.ts")
        with open(path, "w", encoding="utf-8") as f:
            f.write(_ts(lang))
        print(f"wrote ClimaPlots_{lang}.ts ({len(T.SOURCES)} messages)")
    if missing:
        print(f"WARNING: {len(missing)} missing translations:")
        for lang, src in missing[:20]:
            print(f"  [{lang}] {src!r}")


if __name__ == "__main__":
    main()
