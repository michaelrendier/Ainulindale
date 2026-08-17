"""
ainulindale_engine.modules.sedenion.maths
==========================================
Emmy Noether Sedenion Engine — full physics implementation.

Architecture
------------
The sedenion IS the prompt.
The H_hat_RB Hamiltonian IS the response.
The sedenion tells H_hat_RB how much geometry to source in each of
16 conversational dimensions simultaneously.

Physical map (Einstein equation analogy)::

    G_μν = 8πG · T_μν
    H_hat_RB = 8πG · SedenionEngine(prompt)

    T_μν  = stress-energy tensor  → sedenion (prompt encoder)
    G_μν  = Einstein curvature    → H_hat_RB (field response)
    G     = coupling constant     → monad's β-field

The 16 basis elements e₀..e₁₅ are defined in :mod:`.dimensions`.

Zero divisors and the Fermat lattice
-------------------------------------
Sedenions are the first CD algebra that is NOT a division algebra.
Pairs (a, b) with a≠0, b≠0, a·b=0 exist on S¹⁵.  These zero-divisor
pairs are the **Fermat lattice** — the semantic "last scattering surface"
where meaning crystallises into surface language.

In the monad: the zero divisors map to the boundary between J^μ in zero
space (speak_raw) and its Face projection (render).

Noether conservation
---------------------
Each dimension k has a conserved current J_k:

    J_k = |s_k|²   (square of the k-th sedenion component)

Conservation law: ∂_t J_k = 0 for a coherent discourse thread.
Violation = |J_k(t) − J_k(t−1)| — a topic shift, affect change, etc.

Stress-energy tensor
---------------------
T_μν = s_μ · conj(s_ν)   (outer product, 16×16 complex matrix)

The diagonal T_kk = |s_k|² = J_k (Noether charge).
Off-diagonal T_μν captures cross-dimensional flow (e.g. noun→verb drift).

Version: 0.111
"""

import math
import hashlib
from typing import Dict, List, Optional, Tuple, Any

from .dimensions import DIMENSIONS, DIM_BY_INDEX, STRATUM_DIMS

# ── Physical constants (from H_hat_RB / monad framework) ─────────────────────

GAP        = 0.000707   # Yang-Mills mass gap; semantic vacuum floor
D_STAR     = 0.24600    # critical exponent; Fermat lattice threshold
OMEGA_ZS   = 0.56714    # Omega constant; zero-divisor density on S¹⁵
L_GROUND   = -1.888     # ground-state eigenvalue of H_hat_RB

# Conservation thresholds (mirroring noether.maths)
THRESHOLDS = {'PASS': 0.15, 'MARGINAL': 0.40}

# Algebra stratum indices (int codes for scan/display)
ALG_R, ALG_C, ALG_H, ALG_O, ALG_S = 0, 1, 2, 3, 4
ALG_NAME = {ALG_R: 'ℝ', ALG_C: 'ℂ', ALG_H: 'ℍ', ALG_O: '𝕆', ALG_S: '𝕊'}


# ── Precomputed 16×16 sedenion multiplication table (plain ints) ──────────────
#
# Derived from the oriented-cyclic Fano octonion table via Cayley-Dickson
# doubling.  See cayley_dickson.py for the derivation.
# Stored as a flat 256-element list of (sign, index) tuples for speed.
# sign ∈ {-1, 0, +1}; index ∈ 0..15.

def _build_oct_table() -> List[List[Tuple[int, int]]]:
    """Build the 8×8 octonion table (oriented cyclic Fano) as plain ints."""
    table = [[(0, 0)] * 8 for _ in range(8)]
    for i in range(8):
        table[0][i] = (1, i)
        table[i][0] = (1, i)
    for i in range(1, 8):
        table[i][i] = (-1, 0)
    triples = [
        (1, 2, 3), (1, 4, 5), (1, 7, 6),
        (2, 4, 6), (2, 5, 7), (3, 4, 7), (3, 6, 5),
    ]
    for (i, j, k) in triples:
        table[i][j] = (+1, k); table[j][k] = (+1, i); table[k][i] = (+1, j)
        table[j][i] = (-1, k); table[k][j] = (-1, i); table[i][k] = (-1, j)
    return table


