"""Regenerate the presentation panels with compact numerical labels.

Uses the unchanged thesis analysis and recorded 5--9 s interval. The data,
means, standard deviations and units are unchanged. Only labels differ.
"""
from pathlib import Path
import argparse
import sys
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--analysis-dir', type=Path, required=True,
                    help='MyOwn/code/python/figures')
parser.add_argument('--results', type=Path, required=True,
                    help='Thesis_Final_Control/experiments/results')
parser.add_argument('--out-dir', type=Path, default=HERE)
args = parser.parse_args()
sys.path.insert(0, str(args.analysis_dir.resolve()))
import make_nullspace_figure as analysis

analysis.RESULTS = str(args.results.resolve())
analysis.make_figures.FIGURES = str(args.out_dir.resolve())
original_sigma_panel = analysis.sigma_panel

def sigma_panel(ax, groups):
    result = original_sigma_panel(ax, groups)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, position: f'{value*10:.2f}'))
    ax.text(0, 1.025, r'$\times10^{-1}$', transform=ax.transAxes,
            ha='left', va='bottom', fontsize=8)
    return result

def value_label(value):
    if 0 < abs(value) < 0.1:
        return f'${value*100:.1f}' + r'\times10^{-2}$'
    return f'${value:.2f}$'

analysis.sigma_panel = sigma_panel
analysis._net_value_label = value_label
groups = analysis.load_conditions()
if len(groups) != len(analysis.CONDITIONS):
    raise ValueError('All four conditions are required')
analysis.net_displacements(groups)
analysis.make_figure(groups, str(args.out_dir.resolve()))
