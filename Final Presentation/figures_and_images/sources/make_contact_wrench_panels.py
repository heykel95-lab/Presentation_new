#!/usr/bin/env python3
"""Render the recorded contact force and moment on the native slide canvas.

The cache contains the exact plotted samples from the thesis generator's
three representative r01 trials (CoC positions -40, 0 and +40 mm).
The limits and ticks reproduce the existing presentation panels.
"""
import argparse
import csv
import gzip
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from results_grid import apply_results_grid


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=here/'contact_wrench_samples.csv.gz')
    parser.add_argument('--out-dir', type=Path, default=here)
    args = parser.parse_args()
    with gzip.open(args.data, 'rt', newline='') as handle:
        rows = list(csv.DictReader(handle))
    panels = [
        ('contact_force_plot', 'Fn_est_N', (-117.11536959104086, 27.850011993234943),
         [-100, -75, -50, -25, 0, 25]),
        ('contact_moment_plot', 'Mt1_est_Nm', (-6.1451928733668595, 6.6704540671994375),
         [-5, -2.5, 0, 2.5, 5]),
    ]
    for name, column, limits, ticks in panels:
        fig = plt.figure(figsize=(224/72, 231.826087/72))
        ax = fig.add_axes([0, 0, 1, 1])
        for condition, colour in zip(['m040', 'p000', 'p040'], ['#000000', '#c00000', '#0057b8']):
            selected = [row for row in rows if row['condition'] == condition]
            ax.plot([float(row['t_contact_s']) for row in selected],
                    [float(row[column]) for row in selected], color=colour, linewidth=.85)
        ax.set_xlim(-.25005, 5.251049999999999)
        ax.set_ylim(*limits)
        ax.set_xticks([0, 1, 2, 3, 4, 5])
        ax.set_yticks(ticks)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        apply_results_grid(ax, scale=1)
        if column == 'Mt1_est_Nm':
            ax.axhline(0, color='#888888', linewidth=.8, zorder=0)
        for spine in ax.spines.values():
            spine.set_linewidth(.6)
            spine.set_color('#1a1a1a')
        fig.savefig(args.out_dir/(name+'.pdf'))
        plt.close(fig)
        print(args.out_dir/(name+'.pdf'))


if __name__ == '__main__':
    main()