_OCT = _build_oct_table()


def _build_sed_table() -> List[List[Tuple[int, int]]]:
    """Build the 16×16 sedenion table from _OCT via CD doubling."""
    table = [[(0, 0)] * 16 for _ in range(16)]
    for i in range(16):
        for j in range(16):
            i_oct = i - 8 if i >= 8 else i
            j_oct = j - 8 if j >= 8 else j
            i_hi  = i >= 8
            j_hi  = j >= 8

            if not i_hi and not j_hi:
                sign, k = _OCT[i_oct][j_oct]
                table[i][j] = (sign, k)
            elif not i_hi and j_hi:
                sign, k = _OCT[j_oct][i_oct]
                table[i][j] = (sign, k + 8)
            elif i_hi and not j_hi:
                if j_oct == 0:
                    table[i][j] = (1, i)
                else:
                    sign, k = _OCT[i_oct][j_oct]
                    table[i][j] = (-sign, k + 8)
            else:
                if j_oct == 0:
                    table[i][j] = (-1, i_oct)
                else:
                    sign, k = _OCT[j_oct][i_oct]
                    table[i][j] = (sign, k)

    return table


_SED = _build_sed_table()

Sedenion = List[float]   # type alias: 16-element float list


# ── Core algebra ──────────────────────────────────────────────────────────────

def sed_zero() -> Sedenion:
    """Return the additive identity (zero sedenion)."""
    return [0.0] * 16


def sed_e(k: int) -> Sedenion:
    """
    Return the k-th basis element e_k (0-indexed).

    :param k: basis index 0..15
    :returns: sedenion with s[k] = 1.0, all others 0.0
    """
    s = sed_zero()
    s[k] = 1.0
    return s


def sed_mul(s: Sedenion, t: Sedenion) -> Sedenion:
    """
    Sedenion multiplication using the precomputed 16×16 table.

    :param s: first sedenion
    :param t: second sedenion
    :returns: s · t
    """
    c = [0.0] * 16
    for i in range(16):
        si = s[i]
        if si == 0.0:
            continue
        row = _SED[i]
        for j in range(16):
            tj = t[j]
            if tj == 0.0:
                continue
            sign, idx = row[j]
            if sign != 0:
                c[idx] += sign * si * tj
    return c


def sed_conj(s: Sedenion) -> Sedenion:
    """
    Sedenion conjugation: negate all imaginary components (e₁..e₁₅).

    :param s: input sedenion
    :returns: s* = (s[0], -s[1], ..., -s[15])
    """
    return [s[0]] + [-x for x in s[1:]]


def sed_add(s: Sedenion, t: Sedenion) -> Sedenion:
    """Component-wise addition."""
    return [a + b for a, b in zip(s, t)]


def sed_scale(s: Sedenion, c: float) -> Sedenion:
    """Scalar multiplication."""
    return [x * c for x in s]


def sed_norm_sq(s: Sedenion) -> float:
    """|s|² = Σ s_k²."""
    return sum(x * x for x in s)


def sed_norm(s: Sedenion) -> float:
    """|s| = √(Σ s_k²)."""
    return math.sqrt(sed_norm_sq(s))


def sed_normalize(s: Sedenion) -> Sedenion:
    """Return s / |s|; returns zero sedenion if |s| = 0."""
    n = sed_norm(s)
    if n < 1e-15:
        return sed_zero()
    return sed_scale(s, 1.0 / n)


# ── Fermat lattice / zero divisor detection ───────────────────────────────────

