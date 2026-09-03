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

## Wallet recovery services (owner-initiated only)

Assistance for owners who have lost access to **their own** wallets:
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

**Fee:** 15–20% of recovered value, payable after recovery.

## Research backbone (public archives)

- *Note Universelle X — Le potentiel congruentiel unifié* :
  DOI [10.5281/zenodo.22190260](https://doi.org/10.5281/zenodo.22190260) (v1) ·
  [10.5281/zenodo.22200635](https://doi.org/10.5281/zenodo.22200635) (v2) ·
  [10.5281/zenodo.22204698](https://doi.org/10.5281/zenodo.22204698) (v3)
- HAL : [hal-05731921](https://hal.science/hal-05731921)

## Positioning

Verified phenomenology, not proof. Every table regenerates with one command;
every claim ships with its script.

## Contact (audits, recovery & responsible disclosure)

`fouad.bensmail.audit@proton.me`
