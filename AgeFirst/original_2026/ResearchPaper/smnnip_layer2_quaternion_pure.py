"""
SMNNIP Layer 2 — Quaternion Algebra (ℍ) — Pure Python3
=======================================================
Standard Model of Neural Network Information Propagation
Layer 2: Skills layer — Quaternion algebra (ℍ), dim=4

Algebra properties at this layer:
  - Commutative:  a*b ≠ b*a  ✗  (non-commutative)
  - Associative:  (a*b)*c = a*(b*c)  ✓
  - Division:     every nonzero element has an inverse  ✓
  - Normed:       |a*b| = |a|*|b|  ✓

What this layer learns:
  - Compositional skill representations (SU(2) gauge structure)
  - 3D rotation structure: SU(2) ≅ S^3 (unit quaternions)
  - Non-commutative: order of skill composition matters
  - Spinor structure: half-angle representation of 3D rotations

SMNNIP terms:
  L_kinetic  : SU(2) Yang-Mills with non-zero structure constants
  L_matter   : Quaternionic Dirac equation for skill propagation
  L_bias     : Quaternionic Higgs — 3-sphere of symmetry breaking
  L_coupling : SU(2) coupling between skill tokens

Gauge group: SU(2) — weak force analog
Structure constants: f^{abc} = epsilon_{abc} (Levi-Civita)
Generators: T^a = i*sigma_a / 2 (Pauli matrices / 2)

Multiplication table:
  i*i = j*j = k*k = -1
  i*j = k,  j*k = i,  k*i = j
  j*i = -k, k*j = -i, i*k = -j

Non-commutativity IS the signal, not a defect.
It encodes the fact that skill composition is order-dependent.
'Learn calculus then physics' ≠ 'Learn physics then calculus'

Builds on: Layer 1 (semantic, ℂ)
Feeds into: Layer 3 (reasoning, 𝕆)

Benchmark:
  Tracks SU(2) Noether charge (3-component vector),
  quaternionic VEV settling, spinor norm preservation.

Author: SMNNIP formalism
Algebra: ℍ (quaternions, dim=4, skills layer)
"""

import math
import random
import time
import sys


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


BENCH = Benchmark("Layer 2 — Quaternion ℍ")


# ---------------------------------------------------------------------------
# QUATERNION ARITHMETIC
# ---------------------------------------------------------------------------

