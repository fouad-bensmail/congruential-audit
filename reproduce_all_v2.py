#!/usr/bin/env python3
"""
reproduce_all_v2.py — l'audit etendu en une commande (v2.1).

Rejoue les 17 compagnons/invocations du cahier v16 et rend un verdict unique.
Corrections de la v2.0 :
  (1) Signatures : les dix compagnons historiques signent "[OK]", les nouveaux
      "AUDIT VERT" ; les deux sont acceptees.
  (2) Drapeaux : le compte est lu dans la ligne hunt_log "(n cles, m drapeau(x))",
      pas par recherche naive de mots (obstruction_mod12 publie son propre
      refus historique : le mot REFUS y est legitime).
  (3) Encodage : PYTHONIOENCODING=utf-8 passe aux sous-processus ; sous Windows,
      un tube stdout en cp1252 faisait planter lissite_polynome.py sur le
      caractere "≡" (UnicodeEncodeError, code retour 1). Refus publie.
  (4) Registre : un drapeau connu et publie (Addenda XVI, XXII) est rapporte
      comme EXPLIQUE, jamais comme alarme.

Usage : python -u reproduce_all_v2.py
"""
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

ENV = dict(os.environ)
ENV["PYTHONIOENCODING"] = "utf-8"
ENV["PYTHONUTF8"] = "1"

COMPAGNONS = [
    ("lissite_corrigee", ["python", "lissite_corrigee.py"], "Addenda XII-XIV"),
    ("lissite_u4_10M", ["python", "lissite_u4_10M.py"], "Addendum XV"),
    ("obstruction_parite", ["python", "obstruction_parite.py"], "Addendum XV"),
    ("groupe_translations", ["python", "groupe_translations.py"], "Addendum XII"),
    ("tamagawa_local", ["python", "tamagawa_local.py"], "Addendum XIII"),
    ("obstruction_mod3", ["python", "obstruction_mod3.py"], "Addendum XV"),
    ("obstruction_mod12", ["python", "obstruction_mod12.py"], "Addendum XVI"),
    ("terme_croise", ["python", "terme_croise.py"], "Addendum XVII"),
    ("marges_classes", ["python", "marges_classes.py"], "Addendum XIX"),
    ("collatz_conditionne", ["python", "collatz_conditionne.py"], "Addendum XX"),
    ("obstruction_mod24", ["python", "obstruction_modM.py", "24"], "Addendum XXII"),
    ("obstruction_mod30", ["python", "obstruction_modM.py", "30"], "Addendum XXII"),
    ("obstruction_mod60", ["python", "obstruction_modM.py", "60"], "Addendum XXII"),
    ("obstruction_mod64", ["python", "obstruction_modM.py", "64"], "Addendum XXII"),
    ("tamagawa_motifs", ["python", "tamagawa_motifs.py"], "Addendum XXIII"),
    ("lissite_polynome", ["python", "lissite_polynome.py"], "Addendum XXIV"),
    ("sophie_germain", ["python", "sophie_germain.py"], "Addendum XXV"),
]

REGISTRE = {
    "obstruction_mod12": "Addendum XVI : refus publie de la multiplicativite naive",
    "obstruction_mod30": "Addendum XXII : drapeau de persistance explique (jumelles serrees)",
}

SYMBOLE = {"VERT": "+", "DRAPEAU EXPLIQUE": "*", "DRAPEAU INATTENDU": "!",
           "ERREUR": "x", "INCONNU": "?"}

def analyser(nom, rc, out):
    """Verdict : ERREUR si crash ; sinon signature + compte de drapeaux hunt_log."""
    if rc != 0:
        return "ERREUR", 0
    m = re.search(r"\((\d+) cles, (\d+) drapeau", out)
    nflag = int(m.group(2)) if m else 0
    if not ("[OK]" in out or "AUDIT VERT" in out):
        return "INCONNU", nflag
    if nflag == 0:
        return "VERT", 0
    if nom in REGISTRE:
        return "DRAPEAU EXPLIQUE", nflag
    return "DRAPEAU INATTENDU", nflag

def main():
    t_start = time.time()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(f"audit_v2_{stamp}")
    out_dir.mkdir(exist_ok=True)

    print("=" * 78)
    print(f"AUDIT REPRODUCE_ALL V2.1 — {len(COMPAGNONS)} compagnons")
    print(f"Horodatage : {stamp}   Journal : {out_dir}/")
    print("=" * 78)

    resultats = []
    for nom, cmd, add in COMPAGNONS:
        t0 = time.time()
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=600, encoding="utf-8",
                               errors="replace", env=ENV)
            dt, rc, out = time.time() - t0, r.returncode, r.stdout
            if r.stderr.strip():
                out += "\n--- STDERR ---\n" + r.stderr
        except subprocess.TimeoutExpired:
            dt, rc, out = time.time() - t0, -1, "TIMEOUT"
        except Exception as e:
            dt, rc, out = time.time() - t0, -1, f"EXCEPTION : {e}"

        verdict, nflag = analyser(nom, rc, out)
        with open(out_dir / f"{nom}.txt", "w", encoding="utf-8") as f:
            f.write(f"Commande : {' '.join(cmd)}\nTemps : {dt:.2f} s\n"
                    f"Code retour : {rc}\nVerdict : {verdict} ({nflag} drapeau(x))\n"
                    f"\n{'='*78}\n{out}\n")
        print(f"[{SYMBOLE[verdict]}] {nom:<22} {verdict:<18} {dt:>6.2f} s"
              + (f"  ({nflag} drapeau)" if nflag else ""))
        resultats.append((nom, add, verdict, nflag, dt, rc))

    t_total = time.time() - t_start
    n_vert = sum(1 for r in resultats if r[2] == "VERT")
    n_expl = sum(1 for r in resultats if r[2] == "DRAPEAU EXPLIQUE")
    n_bad = sum(1 for r in resultats if r[2] in ("ERREUR", "INCONNU", "DRAPEAU INATTENDU"))

    lignes = ["=" * 78, "RAPPORT D'AUDIT REPRODUCE_ALL V2.1", "=" * 78,
              f"Horodatage : {stamp}   Temps total : {t_total:.2f} s", "",
              f"VERT                 : {n_vert}/{len(COMPAGNONS)}",
              f"DRAPEAU EXPLIQUE     : {n_expl}/{len(COMPAGNONS)}"]
    for nom, add, verdict, nflag, dt, rc in resultats:
        if verdict == "DRAPEAU EXPLIQUE":
            lignes.append(f"    * {nom} : {REGISTRE[nom]}")
    lignes += [f"PROBLEME (erreur/inconnu/inattendu) : {n_bad}/{len(COMPAGNONS)}", ""]
    for nom, add, verdict, nflag, dt, rc in resultats:
        lignes.append(f"  [{SYMBOLE[verdict]}] {nom:<22} {verdict:<18} {dt:>6.2f} s"
                      + (f"  code {rc}" if rc != 0 else ""))
    lignes += ["", "=" * 78]
    if n_bad == 0:
        lignes.append(f"VERDICT FINAL : AUDIT VERT ETEND — {n_vert} vert(s), "
                      f"{n_expl} drapeau(x) explique(s) au registre, 0 alarme.")
    else:
        lignes.append(f"VERDICT FINAL : {n_bad} PROBLEME(S) — voir journaux individuels.")
    lignes.append("=" * 78)

    rapport = "\n".join(lignes)
    with open(out_dir / "RAPPORT.txt", "w", encoding="utf-8") as f:
        f.write(rapport + "\n")
    print("\n" + rapport)
    print(f"\nJournal complet : {out_dir}/")

if __name__ == "__main__":
    main()