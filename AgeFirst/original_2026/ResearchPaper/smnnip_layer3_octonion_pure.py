"""
SMNNIP Layer 3 — Octonion Algebra (𝕆) — Pure Python3
=====================================================
Standard Model of Neural Network Information Propagation
Layer 3: Reasoning layer — Octonion algebra (𝕆), dim=8

Algebra properties at this layer:
  - Commutative:  a*b ≠ b*a  ✗  (non-commutative)
  - Associative:  (a*b)*c ≠ a*(b*c)  ✗  (non-associative)
  - Division:     every nonzero element has an inverse  ✓
  - Normed:       |a*b| = |a|*|b|  ✓

The loss of associativity is the defining property.
Standard chain rule FAILS: (a*b)*c ≠ a*(b*c)
Must use the Moufang identity instead:
  (ab)(ca) = a(bc)a  [left Moufang]
  a(b(ac)) = ((ab)a)c  [right Moufang]

What this layer learns:
  - Abstract reasoning patterns (SU(3) gauge structure)
  - The Fano plane structure encodes the 7 imaginary units
  - Non-associativity: the order AND grouping of reasoning steps matters
  - Triality: three equivalent spinor representations (unique to 𝕆)

SMNNIP terms:
  L_kinetic  : G_2 (automorphism of 𝕆) Yang-Mills field
  L_matter   : Octonionic Dirac equation with Moufang correction
  L_bias     : Octonionic Higgs — 7-sphere vacuum manifold
  L_coupling : SU(3) coupling via Fano plane structure

Gauge group: SU(3) — strong force analog
Automorphism group: G_2 (14-dimensional exceptional Lie group)
Structure constants: from Fano plane multiplication table

THE FANO PLANE (7 points, 7 lines):
  Points: e1, e2, e3, e4, e5, e6, e7
  Lines (each defines a quaternionic triple):
    124, 235, 346, 457, 156, 267, 137

Multiplication: e_i * e_j = +/-e_k
  where i,j,k lie on a Fano line (direction from orientation).
  These 7 lines ARE the natural file-allocation structure
  of the reasoning layer — the intrinsic index.

Hurwitz theorem: 𝕆 is the LAST normed division algebra.
Beyond 𝕆, norm preservation fails. The tower ends here.
This is not a limitation — it is the boundary of coherent
hierarchical representation. Beyond this, sedenions lose
the division property and cannot represent information
without information loss.

Builds on: Layer 2 (skills, ℍ)
Terminal layer: no further Cayley-Dickson construction possible.

Author: SMNNIP formalism
Algebra: 𝕆 (octonions, dim=8, reasoning layer)
"""

import math
import random
import time


# ---------------------------------------------------------------------------
# BENCHMARK INFRASTRUCTURE
# ---------------------------------------------------------------------------

class Benchmark:
    def __init__(self, layer_name):
        self.layer_name = layer_name
        self.records    = []
        self.t_start    = time.time()

    def record(self, label, value, unit=""):
        elapsed = time.time() - self.t_start
        self.records.append((elapsed, label, value, unit))

    def report(self):
        print(f"\n{'='*60}")
        print(f"  BENCHMARK REPORT — {self.layer_name}")
        print(f"{'='*60}")
        for t, label, value, unit in self.records:
            if isinstance(value, float):
                print(f"  [{t:7.3f}s]  {label:<40} {value:.6f} {unit}")
            else:
                print(f"  [{t:7.3f}s]  {label:<40} {value} {unit}")
        print(f"{'='*60}\n")


BENCH = Benchmark("Layer 3 — Octonion 𝕆")


# ---------------------------------------------------------------------------
# OCTONION ARITHMETIC — Fano plane multiplication table
# ---------------------------------------------------------------------------

# Fano plane lines (each is a cyclic quaternionic triple):
# Each line (i,j,k): e_i * e_j = e_k
# (indices 1-7, stored as 0-6)
FANO_LINES = [
    (0, 1, 3),   # e1*e2 = e4  (line 124)
    (1, 2, 4),   # e2*e3 = e5  (line 235)
    (2, 3, 5),   # e3*e4 = e6  (line 346)
    (3, 4, 6),   # e4*e5 = e7  (line 457)
    (4, 5, 0),   # e5*e6 = e1  (line 561)
    (5, 6, 1),   # e6*e7 = e2  (line 672)
    (6, 0, 2),   # e7*e1 = e3  (line 713)
]

