"""Six-condition presentation analysis. No interpolation or smoothing.

Run with --refresh to archive the 12 original and six combined measured trials.
The combined condition extends the presentation only. Original assets remain.
"""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
NEW=ROOT/'experiments/h_mode_combined'
NEW15=ROOT/'experiments/h_mode_combined_1p5'
OLD=Path('/home/hm-panda/Desktop/Thesis_Final_Control/experiments/results')
CONDITIONS=[
 ('MAIN_NS7_baseline_20N_200mm','No null-space torque','#000000','o'),
 ('MAIN_NS7_damping_2p0_20N_200mm',r'Damping, $d_{\rm null}=2\,\mathrm{N\,m\,s/rad}$','#c00000','s'),
 ('MAIN_NS8_ksigma_1p5_20N_200mm',r'Conditioning, $k_\sigma=1.5\,\mathrm{N\,m}$','#0057b8','^'),
 ('MAIN_NS8_ksigma_2p0_20N_200mm',r'Conditioning, $k_\sigma=2\,\mathrm{N\,m}$','#c99700','D'),
 ('MAIN_NS9_combined_ksigma_2p0_dnull_2p0_20N_200mm',r'Combined, $k_\sigma=2$, $d_{\rm null}=2$ (SI)','#00865a','v'),
 ('MAIN_NS10_combined_ksigma_1p5_dnull_2p0_20N_200mm',r'Combined, $k_\sigma=1.5$, $d_{\rm null}=2$ (SI)','#8a3fb0','P')]
REPS=['r01','r02','r03']
COLS=['time','nullspace_speed','sigma_current']+[f'nullspace_dq_{j}' for j in range(1,8)]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def params(path):
 result={}
 for p in sorted(path.glob('*.txt')):
  for line in p.read_text().splitlines():
   s=line.split('#')[0].strip()
   if '=' in s:
    k,v=s.split('=',1);result[k.strip()]=v.strip()
 return result