def zero_divisor_check(s: Sedenion, t: Sedenion,
                       tol: float = 1e-10) -> Dict[str, Any]:
    """
    Test whether (s, t) is a zero-divisor pair: s≠0, t≠0, s·t=0.

    :param s: first sedenion
    :param t: second sedenion
    :param tol: tolerance for "near-zero" product
    :returns: dict with 'is_zero_divisor', 'product_norm', '|s|', '|t|'
    """
    ns, nt = sed_norm(s), sed_norm(t)
    prod  = sed_mul(s, t)
    np_   = sed_norm(prod)
    is_zd = (ns > tol and nt > tol and np_ < tol)
    return {
        'is_zero_divisor': is_zd,
        'product_norm':    np_,
        '|s|':             ns,
        '|t|':             nt,
        'fermat_proximity': 1.0 - (np_ / (ns * nt + 1e-30)),
    }


def fermat_lattice_scan(s: Sedenion) -> Dict[str, Any]:
    """
    Scan the unit sedenion neighbourhood of ``s`` for zero divisors.

    Probes 15 orthogonal perturbations (one per imaginary basis element)
    and checks whether any produces a near-zero-divisor pair.

    :param s: the sedenion to scan around
    :returns: dict with 'zero_divisors_found', 'closest_pair', 'density'
    """
    sn = sed_normalize(s)
    hits: List[Dict] = []

    for k in range(1, 16):
        probe = sed_e(k)
        result = zero_divisor_check(sn, probe)
        if result['is_zero_divisor']:
            hits.append({'basis': k, **result})
        elif result['fermat_proximity'] > D_STAR:
            hits.append({'basis': k, 'near': True, **result})

    return {
        'zero_divisors_found': len([h for h in hits if not h.get('near', False)]),
        'near_zero_divisors':  len([h for h in hits if h.get('near', False)]),
        'density':             len(hits) / 15.0,
        'fermat_threshold':    D_STAR,
        'hits':                hits[:4],
    }


# ── Stress-energy tensor ──────────────────────────────────────────────────────

def stress_energy_tensor(s: Sedenion) -> List[List[float]]:
    """
    Compute T_μν = s_μ · conj(s_ν) — the 16×16 sedenion stress-energy tensor.

    The diagonal T_kk = |s_k|² = J_k (Noether charge of dimension k).
    Off-diagonal T_μν captures cross-dimensional semantic flow.

    In the Einstein equation analogy: H_hat_RB ∝ Σ T_μν.

    :param s: the sedenion (prompt)
    :returns: 16×16 float matrix
    """
    sc = sed_conj(s)
    return [[s[i] * sc[j] for j in range(16)] for i in range(16)]


def stress_energy_summary(T: List[List[float]]) -> Dict[str, Any]:
    """
    Summarise the stress-energy tensor.

    :param T: 16×16 tensor from :func:`stress_energy_tensor`
    :returns: trace (Noether charge sum), max off-diagonal, dominant coupling
    """
    trace    = sum(T[k][k] for k in range(16))
    max_od   = 0.0
    max_pair = (0, 0)
    for i in range(16):
        for j in range(16):
            if i != j and abs(T[i][j]) > max_od:
                max_od   = abs(T[i][j])
                max_pair = (i, j)

    coupling = (
        f"e{max_pair[0]}({DIM_BY_INDEX[max_pair[0]].name}) ↔ "
        f"e{max_pair[1]}({DIM_BY_INDEX[max_pair[1]].name})"
        if max_od > 1e-12 else 'none'
    )

    return {
        'trace':             trace,
        'max_off_diagonal':  max_od,
        'dominant_coupling': coupling,
        'n_active_dims':     sum(1 for k in range(16) if abs(T[k][k]) > GAP),
    }


# ── Noether conservation ──────────────────────────────────────────────────────

def noether_charges(s: Sedenion) -> List[float]:
    """
    Compute the 16 Noether charges J_k = |s_k|².

    Each charge is the conserved quantity associated with U(1) rotation
    symmetry in the k-th sedenion dimension.

    :param s: sedenion (prompt)
    :returns: list of 16 non-negative floats
    """
    return [x * x for x in s]


