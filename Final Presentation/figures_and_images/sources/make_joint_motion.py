"""Measured joint-1 histories from the archived null-space pose-hold trials.

Rebuild: python make_joint_motion.py --out-dir OUTPUT
Archive: add --raw-root PATH --reference-root PATH to verify and extract raw data.
No integration, interpolation, filtering, or averaging is applied to q1.
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

HERE = Path(__file__).resolve().parent
CONDITIONS = [
 ('MAIN_NS7_baseline_20N_200mm', 'No Null-Space Torque', '#000000'),
 ('MAIN_NS7_damping_2p0_20N_200mm', r'Damping, $d_{\mathrm{null}}=2\,\mathrm{N\,m\,s/rad}$', '#c00000'),
 ('MAIN_NS8_ksigma_1p5_20N_200mm', r'Conditioning, $k_\sigma=1.5\,\mathrm{N\,m}$', '#0057b8'),
 ('MAIN_NS8_ksigma_2p0_20N_200mm', r'Conditioning, $k_\sigma=2.0\,\mathrm{N\,m}$', '#c99700'),
]
REPS = ['r01', 'r02', 'r03']
COLS = ['phase_time_s', 'event', 'q1_deg', 'k_sigma_Nm', 'nullspace_damping_Nms_rad']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def archive(raw, reference):
 frames=[]; records=[]
 for ci,(cid,_,_) in enumerate(CONDITIONS):
  for rep in REPS:
   directory=raw/cid/rep
   debug=directory/'surface_grinding_controller_sigma_debug.csv'
   main=directory/'surface_grinding_controller_log.csv'
   known=reference/cid/rep/main.name
   assert sha(main)==sha(known), 'Archive does not match the established trial'
   d=pd.read_csv(debug, float_precision='round_trip')
   d=d.loc[d.phase_time_s.between(5,9)].copy()
   assert d.phase_time_s.iloc[0]==5 and d.phase_time_s.iloc[-1]==9
   assert np.all(np.diff(d.phase_time_s)>=0)
   # Event rows repeat measured q but omit some control diagnostics.
   # Verify joint-angle identity, then use the complete periodic sample rows.
   duplicates=d[d.duplicated('phase_time_s', keep=False)]
   for _,group in duplicates.groupby('phase_time_s'):
    numeric=group[[f'q{j}_deg' for j in range(1,8)]]
    assert (numeric.nunique(dropna=False)<=1).all()
   unique=d.loc[d.event=='sample'].copy()
   assert len(unique)==81 and np.allclose(np.diff(unique.phase_time_s),.05,atol=.002001,rtol=0)
   assert np.isfinite(unique.q1_deg).all()
   # These debug columns are configured coefficients, including inactive terms.
   # The main log's mode identifies which term was actually enabled.
   expected_k=[2,2,1.5,2][ci]; expected_d=2
   assert np.all(unique.k_sigma_Nm==expected_k)
   assert np.all(unique.nullspace_damping_Nms_rad==expected_d)
   log=pd.read_csv(main, usecols=['time','nullspace_mode']+[f'tau_disturbance_{j}' for j in range(1,8)],float_precision='round_trip')
   log=log.loc[log.time.between(5,9)]
   assert np.all(log.nullspace_mode==[0,1,2,2][ci])
   maxima=log[[f'tau_disturbance_{j}' for j in range(1,8)]].abs().max().tolist()
   assert np.argmax(maxima)==0
   selected=unique[COLS].copy()
   selected.insert(0,'repetition',rep); selected.insert(0,'condition',cid)
   frames.append(selected)
   records.append({'condition':cid,'repetition':rep,'diagnostic_file':str(debug),'diagnostic_sha256':sha(debug),'main_log_sha256':sha(main),'reference_main_log':str(known),'main_log_matches_reference':True,'window_rows':len(d),'unique_timestamps':len(unique),'duplicate_event_rows':len(d)-len(unique),'actual_sample_spacing_range_s':[float(np.diff(unique.phase_time_s).min()),float(np.diff(unique.phase_time_s).max())],'peak_absolute_disturbance_torque_Nm':maxima})
 pd.concat(frames,ignore_index=True).to_csv(HERE/'joint_motion_samples.csv.gz',index=False,float_format='%.17g',compression={'method':'gzip','mtime':0})
 report={'source_campaign':'Original MyController MAIN_NS7/MAIN_NS8 campaign, archived in Thesis_Final_Control','joint_angle_source':'Measured state.q -> debug_row.q -> writeVec7Scaled(..., kRadToDeg)','recorded_interval_s':[5,9],'periodic_sample_interval_s':.05,'sources':records}
 (HERE/'joint_motion_provenance.json').write_text(json.dumps(report,indent=2)+'\n')

def plot(out):
 data=pd.read_csv(HERE/'joint_motion_samples.csv.gz',float_precision='round_trip')
 plt.rcParams.update({'text.usetex':True,'text.latex.preamble':r'\usepackage{lmodern}', 'font.family':'serif','font.size':9.5,'axes.labelsize':10,'xtick.labelsize':9,'ytick.labelsize':9,'axes.linewidth':.65,'legend.frameon':False})
 fig=plt.figure(figsize=(6.6,3.3))
 axes=[fig.add_axes([.105,.34,.405,.53]),fig.add_axes([.665,.34,.315,.53])]
 records=[]
 for ci,(cid,label,color) in enumerate(CONDITIONS):
  for ri,rep in enumerate(REPS):
   d=data[(data.condition==cid)&(data.repetition==rep)].drop_duplicates('phase_time_s')
   time=d.phase_time_s.to_numpy()-5
   q=d.q1_deg.to_numpy(); change=q-q[0]
   assert len(time)==81 and time[0]==0 and time[-1]==4
   assert np.all(np.diff(time)>0) and change[0]==0
   for ai,ax in enumerate(axes):
    if ai==1 and ci<2: continue
    selection=time<=1 if ai==1 else np.ones(len(time),dtype=bool)
    ax.plot(time[selection],change[selection],color=color,linewidth=.75,alpha=.85,marker=['o','s','^'][ri],markersize=2.4,markerfacecolor='white',markeredgewidth=.55)
   records.append({'condition':cid,'repetition':rep,'samples':len(time),'initial_q1_deg':float(q[0]),'min_change_deg':float(change.min()),'max_change_deg':float(change.max()),'end_change_deg':float(change[-1])})
 for ax in axes:
  ax.set_xlabel(r'Time, $t$ [s]')
  ax.grid(axis='y',color='.86',linewidth=.5)
  ax.axhline(0,color='.45',linewidth=.6,zorder=0)
  ax.tick_params(length=3,width=.6)
  ax.spines[['top','right']].set_visible(False)
 axes[0].set_xlim(0,4); axes[0].set_xticks([0,1,2,3,4]); axes[0].set_ylim(-.2,6.6);axes[0].set_yticks([0,2,4,6])
 axes[0].set_ylabel('Joint 1 Motion, '+r'$\Delta q_1$ [$^\circ$]')
 axes[1].set_xlim(0,1);axes[1].set_xticks([0,.25,.5,.75,1]);axes[1].set_ylim(-.03,.06);axes[1].set_yticks([-.02,0,.02,.04,.06]);axes[1].set_ylabel(r'$\Delta q_1$ [$^\circ$]')
 axes[1].xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'))
 axes[1].yaxis.set_major_formatter(FuncFormatter(lambda x,p:'0' if abs(x)<1e-10 else f'{x:.2f}'))
 axes[0].set_title('(a) All Settings',fontsize=10,pad=9)
 axes[1].set_title('(b) Conditioning: First Second',fontsize=10,pad=9)
 order=[0,2,1,3]
 handles=[Line2D([0],[0],color=CONDITIONS[i][2],lw=1.2) for i in order]
 fig.legend(handles,[CONDITIONS[i][1] for i in order],loc='lower center',bbox_to_anchor=(.54,.01),ncol=2,fontsize=8.5,columnspacing=1.3,handlelength=1.6)
 out.mkdir(parents=True,exist_ok=True)
 for ext in ['pdf','png','svg']: fig.savefig(out/f'joint_motion_time.{ext}',dpi=300,facecolor='white')
 svg=out/'joint_motion_time.svg'
 svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf8').splitlines())+'\n',encoding='utf8')
 plt.close(fig)
 result={'definition':'Delta_q1(t_d) = q1(t_d+5s) - q1(5s), in degrees','display_time':'t_d = phase_time_s - 5 s, labelled t on figures','individual_trials':True,'averaging':False,'integration':False,'interpolation':False,'smoothing':False,'duplicates':'Periodic sample rows used. Duplicate event rows have identical measured joint angles, verified before extraction.','joint_selection':'Joint 1 has the largest peak absolute directly commanded disturbance torque in each of the 12 trials','panels':[{'time_s':[0,4],'settings':'all four'},{'time_s':[0,1],'settings':'both conditioning magnitudes'}],'trials':records}
 (HERE/'joint_motion_analysis.json').write_text(json.dumps(result,indent=2)+'\n')
 print('Created joint_motion_time PDF, PNG and SVG from 12 individual measured histories.')

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--raw-root',type=Path);parser.add_argument('--reference-root',type=Path)
 parser.add_argument('--out-dir',type=Path,default=HERE.parent)
 args=parser.parse_args()
 if args.raw_root:
  assert args.reference_root
  archive(args.raw_root,args.reference_root)
 plot(args.out_dir)
