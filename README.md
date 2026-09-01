# congruential-audit

**Congruential sieve tools for cryptographic auditing & prime-pattern spectrometry.**

Experimental number-theory toolkit born from the *congruential potential* research
program — a unified singular-series framework across prime pairs, Goldbach
representations, quadratic forms and 2-adic dynamics.

## Tools (coming online)

- `roca_scanner.py` — subgroup test for structurally weak RSA moduli
  (ROCA-style, CVE-2017-15361). Flags bad births without factoring.
- `nonce_spectrometer.py` — congruential bias detector for ECDSA nonces
  (secp256k1 & friends). Second-order terms included.
- The measurement bench: `sg_crible.py`, `goldbach_crible.py`,
  `collatz_tronque.py`, `cousins_sexy_crible.py`, `triplets_crible.py`.

## Research backbone (public archives)

- *Note Universelle X — Le potentiel congruentiel unifié* :
  DOI [10.5281/zenodo.22190260](https://doi.org/10.5281/zenodo.22190260) (v1) ·
  [10.5281/zenodo.22200635](https://doi.org/10.5281/zenodo.22200635) (v2) ·
  [10.5281/zenodo.22204698](https://doi.org/10.5281/zenodo.22204698) (v3)
- HAL : [hal-05731921](https://hal.science/hal-05731921)

## Positioning

Verified phenomenology, not proof. Every table regenerates with one command;
every claim ships with its script.

## Contact (audits & responsible disclosure)

`fouad.bensmail.audit@proton.me`

