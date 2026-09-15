#!/usr/bin/env python3
"""Regenerate the presentation angular-error panel from the supplied data.

The three CSVs contain actual recorded contact time and calibrated normal-error
samples. They were extracted from the r01 campaign logs without interpolation.
The neighbouring force and moment panel PDFs retain their original data.
"""
import argparse
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    here=Path(__file__).resolve().parent
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data-dir',type=Path,default=here)
    p.add_argument('--out',type=Path,default=here/'contact_error_plot.pdf')
    args=p.parse_args()
    plt.rcParams.update({'font.family':'serif','font.serif':['Latin Modern Roman','CMU Serif','cmr10'],'mathtext.fontset':'cm','axes.unicode_minus':False,'pdf.fonttype':42})
    fig=plt.figure(figsize=(224/72,172/72))
    ax=fig.add_axes([0,0,1,1])
    for suffix,colour in zip(['m040','p000','p040'],['#000000','#c00000','#0057b8']):
        with (args.data_dir/f'contact_error_{suffix}_r01.csv').open(newline='') as f:
            rows=list(csv.DictReader(f))
        t=np.array([float(r['t_contact_s']) for r in rows])
        error=np.array([float(r['theta_err_t1_deg']) for r in rows])
        step=max(1,len(t)//900)
        ax.plot(t[::step],error[::step],color=colour,linewidth=.85)
    ax.set_xlim(-.25,5.25)
    ax.set_ylim(0,11)
    ax.set_yticks([0,2,4,6,8,10])
    ax.set_xticks([0,1,2,3,4,5])
    ax.tick_params(left=False,bottom=False,labelleft=False,labelbottom=False)
    ax.grid(axis='y',alpha=.3,linewidth=.6)
    for spine in ax.spines.values():
        spine.set_linewidth(.6)
        spine.set_color('#1a1a1a')
    fig.savefig(args.out)
    plt.close(fig)
    print(args.out)

if __name__=='__main__':
    main()
