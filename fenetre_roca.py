#!/usr/bin/env python3
"""
fenetre_roca.py — la fenêtre 2016-2017 (ROCA historique) — témoin scientifique
Moissonne dans crt.sh les certificats NES en 2016-2017 (données publiques),
extrait leurs modulus et les passe au sonar roca_scanner.
But : pas un butin — un verdict. Si le sonar retrouve des clés historiques,
le silence d'aujourd'hui n'en sera que plus fort.

Usage : python fenetre_roca.py [domaines.txt] [max_par_domaine]
"""
import sys, time
import requests
import cert_corpus
import roca_scanner
import hunt_log

CRT_SH = "https://crt.sh/"

def ids_de_la_fenetre(domaine, annees=("2016", "2017")):
    r = requests.get(CRT_SH, params={"q": domaine, "output": "json"},
                     headers=cert_corpus.UA, timeout=60)
    r.raise_for_status()
    return sorted({e["id"] for e in r.json()
                   if e.get("not_before", "")[:4] in annees and "id" in e})

def main():
    fichier = sys.argv[1] if len(sys.argv) > 1 else "domaines.txt"
    maxi = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    domaines = [l.strip() for l in open(fichier, encoding="utf-8")
                if l.strip() and not l.startswith("#")]

    deja = set()
    total = 0
    suspects = 0
    for domaine in domaines:
        print(f"[*] fenetre 2016-2017 : {domaine}")
        try:
            ids = ids_de_la_fenetre(domaine)
        except Exception as exc:
            print(f"    - crt.sh inaccessible : {exc.__class__.__name__}")
            continue
        print(f"    {len(ids)} certificats nes en 2016-2017 ; ecran sur {min(maxi, len(ids))} max.")
        vus = 0
        for cid in ids:
            if vus >= maxi or cid in deja:
                continue
            deja.add(cid)
            vus += 1
            try:
                fiche = cert_corpus.modulus_du_cert(cid)
            except Exception as exc:
                print(f"    - cert {cid} : ignore ({exc.__class__.__name__})")
                time.sleep(2); continue
            if fiche is None:
                continue
            total += 1
            if roca_scanner.is_roca_suspect(int(fiche["n_hex"], 16)):
                suspects += 1
                print(f"    ! cert {cid} : ROCA-SUSPECT ({fiche['sujet']})")
            time.sleep(2)
        hunt_log.log_scan(domaine, vus, 0, scanner="fenetre-roca",
                          notes="fenetre=2016-2017")

    print(f"[OK] Fenetre 2016-2017 : {total} modulus historiques cribles, {suspects} suspect(s).")
    hunt_log.log_scan("fenetre-roca-global", total, suspects, scanner="fenetre-roca")

if __name__ == "__main__":
    main()