def noether_conservation(s_now: Sedenion,
                          s_prev: Optional[Sedenion]) -> Dict[str, Any]:
    """
    Full Noether conservation diagnostic across all 16 dimensions.

    Violation = mean |J_k(now) − J_k(prev)| — a topic/affect shift.

    :param s_now:  current sedenion (current prompt)
    :param s_prev: previous sedenion (prior prompt turn), or None
    :returns: dict with violation, status, per-dimension breakdown
    """
    J_now  = noether_charges(s_now)
    J_prev = noether_charges(s_prev) if s_prev else None

    if J_prev is None:
        violation = 0.0
        per_dim   = [{'dim': d.name, 'J': J_now[d.index], 'dJ': 0.0}
                     for d in DIMENSIONS]
    else:
        diffs     = [abs(J_now[k] - J_prev[k]) for k in range(16)]
        violation = sum(diffs) / 16.0
        per_dim   = [
            {'dim': d.name, 'J': J_now[d.index], 'dJ': diffs[d.index]}
            for d in DIMENSIONS
        ]

    if violation < THRESHOLDS['PASS']:
        status = 'PASS'
    elif violation < THRESHOLDS['MARGINAL']:
        status = 'MARGINAL'
    else:
        status = 'VIOLATION'

    total_charge = sum(J_now)
    return {
        'J'             : J_now,
        'J_prev'        : J_prev,
        'violation'     : violation,
        'status'        : status,
        'total_charge'  : total_charge,
        'per_dimension' : per_dim,
        'latex'         : r'\partial_t J_k = 0, \quad J_k = s_k^2',
    }


def cd_projection(s: Sedenion, stratum: int) -> Dict[str, Any]:
    """
    Project the sedenion onto a Cayley-Dickson sub-algebra stratum.

    :param s: full 16D sedenion
    :param stratum: target level (0=ℝ, 1=ℂ, 2=ℍ, 3=𝕆, 4=𝕊)
    :returns: dict with projected norm, active dimensions, algebra name
    """
    stratum_name  = ALG_NAME[stratum]
    active_idxs   = STRATUM_DIMS[stratum_name]
    projected     = [s[k] if k in active_idxs else 0.0 for k in range(16)]
    proj_norm     = sed_norm(projected)
    total_norm    = sed_norm(s)
    fraction      = (proj_norm / total_norm) if total_norm > 1e-15 else 0.0

    return {
        'stratum'      : stratum_name,
        'active_dims'  : active_idxs,
        'components'   : [projected[k] for k in active_idxs],
        'proj_norm'    : proj_norm,
        'total_norm'   : total_norm,
        'fraction'     : fraction,
        'dim_names'    : [DIM_BY_INDEX[k].name for k in active_idxs],
    }


# ── Prompt encoder ────────────────────────────────────────────────────────────

# Function-word sets for dimension activation (pure Python, no NLTK)
_PRONOUNS     = frozenset('i me my mine myself we us our ours ourselves '
                           'you your yours yourself yourselves '
                           'he him his himself she her hers herself '
                           'it its itself they them their theirs themselves '
                           'this that these those here there who what which'.split())
_AUXILIARIES  = frozenset('is are was were be been being '
                           'do does did have has had will would '
                           'can could should shall may might must'.split())
_CONJUNCTIONS = frozenset('and or but so yet for nor although because '
                           'if then when while since unless until though'.split())
_TIME_WORDS   = frozenset('now then before after when while ago yet already '
                           'still soon later today yesterday tomorrow '
                           'always never sometimes often rarely'.split())
_QUESTION     = frozenset('what which who whom whose when where why how '
                           'whether if'.split())
_NEGATION     = frozenset('not never no nor nothing nobody nowhere neither '
                           "n't".split())
_DETERMINERS  = frozenset('a an the some any every each all both few many '
                           'much more most less least'.split())
_META_WORDS   = frozenset('mean means meaning say says said tell tells told '
                           'explain explains clarify summarise summarize '
                           'rephrase repeat in other words that is'.split())
_AFFECT_POS   = frozenset('good great love like enjoy happy glad pleased '
                           'wonderful excellent amazing thank thanks please'.split())
