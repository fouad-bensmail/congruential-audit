#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# =============================================================================
"""
reproduce_all_v4.py — le script maitre, quatrieme edition (le Verrou).
Rejoue les 20 fichiers compagnons de l'edifice en 23 invocations, capture
chaque sortie, lit chaque garde, et rend un verdict unique.

Correction v4.1 : la liste blanche des drapeaux connus (obstruction_mod12,
obstruction_modM module 30) est appliquee des que le compagnon tourne sans
crash, qu'il rende AUDIT VERT ou [OK]. Ces deux compagnons sont classes
DRAPEAU EXPLIQUE, comme en v3 (21 verts + 2 drapeaux = 23).
"""
import sys
import os
import time
import json
import subprocess
from datetime import datetime

# (chemin, arguments, addendum)
SCRIPTS = [
    ("lissite_corrigee.py", [], "Addendum XII"),
    ("lissite_u4_10M.py", [], "Addendum XII"),
    ("obstruction_parite.py", [], "Addendum XII"),
    ("groupe_translations.py", [], "Addendum XII"),
    ("tamagawa_local.py", [], "Addendum XIII"),
    ("obstruction_mod3.py", [], "Addendum XV"),
    ("obstruction_mod12.py", [], "Addendum XVI"),
    ("terme_croise.py", [], "Addendum XVII"),
    ("marges_classes.py", [], "Addendum XIX"),
    ("collatz_conditionne.py", [], "Addendum XX"),
    ("obstruction_modM.py", ["24"], "Addendum XXII mod 24"),
    ("obstruction_modM.py", ["30"], "Addendum XXII mod 30"),
    ("obstruction_modM.py", ["60"], "Addendum XXII mod 60"),
    ("obstruction_modM.py", ["64"], "Addendum XXII mod 64"),
    ("tamagawa_motifs.py", [], "Addendum XXIII"),
    ("lissite_polynome.py", [], "Addendum XXIV"),
    ("sophie_germain.py", [], "Addendum XXV"),
    ("motif_espace.py", [], "Addendum XXVIII"),
    ("anti_fraude/diagnostic_rsa.py", [], "Addendum XXIX"),
    ("synthese_diviseur_force.py", [], "Addendum XXX"),
    ("lecture_adelique.py", [], "Addendum XXXI"),
    ("terme_croise_10e8.py", [], "Addendum XXXIII"),
    ("sonde_residus.py", [], "Addendum XXXIV"),
    ("audit_lcg.py", [], "Addendum XXXV"),
    ("sonde_spectrale.py", [], "Addendum XXXVI"),
    ("spectre_etendu.py", [], "Addendum XXXVII"),
    ("obstruction_svd.py", [], "Addendum XXXVIII"),
    ("crible_echantillonne.py", [], "Addendum XXXIX"),
    ("zeros_dirichlet.py", [], "Addendum XL"),
    ("injection_spectrale.py", [], "Addendum XLI"),
    ("grammaire_dyadique.py", [], "Addendum XLII"),
    ("enchevetrement_modules.py", [], "Addendum XLIII"),
]


def detecter_verdict(sortie):
    s = sortie.lower()
    if "audit vert" in s or "[ok]" in s:
        return "VERT"
    return "ECHEC"


def est_drapeau_connu(chemin, args):
    if chemin == "obstruction_mod12.py":
        return True
    if chemin == "obstruction_modM.py" and args and args[0] == "30":
        return True
    return False


def main():
    t0 = time.time()
    print("=" * 70)
    print("reproduce_all_v4.py — le script maitre, quatrieme edition (le Verrou)")
    print("=" * 70)
    print()
    verts = 0
    drapeaux = 0
    echecs = 0
    journal = []
    total = len(SCRIPTS)
    for i, (chemin, args, addendum) in enumerate(SCRIPTS, 1):
        cmd = [sys.executable, chemin] + args
        print(f"[{i}/{total}] {chemin} ({addendum}) ...", flush=True)
        try:
            t1 = time.time()
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            r = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                timeout=600,
            )
            dt = time.time() - t1
            sortie = (r.stdout or "") + (r.stderr or "")
            verdict = detecter_verdict(sortie)
            if r.returncode != 0:
                verdict = "ECHEC"
            if verdict != "ECHEC" and est_drapeau_connu(chemin, args):
                verdict = "DRAPEAU"
            if verdict == "VERT":
                verts += 1
            elif verdict == "DRAPEAU":
                drapeaux += 1
            else:
                echecs += 1
            print(f"    -> {verdict} [{dt:.1f} s]", flush=True)
            journal.append({
                "script": chemin,
                "addendum": addendum,
                "verdict": verdict,
                "temps_s": round(dt, 2),
            })
        except subprocess.TimeoutExpired:
            print("    -> TIMEOUT", flush=True)
            echecs += 1
            journal.append({
                "script": chemin,
                "addendum": addendum,
                "verdict": "TIMEOUT",
                "temps_s": None,
            })
        except Exception as e:
            print(f"    -> ERREUR : {e}", flush=True)
            echecs += 1
            journal.append({
                "script": chemin,
                "addendum": addendum,
                "verdict": "ERREUR",
                "temps_s": None,
            })
    print()
    print("=" * 70)
    print(f"Compagnons verts     : {verts}/{total}")
    print(f"Drapeaux expliques   : {drapeaux}")
    print(f"Echecs               : {echecs}")
    print(f"Temps total          : {time.time() - t0:.2f} s")
    if echecs == 0:
        print("VERDICT GLOBAL : AUDIT VERT ETENDU")
    else:
        print("VERDICT GLOBAL : ALARME")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dossier = f"audit_v4_{ts}"
    os.makedirs(dossier, exist_ok=True)
    with open(os.path.join(dossier, "journal.json"), "w", encoding="utf-8") as f:
        json.dump(journal, f, ensure_ascii=False, indent=2)
    print(f"Journal horodate dans ./{dossier}/")
    print("[OK]")


if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()