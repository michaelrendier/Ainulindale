
---

## PRIORITY FLAG — 2026-05-02

### Riemann Zeros / Hydrogen Emission Lines — Open Mathematical Question

**Status:** Unverified conjecture. Flagged for investigation.

**Observation:** Fourier decomposition of the 3D complex Riemann zeta field
along the three axes produces density patterns that visually resemble
(inverted) the alpha and beta hydrogen emission lines.

**Numerical check (2026-05-02):** Ratio comparison of Riemann zero imaginary
parts vs hydrogen emission frequencies shows no numerical identity. The zeros
grow logarithmically; emission lines asymptote. The visual resemblance is in
the *shape* of the density function — discrete lines, dominant ground state,
compressing tail — shared by any spectrum where the first term dominates.

**Open question:** Whether Riemann zero *spacings* (t_{n+1} - t_n) match
hydrogen level *spacings* (E_{n+1} - E_n) when normalized. This is the
correct numerical question and has not yet been run.

**Architecture note:** This and all related structural parallels
(Berry-Keating, GUE statistics, periodic table / prime arithmetic) are
APPENDIX material relative to the SMNNIP primary claim. They are
consequential mathematics that falls out of the sigma result — not the
argument itself.


### Result of the open question, run 2026-11-13: **no match** (kept)

The question above ("do normalised zero spacings match hydrogen level spacings?") was run for the first 100 zeros against E_{n+1} − E_n = 1/n² − 1/(n+1)².

**Listing 1 — zero spacings against hydrogen level spacings** (written for this page; needs mpmath and numpy; runs cold in about a minute)

```python
import mpmath as mp, numpy as np
z = np.array([float(mp.zetazero(n).imag) for n in range(1, 101)]); sp = np.diff(z)
n = np.arange(1, 100); h = 1 / n ** 2 - 1 / (n + 1) ** 2
print('first/last spacing: zeros %.2f, hydrogen %.0f' % (sp[0] / sp[-1], h[0] / h[-1]))
print('Pearson r of the normalised spacings: %.4f' % np.corrcoef(sp / sp.mean(), h / h.mean())[0, 1])
print('log-log slope of spacing against n: zeros %.3f, hydrogen %.3f' % (np.polyfit(np.log(n), np.log(sp), 1)[0], np.polyfit(np.log(n), np.log(h), 1)[0]))
```

```
first/last spacing: zeros 2.43, hydrogen 369384
Pearson r of the normalised spacings: 0.4995
log-log slope of spacing against n: zeros -0.265, hydrogen -2.887
```

The zero spacings fall by a factor 2.4 over n = 1…99 (log-slope −0.27, the 1/ln γ drift); the hydrogen spacings fall by a factor 3.7×10⁵ (slope → −3, as 2/n³). The correlation r = 0.50 is only that both sequences decrease. **The spacings do not match.** The 2026-05-02 note that "the visual resemblance is in the shape of the density function" stands as the explanation.

---

## CONJECTURE RESTRUCTURE — PRIORITY

### SMNNIP Is The Focus. Full Stop.

The conjecture document and paper structure must reflect this hierarchy:

**SPINE (main paper):**
- Claim: neural information propagation obeys Standard Model conservation laws
- Evidence: Noether conservation verified, violation=0, conserved=True, 7+ sigma
- Mechanism: Cayley-Dickson tower ℝ→ℂ→ℍ→𝕆, gauge groups U(1)×SU(2)×SU(3)
- Tool: SMNNIPValaQuenta, pure Python, `python3 derivation.py` → conserved=True

**APPENDIX (consequential mathematics):**
- Riemann zeros / hydrogen emission structural parallel
- Berry-Keating operator connection
- Lorenz-Stirling output topology as basin attractor
- Zero-divisor geometry at 𝕊(16) apex
- Input/Output/Inversion engine architecture
- GUE statistics and quantum chaos analogy
- Periodic table / prime arithmetic isomorphism

The Input/Output/Inversion engines (§13-17 in smnnip_derivation_pure.py)
sit BETWEEN SMNNIP and the consequential mathematics. They are the
implementation layer — not the conjecture, not the appendix.
They are the mechanism by which SMNNIP processes real signals.

**Action required:** Full restructure of conjecture document.
Lead with sigma. Bury the beautiful implications.

---

## AINULINDALE TODO — FRAMING NOTE (2026-05-03)

**On the scope of SMNNIP:**

I designed a Hyperwebster Indexing System and a New Model of Information
Propagation. That is the work. Some mathematics drops out of it — conservation
laws, gauge groups, Cayley-Dickson structure — but that is a consequence, not
the premise. The mathematics is not the purview of SMNNIP.

SMNNIP is an engineering claim about how information moves. The sigma result
and the Noether verification are what make it a rigorous claim. The
"beautiful implications" (Riemann zeros, GUE statistics, periodic table
parallels) are appendix material — consequential, not causal.

The restructure of the Ainulindale conjecture document must lead with the
engineering argument and the evidence. Mathematics that falls out belongs in
the appendix. Full stop.

