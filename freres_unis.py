#!/usr/bin/env python3
"""
freres_unis.py — les quatre freres en une seule course,
pour les Addenda globaux VI a IX de la v3.

 VI : Sato-Tate modulo l sur E1 (Chebotarev ; THEOREME si image pleine)
 VII : Collatz — Prop 4.1 en masse + marche aleatoire (HEURISTIQUE marquee)
 VIII : lissite de p-1 contre Dickman rho (HEURISTIQUE marquee)
 IX : CM par Z[w] — premiers decomposes, moments du demi-cercle (THEOREME CM)

Usage : python -u freres_unis.py > freres_unis.txt 2>&1
"""
import math, time
from array import array
import hunt_log

def crible(haut):
    t = bytearray([1]) * (haut + 1)
    t[0:2] = b"\x00\x00"
    for i in range(2, int(haut ** 0.5) + 1):
        if t[i]:
            t[i*i:haut+1:i] = bytearray(len(range(i*i, haut+1, i)))
    return t

def ap(p, f):
    qr = bytearray(p)
    for x in range(1, (p + 1) // 2):
        qr[(x * x) % p] = 1
    s = 0
    for x in range(p):
        v = f(x) % p
        if v:
            s += 1 if qr[v] else -1
    return -s

F_E1 = lambda x: x * x * x - x + 1
F_E3 = lambda x: x * x * x + 1

def est_p2(n):
    return n > 0 and (n & (n - 1)) == 0

def pas(n):
    k = ev = 0
    while not est_p2(n):
        if n % 2:
            n = 3 * n + 1
            k += 1
        while n % 2 == 0:
            n //= 2
            ev += 1
    return k, k + ev

def bloc_VI(X=30000):
    t = crible(X)
    ps = [p for p in range(5, X + 1) if t[p]]
    cnt = {2: 0, 3: 0, 5: 0, 7: 0}
    for p in ps:
        a = ap(p, F_E1)
        for l in cnt:
            if a % l == 0:
                cnt[l] += 1
    print(f"[VI] Sato-Tate modulo l — E1: y^2=x^3-x+1, X={X}, n={len(ps)}")
    out = []
    for l in sorted(cnt):
        pred = l / (l * l - 1)
        mes = cnt[l] / len(ps)
        r = mes / pred
        out.append(f"l{l}:{r:.4f}")
        print(f" l={l} predic={pred:.5f} mesure={mes:.5f} ratio={r:.4f}")
    return out

def bloc_VII(X=1000000, K=6):
    print(f"[VII] Collatz — Prop 4.1 en masse + marche, X={X}")
    out = []
    for k in range(1, K + 1):
        mod = 3 ** (k - 1)
        a, nf, ok = 1, 0, 0
        while True:
            n = (4 ** (a + k - 1) - 4 ** k + 3 ** k) // 3 ** k
            if n > X:
                break
            if n >= 3 and not est_p2(n):
                nf += 1
                kk, _ = pas(n)
                if kk == k:
                    ok += 1
            a += mod
        out.append(f"k{k}:{ok}/{nf}")
        print(f" k={k} forme close={nf:4d} verifies={ok:4d} "
              f"accord={'OUI' if ok == nf else 'NON'}")
    sk = ss = cnt = 0
    for n in range(X // 2 + 1, X + 1, 2):
        k, s = pas(n)
        sk += k; ss += s; cnt += 1
    lm = math.log(0.75 * X)
    rk, rs = sk / cnt / lm, ss / cnt / lm
    print(f" marche : moy k/ln n = {rk:.4f} (heuristique 3.4761)")
    print(f" marche : moy sigma/ln n = {rs:.4f} (heuristique 10.428)")
    out.append(f"marche:{rk:.4f}/{rs:.4f}")
    return out

def bloc_VIII(X=1000000):
    lpf = array('I', [0]) * (X + 1)
    for i in range(2, X + 1):
        if lpf[i] == 0:
            for j in range(i, X + 1, i):
                lpf[j] = i
    ps = [i for i in range(5, X + 1, 2) if lpf[i] == i]
    seuils = (2.0, 3.0, 4.0)
    rho = {2.0: 0.30685, 3.0: 0.04861, 4.0: 0.00497}
    cnt = {u: 0 for u in seuils}
    for p in ps:
        m = p - 1
        u = math.log(m) / math.log(lpf[m])
        for u0 in seuils:
            if u >= u0:
                cnt[u0] += 1
    print(f"[VIII] lissite de p-1 contre Dickman — X={X}, n={len(ps)} (heuristique)")
    out = []
    for u0 in seuils:
        mes = cnt[u0] / len(ps)
        r = mes / rho[u0]
        out.append(f"u{int(u0)}:{r:.4f}")
        print(f" u={u0:.0f} rho={rho[u0]:.5f} mesure={mes:.5f} ratio={r:.4f}")
    return out

def bloc_IX(X=30000):
    t = crible(X)
    ps = [p for p in range(5, X + 1) if t[p] and p % 3 == 1]
    m2 = m4 = m6 = 0.0
    z = 0
    for p in ps:
        a = ap(p, F_E3)
        tt = a / (2 * math.sqrt(p))
        m2 += tt * tt; m4 += tt ** 4; m6 += tt ** 6
        if a == 0:
            z += 1
    n = len(ps)
    print(f"[IX] CM Z[w] — E3: y^2=x^3+1, premiers decomposes p=1 mod 3, "
          f"X={X}, n={n}")
    out = []
    for nom, v, pr in zip(("t2", "t4", "t6"),
                          (m2 / n, m4 / n, m6 / n),
                          (0.25, 0.125, 0.078125)):
        out.append(f"{nom}:{v / pr:.4f}")
        print(f" E[{nom}] = {v:.5f} (demi-cercle {pr:.5f}) ratio {v / pr:.4f}")
    print(f" frac(t=0) chez les decomposes = {z / n:.5f} (attendu ~0)")
    out.append(f"zero:{z / n:.4f}")
    return out

def main():
    t0 = time.time()
    notes = []
    for bloc in (bloc_VI, bloc_VII, bloc_VIII, bloc_IX):
        notes += bloc()
        print()
    print(f"[OK] Les quatre freres en {time.time() - t0:.1f} s.")
    hunt_log.log_scan("freres-unis", 0, 0, scanner="freres_unis",
                      notes=" ".join(notes))

if __name__ == "__main__":
    main()
