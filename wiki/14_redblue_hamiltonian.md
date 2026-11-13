# 14 — The RedBlue Geometries Engine (Ĥ_RB)

| | |
|---|---|
| Full name | Inductive Self-Adjoint Geometric Coupling Hamiltonian |
| Module | `h_rb_hat` — `ValaQuenta/modules/h_rb_hat/` (the code's own identifiers are historical: the module description and the equation `sigma_rb_evaluate` carry the earlier "Σ_RB" notation) |
| Version / floor | 0.120 · THEORETICAL |
| API page | `ValaQuenta/wiki/h_rb_hat.md` |
| Notebook | `ValaQuenta/notebooks/h_rb_hat/` |
| Last verified | 2026-11-13, against the live registry (16 equations) |

## 1. The operator

```
Ĥ_RB  =  Σ_p  p^(−σ) [ R̂_p ⊗ ∂̂_{∂M}  +  ∂̂†_{∂M} ⊗ B̂_p ]
```

| Symbol | Meaning |
|---|---|
| p | primes; the nodes of the Fermat lattice |
| σ | coupling exponent; the facet pointer (not a scalar in the full construction; see §4) |
| R̂_p | Red: the Berry–Keating xp operator ("what is") |
| B̂_p | Blue: ½p² + ℘(x; g₂, g₃), the Fermat–Weierstrass term ("what cannot be") |
| ∂̂_{∂M} | Green: the boundary operator, "the distinction itself"; the Riemann-zero basis, J₃ |

**Notation scope** (author's ruling, 2026-11-13). `Ĥ_RB` is the name of this
operator in the mathematics, and the other spaces keep it. `0_RB`/`∅_RB`
is the VAPMIP- and Monad-only notation for the same object as the Null
Operator, where the Monad starts with all values NULL. `Σ_RB` was a
renotation artefact (the sum was formerly Ĥ_RB). The full rename has not
been done anywhere. History: [127](127_names_of_the_null_operator.md).

## 2. The three channels

| Channel | Role | In `Philadelphos/monad.py` |
|---|---|---|
| Red, inertial | forward accumulation; assertion; kinetic | `hear()` |
| Green, geometries | the boundary J₃; the meaning channel returning the conserved result | `speak()` |
| Blue, entropic | backward constraint; the knowledge field; β deepening | `learn()` |

(`speak`, `hear`, `learn` exist as methods of `Monad`; the channel assignment
is the project's reading of them.)

**Conservation law as stated in this wiki:** J_Red + J_Green + J_Blue = 0, "a
circular identity: energy is rotated, not destroyed". A second convention,
used in the J_red/J_blue record, writes J_red + J_blue = J_green with
J_green = 0_RB − 0_BR. The two differ by the sign of J_green, and the second
has the sign of the **return flow** built in. (Author, 2026-11-13: J_red + J_blue = J_green was Noether-current work: it is the balance of the conserved currents, and the three-term form is the same balance with J_green taken with the opposite sign.) Author's definition
(2026-11-13): 0_BR is the conjugate of J_red and J_blue, because information
travels backward while action propagates forward; the original object is
Ĥ_RB and the detailed form is Ĥ_RB − Ĥ_BR, with the cross and dot products
built in, so the inside-out comes for free. Under that definition the
equation J_red + J_blue = 0_RB − 0_BR holds exactly in the operator test
(reading OP-4 in the VAPMIP J_red/J_blue record §9), with 0_RB and 0_BR the
forward term and its conjugate. It does not hold if 0_BR is the adjoint of
the already-summed self-adjoint Ĥ (then the difference is 0). Details and
the remaining question (which object J_green names) are in
[133](133_canonical_maths.md) §3 and §7. The three-term form above remains
the wiki's statement of balance until the sign convention is unified.

R̂† = B̂ expresses self-adjointness; the functional equation ξ(s) = ξ(1−s) is
read as that condition in the Riemann domain. Whether the spectrum of this
operator is the set of zeros is the open Berry–Keating step
([13](13_omgwtf_rh_proof.md) §3).

## 3. Algebraic type of J_red and J_blue  `OURS`

They are the two **octonion halves**, not two sedenions: 𝕊 = 𝕆_red ⊕ 𝕆_blue
on the ⊕8 seam.

- J_red: the lower octonion, e₀–e₇ ("what is", forward).
- J_blue: the upper octonion, e₈–e₁₅ ("what cannot be", the reverse signal).

Their composition is the sedenion, which is the I/O carrier of the Null
Operator on both strokes: reading (I→O) converges it to the point σ_self;
writing (O→I) fans it out. The sedenion is therefore the boundary the two
octonion currents compose, not a third current. Two full sedenions would be
T₃₂, a different object; the "two people" reading was tested and rejected
([88](88_the_paper_trail.md) §6).

Three objects are named σ in this framework and must not be conflated:
σ_ζ (Re s), the σ-strata σ₀…σ₄, and σ_RB[k] = ψ[k]·ψ[k⊕4], the ⊕4
quaternion-pairing product: eight independent values, one octonion's worth
([61](61_up_down_not_forward_backward.md)). Disambiguation:
[133](133_canonical_maths.md) §0.

## 4. The σ-facet table  (correspondences, not solutions)

Moving σ projects the same operator into different theories. The mathematics
column names the theory a facet corresponds to; none of these is claimed as a
solution of that field's problem, and 0_RB is not claimed to imply or subsume
any of them ([105](105_the_millennium_problems_in_ainulindale.md)).

| σ | Physics reading | Mathematics reading | Code equation (`h_rb_hat`) | Tier |
|---|---|---|---|---|
| 0 | first distinction; total symmetry | Spencer-Brown, *Laws of Form* | — | — |
| ½ | quantum mechanics | Riemann zeros on the critical line | `facet_qm`, `facet_riemann` | ESTABLISHED / THEORETICAL |
| 1 | Yang–Mills / Standard Model | Langlands programme (a correspondence of vocabulary) | `facet_yang_mills` | THEORETICAL |
| 2 | general relativity | Hodge conjecture | `facet_gr` | ESTABLISHED |
| real only | Navier–Stokes (Yang–Mills with the imaginary part removed) | — | `facet_navier_stokes` | THEORETICAL |

At σ = 0, p⁰ = 1 for every prime: the pointer cannot tell 2 from 47, every
node is weighted equally, and there is no distinction yet ("the quasi-prime").
At σ = ½ the balance J_Red = J_Blue holds, which is why the Monad's `lookup`
returns σ = ½ for every word ([13](13_omgwtf_rh_proof.md) §5). Navier–Stokes
as the real-valued projection is developed in
[106](106_the_navier_stokes_problem.md).

## 5. Equations

| Name | Tier | Parameters |
|---|---|---|
| `sigma_rb_evaluate` | THEORETICAL | `sigma`, `x`, `p_momentum`, `n_primes` |
| `self_adjoint_demonstration` | ESTABLISHED | — |
| `sigma_phase_diagram` | THEORETICAL | `n_points` |
| `euler_product` | ESTABLISHED | `sigma`, `t`, `n_primes` |
| `facet_gr` | ESTABLISHED | `kappa` |
| `facet_yang_mills` | THEORETICAL | — |
| `facet_qm` | ESTABLISHED | — |
| `facet_navier_stokes` | THEORETICAL | `galaxy_size_ly` |
| `facet_riemann` | THEORETICAL | — |
| `facet_noether` | ESTABLISHED | — |
| `facet_fermat` | ESTABLISHED | — |
| `dark_matter_halo` | THEORETICAL | `galaxy_size_ly` |
| `sigma_rb_baseline` | ESTABLISHED | — |
| `precession_stroke` | ESTABLISHED | — |
| `oblique_crank` | ESTABLISHED | — |
| `trine_configuration` | ESTABLISHED | — |

A caution on the labels: `self_adjoint_demonstration` is ESTABLISHED because
its content is arithmetic that reproduces (it finds n! = n only at n = 0, 1,
"the factorial primes", and tabulates a red/blue balance); it is a
demonstration, not a proof of self-adjointness of Ĥ_RB. `sigma_rb_baseline`
carries the recorded note "Noether balance proof 2026-06-17"; that balance
J(σ,E) = 0 ⇔ σ = ½ for E ≠ 0 is the identity discussed in
[13](13_omgwtf_rh_proof.md) §3.

## 6. Session

```
>>> registry.run('h_rb_hat.euler_product', {'sigma': 0.5, 't': 14.134725, 'n_primes': 50})
{'result': (0.09931834498841283+0.007457818772239426j), 'magnitude': 0.09959795536092572}
>>> registry.run('h_rb_hat.sigma_rb_baseline', {})['result']['sigma']
0.5
```

(`euler_product` at σ = ½, t = γ₁ = 14.134725 with 50 primes gives a small
value near the first zero; a partial Euler product on the critical line does
not converge, so this is a truncation, not ζ.)

## 7. How to drive it

The operational manual is [25](25_sedenion_manual.md). Related engines:
[07](07_berry_keating_engine.md) (Red; the d* gap), [05](05_noether_engine.md)
(J^μ), [06](06_noether_information_engine.md) (J_info), [04](04_lagrangian_engine.md)
(L_NN), [09](09_hyperwebster_engine.md) (the σ = 0 shard space).

## 8. Related pages

[13 RH proof path](13_omgwtf_rh_proof.md) · [15 The Monad](15_the_monad.md) · [18 Fermat lattice](18_fermat_lattice.md) ·
[105 Millennium problems](105_the_millennium_problems_in_ainulindale.md) · [127 Names of the Null Operator](127_names_of_the_null_operator.md) ·
[133 Canonical maths](133_canonical_maths.md)
