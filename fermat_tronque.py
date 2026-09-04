#!/usr/bin/env python3
"""
fermat_tronque.py — case vide 4 de la table de Mendeleïev (Note X, §6)
Constante de Fermat tronque : dans la fenetre ancree (parite, Note VII),
densite des candidats X survivants du crible des 14 residus quadratiques.
Prediction locale exacte, sans parametre libre :
    K_F(N) = prod_p (p + (N|p)) / (2p)      ((N|p) = symbole de Legendre)
Pur Python 3, sans bibliotheque.

Usage : python fermat_tronque.py [M] [n_moduli]   (defaut : 10000000 6)
"""
import math, sys, time
import hunt_log

PREMIERS = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

def legendre(a, p):
    r = pow(a % p, (p - 1) // 2, p)
    return -1 if r == p - 1 else r

def survivants(N, M):
    x0 = math.isqrt(N)
    if x0 * x0 < N:
        x0 += 1
    if N % 4 == 1:
        x0 |= 1              # X impair
    else:
        x0 += x0 % 2         # X pair
    arr = bytearray([1]) * M
    kf = 1.0
    for p in PREMIERS:
        kf *= (p + legendre(N, p)) / (2.0 * p)
        base = x0 % p
        pas = 2 % p
        for r in range(p):
            v = (base + pas * r) % p
            v = (v * v - N) % p
            if v and legendre(v, p) == -1:
                arr[r::p] = bytearray(len(arr[r::p]))
    return sum(arr), kf

def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000_000
    nmod = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    t0 = time.time()
    moduli = []
    with open("moduli.txt", encoding="utf-8") as fh:
        for l in fh:
            if l.strip():
                moduli.append(int(l.strip(), 16))
            if len(moduli) >= nmod:
                break
    tot_s = tot_m = 0.0
    print(f"[*] Fermat tronque — fenetre ancree M = {M} ({nmod} modulus)")
    for i, N in enumerate(moduli):
        s, kf = survivants(N, M)
        tot_s += s
        tot_m += M * kf
        print(f"    N#{i} ({N.bit_length()} bits) : {s} survivants, "
              f"K_F = {kf:.3e}, ratio {s/(M*kf):.4f}")
    print(f"[OK] agregat : ratio {tot_s/tot_m:.4f} ; "
          f"rejetes = {100*(1-tot_s/M/len(moduli)):.4f} %")
    print(f"    ({time.time()-t0:.1f} s)")
    hunt_log.log_scan("fermat-tronque", M, 0, scanner="fermat_tronque",
                      notes=f"ratio={tot_s/tot_m:.4f}")

if __name__ == "__main__":
    main()
