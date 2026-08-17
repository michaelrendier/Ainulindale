"""
ainulindale_engine.modules.sedenion.dimensions
===============================================
The 16 conversational dimensions of the Emmy Noether Sedenion Engine.

Each sedenion basis element ``e_k`` (k=0..15) is assigned a specific
dimension of conversational / linguistic structure.  The sedenion IS the
prompt — not a representation of it.  The H_hat_RB Hamiltonian IS the
response — computed from the field state that the sedenion selects.

Physical analogy:

  - The sedenion = stress-energy tensor T_μν (sources geometry)
  - H_hat_RB = Einstein tensor G_μν (the curvature response)
  - Einstein equation: G = 8πG · T
  - The sedenion engine tells H_hat_RB *how much* geometry to source
    in each conversational dimension simultaneously.

Cayley-Dickson tower:

  ℝ  (e₀)        — scalar ground state
  ℂ  (e₀, e₁)   — letter-gematria complex plane
  ℍ  (e₀..e₃)   — noun/verb/descriptive quaternion
  𝕆  (e₀..e₇)   — full predicate-temporal octonion
  𝕊  (e₀..e₁₅)  — complete 16D conversational sedenion

The zero divisors on S¹⁵ are the Fermat lattice — the "last scattering
surface" where semantic potential crystallises into surface language.

Version: 0.111
"""

from typing import NamedTuple, List


class Dimension(NamedTuple):
    """
    One of the 16 sedenion basis dimensions.

    :param index: basis element index (0..15)
    :param name: short programmatic name
    :param label: display label (with eₖ notation)
    :param algebra_stratum: which CD level introduces this dimension
    :param linguistic_role: what this dimension carries in a conversation
    :param physical_analog: the physics / field-theory analog
    :param noether_symmetry: the symmetry whose conservation this tracks
    :param keywords: heuristic trigger words / patterns (for encode_prompt)
    """
    index:            int
    name:             str
    label:            str
    algebra_stratum:  str
    linguistic_role:  str
    physical_analog:  str
    noether_symmetry: str
    keywords:         List[str]


