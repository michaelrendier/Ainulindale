# 135 — Engine findings ledger (for propagation to ValaQuenta, VAPMIP and the satellites)

| | |
|---|---|
| Purpose | one place where every defect, failed test and discrepancy **found in code during the wiki overhaul** is recorded, so it can be propagated after `FourthAgePapers` is done and the whole GitHub's mathematics is consolidated into the authoritative reference (author's sequence, 2026-11-13) |
| Rule | **nothing listed here has been fixed in code.** Failed results stay in the engines and in the documentation (standing rule). Each row says what was found, where it is documented, and what the later propagation should do |
| Opened | 2026-11-13; appended as the overhaul proceeds (pages 01–55 covered) |
| Verification | every row was reproduced by running the code on 2026-11-13; the runs of the validation engines are in `ContextPlease/claude/scratchpad/2026-11-13_ainulindale_audit/engine_runs/` |

Kinds: **D** defect in code; **T** test design flaw (the test cannot show what it claims); **F** failed prediction (the engine does what it says and the claim is not supported); **R** registry/protocol gap; **X** discrepancy between documents or conventions; **E** environment.

## 1. ValaQuenta

| ID | Kind | Where | Finding | Documented at | Propagation |
|---|---|---|---|---|---|
| VQ-1 | D | `modules/jwst/maths.py::synthetic_spectrum('hydrogen')` | `min` over the four Gaussians where the comment and docstring say "nearest Paschen line" (needs `max`); the spectrum is ≤ 2·10⁻³ everywhere; the registered `synthetic_hydrogen` is labelled ESTABLISHED | [10](10_jwst_engine.md) §4 | fix `min → max`, add a test; relabel until fixed |
| VQ-2 | D | `modules/archimedes_screw` `zeros_upto` | exact to n = 50, then drifts by about +2 (+2.27 at n = 51, +2.81 at n = 60, +1.84 at n = 100) | [133](133_canonical_maths.md) §5 | find the source of the offset past the cached 50 |
| VQ-3 | X | `modules/clay_millennium` | one equation is registered with tier `COMPUTATIONAL`, outside the four-tier scheme (`weakest_tier` returns it unchanged) | [02](02_registry.md) §4 | decide: add the tier or relabel |
| VQ-4 | R | `modules/tier7_cosmos::sedenion_hole_punch` | function exists and is bundled in `full_cosmos`; not registered as an equation. **Deliberate** (author, 2026-11-13): part of the eventual Sedenion Hyperindexing Frame of Reference | [31](31_cavitation_causality_fermat.md) | leave unregistered until that engine exists |
| VQ-5 | R | `modules/bao_mass_gap` | 7/7 `validate` checks pass, but three are tautologies or consistency-with-precision and one rests on an unjustified threshold (`bao_resolvable`, ratio 0.4 > 0.1 with a unit mismatch); `gap_identity` is true to 3 s.f. only | [50](50_bao_mass_gap_engine.md) §§3, 6, 7 | rename the checks honestly; carry d* with its uncertainty |
| VQ-6 | X | wiki ↔ code | module-to-page links: `scale` and `add_scale_sign` both name page 107; nine modules name no Ainulindale page | [01](01_overview.md) §5 | fill the manifests |
| VQ-7 | X | `modules/h_rb_hat` | code identifiers keep the "Σ_RB" notation (module description, `sigma_rb_evaluate`); notation scope ruling: Ĥ_RB in the maths, 0_RB in VAPMIP/Monad only | [14](14_redblue_hamiltonian.md), [127](127_names_of_the_null_operator.md) | rename only when the full rename is decided |
| VQ-8 | T | `tier9_chem.cosic_eiip` | the SOR motif's dominant frequency is mapped to γ₃ with a free scale constant c_bio; a match to one of ~20 zeros is expected; reported as a result | [23](23_resonant_recognition.md) §3 | state c_bio's origin or mark the result as a fit |

## 2. VAPMIP engines (`VAPMIP/engines/`) and `monad.py`

