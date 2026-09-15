#!/usr/bin/env python3
"""
marges_classes.py — table exploitable des marges par classe mod 12.

Pour chaque classe a mod 12 (a = 1, 5, 7, 11) et chaque u = 2, 3, 4, 5,
pèse la proportion de p-1 avec P+(p-1) <= (p-1)^(1/u), et compare au modèle
global validé (règle m : P+(m) <= m^(1/u)).

Sortie : table avec, pour chaque (a, u) :
  - mesure : proportion mesurée dans la classe a
  - modèle : proportion du modèle global corrigé
  - marge  : (mesure - modèle) / modèle * 100 (en %)
  - sigma  : écart en unités de sigma (budget binomial)

Impact : cette table est exploitable par les ingénieurs crypto pour choisir
les classes de premiers sûrs, et par les théoriciens pour calibrer les
heuristiques de lissité conditionnée.

Usage : python -u marges_classes.py
"""
import math, time
from array import array
import hunt_log

US = (2, 3, 4, 5)
SCALES = (1_000_000, 10_000_000)
CL12 = (1, 5, 7, 11)

def primes_to(n):
    c = bytearray([1]) * (n + 1)
    c[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if c[i]:
            c[i*i:n+1:i] = bytearray(len(range(i*i, n+1, i)))
    return [i for i in range(2, n + 1) if c[i]]

def lpf_sieve(X):
    lp = array('I', [0]) * (X + 1)
    for p in range(2, X + 1):
        if lp[p] == 0:
            lp[p::p] = array('I', [p]) * len(range(p, X + 1, p))
    return lp

def new_bucket():
    return {'n': 0, 's': {u: 0 for u in US}}

def prop(b, u):
    return b['s'][u] / b['n']

def weigh_scale(X):
    ps = primes_to(X)
    lp = lpf_sieve(X)
    g = new_bucket()
    m12 = {a: new_bucket() for a in CL12}
    
    for p in ps:
        if p < 5:
            continue
        m = p - 1
        a12 = p % 12
        
        sm = [lp[m] <= m ** (1.0 / u) for u in US]
        
        g['n'] += 1
        for i, u in enumerate(US):
            if sm[i]:
                g['s'][u] += 1
        
        if a12 in m12:
            m12[a12]['n'] += 1
            for i, u in enumerate(US):
                if sm[i]:
                    m12[a12]['s'][u] += 1
    
    return dict(g=g, m12=m12)

def main():
    t0 = time.time()
    R = {X: weigh_scale(X) for X in SCALES}
    r6, r7 = R[1_000_000], R[10_000_000]
    
    print("=" * 80)
    print("TABLE DES MARGES PAR CLASSE MOD 12 (règle m : P+(m) <= m^(1/u))")
    print("=" * 80)
    
    for X, rr, tag in ((1_000_000, r6, '10^6'), (10_000_000, r7, '10^7')):
        print(f"\nÉchelle {tag} :")
        print("-" * 80)
        print(f"{'Classe':<8} {'u':<4} {'Mesure':<12} {'Modèle':<12} {'Marge %':<12} {'Sigma':<10}")
        print("-" * 80)
        
        for a in CL12:
            for u in US:
                mes = prop(rr['m12'][a], u)
                mod = prop(rr['g'], u)
                marge = (mes - mod) / mod * 100 if mod > 0 else 0.0
                
                # Budget sigma binomial
                n = rr['m12'][a]['n']
                sigma = math.sqrt(mod * (1 - mod) / n) if n > 0 else 1.0
                z = (mes - mod) / sigma if sigma > 0 else 0.0
                
                print(f"c{a:<7} {u:<4} {mes:<12.6f} {mod:<12.6f} {marge:<+12.3f} {z:<+10.2f}")
    
    print("=" * 80)
    print("\nLecture :")
    print("- Marge positive : la classe favorise la lissité (plus de premiers lisses)")
    print("- Marge négative : la classe défavorise la lissité")
    print("- Sigma > 2 : écart significatif (pas une fluctuation)")
    print("- Sigma < 1 : dans le bruit statistique")
    
    print(f"\n[OK] {time.time() - t0:.1f} s")
    
    hunt_log.log_scan("marges-classes", 4, 0,
                      scanner="marges_classes",
                      notes=f"table exploitable pour crypto/ingénierie")

if __name__ == "__main__":
    main()