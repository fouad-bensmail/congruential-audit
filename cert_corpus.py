#!/usr/bin/env python3
"""
cert_corpus.py v0.3 — Moissonneur élargi (congruential-audit)
Collecte des clés RSA publiques depuis crt.sh, en lot si désiré.
Journal de chasse branché : chaque domaine laisse sa trace.

Usage unitaire  : python cert_corpus.py --domaine proton.me
Usage en lot    : python cert_corpus.py --batch domaines.txt
Limite relevée  : 50 par défaut (modifiable : --limite 200)
"""
import argparse, hashlib, json, time, sys
from pathlib import Path
import requests
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
import hunt_log

CRT_SH = "https://crt.sh/"
UA = {"User-Agent": "congruential-audit-research/0.3"}

def liste_certificats(domaine):
    r = requests.get(CRT_SH, params={"q": domaine, "output": "json"},
                     headers=UA, timeout=60)
    r.raise_for_status()
    return sorted({e["id"] for e in r.json() if "id" in e})

def charger_cert(data):
    try:
        return x509.load_der_x509_certificate(data)
    except Exception:
        return x509.load_pem_x509_certificate(data)

def date_expire(cert):
    for attr in ("not_valid_after_utc", "not_valid_after"):
        try:
            return getattr(cert, attr).isoformat()
        except Exception:
            continue
    return "inconnu"

def modulus_du_cert(cert_id):
    r = requests.get(CRT_SH, params={"d": cert_id}, headers=UA, timeout=60)
    r.raise_for_status()
    cert = charger_cert(r.content)
    cle = cert.public_key()
    if not isinstance(cle, rsa.RSAPublicKey):
        return None
    nums = cle.public_numbers()
    return {
        "n_hex": format(nums.n, "x"),
        "e": nums.e,
        "sujet": cert.subject.rfc4514_string(),
        "expire_le": date_expire(cert),
        "source": f"crt.sh#{cert_id}",
        "empreinte": hashlib.sha256(r.content).hexdigest(),
    }

def moissonner_domaine(domaine, limite, connu):
    """Moissonne un domaine. Retourne (nouveaux_cles, erreur_ou_None)."""
    print(f"\n[*] Interrogation de crt.sh pour {domaine} ...")
    try:
        ids = liste_certificats(domaine)
    except Exception as exc:
        print(f"    - crt.sh inaccessible pour {domaine} : {exc}")
        return 0, str(exc)
    print(f"[*] {len(ids)} certificats connus ; moisson de {limite} max.")

    nouveaux = 0
    essais = 0
    for cid in ids:
        if nouveaux >= limite or essais >= 60:
            break
        essais += 1
        try:
            fiche = modulus_du_cert(cid)
        except Exception as exc:
            print(f"    - cert {cid} : ignore ({exc.__class__.__name__})")
            time.sleep(2); continue
        if fiche is None:
            print(f"    - cert {cid} : cle non-RSA, ignoree")
        elif fiche["empreinte"] in connu:
            print(f"    - cert {cid} : deja au corpus")
        else:
            connu[fiche["empreinte"]] = fiche
            nouveaux += 1
            print(f"    + cert {cid} : modulus RSA ajoute ({len(fiche['n_hex'])//2} octets)")
        time.sleep(2)
    return nouveaux, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domaine", help="Un seul domaine a moissonner")
    ap.add_argument("--batch", help="Fichier texte contenant une liste de domaines (un par ligne)")
    ap.add_argument("--limite", type=int, default=50,
                    help="Nombre max de nouveaux modulus par domaine (defaut 50)")
    ap.add_argument("--corpus", default="corpus.json")
    args = ap.parse_args()

    # Determiner la liste de domaines
    if args.batch:
        domaines = [l.strip() for l in open(args.batch, encoding="utf-8")
                    if l.strip() and not l.startswith("#")]
    elif args.domaine:
        domaines = [args.domaine]
    else:
        print("[!] Il faut --domaine ou --batch"); sys.exit(1)

    corpus_path = Path(args.corpus)
    connu = {}
    if corpus_path.exists():
        connu = {f["empreinte"]: f for f in json.loads(corpus_path.read_text())}

    total_nouveaux = 0
    domaines_ok = 0
    for domaine in domaines:
        nouv, err = moissonner_domaine(domaine, args.limite, connu)
        total_nouveaux += nouv
        if err is None:
            domaines_ok += 1
        # Trace au journal de chasse
        hunt_log.log_scan(domaine, nouv, 0, scanner="corpus",
                          notes=f"limite={args.limite}, total_corpus={len(connu)}")

    # Sauvegarde finale
    fiches = list(connu.values())
    corpus_path.write_text(json.dumps(fiches, indent=2))
    Path("moduli.txt").write_text("\n".join(f["n_hex"] for f in fiches) + "\n")
    print(f"\n[OK] Corpus : {len(fiches)} modulus au total (+{total_nouveaux} aujourd'hui).")
    print(f"[OK] {domaines_ok}/{len(domaines)} domaines moissonnes.")
    print("[OK] moduli.txt pret pour roca_scanner.py")

if __name__ == "__main__":
    main()
