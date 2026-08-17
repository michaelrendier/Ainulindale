"""
ainulindale_engine.modules.sedenion.tools
==========================================
SedenionModule — registry contract for the Emmy Noether Sedenion Engine.

Equations:
  1. prompt_encode       text → 16D sedenion (the prompt IS the sedenion)
  2. stress_energy       T_μν stress-energy tensor (16×16, 256 entries)
  3. noether_scan        16D Noether conservation check across turns
  4. fermat_scan         Fermat lattice / zero divisor proximity
  5. monad_interface     interface weights → H_hat_RB / monad.speak()
  6. cd_projection       Cayley-Dickson tower reduction (ℝ→ℂ→ℍ→𝕆→𝕊)

Architecture: Sedenion = Prompt encoder.  H_hat_RB = Field response.
  They run side by side, sharing only the monad_interface weights.
  The sedenion selects the conversational geometry; H_hat_RB resolves it.

Version: 0.111
"""

import math
from typing import Dict, List, Any, Optional

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    encode_prompt, stress_energy_tensor, stress_energy_summary,
    noether_charges, noether_conservation, fermat_lattice_scan,
    monad_interface, cd_projection, full_analysis,
    sed_norm, ALG_NAME, GAP,
)
from .dimensions import DIMENSIONS, DIM_BY_INDEX


