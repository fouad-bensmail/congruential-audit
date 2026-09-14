#!/usr/bin/env python3
"""
groupe_translations.py — deuxième compagnon de la Conjecture du Cadre
(Remarque 5.3) : symétries des motifs de paires et covariance de la série
singulière.

Quatre pesées :
  1. invariance exacte : pour tout t, nu_p(H+t) = nu_p(H) => S(H+t)/S(H) = 1 ;
  2. réflexion : nu_p(-H) = nu_p(H) => S(-H) = S(H) ;
  3. covariance des dilatations : loi exacte
     S(d.H) = S(H) * prod_{p|d} (1-1/p)/(1-nu_p(H)/p) ;
  4. ancre empirique à X : comptes de {0,2}, {0,4}, {0,6} ;
     C4/C2 -> 1 et C6/C2 -> 2 dans le bruit de Poisson.
Garde interne : S({0,2}, P) = 1.3203171 (2*C2) à 1e-5.
Usage : python -u groupe_translations.py [X] [P] (défauts 10000000, 1000000)
"""
import sys, math, time
import hunt_log

def primes_to(n):
    c = bytearray([1])*(n+1); c[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5)+1):
        if c[i]:
            c[i*i:n+1:i] = bytearray(len(range(i*i, n+1, i)))
    return [i for i in range(2, n+1) if c[i]]

def pdiv(d):
    f = []; q = 2
    while q*q <= d:
        if d % q == 0:
            f.append(q)
            while d % q == 0: d //= q
        q += 1
    if d > 1: f.append(d)
    return f

def nus(H, ps):
    return [len({h % p for h in H}) for p in ps]

def singular(nu, ps, k):
    s = 1.0
    for p, v in zip(ps, nu):
        s *= (1.0 - v/p) / (1.0 - 1.0/p)**k
    return s

def count_motif(H, X, roots):
    surv = bytearray([1])*(X+1)
    surv[0:2] = b"\x00\x00"
    for h in H:
        for q in roots:
            if q*q > X + h: break
            n0 = (-h) % q
            while n0 < q*q - h: n0 += q
            if n0 <= X:
                surv[n0:X+1:q] = bytearray(len(range(n0, X+1, q)))
    return surv.count(1)

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000_000
    P = int(sys.argv[2]) if len(sys.argv) > 2 else 1_000_000
    t0 = time.time()
    print(f"[1/4] séries singulières et invariances (P = {P}) ...")
    ps = primes_to(P)
    MOT = {"jumeaux": (0, 2), "cousins": (0, 4), "sexys": (0, 6),
           "quadruple": (0, 2, 6, 8)}
    S = {n: singular(nus(H, ps), ps, len(H)) for n, H in MOT.items()}
    garde = abs(S["jumeaux"] - 1.3203171)
    print(f" S(jumeaux) = {S['jumeaux']:.7f} "
          f"(garde |.-1.3203171| = {garde:.2e})")
    dev_inv = 0.0
    for n, H in MOT.items():
        for t in range(1, 31):
            if nus(tuple(h+t for h in H), ps) != nus(H, ps): dev_inv = 1.0
        if nus(tuple(-h for h in H), ps) != nus(H, ps): dev_inv = 1.0
    print(f"[2/4] translations t=1..30 et réflexion : "
          f"déviation max = {dev_inv:.0f} (exact)")
    print("[3/4] covariance des dilatations (loi exacte) :")
    H = MOT["jumeaux"]; nuH = nus(H, ps); dev_dil = 0.0
    for d in (2, 3, 4, 6, 12):
        mes = singular(nus(tuple(d*h for h in H), ps), ps, 2) / S["jumeaux"]
        pred = 1.0
        for p in pdiv(d):
            pred *= (1.0 - 1.0/p) / (1.0 - nuH[ps.index(p)]/p)
        dev_dil = max(dev_dil, abs(mes/pred - 1.0))
        print(f" d={d:2d} : mesure/prediction = {mes/pred:.12f}")
    print(f" déviation max de la loi = {dev_dil:.2e}")
    print(f"[4/4] ancre empirique à X = {X} ...")
    roots = primes_to(int(math.isqrt(X + 8)) + 1)
    C2 = count_motif((0, 2), X, roots)
    C4 = count_motif((0, 4), X, roots)
    C6 = count_motif((0, 6), X, roots)
    r41, r61 = C4/C2, C6/C2
    s41 = math.sqrt(1/C4 + 1/C2); s61 = math.sqrt(1/C6 + 1/C2)
    print(f" C2 = {C2}, C4 = {C4}, C6 = {C6}")
    print(f" C4/C2 = {r41:.4f} (attendu 1, {abs(r41-1)/s41:.2f} sigma)")
    print(f" C6/C2 = {r61:.4f} (attendu 2, {abs(r61-2)/s61:.2f} sigma)")
    ok = (garde < 1e-5 and dev_inv == 0 and dev_dil < 1e-12
          and abs(r41-1) < 3*s41 and abs(r61-2) < 3*s61)
    print(f"[verdict] groupe translations : {'VERT' if ok else 'REFUSE'}")
    print(f"[OK] {time.time()-t0:.1f} s")
    hunt_log.log_scan("groupe-translations", 4 if ok else 0, 0 if ok else 1,
                      scanner="groupe_translations",
                      notes=f"X:{X} P:{P} garde:{garde:.1e} "
                            f"r41:{r41:.4f} r61:{r61:.4f}")

if __name__ == "__main__":
    main()
