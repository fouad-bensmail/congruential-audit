© 2026 Fouad Bensmail — Tous droits réservés.
Cette œuvre est mise à disposition selon les termes de la licence
[Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).
Toute utilisation commerciale est interdite sans l'autorisation écrite expresse de l'auteur.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22900934.svg)](https://doi.org/10.5281/zenodo.22900934)

Fouad Bensmail - ORCID: [0009-0006-9541-4207](https://orcid.org/0009-0006-9541-4207)

# congruential-audit

Congruential sieve tools for cryptographic auditing & prime-pattern spectrometry.
Experimental number-theory toolkit born from the congruential potential research
program — a unified singular-series framework across prime pairs, Goldbach
representations, quadratic forms and 2-adic dynamics.

## Tools (coming online)

- `roca_scanner.py` — subgroup test for structurally weak RSA moduli
  (ROCA-style, CVE-2017-15361). Flags bad births without factoring.
- `nonce_spectrometer.py` — congruential bias detector for ECDSA nonces
  (secp256k1 & friends). Second-order terms included.
- The measurement bench: `sg_crible.py`, `goldbach_crible.py`,
  `collatz_tronque.py`, `cousins_sexy_crible.py`, `triplets_crible.py`.

## Wallet recovery services (owner-initiated only)

Assistance for owners who have lost access to their own wallets:
partial passwords, incomplete seed phrases, corrupted backups,
weak-entropy or flawed-PRNG key generation.

**Charter — five non-negotiable rules:**
1. **Owner-initiated only.** I never contact wallet owners; every request
   comes from the owner. Orphaned wallets are never touched.
2. **Proof of ownership before any work.** The client provides what only
   the owner can hold: the wallet file, a privately known seed fragment,
   transaction history, or the original registration email.
3. **Written agreement first.** Scope, fee, confidentiality and
   *no success, no fee* terms are agreed in writing before any computation.
4. **No custody, ever.** The recovered seed/key is handed back through an
   encrypted channel; the owner sweeps the funds themselves.
   I never hold anyone's funds.
5. **Full transparency.** Verifiable identity (GitHub + Zenodo archives),
   documented method, no upfront deposit of any kind.

*Fee: 15–20% of recovered value, payable after recovery.*

## Research backbone (public archives)

- **Note Universelle X — Le potentiel congruentiel unifié :**
  DOI [10.5281/zenodo.22190260](https://doi.org/10.5281/zenodo.22190260) (v1) -
  [10.5281/zenodo.22200635](https://doi.org/10.5281/zenodo.22200635) (v2) -
  [10.5281/zenodo.22204698](https://doi.org/10.5281/zenodo.22204698) (v3)

- **Le Crible Congruentiel — Cahier de mesures expérimentales :**
  concept DOI [10.5281/zenodo.22314057](https://doi.org/10.5281/zenodo.22314057) -
  v5, Addendum X.4 (11 sept. 2026, label Zenodo v6) :
  [10.5281/zenodo.22702536](https://doi.org/10.5281/zenodo.22702536)

- **Vers une théorie expérimentale des potentiels congruentiels — le cadre :**
  v1 : [10.5281/zenodo.22691824](https://doi.org/10.5281/zenodo.22691824) -
  v3 restauré (11 sept. 2026) : [10.5281/zenodo.22700632](https://doi.org/10.5281/zenodo.22700632).
  La v2 ([10.5281/zenodo.22693861](https://doi.org/10.5281/zenodo.22693861)),
  publiée par erreur avec les fichiers du cahier, est en demande de tombale ;
  la note de correction figure dans la description de la v3.
  Cadre v2 (11 sept. 2026, label Zenodo v4) : DOI 10.5281/zenodo.22703451 —
  chapitre 4 clos (4.6 biais a un corps, 4.7 residu evapore, 4.8 etalon valide) ;
  la Conjecture du Cadre devient le probleme principal.
  v6 (11 sept. 2026, label Zenodo v7)
  Cadre v3 (12 sept. 2026, label Zenodo v5) : DOI [collez-le ici] — table de
  Riemann (proportion 2026 prouvée ; RH conjecture), Remarque 5.4 (microscope
  spectral), état de l'art sept. 2026.
  Cadre v4 (13 sept. 2026, label Zenodo v6) : DOI [collez-le ici] —
  Observation 4.9 (signature de parité, deux échelles), statut
  « conjecture corrigée » dans la table des quatre statuts.

- **Cahier v9** (15 sept. 2026, label Zenodo v9) : DOI 10.5281/zenodo.22757396 —
  Addenda XII–XVII : isométries et homothéties des motifs, volumes de Tamagawa
  et CRT mesuré, caractère des dilatations, échelle mod 3 / mod 12, terme
  croisé et courbure de Dickman ; loi de composition close au premier ordre.

- **Cahier v10** (14 sept. 2026) : DOI 10.5281/zenodo.22758370 —
  Addenda XII–XVIII (preuves inconditionnelles T1–T4 + conjecture C1 déclarée).

- **Cahier v11** (15 sept. 2026, label Zenodo v11) : Version v11 : DOI 10.5281/zenodo.22764582
  Addenda XII–XX. Nouveautés v11 : XIX (marges_classes : retombée crypto,
  +159%/-90% à u=5), XX (collatz_conditionne : résultat négatif publié,
  la grille 2×3 ne descend pas dans Collatz).

- **Cahier v12** (15 sept. 2026) : DOI [10.5281/zenodo.22765398](https://zenodo.org/doi/10.5281/zenodo.22765398)
  Addenda XII–XXI. Nouveauté v12 : Addendum XXI (script maître `reproduce_all.py`, AUDIT VERT 10/10 en 21,6 s).

- **Cahier v13** (15 sept. 2026) : DOI [10.5281/zenodo.22798488](https://zenodo.org/doi/10.5281/zenodo.22798488)
  Addenda XII–XXII. Nouveauté v13 : XXII (obstruction_modM : le diviseur
  forcé universel, cartographie mod 24/30/60/64, 3 AUDIT VERT + 1 drapeau
  expliqué). Le compagnon paramétrique obstruction_modM.py rejoint le pack.

- **Cahier v14** (15 sept. 2026) : DOI [10.5281/zenodo.22799566](https://zenodo.org/doi/10.5281/zenodo.22799566)
  Addenda XII–XXIII. Nouveauté v14 : XXIII (tamagawa_motifs : transfert
  Tamagawa universel, 6 motifs admissibles, poignée 2C2 à 1,2e-7).
  Le compagnon tamagawa_motifs.py rejoint le pack.

- **Cahier v15** (15 sept. 2026) : DOI [10.5281/zenodo.22800304](https://zenodo.org/doi/10.5281/zenodo.22800304)
  Addenda XII–XXIV. Nouveauté v15 : XXIV (lissite_polynome : Dickman rejeté
  pour n²+1, décroissance du ratio avec u, signature de la contrainte
  quadratique). Le compagnon lissite_polynome.py rejoint le pack.

- **Cahier v16** (15 sept. 2026) : DOI [10.5281/zenodo.22800726](https://zenodo.org/doi/10.5281/zenodo.22800726)
  Addenda XII–XXV. Nouveauté v16 : XXV (sophie_germain : les premiers sûrs
  sont structurellement plus lisses que la classe 2 mod 3, retombée crypto
  contre-intuitive). Le compagnon sophie_germain.py rejoint le pack.

- **Cahier v17** (17 sept. 2026) : DOI [10.5281/zenodo.22804592](https://zenodo.org/doi/10.5281/zenodo.22804592)
  Addenda XII–XXVI. Nouveauté v17 : XXVI (reproduce_all_v2 : audit étendu
  en une commande, 17 invocations, AUDIT VERT ÉTENDU 15+2+0). Le script
  maître reproduce_all_v2.py rejoint le pack.

- **Cahier v18** (17 sept. 2026) : DOI [10.5281/zenodo.22831375](https://zenodo.org/doi/10.5281/zenodo.22831375)
  Addenda XII–XXVI + Note Universelle VIII (charte de la maison) +
  Addendum XXVII (évaluation externe reçue et réponse) + Annexe A
  (correspondance des termes). La maison se donne une constitution.

- **Cahier v19** (19 sept. 2026) : DOI [10.5281/zenodo.22836872](https://zenodo.org/doi/10.5281/zenodo.22836872)
  Addendum XXVIII : continuité de la série singulière sur l'espace des motifs.
  Théorème T5 candidat confirmé (contraction x4.38, AUDIT VERT).
  Le compagnon motif_espace.py (17e) rejoint le pack.

- **Cahier v21** (19 sept. 2026) : DOI [10.5281/zenodo.22837465](https://zenodo.org/doi/10.5281/zenodo.22837465)
  Addendum XXIX : Anti-fraude universelle (Axe 1). Scanner géométrique de clés RSA.
  La lunette de l'Addendum v4 devient un outil de diagnostic (AUDIT VERT).
  Le compagnon anti_fraude/diagnostic_rsa.py (18e) rejoint le pack.

- **Cahier v22** (19 sept. 2026) : DOI [10.5281/zenodo.22837772](https://zenodo.org/doi/10.5281/zenodo.22837772)
  Addendum XXX : Synthèse de l'obstruction universelle. Taxonomie du diviseur forcé (Spearman > 0.98 sur mod 12, 24, 60).
  Inclut le refus publié et la correction du bug de valuation.
  Le compagnon synthese_diviseur_force.py (19e) rejoint le pack.

- **Cahier v23** (19 sept. 2026) : DOI [10.5281/zenodo.22837954](https://zenodo.org/doi/10.5281/zenodo.22837954)
  Addendum XXXI : Lecture adélique. La série singulière comme nombre de Tamagawa.
  Le Programme de la Forge est clos.
  Le compagnon lecture_adelique.py (20e et dernier) rejoint le pack.

- **Cahier v24** (19 sept. 2026) : DOI [10.5281/zenodo.22840508](https://zenodo.org/doi/10.5281/zenodo.22840508)
  Addendum XXXII : Audit étendu des 20 compagnons. Le script maître
  `reproduce_all_v3.py` rejoue l'édifice entier en une commande
  (EXTENDED GREEN AUDIT, 141 s, 0 alarme).

- **Cahier v25** (19 sept. 2026) : DOI [10.5281/zenodo.22849609](https://zenodo.org/doi/10.5281/zenodo.22849609)
  Addendum XXXIII : Extinction du terme croisé de Dickman (C1) à 10⁸.
  Contraction monotone ×1,15 à ×1,50 entre 10⁶ et 10⁸ sur les 8 mesures
  (4 classes × 2 valeurs de u). Réponse directe à l'objection du relecteur
  (Addendum XXVII, point 2).
  Deux refus de code publiés (v1 : mauvaise couche + normalisation ;
  v2 : décalage d'indice GPF détecté par la nouvelle garde de densité globale).
  Compagnon terme_croise_10e8.py (22ᵉ) rejoint le pack.

- **Cahier v26** (20 sept. 2026) : DOI [10.5281/zenodo.22849756](https://zenodo.org/doi/10.5281/zenodo.22849756)
  Addendum XXXIV : Sonde des résidus du terme croisé (C1). Le résidu porte une
  oscillation structurée (autocorrélation lag-1 ρ1 in [0.62, 0.76]) et l'extinction
  suit une loi de puissance 1/(log X)^alpha avec alpha in [1.6, 2.6]. Ouverture
  mesurée vers les zéros de fonctions L de Dirichlet.
  Compagnon sonde_residus.py (23e) rejoint le pack.

- **Cahier v27** (21 sept. 2026) : DOI [10.5281/zenodo.22886686](https://zenodo.org/doi/10.5281/zenodo.22886686)
  Addendum XXXV : Axe 2 de l'anti-fraude, audit des générateurs congruentiels (LCG).
  RANDU signalé deux fois : parité confinée (prop pairs = 0,000) et biais de
  lissité à +6,34 σ contre l'aléa véritable. GLIBC et MINSTD conformes.
  Deux refus publiés (v1 : graine paire masquée ; v2 : z-score omis).
  Compagnon audit_lcg.py (24ᵉ) rejoint le pack.

- **Cahier v28** (22 sept. 2026) : DOI [10.5281/zenodo.22900934](https://zenodo.org/doi/10.5281/zenodo.22900934)
  Addendum XXXVI : l'Échelle Spectrale. FFT sur le résidu normalisé du terme
  croisé (C1), 300 paliers entre 10⁶ et 10⁸. Pics spectraux détectés à
  t = 13.6, 21.8, 23.1, 24.5, 27.2, 29.9, 39.4 ; trois correspondent aux
  zéros de ζ à moins de 0.5. Deux refus publiés (v1 : règle individuelle ;
  v2 : variable de régression + soustraction de tendance).
  Compagnon sonde_spectrale.py (25ᵉ) rejoint le pack.

## Soumission académique

- **Manuscrit :** "Weighing the obstruction: the smoothness of p-1, its parity signature, and a measured Tamagawa reconstruction of the twin-prime constant"
- **Revue :** Experimental Mathematics (Taylor & Francis)
- **Statut :** Soumis le 15 septembre 2026
- **Submission ID :** 263532965
- **Preprint (Zenodo) :** 10.5281/zenodo.22758846
- **Cahier de laboratoire (v9) :** 10.5281/zenodo.22757396
- **HAL :** [hal-05731921](https://hal.science/hal-05731921) (Note X).
  HAL n'acceptant pas les dépôts de chercheurs indépendants non docteurs
  (politique CCSD, sept. 2026), les travaux suivants vivent sur Zenodo :
  c'est notre archive de référence, et elle suffit.

*Verified phenomenology, not proof. Every table regenerates with one command;
every claim ships with its script.*

## Contact (audits, recovery & responsible disclosure)

`fouad.bensmail.audit@proton.me`