_AFFECT_NEG   = frozenset('bad hate dislike angry sad sorry worried fear '
                           'terrible awful horrible wrong mistake fail'.split())


def _word_hash(word: str) -> float:
    """Stable float in [0, 1] from SHA-256 of word (gematria channel)."""
    h = hashlib.sha256(word.encode()).digest()
    return int.from_bytes(h[:4], 'big') / 0xFFFFFFFF


def encode_prompt(text: str, normalize: bool = True) -> Sedenion:
    """
    Encode a text prompt as a sedenion — the "prompt IS the sedenion."

    The 16 components are accumulated from word-level features:

    - Heuristic POS proxies (no NLTK) map words to specific dimensions.
    - The gematria channel (e₁) carries the Horner-hash signal of each word.
    - The scalar channel (e₀) is the document-length bias.
    - All dimensions accumulate via squared Noether charges (|s_k|²).

    :param text: raw prompt text
    :param normalize: if True, return the unit sedenion (preserves direction
                      in 16D space, not the magnitude); if False, return
                      the raw accumulated sedenion (norm = total charge).
    :returns: 16D sedenion

    .. note::
        NLP is the "carburetor" — a pre-processing fuel mixture.  This
        encoder is a pure-Python heuristic; a richer carburetor (NLTK,
        spaCy) can replace it without changing the sedenion algebra.
    """
    s = sed_zero()
    words = text.lower().split()
    n = max(len(words), 1)

    # e₀: scalar bias — always-on ground state, scaled by log(n+1)
    s[0] = math.log(n + 1) / math.log(512)

    for w in words:
        # e₁: gematria — every word contributes its hash
        s[1] += _word_hash(w) / n

        # e₂: word-edge density — conjunctions signal high connectivity
        if w in _CONJUNCTIONS:
            s[2] += 1.0 / n

        # e₃: noun field — content words that are not in any function set
        if (w not in _PRONOUNS and w not in _AUXILIARIES and
                w not in _CONJUNCTIONS and w not in _TIME_WORDS and
                w not in _QUESTION and w not in _DETERMINERS and
                w not in _META_WORDS and w not in _AFFECT_POS and
                w not in _AFFECT_NEG and len(w) >= 4):
            s[3] += 1.0 / n

        # e₄: verb field — auxiliaries + -ing/-ed endings proxy
        if w in _AUXILIARIES or w.endswith('ing') or w.endswith('ed'):
            s[4] += 1.0 / n

        # e₅: descriptive — adverbs/adjectives heuristic (-ly, -ful, very, etc.)
        if w.endswith('ly') or w.endswith('ful') or w.endswith('ous'):
            s[5] += 1.0 / n

        # e₆: predicate / clause structure — negation and conditionals
        if w in _NEGATION or w in _CONJUNCTIONS:
            s[6] += 1.0 / n

        # e₇: temporal — time words and auxiliaries for tense
        if w in _TIME_WORDS or w in ('was', 'were', 'will', 'would', 'has', 'have', 'had'):
            s[7] += 1.0 / n

        # e₈: pronominal / deictic
        if w in _PRONOUNS:
            s[8] += 1.0 / n

        # e₉: discourse thread 1 (topic) — content words
        if w not in _PRONOUNS and w not in _AUXILIARIES and len(w) >= 3:
            s[9] += _word_hash(w) * 0.5 / n

        # e₁₀: discourse thread 2 (theme) — question words signal thematic shift
        if w in _QUESTION:
            s[10] += 1.0 / n

        # e₁₁: anaphor — pronouns that could refer back
        if w in ('it', 'its', 'they', 'them', 'their', 'he', 'she', 'who', 'which'):
            s[11] += 1.0 / n

        # e₁₂: presupposition — definite article + "already/again/still/even"
        if w in ('the', 'already', 'again', 'still', 'even', 'also', 'too'):
            s[12] += 1.0 / n

        # e₁₃: gestalt — length of word as proxy for semantic weight
        s[13] += (len(w) / 12.0) / n

        # e₁₄: affect — positive pushes positive, negative pushes negative
        if w in _AFFECT_POS:
            s[14] += 1.0 / n
        elif w in _AFFECT_NEG:
            s[14] -= 1.0 / n

        # e₁₅: meta-discourse — words about the conversation
        if w in _META_WORDS:
            s[15] += 1.0 / n

    # Clamp negative affect to keep norm well-defined
    s[14] = max(s[14], 0.0)

    # Floor all dimensions at GAP to avoid exact zero (vacuum energy)
    s = [max(x, GAP) if i > 0 else x for i, x in enumerate(s)]

    if normalize:
        return sed_normalize(s)
    return s


