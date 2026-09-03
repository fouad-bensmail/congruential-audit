#!/usr/bin/env python3
"""
cert_corpus.py v0.2 — Nourrisseur du sonar ROCA (congruential-audit)
Collecte UNIQUEMENT des clés RSA publiques des journaux Certificate
Transparency (crt.sh). Données déjà publiques, cadence polie.
Usage : python cert_corpus.py --domaine proton.me --limite 10
"""
import argparse, hashlib, json, time
from pathlib import Path
import requests
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa

CRT_SH = "https://crt.sh/"
UA = {"User-Agent": "congruential-audit-research/0.2"}

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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domaine", required=True)
    ap.add_argument("--limite", type=int, default=10)
    ap.add_argument("--corpus", default="corpus.json")
    args = ap.parse_args()

    corpus_path = Path(args.corpus)
    connu = {}
    if corpus_path.exists():
        connu = {f["empreinte"]: f for f in json.loads(corpus_path.read_text())}

    print(f"[*] Interrogation de crt.sh pour {args.domaine} ...")
    ids = liste_certificats(args.domaine)
    print(f"[*] {len(ids)} certificats connus ; moisson de {args.limite} max.")

    nouveaux = 0
    essais = 0
    for cid in ids:
        if nouveaux >= args.limite or essais >= 60:
            break
        essais += 1
        try:
            fiche = modulus_du_cert(cid)
        except Exception as exc:
            print(f"    - cert {cid} : ignore ({exc.__class__.__name__} : {exc})")
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

    fiches = list(connu.values())
    corpus_path.write_text(json.dumps(fiches, indent=2))
    Path("moduli.txt").write_text("\n".join(f["n_hex"] for f in fiches) + "\n")
    print(f"[OK] Corpus : {len(fiches)} modulus au total (+{nouveaux} aujourd'hui).")
    print("[OK] moduli.txt pret pour roca_scanner.py")

if __name__ == "__main__":
    main()
