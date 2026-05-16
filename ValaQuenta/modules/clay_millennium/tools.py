"""
ainulindale_engine.modules.clay_millennium.tools
=================================================
ClayMillenniumModule — registry contract.

Version: 0.120
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    riemann_hypothesis,
    yang_mills_mass_gap,
    navier_stokes_existence,
    p_vs_np,
    hodge_conjecture,
    birch_swinnerton_dyer,
    poincare_conjecture,
    all_clay_problems,
    clay_summary,
)


class ClayMillenniumModule(EquationModule):

    @property
    def name(self): return 'clay_millennium'

    @property
    def display_name(self): return 'Clay Millennium Problems — H_hat_RB derivations'

    @property
    def version(self): return '0.120'

    @property
    def description(self):
        return (
            'All 7 Clay Millennium Problems derived from H_hat_RB. '
            'Each problem shown as a facet projection, with: '
            'what it IS (Red), what it CANNOT BE (Blue), what it MEANS (Noether). '
            'Poincaré (SOLVED) validates the framework. '
            '6 open problems: RH, Yang-Mills, NS, P/NP, Hodge, BSD.'
        )

    @property
    def confidence_floor(self): return 'THEORETICAL'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='clay_summary',
                display='All 7 Clay Millennium Problems — H_hat_RB summary',
                latex=r'\hat{H}_{RB}\to\{\text{RH, YM, NS, P/NP, Hodge, BSD, Poincar\'{e}}\}',
                radian_form='All Clay problems project from H_hat_RB at their respective σ.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=clay_summary,
                display_options=[],
            ),
            Equation(
                name='riemann_hypothesis',
                display='RH — eigenvalues of H_hat_RB at σ=½ on critical line  [OPEN]',
                latex=r'\hat{H}_{RB}|\psi\rangle=\gamma_n|\psi\rangle,\;\hat{H}^\dagger=\hat{H}\Rightarrow\mathrm{Re}(s)=\tfrac{1}{2}',
                radian_form='Self-adjoint H_hat_RB → real eigenvalues → all zeros on σ=½.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=riemann_hypothesis,
                display_options=['complex_plane'],
            ),
            Equation(
                name='yang_mills_mass_gap',
                display='Yang-Mills mass gap — min eigenvalue at σ=1 > 0  [OPEN]',
                latex=r'\Delta=\min\mathrm{spec}(\hat{H}_{RB}|_{\sigma=1})>0',
                radian_form='G_p(1) = p^{-1} > 0 for all primes → ground state > 0 → mass gap.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=yang_mills_mass_gap,
                display_options=[],
            ),
            Equation(
                name='navier_stokes',
                display='Navier-Stokes — real projection of H_hat_RB lacks i  [OPEN]',
                latex=r'\text{NS}=\mathrm{Re}(\hat{H}_{RB}|_{\sigma=1}),\quad i\notin\text{NS}',
                radian_form='NS = Yang-Mills minus i. Smooth in ℂ; may blow up in ℝ.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=navier_stokes_existence,
                display_options=[],
            ),
            Equation(
                name='p_vs_np',
                display='P vs NP — Red (analytic) vs Blue (elliptic) complexity  [OPEN]',
                latex=r'\hat{R}^\dagger=\hat{B}\;\not\Rightarrow\;\text{P}=\text{NP}',
                radian_form='Adjoint ≠ computationally equivalent. 1=1 is cheaper than 1!=1.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=p_vs_np,
                display_options=[],
            ),
            Equation(
                name='hodge_conjecture',
                display='Hodge — algebraic cycles from inductive prime sum  [OPEN]',
                latex=r'\mathrm{Hdg}^k(X)\subset[\text{algebraic cycles}],\quad G_p(1)=1/p\in\mathbb{Q}',
                radian_form='Inductive Σ_p generates algebraic cycles. Rational coupling → rational Hodge.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=hodge_conjecture,
                display_options=[],
            ),
            Equation(
                name='birch_swinnerton_dyer',
                display='BSD — rank(E) = ord L(E,1) = Blue eigenspace multiplicity  [OPEN]',
                latex=r'\mathrm{rank}(E)=\mathrm{ord}_{s=1}L(E,s)=\dim(\hat{B}\text{-eigenspace})',
                radian_form='L(E,s) = Blue Euler product. Geometric rank = spectral order.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=birch_swinnerton_dyer,
                display_options=[],
            ),
            Equation(
                name='poincare_conjecture',
                display='Poincaré — trivial H_hat_RB → S³  [SOLVED — validation]',
                latex=r'\partial g_{\mu\nu}/\partial t=-2R_{\mu\nu}\;\to\;M\cong S^3',
                radian_form='Ricci flow = H_hat_RB coupling flow to trivial facet. Validates framework.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=poincare_conjecture,
                display_options=[],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in clay_millennium module")
        filtered = {k: params[k] for k in eq.params if k in params}
        result = eq.compute(**filtered)
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)['result']
        return {'text': self._fmt(equation_name, result)}

    def _fmt(self, name: str, result: Any) -> str:
        if isinstance(result, dict):
            lines = [f'  [{name}]']
            for k, v in result.items():
                if isinstance(v, list) and v and isinstance(v[0], str):
                    lines.append(f'  {k}:')
                    for item in v:
                        lines.append(f'    • {item}')
                elif isinstance(v, float):
                    lines.append(f'  {k:30s} = {v:.10f}')
                elif not isinstance(v, (list, dict)):
                    lines.append(f'  {k:30s} = {v}')
            return '\n'.join(lines)
        return f'  {name}: {result}'
