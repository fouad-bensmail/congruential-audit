#!/usr/bin/env python3
"""scan_corpus.py — pont entre moduli.txt et roca_scanner.py"""
import sys
import roca_scanner

def main():
    fichier = sys.argv[1] if len(sys.argv) > 1 else "moduli.txt"
    args = []
    for ligne in open(fichier, encoding="utf-8"):
        ligne = ligne.strip()
        if not ligne:
            continue
        if not ligne.startswith("0x"):
            ligne = "0x" + ligne
        args.append(ligne)
    print(f"[*] {len(args)} moduli transmis au sonar...")
    return roca_scanner.main(["roca_scanner.py"] + args)

if __name__ == "__main__":
    sys.exit(main())
