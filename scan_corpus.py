
#!/usr/bin/env python3
"""scan_corpus.py — pont entre moduli.txt et roca_scanner.py, avec journal de chasse"""
import sys
import roca_scanner
import hunt_log

def main():
    fichier = sys.argv[1] if len(sys.argv) > 1 else "moduli.txt"
    domaine = sys.argv[2] if len(sys.argv) > 2 else "inconnu"
    args = []
    for ligne in open(fichier, encoding="utf-8"):
        ligne = ligne.strip()
        if not ligne:
            continue
        if not ligne.startswith("0x"):
            ligne = "0x" + ligne
        args.append(ligne)
    print(f"[*] {len(args)} moduli transmis au sonar...")
    rc = roca_scanner.main(["roca_scanner.py"] + args)
    drapeaux = rc if isinstance(rc, int) and rc > 0 else 0
    hunt_log.log_scan(domaine, len(args), drapeaux, scanner="roca")
    return rc

if __name__ == "__main__":
    sys.exit(main())