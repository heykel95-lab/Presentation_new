"""Four-condition main-presentation views from the verified six-setting study.

Run beside make_combined_nullspace.py. No new processing of raw signals is
introduced. Selection changes only: off, damping, sigma=2, sigma=2 plus damping.
The complete six-condition plots remain available in the hidden backups.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
import make_combined_nullspace as study

HERE=Path(__file__).resolve().parent
SELECT=[0,1,3,4]
NAMES=['No null-space torque',r'Damping, $d_{\rm null}=2\,\mathrm{N\,m\,s/rad}$',r'Conditioning, $k_\sigma=2\,\mathrm{N\,m}$',r'Combined, $k_\sigma=2$, $d_{\rm null}=2$ (SI)']

def legend(fig):
 order=[0,2,1,3]
 handles=[Line2D([0],[0],color=study.CONDITIONS[SELECT[i]][2],lw=1.3,marker=study.CONDITIONS[SELECT[i]][3],markersize=3.5,markerfacecolor='white') for i in order]
 fig.legend(handles,[NAMES[i] for i in order],loc='lower center',bbox_to_anchor=(.51,.035),ncol=2,fontsize=11,frameon=False,columnspacing=1.6,handlelength=1.8)
 fig.text(.51,.015,'Three-trial mean and one sample standard deviation.',ha='center',fontsize=9)

def save(fig,name):
 for ext in ['pdf','png','svg']:fig.savefig(HERE.parent/(name+'.'+ext),dpi=300,facecolor='white')
 plt.close(fig)

def main():
 before=json.loads((HERE/'combined_nullspace_analysis.json').read_text())
 groups,info=study.calculate()
 assert before==info
 plt.rcParams.update({'font.family':'serif','mathtext.fontset':'cm','font.size':11,'axes.labelsize':12,'xtick.labelsize':10,'ytick.labelsize':10,'axes.linewidth':.7,'pdf.fonttype':42,'svg.fonttype':'path','axes.unicode_minus':True})
 for key,name,label,panel in [('cumulative','nullspace_cumulative_main',r'Cumulative Joint Motion, $E_N$ [$^\circ$]','(a)'),('sigma','nullspace_conditioning_main',r'Minimum Singular Value, $\sigma_{\min}$','(b)')]:
  fig=plt.figure(figsize=(9,4.2));ax=fig.add_axes([.12,.28,.85,.65]);study.style(ax)
  for ci in SELECT:
   t,m,sd=study.mean(groups[ci],key);_,_,colour,mark=study.CONDITIONS[ci]
   idx=np.unique(np.linspace(0,len(t)-1,min(900,len(t))).astype(int))
   ax.plot(t[idx],m[idx],color=colour,lw=1.25,marker=mark,markevery=115,ms=3,mfc='white')
   ax.fill_between(t[idx],(m-sd)[idx],(m+sd)[idx],color=colour,alpha=.12,lw=0)
  ax.set_ylabel(label);ax.set_title(panel,loc='right' if key=='sigma' else 'left',fontsize=12)
  if key=='sigma':
   ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v*10:.2f}'));ax.text(0,1.02,r'$\times10^{-1}$',transform=ax.transAxes);ax.set_yticks([.214,.215,.216,.217])
  else:ax.set_ylim(bottom=0)
  legend(fig);save(fig,name)
 fig=plt.figure(figsize=(9,4.5));axes=[fig.add_axes([.09,.30,.43,.60]),fig.add_axes([.68,.30,.29,.60])]
 for ci in SELECT:
  t,m,sd=study.mean(groups[ci],'q');_,_,colour,mark=study.CONDITIONS[ci]
  for ai,ax in enumerate(axes):
   if ai and ci<3:continue
   sel=t<=1 if ai else np.ones(len(t),bool)
   ax.plot(t[sel],m[sel],color=colour,lw=1,marker=mark,ms=2.5,mfc='white')
   ax.fill_between(t[sel],(m-sd)[sel],(m+sd)[sel],color=colour,alpha=.12,lw=0)
   if ai:assert (m-sd)[sel].min()>-.03 and (m+sd)[sel].max()<.075
 for ax in axes:study.style(ax);ax.axhline(0,color='.5',lw=.6)
 axes[0].set_ylabel(r'Joint 1 Motion, $\Delta q_1$ [$^\circ$]');axes[0].set_ylim(-.2,6.6)
 axes[0].set_title('(a) Four settings',fontsize=11)
 axes[1].set_ylabel(r'$\Delta q_1$ [$^\circ$]');axes[1].set_xlim(0,1);axes[1].set_xticks([0,.25,.5,.75,1]);axes[1].set_ylim(-.03,.075)
 axes[1].yaxis.set_major_formatter(FuncFormatter(lambda v,p:'0' if abs(v)<1e-10 else f'{v:.2f}'))
 axes[1].set_title('(b) Conditioning and combined\nFirst second',fontsize=10)
 legend(fig);save(fig,'joint_motion_mean_main')
 summary={'main_conditions':[study.CONDITIONS[i][0] for i in SELECT],'unchanged_processing':True,'recorded_interval_s':[5,9],'three_trial_means_and_sample_sd':True,'main_cumulative_means_deg':[info['conditions'][i]['cumulative_mean'] for i in SELECT],'parameter_comparison':[{'k_sigma_Nm':k,'conditioning_mean_deg':info['conditions'][a]['cumulative_mean'],'combined_mean_deg':info['conditions'][b]['cumulative_mean'],'conditioning_sample_sd_deg':info['conditions'][a]['cumulative_sd'],'combined_sample_sd_deg':info['conditions'][b]['cumulative_sd']} for k,a,b in [(1.5,2,5),(2,3,4)]]}
 (HERE/'nullspace_narrative_analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
 print('Generated three four-condition main plots. All six-setting values and curves preserved.')

if __name__=='__main__':main()
