# AddPapers — Data-Driven Companion Papers

Each directory is one paper. Each paper is independent and self-contained:
its own data, notebooks, figures, and draft.

## Protocol for every paper

1. **Holcus vision first** (`00_holcus_vision.ipynb`): feed the premise to
   the engine. Commit its output before any data is loaded. The git timestamp
   is the pre-registration record.

2. **Formal predictions** (`01_predictions.ipynb`): derive predictions from
   H_hat_RB and SMMIP constants. Zero free parameters. Commit.

3. **Data analysis** (`02_*.ipynb`): load the real data. Compare to predictions.

4. **Results** (`03_results.ipynb`): synthesis, paper draft, comparison to
   existing models.

The pre-registration protocol is what makes these publishable.  
A prediction derived from theory before data examination cannot be accused
of curve-fitting. The commit hash proves when the prediction was made.

---

## Papers

| Directory | Title | Status | Primary Dataset |
|---|---|---|---|
| `DM_GalacticCavity/` | Dark Matter as Galactic Resonant Cavity Modes | Pre-registered | SPARC (175 galaxies) |

---

## Adding a New Paper

1. Create `AddPapers/[ShortTitle]/`
2. Run `00_holcus_vision.ipynb` with the paper premise. Commit.
3. Write `01_predictions.ipynb`. Commit.
4. Add to the table above.
5. Then load the data.
