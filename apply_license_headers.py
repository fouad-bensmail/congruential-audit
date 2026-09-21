#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# =============================================================================
"""
apply_license_headers.py — Bouclier de licence CC BY-NC 4.0.
Ajoute un en-tête de droit d'auteur à chaque script .py du projet.

Mode sans risque : par défaut, DRY-RUN (montre ce qu'il ferait, ne modifie rien).
Pour appliquer réellement : relancez avec l'argument --apply.
"""
import sys
from pathlib import Path

HEADER = '''# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
'''

MARKERS = ["creative commons", "cc by-nc", "copyright", "licence / license"]

def has_license_header(lines):
    head = "".join(lines[:12]).lower()
    return any(m in head for m in MARKERS)

def main():
    apply = "--apply" in sys.argv
    py_files = sorted(Path(".").rglob("*.py"))
    to_modify = []
    for f in py_files:
        if f.name == "apply_license_headers.py":
            continue
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        except Exception as e:
            print(f"[ERREUR] {f} : {e}")
            continue
        if has_license_header(lines):
            print(f"[DEJA PROTEGE] {f}")
        else:
            to_modify.append(f)
            print(f"[A PROTEGER  ] {f}")

    print()
    if not to_modify:
        print("Tous les scripts portent déjà l'en-tête de licence.")
        return
    print(f"{len(to_modify)} script(s) à protéger.")
    if not apply:
        print("Mode DRY-RUN : aucune modification effectuée.")
        print("Relancez avec --apply pour appliquer réellement.")
        return
    for f in to_modify:
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        idx = 0
        if lines and lines[0].startswith("#!"):
            idx = 1
        if len(lines) > idx and "coding" in lines[idx]:
            idx += 1
        new_lines = lines[:idx] + ["\n", HEADER] + lines[idx:]
        f.write_text("".join(new_lines), encoding="utf-8")
    print(f"{len(to_modify)} script(s) protégés.")

if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()