def refresh():
 frames=[];joints=[];audit=[]
 known=json.loads((HERE/'nullspace_trial_provenance.json').read_text())['sources']
 hashes={(x['condition'],x['repetition']):x['sha256'] for x in known}
 ref=params(OLD/CONDITIONS[3][0]/'r01/params_effective')
 relevant=['q_init_case']+[f'q_init_table_{j}' for j in range(1,8)]+[k for k in ref if k.startswith(('hold_','disturbance_'))]+['nullspace_alpha','nullspace_sigma_deadband','nullspace_svd_relative_tolerance','log_every_n_cycles','experiment_duration','sigma_debug_log_period']
 for ci,(cid,_,_,_) in enumerate(CONDITIONS):
  for rep in REPS:
   folder=(NEW if ci==4 else NEW15)/'results'/rep if ci>=4 else OLD/cid/rep
   p=folder/'surface_grinding_controller_log.csv';jp=folder/'surface_grinding_controller_sigma_debug.csv'
   if ci<4:
    raw=p.read_bytes()
    assert hashes[(cid,rep)] in [sha(p),hashlib.sha256(raw.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')).hexdigest()], (cid,rep,'source content mismatch')
   par=params(folder/'params_effective')
   assert all(par[k]==ref[k] for k in relevant), (cid,rep,'parameter mismatch')
   assert par['nullspace_mode']==str([0,1,2,2,3,3][ci])
   assert float(par['nullspace_k_sigma'])==[2,2,1.5,2,2,1.5][ci]
   assert float(par['nullspace_damping'])==2
   d=pd.read_csv(p,float_precision='round_trip')
   assert d.time.iloc[-1]>=17.9
   assert (d.nullspace_mode==[0,1,2,2,3,3][ci]).all()
   w=d[d.time.between(5,9)].copy()
   assert w.time.iloc[0]==5 and w.time.iloc[-1]==9 and len(w)>3500
   assert (w.disturbance_torque_scale>=.999).all()
   assert np.isclose(w.disturbance_scale.max(),1)
   assert np.max(np.linalg.norm(w[[f'tau_disturbance_{j}' for j in range(1,8)]],axis=1))<=3.000001
   if ci>=4:
    prov=json.loads((folder/"provenance.json").read_text())
    assert prov["acquisition_checks_passed"] and prov["files"][p.name]==sha(p) and prov["files"][jp.name]==sha(jp)
    assert (w.sigma_k_sigma==[2,2,1.5,2,2,1.5][ci]).all() and (w.nullspace_damping==2).all()
    # Check logged total null-space norm against the sum of both commanded terms.
    tau=w[[f'tau_sigma_{j}' for j in range(1,8)]].to_numpy()-2*w[[f'nullspace_dq_{j}' for j in range(1,8)]].to_numpy()
    assert np.max(abs(np.linalg.norm(tau,axis=1)-w.tau_nullspace_norm))<1e-7
   small=w[COLS].copy();small.insert(0,'repetition',rep);small.insert(0,'condition',cid);frames.append(small)
   j=pd.read_csv(jp,float_precision='round_trip');j=j[j.phase_time_s.between(5,9)&(j.event=='sample')].copy()
   assert len(j)==81 and not j.phase_time_s.duplicated().any() and j.phase_time_s.iloc[0]==5 and j.phase_time_s.iloc[-1]==9
   q=j[['phase_time_s']+[f'q{k}_deg' for k in range(1,8)]].copy();q.insert(0,'repetition',rep);q.insert(0,'condition',cid);joints.append(q)
   audit.append({'condition':cid,'repetition':rep,'main_sha256':sha(p),'debug_sha256':sha(jp),'main_source':str(p),'debug_source':str(jp),'window_rows':len(w),'q_samples':len(j),'matched_protocol_keys':relevant,'total_run_s':float(d.time.iloc[-1]),'sigma_at_onset':float(w.sigma_current.iloc[0]),'position_error_max_mm':float(1000*np.linalg.norm(w[['e_p_x','e_p_y','e_p_z']],axis=1).max()),'both_terms_sum_verified':ci>=4})
 pd.concat(frames).to_csv(HERE/'combined_nullspace_samples.csv.gz',index=False,float_format='%.17g',compression={'method':'gzip','mtime':0})
 pd.concat(joints).to_csv(HERE/'combined_joint_samples.csv.gz',index=False,float_format='%.17g',compression={'method':'gzip','mtime':0})
 (HERE/'combined_nullspace_provenance.json').write_text(json.dumps(audit,indent=2)+'\n')

def integrate(y,t):
 dt=np.diff(t)
 if y.ndim==2:dt=dt[:,None]
 return np.concatenate([np.zeros_like(y[:1]),np.cumsum((y[:-1]+y[1:])*.5*dt,axis=0)])

def calculate():
 d=pd.read_csv(HERE/'combined_nullspace_samples.csv.gz',float_precision='round_trip')
 j=pd.read_csv(HERE/'combined_joint_samples.csv.gz',float_precision='round_trip')
 groups=[]
 for cid,_,_,_ in CONDITIONS:
  runs=[]
  for rep in REPS:
   w=d[(d.condition==cid)&(d.repetition==rep)];t=w.time.to_numpy();dq=w[COLS[3:]].to_numpy();speed=w.nullspace_speed.to_numpy()
   assert np.all(np.diff(t)>0) and np.max(abs(np.linalg.norm(dq,axis=1)-speed))<2e-9
   q=j[(j.condition==cid)&(j.repetition==rep)]
   runs.append({'time':t,'cumulative':np.degrees(integrate(speed,t)),'sigma':w.sigma_current.to_numpy(),'qt':q.phase_time_s.to_numpy(),'q':q.q1_deg.to_numpy()-q.q1_deg.iloc[0]})
  groups.append(runs)
 report=[]
 for ci,runs in enumerate(groups):
  record={'condition':CONDITIONS[ci][0]}
  for k in ['cumulative','q','sigma']:
   vals=np.array([r[k][-1] for r in runs]);record[k+'_mean']=float(vals.mean());record[k+'_sd']=float(vals.std(ddof=1));record[k+'_trials']=vals.tolist()
  record['sigma_change_mean']=float(np.mean([r['sigma'][-1]-r['sigma'][0] for r in runs]))
  report.append(record)
 assert np.allclose([r['cumulative_mean'] for r in report[:4]],np.degrees([.132614246,.0992980553,.0050197591,.0294435416]),atol=3e-8,rtol=0)
 info={'conditions':report,'recorded_interval_s':[5,9],'display_interval_s':[0,4],'interpolation':False,'smoothing':False,'uncertainty':'One sample SD across three trials, ddof=1','original_endpoints_verified':True,'combined_cumulative_reduction_vs_sigma2_percent':100*(1-report[4]['cumulative_mean']/report[3]['cumulative_mean']),'combined_cumulative_reduction_vs_sigma1p5_percent':100*(1-report[5]['cumulative_mean']/report[2]['cumulative_mean']),'acquisition_note':'Combined conditions acquired in a later session with the exact archived source revision and matching saved settings. Session effects are not independently controlled.'}
 assert np.isclose(report[4]['cumulative_mean'],.8312711146194921,atol=1e-12,rtol=0)
 (HERE/'combined_nullspace_analysis.json').write_text(json.dumps(info,indent=2)+'\n')
 pd.DataFrame(report).drop(columns=[c for c in pd.DataFrame(report) if c.endswith('_trials')]).to_csv(HERE/'combined_nullspace_summary.csv',index=False)
 return groups,info

def mean(runs,key):
 tk='qt' if key=='q' else 'time';t=runs[0][tk]
 for r in runs[1:]:t=np.intersect1d(t,r[tk])
 assert len(t)>60 and t[0]==5 and t[-1]==9
 vals=np.array([r[key][np.searchsorted(r[tk],t)] for r in runs])
 return t-5,vals.mean(0),vals.std(0,ddof=1)

def style(ax):
 ax.set_xlabel(r'Time, $t$ [s]');ax.grid(axis='y',color='.85',lw=.5)
 for s in ['top','right']:ax.spines[s].set_visible(False)
 ax.tick_params(length=3,width=.6)
 ax.set_xlim(0,4);ax.set_xticks([0,1,2,3,4])

def legend(fig,trial=False):
 order=[0,2,5,1,3,4]
 handles=[Line2D([0],[0],color=CONDITIONS[i][2],lw=1.3,marker=CONDITIONS[i][3],markersize=3,markerfacecolor='white') for i in order]
 fig.legend(handles,[CONDITIONS[i][1] for i in order],loc='lower center',bbox_to_anchor=(.51,.015),ncol=2,fontsize=11,frameon=False,columnspacing=1.5,handlelength=1.5)

def save(fig,name):
 for ext in ['pdf','png','svg']:fig.savefig(HERE.parent/(name+'_combined.'+ext),dpi=300,facecolor='white')
 plt.close(fig)

def plots(groups,info):
 plt.rcParams.update({'font.family':'serif','mathtext.fontset':'cm','font.size':11,'axes.labelsize':12,'xtick.labelsize':10,'ytick.labelsize':10,'axes.linewidth':.7,'pdf.fonttype':42,'svg.fonttype':'path','axes.unicode_minus':True})
 for key,name,label,panel in [('cumulative','nullspace_damping',r'Cumulative Joint Motion, $E_N$ [$^\circ$]','(a)'),('sigma','nullspace_conditioning',r'Minimum Singular Value, $\sigma_{\min}$','(b)')]:
  fig=plt.figure(figsize=(9,4.2));ax=fig.add_axes([.12,.31,.85,.63]);style(ax)
  for ci,runs in enumerate(groups):
   t,m,sd=mean(runs,key);_,_,c,mark=CONDITIONS[ci];ix=np.unique(np.linspace(0,len(t)-1,min(900,len(t))).astype(int))
   ax.plot(t[ix],m[ix],color=c,lw=1.2,marker=mark,markevery=115,ms=3,mfc='white');ax.fill_between(t[ix],(m-sd)[ix],(m+sd)[ix],color=c,alpha=.12,lw=0)
  ax.set_ylabel(label);ax.set_title(panel,loc='left',fontsize=12)
  if key=='sigma':ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v*10:.2f}'));ax.text(0,1.02,r'$\times10^{-1}$',transform=ax.transAxes);ax.set_yticks([.214,.215,.216,.217]);ax.set_title('',loc='left');ax.set_title('(b)',loc='right',fontsize=12)
  else:ax.set_ylim(bottom=0)
  legend(fig);save(fig,name)
 for key,name,view in [('q','joint_motion_time','all'),('q','joint_motion_single','single'),('q','joint_motion_mean','mean')]:
  fig=plt.figure(figsize=(9,4.5));axes=[fig.add_axes([.09,.34,.43,.56]),fig.add_axes([.68,.34,.29,.56])]
  for ci,runs in enumerate(groups):
   _,_,c,mark=CONDITIONS[ci]
   for ai,ax in enumerate(axes):
    if ai==1 and ci<2:continue
    if view=='mean':
     t,m,sd=mean(runs,key);sel=t<=1 if ai==1 else np.ones(len(t),dtype=bool)
     ix=np.flatnonzero(sel);ix=ix[np.unique(np.linspace(0,len(ix)-1,min(900,len(ix))).astype(int))]
     ax.plot(t[ix],m[ix],color=c,lw=1,marker=mark,markevery=1,ms=2.5,mfc='white');ax.fill_between(t[ix],(m-sd)[ix],(m+sd)[ix],color=c,alpha=.12,lw=0)
    else:
     for ri,r in enumerate(runs[:1] if view=='single' else runs):
      t=r['qt']-5;sel=t<=1 if ai else np.ones(len(t),dtype=bool)
      ax.plot(t[sel],r['q'][sel],color=c,linestyle=['-','--',':'][ri],lw=.85,marker=mark,ms=2.1,mfc='white')
  for ax in axes:style(ax);ax.axhline(0,color='.5',lw=.6)
  axes[0].set_ylabel(r'Joint 1 Motion, $\Delta q_1$ [$^\circ$]')
  axes[1].set_ylabel(r'$\Delta q_1$ [$^\circ$]')
  axes[0].set_title('(a) All settings',fontsize=11);axes[1].set_title('(b) Conditioning and combined\nFirst second',fontsize=10)
  axes[0].set_ylim(-.2,6.6)
  axes[1].set_xlim(0,1);axes[1].set_xticks([0,.25,.5,.75,1]);axes[1].set_ylim(-.03,.075)
  axes[1].yaxis.set_major_formatter(FuncFormatter(lambda v,p:'0' if abs(v)<1e-10 else f'{v:.2f}'))
  legend(fig);save(fig,name)
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--refresh',action='store_true');args=parser.parse_args()
 if args.refresh:refresh()
 groups,report=calculate();plots(groups,report);print(json.dumps(report,indent=2))
