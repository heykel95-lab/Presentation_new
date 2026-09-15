"""Single-trial and three-trial mean views of the measured joint-1 histories.

Rebuild: python make_joint_motion_views.py --out-dir OUTPUT --repetition r01
The existing all-repetitions figure remains unchanged. Mean and sample SD use
only exact recorded timestamps shared by the three trials of each setting.
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
from make_joint_motion import CONDITIONS, REPS

HERE=Path(__file__).resolve().parent

def calculate(repetition):
    path=HERE/'joint_motion_samples.csv.gz'
    data=pd.read_csv(path,float_precision='round_trip')
    curves=[];report=[];table=[]
    for cid,label,colour in CONDITIONS:
        trials={}
        for rep in REPS:
            d=data.loc[(data.condition==cid)&(data.repetition==rep)].copy()
            assert len(d)==81 and not d.phase_time_s.duplicated().any()
            time=d.phase_time_s.to_numpy();q=d.q1_deg.to_numpy()
            assert time[0]==5 and time[-1]==9 and np.all(np.diff(time)>0)
            assert np.isfinite(q).all()
            trials[rep]=pd.Series(q-q[0],index=time)
        common=np.array(sorted(set.intersection(*(set(v.index) for v in trials.values()))))
        assert common[0]==5 and common[-1]==9 and len(common)>=80
        values=np.array([trials[rep].loc[common].to_numpy() for rep in REPS])
        mean=values.mean(axis=0);sd=values.std(axis=0,ddof=1)
        assert mean[0]==0 and sd[0]==0
        single=trials[repetition]
        curves.append({'single_time':single.index.to_numpy()-5,'single':single.to_numpy(),
                       'mean_time':common-5,'mean':mean,'sd':sd})
        report.append({'condition':cid,'single_repetition':repetition,'single_samples':len(single),
          'mean_common_samples':len(common),'single_endpoint_deg':float(single.iloc[-1]),
          'mean_endpoint_deg':float(mean[-1]),'sample_sd_endpoint_deg':float(sd[-1]),
          'unshared_recorded_times_s':{rep:sorted(set(v.index)-set(common)) for rep,v in trials.items()}})
        for t,m,s in zip(common-5,mean,sd):table.append((cid,t,m,s))
    summary={'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'definition':'Delta q1(t) = q1(t+5 s) - q1(5 s), in degrees',
      'single_repetition':repetition,'selection_rule':'Same repetition number for every setting',
      'mean':'Arithmetic mean of three onset-relative joint-angle changes at exact common recorded timestamps',
      'uncertainty':'One sample standard deviation across three trials, ddof=1',
      'interpolation':False,'time_rounding':False,'smoothing':False,'integration':False,
      'absolute_values':False,'recorded_interval_s':[5,9],'display_interval_s':[0,4],
      'conditioning_detail_s':[0,1],'conditions':report}
    return curves,summary,table

def plot(curves,out,view):
    plt.rcParams.update({'text.usetex':True,'text.latex.preamble':r'\usepackage{lmodern}',
      'font.family':'serif','font.size':9.5,'axes.labelsize':10,'xtick.labelsize':9,
      'ytick.labelsize':9,'axes.linewidth':.65,'legend.frameon':False})
    fig=plt.figure(figsize=(6.6,3.3))
    axes=[fig.add_axes([.105,.34,.405,.53]),fig.add_axes([.665,.34,.315,.53])]
    for ci,((cid,label,colour),curve) in enumerate(zip(CONDITIONS,curves)):
        time=curve[view+'_time'];value=curve[view]
        for ai,ax in enumerate(axes):
            if ai==1 and ci<2:continue
            selection=time<=1 if ai==1 else np.ones(len(time),dtype=bool)
            ax.plot(time[selection],value[selection],color=colour,lw=.9,
              marker=['o','s','^','D'][ci],markersize=2.6,markerfacecolor='white',markeredgewidth=.6)
            if view=='mean':
                low=value-curve['sd'];high=value+curve['sd']
                ax.fill_between(time[selection],low[selection],high[selection],color=colour,alpha=.13,lw=0)
                assert np.min(low[selection])>(-.03 if ai==1 else -.2)
                assert np.max(high[selection])<(.06 if ai==1 else 6.6)
    for ax in axes:
        ax.set_xlabel(r'Time, $t$ [s]');ax.grid(axis='y',color='.86',lw=.5)
        ax.axhline(0,color='.45',lw=.6,zorder=0);ax.tick_params(length=3,width=.6)
        ax.spines[['top','right']].set_visible(False)
    axes[0].set_xlim(0,4);axes[0].set_xticks([0,1,2,3,4]);axes[0].set_ylim(-.2,6.6);axes[0].set_yticks([0,2,4,6])
    axes[0].set_ylabel('Joint 1 Motion, '+r'$\Delta q_1$ [$^\circ$]')
    axes[1].set_xlim(0,1);axes[1].set_xticks([0,.25,.5,.75,1]);axes[1].set_ylim(-.03,.06)
    axes[1].set_yticks([-.02,0,.02,.04,.06]);axes[1].set_ylabel(r'$\Delta q_1$ [$^\circ$]')
    axes[1].xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'))
    axes[1].yaxis.set_major_formatter(FuncFormatter(lambda x,p:'0' if abs(x)<1e-10 else f'{x:.2f}'))
    axes[0].set_title('(a) All Settings',fontsize=10,pad=9)
    axes[1].set_title('(b) Conditioning: First Second',fontsize=10,pad=9)
    order=[0,2,1,3]
    handles=[Line2D([0],[0],color=CONDITIONS[i][2],lw=1.2,marker=['o','s','^','D'][i],markersize=3,markerfacecolor='white') for i in order]
    fig.legend(handles,[CONDITIONS[i][1] for i in order],loc='lower center',bbox_to_anchor=(.54,.01),ncol=2,fontsize=8.5,columnspacing=1.3,handlelength=1.6)
    out.mkdir(parents=True,exist_ok=True)
    for ext in ['pdf','png','svg']:fig.savefig(out/f'joint_motion_{view}.{ext}',dpi=300,facecolor='white')
    p=out/f'joint_motion_{view}.svg';p.write_text('\n'.join(s.rstrip() for s in p.read_text(encoding='utf8').splitlines())+'\n',encoding='utf8')
    plt.close(fig)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',type=Path,default=HERE.parent)
    parser.add_argument('--repetition',choices=REPS,default='r01')
    args=parser.parse_args();curves,summary,table=calculate(args.repetition)
    for view in ['single','mean']:plot(curves,args.out_dir,view)
    (HERE/'joint_motion_views_analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
    pd.DataFrame(table,columns=['condition','time_s','mean_joint_motion_deg','sample_sd_deg']).to_csv(HERE/'joint_motion_mean_curves.csv',index=False,float_format='%.17g')
    print('Created single-trial and three-trial mean joint-motion figures.')
    print(json.dumps(summary['conditions'],indent=2))
