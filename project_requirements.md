# Project Requirements — What This PRoot Needs to Run Cody's Code

Generated 2026-07-08 by scanning `.claude/.clauderc_file_structure` for all
`.py`/`.c`/`.h`/Android files under ThePlace, cross-referenced against
actual `import`/`#include` statements in each file. **Nothing in this
document has been installed yet** — this is the list to review before
anything is installed. Method and confidence level are noted per section
so it's clear what's a hard fact vs. an inference.

**UPDATE 2026-07-08 (later same day):** `Ptolemy2/` and `TheWanderingGod/`
were deleted from this device to free ~7.1GB (both remain backed up on the
dead laptop's NVMe, in an enclosure, not yet readable from this phone).
Every mention of `Ptolemy2/...` below is a description of what the scan
found BEFORE that deletion — kept as-is for the historical/architectural
record (e.g. "Ptolemy2/Tesla/PtolDroid was an earlier Kivy-based Android
prototype" is still useful to know), but none of those paths currently
exist on this device, and the vendored-code install guidance for them is
moot until the NVMe is recoverable.

---

## Scope

8,491 `.py`/`.c`/`.h`/Android files exist under ThePlace. **6,375 of those
(86%, all under `Ptolemy2/technical/sourcebuilds/` and
`Ptolemy2/technical/examples/`) are vendored third-party reference
material** — downloaded example/source dumps (Kivy, PyQt5 demos,
cmusphinx/sphinx4, ChatterBot, dualscope123, learnopencv, Zork Z-Machine,
etc.), not code Cody wrote. This document scopes to the **1,524 primary
files** (1,440 Python, 84 C/H) across the actual research repos + Android
project. If you want the vendored bulk scanned too, say so — it's a much
bigger, lower-value pass (mostly abandoned/reference code, not run
day-to-day).

Primary-file breakdown by repo:

```
582  PtolemyDesktop   (Eleven Faces: Callimachus, Mouseion, Archimedes, Pharos,
                        Phaleron, Philadelphos, PtolC, Tesla, Kryptos, PtolFlutter,
                        Aule, Alexandria, Mandos, Anaximander + working/, Archive/)
147  AinulindaleBAK    (STALE — superseded snapshot, see .clauderc_context_1;
                        lower priority unless specifically needed)
132  ValaQuenta        (the canonical derivation engines)
131  VAPMIP            (ptol.c + monad.py + UDEO_monad.py + skills/)
 45  PTorrent          (Android app: Kotlin + Chaquopy Python bridge)
 22  FourthAgePapers   (paper engines, incl. CryptoVulnerability/)
 22  ArdaQuenta        (VCDS-styled Qt viewer)
 18  BulletCluster     (JWST/Chandra/MeerKAT analysis pipeline)
  8  SedenionSpectralRelativity
  7  AbrikosovTree
  4  TuringStack       (UDEO public disclosure mirror + GPI-1)
  3  Ainulindale       (mostly docs, near-zero code — this is the "Music," not the "Engines")
  2  SemanticWordEngine
  1  RiemannHypothesisProof (+ notebooks, not counted here)
    (DeriveCancerDrugs, MedicineIsAlwaysFree, POE, UniversalSynth: no
     primary .py/.c files matched — POE and UniversalSynth are hardware-
     spec/design-doc repos with no code yet; Derive/Medicine are docs-only)
```

---

## Already fixed / already installed this session (don't redo)

- `apt`-based Python is now on PATH (`/usr/bin/python3`, 3.14.4) — previously
  `python3` silently fell back to a slow Termux build. **Always confirm
  `which python3` resolves to `/usr/bin/python3` before installing anything**
  — if it drifts back to the Termux path, from-source numpy builds will
  stall again like they did earlier this session.
- Already installed via apt (prebuilt binaries): `python3-numpy`,
  `python3-astropy`, `python3-requests`, `jq`, `git`.
- Already installed via pip (`--break-system-packages`, fast since deps were
  satisfied): `astroquery` (pulled in `beautifulsoup4`, `cryptography`,
  `lxml`-adjacent deps, `keyring`, `pyvo` as transitive deps — see current
  installed-package check below).
- `gcc`/`make` already present (Ubuntu 15.2.0 toolchain) — no C toolchain
  install needed.
- Currently installed and importable, confirmed by direct check: `numpy`,
  `scipy`, `PIL`, `bs4`, `requests`, `astropy`, `astroquery`, `cryptography`.
  Everything else below is confirmed **missing**.

---

## Python — core packages actually needed (high confidence)

Grouped by what pulls them in. Version pins are from repos' own existing
`requirements.txt` where one exists; unpinned otherwise.

**GUI / visualization** (PtolemyDesktop, ArdaQuenta — several Faces, largest single category):
```
PyQt5>=5.15        # ArdaQuenta pin; also PtolemyDesktop's primary GUI toolkit
PyQt6               # newer Faces / newer code paths use this instead of PyQt5 — check which per-Face
vispy>=0.12          # ArdaQuenta pin — 16-channel sedenion GLSL canvas
pyqtgraph>=0.13      # ArdaQuenta pin — equation plotter
matplotlib>=3.7      # ArdaQuenta pin; also BulletCluster plots, notebooks generally
OpenGL               # PyOpenGL — Archimedes/rendering
mathutils, bpy       # Blender's OWN bundled Python API — NOT pip-installable;
                     #   needs actual Blender installed, used by AbrikosovTree's blender/ scripts
```

**Math / science** (ValaQuenta, VAPMIP, BulletCluster, RiemannHypothesisProof, SemanticWordEngine):
```
scipy                # already installed
sympy                 # RiemannHypothesisProof notebooks, ValaQuenta
mpmath>=1.3.0         # SemanticWordEngine pin — arbitrary-precision Riemann zeros
pandas
h5py, healpy, reproject, sep, skimage  # astronomy stack — BulletCluster specifically
```

**Astronomy data access** (BulletCluster — this repo needs the most beyond stdlib):
```
astropy               # already installed
astroquery            # already installed
RMtools_1D            # pip name: RM-Tools — Faraday rotation synthesis,
                       #   BulletCluster/engine/modules/transect.py imports this directly
                       #   and it's NOT installed yet — needed for the actual RM falsification test
```

**NLP / text**:
```
nltk>=3.8.0           # SemanticWordEngine pin, also PtolemyDesktop hyperwebster paths
spacy                  # PtolemyDesktop requirements_acquire.txt lists as "optional future"
lxml>=4.9.0            # PtolemyDesktop pin — faster HTML parsing than bs4
beautifulsoup4         # already installed (as bs4)
polyglot
```

**Web / scraping / APIs**:
```
requests>=2.31.0       # already installed
flask, django, wagtail, mezzanine, feincms   # Mouseion Face (web/CMS experiments)
flask_wtf, flask_login, flask_admin, flask_bootstrap, flask_ckeditor,
  flask_menu, flask_mysqldb, wtforms, werkzeug   # Flask ecosystem, Mouseion Face
selenium, chardet, certifi, html2text, pdfminer.six, pdf2image, pdfkit,
  python-docx, EbookLib, odfpy, openpyxl, qrcode  # Phaleron Face (document/discovery tooling)
googlemaps             # Anaximander Face (spatial/geolocation)
cherrypy, pymysql, mysqlclient (MySQLdb)   # Mouseion Face alt web stack
```

**AI API clients** (real, current, worth getting right):
```
anthropic               # PtolemyDesktop/Philadelphos/Ainur/ainur.py — Claude API client
google-generativeai      # older Gemini SDK form (`import google.generativeai`)
google-genai              # newer Gemini SDK form (`from google import genai`) — BOTH
                           #   forms appear in the codebase across different files; check
                           #   which specific files need which before installing just one
```

**Hardware / audio / signal** (Tesla Face, POE-adjacent, VAPMIP sonification):
```
pyaudio, sounddevice, soundfile, speech_recognition, striprtf, espeak
rtlsdr                    # pip name: pyrtlsdr — VAPMIP/lshs_sdr.py, SDR radio bridge,
                           #   connects to POE's radio/antenna hardware work
netmiko                   # network device automation — likely POE vehicle-interface adjacent
psutil
```

**Game/roguelike** (found under Ptolemy2/working and/or PtolemyDesktop, tcod-tutorial-shaped
module set: game_states, game_messages, entity, map_objects, death_functions, fov_functions,
input_handlers, item_functions, render_functions, loader_functions are LOCAL files, not pip —
only tcod itself is external):
```
tcod                     # python-tcod, roguelike/libtcod bindings
```

**ML / vision** (present, unclear how load-bearing vs. experimental):
```
tensorflow, torch, cv2 (opencv-python), whisper (openai-whisper), skimage
```

**Misc real deps**:
```
pytest                   # test running
kivy                      # PtolDroid / earlier Android prototypes (Ptolemy2/Tesla/PtolDroid,
                           #   PtolemyDesktop/Tesla/PtolDroid) — distinct from the Chaquopy-based
                           #   PTorrent Android app, an EARLIER/alternate Android approach
jnius                     # pyjnius, Kivy's Android/Java bridge — pairs with kivy above
PyInquirer, prettytable, colorama, future, regex, imutils, moderngl, glfw,
  vpython, memory_profiler, guestfs, Xlib (python-xlib), chatterbot
```

---

## Long tail — extracted but not individually verified

The automated import scan surfaced ~180 candidate external names total.
The list above covers the ones I could confidently identify and place.
The remainder includes real-but-minor packages I didn't chase down
(`getch`, `uinput`, `magic`/`python-magic`, `keyring` transitive deps,
`qtermwidget`/`QTermWidget` — this last one is a **C++ Qt widget, not a
pip package**, PtolemyDesktop's own INSTALL.md says it "requires CMake
build from source") mixed with a handful of likely false-positives from
my regex matching prose inside docstrings/comments that happened to start
a line with "from X" or "import X" (e.g. single-hit oddities like `above`,
`hood`, `trunk`, `two`). I did not hand-verify every one of the ~180 — flag
anything specific you want confirmed and I'll check it against the actual
file.

---

## C build dependencies

Only 3 repos have C code: VAPMIP (34 files — `ptol.c` and friends, the
active engine), PtolemyDesktop (35 files), Ptolemy2 (15 files, mostly
older/parallel versions of the same).

**VAPMIP specifically** (the one actively worked on) needs, beyond
standard libc (already fine — `gcc`/`make` present):
```
libxml2-dev     # ptol.c's filesystem-ingest PDF/HTML extraction (libxml/HTMLparser.h,
                #   parser.h, tree.h) — NOT currently installed
```
Links against `-lm` (math, standard) and `pthread.h` (needs `-lpthread` at
link time, header itself ships with libc6-dev, already present).

**PtolemyDesktop + Ptolemy2's C code** additionally reference, across
various older/Face-specific files:
```
libgtk-3-dev       # gtk/gtk.h
libglfw3-dev        # GLFW/glfw3.h
tcl-dev, tk-dev      # tcl.h, tk.h
```
Plus `flutter/dart_project.h` etc. (PtolFlutter) — that's the Flutter SDK
itself, not an apt package, and `windows.h`/`windowsx.h` references are
Windows-only code paths, irrelevant on this device.
`wn.h` (WordNet C library header) appears once — would need
`wordnet-dev`/`libwn-dev` if that specific file is ever built.

---

## Android (PTorrent — the one real, current Android project)

This is a heavier lift than anything above — not a pip/apt install, a full
SDK toolchain:

```
compileSdk 35, minSdk 26, targetSdk 35
JDK 17 (compileOptions sourceCompatibility/targetCompatibility)
Kotlin (org.jetbrains.kotlin.android plugin)
Chaquopy plugin (com.chaquo.python) — bridges Python 3.12 into the APK;
  monad.py is stated stdlib-only, "no pip dependencies" per the build.gradle's own comment
NDK, abiFilters "arm64-v8a", "x86_64"
Standard AndroidX deps (core-ktx, appcompat, material, constraintlayout,
  lifecycle-*, preference-ktx, cardview) — resolved automatically via Gradle/Maven,
  not a manual install, just needs network access (already confirmed working)
```

**Known blocker if you try to build this here**: `build.gradle` hardcodes
`buildDir = "/home/rendier/ptolemy_build/PTorrentSeeder"` — the laptop's
home directory. Same category of problem as the JWST download script
fixed earlier this session (laptop-absolute-path baked into a script/config).
Would need the same kind of workaround (patched copy or an override) before
a build could run on this device. Not attempted yet.

Two OLDER, apparently-abandoned Android prototypes also exist
(`Ptolemy2/Tesla/PtolDroid`, `PtolemyDesktop/Tesla/PtolDroid`) — Kivy-based
rather than Chaquopy-based, i.e. a different, earlier approach to the same
goal. Not clear if these are still meant to be buildable — flagged, not
investigated further.

---

## Suggested install order, if/when you say go

1. `libxml2-dev` (apt) — unblocks VAPMIP's `ptol.c` build immediately, cheap.
2. Core Python stack: `mpmath nltk lxml pandas sympy` (apt-first where
   possible — `python3-sympy`, `python3-pandas`, `python3-lxml` all likely
   have prebuilt arm64 debs like numpy/astropy did, worth checking before
   pip to avoid another from-source stall).
3. `RM-Tools`, `matplotlib`, `pyqtgraph` — unblocks BulletCluster's actual
   analysis code now that the JWST data is in place.
4. PyQt5/PyQt6/vispy — only if you want to run the GUI Faces / ArdaQuenta
   viewer on this device (heavier, and a phone PRoot may not have a usable
   display target for a Qt app at all — worth confirming that's even the
   goal before installing a large GUI stack).
5. Everything else, on demand, as you actually hit an ImportError running
   something specific — installing all ~40 remaining packages speculatively
   isn't worth it if most of this code isn't run day-to-day.

Nothing above has been installed. Waiting for your review.
