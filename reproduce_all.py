#!/usr/bin/env python3
"""
reproduce_all.py — le script maitre d'audit du Crible Congruentiel.

Joue les dix compagnons dans l'ordre du manuscrit, capture chaque sortie,
verifie chaque garde, et produit un verdict unique. Un relecteur tape une
seule commande et voit tout le papier se regenerer.

Usage : python -u reproduce_all.py
Sortie : verdict en console + journal complet dans ./audit_<horodatage>/
"""
import subprocess, sys, os, time, datetime

# Les dix compagnons, dans l'ordre du recit du manuscrit (section 8 + Addenda XIX-XX).
COMPANIONS = [
    ("lissite_corrigee.py",      "rejet du modele naive Dickman + modele corrige"),
    ("lissite_u4_10M.py",        "modele corrige a l'echelle 10^7"),
    ("obstruction_parite.py",    "signature de parite mod 4 (q=2)"),
    ("groupe_translations.py",    "isometries et homotheties des motifs"),
    ("tamagawa_local.py",        "volumes locaux de Tamagawa + independance CRT"),
    ("obstruction_mod3.py",      "obstruction mod 3"),
    ("obstruction_mod12.py",     "obstruction mod 12, volumes locaux exacts"),
    ("terme_croise.py",          "terme croise de composition, courbure de Dickman"),
    ("marges_classes.py",        "marges par classe, retombee crypto"),
    ("collatz_conditionne.py",   "Collatz conditionne mod 12 (resultat negatif)"),
]

TIMEOUT_S = 3600  # garde-fou par compagnon ; le Dell a tout son temps

def run_one(path):
    """Joue un compagnon, renvoie (ok, duree_s, sortie)."""
    t0 = time.time()
    try:
        r = subprocess.run(
            [sys.executable, "-u", path],
            capture_output=True, text=True, timeout=TIMEOUT_S,
        )
        duree = time.time() - t0
        ok = (r.returncode == 0) and ("[OK]" in r.stdout)
        sortie = r.stdout
        if r.stderr.strip():
            sortie += "\n--- STDERR ---\n" + r.stderr
        return ok, duree, sortie
    except subprocess.TimeoutExpired:
        return False, time.time() - t0, f"TIMEOUT apres {TIMEOUT_S} s"
    except Exception as e:
        return False, time.time() - t0, f"EXCEPTION : {e}"

def main():
    t_start = time.time()
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    audit_dir = "audit_" + stamp
    os.makedirs(audit_dir, exist_ok=True)

    print("=" * 78)
    print("AUDIT DU CRIBLE CONGRUENTIEL — reproduction complete en une commande")
    print(f"Python  : {sys.executable}")
    print(f"Journal : ./{audit_dir}/")
    print("=" * 78)

    results = []
    for i, (name, desc) in enumerate(COMPANIONS, 1):
        if not os.path.isfile(name):
            print(f"[{i:2d}/10] {name:<26} ABSENT — fichier introuvable")
            results.append((name, desc, False, 0.0, "fichier absent"))
            continue
        print(f"[{i:2d}/10] {name:<26} en cours... ({desc})")
        ok, duree, out = run_one(name)
        etat = "VERT" if ok else "REFUS"
        print(f"        -> {etat} en {duree:.1f} s")
        with open(os.path.join(audit_dir, name.replace(".py", ".log")),
                  "w", encoding="utf-8") as f:
            f.write(out)
        results.append((name, desc, ok, duree, out))

    total = time.time() - t_start
    n_ok = sum(1 for r in results if r[2])

    print("=" * 78)
    print("VERDICT DE L'AUDIT")
    print("=" * 78)
    print(f"{'compagnon':<28}{'etat':<8}{'duree':>10}")
    print("-" * 78)
    for name, desc, ok, duree, _ in results:
        etat = "VERT" if ok else "REFUS"
        print(f"{name:<28}{etat:<8}{duree:>9.1f} s")
    print("-" * 78)
    print(f"{n_ok}/10 compagnons reproductibles, en {total:.1f} s au total.")

    if n_ok == 10:
        verdict = ("AUDIT VERT : 10/10 compagnons reproductibles. "
                   "Le manuscrit est integralement rejouable en une commande.")
    else:
        verdict = (f"AUDIT INCOMPLET : {n_ok}/10 compagnons verts. "
                   f"Voir les journaux dans ./{audit_dir}/")
    print("\n" + verdict)

    with open(os.path.join(audit_dir, "verdict.txt"), "w", encoding="utf-8") as f:
        f.write(verdict + "\n\n")
        for name, desc, ok, duree, _ in results:
            f.write(f"{name:<28}{'VERT' if ok else 'REFUS':<8}{duree:>8.1f} s\n")

if __name__ == "__main__":
    main()