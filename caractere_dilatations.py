#!/usr/bin/env python3
"""
caractere_dilatations.py — vision geometrique : la serie singuliere comme
invariant relatif. Le monoide des dilatations agit sur les motifs ; S se
transforme par un caractere multiplicatif chi_H supporte par la partie sans
carre. Trois pesees (non tautologiques : tout passe par singular()) :
  1. multiplicativite mesuree : mes(d1*d2) = mes(d1)*mes(d2) (copremiers) ;
  2. support sans carre : mes(p^2.H) = mes(p.H) ;
  3. universalite : meme loi de caractere pour cousins, sexys, quadruple.
Garde : mes(d) == chi_H(d) a 1e-12 pour d = 2..30.
Usage : python -u caractere_dilatations.py [P]   (defaut 1000000)
"""
import sys, time
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

def main():
    P = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    t0 = time.time()
    ps = primes_to(P)
    MOT = {"jumeaux": (0, 2), "cousins": (0, 4), "sexys": (0, 6),
           "quadruple": (0, 2, 6, 8)}
    S = {n: singular(nus(H, ps), ps, len(H)) for n, H in MOT.items()}
    def mes(H, d):
        return singular(nus(tuple(d*h for h in H), ps), ps, len(H)) / S["jumeaux"] if H == MOT["jumeaux"] \
           else singular(nus(tuple(d*h for h in H), ps), ps, len(H)) / singular(nus(H, ps), ps, len(H))
    def chi(H, d):
        nuH = nus(H, ps)
        c = 1.0
        for p in pdiv(d):
            c *= (1.0 - 1.0/p) / (1.0 - nuH[ps.index(p)]/p)
        return c
    print("[1/3] caractere mesure = caractere defini (d = 2..30) ...")
    dev_g = 0.0
    for d in range(2, 31):
        dev_g = max(dev_g, abs(mes(MOT["jumeaux"], d)/chi(MOT["jumeaux"], d) - 1.0))
    print(f"      deviation max = {dev_g:.2e}")
    print("[2/3] multiplicativite mesuree et support sans carre ...")
    dev_m = 0.0
    for (a, b) in [(2, 3), (2, 5), (3, 5), (4, 3), (6, 5), (2, 15), (3, 10), (5, 6)]:
        r = mes(MOT["jumeaux"], a*b) / (mes(MOT["jumeaux"], a) * mes(MOT["jumeaux"], b))
        dev_m = max(dev_m, abs(r - 1.0))
    dev_sq = 0.0
    for p in (2, 3, 5, 7):
        dev_sq = max(dev_sq, abs(mes(MOT["jumeaux"], p*p)/mes(MOT["jumeaux"], p) - 1.0))
    print(f"      mes(d1*d2)/mes(d1)mes(d2) : deviation max = {dev_m:.2e}")
    print(f"      mes(p^2)/mes(p) : deviation max = {dev_sq:.2e}")
    print("[3/3] universalite du caractere (autres motifs) ...")
    dev_u = 0.0
    for n, H in MOT.items():
        for d in (2, 3, 6, 12):
            dev_u = max(dev_u, abs(mes(H, d)/chi(H, d) - 1.0))
        print(f"      {n:9s} : deviation max caractere = {dev_u:.2e}")
    ok = dev_g < 1e-12 and dev_m < 1e-12 and dev_sq < 1e-12 and dev_u < 1e-12
    print(f"[verdict] caractere dilatations : {'VERT' if ok else 'REFUSE'}")
    print(f"[OK] {time.time()-t0:.1f} s")
    hunt_log.log_scan("caractere-dilatations", 3 if ok else 0, 0 if ok else 1,
                      scanner="caractere_dilatations",
                      notes=f"P:{P} chi:{dev_g:.1e} mult:{dev_m:.1e} sq:{dev_sq:.1e}")

if __name__ == "__main__":
    main()