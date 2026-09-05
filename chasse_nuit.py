#!/usr/bin/env python3
"""
chasse_nuit.py — la chasse de nuit : moisson elargie, toutes epoques,
chaque modulus passe au sonar ROCA. Poli (2 s), trace au hunt_log.

Usage : python chasse_nuit.py [domaines.txt] [max_par_domaine] (defaut : 300)
"""
import sys, time
import requests
import cert_corpus
import roca_scanner
import hunt_log

CRT_SH = "https://crt.sh/"

def ids_du_domaine(domaine):
    r = requests.get(CRT_SH, params={"q": domaine, "output": "json"},
                     headers=cert_corpus.UA, timeout=60)
    r.raise_for_status()
    return sorted({e["id"] for e in r.json() if "id" in e})

def main():
    fichier = sys.argv[1] if len(sys.argv) > 1 else "domaines.txt"
    maxi = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    domaines = [l.strip() for l in open(fichier, encoding="utf-8")
                if l.strip() and not l.startswith("#")]
    deja = set()
    total = 0
    suspects = 0
    for domaine in domaines:
        print(f"[*] chasse : {domaine}")
        try:
            ids = ids_du_domaine(domaine)
        except Exception as exc:
            print(f" - crt.sh inaccessible : {exc.__class__.__name__}")
            continue
        print(f" {len(ids)} certificats ; ecran sur {min(maxi, len(ids))} max.")
        vus = 0
        for cid in ids:
            if vus >= maxi or cid in deja:
                continue
            deja.add(cid)
            vus += 1
            try:
                fiche = cert_corpus.modulus_du_cert(cid)
            except Exception as exc:
                print(f" - cert {cid} : ignore ({exc.__class__.__name__}")
                time.sleep(2); continue
            if fiche is None:
                continue
            total += 1
            if roca_scanner.is_roca_suspect(int(fiche["n_hex"], 16)):
                suspects += 1
                print(f" ! cert {cid} : ROCA-SUSPECT ({fiche['sujet']})")
            time.sleep(2)
        hunt_log.log_scan(domaine, vus, 0, scanner="chasse-nuit")
    print(f"[OK] Chasse de nuit : {total} modulus cribles, {suspects} suspect(s).")
    hunt_log.log_scan("chasse-nuit-global", total, suspects, scanner="chasse-nuit")

if __name__ == "__main__":
    main()