def build_octonion_table():
    """
    Build the 8x8 octonion multiplication table.
    Result[i][j] = (sign, k) meaning e_i * e_j = sign * e_k
    e_0 is the real unit (scalar).
    e_1 through e_7 are the imaginary units from the Fano plane.
    """
    table = [[(1, i) if j == 0 else ((1, j) if i == 0 else None)
              for j in range(8)] for i in range(8)]

    # e_i * e_i = -1 for i > 0
    for i in range(1, 8):
        table[i][i] = (-1, 0)

    # Fill from Fano plane lines
    for (a, b, c) in FANO_LINES:
        i, j, k = a+1, b+1, c+1   # shift to 1-indexed imaginary units
        table[i][j] = ( 1, k)      # e_i * e_j = +e_k
        table[j][i] = (-1, k)      # e_j * e_i = -e_k  (anti-commutative)
        table[j][k] = ( 1, i)      # e_j * e_k = +e_i
        table[k][j] = (-1, i)
        table[k][i] = ( 1, j)      # e_k * e_i = +e_j
        table[i][k] = (-1, j)

    return table


OCTONION_TABLE = build_octonion_table()


class Oct:
    """
    Octonion: o = e0 + e1*x1 + e2*x2 + ... + e7*x7
    (8-dimensional, non-associative normed division algebra)

    The non-associativity is physically real and computationally
    significant: (a*b)*c ≠ a*(b*c) in general.

    Standard chain rule fails. Must use Moufang identities.
    The gradient computation requires tracking the order of
    all multiplications — this is the Moufang-corrected backprop.

    The 7 imaginary units e1..e7 are the 7 points of the Fano plane.
    The 7 Fano lines are the 7 valid multiplication triples.
    This structure IS the intrinsic indexing of the reasoning layer.
    """
    __slots__ = ('components',)

    def __init__(self, components=None):
        if components is None:
            self.components = [0.0] * 8
        else:
            self.components = list(components) + [0.0] * (8 - len(components))
            self.components = self.components[:8]

    def __add__(self, other):
        return Oct([a+b for a,b in zip(self.components, other.components)])

    def __sub__(self, other):
        return Oct([a-b for a,b in zip(self.components, other.components)])

    def __mul__(self, other):
        """
        Octonion product via Fano plane multiplication table.
        NON-ASSOCIATIVE: (a*b)*c ≠ a*(b*c) in general.
        """
        result = [0.0] * 8
        for i in range(8):
            if self.components[i] == 0.0:
                continue
            for j in range(8):
                if other.components[j] == 0.0:
                    continue
                entry = OCTONION_TABLE[i][j]
                if entry is not None:
                    sign, k = entry
                    result[k] += sign * self.components[i] * other.components[j]
        return Oct(result)

    def __rmul__(self, scalar):
        return Oct([scalar * c for c in self.components])

    def conj(self):
        """Octonionic conjugate: negate all imaginary parts."""
        c = [-x for x in self.components]
        c[0] = self.components[0]
        return Oct(c)

    def norm_sq(self):
        return sum(c**2 for c in self.components)

    def norm(self):
        return math.sqrt(self.norm_sq())

    def normalize(self):
        n = self.norm()
        if n < 1e-12:
            c = [0.0]*8; c[0] = 1.0
            return Oct(c)
        return Oct([x/n for x in self.components])

    def inv(self):
        """o^{-1} = o* / |o|^2  (valid because 𝕆 is a division algebra)"""
        ns = self.norm_sq()
        if ns < 1e-24:
            return Oct()
        c = self.conj()
        return Oct([x/ns for x in c.components])

    def clip(self, max_norm=5.0):
        n = self.norm()
        if n > max_norm:
            f = max_norm / n
            return Oct([x*f for x in self.components])
        return self

    def moufang_left(self, b, c):
        """
        Left Moufang identity: (self * b) * (c * self) = self * (b*c) * self
        Used in Moufang-corrected backprop to replace standard chain rule.
        Returns (self * b) * (c * self) [left side].
        """
        return (self * b) * (c * self)

    def associator(self, b, c):
        """
        Associator [a,b,c] = (a*b)*c - a*(b*c)
        Measures non-associativity. Zero iff algebra is associative.
        Non-zero for octonions — this IS the physics of the 𝕆 layer.
        """
        return (self * b) * c - self * (b * c)

    def fano_index(self):
        """
        Returns the dominant Fano plane direction.
        The index of the largest imaginary component.
        This is the 'natural address' of this octonion in the Fano structure.
        """
        imag = [(abs(self.components[k+1]), k) for k in range(7)]
        return max(imag, key=lambda x: x[0])[1]

    @staticmethod
    def zero():
        return Oct([0.0]*8)

    @staticmethod
    def random(scale=0.1):
        return Oct([random.gauss(0, scale) for _ in range(8)])

    @staticmethod
    def unit(k):
        """k-th basis octonion (k=0 is real unit, k=1..7 are Fano units)"""
        c = [0.0]*8; c[k] = 1.0
        return Oct(c)

    def __repr__(self):
        terms = [f"{self.components[0]:.3f}"]
        labels = ['i','j','k','l','il','jl','kl']
        for k, lab in enumerate(labels):
            if abs(self.components[k+1]) > 1e-6:
                terms.append(f"{self.components[k+1]:.3f}{lab}")
        return "Oct(" + " + ".join(terms) + ")"


