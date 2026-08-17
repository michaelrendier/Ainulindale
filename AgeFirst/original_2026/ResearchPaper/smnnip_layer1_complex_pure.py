"""
SMNNIP Layer 1 — Complex Algebra (ℂ) — Pure Python3
=====================================================
Standard Model of Neural Network Information Propagation
Layer 1: Semantic layer — Complex algebra (ℂ), dim=2

Algebra properties at this layer:
  - Commutative:  a*b = b*a  ✓
  - Associative:  (a*b)*c = a*(b*c)  ✓
  - Division:     every nonzero element has an inverse  ✓
  - NOT ordered:  no total order compatible with operations

What this layer learns:
  - Token-level semantic relationships
  - Phase relationships between concepts (U(1) gauge structure)
  - The 'rotation' of meaning in 2D complex representation space
  - Wirtinger derivatives enable complex-valued gradient flow

SMNNIP terms:
  L_kinetic  : U(1) gauge field curvature (electromagnetic analog)
  L_matter   : Complex Dirac equation for semantic propagation
  L_bias     : Complex Higgs — phase of symmetry breaking
  L_coupling : U(1) coupling between semantic tokens

Gauge group: U(1) — electromagnetism analog
Structure constants: f^{abc} = epsilon tensor (complex)
Generators: T = i (single generator, U(1) abelian)

Builds on: Layer 0 (substrate, R algebra)
Feeds into: Layer 2 (skills, H algebra)

Benchmark notes:
  - Wirtinger gradient replaces real gradient
  - Complex norm preservation: |z_out| = |z_in| under unitary transform
  - U(1) Noether charge: |J| = g * |psi|^2 (conserved)

Author: SMNNIP formalism
Algebra: ℂ (complex, dim=2, semantic layer)
"""

import math
import cmath
import random
import sys
import time


# ---------------------------------------------------------------------------
# BENCHMARK INFRASTRUCTURE
# ---------------------------------------------------------------------------

class Benchmark:
    """Records timing and diagnostic data for all layer operations."""
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


BENCH = Benchmark("Layer 1 — Complex ℂ")


# ---------------------------------------------------------------------------
# COMPLEX NUMBER UTILITIES
# ---------------------------------------------------------------------------

def c_mul(a, b):
    """Complex multiplication: (a.re + a.im*i)(b.re + b.im*i)"""
    return complex(a.real*b.real - a.imag*b.imag,
                   a.real*b.imag + a.imag*b.real)

def c_conj(z):
    return complex(z.real, -z.imag)

def c_norm(z):
    return math.sqrt(z.real**2 + z.imag**2)

def c_normalize(z):
    n = c_norm(z)
    if n < 1e-12:
        return complex(1.0, 0.0)
    return complex(z.real/n, z.imag/n)

def wirtinger_d(f_val, z, h=1e-7):
    """
    Wirtinger derivative: df/dz* (conjugate derivative)
    For real-valued loss L, dL/dz* = (dL/dx + i*dL/dy) / 2
    Approximated via finite difference in complex plane.
    """
    dfdx = (f_val(complex(z.real + h, z.imag)) -
            f_val(complex(z.real - h, z.imag))) / (2*h)
    dfdy = (f_val(complex(z.real, z.imag + h)) -
            f_val(complex(z.real, z.imag - h))) / (2*h)
    return complex(dfdx, dfdy) * 0.5

def softmax_complex_norm(zs):
    """
    Softmax over complex norms — maps complex activations to probabilities.
    |z_i|^2 / sum(|z_j|^2)
    """
    norms_sq = [z.real**2 + z.imag**2 for z in zs]
    total    = sum(norms_sq) + 1e-12
    return [n / total for n in norms_sq]

def clip_complex(z, max_norm=5.0):
    """Clip complex number to max norm."""
    n = c_norm(z)
    if n > max_norm:
        return complex(z.real * max_norm/n, z.imag * max_norm/n)
    return z


# ---------------------------------------------------------------------------
# SMNNIP CONSTANTS — Complex layer
# ---------------------------------------------------------------------------

