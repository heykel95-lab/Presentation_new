"""Four-condition main-presentation views from the verified six-setting study.

Run beside make_combined_nullspace.py. No new processing of raw signals is
introduced. Selection changes only: off, damping, sigma=2, sigma=2 plus damping.
The complete six-condition plots remain available in the hidden backups.
"""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
import make_combined_nullspace as study
from results_grid import apply_results_grid

HERE=Path(__file__).resolve().parent
PRINT_WIDTH=160/25.4
DRAW_SCALE=PRINT_WIDTH/9
SELECT=[0,1,3,4]
NAMES=['No null-space torque',r'Damping, $d_{\rm null}=2\,\mathrm{N\,m\,s/rad}$',r'Conditioning, $k_\sigma=2\,\mathrm{N\,m}$',r'Combined, $k_\sigma=2$, $d_{\rm null}=2$']

def legend(fig):
 order=[0,2,1,3]
 handles=[Line2D([0],[0],color=study.CONDITIONS[SELECT[i]][2],lw=1.3*DRAW_SCALE,marker=study.CONDITIONS[SELECT[i]][3],markersize=3.5*DRAW_SCALE,markeredgewidth=DRAW_SCALE,markerfacecolor='white') for i in order]
 fig.legend(handles,[NAMES[i] for i in order],loc='lower center',bbox_to_anchor=(.5,.035),ncol=2,fontsize=8,frameon=False,columnspacing=1.6,handlelength=1.8)
 fig.text(.5,.015,'Three-trial mean and one sample standard deviation.',ha='center',fontsize=7)

def style(ax):
 """Match Figures 5.4 and 5.6: thin boxed axes with inward ticks."""
 study.style(ax)
 for spine in ax.spines.values():
  spine.set_visible(True)
  spine.set_color('black')
  spine.set_linewidth(.57*DRAW_SCALE)
 ax.tick_params(direction='in',length=4*DRAW_SCALE,width=.57*DRAW_SCALE,top=True,right=True)
 apply_results_grid(ax)

def font_style():
 # Render at the final 160 mm text width so TeX selects the same optical
 # font sizes as the reference figures: labels/ticks 10 pt, legends 8 pt.
 # Computer Modern Roman selects LaTeX's serif family; lmodern replaces both
 # its text and maths faces, matching the pgfplots figures without font mixing.
 plt.rcParams.update({'text.usetex':True,'text.latex.preamble':r'\usepackage[T1]{fontenc}\usepackage{lmodern}','font.family':'serif','font.serif':['Computer Modern Roman'],'font.size':10,'axes.labelsize':10,'xtick.labelsize':10,'ytick.labelsize':10,'axes.linewidth':.57*DRAW_SCALE,'pdf.fonttype':42,'svg.fonttype':'path','axes.unicode_minus':False})

def save(fig,name):
 for ext in ['pdf','png','svg']:fig.savefig(HERE.parent/(name+'.'+ext),dpi=450,facecolor='white')
 svg=HERE.parent/(name+'.svg')
 svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
 plt.close(fig)

def same_report(expected,actual):
 if isinstance(expected,dict):
  assert expected.keys()==actual.keys()
  for key in expected:same_report(expected[key],actual[key])
 elif isinstance(expected,list):
  assert len(expected)==len(actual)
  for a,b in zip(expected,actual):same_report(a,b)
 elif isinstance(expected,float):
  np.testing.assert_allclose(actual,expected,rtol=1e-13,atol=1e-14)
 else:assert expected==actual