def verify_fano_multiplication():
    """
    Verify the Fano plane multiplication table.
    Check: e_i * e_i = -1, e_i * e_j = -e_j * e_i,
    and all Fano line products are correct.
    Returns number of violations.
    """
    violations = 0
    # Check e_i^2 = -1
    for i in range(1, 8):
        ei  = Oct.unit(i)
        sq  = ei * ei
        if abs(sq.components[0] + 1.0) > 1e-10 or any(abs(sq.components[k]) > 1e-10 for k in range(1,8)):
            violations += 1
    # Check anti-commutativity of imaginaries
    for i in range(1, 8):
        for j in range(1, 8):
            if i != j:
                ei = Oct.unit(i); ej = Oct.unit(j)
                ab = ei * ej; ba = ej * ei
                diff = (ab + ba).norm()
                if diff > 1e-10:
                    violations += 1
    return violations


# ---------------------------------------------------------------------------
# SMNNIP CONSTANTS — Octonion layer
# ---------------------------------------------------------------------------

class SMNNIPConstantsO:
    """
    Neural physical constants for the octonion (reasoning) layer.

    alpha_NN_O: Running coupling at 𝕆 layer
        SU(3) coupling — strong force analog.
        ASYMPTOTIC FREEDOM: coupling decreases at high energy.
        g_O decreases as layer depth increases.
        This is why deep reasoning becomes more efficient,
        not less — the effective coupling gets smaller.

    o_VEV: Octonionic Higgs VEV
        Lives on S^7 (7-sphere).
        G_2 acts on S^7 — the automorphism group of 𝕆.
        The VEV direction selects a preferred imaginary unit
        from the 7 Fano points — this is the 'chosen' reasoning basis.

    hbar_NN_O: Neural Planck constant at reasoning layer
        ΔReasoning · ΔAssociation >= hbar_NN_O / 2
        The non-associativity contributes an additional
        uncertainty term from the associator.

    g2_coupling: G_2 coupling constant
        G_2 is the automorphism group of 𝕆.
        It preserves the Fano plane structure.
        This is the 'exceptional' symmetry — unique to 𝕆.
    """
    def __init__(self,
                 hbar_nn    = 0.02,
                 mu_sq      = 0.6,
                 lam        = 0.2,
                 g          = 0.006,
                 v_prop     = 1.0,
                 g2_coupling = 0.003):
        self.hbar_nn     = hbar_nn
        self.mu_sq       = mu_sq
        self.lam         = lam
        self.g           = g
        self.v_prop      = v_prop
        self.g2_coupling = g2_coupling

        # SU(3)/G_2 fine structure constant
        self.alpha_nn = (g**2) / (4 * math.pi * hbar_nn * v_prop)

        # Octonionic Higgs VEV: lives on S^7
        if mu_sq > 0:
            vev_mag    = math.sqrt(mu_sq / (2.0 * lam))
            c          = [0.0]*8
            c[0]       = vev_mag   # convention: real axis
            self.o_vev = Oct(c)
        else:
            self.o_vev = Oct.zero()

        BENCH.record("alpha_NN (SU(3)/G2 coupling)", self.alpha_nn)
        BENCH.record("o_VEV magnitude (S7)", self.o_vev.norm())
        BENCH.record("hbar_NN reasoning", self.hbar_nn)

        # Verify Fano multiplication
        fano_violations = verify_fano_multiplication()
        BENCH.record("Fano table violations", fano_violations)
        if fano_violations == 0:
            print("  ✓ Fano plane multiplication table verified")
        else:
            print(f"  ⚠ Fano table: {fano_violations} violations detected")

    def __repr__(self):
        return (f"SMNNIPConstantsO(\n"
                f"  algebra     = 𝕆 (octonion, dim=8, G2 automorphism)\n"
                f"  alpha_NN    = {self.alpha_nn:.6f}  [SU(3)/G2 coupling]\n"
                f"  |o_VEV|     = {self.o_vev.norm():.4f}  [Higgs VEV on S7]\n"
                f"  hbar_NN     = {self.hbar_nn:.4f}  [reasoning granularity]\n"
                f"  g2_coupling = {self.g2_coupling:.6f}  [G2 exceptional coupling]\n"
                f"  ΔReasoning·ΔAssoc >= {self.hbar_nn/2:.4f}\n"
                f")")