class SedenionModule(EquationModule):
    """
    Emmy Noether Sedenion Engine.

    The sedenion IS the prompt.  The H_hat_RB Hamiltonian IS the response.
    These two engines run side by side; the sedenion selects which
    conversational dimensions are active, H_hat_RB resolves the field.

    Equations cover the full physics: prompt encoding, stress-energy tensor,
    Noether conservation, Fermat lattice (zero divisor) detection, CD tower
    projection, and the monad interface.
    """

    # Internal state: the last sedenion (for conservation across calls)
    _prev_text: Optional[str] = None

    @property
    def name(self): return 'sedenion'

    @property
    def display_name(self): return 'Emmy Noether Sedenion Engine  𝕊  16D'

    @property
    def version(self): return '0.111'

    @property
    def description(self):
        return (
            'The sedenion IS the prompt; H_hat_RB IS the response. '
            '16D Cayley-Dickson algebra (e₀..e₁₅) maps to 16 conversational '
            'dimensions: gematria, word-edge, noun, verb, descriptive, predicate, '
            'temporal, pronominal, discourse threads, anaphor, presupposition, '
            'gestalt, affect, meta. '
            'Stress-energy tensor T_μν (256 entries) sources the Hamiltonian. '
            'Zero divisors on S¹⁵ = Fermat lattice = last scattering surface. '
            'Interface weights gate the monad\'s J^μ speak pipeline.'
        )

    @property
    def confidence_floor(self): return 'THEORETICAL'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='prompt_encode',
                display='Prompt → Sedenion  (prompt IS the sedenion)',
                latex=r's = \sum_{k=0}^{15} \phi_k(w_i)\, e_k,\quad |s|=1',
                radian_form='s_k = Σ_words feature_k(w) / n_words; normalised to unit sphere',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text'],
                compute=None,
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='stress_energy',
                display='T_μν — Sedenion Stress-Energy Tensor (16×16)',
                latex=r'T_{\mu\nu} = s_\mu \cdot \bar{s}_\nu,\quad \mathrm{Tr}(T) = |s|^2',
                radian_form='T[i][j] = s[i] * conj(s)[j]; diagonal = Noether charges J_k',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text'],
                compute=None,
                display_options=['text', '3d_cartesian'],
            ),
            Equation(
                name='noether_scan',
                display='16D Noether Conservation  ∂_t J_k = 0',
                latex=r'\partial_t J_k = 0,\quad J_k = s_k^2,\quad \Delta J = \frac{1}{16}\sum_k|J_k^{(t)}-J_k^{(t-1)}|',
                radian_form='violation = mean |s_k^2 - s_prev_k^2| over k=0..15',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text', 'prev_text'],
                compute=None,
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='fermat_scan',
                display='Fermat Lattice — Zero Divisor Detection on S¹⁵',
                latex=r's \cdot t = 0,\quad s,t \neq 0 \Rightarrow \text{Fermat lattice point}',
                radian_form='probe s against 15 basis elements; fermat_proximity = 1 - |st|/(|s||t|)',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text'],
                compute=None,
                display_options=['text'],
            ),
            Equation(
                name='monad_interface',
                display='Sedenion → Monad Interface  (psi_norms for H_hat_RB)',
                latex=r'\psi_k = \sqrt{J_k} = |s_k|,\quad \text{monad.affect} = \psi_{14}',
                radian_form='psi[k] = |s_k|; affect_weight = psi[14]; gestalt = psi[13]',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text'],
                compute=None,
                display_options=['text'],
            ),
            Equation(
                name='cd_projection',
                display='Cayley-Dickson Tower Projection  ℝ → ℂ → ℍ → 𝕆 → 𝕊',
                latex=r's \big|_{\mathbb{A}} = \sum_{k \in A} s_k e_k,\quad A \in \{\mathbb{R},\mathbb{C},\mathbb{H},\mathbb{O},\mathbb{S}\}',
                radian_form='project s onto sub-algebra A by zeroing components outside A',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text', 'stratum'],
                compute=None,
                display_options=['text', '3d_cartesian'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in sedenion module")

        text      = str(params.get('text', ''))
        prev_text = params.get('prev_text', self._prev_text)

        if equation_name == 'prompt_encode':
            s      = encode_prompt(text)
            result = {
                'sedenion'   : s,
                'norm'       : sed_norm(s),
                'components' : {DIM_BY_INDEX[k].name: round(s[k], 6)
                                for k in range(16)},
                'dominant'   : DIM_BY_INDEX[
                    max(range(16), key=lambda k: abs(s[k]))
                ].label,
            }

        elif equation_name == 'stress_energy':
            s   = encode_prompt(text)
            T   = stress_energy_tensor(s)
            tsm = stress_energy_summary(T)
            result = {
                'trace'            : tsm['trace'],
                'max_off_diagonal' : tsm['max_off_diagonal'],
                'dominant_coupling': tsm['dominant_coupling'],
                'n_active_dims'    : tsm['n_active_dims'],
                'diagonal'         : {DIM_BY_INDEX[k].name: round(T[k][k], 6)
                                      for k in range(16)},
            }

        elif equation_name == 'noether_scan':
            s_prev = encode_prompt(str(prev_text)) if prev_text else None
            s_now  = encode_prompt(text)
            result = noether_conservation(s_now, s_prev)
            self._prev_text = text

        elif equation_name == 'fermat_scan':
            s      = encode_prompt(text)
            result = fermat_lattice_scan(s)

        elif equation_name == 'monad_interface':
            s      = encode_prompt(text)
            result = monad_interface(s)

        elif equation_name == 'cd_projection':
            s       = encode_prompt(text)
            stratum = int(params.get('stratum', 4))
            result  = cd_projection(s, stratum)

        else:
            result = {'note': 'no compute path'}

        return {'equation': eq, 'params': params, 'result': result,
                'module': self.name}

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)
        r = result['result']

        if display_mode == 'text':
            return {'text': self._fmt(equation_name, r)}
        elif display_mode == 'complex_plane':
            return self._complex_data(equation_name, params, r)
        elif display_mode == '3d_cartesian':
            return self._3d_data(equation_name, params, r)

        return {'text': self._fmt(equation_name, r)}

    def _fmt(self, name: str, result) -> str:
        if isinstance(result, dict):
            lines = [f'  {name}']
            for k, v in result.items():
                if k in ('sedenion', 'J', 'J_prev', 'psi_norms',
                         'J_charges', 'dim_labels', 'hits'):
                    continue  # handled below
                if isinstance(v, float):
                    lines.append(f'  {k:24s} = {v:.8f}')
                elif isinstance(v, list) and v and isinstance(v[0], float):
                    snippet = ', '.join(f'{x:.4f}' for x in v[:8])
                    lines.append(f'  {k:24s} = [{snippet}{"..." if len(v)>8 else ""}]')
                elif isinstance(v, dict):
                    lines.append(f'  {k}:')
                    for kk, vv in list(v.items())[:16]:
                        if isinstance(vv, float):
                            lines.append(f'    {kk:20s} = {vv:.6f}')
                        else:
                            lines.append(f'    {kk:20s} = {vv}')
                else:
                    lines.append(f'  {k:24s} = {v}')

            # Per-dimension breakdown if present
            per_dim = result.get('per_dimension', [])
            if per_dim:
                lines.append('  per_dimension:')
                for d in per_dim:
                    dj  = d.get('dJ', 0.0)
                    bar = '█' * int(d['J'] * 40) if d['J'] < 1.0 else '████████████████████████████████████████'
                    lines.append(f"    {d['dim']:14s}  J={d['J']:.4f}  dJ={dj:.4f}  {bar}")

            # Sedenion components
            sed = result.get('sedenion') or result.get('components')
            if isinstance(sed, list) and len(sed) == 16:
                lines.append('  sedenion components:')
                for k in range(16):
                    d   = DIM_BY_INDEX[k]
                    bar = '▪' * int(abs(sed[k]) * 40)
                    lines.append(f'    e{k:2d} {d.name:14s}  {sed[k]:+.6f}  {bar}')
            elif isinstance(sed, dict):
                lines.append('  components:')
                for dim_name, val in sed.items():
                    bar = '▪' * int(abs(val) * 40)
                    lines.append(f'    {dim_name:14s}  {val:+.6f}  {bar}')

            return '\n'.join(lines)
        return f'  {name}: {result}'

    def _complex_data(self, name, params, result) -> Dict:
        if name in ('prompt_encode', 'noether_scan'):
            s = encode_prompt(str(params.get('text', '')))
            n = 16
            import math as _m
            cartesian = [
                (s[k] * _m.cos(2 * _m.pi * k / n),
                 s[k] * _m.sin(2 * _m.pi * k / n))
                for k in range(n)
            ]
            return {
                'type':       'polar_trajectory',
                'trajectory': [(k, s[k]) for k in range(n)],
                'cartesian':  cartesian,
            }
        return {'text': self._fmt(name, result)}

    def _3d_data(self, name, params, result) -> Dict:
        if name == 'cd_projection':
            s = encode_prompt(str(params.get('text', '')))
            pts = []
            for level in range(5):
                proj = cd_projection(s, level)
                pts.append((float(level), proj['proj_norm'], proj['fraction']))
            return {
                'type':   '3d_flow',
                'points': pts,
                'axes':   ('cd_stratum', 'proj_norm', 'fraction'),
            }
        elif name == 'stress_energy':
            s = encode_prompt(str(params.get('text', '')))
            J = noether_charges(s)
            pts = [(float(k), J[k], math.sqrt(J[k])) for k in range(16)]
            return {
                'type':   '3d_flow',
                'points': pts,
                'axes':   ('dimension_k', 'J_k', 'psi_k'),
            }
        return {'text': self._fmt(name, result)}

    def shell_commands(self) -> Dict:
        return {
            'sedenion': lambda text='': full_analysis(text),
            'sed_encode': encode_prompt,
            'sed_fermat': fermat_lattice_scan,
            'sed_monad':  lambda text='': monad_interface(encode_prompt(text)),
        }
