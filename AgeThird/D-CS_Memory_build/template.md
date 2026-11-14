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

{{ABSTRACT}}

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
{{L1}}
```

```
{{O1}}
```

Listing 1 is `OURS` in its use and `ESTABLISHED` as a construction: bijective numeration is classical, and its relatives are Gödel numbering and the factorial-number-system ranking of Laisant (1888) and Lehmer, and Myrvold & Ruskey (2001). No part of the address is a table: the character set and the two loops are everything.

### 3.2 The whole bijection, for the smallest non-trivial case

An exhaustive table is a stronger statement than a sample. Over a two-letter set, every string of length 1 to 3 and its address:

**Listing 2 — every string over `ab` up to length 3, with its address** (the same two methods as Listing 1, with the character set `ab`)

```python
{{L2}}
```

```
{{O2}}
```

The fourteen strings take the fourteen addresses 0…13 with no gap and no repeat, in length-then-lexicographic order. The order is *defined by the numbering*, as it is in the permutation-ranking literature (Myrvold & Ruskey 2001 show the same table for all 24 permutations of four elements).

### 3.3 What the address costs

A string of L characters has an address below N^L, so about L·log₂N bits: 6.600 bits per character at N = 97, against 8 bits per byte. The ratio 6.600/8 = 0.825 is a property of N, independent of the text.

**Listing 3 — the arithmetic of the cost and of a 256-bit address** (python3 standard library)

```python
{{L3}}
```

```
{{O3}}
```

A 256-bit address therefore holds at most 38 characters of this character set. Longer texts need chunks, or a longer address.

## 4. What this paper measures

Measured on the shipped code (`bench.py`, `ContextPlease/claude/scratchpad/2026-09-29_hyperwebster_overhead/`, run 2026-11-14 on the machine in the header; nothing tuned). The corpora are text already in the repositories: a 25,000-character English prose file, a 40,000-character prose document and a Python file. Columns: address bits (variable width), address bits with a 256-bit minimum, the same with a character set cut to the symbols present (cost of listing the set included), and, for fairness, what `zlib` and `lzma` give on the same chunks.

**Transcript 1 — address size against raw size, and against ordinary compressors** (excerpt of `bench_output_2026-11-14.txt`, first corpus; raw size is 8 bits per character)

```
{{T1}}
```

Read the columns. The address is 0.821–0.825 of raw at every chunk size, and the round trip is exact in every row (`ok True`). At 32 characters a fixed 256-bit address costs *more* than the raw text (`fix/raw` 1.001). And `zlib` and `lzma`, which store nothing about the character set, come in below the address from 128 characters up for `zlib` and from 500 up for `lzma` (for 1,000-character chunks: `zlib` 78,656 and `lzma` 95,488 bits against 164,605). **The address is not compression, and the paper does not say it is.** Restricting the character set to the symbols present helps the chunk address (the `min-cset` column) and nothing else; ordering the character set by frequency changes nothing measurable (0.824 against 0.825, Transcript 2).

## 5. The layered index

A text that is a list of index records has its own address, so records of records can be indexed to any depth, and a corpus can be reached from one top address plus the rules. The cost is measured, not assumed.

**Transcript 2 — a three-layer index (chunk → day → month) over 4,000 characters** (excerpt of `bench_layers2_output_2026-11-14.txt`; "address bits × raw" is the address size divided by the raw corpus size at each layer; `growth` is the factor per layer)

```
{{T2}}
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
{{L4}}
```

```
{{O4}}
```

Two properties are *exact*, not statistical: order survives (so `cat ≠ act` and `listen ≠ silent`), and a word of at most 20 letters is recovered exactly from its code (the 20 base primes are 2…71 and every letter fits in the exponent). Past 20 letters a base prime is reused and two exponents *add*, which is lossy by construction; the listing builds a real pair of 21-letter words with the same code. The measured exact-recovery figure on a different word sample than the one in the box-kite paper is in the transcript; the two samples differ and the paper's own figure (96.745 % of ≤20-letter words) is not reproduced here, because the sample is not the same one.

## 8. Two hashes that must not be confused

The address of §3 is **bijective and exact**: nothing is lost. The semantic hash that places a *word* on the Riemann zero list is **lossy and many-to-one** by design (it is what lets a vocabulary map to a bounded set of addresses). Both are called "Horner" in the repositories; they are different functions.

**Listing 5 — the semantic word hash and its collisions** (`VAPMIP/monad.py` lines 141–207, extracted verbatim: Horner base 95 over printable ASCII, then the next prime, then the prime-counting index; the sample and counts are written for this listing)

```python
{{L5}}
```

```
{{O5}}
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