| ID | Kind | Where | Finding | Documented at | Propagation |
|---|---|---|---|---|---|
| VP-1 | E | `e01_operator_selforg.py` | prints nothing and returns `{'error': 'No operators found in vocab'}` because `monad_sedenion.bin` is absent; the only copy is in the old SD-card backup (`TheSDCard/ThePlace/PTorrent/bin_archive/clean/monad_sedenion.bin`, sha256 `c97c272b0657dc92…`) | [27](27_third_age_CS_paper.md) §2 | print the error; locate or rebuild the bin |
| VP-2 | D/F | `e01` | zone cutoffs 0.3 / 0.6 hard-coded; "FREE PARAMETERS USED: 0" and σ = ∞ / 3.5 are fixed strings; zones 2/5/9 | [27](27_third_age_CS_paper.md) §2 | compute, do not print constants |
| VP-3 | F | `e02_gnarl_validator.py`, `e07_observer_fixed_point.py` | Ω_ζΣ is **not** a fixed point of the Gnarl map at α = 3 (roots of y + tan 3y = 0: 0.8185, 1.7443, 2.7348); 0 % converged (e02: DIVERGED; e07: 0/6, 0/50) | [27](27_third_age_CS_paper.md) §3, [48](48_observer_fixed_point.md) §4 | keep as failed; test a map that has Ω_ζΣ as a fixed point or drop the claim |
| VP-4 | D | `e07` | the summary line "All near OMEGA_ZS (Δ<0.1): True [FAIL]" is printed beside a table in which every Δω > 0.5 | [48](48_observer_fixed_point.md) §4 | correct the summary computation |
| VP-5 | F | `e03_hermite_cam.py` | the H₁₆ zeros are not GUE-spaced (normalised variance 0.0203, Wigner–Dyson ratio 1.0203 vs 1.5708); `E_target` is a deterministic function of the zeros | [27](27_third_age_CS_paper.md) §5 | remove the GUE claim from the docstring |
| VP-6 | F | `e04_tia_similarity.py` | TIA 0.4770 (related) vs 0.4769 (distant): no separation | [27](27_third_age_CS_paper.md) §4 | measure is not discriminating |
| VP-7 | F | `e05_nball_transformer.py` | V(16) = 0.2353 ≠ d*_spec 0.2460 (diff 0.0107); the ratio is π/2 only at ℝ→ℂ and ℂ→ℍ | [26](26_TODO_and_roadmap.md) §3, [31](31_cavitation_causality_fermat.md) §4 | recorded |
| VP-8 | F | `e06_two_trees.py` | T/L ratio 0.456 vs π/φ 1.942; T ⟂ L: mean 0.85, max 0.88 (not orthogonal) | [26](26_TODO_and_roadmap.md) §3 | recorded |
| VP-9 | F | `e08_vortex_quantizing_shear.py` | J_cross vs φ-threshold agreement 0.2648; the half-turn e^{π e₁}e₀ = −e₀ passes (this is Euler's identity in ℂ) | [50](50_vortex_quantizing_shear.md) §4 | recorded |
| VP-10 | T | `e09_j2_involution.py` | tests whether **basis products** e_a·e_b are zero (they never are): "0/14 known pairs", "found 0, expected 42" are artefacts. The zero-divisors are the sums e_a ± e_b (84, 42 index pairs, 168 zero-product pairs). The J₂ "automorphism" failure (256/256) is **correct**: the swap e_i ↔ e_{i+8} sends the identity to e₈; the grading (a, b) ↦ (a, −b) is an automorphism (256/256) | [26](26_TODO_and_roadmap.md) §4, [51](51_j2_involution_riemann_fermat.md) §2 | rewrite the zero-divisor test as (e_a ± e_b)(e_c ± e_d) = 0; test the grading as J₂ |
| VP-11 | T/F | `e10_caustic_l_dynamic.py` | the similarity measure is near-constant: random pairs 0.9789 ± 0.0238, synonyms 0.9759, antonyms 0.9856; so 0/5 convergence and 0/5 divergence say nothing about meaning | [52](52_l_dynamic_avoided_collaborator.md) §5 | a measure with discriminating power |
| VP-12 | T | `e11_two_doublings.py` | "pathway count" is n(n−1) (ordered pairs of distinct basis elements), × 4 per doubling, no saturation at two | [54](54_two_doublings_all_pathways.md) §2 | define a quantity that can saturate |
| VP-13 | T | `e12_index_not_value.py` | compares a one-step value shift (0.086) with one large index permutation (0.406); matched controls: random permutation 0.557, random prime values 0.507. Reversing P16 moves the dominant dimensions to the same prime *values* (53, 47) at indices 0, 1 | [55](55_index_not_value.md) §§2–3 | matched-magnitude controls |
| VP-14 | F | `e13_fermat_riemann_firing.py` | specific prompts depart *less* from ordinal order than flat ones (0.4750 vs 0.7583): claim not supported | [26](26_TODO_and_roadmap.md) §3 | recorded |
| VP-15 | F | `e16_penrose_swap.py` | below-GAP perturbation snaps back 100/100; above-GAP changes the order in only 8/100; 5 variant inputs → 5 distinct orders | [26](26_TODO_and_roadmap.md) §3 | recorded |
| VP-16 | X | `monad.py` | the slot layout of the Sedenion Manual ([25](25_sedenion_manual.md) §2) is not implemented; `cam_encode` is the real encoder. β update is a linear clamp (`min(β·mult + GAP, 1.0)`), not a sigmoid; golden walk is `int(count·φ) % n`; `GAP` uses d*_spec = 0.24600 | [47](47_the_two_trees.md) §3, [25](25_sedenion_manual.md) §7 | align the docs or the code |
| VP-17 | D | `monad.py` prime hash | many-to-one: 73,445 dictionary words → 6,436 indices (max 80 per index); index range 1…6543 while the comment says 6542; translation equivalents do not share an index | [15](15_the_monad.md) §3, [16](16_semantic_word_engine.md) §3 | fix the comment; the many-to-one is by design, state it |
| VP-18 | F | PTorrent `peval/sparc_σface.peval` | the registered d* = 0.246 prediction on SPARC failed: 14 hits within 5 % of 175 galaxies (0.08), mean d_ratio 0.2833 vs 0.246; σ-face counts not reproducible (the "buoyancy table" thresholds are not in the file) | [35](35_frame_dragging_bec_vortices.md) §4 | pre-register any redefinition; store the thresholds |

## 3. Other repositories

| ID | Kind | Where | Finding | Documented at | Propagation |
|---|---|---|---|---|---|
| X-1 | E | `RiemannHypothesisProof/.venv` | no `scipy`, so `tests/test_unsmap_chladni_coil.py` fails to collect; with system `python3` the full suite passes (149 passed, 2026-11-13) | this page | add `scipy` to `requirements.txt` |
| X-2 | D | `FourthAgePapers/…/ArdaQuenta/modes/witches_hat.py` | the operator mapping printed on wiki 29 §9 is not found as code; the referenced animation file is missing (`Ainulindale/animations/` does not exist) | [29](29_witches_hat_paper.md) §6 | regenerate the animation; document the mapping |
| X-3 | X | `UniversalSynth/README.md` | left/right hand = Blue/Red assigned by the three-finger rule; the J_red/J_blue record takes J_red as the lower octonion; **the author's source of handedness is the tilt of the real axis against the imaginary axis (swap-twist; two precessions), not the three-finger rule**; open | [133](133_canonical_maths.md) §7.6 | settle by calculation (in progress) |
| X-4 | X | wiki 14 vs wiki 51 (J₂) | Riemann = Red / Fermat = Blue on page 14; the reverse on page 51 | [51](51_j2_involution_riemann_fermat.md) §4 | same handedness resolution |
| X-5 | X | `FourthAgePapers/addenda/addendum_VII` | Wyler/A_π identification contradicts the A_fermat ruling; unverified "85 %" and "seven independent programmes"; withdrawn wording (Euler's identity, Dixon) | [134](134_the_library.md) §5 | correct on reaching FourthAgePapers |
| X-6 | X | `UniversalSynth/README.md` | piano/melancholy observation does not reproduce under the current prime hash (piano → zero 4066, melancholy → 1182) | UniversalSynth README | kept as dated record |
| X-7 | X | `~/.clauderc_citations`, wiki 98 | Cosic, Wyler, Dixon, Furey absent from the library and the bibliography; Leech journal details unconfirmed; Hutsemékers, Taylor–Jagannathan, Tempel–Libeskind, Gott, Peebles, GP-B values from memory | [134](134_the_library.md) §6, [23](23_resonant_recognition.md) §6, [37](37_agn_alignment_bec_vortex.md) §8 | download and title-verify |

## 4. Page-level numbering note (index repass)

Four pages carry duplicate numbers; chronological order from git history (author's rule, 2026-11-13: *succinct, contextual, chronological, these were steps taken in order*):

| Chronological position | File | First committed |
|---|---|---|
| 1 | `50_causality_upper_limit.md` | 2026-06-12 17:01 |
| 2 | `51_dynamic_geodesic.md` | 2026-06-12 17:42 |
| 3 | `52_l_dynamic_avoided_collaborator.md` | 2026-06-12 23:57 |
| 4 | `50_vortex_quantizing_shear.md` | 2026-06-13 00:00 |
| 5 | `51_j2_involution_riemann_fermat.md` | 2026-06-13 00:05 |
| later | `50_bao_mass_gap_engine.md` | 2026-07-31 (a different series: the engine) |

The renumbering follows this order, with the BAO engine page moved to the engine series. The cross-links in pages 40–55 use the present file names and will be updated with the rename.

## 5. Related pages

[26 Roadmap and engine status](26_TODO_and_roadmap.md) · [133 Canonical maths](133_canonical_maths.md) §7 ·
[134 The library](134_the_library.md) · `ContextPlease/claude/scratchpad/2026-11-13_ainulindale_audit/engine_runs/`
