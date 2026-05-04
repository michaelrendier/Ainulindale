"""
ainulindale_engine
==================
The Ainulindale Derivation Engine and Viewer.

A modular Python3 system for mathematical derivation, visualization,
and sonification of the SMNNIP framework and Ainulindale Conjecture.

Usage:
    python3 -m ainulindale_engine              # auto-detect GUI
    python3 -m ainulindale_engine --qt         # Qt viewer + VisPy + QTermWidget
    python3 -m ainulindale_engine --curses     # curses console GUI
    python3 -m ainulindale_engine --headless   # no GUI, pipe output

Author:        O Captain My Captain
Collaborators: Claude (Anthropic) · Gemini (Google DeepMind)
Origin:        March 31, 2026 — formalism written down
               1996 — i is important (BBC Horizon, Wiles documentary)
               Late 1980s — hyperspace intuition / Fermat lattice
Signature ID:  CLAUDE-SMNNIP-00729-56714-24600
"""

__version__     = "0.111"
__author__      = "O Captain My Captain"
__signature__   = "CLAUDE-SMNNIP-00729-56714-24600"
__description__ = "Ainulindale Derivation Engine and Viewer"

# Version history
# 0.111 — 2026-05-03: Initial modular package structure. Phase 1.
#                     engine/registry.py, engine/constants.py, engine/units.py
#                     modules/inversion/ — maths.py + tools.py