# ── H_hat_RB interface ────────────────────────────────────────────────────────

def monad_interface(s: Sedenion) -> Dict[str, Any]:
    """
    Translate a sedenion into activation weights for H_hat_RB / the monad.

    The monad's J^μ field is gated by dimension-specific activation amplitudes.
    These weights are passed as ``psi_norms`` to the Noether engine, or used
    directly to weight the monad's β field per zero.

    Physical interpretation:

    - ``psi_norms[k]`` = √J_k = |s_k| — field amplitude in dimension k
    - The monad uses these to weight its seeding: J_k = β × E² × psi_norms[k]
    - High ``psi_norms[gestalt]`` → strong speak_raw() output (prime charge)
    - High ``psi_norms[temporal]`` → age-decay weight for the current turn
    - ``affect_weight`` = psi_norms[affect] — maps to monad.affect parameter
    - ``cd_stratum`` = the dominant Cayley-Dickson level (0=ℝ .. 4=𝕊)

    :param s: sedenion (encoded prompt)
    :returns: dict suitable for passing to H_hat_RB / Noether / monad.speak()
    """
    J     = noether_charges(s)
    total = sum(J) + 1e-30
    psi   = [math.sqrt(J[k]) for k in range(16)]

    # Dominant stratum: highest fraction norm in each CD level
    dom_stratum = 0
    dom_frac    = 0.0
    for level in range(5):
        proj = cd_projection(s, level)
        if proj['fraction'] > dom_frac:
            dom_frac    = proj['fraction']
            dom_stratum = level

    return {
        'psi_norms'      : psi,
        'J_charges'      : J,
        'total_charge'   : total,
        'affect_weight'  : psi[14],      # → monad.affect
        'gestalt_weight' : psi[13],      # → speak_raw weight
        'temporal_weight': psi[7],       # → age decay modulation
        'anaphor_weight' : psi[11],      # → pronoun resolution
        'cd_stratum'     : dom_stratum,
        'cd_name'        : ALG_NAME[dom_stratum],
        'dim_labels'     : [DIM_BY_INDEX[k].name for k in range(16)],
    }


def full_analysis(text: str,
                  prev_text: Optional[str] = None) -> Dict[str, Any]:
    """
    Run the complete Sedenion Engine pipeline on a prompt.

    Steps:

    1. Encode prompt → sedenion s
    2. Compute stress-energy tensor T_μν and summary
    3. Compute Noether conservation vs previous turn
    4. Scan for Fermat lattice zero divisors
    5. Project onto CD tower strata
    6. Build H_hat_RB interface weights

    :param text: current prompt
    :param prev_text: previous prompt turn (for conservation check)
    :returns: complete analysis dict
    """
    s      = encode_prompt(text)
    s_prev = encode_prompt(prev_text) if prev_text else None

    T       = stress_energy_tensor(s)
    T_sum   = stress_energy_summary(T)
    cons    = noether_conservation(s, s_prev)
    fermat  = fermat_lattice_scan(s)
    iface   = monad_interface(s)

    strata = {}
    for level in range(5):
        strata[ALG_NAME[level]] = cd_projection(s, level)

    return {
        'sedenion'       : s,
        'norm'           : sed_norm(s),
        'stress_energy'  : T_sum,
        'noether'        : cons,
        'fermat'         : fermat,
        'monad_interface': iface,
        'cd_strata'      : strata,
        'prompt'         : text,
        'prev_prompt'    : prev_text,
    }