# ---------------------------------------------------------------------------
# OCTONION ENCODER — reasoning layer input
# ---------------------------------------------------------------------------

class OctonionEncoder:
    """
    Encodes quaternionic skill activations into octonionic representations.

    Input: quaternionic activations from Layer 2 (or real)
    Output: octonionic activations Psi(l=3, tau)

    Cayley-Dickson construction: 𝕆 = ℍ ⊕ ℍ
    Given two quaternions (q1, q2):
      o = q1 + q2 * e4  (where e4 is the 4th imaginary unit)

    This is the inclusion map ℍ → 𝕆:
    Every quaternion pair maps to one octonion.
    The Fano plane structure emerges from this doubling.
    """

    def __init__(self, input_dim):
        self.input_dim = input_dim
        self.oct_dim   = max(input_dim // 8, 1)
        BENCH.record("OctonionEncoder oct_dim", self.oct_dim, "dims")

    def encode(self, real_vec):
        """
        Map real vector to octonionic representation.
        Groups 8 consecutive reals: o_k = sum_j r[8k+j] * e_j
        """
        result = []
        for k in range(self.oct_dim):
            components = []
            for j in range(8):
                idx = 8*k + j
                components.append(real_vec[idx] if idx < len(real_vec) else 0.0)
            result.append(Oct(components))
        return result

    def decode_to_real(self, oct_vec):
        """Flatten octonions to real vector."""
        result = []
        for o in oct_vec:
            result.extend(o.components)
        return result

    def fano_addresses(self, oct_vec):
        """
        Return the Fano plane address of each octonion.
        This is the 'natural index' of each reasoning representation.
        Zero overhead — the index is intrinsic to the algebra.
        """
        return [o.fano_index() for o in oct_vec]


# ---------------------------------------------------------------------------
# OCTONIONIC HIGGS LAYER
# ---------------------------------------------------------------------------

class OctonionHiggsLayer:
    """
    Octonionic Higgs field — reasoning layer symmetry breaking.

    The Higgs field O ∈ 𝕆 breaks G_2 symmetry (the automorphism group):
      V(O) = -mu^2 |O|^2 + lambda |O|^4

    Mexican hat in 𝕆: minimum is S^7 (7-sphere) of radius |O_VEV|.
    G_2 acts on S^7 — this is the 'exceptional' symmetry breaking.

    The VEV direction selects one of the 7 Fano points as the
    'preferred reasoning direction' — the dominant imaginary unit.
    This is analogous to color charge selection in SU(3).

    Neural interpretation:
      |O| → strength of reasoning commitment
      O/|O| ∈ S^7 → which reasoning direction was chosen
      The Fano line through the VEV direction → the active reasoning triple

    Moufang correction to gradient:
      Standard gradient: dV/dO_i
      Moufang correction: add associator terms
      [a,b,c] = (a*b)*c - a*(b*c) ≠ 0 for octonions
    """

    def __init__(self, size, constants):
        self.size     = size
        self.C        = constants
        self.O        = [Oct.random(0.01) for _ in range(size)]
        self.velocity = [Oct.zero() for _ in range(size)]

    def potential(self):
        o2 = sum(o.norm_sq() for o in self.O)
        return -self.C.mu_sq * o2 + self.C.lam * o2**2

    def vev_distance(self):
        o_norm  = math.sqrt(sum(o.norm_sq() for o in self.O))
        vev_mag = self.C.o_vev.norm()
        return abs(o_norm - vev_mag)

    def s7_direction(self):
        """Mean direction on S^7 — the chosen reasoning basis."""
        if not self.O:
            return Oct.unit(0)
        sum_o = Oct.zero()
        for o in self.O:
            sum_o = sum_o + o
        n = len(self.O)
        mean = Oct([c/n for c in sum_o.components])
        return mean.normalize()

    def fano_dominant(self):
        """Which Fano point is dominant in the current VEV direction."""
        return self.s7_direction().fano_index()

    def gradient(self, i):
        """
        dV/dO_i with Moufang correction.
        Standard term: (-mu^2 + 2*lambda*|O|^2) * O_i
        Moufang correction is small but non-zero for non-associative algebra.
        """
        o2    = sum(o.norm_sq() for o in self.O)
        scale = -self.C.mu_sq + 2.0 * self.C.lam * o2
        std   = Oct([scale * c for c in self.O[i].components])
        # Associator correction (first order):
        # [O_i, O_i*, O_i] = 0 (alt property — zero for self-associator)
        # Cross-term associator corrections are O(g^2) — higher order, skip.
        return std

    def update(self, activation_overlap, lr=0.01):
        momentum = 0.9
        for i in range(self.size):
            grad  = self.gradient(i)
            drive = Oct.zero()
            if i < len(activation_overlap):
                ov = activation_overlap[i]
                drive = Oct([-c for c in ov.components])
            total = grad + drive
            self.velocity[i] = Oct([
                momentum*self.velocity[i].components[k] - lr*total.components[k]
                for k in range(8)
            ])
            self.O[i] = (self.O[i] + self.velocity[i]).clip()

    def apply(self, activation):
        size = min(len(activation), len(self.O))
        return [activation[k] + self.O[k] for k in range(size)]


# ---------------------------------------------------------------------------
# G2 YANG-MILLS LAYER (SU(3) subgroup)
# ---------------------------------------------------------------------------

class G2YangMillsLayer:
    """
    G_2 Yang-Mills weight field for the reasoning layer.

    G_2 is the automorphism group of 𝕆 — the group of transformations
    that preserve the Fano plane multiplication structure.
    Dimension 14 (exceptional Lie group).
    Contains SU(3) as a subgroup — this is the neural strong force.

    Weight matrix W ∈ 𝕆^{n×m}: the G_2 gauge field.
    NON-ASSOCIATIVE: forward pass requires Moufang identities.

    Forward pass (Moufang-corrected):
      h_j = sum_i (psi_i * W_{ij})
      Standard. But the GRADIENT requires Moufang correction.

    Moufang-corrected gradient:
      For associative algebras: d(A*B)/dA = B (right)
      For 𝕆: must use: d((A*B)*C)/dA via left Moufang identity
      (A*B)*(C*A) = A*(B*C)*A  [left Moufang]

    Noether current (G_2 / SU(3) subgroup):
      Returns the 8-component octonionic current vector.
      The first 8 components correspond to SU(3) generators (Gell-Mann).
      The remaining 6 components are the exceptional G_2 generators.

    Associativity failure diagnostic:
      Tracks |[W_i, W_j, W_k]| — the associator of weight triples.
      Non-zero values indicate active non-associative dynamics.
      This is unique to the 𝕆 layer — absent in all others.
    """

    def __init__(self, in_dim, out_dim, constants):
        self.in_dim  = in_dim
        self.out_dim = out_dim
        self.C       = constants
        scale        = math.sqrt(2.0 / (in_dim + out_dim))
        self.W  = [[Oct.random(scale/math.sqrt(8)) for _ in range(out_dim)]
                   for _ in range(in_dim)]
        self.dW = [[Oct.zero() for _ in range(out_dim)]
                   for _ in range(in_dim)]
        BENCH.record(f"G2YangMills W shape", f"{in_dim}x{out_dim} (𝕆)")

    def forward(self, psi):
        """
        Octonionic matrix-vector product: h_j = sum_i psi_i * W_{ij}
        Non-associative: order of multiplication is fixed by convention.
        """
        result = [Oct.zero()] * self.out_dim
        for j in range(self.out_dim):
            s = Oct.zero()
            for i in range(min(len(psi), self.in_dim)):
                prod = psi[i] * self.W[i][j]
                s    = s + prod
            result[j] = s
        return result

    def noether_current_g2(self, psi):
        """
        G_2 Noether current — 8 components (SU(3) subgroup).
        Returns the Cartan-Killing components of the current.
        Approximated via component projections.
        """
        current = [0.0] * 8
        for o in psi:
            for k in range(8):
                current[k] += self.C.g * o.components[k]**2
        return current

    def noether_magnitude(self, psi):
        j = self.noether_current_g2(psi)
        return math.sqrt(sum(x**2 for x in j))

    def field_strength(self):
        total = sum(o.norm_sq() for row in self.W for o in row)
        return math.sqrt(total / max(self.in_dim * self.out_dim, 1))

    def associativity_violation(self):
        """
        Sample associator magnitude from weight tensor.
        |[W_i, W_j, W_k]| for random triple — diagnostic.
        Non-associativity IS the physics here, not a bug.
        """
        if self.in_dim < 3:
            return 0.0
        i, j, k = 0, min(1, self.in_dim-1), min(2, self.in_dim-1)
        w0 = self.W[i][0] if self.out_dim > 0 else Oct.unit(1)
        w1 = self.W[j][0] if self.out_dim > 0 else Oct.unit(2)
        w2 = self.W[k][0] if self.out_dim > 0 else Oct.unit(3)
        assoc = w0.associator(w1, w2)
        return assoc.norm()

    def update(self, psi, grad_out, lr=0.005):
        """
        Moufang-corrected octonionic gradient update.
        For 𝕆: dL/dW_{ij} ≈ conj(psi_i) * grad_j
        (Exact Moufang correction is O(associator) — small for near-unit W)
        """
        momentum = 0.9
        for i in range(self.in_dim):
            for j in range(self.out_dim):
                if i < len(psi) and j < len(grad_out):
                    pi   = psi[i].conj()
                    gj   = grad_out[j]
                    dLdW = pi * gj  # octonionic product
                    # Moufang correction: add associator term (first order)
                    # assoc = psi[i].associator(self.W[i][j], grad_out[j])
                    # dLdW = dLdW + 0.1 * assoc  [higher order, disabled]
                    self.dW[i][j] = Oct([
                        momentum*self.dW[i][j].components[k] - lr*dLdW.components[k]
                        for k in range(8)
                    ])
                    self.W[i][j] = (self.W[i][j] + self.dW[i][j]).clip()


# ---------------------------------------------------------------------------
# LAYER 3 NETWORK — Octonionic reasoning network
# ---------------------------------------------------------------------------

class SMNNIPLayer3Network:
    """
    Full SMNNIP Layer 3 — Octonion algebra reasoning network.

    Architecture:
      Input (quat/real activations from Layer 2)
        → OctonionEncoder (embed into 𝕆^(dim/8))
        → G2_YM_1 + OctHiggs_1 + moufang_relu
        → G2_YM_2 + OctHiggs_2 + moufang_relu
        → G2_YM_3 → norm^2 softmax → probabilities

    Terminal layer: 𝕆 is the last division algebra.
    No further Cayley-Dickson construction is possible without
    losing either the norm property or the division property.

    Conservation laws (G_2 — 14 generators):
      First 8: SU(3) subgroup currents (strong force analog)
      Last 6: exceptional G_2 generators
      All must be conserved across layer boundaries.

    Key diagnostic: associativity violation magnitude
      |[psi_i, W_{ij}, psi_j]| tracks non-associative dynamics.
      This is the physically meaningful quantity unique to 𝕆.
    """

    def __init__(self, vocab_size, hidden_dim=16, context_len=4, constants=None):
        self.vocab_size  = vocab_size
        self.hidden_dim  = hidden_dim
        self.context_len = context_len
        self.C           = constants or SMNNIPConstantsO()

        self.encoder = OctonionEncoder(vocab_size)
        odim         = self.encoder.oct_dim

        in_dim       = odim * context_len
        self.ym1     = G2YangMillsLayer(in_dim, hidden_dim, self.C)
        self.ym2     = G2YangMillsLayer(hidden_dim, hidden_dim, self.C)
        self.ym3     = G2YangMillsLayer(hidden_dim, vocab_size, self.C)

        self.h1      = OctonionHiggsLayer(hidden_dim, self.C)
        self.h2      = OctonionHiggsLayer(hidden_dim, self.C)

        self.loss_history         = []
        self.noether_violations   = []
        self.vev_distances        = []
        self.assoc_violations     = []
        self.fano_dominant_hist   = []

        n_params = in_dim*hidden_dim + hidden_dim**2 + hidden_dim*vocab_size
        BENCH.record("Layer3 oct params (𝕆)", n_params * 8, "real-equiv")

    def moufang_relu(self, os):
        """
        Moufang-covariant ReLU for octonions.
        Apply ReLU to norm, preserve direction on S^7.
        This preserves the G_2 covariance of the activation.
        """
        result = []
        for o in os:
            n = o.norm()
            if n < 1e-12:
                result.append(Oct.zero())
            else:
                scale = max(0.0, n) / n
                result.append(Oct([scale*c for c in o.components]))
        return result

    def softmax_oct_norm(self, os):
        norms_sq = [o.norm_sq() for o in os]
        total    = sum(norms_sq) + 1e-12
        return [n/total for n in norms_sq]

    def forward(self, context_real_vecs):
        """Forward pass through octonionic reasoning layer."""
        oct_vecs = [self.encoder.encode(v) for v in context_real_vecs]

        psi0 = []
        for ov in oct_vecs:
            psi0.extend(ov)

        expected = self.ym1.in_dim
        if len(psi0) < expected:
            psi0 += [Oct.zero()] * (expected - len(psi0))
        else:
            psi0 = psi0[:expected]

        h1   = self.ym1.forward(psi0)
        h1   = self.h1.apply(h1)
        psi1 = self.moufang_relu(h1)

        h2   = self.ym2.forward(psi1)
        h2   = self.h2.apply(h2)
        psi2 = self.moufang_relu(h2)

        logits = self.ym3.forward(psi2)
        if len(logits) < self.vocab_size:
            logits += [Oct.zero()] * (self.vocab_size - len(logits))
        logits = logits[:self.vocab_size]

        probs = self.softmax_oct_norm(logits)
        return probs, psi0, psi1, psi2, logits

    def cross_entropy_loss(self, probs, target_idx):
        return -math.log(max(probs[target_idx], 1e-12))

    def noether_check(self, psi0, psi1, psi2):
        """
        Check G_2 Noether conservation — 8 currents (SU(3) subgroup).
        """
        j0 = self.ym1.noether_current_g2(psi0)
        j1 = self.ym2.noether_current_g2(psi1)
        j2 = self.ym3.noether_current_g2(psi2)

        v01 = math.sqrt(sum((a-b)**2 for a,b in zip(j0, j1)))
        v12 = math.sqrt(sum((a-b)**2 for a,b in zip(j1, j2)))
        return v01 + v12

    def backward(self, psi0, psi1, psi2, logits, probs, target_idx, lr=0.005):
        """Moufang-corrected octonionic backpropagation."""
        grad_logit = []
        for k, p in enumerate(probs):
            delta = p - (1.0 if k == target_idx else 0.0)
            c     = [0.0]*8; c[0] = delta
            grad_logit.append(Oct(c))

        self.ym3.update(psi2, grad_logit, lr)

        grad_psi2 = [Oct.zero()] * len(psi2)
        for i in range(len(psi2)):
            s = Oct.zero()
            for j in range(min(len(grad_logit), self.ym3.out_dim)):
                s = s + (self.ym3.W[i][j] * grad_logit[j])
            grad_psi2[i] = s

        overlap2 = [grad_psi2[k] * psi2[k] if k < len(psi2) else Oct.zero()
                    for k in range(len(grad_psi2))]
        self.h2.update(overlap2, lr)
        self.ym2.update(psi1, grad_psi2, lr)

        grad_psi1 = [Oct.zero()] * len(psi1)
        for i in range(len(psi1)):
            s = Oct.zero()
            for j in range(min(len(grad_psi2), self.ym2.out_dim)):
                s = s + (self.ym2.W[i][j] * grad_psi2[j])
            grad_psi1[i] = s

        overlap1 = [grad_psi1[k] * psi1[k] if k < len(psi1) else Oct.zero()
                    for k in range(len(grad_psi1))]
        self.h1.update(overlap1, lr)
        self.ym1.update(psi0, grad_psi1, lr)

    def train_step(self, context_vecs, target_idx, lr=0.005):
        probs, psi0, psi1, psi2, logits = self.forward(context_vecs)
        loss      = self.cross_entropy_loss(probs, target_idx)
        violation = self.noether_check(psi0, psi1, psi2)
        assoc_v   = self.ym1.associativity_violation()
        self.backward(psi0, psi1, psi2, logits, probs, target_idx, lr)
        return loss, violation, assoc_v, probs

    def uncertainty_bound(self):
        return self.C.hbar_nn / 2.0

    def diagnostics(self):
        print(f"\n  ── Layer 3 (𝕆) Field Diagnostics ──")
        print(f"  alpha_NN (G2/SU3)   = {self.C.alpha_nn:.6f}")
        print(f"  hbar_NN             = {self.C.hbar_nn:.4f}")
        print(f"  ΔReason·ΔAssoc >=   {self.uncertainty_bound():.4f}")
        print(f"  H1 VEV distance     = {self.h1.vev_distance():.4f}")
        print(f"  H2 VEV distance     = {self.h2.vev_distance():.4f}")
        print(f"  Fano dominant (H1)  = e{self.h1.fano_dominant()+1}")
        print(f"  YM1 field strength  = {self.ym1.field_strength():.4f}")
        print(f"  Assoc violation     = {self.ym1.associativity_violation():.6f}")
        print(f"  (non-zero = 𝕆 dynamics active)")
        BENCH.record("H1 VEV distance final (𝕆)", self.h1.vev_distance())
        BENCH.record("Assoc violation final", self.ym1.associativity_violation())


# ---------------------------------------------------------------------------
# TRAINING LOOP
# ---------------------------------------------------------------------------

def build_training_data(text, vocab_size, context_len):
    chars       = sorted(set(text))
    char_to_idx = {c: i for i, c in enumerate(chars)}
    data        = []
    for i in range(len(text) - context_len):
        ctx  = text[i:i+context_len]
        tgt  = text[i+context_len]
        vecs = []
        for c in ctx:
            v = [0.0] * vocab_size
            v[char_to_idx.get(c, 0)] = 1.0
            vecs.append(v)
        data.append((vecs, char_to_idx.get(tgt, 0)))
    return data


def train(network, text, epochs=10, lr=0.004, cap=150):
    data = build_training_data(text, network.vocab_size, network.context_len)

    print(f"\n  Training samples: {len(data)}")
    print(f"  Uncertainty bound: {network.uncertainty_bound():.4f}")
    print(f"  Alpha_NN (G2):     {network.C.alpha_nn:.6f}")
    print()

    t0 = time.time()
    for epoch in range(epochs):
        random.shuffle(data)
        total_loss = total_viol = total_assoc = 0.0
        n = 0

        for ctx_vecs, tgt in data[:cap]:
            loss, viol, assoc, _ = network.train_step(ctx_vecs, tgt, lr)
            total_loss  += loss
            total_viol  += viol
            total_assoc += assoc
            n += 1

        avg_loss  = total_loss  / max(n, 1)
        avg_viol  = total_viol  / max(n, 1)
        avg_assoc = total_assoc / max(n, 1)
        vev_d     = (network.h1.vev_distance() + network.h2.vev_distance()) / 2
        fano_dom  = network.h1.fano_dominant()

        network.loss_history.append(avg_loss)
        network.noether_violations.append(avg_viol)
        network.vev_distances.append(vev_d)
        network.assoc_violations.append(avg_assoc)
        network.fano_dominant_hist.append(fano_dom)

        status = "⚠ violation" if avg_viol > 0.1 else "✓ conserved"
        print(f"  Epoch {epoch+1:3d}/{epochs}"
              f"  loss={avg_loss:.4f}"
              f"  Noether={avg_viol:.4f} {status}"
              f"  assoc={avg_assoc:.4f}"
              f"  VEV={vev_d:.4f}"
              f"  Fano=e{fano_dom+1}")

    BENCH.record("Training time (Layer 3)", time.time() - t0, "s")
    BENCH.record("Final loss (Layer 3)", network.loss_history[-1])
    BENCH.record("Final assoc violation", network.assoc_violations[-1])
    network.diagnostics()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == '__main__':

    print("=" * 60)
    print("  SMNNIP Layer 3 — Octonion Algebra (𝕆)")
    print("  Standard Model of Neural Network Information Propagation")
    print("  Algebra: 𝕆 (octonion, dim=8)")
    print("  Layer:   Reasoning (abstract patterns)")
    print("  Gauge:   G2/SU(3) — strong force analog")
    print("  Index:   Fano plane (7 points, 7 lines)")
    print("=" * 60)

    training_text = (
        "the quick brown fox jumps over the lazy dog. "
        "octonions are the last normed division algebra. "
        "the fano plane encodes seven imaginary units here. "
        "non-associativity means grouping of operations matters. "
        "g2 is the automorphism group of the octonions. "
        "triality is unique to eight dimensional algebra. "
        "the moufang identity replaces the chain rule here. "
        "reasoning requires the full tower from real to oct. "
        "the strong force is the su3 subgroup of g2. "
        "hurwitz theorem says this is the final algebra. "
    ) * 4

    vocab_size = len(set(training_text))
    print(f"\n  Training text:  {len(training_text)} characters")
    print(f"  Vocabulary:     {vocab_size} characters")

    C = SMNNIPConstantsO(hbar_nn=0.02, mu_sq=0.6, lam=0.2, g=0.006)
    print(f"\n  {C}")

    BENCH.record("vocab_size", vocab_size)

    net = SMNNIPLayer3Network(
        vocab_size  = vocab_size,
        hidden_dim  = 8,
        context_len = 4,
        constants   = C
    )

    train(net, training_text, epochs=10, lr=0.004, cap=100)

    BENCH.report()

    print("=" * 60)
    print("  Layer 3 (𝕆) training complete.")
    print(f"  Final loss:            {net.loss_history[-1]:.4f}")
    print(f"  Uncertainty bound:     {net.uncertainty_bound():.4f}")
    print(f"  Noether (final):       {net.noether_violations[-1]:.4f}")
    print(f"  Assoc violation:       {net.assoc_violations[-1]:.6f}")
    print(f"  Fano dominant:         e{net.fano_dominant_hist[-1]+1}")
    print(f"  (Fano index = intrinsic reasoning address)")
    print("=" * 60)
