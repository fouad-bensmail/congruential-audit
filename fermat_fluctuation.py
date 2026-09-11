#!/usr/bin/env python3
"""
fermat_fluctuation.py — compagnon de l'Addendum XI : l'ancrage de Fermat
et la fluctuation differentielle (borne 0 <= n < 2i+1).

Trois pesees :
  1. ancrage : i = isqrt(N), n = N - i^2, borne verifiee ; cas critique
     n = 2i (N = (i+1)^2 - 1) : un seul test ;
  2. physique du saut : T naif = y - i contre prediction z^2 / (2*sqrt(N)),
     avec y = (p+q)/2 et z = (q-p)/2 ;
  3. gain du Crible Pro : y parcouru seulement dans les classes permises
     modulo Q = 8*3*5*7*11 (y^2 - N carrable modulo chaque facteur) ;
     acceleration comparee a 1/f, f = #classes permises / Q.

Usage : python -u fermat_fluctuation.py [K] (defaut K = 25 semi-premiers)
"""
import sys, math, time
import hunt_log

BASES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
MODS = (8, 3, 5, 7, 11)
Q = 8 * 3 * 5 * 7 * 11

def is_prime(n):
    if n < 2:
        return False
    for p in BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def carres_mod8(r):
    return r in (0, 1, 4)

def leg_ok(r, q):
    r %= q
    return r == 0 or pow(r, (q - 1) // 2, q) == 1

def classes_permises(N):
    ok = []
    for a in range(Q):
        bon = True
        for m in MODS:
            r = (a * a - N) % m
            if m == 8:
                if not carres_mod8(r):
                    bon = False
                    break
            elif not leg_ok(r, m):
                bon = False
                break
        if bon:
            ok.append(a)
    return ok

def construire(z, y0):
    y = y0
    if (y - z) % 2 == 0:
        y += 1
    while True:
        p, q = y - z, y + z
        if p > 2 and is_prime(p) and is_prime(q):
            return y, p, q
        y += 2

def main():
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    Y0 = 10 ** 10
    t0 = time.time()

    print(f"[X] fermat-fluctuation — K={K} semi-premiers, ancrage i ~ {Y0}")
    print(" # | z | T naif | T pred | ratio | T crible | accel | 1/f | accel*f")
    ratios, gains = [], []
    for k in range(K):
        z = 3_000_000 + 200_000 * k
        y, p, q = construire(z, Y0 + 7 * k)
        N = y * y - z * z
        i = math.isqrt(N)
        n = N - i * i
        assert 0 <= n <= 2 * i # la borne de la note

        # 1) Fermat naif : combien de tests depuis i+1 ?
        yy = i + 1
        while True:
            r = yy * yy - N
            s = math.isqrt(r)
            if s * s == r:
                break
            yy += 1
        T = yy - i
        assert yy == y

        # 2) prediction differentielle
        P = z * z / (2 * math.sqrt(N))
        ratios.append(T / P)

        # 3) Crible Pro : classes permises modulo Q
        ok = classes_permises(N)
        f = len(ok) / Q
        okset = set(ok)
        assert (y % Q) in okset # le vrai y est permis
        yy = i + 1
        tc = 0
        while True:
            if (yy % Q) in okset:
                tc += 1
                r = yy * yy - N
                s = math.isqrt(r)
                if s * s == r:
                    break
            yy += 1
        accel = T / tc
        gains.append(accel * f)
        print(f" {k:2d} | {z:8d} | {T:6d} | {P:6.1f} | {T/P:.4f} | {tc:8d} "
              f"| {accel:5.1f} | {1/f:5.1f} | {accel*f:.4f}")

    # cas critique de la note : n = 2i => N = (i+1)^2 - 1 => T = 1
    i0 = 10 ** 7
    N0 = (i0 + 1) ** 2 - 1
    assert math.isqrt(N0) == i0 and N0 - i0 * i0 == 2 * i0
    r = (i0 + 1) ** 2 - N0
    print(f"[critique] n = 2i : N = (i+1)^2 - 1, i = {i0} -> T = 1 "
          f"(z = 1), verifie : {r == 1}")

    mr = sum(ratios) / len(ratios)
    mg = sum(gains) / len(gains)
    print(f"[aggregate] ratio moyen T/pred = {mr:.4f} ; accel*f moyen = {mg:.4f}")
    print(f"[OK] {time.time() - t0:.1f} s.")
    hunt_log.log_scan("fermat-fluctuation", K, 0,
                      scanner="fermat_fluctuation",
                      notes=f"T/pred:{mr:.4f} accel*f:{mg:.4f}")

if __name__ == "__main__":
    main()