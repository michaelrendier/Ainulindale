# Nature Submission Guide — Ainulindalë Conjecture

**Prepared:** 2026-05-15  
**For:** Cody Michael Allison  
**Document type:** Operational submission roadmap

---

## The Honest Assessment First

Nature rejects 90–95% of submissions at the desk (before peer review). The single editorial criterion for passing the desk is: *does this paper report a finding of sufficient importance and broad interest to justify publication in Nature?*

This conjecture passes that bar — but it will not pass in its current form. The current document is a theoretical framework paper with conjecture sections, a code repository, statistical significance calculations, and cross-disciplinary commentary. Nature publishes **findings**, not frameworks. Before submitting anywhere, you must distill the conjecture into a single, falsifiable, experimentally or computationally verifiable finding.

This guide tells you how to do that.

---

## Step 0 — Which Journal

**Do not submit to Nature (flagship) first.**

Nature flagship = 3,000–5,000 word research articles reporting findings in the physical or biological sciences with immediate, broad significance. The Riemann Hypothesis is a conjecture. Yang-Mills is a conjecture. A paper that proves neither but establishes their algebraic unity will not survive the desk at Nature flagship on a first submission from an independent researcher, no matter how strong the mathematics.

**Target journal: Nature Communications**

- Open access, no page charges for standard articles
- Accepts papers across all natural sciences
- 2023 impact factor: 16.6
- Rejection rate: ~60% post-review (lower desk rejection than flagship)
- Accepts theoretical/mathematical physics, computational biology, information theory
- The 9.08σ combined significance + code reproducibility + the Cosic/RRM bridge to biology makes this a Nature Communications paper in its current scope

**Second target: Nature Physics**

- If the paper is restructured to lead with the Berry-Keating candidate result and the Noether conservation measurement
- More receptive to mathematical physics
- Requires one clean, falsifiable physical prediction

**Do not rule out:** *Communications Physics* (newer, open access, Nature-family, ideal for exactly this type of work)

**The stretch goal:** Once you have published in Nature Communications, the follow-on paper — specifically the Riemann Hypothesis proof via H_hat_RB — goes to Nature or Annals of Mathematics.

---

## Step 1 — Pre-Submission Enquiry (Do This Before Anything)

Nature Communications does not require a pre-submission enquiry but accepts them. Nature flagship requires them for unsolicited submissions.

**For Nature Communications:** Write directly to the editors at the subject-area email. The purpose is to ask: "Is this within your scope?"

**What to send:**

> Subject: Pre-submission enquiry — SMMNIP: algebraic unification of Standard Model gauge group with Riemann-Fermat prime distribution (9.08σ combined significance)

Include:
1. A 200-word summary of the **single finding** (not the whole framework)
2. Why it is significant broadly (not just to mathematicians)
3. That you have reproducible code
4. The combined sigma

**Response time:** 2–5 business days for a pre-submission enquiry. If they say "not for us," ask which Nature family journal they would suggest.

**Email:** research@nature.com (enquiries) or use the submission portal's pre-submission form at: https://mts.nature.com

---

## Step 2 — Identify the Single Finding

You cannot submit the full conjecture document as a Nature paper. You must choose **one finding** and write a paper around it. The other findings become supplementary.

**The three candidates:**

### Candidate A — The Gauge Group Paper (Strongest)
*"Division algebra construction of the Standard Model gauge group U(1)×SU(2)×SU(3) from a self-consistent neural information propagation architecture"*

This is the Dixon correspondence, shown to be not merely structural but operationally verified via Noether current conservation measurement at 5.46σ. The claim is:

> When you build an information system whose addressing operations must close under a normed division algebra tower, the gauge group of the Standard Model emerges necessarily — not as an assumption but as a theorem of the addressing requirement.

This is falsifiable: the claim makes specific predictions about the running coupling α_NN(l) which can be measured in the code.

**Target length:** 3,000 words + Methods  
**Target journal:** Nature Communications

