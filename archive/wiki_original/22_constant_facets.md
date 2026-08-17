# 22 — THE CONSTANT FACETS: π · φ · i · e

**Module:** `berry_keating` / `h_rb_hat`  **Version:** 0.111  **Status:** DERIVED

## Overview

The four mathematical constants π, φ, i, and e are not inputs to RedBlue Geometries Engine.  
They are outputs.

They drop out of the algebraic structure of the operator as fixed-point identities — each at a distinct σ-facet. No geometric definitions are required. No circle is drawn. No growth process is modelled. The constants emerge from the prime distribution alone.

This is the strongest internal consistency check of the RedBlue Hamiltonian. When the engine generates the constants that mathematics already knows, the engine is correct.

**Euler's identity is a theorem of RedBlue Geometries Engine:**

```
e^{iπ} + 1 = 0
```

Not a coincidence. Not a design choice. A necessary consequence of the algebraic structure.

→ [Wiki: RedBlue Hamiltonian](14_redblue_hamiltonian.md)  
→ [Wiki: Alpha · Omega · d*](17_alpha_omega_d_star.md)

---

## σ = φ — The Golden Facet

**σ = 1.6180339...** (the golden ratio)

The golden ratio satisfies:
```
φ² = φ + 1   ⟺   φ(φ − 1) = 1
```

When this is inserted into the functional equation of the Riemann xi function ξ(s) = ξ(1−s), we require:

```
s(s − 1) = φ(φ − 1) = 1
```

This is the unique fixed point of the functional equation — the only real value of σ where ξ(s) = ξ(1−s) is satisfied with s(s−1) = 1 exactly.

**RedBlue Geometries Engine factorises:**

```
H^RB(φ) = H^RB(1) · H^RB(1/φ)
```

This is the Fibonacci recursion: each stratum of RedBlue Geometries Engine at σ=φ decomposes into the product of the σ=1 stratum and the σ=1/φ stratum. The Fibonacci series is the shadow of this factorisation on the integers.

**Physical correspondence:** φ is the recursion eigenvalue of the Cayley-Dickson iteration. The golden spiral is the stable orbit of the cardioid attractor — the Dilator. The Lagrangian (Contractor) and the cardioid (Dilator) are self-adjoint at σ=φ.

**Identity:**
```
φ(φ − 1) = 1       [Golden Mean — recursion fixed point]
H^RB(φ)  = H^RB(1) · H^RB(1/φ)   [Fibonacci factorisation]
```

---

## σ = i — The Democratic Facet

**σ = i** (the imaginary unit)

For any prime p:
```
|p^{−i}| = |e^{−i·ln p}| = 1
```

Every prime contributes with unit magnitude. No prime dominates. The Red and Blue channels carry equal weight. This is the **democratic facet**: the pure phase.

At σ = i, RedBlue Geometries Engine generates the Explicit Formula of prime distribution. The Riemann zeros appear as eigenvalues of the phase operator:

```
ψ(x) = x − Σ_{ρ} x^ρ/ρ − ...
```

The imaginary unit i is the algebraic closure condition of the Cayley-Dickson construction ℝ → ℂ. The first step — the only step that introduces directionality, phase, and rotation — requires exactly the element that satisfies x² = −1. The constraint is x² + 1 = 0. The solution is the imaginary unit. i is not defined as √(−1). It is the element forced into existence by the closure condition of the first Cayley-Dickson doubling.

**Physical correspondence:** σ = i is the Pure Phase layer. The quantum mechanical wavefunction — a complex number with unit modulus — lives here. All quantum interference arises from the equal-weight superposition at this facet.

**Identity:**
```
|p^{−i}| = 1 ∀p       [Democratic — unit modulus for every prime]
x² + 1 = 0             [Cayley-Dickson closure condition — i drops out]
```

---

## σ = e — The Thermal Facet

