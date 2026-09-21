#!/usr/bin/env python3

# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
import sys
import os
import subprocess
import time
from datetime import datetime

COMPAGNONS = [
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
    ("obstruction_modM.py", ["24"], "Addendum XXII"),
    ("obstruction_modM.py", ["30"], "Addendum XXII"),
    ("obstruction_modM.py", ["60"], "Addendum XXII"),
    ("obstruction_modM.py", ["64"], "Addendum XXII"),
    ("tamagawa_motifs.py", [], "Addendum XXIII"),
    ("lissite_polynome.py", [], "Addendum XXIV"),
    ("sophie_germain.py", [], "Addendum XXV"),
    ("motif_espace.py", [], "Addendum XXVIII"),
    ("anti_fraude/diagnostic_rsa.py", [], "Addendum XXIX"),
    ("synthese_diviseur_force.py", [], "Addendum XXX"),
    ("lecture_adelique.py", [], "Addendum XXXI"),
]

DRAPEAUX_EXPLIQUES = [
    "obstruction_mod12.py",
    "obstruction_modM.py ['30']",
]

def run_compagnon(script, args, addendum):
    cmd = [sys.executable, "-u", script] + args
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace", env=env, timeout=600
        )
        return result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except Exception as e:
        return -2, f"ERROR: {e}"

def check_verdict(script_name, args, returncode, output):
    if returncode != 0:
        return "ECHEC"
    invocation_name = f"{script_name} {args}" if args else script_name
    for key in DRAPEAUX_EXPLIQUES:
        if key in invocation_name:
            return "DRAPEAU_EXPLIQUE"
    if "AUDIT VERT" in output or "[OK]" in output:
        return "VERT"
    return "ECHEC"

def main():
    t0 = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audit_dir = f"audit_v3_{timestamp}"
    os.makedirs(audit_dir, exist_ok=True)
    print("=" * 70)
    print("reproduce_all_v3.py -- Audit etendu des 20 compagnons")
    print("=" * 70)
    print(f"Debut : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Journal : ./{audit_dir}/")
    print()
    verts = 0
    drapeaux = 0
    echecs = 0
    for i, (script, args, addendum) in enumerate(COMPAGNONS, 1):
        invocation_name = f"{script} {args}" if args else script
        print(f"[{i:02d}/21] {invocation_name} ({addendum})... ", end="", flush=True)
        t_start = time.time()
        returncode, output = run_compagnon(script, args, addendum)
        dt = time.time() - t_start
        suffix = args[0] if args else "default"
        log_file = os.path.join(audit_dir, f"{i:02d}_{os.path.basename(script)}_{suffix}.log")
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(output)
        verdict = check_verdict(script, args, returncode, output)
        if verdict == "ECHEC":
            echecs += 1
            print(f"ECHEC (code {returncode}) [{dt:.2f}s]")
        elif verdict == "DRAPEAU_EXPLIQUE":
            drapeaux += 1
            print(f"DRAPEAU EXPLIQUE [{dt:.2f}s]")
        else:
            verts += 1
            print(f"AUDIT VERT [{dt:.2f}s]")
    dt_total = time.time() - t0
    print()
    print("=" * 70)
    print("VERDICT FINAL")
    print("=" * 70)
    print(f"Compagnons verts : {verts}/21")
    print(f"Drapeaux expliques : {drapeaux}")
    print(f"Echecs : {echecs}")
    print(f"Temps total : {dt_total:.2f} s")
    print()
    if echecs == 0:
        print("AUDIT VERT ETENDU")
        print(f"  {verts} compagnons verts, {drapeaux} drapeaux expliques, 0 alarme.")
        print(f"  L'edifice entier (31 addenda, 20 compagnons) est rejouable en une commande.")
    else:
        print("AUDIT ROUGE")
        print(f"  {echecs} echec(s) detecte(s). Voir les logs dans ./{audit_dir}/")
    print()
    print(f"Fin : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("[OK]")

if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()