# 77 — Hypergon Constructibility: All 16, and the Factorisation Test that Did Not Survive

| | |
|---|---|
| Scope | Gauss–Wantzel constructibility of the 16 sedenion basis primes; the T32/GF(2) nilpotency "factoring conjecture" and its failed control; the two definitions of a prime |
| Origin | 2026-07-11, derived by Claude Sonnet 5, directed by the author: "Create the factorization engine purely … test all hyper *-gons to 16 for the sedenion. Get me a good description of the definition of all the primes." |
| Predecessors | [76](76_sigma_expansion.md), [75](75_abrikosov_lattice.md) |
| Code | `ValaQuenta/modules/hypergon_constructibility/` (`sedenion_hypergon_sweep`, `verify_nilpotent_split_conjecture`, `prime_definition_report`); `VAPMIP/docs/wiki/Tuning-the-Engine.md` Phases 19 and 22; `TuringStack/fermat_sedenion_test.py` |
| Confidence | Part 1 (Gauss–Wantzel): ESTABLISHED · Part 2: an ARTIFACT verdict, reproduced 2026-11-13 and kept |
| Last verified | 2026-11-13: Part 1 and the Part 2 control re-run with the installed engine; output quoted below |

## 1. Resolving a same-session confusion

"The 13-gon" was first checked against the wrong object (`fermat_monster_engine.py`'s
Coxeter-number/Niemeier structure, where h = 13 is achievable). The intended 13-gon is the one
of Phase 19 of `Tuning-the-Engine.md`: dimension e₅ (channel v[5], tied to prime 13) of the
Dirichlet projection, extinct because 13 is not a Fermat prime and has no Cayley–Dickson tower
anchor. This page generalises that single case to all sixteen positions.

## 2. Part 1: all sixteen hyper-n-gons  `ESTABLISHED`

**Gauss–Wantzel** (1796/1837): a regular n-gon is constructible with straightedge and compass
iff n = 2^k × (a product of distinct Fermat primes). Only five Fermat primes are known, 3, 5, 17,
257 and 65537, and whether there are more is open.

Applied to the sixteen basis primes {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53}:

```
CONSTRUCTIBLE (4/16):  e0 = 2, e1 = 3, e2 = 5, e6 = 17
HOLES        (12/16):  e3 = 7, e4 = 11, e5 = 13, e7 = 19, e8 = 23, e9 = 29, e10 = 31,
                       e11 = 37, e12 = 41, e13 = 43, e14 = 47, e15 = 53
```

The engine run (2026-11-13) returns exactly these: constructible [('e0', 2), ('e1', 3), ('e2', 5),
('e6', 17)], 12 holes. (The prime 2 is listed constructible as 2 = 2¹, the power-of-two case; a
"2-gon" is degenerate.) Constructibility is the exception among primes.

## 3. Part 2: the factorisation engine, tested honestly  `ARTIFACT`

Phase 22 corrected the factoring conjecture from the Fermat-midpoint parameters (a, b) to the actual
prime factors (p, q), reporting q at +26 percentage points of T32/GF(2) nilpotency above
baseline. That number reproduces for close-magnitude pairs and does not survive a control that
was not run before:

**Listing 1 — the magnitude-matched control** (needs the installed ValaQuenta package; runs from any directory)

```python
import importlib
hg = importlib.import_module('ValaQuenta.modules.hypergon_constructibility.maths')
v = hg.verify_nilpotent_split_conjecture()
for k in ('close_prime_pairs', 'far_apart_prime_pairs', 'random_pair_control'):
    d = v[k]; print('%-24s n=%3d  p=%.1f%%  q=%.1f%%  both=%.1f%%' % (k, d['n'], d['p_pct'], d['q_pct'], d['both_pct']))
print(v['verdict'])
```

```
close_prime_pairs        n=110  p=69.1%  q=76.4%  both=52.7%
far_apart_prime_pairs    n= 97  p=47.4%  q=45.4%  both=22.7%
random_pair_control      n= 97  p=50.5%  q=56.7%  both=26.8%
ARTIFACT — close-prime elevation does not survive far-apart + random-control comparison; likely a small-magnitude artifact of the Hyperwebster address mapping, not evidence the mechanism tracks factoring relationships
```

The
random control beats the far-apart real-factor pairs on q (56.7 % against 45.4 %); if the
mechanism tracked factoring structure it should not. **Verdict: artifact**, most likely of how
small numbers map through the Hyperwebster base-97 address encoding. Reported plainly, per the
policy that failed predictions stay in the record.

## 4. Two bugs caught mid-build  `kept`

The engine reused `hw_to_t32`. A first attempt used a placeholder (`n & 0xFFFFFFFF`) with an
unverified docstring claiming it "matched exactly"; it did not. A second attempt hand-transcribed the
97-character Hyperwebster charset from memory, giving a 120-character alphabetical string instead of the real
keyboard-row mapping. Both were caught by raw-number mismatches against an earlier standalone
verification, not by trusting the code. The final version took the real string via `repr()`,
checked byte for byte and numerically on 21 test values. This is the origin of the separate
module in [78](78_t32_nilpotency.md).

## 5. The definition of the primes

Two verified definitions, not yet unified:

- **Arithmetic:** no non-trivial factorisation. This is why the AbrikosovTree has the primes as
  leaves surviving all nine Cayley–Dickson levels (no factorisation, so no zero-divisor pair).
- **Geometric:** Gauss–Wantzel constructibility (Part 1), which is the exception.

What connects either to factoring a composite N remains open; Part 2 closes the one candidate
bridge that looked promising in the previous session's narrower test.

## 6. Related pages

[76](76_sigma_expansion.md) · [78 T32 nilpotency](78_t32_nilpotency.md) · [135 findings ledger](135_engine_findings_ledger.md) ·
[19 the Cayley–Dickson tower](19_cayley_dickson_tower.md)
