# 78 — T32 Nilpotency: One Shared Mechanism, Two Repositories

| | |
|---|---|
| Scope | the separate `t32_nilpotency` module (Hyperwebster address → T32/GF(2) element → nilpotency test); its wiring into the N-shape engine; the raw result and its chance baseline |
| Origin | 2026-07-11, derived by Claude Sonnet 5, directed by the author: "Separate but importable engine into the n-shape engine." |
| Predecessor | [77](77_hypergon_constructibility.md) |
| Code | `ValaQuenta/modules/t32_nilpotency/` (`hw_address`, `hw_to_t32`, `t32_mul`, `is_zero_divisor_pair`, `is_nilpotent`, `prime_nilpotency_report`); `FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py` (`t32_nilpotency_check()`); `hypergon_constructibility` now imports from here |
| Confidence | the primitives: ESTABLISHED (verified byte for byte against the source) · the two uses: not validated: one failed its control ([77](77_hypergon_constructibility.md)), this one has not been given one |
| Last verified | 2026-11-13: the nilpotency split re-run; output quoted below |

## 1. Why separate

The factoring engine of [77](77_hypergon_constructibility.md) needed the Hyperwebster address and the T32/GF(2) machinery and
exposed two bugs (a placeholder claimed to match the source; a hand-transcribed character table
that was wrong). Both were caught only by numbers failing to match. Splitting the machinery into
one module that every consumer imports removes the failure mode of several copies that can
diverge.

## 2. Wired into the N-shape engine

`fermat_monster_engine.py` gained `t32_nilpotency_check()`, which imports `t32_nilpotency` across
repositories (via `sys.path`, falling back to `None` and not failing silently) and tests its own
`MOONSHINE_PRIMES` list for nilpotency, cross-referenced against the primes that fill the Niemeier
gap {e₁, e₁₁, e₁₅}.

## 3. The raw result, re-run  `MEASURED`

**Listing 1 — nilpotency of the 15 Moonshine primes, split by the Niemeier-gap set** (needs the installed ValaQuenta package; runs from any directory)

```python
import importlib
t3 = importlib.import_module('ValaQuenta.modules.t32_nilpotency.maths')
MOON = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]; gap = [11, 17, 31, 47, 59]
nil = {p: t3.is_nilpotent(t3.hw_to_t32(p)) for p in MOON}
print('nilpotent:', [p for p in MOON if nil[p]], ' (%d of 15 = %.0f%%)' % (sum(nil.values()), 100 * sum(nil.values()) / 15))
print('gap-filling primes all nilpotent:', all(nil[p] for p in gap), ' non-gap:', sum(nil[p] for p in MOON if p not in gap), '/ 10')
print('chance of 5/5 at a 70%% baseline: %.3f = 1 in %.1f' % (0.7**5, 1 / 0.7**5))
```

```
nilpotent: [3, 5, 11, 13, 17, 23, 29, 31, 41, 47, 59, 71]  (12 of 15 = 80%)
gap-filling primes all nilpotent: True  non-gap: 7 / 10
chance of 5/5 at a 70% baseline: 0.168 = 1 in 5.9
```

This reproduces the record: overall 80 %, gap-filling 100 % (n = 5), non-gap 70 % (n = 10). At a 70 %
baseline, 5 of 5 nilpotent happens by chance about 1 time in 6, so the correlation is not strong
evidence. It has **not** been run through the magnitude-matched control that caught the factoring use
failing ([77](77_hypergon_constructibility.md) Listing 1), and until it has, it is held as an observation.
(The non-nilpotent Moonshine primes in the run are 2, 7 and 19.)

## 4. The standing lesson

For the second time in a session the value lay as much in what failed a control (the factoring
conjecture) and in the bugs caught building the tooling as in what held. Both belong in the
record: failed results stay in documentation and code.

## 5. Related pages

[77 hypergon constructibility](77_hypergon_constructibility.md) · [81 SHA-1 collision geometry](81_sha1_real_collision_geometry.md) ·
[135 findings ledger](135_engine_findings_ledger.md)