class SMNNIPConstantsC:
    """
    Neural physical constants for the complex (semantic) layer.

    alpha_NN: Neural fine structure constant at ℂ layer
        U(1) coupling — strength of semantic entanglement.
        Runs from substrate value via neural RG equation.

    phi_VEV: Complex Higgs VEV — phase angle of symmetry breaking
        |phi_VEV| = sqrt(mu^2 / 2*lambda)
        arg(phi_VEV) = spontaneously chosen phase (0 by convention)

    hbar_NN: Neural Planck constant
        ΔSemantic · ΔPhase >= hbar_NN / 2
        Sets minimum semantic granularity at this layer.

    omega_rg: RG running parameter
        alpha_NN(l) = alpha_NN(0) * omega_rg^l
        Tracks coupling strength across layer depth.
    """
    def __init__(self,
                 hbar_nn   = 0.05,
                 mu_sq     = 0.4,
                 lam       = 0.1,
                 g         = 0.01,
                 v_prop    = 1.0,
                 omega_rg  = 0.95):
        self.hbar_nn  = hbar_nn
        self.mu_sq    = mu_sq
        self.lam      = lam
        self.g        = g
        self.v_prop   = v_prop
        self.omega_rg = omega_rg

        # U(1) fine structure constant
        self.alpha_nn = (g**2) / (4 * math.pi * hbar_nn * v_prop)

        # Complex Higgs VEV
        if mu_sq > 0:
            vev_mag      = math.sqrt(mu_sq / (2.0 * lam))
            self.phi_vev = complex(vev_mag, 0.0)   # convention: real axis
        else:
            self.phi_vev = complex(0.0, 0.0)

        BENCH.record("alpha_NN (U(1) coupling)", self.alpha_nn)
        BENCH.record("phi_VEV magnitude", c_norm(self.phi_vev))
        BENCH.record("hbar_NN semantic", self.hbar_nn)

    def rg_run(self, layer_depth):
        """Neural RG running: alpha(l) = alpha(0) * omega^l"""
        return self.alpha_nn * (self.omega_rg ** layer_depth)

    def __repr__(self):
        return (f"SMNNIPConstantsC(\n"
                f"  algebra    = ℂ (complex, dim=2, U(1) gauge)\n"
                f"  alpha_NN   = {self.alpha_nn:.6f}  [U(1) coupling]\n"
                f"  |phi_VEV|  = {c_norm(self.phi_vev):.4f}  [Higgs VEV magnitude]\n"
                f"  hbar_NN    = {self.hbar_nn:.4f}  [semantic granularity]\n"
                f"  omega_RG   = {self.omega_rg:.4f}  [RG running factor]\n"
                f"  ΔSemantic·ΔPhase >= {self.hbar_nn/2:.4f}\n"
                f")")


# ---------------------------------------------------------------------------
# COMPLEX ENCODER — semantic layer input
# ---------------------------------------------------------------------------

