© 2026 Fouad Bensmail — Tous droits réservés.
Cette œuvre est mise à disposition selon les termes de la licence
[Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).
Toute utilisation commerciale est interdite sans l'autorisation écrite expresse de l'auteur.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![DOI][![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22950183.svg)](https://doi.org/10.5281/zenodo.22950183)
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

- **Cahier v29** (23 sept. 2026) : DOI [10.5281/zenodo.22901622](https://zenodo.org/doi/10.5281/zenodo.22901622)
  Addendum XXXVII : Spectre étendu. Raffinement méthodologique publié : la
  résolution fréquentielle d'une FFT dépend de l'étendue logarithmique totale.
  Fenêtre élargie [10⁵, 10⁸], 600 paliers, fenêtre de Hann, résolution Δt = 0,91
  (vs 1,36 dans la v28). 15 correspondances aux zéros de ζ (écart < 0,60),
  dont t = 40,86 vs 40,919 (écart 0,06) et t = 20,89 vs 21,022 (écart 0,14).
  Refus v1 publié (α > 3 sur la fenêtre complète) ; v2 restreint la régression
  à [10⁶, 10⁸]. Pics à bas t (4,54 ; 5,45 ; 7,26) suggèrent les premiers
  zéros des fonctions L de Dirichlet mod 12.
  Compagnon spectre_etendu.py (26ᵉ) rejoint le pack.

- **Cahier v30** (23 sept. 2026) : DOI [10.5281/zenodo.22908992](https://zenodo.org/doi/10.5281/zenodo.22908992)
  Addendum XXXVIII : le rang de l'obstruction. SVD de la matrice des log-marges
  (28 classes × 4 profondeurs) : produit externe de rang 1, 99,20 % de la
  variance, L ≈ κ(u)·ln d(a) avec κ = 1,000 ; 2,345 ; 3,979 ; 5,708.
  Le drapeau mod 30 de l'Addendum XXII est absorbé (familles jumelles = rang 1).
  Inspiration publiée : E. Tang, STOC'19 (rang faible mesuré, non supposé).
  Compagnon obstruction_svd.py (27ᵉ) rejoint le pack.

- **Cahier v31** (23 sept. 2026) : DOI [10.5281/zenodo.22909499](https://zenodo.org/doi/10.5281/zenodo.22909499)
  Addendum XXXIX : le cristal à 10⁹. Crible échantillonné (120 fenêtres de 10⁶,
  estimateur pondéré sans biais) : le rang 1 tient jusqu'à 10⁹ sans porter la
  table GPF de 4 Go. Raffinement publié : le modèle binomial à n_eff sous-estime
  la variance de l'estimateur pondéré (facteur 3,01, recalibré sur l'ancre 10⁷).
  Compagnon crible_echantillonne.py (28ᵉ) rejoint le pack.

- **Cahier v32** (23 sept. 2026) : DOI [10.5281/zenodo.22910817](https://zenodo.org/doi/10.5281/zenodo.22910817)
  Addendum XL : les zéros bas-t calculés dans l'atelier, et l'identification
  partiellement refusée. Ferme la boucle de l'Addendum XXXIV. L'instrument
  maison (log-gamma de Lanczos, queues d'Euler–Maclaurin, fonction Z de Hardy)
  calcule les zéros de ζ et des fonctions L de Dirichlet mod 3, 4, 12 sans
  table extérieure. Validé sur ζ (14,134725) et sur la bêta (6,0209).
  L'identification des pics bas-t de l'Addendum XXXVII est partiellement refusée :
  2 sur 5 s'alignent sur χ12 (9,08 et 10,90) ; les trois orphelins (4,54 ; 5,45 ;
  7,26) ne sont pas des zéros de Dirichlet mod 12 — ouverture mesurée, test
  d'injection à venir. Deux refus publiés (v1 : cmath.gamma ; v2 : signe de
  l'intégrale Euler–Maclaurin).
  Compagnon zeros_dirichlet.py (29ᵉ) rejoint le pack.

- **Cahier v33** (24 sept. 2026) : DOI [10.5281/zenodo.22919215](https://zenodo.org/doi/10.5281/zenodo.22919215)
  Addendum XLI : test d'injection spectrale et refus de l'hypothèse Dirichlet mod 12
  pour les pics bas-t. Le modèle d'injection (cos/sin des zéros de χ12 calculés)
  n'explique que 3,8 % de la variance (R2 = 0,038). Les pics orphelins (4,54 ; 5,45 ;
  7,26) persistent après nettoyage, prouvant qu'ils ne sont pas des harmoniques de
  χ12, mais probablement de la fuite spectrale ou de la covariance inter-modules.
  Le cristal haut-t (zéros de ζ) reste intact. Boucle fermée par un refus publié,
  conformément à l'Article II.
  Compagnon injection_spectrale.py (30ᵉ) rejoint le pack.

- **Cahier v34** (24 sept. 2026) : DOI [10.5281/zenodo.22929438](https://doi.org/10.5281/zenodo.22929438)
  Addendum XLII : grammaire_dyadique. Décomposition de l'amplification extrême mod 64 (+824 % à u=5).
  Découverte de l'enchevêtrement dyadique en profondeur : la partie impaire m = (p-1)/2^k est
  structurellement plus lisse aux grandes profondeurs 2-adiques (+73 % à u=5, une fois l'effet
  mécanique soustrait). Conjecture arithmétique ouverte et mesurée. Ouverture de la Voie B (Article VII).
  Le compagnon grammaire_dyadique.py (31ᵉ) rejoint le pack.
- **Cahier v35** (24 sept. 2026) : DOI [10.5281/zenodo.22930061](https://doi.org/10.5281/zenodo.22930061)
  Addendum XLIII : enchevetrement_modules. Test d'universalité de l'enchevêtrement dyadique (Addendum XLII) sous conditionnement par des congruences impaires (mod 3, mod 5). Refus publié (v1 : protocole dégénéré, c1 mod 2^j = strate dyadique). Recalibration publiée (G0 densité cumulative). Découverte d'un couplage inter-modulaire : l'enchevêtrement est directionnellement universel (6/6 classes avec z > 0) mais sélectivement amplifié par les volumes forcés impairs (c1 mod 3 et c1 mod 5). Pendant dyadique du terme croisé de Dickman. Le compagnon enchevetrement_modules.py (32ᵉ) rejoint le pack.
- **Cahier v36** (24 sept. 2026) : DOI [10.5281/zenodo.22931155](https://doi.org/10.5281/zenodo.22931155)
  Addendum XLIV : carte_dyadique. La carte de l'enchevêtrement dyadique sur l'espace des structures à 10^8. Trois gardes tombent et livrent trois vérités : (1) le couplage inter-modulaire n'est pas monotone mais présente une résonance (pic en q=7, 11) ; (2) la famille Sophie Germain ne présente pas de super-enchevêtrement mais une saturation (la contrainte de primalité aplatit le gradient dyadique) ; (3) l'enchevêtrement traverse l'espace des motifs (jumeaux, cousins, sexy) avec une amplitude atténuée. L'ancre globale à 10^8 confirme massivement l'Addendum XLII (>10 sigmas). Le compagnon carte_dyadique.py (33ᵉ) rejoint le pack.
- **Cahier v37** (24 sept. 2026) : DOI [10.5281/zenodo.22932193](https://doi.org/10.5281/zenodo.22932193)
  Addendum XLV : null_stratifie. Retombée cryptographique de la saturation des premiers de Sophie Germain (Addendum XLIV) sur l'Axe 2 de l'Anti-Fraude. Un générateur conforme de premiers SG audité contre le Nul Global lève un faux drapeau de fraude à -4,85 sigma. La stratification du modèle nul par famille déclarée restaure la conformité (z = +0,67). Dégénérescence mesurée des premiers Sûrs (k=1 et m premier à 99,997 %). Refus publiés (v1 : bug ChaCha20 abandonné au profit de numpy.random ; v2 : comparaison erronée et manque de puissance statistique). Le compagnon null_stratifie.py (34ᵉ) rejoint le pack.
- **Cahier v38** (25 sept. 2026) : DOI [10.5281/zenodo.22945763](https://doi.org/10.5281/zenodo.22945763)
  Addendum XLVI : injection_zeta. Clôture de la Direction Spectrale par un refus publié. Le test d'injection des 9 premiers zéros de zêta échoue globalement ($R^2_{in} = -0,23$) malgré une validation croisée positive ($R^2_{pred} = +0,52$). Le paradoxe révèle que les pics haut-t sont des résonances transitoires (non-stationnarité), et non un cristal rigide phase-verrouillé. La frontière du prouvable est tracée. Le compagnon injection_zeta.py (35ᵉ) rejoint le pack. Verrou v4.12 (35 invocations).
- **Cahier v39** (25 sept. 2026) : DOI [10.5281/zenodo.22950183](https://doi.org/10.5281/zenodo.22950183)
  Addendum XLVII : note de clôture de la Direction Spectrale (non-stationnarité mesurée) +
  erratum textuel de la garde G2 de l'Addendum XLVI (blocs contigus K=5, critère médian).
  Évaluation externe III publiée : le paradoxe R²_in = -0,23 / R²_pred = +0,52 est lu comme
  une non-stationnarité orientée en échelle du résidu de C1. La Direction Spectrale
  (XXXIV–XLVI) est close par clarification, non par refus. Pas de compagnon nouveau.
> **Refus Git publié (25 sept. 2026).** Les états v37 et v38 n'ont pas été
> commités en leur temps : leurs compagnons (`null_stratifie.py`,
> `injection_zeta.py`, `crible_echantillonne.py`, `requirements.txt`) ne
> sont entrés au dépôt qu'au commit `a80d070` (v39). Les tags `cahier-v37`
> et `cahier-v38`, absents ou mal pointés, ont été recoupés sur `a80d070`
> avec annotation de coupe tardive. Les DOI Zenodo v37 et v38 demeurent
> l'archive de référence de ces états.

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