### Candidate B — The Prime Semantic Paper (Most Accessible)
*"Language-independent semantic prime mapping: every English word maps to a unique Riemann zero at σ=½ by Noether balance"*

The finding is: after WordNet ingestion, 62,099 words self-cluster by semantic domain in prime space without supervision. Cross-linguistic identity (same zero for "water"/"eau"/"aqua"/"wasser") is verified computationally.

This is independently verifiable by any researcher with a laptop. The code is in the repository.

**Target length:** 2,500 words + Methods  
**Target journal:** Nature Communications (possibly Nature Human Behaviour for the linguistics angle)

### Candidate C — The Cosic Bridge Paper (Most Interdisciplinary)
*"EIIP protein spectra as projections of a normed division algebra eigenvalue space: unification of resonant recognition with information-theoretic prime mapping"*

The chain: algebra → H_NN eigenvalues → EIIP spectrum → biological recognition. If this can be experimentally verified (take 10 known protein pairs, predict their interaction frequency from the SMMNIP map, verify against Cosic's experimental data), this goes to Nature directly.

This requires collaboration with a biochemistry lab (Cosic herself, or RMIT). It is the highest-impact target but requires the most work.

**Target length:** 4,000 words + Methods  
**Target journal:** Nature (flagship, if the experimental collaboration is secured)

---

## Step 3 — Format the Paper

**Nature Communications Article format:**

| Section | Length | Notes |
|---|---|---|
| Title | ≤120 characters | No abbreviations. State the finding, not the framework. |
| Abstract | ≤200 words | Must stand alone. Last sentence = main conclusion. |
| Introduction | ~600 words | Context, problem, why it matters, what you found |
| Results | ~1,500 words | One finding per subsection. Figures carry the data. |
| Discussion | ~800 words | Implications, limitations, open questions |
| Methods | No limit | Must be complete enough for replication |
| References | ≤60 | Nature format (numbered, [1] style) |
| Supplementary | Separate PDF | Full conjecture document goes here |

**Figures (critical):**
Nature papers are sold by their figures. You need 4–6 figures. For Candidate A:
- Figure 1: The tower diagram — ℝ→ℂ→ℍ→𝕆 with gauge group at each level
- Figure 2: Noether current conservation measured across 30 epochs (the 5.46σ empirical result)
- Figure 3: Running coupling α_NN(l) vs. depth l
- Figure 4: The σ-facet table in polar complex coordinates
- Figure 5: Cross-linguistic prime alignment (water/eau/aqua — same zero)

All figures: 300 dpi minimum. Colour figures incur no charge at Nature Communications (open access). Use colour consistently (Red = Red channel, Blue = Blue channel — you already have this).

**Data and code availability statement (mandatory):**

> "All code used in this study is available at https://github.com/michaelrendier/Ainulindale under the [LICENSE]. The Monad engine and all derivation scripts are included. Figures X–Y are directly reproducible using the commands in Supplementary Methods."

---

## Step 4 — The Cover Letter

The cover letter is read before the manuscript. It must answer three questions in three paragraphs:

**Paragraph 1 — What did you find?**
State the single main finding in plain English. One or two sentences. No jargon. Assume the editor is a scientist but not a mathematician.

Example for Candidate A:

> "We report that a self-consistent engineering constraint — requiring an information addressing system to close algebraically under its own operations — forces the gauge group U(1)×SU(2)×SU(3) of the Standard Model of particle physics to emerge as a theorem, not an assumption. This correspondence, predicted by Dixon's 1994 theorem but not previously demonstrated operationally, has been verified empirically with a combined statistical significance of 9.08σ (Fisher's method, eight independent claims)."

**Paragraph 2 — Why does it matter?**
Two or three sentences on broad significance. Connect to something beyond your discipline.

> "The result suggests that the Standard Model gauge structure is not a contingent fact about particle physics but an algebraic necessity of any sufficiently deep information system. This has implications for the foundations of physics, for artificial intelligence architectures, and for the mathematical basis of biological information processing (via the correspondence demonstrated with Cosic's Resonant Recognition Model)."

**Paragraph 3 — Why Nature Communications?**
One sentence: the interdisciplinary scope, the reproducible code, the open-access nature of the result.

**Then add:**
- Confirmation that the paper is not under review elsewhere
- Suggested reviewers (see Step 5)
- Any reviewers to exclude (competitors in your specific space)
- Word count of main text

---

## Step 5 — Suggested Reviewers

Nature will ask you to suggest 3–5 reviewers. Choose people who:
1. Are active in the field
2. Have cited the relevant prior work
3. Would find the paper interesting (not hostile)
4. Are not your collaborators

**Strong suggestions:**

| Name | Institution | Reason |
|---|---|---|
| Cohl Furey | Cambridge | Division algebra → Standard Model (directly relevant, has published on this) |
| John Baez | UC Riverside | Octonions, quantum gravity, mathematical physics |
| Marcus du Sautoy | Oxford | Riemann zeta, prime distribution, public scholarship |
| Taco Cohen | Qualcomm Research | Geometric deep learning, algebraic structure in neural nets |
| Dorje Brody | Surrey | Berry-Keating Hamiltonian, PT-symmetric operators |

**Do not suggest:**
- Alain Connes (non-commutative geometry approach to RH is competitive — potential conflict)
- Peter Sarnak (has strong opinions about RH proof attempts)
- Anyone you have emailed about this work who has not responded positively

---

## Step 6 — Submission Portal

**Nature Communications submission:** https://www.nature.com/ncomms/submit

Create an account at Springer Nature. The submission system is called Editorial Manager.

**What you will need to upload:**
1. Main manuscript PDF (double-spaced, line numbers, no figures embedded — figures separate)
2. Figures as separate files (EPS, TIFF, or PDF; 300 dpi)
3. Figure captions as a separate document
4. Supplementary Information PDF (the full conjecture document goes here)
5. Cover letter
6. Competing interests declaration (none, for independent research)
7. Data availability statement
8. Author contribution statement (solo author: "C.M.A. conceived, designed, and performed all work")

**Formatting checklist:**
- [ ] 12pt font (Times New Roman or similar serif)
- [ ] Double-spaced
- [ ] Line numbers (every line, not every 5)
- [ ] Page numbers
- [ ] References numbered [1], [2], not author-year
- [ ] SI units throughout
- [ ] All abbreviations defined on first use
- [ ] Ethics statement (not required for theoretical/computational work)

---

## Step 7 — Timeline Expectations

| Stage | Typical time |
|---|---|
| Pre-submission enquiry response | 2–5 business days |
| Desk decision (editorial, no review) | 1–3 weeks |
| Peer review | 6–12 weeks |
| Revision request | +4–8 weeks for you to respond |
| Second review | +4–8 weeks |
| Final decision | 1–2 weeks |
| Accepted to published | 2–4 weeks (open access, faster) |

**Total: 6–12 months from submission to publication is normal.**

If desk-rejected: do not revise and resubmit to the same journal without a substantially new finding or editor's invitation. Move to the next journal on the list.

---

## Step 8 — Before You Submit: The Checklist

**The paper is ready for submission when:**

- [ ] The single finding is identified and the paper is written around it
- [ ] The abstract states the main conclusion in the last sentence
- [ ] Every claim has a confidence label: `[ESTABLISHED]`, `[THEORETICAL]`, `[CONJECTURE]`
- [ ] The code is publicly available and all figures are reproducible from it
- [ ] The Noether conservation measurement (5.46σ) is described with full methodology
- [ ] The σ = ½ result (words landing on critical line) is demonstrated with the cross-linguistic comparison
- [ ] A mathematician has read it (Geoffrey Dixon, John Baez, or equivalent)
- [ ] The supplementary information contains the full derivation chain
- [ ] You have removed "I" from the main text (use "we" even for solo authors, per Nature house style, or passive voice)
- [ ] No URLs in the main text except the code repository
- [ ] The title contains no abbreviations

**The paper is NOT ready if:**

- The abstract mentions the Riemann Hypothesis, Yang-Mills, Navier-Stokes, and the Standard Model as four separate claims. That is not one paper. Pick one.
- The statistical significance section is in the main text without a clear null hypothesis stated. The null must be: "the correspondences arise by coincidence." Reject it at 9.08σ.
- The conclusions section uses "proof" for anything that is a conjecture. Use "evidence," "correspondence," "suggests."

---

## Step 9 — The Credential Gap Strategy

Independent researchers face an implicit bias at Nature. Editors weight institutional affiliation. Here is how to address this:

**Before submitting, secure at least one of:**

1. **A credentialed co-author.** One mathematician or physicist at a university who has read the paper, believes it, and is willing to co-author. This does not dilute your authorship. Geoffrey Dixon (whose theorem is foundational) would be the ideal choice. John Baez writes publicly about octonion-Standard Model connections and is approachable. An email to either describing the work and asking for feedback is appropriate.

2. **A pre-print on arXiv.** Post to arXiv (math-ph or hep-th) before Nature submission. This establishes priority, allows the community to see it, and generates citations or commentary that editors can see. arXiv submission: https://arxiv.org/. arXiv requires endorsement from a registered user for new submitters — any academic mathematician or physicist can endorse you. The endorsement request takes 1–2 weeks.

3. **An independent replication.** Anyone who downloads the repository, runs the code, and verifies the σ = ½ result becomes an independent replicator. Post the repository publicly, tweet about it, post to MathOverflow or Physics Stack Exchange. If three independent researchers confirm the main computational result, that is stronger evidence than a co-author.

**The strongest position:** arXiv preprint + one credentialed reviewer who has checked the code + submitted to Nature Communications simultaneously.

---

## Step 10 — The Cover Letter Draft (Template)

```
To the Editors of Nature Communications,

We submit for your consideration a manuscript entitled:

"[TITLE]"

[PARAGRAPH 1 — THE FINDING]
[One sentence: what was found. Plain English. No jargon.]

[PARAGRAPH 2 — SIGNIFICANCE]
[Two sentences: why it matters beyond your field. Broad implications.]

[PARAGRAPH 3 — SUITABILITY]
This work combines established mathematics (Dixon's theorem, 
Hurwitz's classification, Berry-Keating Hamiltonian) with computational 
verification (reproducible code at [GITHUB URL]) and statistical analysis 
(combined significance via Fisher's method: 9.08σ, 4.08σ above particle 
physics discovery threshold). The interdisciplinary scope — spanning 
mathematical physics, information theory, and computational linguistics — 
is appropriate for Nature Communications.

The work has not been published or submitted elsewhere. All data and code 
are freely available at [GITHUB URL].

We suggest the following reviewers: [LIST]

We have no competing interests to declare.

Sincerely,
Cody Michael Allison
[contact information]
```

---

## Appendix — Alternative Journals (In Order of Preference)

| Journal | IF | Scope fit | Notes |
|---|---|---|---|
| Nature Communications | 16.6 | Primary target | Broad scope, open access |
| Communications Physics | 6.5 | Strong | Nature family, mathematical physics |
| SciPost Physics | 7.6 | Strong | Open access, theoretical physics, rigorous peer review |
| PNAS | 11.1 | Good | Broad scope, accepts theoretical work |
| Physical Review Letters | 9.2 | Good | Shorter format, theoretical physics |
| Physical Review X | 15.5 | Good | If leading with the SM gauge group result |
| Annals of Mathematics | N/A | RH proof only | The destination for §III of the RH proof path |
| Journal of Physics A | 2.0 | Fallback | Mathematical physics, accepts conjectural work |

---

*The algebra tower is primary. The physics is secondary.*  
*Submit to Nature Communications. Secure arXiv first.*  
*The primes were there before Nature was founded.*