def main(only=None):
 only=set(only or ["cumulative","conditioning","joint"])
 # Keep audited reports byte-for-byte unchanged when only rendering figures.
 reports={p:p.read_bytes() for p in [HERE/'combined_nullspace_analysis.json',HERE/'combined_nullspace_summary.csv']}
 before=json.loads(reports[HERE/'combined_nullspace_analysis.json'])
 try:groups,info=study.calculate()
 finally:
  for path,data in reports.items():path.write_bytes(data)
 same_report(before,info)
 font_style()
 for key,name,label,panel in [('cumulative','nullspace_cumulative_main',r'Cumulative Joint Motion, $E_N$ [$^\circ$]','(a)'),('sigma','nullspace_conditioning_main',r'Minimum Singular Value, $\sigma_{\min}$','(b)')]:
  if ("conditioning" if key=="sigma" else key) not in only:continue
  fig=plt.figure(figsize=(PRINT_WIDTH,4.2*DRAW_SCALE));ax=fig.add_axes([.12,.28,.85,.65]);style(ax)
  for ci in SELECT:
   t,m,sd=study.mean(groups[ci],key);_,_,colour,mark=study.CONDITIONS[ci]
   idx=np.unique(np.linspace(0,len(t)-1,min(900,len(t))).astype(int))
   ax.plot(t[idx],m[idx],color=colour,lw=1.25*DRAW_SCALE,marker=mark,markevery=115,ms=3*DRAW_SCALE,mew=DRAW_SCALE,mfc='white')
   ax.fill_between(t[idx],(m-sd)[idx],(m+sd)[idx],color=colour,alpha=.12,lw=0)
  ax.set_ylabel(label);ax.set_title(panel,loc='right' if key=='sigma' else 'left',fontsize=10,pad=3*DRAW_SCALE)
  if key=='sigma':
   ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v*10:.2f}'));ax.text(0,1.02,r'$\times10^{-1}$',transform=ax.transAxes);ax.set_yticks([.214,.215,.216,.217])
  else:ax.set_ylim(bottom=0)
  legend(fig);save(fig,name)
 if 'joint' in only:
  # Equal cells give both panels identical plotting areas and label margins.
  fig=plt.figure(figsize=(PRINT_WIDTH,4.5*DRAW_SCALE));axes=[fig.add_axes([left,.30,.35,.60]) for left in [.12,.62]]
  for ci in SELECT:
   t,m,sd=study.mean(groups[ci],'q');_,_,colour,mark=study.CONDITIONS[ci]
   for ai,ax in enumerate(axes):
    if ai and ci<3:continue
    sel=np.ones(len(t),bool)
    ax.plot(t[sel],m[sel],color=colour,lw=1.25*DRAW_SCALE,marker=mark,markevery=10,ms=3*DRAW_SCALE,mew=DRAW_SCALE,mfc='white')
    ax.fill_between(t[sel],(m-sd)[sel],(m+sd)[sel],color=colour,alpha=.12,lw=0)
    if ai:assert t[sel][0]==0 and t[sel][-1]==4
  for ax in axes:style(ax);ax.axhline(0,color='.5',lw=.6*DRAW_SCALE)
  axes[0].set_ylabel(r'Joint 1 Motion, $\Delta q_1$ [$^\circ$]');axes[0].set_ylim(-.2,6.6)
  axes[0].set_yticks([0,1,2,3,4,5,6])
  axes[0].set_title('(a) Four settings',fontsize=10,pad=6*DRAW_SCALE)
  axes[1].set_ylabel(r'Joint 1 Motion, $\Delta q_1$ [$^\circ$]');axes[1].set_xlim(0,4);axes[1].set_xticks([0,1,2,3,4])
  axes[1].set_yticks([-.02,0,.02,.04,.06,.08])
  axes[1].yaxis.set_major_formatter(FuncFormatter(lambda v,p:'0' if abs(v)<1e-10 else f'{v:.2f}'))
  axes[1].set_title('(b) Conditioning and combined',fontsize=10,pad=6*DRAW_SCALE)
  for ax in axes:ax.yaxis.set_label_coords(-.22,.5)
  legend(fig);save(fig,'joint_motion_mean_main')
 summary={'main_conditions':[study.CONDITIONS[i][0] for i in SELECT],'unchanged_processing':True,'recorded_interval_s':[5,9],'three_trial_means_and_sample_sd':True,'main_cumulative_means_deg':[info['conditions'][i]['cumulative_mean'] for i in SELECT],'parameter_comparison':[{'k_sigma_Nm':k,'conditioning_mean_deg':info['conditions'][a]['cumulative_mean'],'combined_mean_deg':info['conditions'][b]['cumulative_mean'],'conditioning_sample_sd_deg':info['conditions'][a]['cumulative_sd'],'combined_sample_sd_deg':info['conditions'][b]['cumulative_sd']} for k,a,b in [(1.5,2,5),(2,3,4)]]}
 (HERE/'nullspace_narrative_analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
 print('Generated requested main plots: '+', '.join(sorted(only))+'. Recorded data and six-setting views preserved.')

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--only',nargs='+',choices=['cumulative','conditioning','joint'])
 main(parser.parse_args().only)