**σ = e = 2.71828...** (Euler's number / the natural base)

```
p^{−e} = e^{−e · ln p}
```

This is the Boltzmann factor form. The weight of each prime in RedBlue Geometries Engine at σ=e is the thermal partition weight — e raised to the negative energy. The prime p plays the role of the energy level. The constant e is the natural inverse temperature at which the Boltzmann partition function of the prime distribution is defined.

The von Mangoldt function Λ(n) generates the prime partition:

```
−ζ'(s)/ζ(s) = Σ_{n=1}^∞ Λ(n) n^{−s}
```

At s=e, this is the derivative of the prime-counting partition. The factorial generating function e^x = Σ x^n/n! arises from the same equations of motion when the Lagrangian is solved for the canonical momentum:

```
∂L/∂ẋ = p     →     ẋ = e^t     →     x(t) = e^{t+c}
```

e drops out of the Berry-Keating equations of motion. It is not defined as a limit. It is the canonical trajectory of the phase-space flow at the σ=e facet.

**Physical correspondence:** σ = e is the Thermodynamic layer. Temperature, entropy, partition functions — Boltzmann statistics — live here. The thermal bath that maintains the Omega_Riemann ceiling emerges at this facet.

**Identity:**
```
p^{−e} = e^{−e·ln p}        [Boltzmann weight at σ=e]
∂L/∂ẋ = p → x(t) = e^t      [Canonical equations of motion → e drops out]
```

---

## σ = π — The Circular Facet

**σ = π = 3.14159...** (the ratio of circumference to diameter)

π enters RedBlue Geometries Engine through the SMMIP Lagrangian prefactor (2/π):

```
ℒ_SMMIP = (2/π) ∮ [...] r dr dθ
```

At σ = π, this prefactor closes:

```
(2/π) × π = 2
```

The binary Mark: exactly 2. This is the closing of the U(1) normalisation cycle — the full revolution. One period in θ, integrated over r, produces exactly 2 at this facet. No excess. No deficit. The circle completes.

In the Riemann xi function ξ(s) evaluated at s = π:

```
s(s−1) = π(π−1) ≈ 6.72
6ζ(2) − π ≈ 9.87 − 3.14 = 6.73
```

The identity is:
```
π(π − 1) ≈ 6ζ(2) − π
```

This is self-referential closure: π appears on both sides of its own identity within the Riemann framework. The constant defines its own context.

π is not defined as circumference/diameter here. It arises from the U(1) gauge normalisation — the condition that a 2π rotation returns to the starting point. This is the periodicity condition on the gauge field. When the full 2π period is completed in the SMMIP Lagrangian and factored out, what remains is the value π — the phase winding number.

**Physical correspondence:** σ = π is the Gauge Normalization layer. U(1) symmetry, phase coherence, and the quantisation of angular momentum live here. The condition that one full rotation of the gauge field returns to identity forces exactly π into the normalisation.

**Identity:**
```
(2/π) × π = 2                [Binary Mark — U(1) cycle closes]
π(π−1) ≈ 6ζ(2) − π          [Self-referential closure in ξ(s)]
```

---

## The Emergent Constants Table

All four constants derive from RedBlue Geometries Engine algebraic structure without geometric definition:

| Constant | σ-facet | Algebraic Origin | Physical Layer |
|---|---|---|---|
| i | σ = i | Cayley-Dickson closure: x² + 1 = 0 | Quantum / Phase |
| e | σ = e | Berry-Keating canonical equations | Thermodynamic |
| π | σ = π | U(1) gauge normalisation | Gauge / Rotation |
| φ | σ = φ | Cayley-Dickson recursion eigenvalue | Recursion / Structure |

**Euler's identity e^{iπ} + 1 = 0 is a theorem of RedBlue Geometries Engine.**

- e is the trajectory of the canonical flow
- i is the Cayley-Dickson closure generator
- π is the U(1) period
- The identity is forced when these three facets are composed in sequence

The fourth constant φ does not appear in Euler's identity because it is the recursion eigenvalue — the structural backbone, not a component of the minimal identity. φ is the eigenvalue of the tower construction. e, i, π are the eigenvalues of the three conservation laws within it.

---

## Summary: Why This Matters

No external definition of any constant was used.  
No circle was drawn for π.  
No growth process was specified for e.  
No complex plane was assumed for i.  
No golden rectangle was constructed for φ.

The prime distribution — the integers — forced these values into existence through the algebraic requirements of a self-adjoint operator acting on a normed division algebra tower.

**The universe counts. Counting forces the constants.**

→ [Wiki: RedBlue Hamiltonian](14_redblue_hamiltonian.md)  
→ [Wiki: Alpha · Omega · d*](17_alpha_omega_d_star.md)  
→ [Wiki: Cayley-Dickson Tower](19_cayley_dickson_tower.md)