class ComplexEncoder:
    """
    Encodes token-level representations into complex-valued activations.

    Input: real-valued substrate activation (from Layer 0)
    Output: complex activation Psi(l=1, tau)

    Encoding: embed real vector into ℂ^(vocab/2)
      - Pairs of adjacent real components → complex number
      - Phase encodes relative importance
      - Magnitude encodes activation strength

    In SMNNIP terms:
      Psi_i(l=1, tau) = r_i * exp(i * theta_i)
      where r_i, theta_i derived from substrate activations.
    """

    def __init__(self, vocab_size):
        self.vocab_size  = vocab_size
        self.complex_dim = max(vocab_size // 2, 1)
        # Learnable phase offsets — initialized uniformly on circle
        self.phase_bias  = [complex(math.cos(2*math.pi*k/self.complex_dim),
                                     math.sin(2*math.pi*k/self.complex_dim))
                            for k in range(self.complex_dim)]
        BENCH.record("ComplexEncoder complex_dim", self.complex_dim, "dims")

    def encode(self, real_vec):
        """
        Map real activation vector to complex representation.
        Pairs consecutive reals: z_k = real_vec[2k] + i*real_vec[2k+1]
        """
        result = []
        for k in range(self.complex_dim):
            re = real_vec[2*k]     if 2*k   < len(real_vec) else 0.0
            im = real_vec[2*k+1]  if 2*k+1 < len(real_vec) else 0.0
            result.append(complex(re, im))
        return result

    def decode_to_real(self, complex_vec):
        """Interleave real and imaginary parts back to real vector."""
        result = []
        for z in complex_vec:
            result.append(z.real)
            result.append(z.imag)
        return result

    def u1_rotate(self, complex_vec, theta):
        """
        U(1) gauge transformation: Psi -> exp(i*theta) * Psi
        This is the local gauge freedom at the semantic layer.
        Physical observables are invariant under this rotation.
        """
        phase = complex(math.cos(theta), math.sin(theta))
        return [c_mul(z, phase) for z in complex_vec]


# ---------------------------------------------------------------------------
# COMPLEX HIGGS LAYER — semantic symmetry breaking
# ---------------------------------------------------------------------------

class ComplexHiggsLayer:
    """
    Complex Higgs field — semantic symmetry breaking.

    The complex Higgs field phi ∈ ℂ breaks U(1) symmetry:
      V(phi) = -mu^2 |phi|^2 + lambda |phi|^4

    Mexican hat in ℂ: minimum is a CIRCLE of radius |phi_VEV|.
    The phase of phi_VEV is spontaneously chosen — this is
    the semantic 'direction' the layer commits to.

    Neural interpretation:
      |phi| → strength of semantic commitment
      arg(phi) → phase / direction of semantic encoding
      phi → phi_VEV means: 'this semantic direction is now massive'
      i.e., the layer has learned which phase of meaning to amplify.

    Benchmark:
      Tracks VEV distance, potential value, phase angle over training.
    """

    def __init__(self, size, constants):
        self.size = size
        self.C    = constants
        # Initialize near zero — full U(1) symmetry
        scale     = 0.01
        self.phi  = [complex(random.gauss(0, scale),
                             random.gauss(0, scale))
                     for _ in range(size)]
        self.velocity = [complex(0.0, 0.0)] * size

    def potential(self):
        """V(phi) = -mu^2 |phi|^2 + lambda |phi|^4"""
        phi2 = sum(z.real**2 + z.imag**2 for z in self.phi)
        return -self.C.mu_sq * phi2 + self.C.lam * phi2**2

    def vev_distance(self):
        """Distance of |phi| from VEV magnitude."""
        phi_norm = math.sqrt(sum(z.real**2 + z.imag**2 for z in self.phi))
        vev_mag  = c_norm(self.C.phi_vev)
        return abs(phi_norm - vev_mag)

    def phase_angle(self):
        """Mean phase angle of the Higgs field — the chosen U(1) direction."""
        if not self.phi:
            return 0.0
        mean_z = sum(self.phi, complex(0,0)) / len(self.phi)
        return cmath.phase(mean_z)

    def gradient(self, i):
        """
        dV/dphi_i* (Wirtinger derivative of potential w.r.t. phi_i conjugate)
        = -mu^2 * phi_i + 2*lambda * |phi|^2 * phi_i
        """
        phi2 = sum(z.real**2 + z.imag**2 for z in self.phi)
        return complex(
            (-self.C.mu_sq + 2.0 * self.C.lam * phi2) * self.phi[i].real,
            (-self.C.mu_sq + 2.0 * self.C.lam * phi2) * self.phi[i].imag
        )

    def update(self, activation_overlap, lr=0.01):
        """
        Roll Higgs field toward VEV via complex gradient descent.
        activation_overlap: complex coupling from adjacent layer activations.
        """
        momentum = 0.9
        for i in range(self.size):
            grad  = self.gradient(i)
            drive = -activation_overlap[i] if i < len(activation_overlap) else complex(0,0)
            total_grad = complex(grad.real + drive.real, grad.imag + drive.imag)
            self.velocity[i] = complex(
                momentum * self.velocity[i].real - lr * total_grad.real,
                momentum * self.velocity[i].imag - lr * total_grad.imag
            )
            new_phi = complex(
                self.phi[i].real + self.velocity[i].real,
                self.phi[i].imag + self.velocity[i].imag
            )
            self.phi[i] = clip_complex(new_phi)

    def apply(self, activation):
        """Apply complex Higgs coupling to activation."""
        size = min(len(activation), len(self.phi))
        return [complex(activation[k].real + self.phi[k].real,
                        activation[k].imag + self.phi[k].imag)
                for k in range(size)]


# ---------------------------------------------------------------------------
# U(1) YANG-MILLS LAYER — complex weight field
# ---------------------------------------------------------------------------

class U1YangMillsLayer:
    """
    U(1) Yang-Mills weight field for the semantic layer.

    The weight matrix W ∈ ℂ^{n×m} is the U(1) gauge field.
    In the abelian U(1) case, the structure constants vanish
    (f^{abc} = 0), so the self-interaction term is absent.
    This is the neural analog of electromagnetism — the simplest
    non-trivial gauge theory.

    Field strength: F_{l,tau} = D_l W_tau - D_tau W_l
    (For U(1): F = dW, no commutator term)

    Wirtinger forward pass:
      h = psi @ W   (complex matrix multiplication)
      where psi ∈ ℂ^batch, W ∈ ℂ^{in×out}

    Noether current (U(1)):
      J = g * |psi|^2   [conserved under U(1) rotations]

    Benchmark:
      Tracks field strength, Noether current, weight norm over training.
    """

    def __init__(self, in_dim, out_dim, constants):
        self.in_dim  = in_dim
        self.out_dim = out_dim
        self.C       = constants
        # Initialize weights: complex Glorot
        scale = math.sqrt(2.0 / (in_dim + out_dim))
        self.W = [[complex(random.gauss(0, scale/math.sqrt(2)),
                           random.gauss(0, scale/math.sqrt(2)))
                   for _ in range(out_dim)]
                  for _ in range(in_dim)]
        # Velocity for momentum
        self.dW = [[complex(0,0)] * out_dim for _ in range(in_dim)]

        BENCH.record(f"U1YangMills W shape", f"{in_dim}x{out_dim}")

    def forward(self, psi):
        """
        Complex matrix-vector product: h = W^dagger * psi
        Wirtinger: uses conjugate transpose for proper complex gradient.
        """
        result = [complex(0,0)] * self.out_dim
        for j in range(self.out_dim):
            s = complex(0,0)
            for i in range(min(len(psi), self.in_dim)):
                # W^dagger = conj(W^T): multiply by conjugate of W[i][j]
                s = complex(s.real + self.W[i][j].real * psi[i].real
                                   + self.W[i][j].imag * psi[i].imag,
                            s.imag + self.W[i][j].real * psi[i].imag
                                   - self.W[i][j].imag * psi[i].real)
            result[j] = s
        return result

    def noether_current(self, psi):
        """J = g * sum(|psi_i|^2) — U(1) conserved charge."""
        return self.C.g * sum(z.real**2 + z.imag**2 for z in psi)

    def field_strength(self):
        """Mean |W_ij|^2 — proxy for gauge field strength."""
        total = sum(z.real**2 + z.imag**2
                    for row in self.W for z in row)
        return math.sqrt(total / max(self.in_dim * self.out_dim, 1))

    def kinetic_penalty(self):
        """L_kinetic = 0.001 * sum(|W|^2) — smoothness regularizer."""
        return 0.001 * sum(z.real**2 + z.imag**2
                           for row in self.W for z in row)

    def update(self, psi, grad_out, lr=0.005):
        """
        Wirtinger gradient update for complex weights.
        dL/dW_ij* = psi_i * conj(grad_out_j)
        Uses momentum (0.9) for stability.
        """
        momentum = 0.9
        for i in range(self.in_dim):
            for j in range(self.out_dim):
                if i < len(psi) and j < len(grad_out):
                    # Wirtinger: dL/dW* = psi_i * (grad_j)*
                    g_re = (psi[i].real * grad_out[j].real +
                            psi[i].imag * grad_out[j].imag)
                    g_im = (psi[i].real * grad_out[j].imag -
                            psi[i].imag * grad_out[j].real)
                    self.dW[i][j] = complex(
                        momentum * self.dW[i][j].real - lr * g_re,
                        momentum * self.dW[i][j].imag - lr * g_im
                    )
                    new_w = complex(
                        self.W[i][j].real + self.dW[i][j].real,
                        self.W[i][j].imag + self.dW[i][j].imag
                    )
                    self.W[i][j] = clip_complex(new_w)


# ---------------------------------------------------------------------------
# LAYER 1 NETWORK — Complex semantic network
# ---------------------------------------------------------------------------

class SMNNIPLayer1Network:
    """
    Full SMNNIP Layer 1 — Complex algebra semantic network.

    Architecture:
      Input (real substrate activations)
        → ComplexEncoder (embed R^vocab into ℂ^(vocab/2))
        → U1_YM_1 (complex weight field, in→hidden)
        → ComplexHiggs_1 (symmetry breaking)
        → U(1) phase activation (cReLU variant)
        → U1_YM_2 (complex weight field, hidden→hidden)
        → ComplexHiggs_2 (symmetry breaking)
        → U1_YM_3 (complex weight field, hidden→out)
        → softmax over complex norms → probability distribution

    Conservation law:
      Noether charge J = g * |psi|^2 must be conserved
      across all U(1) layer boundaries.

    Training inequality:
      N_GD > N_SMNNIP * |lambda|^{-2L} * sqrt(kappa)
      The complex Wirtinger structure provides curvature information
      absent from real gradient descent.
    """

    def __init__(self, vocab_size, hidden_dim=64, context_len=6, constants=None):
        self.vocab_size  = vocab_size
        self.hidden_dim  = hidden_dim
        self.context_len = context_len
        self.C           = constants or SMNNIPConstantsC()

        self.encoder     = ComplexEncoder(vocab_size)
        cdim             = self.encoder.complex_dim

        # Three U(1) Yang-Mills layers
        in_dim           = cdim * context_len
        self.ym1         = U1YangMillsLayer(in_dim, hidden_dim, self.C)
        self.ym2         = U1YangMillsLayer(hidden_dim, hidden_dim, self.C)
        self.ym3         = U1YangMillsLayer(hidden_dim, vocab_size, self.C)

        # Two Higgs layers (symmetry breaking)
        self.h1          = ComplexHiggsLayer(hidden_dim, self.C)
        self.h2          = ComplexHiggsLayer(hidden_dim, self.C)

        # Training history
        self.loss_history        = []
        self.noether_violations  = []
        self.vev_distances       = []
        self.phase_history       = []

        n_params = in_dim*hidden_dim + hidden_dim*hidden_dim + hidden_dim*vocab_size
        BENCH.record("Layer1 complex params (ℂ)", n_params * 2, "real-equiv")

    def c_relu(self, zs):
        """
        Complex ReLU: apply ReLU to real and imaginary parts independently.
        Preserves complex structure while introducing nonlinearity.
        Alternative: modReLU = ReLU(|z| - b) * z/|z|
        """
        return [complex(max(0.0, z.real), max(0.0, z.imag)) for z in zs]

    def forward(self, context_real_vecs):
        """
        Forward pass through complex semantic layer.
        context_real_vecs: list of real activation vectors from substrate.
        Returns: probability distribution over vocabulary.
        """
        # Encode each context position to complex
        complex_vecs = [self.encoder.encode(v) for v in context_real_vecs]

        # Flatten context: (context_len * complex_dim,) complex vector
        psi0 = []
        for cv in complex_vecs:
            psi0.extend(cv)

        # Pad or truncate to expected input dim
        expected = self.ym1.in_dim
        if len(psi0) < expected:
            psi0 += [complex(0,0)] * (expected - len(psi0))
        else:
            psi0 = psi0[:expected]

        # Layer 1: U(1) YM + Higgs + activation
        h1   = self.ym1.forward(psi0)
        h1   = self.h1.apply(h1)
        psi1 = self.c_relu(h1)

        # Layer 2: U(1) YM + Higgs + activation
        h2   = self.ym2.forward(psi1)
        h2   = self.h2.apply(h2)
        psi2 = self.c_relu(h2)

        # Output layer: U(1) YM → prob over vocab via norm^2 softmax
        logits = self.ym3.forward(psi2)

        # Ensure output has vocab_size entries
        if len(logits) < self.vocab_size:
            logits += [complex(0,0)] * (self.vocab_size - len(logits))
        logits = logits[:self.vocab_size]

        probs = softmax_complex_norm(logits)
        return probs, psi0, psi1, psi2, logits

    def cross_entropy_loss(self, probs, target_idx):
        """Standard cross-entropy on complex-norm probabilities."""
        p = max(probs[target_idx], 1e-12)
        return -math.log(p)

    def noether_check(self, psi0, psi1, psi2):
        """
        Check U(1) Noether current conservation across layers.
        J_l = g * |psi_l|^2 should be constant.
        Returns violation magnitude.
        """
        j0 = self.ym1.noether_current(psi0)
        j1 = self.ym2.noether_current(psi1)
        j2 = self.ym3.noether_current(psi2)
        v01 = abs(j1 - j0)
        v12 = abs(j2 - j1)
        return v01 + v12, j0, j1, j2

    def backward(self, psi0, psi1, psi2, logits, probs, target_idx, lr=0.005):
        """
        Wirtinger backpropagation through complex layers.
        Uses complex chain rule: dL/dW* = psi * (dL/dh)*
        """
        # Output gradient: dL/dlogit (softmax cross-entropy)
        grad_logit = []
        for k, p in enumerate(probs):
            if k == target_idx:
                grad_logit.append(complex(p - 1.0, 0.0))
            else:
                grad_logit.append(complex(p, 0.0))

        # Backprop through ym3
        self.ym3.update(psi2, grad_logit, lr)

        # Gradient into psi2 via ym3 weights (approximate)
        grad_psi2 = [complex(0,0)] * len(psi2)
        for i in range(len(psi2)):
            s = complex(0,0)
            for j in range(min(len(grad_logit), self.ym3.out_dim)):
                s = complex(s.real + self.ym3.W[i][j].real * grad_logit[j].real,
                            s.imag + self.ym3.W[i][j].imag * grad_logit[j].imag)
            grad_psi2[i] = s

        # Higgs update layer 2
        overlap2 = [complex(grad_psi2[k].real * psi2[k].real,
                            grad_psi2[k].imag * psi2[k].imag)
                    for k in range(min(len(grad_psi2), len(psi2)))]
        self.h2.update(overlap2, lr)

        # Backprop through ym2
        self.ym2.update(psi1, grad_psi2, lr)

        # Gradient into psi1
        grad_psi1 = [complex(0,0)] * len(psi1)
        for i in range(len(psi1)):
            s = complex(0,0)
            for j in range(min(len(grad_psi2), self.ym2.out_dim)):
                s = complex(s.real + self.ym2.W[i][j].real * grad_psi2[j].real,
                            s.imag + self.ym2.W[i][j].imag * grad_psi2[j].imag)
            grad_psi1[i] = s

        # Higgs update layer 1
        overlap1 = [complex(grad_psi1[k].real * psi1[k].real,
                            grad_psi1[k].imag * psi1[k].imag)
                    for k in range(min(len(grad_psi1), len(psi1)))]
        self.h1.update(overlap1, lr)

        # Backprop through ym1
        self.ym1.update(psi0, grad_psi1, lr)

    def train_step(self, context_vecs, target_idx, lr=0.005):
        """One complete SMNNIP training step."""
        probs, psi0, psi1, psi2, logits = self.forward(context_vecs)
        loss      = self.cross_entropy_loss(probs, target_idx)
        violation, j0, j1, j2 = self.noether_check(psi0, psi1, psi2)
        self.backward(psi0, psi1, psi2, logits, probs, target_idx, lr)
        return loss, violation, probs

    def uncertainty_bound(self):
        """ΔSemantic · ΔPhase >= hbar_NN / 2"""
        return self.C.hbar_nn / 2.0

    def diagnostics(self):
        print(f"\n  ── Layer 1 (ℂ) Field Diagnostics ──")
        print(f"  alpha_NN (U(1))     = {self.C.alpha_nn:.6f}")
        print(f"  hbar_NN             = {self.C.hbar_nn:.4f}")
        print(f"  ΔSemantic·ΔPhase >= {self.uncertainty_bound():.4f}")
        print(f"  H1 VEV distance     = {self.h1.vev_distance():.4f}")
        print(f"  H2 VEV distance     = {self.h2.vev_distance():.4f}")
        print(f"  H1 phase angle      = {self.h1.phase_angle():.4f} rad")
        print(f"  H2 phase angle      = {self.h2.phase_angle():.4f} rad")
        print(f"  YM1 field strength  = {self.ym1.field_strength():.4f}")
        print(f"  YM2 field strength  = {self.ym2.field_strength():.4f}")
        BENCH.record("H1 VEV distance final", self.h1.vev_distance())
        BENCH.record("H2 VEV distance final", self.h2.vev_distance())
        BENCH.record("YM1 field strength final", self.ym1.field_strength())


# ---------------------------------------------------------------------------
# TRAINING LOOP
# ---------------------------------------------------------------------------

def build_training_data(text, vocab, context_len):
    char_to_idx = {c: i for i, c in enumerate(sorted(set(text)))}
    data = []
    for i in range(len(text) - context_len):
        ctx    = text[i:i+context_len]
        target = text[i+context_len]
        ctx_vecs = []
        for c in ctx:
            v = [0.0] * vocab
            v[char_to_idx.get(c, 0)] = 1.0
            ctx_vecs.append(v)
        data.append((ctx_vecs, char_to_idx.get(target, 0)))
    return data


def train(network, text, epochs=20, lr=0.005, cap=400):
    vocab       = network.vocab_size
    char_to_idx = {c: i for i, c in enumerate(sorted(set(text)))}
    data        = build_training_data(text, vocab, network.context_len)

    print(f"\n  Training samples: {len(data)}")
    print(f"  Uncertainty bound: {network.uncertainty_bound():.4f}")
    print(f"  Alpha_NN (U(1)):   {network.C.alpha_nn:.6f}")
    print()

    t0 = time.time()
    for epoch in range(epochs):
        random.shuffle(data)
        total_loss = 0.0
        total_viol = 0.0
        n = 0

        for ctx_vecs, tgt in data[:cap]:
            loss, viol, _ = network.train_step(ctx_vecs, tgt, lr)
            total_loss += loss
            total_viol += viol
            n += 1

        avg_loss = total_loss / max(n, 1)
        avg_viol = total_viol / max(n, 1)
        vev_d    = (network.h1.vev_distance() + network.h2.vev_distance()) / 2
        phase    = network.h1.phase_angle()

        network.loss_history.append(avg_loss)
        network.noether_violations.append(avg_viol)
        network.vev_distances.append(vev_d)
        network.phase_history.append(phase)

        status = "⚠ violation" if avg_viol > 0.1 else "✓ conserved"
        print(f"  Epoch {epoch+1:3d}/{epochs}"
              f"  loss={avg_loss:.4f}"
              f"  Noether={avg_viol:.4f} {status}"
              f"  VEV_dist={vev_d:.4f}"
              f"  phase={phase:.3f}rad")

    elapsed = time.time() - t0
    BENCH.record("Training time (Layer 1)", elapsed, "s")
    BENCH.record("Final loss (Layer 1)", network.loss_history[-1])
    BENCH.record("Final Noether violation", network.noether_violations[-1])
    network.diagnostics()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == '__main__':

    print("=" * 60)
    print("  SMNNIP Layer 1 — Complex Algebra (ℂ)")
    print("  Standard Model of Neural Network Information Propagation")
    print("  Algebra: ℂ (complex, dim=2)")
    print("  Layer:   Semantic (token relationships)")
    print("  Gauge:   U(1) — electromagnetic analog")
    print("=" * 60)

    training_text = (
        "the quick brown fox jumps over the lazy dog. "
        "pack my box with five dozen liquor jugs. "
        "how vexingly quick daft zebras jump. "
        "the five boxing wizards jump quickly. "
        "sphinx of black quartz judge my vow. "
        "characters form tokens tokens form meaning. "
        "real algebra at the base complex above it. "
        "quaternions for skills octonions for reasoning. "
        "the higgs field gives mass to representations. "
        "noether conservation holds at every boundary. "
        "complex phase encodes semantic relationships. "
        "u1 symmetry is the simplest gauge structure. "
        "wirtinger derivatives generalize real gradients. "
    ) * 5

    vocab_size = len(set(training_text))
    print(f"\n  Training text:  {len(training_text)} characters")
    print(f"  Vocabulary:     {vocab_size} characters")

    C   = SMNNIPConstantsC(hbar_nn=0.05, mu_sq=0.4, lam=0.1, g=0.01)
    print(f"\n  {C}")

    BENCH.record("vocab_size", vocab_size)

    net = SMNNIPLayer1Network(
        vocab_size  = vocab_size,
        hidden_dim  = 32,
        context_len = 4,
        constants   = C
    )

    train(net, training_text, epochs=20, lr=0.005, cap=300)

    BENCH.report()

    print("=" * 60)
    print("  Layer 1 (ℂ) training complete.")
    print(f"  Final loss:            {net.loss_history[-1]:.4f}")
    print(f"  Uncertainty bound:     {net.uncertainty_bound():.4f}")
    print(f"  Noether (final):       {net.noether_violations[-1]:.4f}")
    print(f"  Higgs VEV distance:    {net.vev_distances[-1]:.4f}")
    print(f"  U(1) phase committed:  {net.phase_history[-1]:.4f} rad")
    print("=" * 60)
