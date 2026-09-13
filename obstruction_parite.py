#!/usr/bin/env python3
"""
obstruction_parite.py — premier compagnon de la Conjecture du Cadre
(Remarque 5.3 du cadre v3) : signature de parite sur P+(p-1) selon p mod 4.

Trois pesees :
  1. signature : pour u = 2..5, proportions rho1(u) = P(P+(p-1) <= (p-1)^{1/u})
     chez p = 1 mod 4 et rho3(u) chez p = 3 mod 4 ; l'ecart rho1 - rho3 est la
     signature de l'obstruction en q = 2 (v2(p-1) >= 2 contre = 1) ;
  2. modele corrige conditionne : M1 = {m <= X, m = 0 mod 4, m+1 sans facteur
     premier <= Q} et M3 = {m = 2 mod 4, idem} ; les ratios modele/mesure par
     classe doivent tenir dans +/- 2 sigma ;
  3. temoin : le modele SANS conditionnement mod 4 doit, lui, rater chaque
     classe dans des sens opposes : c'est la signature meme de l'obstruction.
Garde interne : v2(p-1) moyen = 3,00 chez 1 mod 4 et 1,00 chez 3 mod 4
(exact par construction), et n1 ~ n3 ~ pi(X)/2 (biais de Chebyshev petit).

Usage : python -u obstruction_parite.py [X] [Q] (defauts 10^6, 1000)
"""
import sys, math, time
from array import array
import hunt_log

def cribles(X, Q):
    c = bytearray([1]) * (X + 2); c[0:2] = b"\x00\x00"
    for i in range(2, int(X ** 0.5) + 1):
        if c[i]:
            c[i*i:X+2:i] = bytearray(len(range(i*i, X+2, i)))
    premiers = [i for i in range(2, X + 1) if c[i]]
    Pplus = array('I', [1]) * (X + 2)
    for q in premiers:
        n = len(range(q, X + 2, q))
        Pplus[q:X+2:q] = array('I', [q]) * n
    nosmall = bytearray([1]) * (X + 2)
    for q in premiers:
        if q > Q: break
        nosmall[q:X+2:q] = bytearray(len(range(q, X+2, q)))
    return premiers, Pplus, nosmall

def v2(m):
    return (m & -m).bit_length() - 1

def lisse(Pplus, m, u):
    return Pplus[m] <= m ** (1.0 / u)

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    Q = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    t0 = time.time()
    print(f"[1/3] cribles jusqu'a X = {X}, Q = {Q} ...")
    premiers, Pplus, nosmall = cribles(X, Q)

    print("[2/3] pesees par classe p mod 4 ...")
    US = (2, 3, 4, 5)
    n1 = n3 = 0; s1 = {u: 0 for u in US}; s3 = {u: 0 for u in US}
    v1 = v3 = 0
    for p in premiers:
        if p < 5: continue
        m = p - 1
        if p % 4 == 1:
            n1 += 1; v1 += v2(m)
            for u in US:
                if lisse(Pplus, m, u): s1[u] += 1
        else:
            n3 += 1; v3 += v2(m)
            for u in US:
                if lisse(Pplus, m, u): s3[u] += 1

    M1 = {u: 0 for u in US}; M3 = {u: 0 for u in US}
    MP = {u: 0 for u in US} # modele SANS conditionnement mod 4
    c1 = c3 = cp = 0
    for m in range(4, X + 1, 2):
        if not nosmall[m + 1]: continue
        cp += 1
        ok = {u: lisse(Pplus, m, u) for u in US}
        if m % 4 == 0:
            c1 += 1
            for u in US:
                if ok[u]: M1[u] += 1
        else:
            c3 += 1
            for u in US:
                if ok[u]: M3[u] += 1
        for u in US:
            if ok[u]: MP[u] += 1

    print(f" n1 = {n1} (p=1 mod 4), n3 = {n3} (p=3 mod 4) ; "
          f"v2 moyen = {v1/n1:.2f} / {v3/n3:.2f} (attendu 3.00 / 1.00)")
    print("[3/3] table de la signature :")
    print(" u | rho1 | rho3 | ecart | mod1/mes1 | mod3/mes3 | sansCond1 | sansCond3")
    verts = 0
    for u in US:
        r1 = s1[u]/n1; r3 = s3[u]/n3
        m1 = M1[u]/c1 if c1 else 0.0; m3 = M3[u]/c3 if c3 else 0.0
        p1 = MP[u]/cp; p3 = MP[u]/cp
        sg1 = math.sqrt(r1*(1-r1)/n1); sg3 = math.sqrt(r3*(1-r3)/n3)
        ok1 = abs(m1-r1) <= 2*sg1; ok3 = abs(m3-r3) <= 2*sg3
        verts += ok1 + ok3
        print(f" {u} | {r1:.5f} | {r3:.5f} | {r1-r3:+.5f} | {m1/r1:.4f} | "
              f"{m3/r3:.4f} | {p1/r1:.4f} | {p3/r3:.4f}")
    print(f"[verdict] signature : ecart rho1-rho3 > 0 sur {sum(1 for u in US if s1[u]/n1 > s3[u]/n3)}/{len(US)} decades ; "
          f"modele conditionne dans 2 sigma : {verts}/{2*len(US)}")
    print(f"[OK] {time.time()-t0:.1f} s ; memoire : deux tableaux de {X+2} entiers.")
    hunt_log.log_scan("obstruction-parite", verts, 0,
                      scanner="obstruction_parite",
                      notes=f"X:{X} Q:{Q} sigma-ok:{verts}/{2*len(US)} "
                            f"v2:{v1/n1:.2f}/{v3/n3:.2f}")

if __name__ == "__main__":
    main()