DIMENSIONS: List[Dimension] = [
    Dimension(
        index=0,
        name='scalar',
        label='e₀ — Scalar / Ground State',
        algebra_stratum='ℝ',
        linguistic_role='Bias term; always-on baseline charge; the "DC offset" of meaning',
        physical_analog='Vacuum energy; cosmological constant Λ',
        noether_symmetry='Trivial (no imaginary part — cannot be violated)',
        keywords=[],
    ),
    Dimension(
        index=1,
        name='gematria',
        label='e₁ — Gematria / Letter-Number Identity',
        algebra_stratum='ℂ',
        linguistic_role=(
            'The letter IS the number.  Hebrew gematria: aleph=1, bet=2, '
            'etc.  HyperWebster Horner hash: word → seed ∈ [0,1] → γ_n.  '
            'This is the original encoding that made the Septuagint possible.'
        ),
        physical_analog='Phase angle φ = γ/2 in the Riemann zero plane',
        noether_symmetry='U(1) rotational symmetry in the letter-number complex plane',
        keywords=['hash', 'number', 'letter', 'index', 'code', 'symbol'],
    ),
    Dimension(
        index=2,
        name='word_edge',
        label='e₂ — Word Co-occurrence / A-Matrix',
        algebra_stratum='ℂ',
        linguistic_role=(
            'A-matrix edge weight between co-occurring words.  '
            'Captures lexicographic neighborhood — which words live near '
            'each other in semantic space.'
        ),
        physical_analog='Propagator A_ij in the monad field; coupling constant g',
        noether_symmetry='Translation symmetry in word-pair space',
        keywords=['with', 'and', 'or', 'also', 'together', 'both'],
    ),
    Dimension(
        index=3,
        name='noun',
        label='e₃ — Noun Field / Subject Carrier',
        algebra_stratum='ℍ',
        linguistic_role='Subject and object positions; entities being talked about',
        physical_analog='Matter field Ψ (fermion source of J^μ)',
        noether_symmetry='SU(2) isospin — noun ↔ pronoun substitution invariance',
        keywords=['the', 'a', 'an', 'thing', 'object', 'entity', 'person', 'place'],
    ),
    Dimension(
        index=4,
        name='verb',
        label='e₄ — Verb Field / Action Carrier',
        algebra_stratum='ℍ',
        linguistic_role='Actions, states, events; what is happening to/with the nouns',
        physical_analog='Gauge field A^μ; force carrier mediating interactions',
        noether_symmetry='SU(2) — active/passive voice transformation',
        keywords=['is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'do', 'does', 'did', 'have', 'has', 'had', 'will',
                  'would', 'can', 'could', 'should', 'may', 'might'],
    ),
    Dimension(
        index=5,
        name='descriptive',
        label='e₅ — Descriptive Field / Adjective-Adverb',
        algebra_stratum='ℍ',
        linguistic_role='Qualifiers and modifiers; how nouns/verbs are coloured',
        physical_analog='Spin label σ; quantum number decorating the state',
        noether_symmetry='SU(2) — scale transformation (very/quite/slightly invariance)',
        keywords=['very', 'quite', 'much', 'more', 'most', 'less', 'least',
                  'really', 'just', 'quite', 'rather', 'fairly', 'pretty'],
    ),
    Dimension(
        index=6,
        name='predicate',
        label='e₆ — Predicate / Clause Structure',
        algebra_stratum='𝕆',
        linguistic_role=(
            'The predicate binds subject to verb to object.  '
            'Clause-level logic: implication, negation, question formation.'
        ),
        physical_analog='Boundary operator ∂; the boundary of the boundary is zero',
        noether_symmetry='G₂ — predicate-argument permutation invariance',
        keywords=['if', 'then', 'because', 'therefore', 'so', 'but', 'although',
                  'however', 'not', 'never', 'always', 'sometimes'],
    ),
    Dimension(
        index=7,
        name='temporal',
        label='e₇ — Temporal / Aspect',
        algebra_stratum='𝕆',
        linguistic_role=(
            'Tense (past/present/future), aspect (ongoing/completed), '
            'temporal adverbials.  The "age" of the utterance in discourse time.'
        ),
        physical_analog='Time coordinate t; age decay _advance_age() in the monad',
        noether_symmetry='G₂ — time-translation invariance (Hamiltonian conservation)',
        keywords=['was', 'were', 'will', 'would', 'has', 'have', 'had',
                  'now', 'then', 'before', 'after', 'when', 'while',
                  'ago', 'yet', 'already', 'still', 'soon', 'later'],
    ),
    Dimension(
        index=8,
        name='pronominal',
        label='e₈ — Pronominal / Deictic',
        algebra_stratum='𝕊',
        linguistic_role=(
            'First, second, third person; demonstratives (this/that/here/there). '
            'The speaker-listener axis: "I" and "you" define the coordinate frame '
            'of the conversation, just as the observer defines the measurement basis.'
        ),
        physical_analog='Observer frame; the "cos" face in the monad (observer perspective)',
        noether_symmetry='𝕊-level — frame-of-reference invariance',
        keywords=['i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our',
                  'you', 'your', 'he', 'she', 'it', 'they', 'this', 'that',
                  'here', 'there', 'who', 'what'],
    ),
    Dimension(
        index=9,
        name='thread_1',
        label='e₉ — Discourse Thread 1 / Topic Chain',
        algebra_stratum='𝕊',
        linguistic_role=(
            'The primary topic being tracked through the conversation.  '
            'Each new sentence either extends or switches the topic chain.'
        ),
        physical_analog='World-line of a particle; trajectory through semantic space',
        noether_symmetry='𝕊-level — topic persistence invariance',
        keywords=['topic', 'about', 'regarding', 'concerning', 'subject', 'matter'],
    ),
    Dimension(
        index=10,
        name='thread_2',
        label='e₁₀ — Discourse Thread 2 / Thematic Progression',
        algebra_stratum='𝕊',
        linguistic_role=(
            'The secondary theme or rheme.  In "John bought a car — it was red," '
            '"car" is thread_1 (topic), "red" is thread_2 (new information/theme).'
        ),
        physical_analog='Second world-line; interference pattern with thread_1',
        noether_symmetry='𝕊-level — topic-theme separation invariance',
        keywords=['new', 'also', 'additionally', 'furthermore', 'moreover'],
    ),
    Dimension(
        index=11,
        name='anaphor',
        label='e₁₁ — Anaphor / Inter-Thread Connection',
        algebra_stratum='𝕊',
        linguistic_role=(
            'Coreference and pronoun resolution — the inter-thread binding.  '
            '"your becomes I, name stays name" (the user\'s key observation).  '
            'This is why "What is your name?" → "My name is..." works: '
            'the anaphor dimension carries the you→I transformation.'
        ),
        physical_analog='Propagator between two Riemann zeros (A-matrix off-diagonal)',
        noether_symmetry='𝕊-level — coreference invariance',
        keywords=['it', 'its', 'they', 'them', 'their', 'he', 'she', 'who',
                  'which', 'that', 'this', 'these', 'those'],
    ),
    Dimension(
        index=12,
        name='presupposition',
        label='e₁₂ — Presupposition / Background',
        algebra_stratum='𝕊',
        linguistic_role=(
            'Unstated background assumptions that the conversation takes for granted.  '
            '"Stop drinking" presupposes the listener currently drinks.  '
            'This is the "capacitor" dimension — charge stored between utterances.'
        ),
        physical_analog='Vacuum / background field; the β-field before a new word arrives',
        noether_symmetry='𝕊-level — background-stability invariance',
        keywords=['the', 'already', 'again', 'still', 'even', 'only', 'too'],
    ),
    Dimension(
        index=13,
        name='gestalt',
        label='e₁₃ — Thoughtform / Gestalt',
        algebra_stratum='𝕊',
        linguistic_role=(
            'The unified impression — the thing being communicated as a whole, '
            'beyond its grammatical parts.  The "prime charge IS the response" '
            'lives here: J^μ in zero space before Face rendering.'
        ),
        physical_analog='Prime charge J^μ = β×E² in the monad; speak_raw() output',
        noether_symmetry='𝕊-level — holistic-meaning invariance',
        keywords=['mean', 'means', 'meant', 'understand', 'understand', 'sense',
                  'idea', 'concept', 'notion', 'think', 'believe', 'feel'],
    ),
    Dimension(
        index=14,
        name='affect',
        label='e₁₄ — Affect / Valence',
        algebra_stratum='𝕊',
        linguistic_role=(
            'Emotional charge and valence.  The monad\'s affect parameter.  '
            'Positive affect → Wick-rotated (QM) speak mode.  '
            'Neutral affect → geometric (GR) speak mode.'
        ),
        physical_analog='Affect parameter in monad_speak(); phase φ = affect × π/2',
        noether_symmetry='𝕊-level — affect-invariance (same meaning across emotional register)',
        keywords=['good', 'bad', 'love', 'hate', 'happy', 'sad', 'angry',
                  'excited', 'worried', 'glad', 'sorry', 'please', 'thank'],
    ),
    Dimension(
        index=15,
        name='meta',
        label='e₁₅ — Meta-Discourse',
        algebra_stratum='𝕊',
        linguistic_role=(
            'Discourse about the conversation itself.  "What I\'m saying is...", '
            '"To summarise...", "Going back to...".  The self-referential dimension.  '
            'The sedenion\'s e₁₅ is the final Cayley-Dickson doubling — the '
            'algebra\'s own self-awareness of its structure.'
        ),
        physical_analog='Meta-level operator; the algebra acting on itself',
        noether_symmetry='𝕊-level — self-reference invariance',
        keywords=['mean', 'say', 'said', 'tell', 'told', 'ask', 'asked',
                  'explain', 'clarify', 'summarise', 'summarize', 'repeat',
                  'rephrase', 'in other words', 'that is', 'i.e.', 'e.g.'],
    ),
]

# Fast lookup by index
DIM_BY_INDEX = {d.index: d for d in DIMENSIONS}

# Algebra stratum membership
STRATUM_DIMS = {
    'ℝ': [0],
    'ℂ': [0, 1, 2],
    'ℍ': [0, 1, 2, 3, 4, 5],
    '𝕆': [0, 1, 2, 3, 4, 5, 6, 7],
    '𝕊': list(range(16)),
}
