#!/usr/bin/env python3
"""
sato_tate_mod_l.py — Addendum VI : Sato-Tate modulo l.

Pour une courbe elliptique E/Q sans CM, l'image de Galois dans GL_2(F_l)
est pleine pour l assez grand (Serre 1981, ref. [9] du cahier). La
proportion de premiers avec a_p = p + 1 - #E(F_p) ≡ 0 (mod l) vaut alors
exactement l / (l^2 - 1), fraction purement groupiste, independante de E.

On teste E: y^2 = x^3 - x + 1 (sans CM, discriminant -368).

Usage : python sato_tate_mod_l.py [X] (defaut X = 30000)
"""
import sys, time
import hunt_log

def crible(haut):
    t = bytearray([1]) * (haut + 1)
    t[0:2] = b"\x00\x00"
    for i in range(2, int(haut ** 0.5) + 1):
        if t[i]:
            t[i*i:haut+1:i] = bytearray(len(range(i*i, haut+1, i)))
    return t

def ap(p):
    # Pre-calcul des residus quadratiques mod p
    qr = bytearray(p)
    for x in range(1, (p + 1) // 2):
        qr[(x * x) % p] = 1
    s = 0
    for x in range(p):
        v = (x * x * x - x + 1) % p
        if v == 0:
            continue # legendre(0, p) = 0
        s += 1 if qr[v] else -1
    return -s

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    t0 = time.time()
    table = crible(X)
    premiers = [p for p in range(5, X + 1) if table[p]]
    print(f"[*] Sato-Tate modulo l — E: y^2 = x^3 - x + 1")
    print(f" X = {X}, {len(premiers)} premiers >= 5")
    print(f" l | predic | mesure | ratio")
    compte = {2: 0, 3: 0, 5: 0, 7: 0}
    total = len(premiers)
    for i, p in enumerate(premiers, 1):
        a = ap(p)
        for l in compte:
            if a % l == 0:
                compte[l] += 1
        if i % 500 == 0:
            print(f" {i}/{len(premiers)}", end="\r")
    print()
    notes = []
    for l in sorted(compte):
        pred = l / (l * l - 1)
        mesure = compte[l] / total
        ratio = mesure / pred if pred else 0.0
        notes.append(f"l{l}:{ratio:.4f}")
        print(f" {l} | {pred:.5f} | {mesure:.5f} | {ratio:.4f}")
    print(f"[OK] {time.time() - t0:.1f} s.")
    hunt_log.log_scan("sato-tate-mod-l", X, 0, scanner="sato_tate_mod_l",
                       notes=" ".join(notes))

if __name__ == "__main__":
    main()