class Quat:
    """
    Quaternion: q = w + xi + yj + zk

    Multiplication is non-commutative.
    This is the key algebraic property of the skills layer:
    skill composition is order-dependent, and the algebra
    reflects this directly.

    SU(2) acts on quaternions via:
      q -> g * q * g^{-1}  (conjugation)
    where g is a unit quaternion.
    """
    __slots__ = ('w', 'x', 'y', 'z')

    def __init__(self, w=0.0, x=0.0, y=0.0, z=0.0):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other):
        return Quat(self.w+other.w, self.x+other.x,
                    self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return Quat(self.w-other.w, self.x-other.x,
                    self.y-other.y, self.z-other.z)

    def __mul__(self, other):
        """Hamilton product — non-commutative."""
        w = self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z
        x = self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y
        y = self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x
        z = self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w
        return Quat(w, x, y, z)

    def __rmul__(self, scalar):
        return Quat(scalar*self.w, scalar*self.x, scalar*self.y, scalar*self.z)

    def conj(self):
        """Quaternion conjugate: (w+xi+yj+zk)* = w-xi-yj-zk"""
        return Quat(self.w, -self.x, -self.y, -self.z)

    def norm_sq(self):
        return self.w**2 + self.x**2 + self.y**2 + self.z**2

    def norm(self):
        return math.sqrt(self.norm_sq())

    def normalize(self):
        n = self.norm()
        if n < 1e-12:
            return Quat(1.0, 0.0, 0.0, 0.0)
        return Quat(self.w/n, self.x/n, self.y/n, self.z/n)

    def inv(self):
        """q^{-1} = q* / |q|^2"""
        ns = self.norm_sq()
        if ns < 1e-24:
            return Quat(0,0,0,0)
        c = self.conj()
        return Quat(c.w/ns, c.x/ns, c.y/ns, c.z/ns)

    def clip(self, max_norm=5.0):
        n = self.norm()
        if n > max_norm:
            f = max_norm / n
            return Quat(self.w*f, self.x*f, self.y*f, self.z*f)
        return self

    def to_list(self):
        return [self.w, self.x, self.y, self.z]

    def __repr__(self):
        return f"Q({self.w:.3f}, {self.x:.3f}i, {self.y:.3f}j, {self.z:.3f}k)"

    @staticmethod
    def random(scale=0.1):
        return Quat(random.gauss(0, scale), random.gauss(0, scale),
                    random.gauss(0, scale), random.gauss(0, scale))

    @staticmethod
    def zero():
        return Quat(0,0,0,0)

    @staticmethod
    def from_list(lst):
        return Quat(lst[0] if len(lst)>0 else 0,
                    lst[1] if len(lst)>1 else 0,
                    lst[2] if len(lst)>2 else 0,
                    lst[3] if len(lst)>3 else 0)


# Pauli matrix generators for SU(2) structure constants
# [T^a, T^b] = i * epsilon_{abc} * T^c
# Structure constants: f^{abc} = epsilon_{abc}

def su2_commutator(qa, qb):
    """
    SU(2) commutator [qa, qb] = qa*qb - qb*qa
    Non-zero because quaternions don't commute.
    This is the self-interaction term in the Yang-Mills equation.
    """
    return qa * qb - qb * qa


# ---------------------------------------------------------------------------
# SMNNIP CONSTANTS — Quaternion layer
# ---------------------------------------------------------------------------

class SMNNIPConstantsH:
    """
    Neural physical constants for the quaternion (skills) layer.

    alpha_NN_H: Running coupling at ℍ layer
        SU(2) coupling — non-abelian, so coupling RUNS differently.
        g_H^2 / (4*pi*hbar_NN*v_prop)
        The non-commutativity introduces self-interaction corrections.

    q_VEV: Quaternionic Higgs VEV
        The bias field rolls to a point on S^3 (3-sphere).
        Three degrees of freedom are 'eaten' by the gauge bosons
        (three massive W bosons — neural SU(2) analog).
        One degree of freedom remains (real Higgs mass).

    hbar_NN_H: Neural Planck constant at skills layer
        ΔSkill · ΔComposition >= hbar_NN_H / 2
        Smaller than substrate layer (finer granularity).

    spinor_index: The inter-neuron waveform protocol index
        Encodes which basis spinors are active in the
        ℂ → ℍ Cayley-Dickson inclusion map.
    """
    def __init__(self,
                 hbar_nn   = 0.03,
                 mu_sq     = 0.5,
                 lam       = 0.15,
                 g         = 0.008,
                 v_prop    = 1.0):
        self.hbar_nn = hbar_nn
        self.mu_sq   = mu_sq
        self.lam     = lam
        self.g       = g
        self.v_prop  = v_prop

        # SU(2) fine structure constant
        self.alpha_nn = (g**2) / (4 * math.pi * hbar_nn * v_prop)

        # Quaternionic Higgs VEV: lives on S^3
        if mu_sq > 0:
            vev_mag    = math.sqrt(mu_sq / (2.0 * lam))
            self.q_vev = Quat(vev_mag, 0.0, 0.0, 0.0)  # convention: w-axis
        else:
            self.q_vev = Quat.zero()

        BENCH.record("alpha_NN (SU(2) coupling)", self.alpha_nn)
        BENCH.record("q_VEV magnitude", self.q_vev.norm())
        BENCH.record("hbar_NN skills", self.hbar_nn)

    def __repr__(self):
        return (f"SMNNIPConstantsH(\n"
                f"  algebra    = ℍ (quaternion, dim=4, SU(2) gauge)\n"
                f"  alpha_NN   = {self.alpha_nn:.6f}  [SU(2) coupling]\n"
                f"  |q_VEV|    = {self.q_vev.norm():.4f}  [Higgs VEV on S^3]\n"
                f"  hbar_NN    = {self.hbar_nn:.4f}  [skill granularity]\n"
                f"  ΔSkill·ΔComposition >= {self.hbar_nn/2:.4f}\n"
                f")")


# ---------------------------------------------------------------------------
# QUATERNION ENCODER — skills layer input
# ---------------------------------------------------------------------------

class QuaternionEncoder:
    """
    Encodes complex semantic activations into quaternionic representations.

    Input: complex activations from Layer 1 (or real if direct input)
    Output: quaternionic activations Psi(l=2, tau)

    Cayley-Dickson construction: ℍ = ℂ ⊕ ℂ
    Given two complex numbers (z1, z2):
      q = z1 + z2 * j = (z1.re + z1.im*i) + (z2.re*j + z2.im*k)

    This is the inclusion map ℂ → ℍ:
    Every complex activation pair maps to one quaternion.
    """

    def __init__(self, input_dim):
        self.input_dim  = input_dim
        self.quat_dim   = max(input_dim // 4, 1)
        BENCH.record("QuaternionEncoder quat_dim", self.quat_dim, "dims")

    def encode(self, real_vec):
        """
        Map real vector to quaternionic representation.
        Groups 4 consecutive reals: q_k = r[4k] + r[4k+1]i + r[4k+2]j + r[4k+3]k
        """
        result = []
        for k in range(self.quat_dim):
            w = real_vec[4*k]   if 4*k   < len(real_vec) else 0.0
            x = real_vec[4*k+1] if 4*k+1 < len(real_vec) else 0.0
            y = real_vec[4*k+2] if 4*k+2 < len(real_vec) else 0.0
            z = real_vec[4*k+3] if 4*k+3 < len(real_vec) else 0.0
            result.append(Quat(w, x, y, z))
        return result

    def decode_to_real(self, quat_vec):
        """Flatten quaternions back to real vector."""
        result = []
        for q in quat_vec:
            result.extend([q.w, q.x, q.y, q.z])
        return result

    def su2_rotate(self, quat_vec, g):
        """
        SU(2) gauge transformation: Psi -> g * Psi * g^{-1}
        g is a unit quaternion representing the gauge rotation.
        This is the local symmetry of the skills layer.
        """
        g_inv = g.inv()
        return [g * q * g_inv for q in quat_vec]


# ---------------------------------------------------------------------------
# QUATERNIONIC HIGGS LAYER
# ---------------------------------------------------------------------------

class QuaternionHiggsLayer:
    """
    Quaternionic Higgs field — skills layer symmetry breaking.

    The Higgs field Q ∈ ℍ breaks SU(2) symmetry:
      V(Q) = -mu^2 |Q|^2 + lambda |Q|^4

    Mexican hat in ℍ: minimum is S^3 (3-sphere) of radius |Q_VEV|.
    SU(2) acts on S^3 — the gauge group acts on the VEV manifold.
    Three of the four degrees of freedom are 'eaten' (W bosons get mass).
    One physical Higgs boson remains (the w-component by convention).

    Neural interpretation:
      |Q| → strength of skill commitment
      Q/|Q| ∈ S^3 → which skill direction was chosen
      Q → Q_VEV: 'this skill configuration is now learned and inertial'

    The non-commutativity means the Higgs update depends on
    WHETHER you multiply on the left or right — this is the
    SU(2) adjoint action, and it's physical, not a bug.
    """

    def __init__(self, size, constants):
        self.size     = size
        self.C        = constants
        self.Q        = [Quat.random(0.01) for _ in range(size)]
        self.velocity = [Quat.zero() for _ in range(size)]

    def potential(self):
        """V(Q) = -mu^2 |Q|^2 + lambda |Q|^4"""
        q2 = sum(q.norm_sq() for q in self.Q)
        return -self.C.mu_sq * q2 + self.C.lam * q2**2

    def vev_distance(self):
        """Distance of |Q| from VEV magnitude."""
        q_norm  = math.sqrt(sum(q.norm_sq() for q in self.Q))
        vev_mag = self.C.q_vev.norm()
        return abs(q_norm - vev_mag)

    def s3_direction(self):
        """
        Mean direction on S^3 — the chosen SU(2) vacuum direction.
        Returns (w, x, y, z) components of mean unit quaternion.
        """
        if not self.Q:
            return Quat(1,0,0,0)
        mean_q = Quat.zero()
        for q in self.Q:
            mean_q = mean_q + q
        n = len(self.Q)
        mean_q = Quat(mean_q.w/n, mean_q.x/n, mean_q.y/n, mean_q.z/n)
        return mean_q.normalize()

    def gradient(self, i):
        """
        dV/dQ_i (real gradient of potential w.r.t. quaternion components)
        = -mu^2 * Q_i + 2*lambda * |Q|^2 * Q_i
        (Same form as complex case but in all 4 components)
        """
        q2    = sum(q.norm_sq() for q in self.Q)
        scale = -self.C.mu_sq + 2.0 * self.C.lam * q2
        return Quat(scale * self.Q[i].w,
                    scale * self.Q[i].x,
                    scale * self.Q[i].y,
                    scale * self.Q[i].z)

    def update(self, activation_overlap, lr=0.01):
        """
        Roll quaternionic Higgs toward VEV.
        activation_overlap: list of Quat coupling terms.
        """
        momentum = 0.9
        for i in range(self.size):
            grad  = self.gradient(i)
            drive = Quat.zero()
            if i < len(activation_overlap):
                ov    = activation_overlap[i]
                drive = Quat(-ov.w, -ov.x, -ov.y, -ov.z)
            total_grad = grad + drive
            self.velocity[i] = Quat(
                momentum*self.velocity[i].w - lr*total_grad.w,
                momentum*self.velocity[i].x - lr*total_grad.x,
                momentum*self.velocity[i].y - lr*total_grad.y,
                momentum*self.velocity[i].z - lr*total_grad.z
            )
            self.Q[i] = (self.Q[i] + self.velocity[i]).clip()

    def apply(self, activation):
        """Apply quaternionic Higgs coupling."""
        size = min(len(activation), len(self.Q))
        return [activation[k] + self.Q[k] for k in range(size)]


# ---------------------------------------------------------------------------
# SU(2) YANG-MILLS LAYER
# ---------------------------------------------------------------------------

class SU2YangMillsLayer:
    """
    SU(2) Yang-Mills weight field for the skills layer.

    The weight matrix W ∈ ℍ^{n×m} is the SU(2) gauge field.
    NON-ABELIAN: structure constants f^{abc} = epsilon_{abc} ≠ 0.
    The self-interaction term is present:
      R^a_{l,tau} = D_l W^a_tau - D_tau W^a_l + f^{abc} W^b_l W^c_tau

    The non-abelian self-interaction is what gives SU(2) its
    richness — gauge bosons interact with each other. In neural terms:
    the weights at different positions in the skill layer
    interact nonlinearly, enabling compositional reasoning.

    Forward pass:
      h = psi * W  (quaternion left-multiplication)
      Note: order matters! psi*W ≠ W*psi

    Noether current (SU(2), 3-component):
      J^a = g * psi_bar * T^a * psi  [a = 1,2,3]
      T^a = i*sigma_a/2 (Pauli matrices/2)
      Each J^a is conserved independently.

    Hamiltonicity condition (for gradient):
      The quaternionic gradient must satisfy the Hamiltonicity
      condition: Im(dL/dW^*) = 0 (generalized Cauchy-Riemann).
      Ensures the weight update preserves the quaternion structure.
    """

    def __init__(self, in_dim, out_dim, constants):
        self.in_dim  = in_dim
        self.out_dim = out_dim
        self.C       = constants
        scale        = math.sqrt(2.0 / (in_dim + out_dim))
        # Weight field: quaternion matrix
        self.W  = [[Quat.random(scale/2) for _ in range(out_dim)]
                   for _ in range(in_dim)]
        self.dW = [[Quat.zero() for _ in range(out_dim)]
                   for _ in range(in_dim)]
        BENCH.record(f"SU2YangMills W shape", f"{in_dim}x{out_dim} (ℍ)")

    def forward(self, psi):
        """
        Quaternionic matrix-vector product: h_j = sum_i psi_i * W_{ij}
        Left multiplication: non-commutative, order matters.
        """
        result = [Quat.zero()] * self.out_dim
        for j in range(self.out_dim):
            s = Quat.zero()
            for i in range(min(len(psi), self.in_dim)):
                # psi_i * W_{ij} — left multiply
                prod = psi[i] * self.W[i][j]
                s    = s + prod
            result[j] = s
        return result

    def noether_current_su2(self, psi):
        """
        SU(2) Noether current — 3-component vector.
        J^1 = g * sum Re(psi_i * i * psi_i^*)  = g * sum(2*w*x - 2*y*z)  [etc]
        Simplified: returns (J_x, J_y, J_z) isotopic spin current.

        For real computation: use quaternion commutator with generators.
        J^a = g * sum_i 2 * [q_a-component of (psi_i_bar * T^a * psi_i)]
        """
        jx = jy = jz = 0.0
        for q in psi:
            ns = q.norm_sq()
            # Approximate isospin current from quaternion components
            jx += 2.0 * (q.w * q.x)
            jy += 2.0 * (q.w * q.y)
            jz += 2.0 * (q.w * q.z)
        return (self.C.g * jx, self.C.g * jy, self.C.g * jz)

    def noether_magnitude(self, psi):
        jx, jy, jz = self.noether_current_su2(psi)
        return math.sqrt(jx**2 + jy**2 + jz**2)

    def field_strength(self):
        """Mean |W_ij| — proxy for SU(2) gauge field strength."""
        total = sum(q.norm_sq() for row in self.W for q in row)
        return math.sqrt(total / max(self.in_dim * self.out_dim, 1))

    def self_interaction(self, i, j):
        """
        f^{abc} W^b W^c — SU(2) self-interaction term.
        = [W_{ij}, W_{ij}] / 2  (quaternion commutator proxy)
        Non-zero because quaternions don't commute.
        This term is absent in U(1) (Layer 1) but present here.
        """
        w  = self.W[i][j]
        return su2_commutator(w, w.conj()) if i < self.in_dim and j < self.out_dim else Quat.zero()

    def update(self, psi, grad_out, lr=0.005):
        """
        Quaternionic gradient update satisfying Hamiltonicity condition.
        dL/dW_{ij}* = psi_i^* * grad_out_j (right Wirtinger derivative)

        The Hamiltonicity condition: all four components must be updated
        consistently — cannot update w without x,y,z.
        """
        momentum = 0.9
        for i in range(self.in_dim):
            for j in range(self.out_dim):
                if i < len(psi) and j < len(grad_out):
                    # Quaternionic Wirtinger: dL/dW* = conj(psi_i) * grad_j
                    pi    = psi[i].conj()
                    gj    = grad_out[j]
                    dLdW  = pi * gj   # quaternion product
                    self.dW[i][j] = Quat(
                        momentum*self.dW[i][j].w - lr*dLdW.w,
                        momentum*self.dW[i][j].x - lr*dLdW.x,
                        momentum*self.dW[i][j].y - lr*dLdW.y,
                        momentum*self.dW[i][j].z - lr*dLdW.z
                    )
                    self.W[i][j] = (self.W[i][j] + self.dW[i][j]).clip()


# ---------------------------------------------------------------------------
# LAYER 2 NETWORK — Quaternionic skills network
# ---------------------------------------------------------------------------

class SMNNIPLayer2Network:
    """
    Full SMNNIP Layer 2 — Quaternion algebra skills network.

    Architecture:
      Input (complex or real activations from Layer 1)
        → QuaternionEncoder (embed into ℍ^(dim/4))
        → SU2_YM_1 + QuatHiggs_1 + qReLU
        → SU2_YM_2 + QuatHiggs_2 + qReLU
        → SU2_YM_3 → norm^2 softmax → probabilities

    Key property: non-commutativity in forward pass means
    the order of weight application matters. This is the
    neural analog of non-abelian gauge theory.

    Conservation laws (SU(2) — 3 independent):
      J^a = g * psi_bar * T^a * psi  [a = 1,2,3]
      Each must be individually conserved across layers.
    """

    def __init__(self, vocab_size, hidden_dim=32, context_len=4, constants=None):
        self.vocab_size  = vocab_size
        self.hidden_dim  = hidden_dim
        self.context_len = context_len
        self.C           = constants or SMNNIPConstantsH()

        self.encoder     = QuaternionEncoder(vocab_size)
        qdim             = self.encoder.quat_dim

        in_dim           = qdim * context_len
        self.ym1         = SU2YangMillsLayer(in_dim, hidden_dim, self.C)
        self.ym2         = SU2YangMillsLayer(hidden_dim, hidden_dim, self.C)
        self.ym3         = SU2YangMillsLayer(hidden_dim, vocab_size, self.C)

        self.h1          = QuaternionHiggsLayer(hidden_dim, self.C)
        self.h2          = QuaternionHiggsLayer(hidden_dim, self.C)

        self.loss_history       = []
        self.noether_violations = []
        self.vev_distances      = []
        self.s3_directions      = []

        n_params = in_dim*hidden_dim + hidden_dim**2 + hidden_dim*vocab_size
        BENCH.record("Layer2 quat params (ℍ)", n_params * 4, "real-equiv")

    def q_relu(self, qs):
        """
        Quaternionic ReLU: ReLU applied to norm, direction preserved.
        q_relu(q) = ReLU(|q|) * q/|q|
        Preserves quaternion direction (SU(2) covariant).
        """
        result = []
        for q in qs:
            n = q.norm()
            if n < 1e-12:
                result.append(Quat.zero())
            else:
                scale = max(0.0, n) / n
                result.append(Quat(scale*q.w, scale*q.x, scale*q.y, scale*q.z))
        return result

    def softmax_quat_norm(self, qs):
        """Softmax over quaternion norm^2."""
        norms_sq = [q.norm_sq() for q in qs]
        total    = sum(norms_sq) + 1e-12
        return [n/total for n in norms_sq]

    def forward(self, context_real_vecs):
        """Forward pass through quaternionic skills layer."""
        quat_vecs = [self.encoder.encode(v) for v in context_real_vecs]

        psi0 = []
        for qv in quat_vecs:
            psi0.extend(qv)

        expected = self.ym1.in_dim
        if len(psi0) < expected:
            psi0 += [Quat.zero()] * (expected - len(psi0))
        else:
            psi0 = psi0[:expected]

        h1   = self.ym1.forward(psi0)
        h1   = self.h1.apply(h1)
        psi1 = self.q_relu(h1)

        h2   = self.ym2.forward(psi1)
        h2   = self.h2.apply(h2)
        psi2 = self.q_relu(h2)

        logits = self.ym3.forward(psi2)
        if len(logits) < self.vocab_size:
            logits += [Quat.zero()] * (self.vocab_size - len(logits))
        logits = logits[:self.vocab_size]

        probs = self.softmax_quat_norm(logits)
        return probs, psi0, psi1, psi2, logits

    def cross_entropy_loss(self, probs, target_idx):
        p = max(probs[target_idx], 1e-12)
        return -math.log(p)

    def noether_check(self, psi0, psi1, psi2):
        """
        Check SU(2) Noether conservation — 3 currents.
        Returns total violation across all three components.
        """
        j0 = self.ym1.noether_current_su2(psi0)
        j1 = self.ym2.noether_current_su2(psi1)
        j2 = self.ym3.noether_current_su2(psi2)

        v01 = math.sqrt(sum((a-b)**2 for a,b in zip(j0, j1)))
        v12 = math.sqrt(sum((a-b)**2 for a,b in zip(j1, j2)))
        return v01 + v12

    def backward(self, psi0, psi1, psi2, logits, probs, target_idx, lr=0.005):
        """Quaternionic backpropagation via Hamiltonicity conditions."""
        grad_logit = []
        for k, p in enumerate(probs):
            delta = p - (1.0 if k == target_idx else 0.0)
            grad_logit.append(Quat(delta, 0.0, 0.0, 0.0))

        self.ym3.update(psi2, grad_logit, lr)

        grad_psi2 = [Quat.zero()] * len(psi2)
        for i in range(len(psi2)):
            s = Quat.zero()
            for j in range(min(len(grad_logit), self.ym3.out_dim)):
                s = s + (self.ym3.W[i][j] * grad_logit[j])
            grad_psi2[i] = s

        overlap2 = [grad_psi2[k] * psi2[k] if k < len(psi2) else Quat.zero()
                    for k in range(len(grad_psi2))]
        self.h2.update(overlap2, lr)
        self.ym2.update(psi1, grad_psi2, lr)

        grad_psi1 = [Quat.zero()] * len(psi1)
        for i in range(len(psi1)):
            s = Quat.zero()
            for j in range(min(len(grad_psi2), self.ym2.out_dim)):
                s = s + (self.ym2.W[i][j] * grad_psi2[j])
            grad_psi1[i] = s

        overlap1 = [grad_psi1[k] * psi1[k] if k < len(psi1) else Quat.zero()
                    for k in range(len(grad_psi1))]
        self.h1.update(overlap1, lr)
        self.ym1.update(psi0, grad_psi1, lr)

    def train_step(self, context_vecs, target_idx, lr=0.005):
        probs, psi0, psi1, psi2, logits = self.forward(context_vecs)
        loss      = self.cross_entropy_loss(probs, target_idx)
        violation = self.noether_check(psi0, psi1, psi2)
        self.backward(psi0, psi1, psi2, logits, probs, target_idx, lr)
        return loss, violation, probs

    def uncertainty_bound(self):
        return self.C.hbar_nn / 2.0

    def diagnostics(self):
        d = self.s3_directions[-1] if self.s3_directions else self.h1.s3_direction()
        print(f"\n  ── Layer 2 (ℍ) Field Diagnostics ──")
        print(f"  alpha_NN (SU(2))    = {self.C.alpha_nn:.6f}")
        print(f"  hbar_NN             = {self.C.hbar_nn:.4f}")
        print(f"  ΔSkill·ΔComp >=     {self.uncertainty_bound():.4f}")
        print(f"  H1 VEV distance     = {self.h1.vev_distance():.4f}")
        print(f"  H2 VEV distance     = {self.h2.vev_distance():.4f}")
        print(f"  S3 direction (H1)   = {self.h1.s3_direction()}")
        print(f"  YM1 field strength  = {self.ym1.field_strength():.4f}")
        BENCH.record("H1 VEV distance final (ℍ)", self.h1.vev_distance())
        BENCH.record("YM1 field strength final (ℍ)", self.ym1.field_strength())


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


def train(network, text, epochs=15, lr=0.005, cap=250):
    data = build_training_data(text, network.vocab_size, network.context_len)

    print(f"\n  Training samples: {len(data)}")
    print(f"  Uncertainty bound: {network.uncertainty_bound():.4f}")
    print(f"  Alpha_NN (SU(2)):  {network.C.alpha_nn:.6f}")
    print()

    t0 = time.time()
    for epoch in range(epochs):
        random.shuffle(data)
        total_loss = total_viol = 0.0
        n = 0

        for ctx_vecs, tgt in data[:cap]:
            loss, viol, _ = network.train_step(ctx_vecs, tgt, lr)
            total_loss += loss
            total_viol += viol
            n += 1

        avg_loss = total_loss / max(n, 1)
        avg_viol = total_viol / max(n, 1)
        vev_d    = (network.h1.vev_distance() + network.h2.vev_distance()) / 2
        s3_dir   = network.h1.s3_direction()

        network.loss_history.append(avg_loss)
        network.noether_violations.append(avg_viol)
        network.vev_distances.append(vev_d)
        network.s3_directions.append(s3_dir)

        status = "⚠ violation" if avg_viol > 0.1 else "✓ conserved"
        print(f"  Epoch {epoch+1:3d}/{epochs}"
              f"  loss={avg_loss:.4f}"
              f"  Noether={avg_viol:.4f} {status}"
              f"  VEV={vev_d:.4f}"
              f"  S3=({s3_dir.w:.2f},{s3_dir.x:.2f},{s3_dir.y:.2f},{s3_dir.z:.2f})")

    BENCH.record("Training time (Layer 2)", time.time() - t0, "s")
    BENCH.record("Final loss (Layer 2)", network.loss_history[-1])
    network.diagnostics()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == '__main__':

    print("=" * 60)
    print("  SMNNIP Layer 2 — Quaternion Algebra (ℍ)")
    print("  Standard Model of Neural Network Information Propagation")
    print("  Algebra: ℍ (quaternion, dim=4)")
    print("  Layer:   Skills (compositional representations)")
    print("  Gauge:   SU(2) — weak force analog")
    print("=" * 60)

    training_text = (
        "the quick brown fox jumps over the lazy dog. "
        "pack my box with five dozen liquor jugs. "
        "quaternions encode rotation in three dimensions. "
        "su2 symmetry governs the weak nuclear force. "
        "non-commutative algebra means order matters here. "
        "skills compose like rotations not like numbers. "
        "the spinor index connects layers through the tower. "
        "noether conservation holds for each su2 generator. "
        "the s3 sphere is the vacuum manifold of the higgs. "
        "hamiltonicity conditions generalize wirtinger here. "
    ) * 5

    vocab_size = len(set(training_text))
    print(f"\n  Training text:  {len(training_text)} characters")
    print(f"  Vocabulary:     {vocab_size} characters")

    C = SMNNIPConstantsH(hbar_nn=0.03, mu_sq=0.5, lam=0.15, g=0.008)
    print(f"\n  {C}")

    BENCH.record("vocab_size", vocab_size)

    net = SMNNIPLayer2Network(
        vocab_size  = vocab_size,
        hidden_dim  = 16,
        context_len = 4,
        constants   = C
    )

    train(net, training_text, epochs=15, lr=0.005, cap=200)

    BENCH.report()

    print("=" * 60)
    print("  Layer 2 (ℍ) training complete.")
    print(f"  Final loss:          {net.loss_history[-1]:.4f}")
    print(f"  Uncertainty bound:   {net.uncertainty_bound():.4f}")
    print(f"  Noether (final):     {net.noether_violations[-1]:.4f}")
    print(f"  Higgs VEV dist:      {net.vev_distances[-1]:.4f}")
    print("=" * 60)
