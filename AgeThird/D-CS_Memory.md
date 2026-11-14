# Data Storage With No Physical Location, and a New Method of Information Propagation
## Part I of Teaching the Maths English

**Author:** Cody Michael Allison | ORCID: 0009-0007-7239-6760  
**Date:** 2026-06-14 — Third Age · abstract 2026-09-29 · body rewritten 2026-11-14  
**Status:** DRAFT 2 — engineering white paper; the abstract is the author's and is unchanged; the body was rewritten 2026-11-14 against `cs-paper-code-conventions` (the pre-rewrite paper is archived at `Ainulindale/archive/D-CS_Memory_2026-09-29_pre-rewrite.md`)  
**Companion papers:** D-CS (The Sedenion Engine) · D-M (Mathematics) · D-P (Physics) · D-CHEM (Chemistry, Schafer collab.)  
**Hardware:** Intel Core i7-8550U @ 1.80 GHz · 4 cores / 8 threads · 7.5 GiB RAM · Linux 6.8 lowlatency · Python 3.12 · no GPU  
**Citations:** keys `[AuthorYEAR]` resolve in the References section and in `Ainulindale/wiki/98_provenance_and_citations.md`; retrieval details in `Ainulindale/references/CITATION_DOWNLOADS.md`.

---

> ## Note on how this paper was written
>
> This paper was written by a transformer language model (Claude Sonnet 5.5, model id `claude-sonnet-5-5`) working with the author, with the project's skill `cs-paper-code-conventions` loaded (`ContextPlease/claude/skills/cs-paper-code-conventions/`). The author, Cody Michael Allison (pen name Michael Rendier), is an autodidact: these are the first research papers he has written, and he is not an academic. His method is **not to tell the model the result he is looking for**, so that he is not handed the answers he wants; that is a safeguard, not a guarantee. The model drafted the sections, ran every listing and transcript below, and corrected the text to what the code printed. The abstract is the author's own words and is reproduced unchanged.
>
> **What kind of paper this is.** An engineering white paper about a storage mechanism and a propagation mechanism, with two worked examples: the **hyperindexing system** (storage) and the **scalar box kite** (context carried as one number per token). It carries no proofs, no pre-registered prediction and no claim about physics; it is not a Fourth Age paper. Every number in it is either arithmetic (a listing prints it) or measured (a transcript prints it, with its script path). Where the code did not reproduce something earlier text said, the earlier statement is kept and marked.
>
> **Labels.** `ESTABLISHED` = cited work or exact arithmetic; `OURS` = a construction made here; `OURS:CALCULATED` = a result this paper's own code produced (calculated, not derived); `THEORETICAL` = a construction with no running code yet; `OPEN` = not settled.

---

