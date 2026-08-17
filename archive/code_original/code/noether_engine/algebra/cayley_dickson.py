"""
noether_engine.algebra.cayley_dickson — the Cayley-Dickson algebra tower.

Provides multiplication operations for:
  ℝ  (real, dim 1)
  ℂ  (complex, dim 2)
  ℍ  (quaternions, dim 4)
  𝕆  (octonions, dim 8)
  𝕊  (sedenions, dim 16)

All four are normed division algebras — the only four (Hurwitz's theorem).
The Cayley-Dickson construction builds each from the one below by doubling:
if A has multiplication (a, b)(c, d) = (ac - d*b, da + bc*), then the
doubled algebra is (A, A) with element pairs.

Sedenions (𝕊, 16D) are the next Cayley-Dickson step beyond octonions.
They are neither a division algebra nor alternative — zero divisors exist
on S¹⁵, forming the Fermat lattice (the "last scattering surface" of
semantic crystallisation in the monad framework).  The 16 basis elements
{e₀..e₁₅} map to 16 conversational dimensions; the 256-entry product
catalog is the Emmy Noether Sedenion stress-energy tensor T_μν.

Octonions specifically admit 480 distinct Fano-plane sign conventions
(Baez 2002). This module uses the **oriented cyclic** convention:

    e_1 e_2 = e_3,  e_1 e_4 = e_5,  e_1 e_6 = e_7,
    e_2 e_4 = e_6,  e_2 e_7 = e_5,  e_3 e_4 = e_7,
    e_3 e_5 = e_6.

All other nonzero products follow from anticommutativity e_i e_j = -e_j e_i.

The convention is set globally via the `octonion_fano` sub-switch (default
'oriented_cyclic'). 'alternate' and 'custom' settings are available for
researchers using a different Fano convention.

References:
  - Baez, J.C. (2002). The octonions. Bull. Amer. Math. Soc. 39(2).
  - Dixon, G.M. (1994). Division Algebras: Octonions, Quaternions,
    Complex Numbers and the Algebraic Design of Physics. Kluwer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

import sympy as sp


# ═══════════════════════════════════════════════════════════════════════════
#  REAL (ℝ)
# ═══════════════════════════════════════════════════════════════════════════

def real_multiplication(a: Sequence[sp.Expr], b: Sequence[sp.Expr]) -> List[sp.Expr]:
    """Real multiplication: just numeric product."""
    assert len(a) == 1 and len(b) == 1
    return [a[0] * b[0]]


# ═══════════════════════════════════════════════════════════════════════════
#  COMPLEX (ℂ)
# ═══════════════════════════════════════════════════════════════════════════

def complex_multiplication(
    a: Sequence[sp.Expr],
    b: Sequence[sp.Expr],
) -> List[sp.Expr]:
    """
    (a0 + a1 i)(b0 + b1 i) = (a0 b0 - a1 b1) + (a0 b1 + a1 b0) i.
    """
    assert len(a) == 2 and len(b) == 2
    return [
        a[0] * b[0] - a[1] * b[1],
        a[0] * b[1] + a[1] * b[0],
    ]


def complex_i_generator() -> sp.Matrix:
    """
    Left-multiplication matrix for the imaginary unit i acting on ℂ vectors.
    i · (a0, a1) = (-a1, a0).
    """
    return sp.Matrix([
        [0, -1],
        [1,  0],
    ])


# ═══════════════════════════════════════════════════════════════════════════
#  QUATERNIONS (ℍ)
# ═══════════════════════════════════════════════════════════════════════════
# Basis: 1, i, j, k    with  i² = j² = k² = ijk = -1,
#                           ij = k,  jk = i,  ki = j,
#                           ji = -k, kj = -i, ik = -j.
# Components: (a0, a1, a2, a3) = a0·1 + a1·i + a2·j + a3·k.

def quaternion_multiplication(
    a: Sequence[sp.Expr],
    b: Sequence[sp.Expr],
) -> List[sp.Expr]:
    """
    Hamilton quaternion multiplication.
    Verified: i²=j²=k²=ijk=-1, ij=k, jk=i, ki=j.
    """
    assert len(a) == 4 and len(b) == 4
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return [
        a0*b0 - a1*b1 - a2*b2 - a3*b3,
        a0*b1 + a1*b0 + a2*b3 - a3*b2,
        a0*b2 - a1*b3 + a2*b0 + a3*b1,
        a0*b3 + a1*b2 - a2*b1 + a3*b0,
    ]


def quaternion_generators() -> Tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    """
    Left-multiplication matrices for i, j, k acting on ℍ vectors (a0,a1,a2,a3).
    These are the 4x4 real-matrix generators of SU(2) ⊂ ℍ^* acting on itself.
    """
    # L_i : i · (a0,a1,a2,a3) = -a1, a0, a3, -a2 ? let's compute:
    #   i · (a0 + a1 i + a2 j + a3 k) = a0 i - a1 + a2 k - a3 j
    #     = -a1 · 1 + a0 · i - a3 · j + a2 · k
    L_i = sp.Matrix([
        [0, -1,  0,  0],
        [1,  0,  0,  0],
        [0,  0,  0, -1],
        [0,  0,  1,  0],
    ])
    # L_j : j · (a0 + a1 i + a2 j + a3 k) = a0 j - a1 k - a2 + a3 i
    #     = -a2 · 1 + a3 · i + a0 · j - a1 · k
    L_j = sp.Matrix([
        [0,  0, -1,  0],
        [0,  0,  0,  1],
        [1,  0,  0,  0],
        [0, -1,  0,  0],
    ])
    # L_k : k · (a0 + a1 i + a2 j + a3 k) = a0 k + a1 j - a2 i - a3
    #     = -a3 · 1 - a2 · i + a1 · j + a0 · k
    L_k = sp.Matrix([
        [0,  0,  0, -1],
        [0,  0, -1,  0],
        [0,  1,  0,  0],
        [1,  0,  0,  0],
    ])
    return (L_i, L_j, L_k)


# ═══════════════════════════════════════════════════════════════════════════
#  OCTONIONS (𝕆)
# ═══════════════════════════════════════════════════════════════════════════
# Basis: 1, e_1, e_2, e_3, e_4, e_5, e_6, e_7.
# Each e_i² = -1 (for i=1..7).
# Anticommutative: e_i e_j = -e_j e_i for i ≠ j.
# Oriented cyclic Fano convention:
#   e_1 e_2 = e_3,  e_1 e_4 = e_5,  e_1 e_6 = e_7,
#   e_2 e_4 = e_6,  e_2 e_7 = e_5,  e_3 e_4 = e_7,
#   e_3 e_5 = e_6.
# Other products by anticommutativity and Fano closure.
# Indexing: components a[0] is scalar, a[1..7] are coefficients of e_1..e_7.


def _octonion_multiplication_table() -> List[List[Tuple[int, int]]]:
    """
    Build the 8x8 octonion multiplication table in the oriented-cyclic Fano
    convention.

    Returns a 8x8 list where table[i][j] = (sign, index) means e_i · e_j
    = sign * e_{index}  (sign ∈ {-1, 0, +1}; 0 is only for e_0·... which is
    handled separately as scalar).

    Actually, we store:
      table[i][j] = (sign, index)
    for i, j ∈ {1,...,7} giving e_i·e_j. e_0 = 1 is the scalar identity and
    is handled outside this table.
    """
    # Initialize: diagonal is -1 * e_0 (but we encode as (-1, 0))
    table: List[List[Tuple[int, int]]] = [
        [(0, 0) for _ in range(8)] for _ in range(8)
    ]
    # e_0 is the identity: e_0·e_i = e_i, e_i·e_0 = e_i
    for i in range(8):
        table[0][i] = (1, i)
        table[i][0] = (1, i)
    # Diagonals: e_i · e_i = -1 (for i >= 1)
    for i in range(1, 8):
        table[i][i] = (-1, 0)

    # Define the 7 positive triples in oriented cyclic convention:
    # (i, j, k) means e_i · e_j = e_k, with cyclic permutations giving same.
    triples = [
        (1, 2, 3),
        (1, 4, 5),
        (1, 7, 6),   # e_1 e_7 = -e_6 in oriented-cyclic; using (1,6,7) with sign below
        (2, 4, 6),
        (2, 5, 7),
        (3, 4, 7),
        (3, 6, 5),
    ]
    # Encode each triple: e_i e_j = +e_k, e_j e_k = +e_i, e_k e_i = +e_j.
    # The opposite orderings give -.
    for (i, j, k) in triples:
        table[i][j] = (+1, k)
        table[j][k] = (+1, i)
        table[k][i] = (+1, j)
        table[j][i] = (-1, k)
        table[k][j] = (-1, i)
        table[i][k] = (-1, j)

    return table


_OCT_TABLE = _octonion_multiplication_table()


def octonion_multiplication(
    a: Sequence[sp.Expr],
    b: Sequence[sp.Expr],
) -> List[sp.Expr]:
    """
    Octonion multiplication in the oriented-cyclic Fano convention.

    Elements a, b are length-8 sequences:
      a = [a0, a1, a2, a3, a4, a5, a6, a7]
    with a0 the scalar part and a1..a7 the coefficients of e_1..e_7.

    Returns the product c = a·b as a length-8 list.
    """
    assert len(a) == 8 and len(b) == 8
    c: List[sp.Expr] = [sp.Integer(0) for _ in range(8)]
    for i in range(8):
        for j in range(8):
            sign, idx = _OCT_TABLE[i][j]
            if sign == 0:
                continue
            c[idx] += sign * a[i] * b[j]
    return [sp.expand(x) for x in c]


def octonion_generators() -> List[sp.Matrix]:
    """
    Left-multiplication matrices for e_1 through e_7 acting on 𝕆 vectors.
    Returns a list of 7 8x8 matrices.

    The SMNNIP framework uses these as the 7 generators of the G_2 algebra
    (the automorphism group of the octonions) acting on octonion-valued
    fields.
    """
    generators: List[sp.Matrix] = []
    for a in range(1, 8):
        M = sp.zeros(8, 8)
        for j in range(8):
            sign, idx = _OCT_TABLE[a][j]
            if sign != 0:
                M[idx, j] = sp.Integer(sign)
        generators.append(M)
    return generators


# ═══════════════════════════════════════════════════════════════════════════
#  UNIFIED INTERFACE
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CayleyDicksonAlgebra:
    """
    A single stratum of the Cayley-Dickson tower.

    :param label: ``'R'``, ``'C'``, ``'H'``, ``'O'``, or ``'S'``
    :param dim: 1, 2, 4, 8, or 16
    :param name: human-readable name
    """
    label: str
    dim: int
    name: str

    def multiply(self, a: Sequence[sp.Expr], b: Sequence[sp.Expr]) -> List[sp.Expr]:
        """
        Multiply two algebra elements.

        :param a: first element
        :param b: second element
        :returns: product a·b
        """
        if self.label == 'R':
            return real_multiplication(a, b)
        elif self.label == 'C':
            return complex_multiplication(a, b)
        elif self.label == 'H':
            return quaternion_multiplication(a, b)
        elif self.label == 'O':
            return octonion_multiplication(a, b)
        elif self.label == 'S':
            return sedenion_multiplication(a, b)
        else:
            raise ValueError(f"Unknown algebra label: {self.label}")

    def conjugate(self, a: Sequence[sp.Expr]) -> List[sp.Expr]:
        """
        Algebra conjugation: negate imaginary components.

        - ``R``: a* = a
        - ``C``: (a0, a1)* = (a0, -a1)
        - ``H``, ``O``, ``S``: (a0, a_1,...,a_n) → (a0, -a_1,..., -a_n)
        """
        if self.label == 'R':
            return list(a)
        return [a[0]] + [-ai for ai in a[1:]]

    def norm_squared(self, a: Sequence[sp.Expr]) -> sp.Expr:
        """|a|² = a · a* (scalar component of the product)."""
        conj_a = self.conjugate(a)
        prod = self.multiply(a, conj_a)
        return sp.expand(prod[0])

    def generators(self) -> List[sp.Matrix]:
        """Left-multiplication matrices for the imaginary basis elements."""
        if self.label == 'R':
            return []
        elif self.label == 'C':
            return [complex_i_generator()]
        elif self.label == 'H':
            return list(quaternion_generators())
        elif self.label == 'O':
            return octonion_generators()
        elif self.label == 'S':
            return sedenion_generators()
        else:
            raise ValueError(f"Unknown algebra label: {self.label}")


# ═══════════════════════════════════════════════════════════════════════════
#  SEDENIONS (𝕊)
# ═══════════════════════════════════════════════════════════════════════════
# 16-dimensional Cayley-Dickson algebra built by doubling 𝕆.
# Basis: e₀(scalar), e₁..e₇ (octonion imaginaries), e₈..e₁₅ (new imaginaries).
#
# CD doubling rule: (a,b)(c,d) = (ac − d̄b, da + bc̄)
# where ā is conjugation in 𝕆 (negate components 1-7).
#
# Key property: 𝕊 has zero divisors — it is NOT a division algebra.
# This is the algebraic signature of the Fermat lattice.
#
# Indexing: sedenion s = [s₀..s₁₅]; s[:8] is the left octonion (a),
#           s[8:] is the right octonion (b).

def _sedenion_table_from_oct() -> List[List[Tuple[int, int]]]:
    """
    Build the 16×16 sedenion multiplication table from :data:`_OCT_TABLE`.

    The construction follows CD doubling with basis split:

    - Index ``r ∈ [0,7]``  ↔ ``s_r = (e_r, 0)``  (left octonion half)
    - Index ``r ∈ [8,15]`` ↔ ``s_r = (0, e_{r-8})`` (right octonion half)

    Four cases for ``e_i · e_j``:

    1. ``i,j ∈ [0,7]``:   use octonion table directly → result in ``[0,7]``
    2. ``i ∈ [0,7], j ∈ [8,15]``:  ``(e_i,0)·(0,e_{j'}) = (0, e_{j'}·e_i)``
       → result in ``[8,15]``
    3. ``i ∈ [8,15], j ∈ [0,7]``:  ``(0,e_{i'})·(e_j,0) = (0, e_{i'}·ē_j)``
       (conjugate negates j≥1)  → result in ``[8,15]``
    4. ``i,j ∈ [8,15]``:  ``(0,e_{i'})·(0,e_{j'}) = (−ē_{j'}·e_{i'}, 0)``
       → result in ``[0,7]``

    :returns: 16×16 list of ``(sign, index)`` pairs.
    """
    table: List[List[Tuple[int, int]]] = [
        [(0, 0)] * 16 for _ in range(16)
    ]

    for i in range(16):
        for j in range(16):
            i_oct = i - 8 if i >= 8 else i
            j_oct = j - 8 if j >= 8 else j
            i_hi  = i >= 8
            j_hi  = j >= 8

            if not i_hi and not j_hi:
                # Case 1: (e_i, 0)·(e_j, 0) = (e_i·e_j, 0)
                sign, k = _OCT_TABLE[i_oct][j_oct]
                table[i][j] = (sign, k)

            elif not i_hi and j_hi:
                # Case 2: (e_i, 0)·(0, e_{j'}) = (0, e_{j'}·e_i)
                sign, k = _OCT_TABLE[j_oct][i_oct]
                table[i][j] = (sign, k + 8)

            elif i_hi and not j_hi:
                # Case 3: (0, e_{i'})·(e_j, 0) = (0, e_{i'}·ē_j)
                # ē_j = e_j for j=0; ē_j = -e_j for j≥1
                if j_oct == 0:
                    # e_{i'}·e_0 = e_{i'} → result (0, e_{i'}) = s_{i'+8} = s_i
                    table[i][j] = (1, i)
                else:
                    # e_{i'}·(-e_j) = -(e_{i'}·e_j)
                    sign, k = _OCT_TABLE[i_oct][j_oct]
                    table[i][j] = (-sign, k + 8)

            else:
                # Case 4: (0, e_{i'})·(0, e_{j'}) = (-ē_{j'}·e_{i'}, 0)
                # ē_{j'} = e_0 for j'=0; ē_{j'} = -e_{j'} for j'≥1
                if j_oct == 0:
                    # -e_0·e_{i'} = -e_{i'} → (-1, i_oct)
                    table[i][j] = (-1, i_oct)
                else:
                    # -(-e_{j'})·e_{i'} = e_{j'}·e_{i'}
                    sign, k = _OCT_TABLE[j_oct][i_oct]
                    table[i][j] = (sign, k)

    return table


_SED_TABLE = _sedenion_table_from_oct()


def sedenion_multiplication(
    a: Sequence[sp.Expr],
    b: Sequence[sp.Expr],
) -> List[sp.Expr]:
    """
    Sedenion multiplication built by Cayley-Dickson doubling of 𝕆.

    Elements ``a``, ``b`` are length-16 sequences:
    ``[a0..a7, a8..a15]`` where ``a[:8]`` is the left octonion half and
    ``a[8:]`` is the right octonion half.

    Uses the precomputed :data:`_SED_TABLE` for a single O(16²) pass.

    :param a: first sedenion (16 sympy expressions)
    :param b: second sedenion (16 sympy expressions)
    :returns: product c = a·b as a length-16 list.

    .. note::
        The sedenions are **not** a division algebra — the product of two
        non-zero elements can be zero.  The zero-divisor locus on S¹⁵ is
        the Fermat lattice.
    """
    assert len(a) == 16 and len(b) == 16
    c: List[sp.Expr] = [sp.Integer(0)] * 16
    for i in range(16):
        for j in range(16):
            sign, idx = _SED_TABLE[i][j]
            if sign == 0:
                continue
            c[idx] += sign * a[i] * b[j]
    return [sp.expand(x) for x in c]


def sedenion_generators() -> List[sp.Matrix]:
    """
    Left-multiplication matrices for e₁..e₁₅ acting on 𝕊 vectors (16D).

    Returns a list of 15 16×16 matrices — the generators of the algebra
    (not a Lie algebra, since 𝕊 is not alternative).

    :returns: list of 15 ``sp.Matrix`` objects.
    """
    gens: List[sp.Matrix] = []
    for a in range(1, 16):
        M = sp.zeros(16, 16)
        for j in range(16):
            sign, idx = _SED_TABLE[a][j]
            if sign != 0:
                M[idx, j] = sp.Integer(sign)
        gens.append(M)
    return gens


def left_multiplication_matrix(
    algebra_label: str,
    imag_unit_index: int,
) -> sp.Matrix:
    """
    Return the left-multiplication matrix :math:`L_{e_k}` where ``k = imag_unit_index`` (1-based).

    - ``'C'``, index 1: the single i-matrix (2×2).
    - ``'H'``, index 1-3: L_i, L_j, L_k (4×4).
    - ``'O'``, index 1-7: the octonion generators (8×8).
    - ``'S'``, index 1-15: the sedenion generators (16×16).

    :param algebra_label: one of ``'R'``, ``'C'``, ``'H'``, ``'O'``, ``'S'``
    :param imag_unit_index: 1-based index of the imaginary basis unit.
    :returns: the corresponding left-multiplication matrix.
    """
    _DIM  = {'R': 1, 'C': 2, 'H': 4, 'O': 8, 'S': 16}
    _NAME = {'R': 'Real', 'C': 'Complex', 'H': 'Quaternion',
             'O': 'Octonion', 'S': 'Sedenion'}
    alg = CayleyDicksonAlgebra(
        label=algebra_label,
        dim=_DIM[algebra_label],
        name=_NAME[algebra_label],
    )
    gens = alg.generators()
    return gens[imag_unit_index - 1]


# Convenient algebra singletons
ALG_R = CayleyDicksonAlgebra(label='R', dim=1,  name='Real')
ALG_C = CayleyDicksonAlgebra(label='C', dim=2,  name='Complex')
ALG_H = CayleyDicksonAlgebra(label='H', dim=4,  name='Quaternion')
ALG_O = CayleyDicksonAlgebra(label='O', dim=8,  name='Octonion')
ALG_S = CayleyDicksonAlgebra(label='S', dim=16, name='Sedenion')
