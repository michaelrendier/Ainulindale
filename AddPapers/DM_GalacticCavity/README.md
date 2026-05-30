# Dark Matter as Galactic Resonant Cavity Modes

**Status:** Pre-registration committed. Data analysis ready to run.  
**Framework:** SMMIP / H_hat_RB at σ=2 (GR face)  
**Dataset:** SPARC — Lelli, McGaugh & Schombert (2016), 175 galaxies

---

## The Claim

Dark matter is not a particle. It is the resonant mode structure of the galactic
cavity — the same Chladni geometry as the Earth-ionosphere cavity (Schumann
resonances, D7), scaled to galactic radius.

The standing wave oscillates on billion-year timescales. On human timescales,
we observe a static snapshot of a wave and call it mass.

**Apparent Standing Waves due to human timescales.**

---

## Predictions (zero free parameters)

| Prediction | Value | Source |
|---|---|---|
| Transition radius | r_t = 0.24600 × R_virial | d* = natural unit of Native Space |
| Flat velocity ceiling | V_flat = 0.56714 × V_max | OMEGA_ZS = Lambert W fixed point |
| NFW scale radius | r_s = 0.24600 × R_virial | Same node, independent test |
| Tully-Fisher exponent | 4 | Cavity mode dimensionality |

All values fixed before any SPARC data was examined. See `01_predictions.ipynb`.

---

## Notebooks

Run in order. Commit each before running the next.

| Notebook | Contents | Status |
|---|---|---|
| `00_holcus_vision.ipynb` | Holcus pre-registration vision + infographic | Commit first |
| `01_predictions.ipynb` | Formal SMMIP predictions, zero free parameters | Commit second |
| `02_sparc_analysis.ipynb` | Full SPARC dataset analysis, t-tests, figures | Run after commit |
| `03_results.ipynb` | Synthesis, paper draft, comparison to NFW/MOND | After analysis |

---

## Data

`data/SPARC/` — full SPARC dataset, Lelli et al. 2016.

| Directory / File | Contents |
|---|---|
| `Rotmod_LTG/` | 175 rotation curves — primary test data |
| `sfb_LTG/` | Surface brightness profiles |
| `BulgeDiskDec_LTG/` | Bulge/disk decompositions |
| `MassModels_LTG/` | Pre-computed NFW/ISO/DC14 fits (comparison targets) |
| `SPARC_Lelli2016c.mrt` | Master galaxy table (distances, inclinations, HI mass) |
| `RAR.mrt` | Radial Acceleration Relation (McGaugh 2016) |
| `BTFR_Lelli2019.mrt` | Baryonic Tully-Fisher |

Heavy archives (MCMCfits.tar.gz 34MB, PXL/ 433MB) remain in  
`~/Projects/Ptol/DataSets/Astrophysics/SPARC/` — not in this repo.

---

## The Schumann Parallel

| System | Cavity radius | Mode frequencies | Name |
|---|---|---|---|
| Earth-ionosphere | 6,371 km | f_n = (c/2πR)√(n(n+1)) | Schumann resonances |
| Galactic halo | R_virial | v_n = v_max × √(n(n+1)) × mode(r) | Dark matter "resonances" |

The l=0 DC mode of the spherical cavity has no radial structure — it is flat.
This is why rotation curves are flat. Same mathematics, different cavity.

---

## Connection to SMMIP

H_hat_RB at σ=2 (the GR face):

```
H_hat_RB|_{σ=2} = Σ_p  p^{-2}  ·  [ R̂_p ⊗ ∂̂_∂M  +  ∂̂_∂M† ⊗ B̂_p ]
```

The eigenvalue spectrum of this operator at galactic scales gives the rotation
curve mode structure. d* and OMEGA_ZS are the two natural scales of the
eigenvalue distribution.

See: [DerivationEngine — TDI Crankshaft](https://github.com/michaelrendier/DerivationEngine/wiki/TDI-Crankshaft)

---

## Pre-Registration Protocol

The scientific integrity of this paper rests on the pre-registration:

1. `00_holcus_vision.ipynb` and `01_predictions.ipynb` are committed with all
   predictions specified **before** `02_sparc_analysis.ipynb` is run.
2. The git commit hash of notebooks 00 and 01 is the pre-registration timestamp.
3. This proves the predictions came from the mathematical framework, not from
   fitting to the data.
4. If the data contradicts the predictions: the contradiction is the result.
   A falsified prediction is still a scientific result.