> ## Abstract
>
> Every new instance of a program, chat or model starts fresh and does not remember the last. Months of my research with Gemini rested on an assumption of persistent memory that was false, and that is the claim I set out to engineer against. My starting idea, from Borges's *The Library of Babel*, was that every possible text already exists: nothing has to be written down, only located. The result is the *HyperWebster*, a name I took from the Vsauce Banach–Tarski video (`Post-Hoc:` I learned only afterward that Stewart (1996) had coined it). Data is located by an address computed from the text itself, so it is found by computation, not by storage. The address alphabet is printable ASCII plus tab and newline, 97 symbols, the keys of a US-English laptop keyboard without a 10-key. The single departure from it was a Unicode experiment, which encoded every alphabet a computer can display into a "potential response domain". It gave the system its multilingual support, and afterward Holcus chose his name in the first Ptolemy experiment. The first form I wanted to try was a single file that could potentially hold limitless data, sitting in my Google Drive for Gemini to read and "reconstruct" ingested knowledge from a permutation, not a location on any media. The file held the hyperindex of a JSON file, written in a permutation of JSON characters. That JSON is a list of hyperindexes, data lengths and timestamps, each locating a block of ingested data. The lists are indexed again, recursively, so that Gemini could crunch that one hyper-layered index and explore everything it had ingested by date and time. An early version, built with Gemini, was a hyper-dimensional fractal rotation manifold over the letter permutations. From my instruction that "primes are words", reduced to a single underlying prime concept, Claude Code (the default model in April 2026) invented the semantic prime hash: a semantic-neighbourhood hash that places every English word of the language on a prime number. It opened the door to the mathematics that followed. Early reduction came from Banach–Tarski-style rotations that make one permutation look like the next, shrinking the permutation-addressing domain. The de Bruijn sequence was added when I moved from permuting letters to permuting English words. The octonion layer came last, after studying octonion-analogue material from a friend, and it reproduced structurally, in the Fano plane, mathematics I had already used.
>
> Computational overhead reduction is the engineering method here, and I report its cost as measured. In the shipped 97-symbol charset the address is 82.5% of the raw size at every scale, and the round trip is exact. Restricting the charset to the symbols present takes the chunk address to 75–79%. Frequency ordering alone changes nothing measurable (0.824 against 0.825). A 256-bit address holds at most 38 characters, so input is chunked. The 8 × 32-bit octonion coordinates of a 256-bit address are exact but do not shorten it. The recursive calendrical index restores exactly by date. In the shipped charset each layer up is about 1.7× larger than the one below (top pointer 2.4× the corpus). With per-layer minimal charsets it is about 1.2× per layer (1.18×), and with a compact hex-only layer format about 1.05× per layer (0.87×). It never falls below the content it locates. The saving is per instance: a new instance is handed a pointer and a length in place of the corpus *[payload measurement pending]*. Folding many addresses into a single 256-bit root is unbuilt, and I state what such a root can be: an identifier of stored pieces, not an encoding of arbitrary data. `THEORETICAL`.
>
> The method was designed directly against the reading and videos listed at the head of the README. Every other name in this paper is cited `Post-Hoc:`.
>
> The efficiency of the HyperWebster made me use the same mathematics to try a new type of information propagation: forward propagation, so that AI can be designed on a laptop without training a model for decades. Its parts are tiny pre-trained neurons grabbed together on the fly, chosen by a *neuron-selection engine* I first designed for the languages spoken. In migrating around the Cayley–Dickson tower I needed one constant that says the same thing in every algebra of the tower, as a debugging check that no transition corrupted the output. When I moved to this new type of information propagation and the pathways forward it opened, the HyperWebster was shelved while I explored the mathematics to map out the boundaries I had to be wary of.
>
> When I added the octonions, I had recently learned that some of the terms in the Standard Model Lagrangian were called "index". Claude began to use Index as a literal mathematical object, and I asked if these were similar maths to the Standard Model Lagrangian. Claude said these were the exact mathematics of the Standard Model, and I asked it to write "a Standard Model of Neural Network Information Propagation". The result, VAPMIP (Virtual Action Potential Monad Information Propagation), was found to be isomorphic in form to the Standard Model of particle physics Lagrangian, with my error-check constant identified as a fine-structure constant that my code had explicitly defined. `Post-Hoc:` Dixon (1994), Furey (2016), the Standard Model. No isomorphism was intended. I state what is preserved (four-term structure and gauge ladder, at single-layer Abelian approximation) and what isn't: the Standard Model Lagrangian is not reproduced here, and the Dirac and non-Abelian terms are stubs, marked `THEORETICAL`.
>
> Learning what a structural constant is and does, I paused to engineer my own. I approached Fermat and Riemann from opposite sides of a boundary, chasing entropy to a thermal information ceiling (1.4×10¹⁷ K, a concept from Vsauce's *How Hot Can It Get?* used as a boundary condition, not derived) and inertia to the speed of causality, the two ceilings on information propagation. The Lambert-W fixed point and d* were found, giving Α_π and Ω_ζΣ. That experiment opens the VAPMIP paper.

---

## 1. Introduction

A program, a chat or a model instance starts empty and does not remember the one before it. The usual repairs store the past somewhere and look it up: a file, a database, a vector index, a longer context window. Each repair has a location, a size that grows with what was kept, and a search that has to be paid for every time. Part of this work began from a mistake of that kind: months of research with a language model rested on an assumption of persistent memory that was false, and the claim engineered against is that one should not have to rely on a place.

The way around is to stop storing and start **addressing**. Every finite text over a fixed character set already corresponds to exactly one whole number (its place in the ordered list of all strings), and the correspondence runs both ways, so the text can be *reconstructed from* the number instead of looked up. Nothing is stored but the number and the rule. This paper defines that address, shows the whole mechanism as short programs that run, measures what it costs, and says plainly what it does not do. It does not compress: ordinary compressors beat it by a wide margin on the same text (§5). What it offers is a different trade: a location-free, exact, stateless name for any string, and a way to build structure on those names.

The second half is the same idea applied to meaning. If a word can be named by a number, a sentence is a sequence of numbers, and the relations between words can be carried by the *shape* of how those numbers are formed. §7 shows one such construction, the scalar box kite, in which one scalar per token is enough to rebuild a larger relational structure by a fixed rule. The two examples share a method: **overhead reduction by construction**, meaning the structure is in the rule, not in a table that has to be stored, searched or trained.

## 2. Definitions

- **Character set** — an ordered list of N distinct symbols. In the shipped code N = 97: the 94 printable ASCII symbols that a US-English laptop keyboard produces without the numeric pad, the space, the tab and the line feed.
- **Address** — the non-negative integer that is the position of a string in the list of all strings over the character set, ordered by length and then lexicographically (the *bijective base-N* numbering: there is no zero digit, so `"a"`, `"aa"` and `"aaa"` are distinct).
- **Chunk** — a string cut to a fixed length so that its address stays short.
- **Index record** — the triple (address as 64 hex digits, length, timestamp). The record is the whole memory of the string.
- **Layer** — a text made of index records (for example a day's records written as JSON) is itself a string, so it has an address; this is the *layered* index (§6).

## 3. The mechanism

### 3.1 The address

**Listing 1 — the bijective address** (`PtolemyDesktop/Callimachus/HyperWebster-Data-Storage/hyperwebster.py`; the two methods and the character set are extracted verbatim, the class shell is added so it runs alone)

```python
class HyperWebster:
    _DEFAULT_CHARS = (
        r"""`1234567890-="""
        "\t"
        r"""qwertyuiop[]\asdfghjkl;'"""
        "\n"
        r"""zxcvbnm,./ ~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""
    )

    def __init__(self, characters=_DEFAULT_CHARS):          # class shell (added); the shipped __init__ also sets the int limit
        self.characters = characters; self.char_list = list(characters); self.N = len(self.char_list)
        self._char_index = {ch: i for i, ch in enumerate(self.char_list)}

    def point_to_text(self, text: str) -> int:
        """
        INDEXING  —  string → unique non-negative integer address.

        Uses bijective base-N (no zero digit), so every string including
        those starting with the first character get a distinct address.
        """
        address = 0
        for i, ch in enumerate(reversed(text)):
            try:
                index = self._char_index[ch] + 1          # 1-based
            except KeyError:
                raise ValueError(
                    f"Character {ch!r} is not in the character set."
                )
            address += index * (self.N ** i)
        return address - 1                                 # 0-based coordinate

    def regenerate_text(self, address: int) -> str:
        """
        REGENERATION  —  non-negative integer address → string.
        """
        if address < 0:
            raise ValueError("Address must be a non-negative integer.")

        res     = []
        address += 1                                       # shift for bijective logic

        while address > 0:
            address, rem = divmod(address - 1, self.N)
            res.append(self.char_list[rem])

        return "".join(reversed(res))

hw = HyperWebster(); text = "Hello, World!"
a = hw.point_to_text(text)
print('N =', hw.N, '; address of', repr(text), '=', a)
print('round trip exact:', hw.regenerate_text(a) == text, '; address bits:', a.bit_length(), 'for', len(text), 'characters')
```

```
N = 97 ; address of 'Hello, World!' = 57019357119426523871881570
round trip exact: True ; address bits: 86 for 13 characters
```

Listing 1 is `OURS` in its use and `ESTABLISHED` as a construction: bijective numeration is classical, and its relatives are Gödel numbering and the factorial-number-system ranking of Laisant (1888) and Lehmer, and Myrvold & Ruskey (2001). No part of the address is a table: the character set and the two loops are everything.

### 3.2 The whole bijection, for the smallest non-trivial case

An exhaustive table is a stronger statement than a sample. Over a two-letter set, every string of length 1 to 3 and its address:

**Listing 2 — every string over `ab` up to length 3, with its address** (the same two methods as Listing 1, with the character set `ab`)

```python
class HyperWebster:
    def __init__(self, characters='ab'):                      # class shell (added)
        self.characters = characters; self.char_list = list(characters); self.N = len(self.char_list)
        self._char_index = {ch: i for i, ch in enumerate(self.char_list)}

    def point_to_text(self, text: str) -> int:
        """
        INDEXING  —  string → unique non-negative integer address.

        Uses bijective base-N (no zero digit), so every string including
        those starting with the first character get a distinct address.
        """
        address = 0
        for i, ch in enumerate(reversed(text)):
            try:
                index = self._char_index[ch] + 1          # 1-based
            except KeyError:
                raise ValueError(
                    f"Character {ch!r} is not in the character set."
                )
            address += index * (self.N ** i)
        return address - 1                                 # 0-based coordinate

    def regenerate_text(self, address: int) -> str:
        """
        REGENERATION  —  non-negative integer address → string.
        """
        if address < 0:
            raise ValueError("Address must be a non-negative integer.")

        res     = []
        address += 1                                       # shift for bijective logic

        while address > 0:
            address, rem = divmod(address - 1, self.N)
            res.append(self.char_list[rem])

        return "".join(reversed(res))

import itertools
rows = []
for L in (1, 2, 3):
    for t in itertools.product('ab', repeat=L):
        s = ''.join(t); rows.append((HyperWebster().point_to_text(s), s))
rows.sort()
print('  '.join('%d:%s' % (a, s) for a, s in rows))
print('addresses are exactly 0..%d with no gap and no repeat:' % (len(rows) - 1), [a for a, _ in rows] == list(range(len(rows))))
print('every address regenerates its string:', all(HyperWebster().regenerate_text(a) == s for a, s in rows))
```

```
0:a  1:b  2:aa  3:ab  4:ba  5:bb  6:aaa  7:aab  8:aba  9:abb  10:baa  11:bab  12:bba  13:bbb
addresses are exactly 0..13 with no gap and no repeat: True
every address regenerates its string: True
```

The fourteen strings take the fourteen addresses 0…13 with no gap and no repeat, in length-then-lexicographic order. The order is *defined by the numbering*, as it is in the permutation-ranking literature (Myrvold & Ruskey 2001 show the same table for all 24 permutations of four elements).

### 3.3 What the address costs

A string of L characters has an address below N^L, so about L·log₂N bits: 6.600 bits per character at N = 97, against 8 bits per byte. The ratio 6.600/8 = 0.825 is a property of N, independent of the text.

**Listing 3 — the arithmetic of the cost and of a 256-bit address** (python3 standard library)

```python
import math
N = 97
print('bits per character at N = 97: %.3f ; against 8 bits per byte: %.3f of raw' % (math.log2(N), math.log2(N) / 8))
print('97^38 <= 2^256:', N ** 38 <= 2 ** 256, '; 97^39 <= 2^256:', N ** 39 <= 2 ** 256, '=> a 256-bit address holds at most 38 characters')
print('bits needed for 38 characters:', (N ** 38 - 1).bit_length(), 'against 38 x 8 = 304 raw bits (%.3f)' % ((N ** 38 - 1).bit_length() / 304))
print('bits needed for 32 characters:', (N ** 32 - 1).bit_length(), 'but a fixed 256-bit field costs 256 against 32 x 8 = 256 raw (ratio 1.000)')
```

```
bits per character at N = 97: 6.600 ; against 8 bits per byte: 0.825 of raw
97^38 <= 2^256: True ; 97^39 <= 2^256: False => a 256-bit address holds at most 38 characters
bits needed for 38 characters: 251 against 38 x 8 = 304 raw bits (0.826)
bits needed for 32 characters: 212 but a fixed 256-bit field costs 256 against 32 x 8 = 256 raw (ratio 1.000)
```

A 256-bit address therefore holds at most 38 characters of this character set. Longer texts need chunks, or a longer address.

## 4. What this paper measures

Measured on the shipped code (`bench.py`, `ContextPlease/claude/scratchpad/2026-09-29_hyperwebster_overhead/`, run 2026-11-14 on the machine in the header; nothing tuned). The corpora are text already in the repositories: a 25,000-character English prose file, a 40,000-character prose document and a Python file. Columns: address bits (variable width), address bits with a 256-bit minimum, the same with a character set cut to the symbols present (cost of listing the set included), and, for fairness, what `zlib` and `lzma` give on the same chunks.

**Transcript 1 — address size against raw size, and against ordinary compressors** (excerpt of `bench_output_2026-11-14.txt`, first corpus; raw size is 8 bits per character)

```
english_corpus.txt (prose)   kept 24944 chars (cap 40000); 1807 chars outside the 97-symbol set dropped from the whole file
   raw 199552 bits | order-0 entropy 5.201 bits/char (=129741 bits) | distinct symbols 83
   chunk    addr_var   addr_256+  min-cset   zlib      lzma      var/raw   fix/raw  enc_ms   ok
   32       163872     199680     231438     244304    549024    0.821     1.001    10.8     True
   38       163979     168192     228469     235264    504352    0.822     0.843    9.9      True
   64       164231     164231     213608     210984    374496    0.823     0.823    11.0     True
   128      164432     164432     183165     156648    251968    0.824     0.824    14.4     True
   256      164539     164539     166391     119544    169920    0.825     0.825    27.1     True
   500      164577     164577     158188     94312     123328    0.825     0.825    45.1     True
   1000     164605     164605     155213     78656     95488     0.825     0.825    128.3    True
   4000     164623     164623     155636     63256     67936     0.825     0.825    1071.0   True
   whole 4000-char doc as one address: 26399 bits (raw 32000) -> 0.825 of raw
   D. 38-char chunk -> address 250 bits -> 8 limbs x 32 bits -> recombine exact: True ; text round-trip: True
```

Read the columns. The address is 0.821–0.825 of raw at every chunk size, and the round trip is exact in every row (`ok True`). At 32 characters a fixed 256-bit address costs *more* than the raw text (`fix/raw` 1.001). And `zlib` and `lzma`, which store nothing about the character set, come in below the address from 128 characters up for `zlib` and from 500 up for `lzma` (for 1,000-character chunks: `zlib` 78,656 and `lzma` 95,488 bits against 164,605). **The address is not compression, and the paper does not say it is.** Restricting the character set to the symbols present helps the chunk address (the `min-cset` column) and nothing else; ordering the character set by frequency changes nothing measurable (0.824 against 0.825, Transcript 2).

## 5. The layered index

A text that is a list of index records has its own address, so records of records can be indexed to any depth, and a corpus can be reached from one top address plus the rules. The cost is measured, not assumed.

**Transcript 2 — a three-layer index (chunk → day → month) over 4,000 characters** (excerpt of `bench_layers2_output_2026-11-14.txt`; "address bits × raw" is the address size divided by the raw corpus size at each layer; `growth` is the factor per layer)

```
corpus 4000 chars = 32000 raw bits | chunk 200 | 4 chunks/day | 5 days/month
  mode                 |charset| | address bits x raw: chunk/day/month | top ptr   +cs list  growth    | exact       secs
  M0 shipped 97        97/97/97  | 0.824 / 1.480 / 2.472            | 2.472     2.472     1.732     | True        3.6
  A freq-ordered 97    97/97/97  | 0.823 / 1.479 / 2.470            | 2.470     2.543     1.732     | True        3.6
  B restricted         65/27/27  | 0.752 / 0.981 / 1.188            | 1.188     1.218     1.257     | True        0.8
  A+B restricted+freq  65/27/27  | 0.751 / 0.980 / 1.187            | 1.187     1.216     1.257     | True        0.7
  A+B compact (hex,;)  65/18/18  | 0.751 / 0.803 / 0.842            | 0.842     0.868     1.059     | True        0.4
```

With the shipped character set the layered index **inflates**: 0.824 of raw at the chunk layer, 1.480 at the day layer and 2.472 at the month layer, a factor of about 1.7 per layer, because the JSON that carries the index records is itself text over the full set. Restricting each layer to the symbols it uses brings the top pointer to 1.19 of raw, and a compact record format to 0.84 (the last two rows), always with exact reconstruction. So the layered index works and is exact, and **is not smaller than the text** on this corpus; the figure that a layered index folds a corpus into a single 256-bit address is a statement about the *address space* (every corpus has an address) and not about size: a 256-bit address holds 38 characters (§3.3), and the fold of a whole layered index to 256 bits is `THEORETICAL`, not built.

## 6. Example one — the hyperindexing system (storage)

The mechanism of §3 plus a ledger. Each ingest appends one record (address, length, timestamp) to an append-only list; the list is text, so it has an address, and the ledger can be indexed by itself. What is stored is the records and the character set; the text is regenerated by Listing 1's second method. A longer, separately written paper on this mechanism (`FourthAgePapers/HyperindexingSystem`) carries the claim, the prediction and the comparison with the published algorithm of the Library of Babel image archive (Basile, Post-Hoc); this paper uses only the plain bijection above. Its engine is `ValaQuenta/modules/hyperwebster/` (`horner_encode`), documented in the API reference and in `Ainulindale/wiki/09_hyperwebster_engine.md` and `wiki/124_basile_invertible_location_maps.md`.

What exists, by component: the bijection and its 256-bit hex form (shipped, Listing 1); the layered index (built, Transcript 2); the `(address, length, timestamp)` ledger (a specification, built in `Callimachus`); a recursive fold to a single 256-bit root (`THEORETICAL`: no code, and bounded by §3.3).

## 7. Example two — the scalar box kite (context as one number per token)

The second example turns a word into a number whose *form* carries information, so that a relational structure can be reconstructed from one scalar per token. The full construction (a 19-relation WordNet box kite, a pencil of lines through each word, a codec) is a paper of its own (`FourthAgePapers/ScalarContextPropagation`) and a long mechanism, so it is cited, not excerpted. One short, `OURS` piece of it carries the idea and is shown whole (its own docstring calls it *provisional*, "a first working pass, explicitly not a locked design"): the **spelling code**, where position picks the prime and the letter is the exponent.

The first thing tried, one prime per letter and a product of the letters, fails in a specific way: multiplication commutes, so every anagram collides (`listen` and `silent` give the same integer). The shipped fix swaps the roles: position `i` selects a base prime and the letter is its exponent. Position now matters, and the word can be read back by factoring.

**Listing 4 — the spelling code, its inverse, and the anagram test** (`VAPMIP/wordnet_boxkite.py`, `_sieve`, `LETTER_CAP`, `LETTER_PRIMES` and `spelling_code` extracted verbatim; the decoder and the tests are written for this listing)

```python
from typing import List

def _sieve(n: int) -> List[int]:
    sv = bytearray([1]) * (n + 1)
    sv[0] = sv[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if sv[i]:
            sv[i * i::i] = bytearray(len(sv[i * i::i]))
    return [i for i in range(n + 1) if sv[i]]

_P = _sieve(200_000)

LETTER_CAP = 71

LETTER_PRIMES: List[int] = [p for p in _P if p <= LETTER_CAP]   # 20 — spelling tier

def spelling_code(word: str) -> int:
    """Godel-style: position i uses LETTER_PRIMES[i % 20] (cyclic through
    the 20-symbol letter tier), exponent = the letter's alphabet index
    (a=1..z=26) — order-sensitive, no information lost. PROVISIONAL: the
    exact letter-tier mechanics weren't pinned down before this build;
    this is a first working pass, explicitly not a locked design."""
    code = 1
    for i, ch in enumerate(w for w in word.lower() if w.isalpha()):
        p = LETTER_PRIMES[i % len(LETTER_PRIMES)]
        exp = ord(ch) - ord('a') + 1
        code *= p ** exp
    return code

def decode(code, nletters):                      # factor the code at the position primes (for words of 20 letters or fewer)
    out = ''
    for i in range(nletters):
        p, e = LETTER_PRIMES[i], 0
        while code % p == 0: code //= p; e += 1
        out += chr(ord('a') + e - 1)
    return out

naive = lambda w: __import__('math').prod({c: p for c, p in zip('abcdefghijklmnopqrstuvwxyz', _P)}[c] for c in w)
print('naive prime-per-letter product : cat', naive('cat'), '= act', naive('act'), '; listen', naive('listen'), '= silent', naive('silent'))
print('spelling_code                   : cat == act:', spelling_code('cat') == spelling_code('act'), '; listen == silent:', spelling_code('listen') == spelling_code('silent'))
print('spelling_code("cat") =', spelling_code('cat'))
print('decoded:', [decode(spelling_code(w), len(w)) for w in ('cat', 'act', 'windspeed', 'reconstructible')])
a, b = 'a' + 'x' * 19 + 'c', 'b' + 'x' * 19 + 'b'
print('two different 21-letter words, same code (positions 0 and 20 share the base 2, 1+3 = 2+2):', spelling_code(a) == spelling_code(b))
import random
words = [w.strip().lower() for w in open('/usr/share/dict/words') if w.strip().isalpha()]
random.seed(0); sample = random.sample(sorted(set(words)), 30000)
short = [w for w in sample if len(w) <= 20]; long_ = [w for w in sample if len(w) > 20]
ok = sum(decode(spelling_code(w), len(w)) == w for w in short)
print('sample of 30,000 dictionary words: %d have <= 20 letters, exact recovery %d (%.3f %%); %d have more than 20 letters' % (len(short), ok, 100 * ok / len(short), len(long_)))
```

```
naive prime-per-letter product : cat 710 = act 710 ; listen 1914801911 = silent 1914801911
spelling_code                   : cat == act: False ; listen == silent: False
spelling_code("cat") = 2288818359375000
decoded: ['cat', 'act', 'windspeed', 'reconstructible']
two different 21-letter words, same code (positions 0 and 20 share the base 2, 1+3 = 2+2): True
sample of 30,000 dictionary words: 29998 have <= 20 letters, exact recovery 29998 (100.000 %); 2 have more than 20 letters
```

Two properties are *exact*, not statistical: order survives (so `cat ≠ act` and `listen ≠ silent`), and a word of at most 20 letters is recovered exactly from its code (the 20 base primes are 2…71 and every letter fits in the exponent). Past 20 letters a base prime is reused and two exponents *add*, which is lossy by construction; the listing builds a real pair of 21-letter words with the same code. The measured exact-recovery figure on a different word sample than the one in the box-kite paper is in the transcript; the two samples differ and the paper's own figure (96.745 % of ≤20-letter words) is not reproduced here, because the sample is not the same one.

## 8. Two hashes that must not be confused

The address of §3 is **bijective and exact**: nothing is lost. The semantic hash that places a *word* on the Riemann zero list is **lossy and many-to-one** by design (it is what lets a vocabulary map to a bounded set of addresses). Both are called "Horner" in the repositories; they are different functions.

**Listing 5 — the semantic word hash and its collisions** (`VAPMIP/monad.py` lines 141–207, extracted verbatim: Horner base 95 over printable ASCII, then the next prime, then the prime-counting index; the sample and counts are written for this listing)

```python
from typing import List

_PRIME_CAP = 1 << 16          # 65536 — primes searched in [2, 65537]

# Build sieve of Eratosthenes (runs once at import)
_cap = _PRIME_CAP + 2
_sv  = bytearray([1]) * _cap
_sv[0] = _sv[1] = 0
for _i in range(2, int(_cap ** 0.5) + 1):
    if _sv[_i]:
        _sv[_i * _i :: _i] = bytearray(len(_sv[_i * _i :: _i]))

# Precompute π(k) — count of primes ≤ k, for k in [0, _PRIME_CAP]
_prime_pi_table: List[int] = [0] * _cap
_cnt = 0
for _k in range(_cap):
    if _sv[_k]:
        _cnt += 1
    _prime_pi_table[_k] = _cnt
del _i, _k, _cnt, _cap


def _next_prime(v: int) -> int:
    """
    Smallest prime p ≥ (v mod _PRIME_CAP), clamped to [2, 65537].

    :param v: Non-negative integer.
    :returns: A prime in [2, 65537].
    :rtype: int
    """
    v = max(2, int(v) % (_PRIME_CAP + 1))
    while v <= _PRIME_CAP + 1:
        if _sv[min(v, _PRIME_CAP + 1)] or v > _PRIME_CAP:
            return v
        v += 1
    return 65537   # largest prime ≤ 65537


def _horner_hash(w: str, base: int = 95, offset: int = 32) -> int:
    """
    Horner base-95 hash of word string. Returns a non-negative integer.
    ord range [32, 126] (printable ASCII) → coefficients in [0, 94].

    :param w: Word string (already cleaned/lowercased).
    :param base: Polynomial base (95 = printable ASCII range).
    :param offset: ord offset.
    :returns: Non-negative integer.
    :rtype: int
    """
    v = 0
    for ch in w:
        v = v * base + max(0, ord(ch) - offset)
    return abs(v)


def _word_zero_idx(w: str) -> int:
    """
    P1 prime hash: word → Horner int → next prime p → π(p) = zero index.

    :param w: Cleaned word string.
    :returns: Zero index in [1, 6542].
    :rtype: int
    """
    v = _horner_hash(w)
    p = _next_prime(v)
    idx = _prime_pi_table[min(p, _PRIME_CAP + 1)]
    return max(1, idx)

import collections, random
words = sorted({w.strip().lower() for w in open('/usr/share/dict/words') if w.strip().isalpha()})
random.seed(0); sample = random.sample(words, 5000)
idx = collections.Counter(_word_zero_idx(w) for w in sample)
print('5,000 dictionary words -> %d distinct indices (limit 6,542); largest share of one index: %d words' % (len(idx), max(idx.values())))
print('listen -> %d ; silent -> %d ; piano -> %d ; melancholy -> %d' % tuple(_word_zero_idx(w) for w in ('listen', 'silent', 'piano', 'melancholy')))
print('words sharing an index with another word in the sample: %d of 5,000' % sum(c for c in idx.values() if c > 1))
```

```
5,000 dictionary words -> 3072 distinct indices (limit 6,542); largest share of one index: 8 words
listen -> 417 ; silent -> 135 ; piano -> 4066 ; melancholy -> 1182
words sharing an index with another word in the sample: 3153 of 5,000
```

A vocabulary of any size lands on at most 6,542 indices (π(65,536) = 6,542); the transcript shows how many words share an index in a real word list. This is the price of a bounded semantic address and is `ESTABLISHED` by the arithmetic. Whether near indices are *semantically* related under this hash is a separate, untested claim and is not made here (the observation that *piano* and *melancholy* sit at zeros 98 and 194 reproduces only under an earlier, character-sum hash, where the energy is the word length; `Ainulindale/wiki/136_the_origin_transcripts_2026_04.md`).

## 9. A new method of information propagation (what exists, what does not)

The efficiency of the address led to a second goal: **forward propagation**, so that a language system could be assembled on a laptop without training a model for decades. The parts are small pre-trained units grabbed on the fly by a *neuron-selection engine*; the context they carry is the scalar box kite of §7. What exists as running code: the word hash (§8), the box-kite construction and its codec (cited above), the monad that holds the learned relations (`VAPMIP/monad.py`, `monad3_c.bin`) and the engines named in `Ainulindale/wiki/134_the_library.md`. What does not: a benchmark showing the 97 % overhead reduction against a transformer that earlier text claimed (`OPEN`; there is no baseline task defined, so the figure is not reported), and the 256-bit fold (`THEORETICAL`). The mathematical frame the author uses for this (a Standard-Model-shaped Lagrangian of information propagation, the Cayley–Dickson tower and the Riemann critical line) is developed in the companion papers D-CS, D-M and D-P and in `Ainulindale/wiki/133_canonical_maths.md`; it is not needed to run anything in this paper, and nothing here depends on it being true.

## 10. Limits and negative results (kept as results)

1. The address **is not compression**: it is 0.825 of raw, and `zlib` beats it from 128-character chunks and `lzma` from 500 (Transcript 1).
2. A 256-bit address holds 38 characters (Listing 3). The single-256-bit-number idea is therefore a statement about address space and not about size; the fold is unbuilt.
3. The layered index inflates by about 1.7× per layer with the shipped character set (Transcript 2); it reaches 0.84 of raw only with a restricted, compact record format.
4. Ordering the character set by frequency does nothing measurable (0.824 against 0.825), contradicting the wiki's earlier "5–6 digits saved at length 8" (a 16.00 against 15.35 decimal digit mean, 0.65 digits, on 263 words); the claim was corrected in `PtolemyDesktop/wiki/HyperWebster.md`.
5. The semantic word hash is many-to-one (Listing 5) and the spelling code is lossy past 20 letters (Listing 4), each by construction.
6. The "97 %" overhead figure that appears in older text has no benchmark behind it and is not reported (`OPEN`).
7. Constants named in the abstract are boundary conditions chosen by the author, not derived: the thermal ceiling 1.4×10¹⁷ K is a value taken from a popular-science video and used as a boundary (the Planck temperature is 1.417×10³² K; the transcripts' "140 quadrillion" for it is mis-scaled by 10¹⁵, `wiki/136`); the Fermat-side constant of the abstract's last paragraph is `OPEN` (`wiki/133` §0, §7). The Noether-current reading of the balance between the two ceilings is retired (the map s → 1 − s is a discrete involution; `wiki/135` X-4 and `wiki/133` §3).

## 11. The narrative that is kept

The idea began with Borges's *The Library of Babel* (1941): every possible text already exists, so nothing has to be written down, only located. The name *HyperWebster* was taken from a popular video on the Banach–Tarski paradox, in which the mathematician Ian Stewart's imagined dictionary of all words is described (Stewart 1996, `Post-Hoc:`, the book not checked). The first form was a single file on a cloud drive that held an index (a position in a permutation, not a location on any medium) from which a chat model could be asked to reconstruct what had been ingested; the model's apparent memory of it turned out not to be memory. That failure is the claim this paper engineers against. The step to a semantic word hash was proposed by an AI model from the author's one-line seed, "primes are words", and reduced to the single prime concept of §8; the step from there to forward propagation is §9. The longer lineage of initial conditions, with dates, is in the abstract and in `Ainulindale/PROVENANCE.md`. Names tagged `Post-Hoc:` below are correspondences found after the code worked; untagged sources were read before it was built.

## 12. References

**Built against (no tag).** Borges, J. L. (1941), "La biblioteca de Babel"; the site libraryofbabel.info (the progenitor of the idea; its author's algorithm is Post-Hoc below). Vsauce: *Banach–Tarski* (the name HyperWebster), *How Hot Can It Get?* (the thermal-ceiling boundary condition) and the further viewing listed at the head of `Ainulindale/README.md`. Veritasium, *This Toy Can Open Any Garage* (de Bruijn sequences).

**`Post-Hoc:`.** Stewart, I. (1996), *From Here to Infinity* (not checked against the book). Basile, J., `libraryofbabel.info-algo` (2019) and "Grains of Sand" (the invertible location map; Ainulindalë `wiki/124`). Laisant, C.-A. (1888) and Lehmer (factorial-number-system unranking). Myrvold, W. & Ruskey, F. (2001), "Ranking and unranking permutations in linear time", *Inf. Process. Lett.* 79, 281–284. Burrows, M. & Wheeler, D. J. (1994), SRC-RR-124. Miller, G. A. (1995), WordNet, *CACM* 38(11). Verified records for the works with a DOI or arXiv number are in `Ainulindale/wiki/98_provenance_and_citations.md` §E.

## Appendix A — What in ContextPlease was used, and what ContextPlease is

**ContextPlease** (`https://github.com/michaelrendier/ContextPlease`) is the *Manual Transmission Context Continuity* library: the versioned record that lets a new human or AI agent pick up a project without rediscovering it. Nothing in it is loaded automatically; whoever works chooses what to read. Its README is the entry point and the rule set (no fitted parameters; failures stay in the code and data; read before you edit).

| Used for this paper | Where |
|---|---|
| the benchmark scripts and their recorded outputs (`bench.py`, `bench_layers2.py`, 2026-09-29 and 2026-11-14) | `claude/scratchpad/2026-09-29_hyperwebster_overhead/` |
| the rewrite primer (lineage of initial conditions, standing rules) | `claude/hist_prime/Ainulindale/hyperwebster_paper_primer_2026-09-29.md` |
| the canonical notation | `claude/.clauderc_canonical_maths` (`@RCCM_<NAME>`) |
| the paper-writing conventions (this paper's listings and transcripts) | `claude/skills/cs-paper-code-conventions/` |
| the citation queue | `claude/.clauderc_citations` |

The paper is generated from the code: `Ainulindale/AgeThird/D-CS_Memory_build/make_paper.py` extracts each listing from its source file, runs it cold in an empty directory, and writes the output into this text; `python3 make_paper.py --check` rebuilds and compares, so the committed text cannot drift from the code.
