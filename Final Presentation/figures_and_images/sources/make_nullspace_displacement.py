"""Plot directional null-space displacement from the recorded joint velocities.

Rebuild from the portable recorded-sample archive beside this script:
    python make_nullspace_displacement.py
Refresh that archive using the original twelve controller logs:
    python make_nullspace_displacement.py --raw-root PATH/experiments/results

At each time, integrate all seven projected joint velocities with the recorded
time steps, then resolve that vector onto the fixed reference direction used
by the thesis net-displacement metric. There is no absolute value or norm in
this displacement integral. The positive reference direction is the mean net
motion of the three no-null-space-torque trials. This is a joint-space
component, not a tool angle or a full seven-joint posture difference.
"""
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MultipleLocator, FuncFormatter

HERE=Path(__file__).resolve().parent
CONDITIONS=[
    ('MAIN_NS7_baseline_20N_200mm','No Null-Space Torque','#000000','o'),
    ('MAIN_NS7_damping_2p0_20N_200mm',r'Projected Damping, $d_{\mathrm{null}}=2\,\mathrm{N\,m\,s/rad}$','#c00000','s'),
    ('MAIN_NS8_ksigma_1p5_20N_200mm',r'Conditioning, $k_\sigma=1.5\,\mathrm{N\,m}$','#0057b8','^'),
    ('MAIN_NS8_ksigma_2p0_20N_200mm',r'Conditioning, $k_\sigma=2.0\,\mathrm{N\,m}$','#e0ad00','D'),
]
COLS=['time','nullspace_speed']+[f'nullspace_dq_{j}' for j in range(1,8)]
EXPECTED_CUMULATIVE_RAD=np.array([.132614246,.0992980553,.0050197591,.0294435416])
EXPECTED_NET_RAD=np.array([.131175694,.0978973381,.000253676218,-.000185304078])


def archive(raw_root):
    frames=[];provenance=[]
    for cid,_,_,_ in CONDITIONS:
        for rep in ['r01','r02','r03']:
            path=raw_root/cid/rep/'surface_grinding_controller_log.csv'
            frame=pd.read_csv(path,usecols=COLS,float_precision='round_trip')
            frame=frame.loc[frame.time.between(5.,9.)].copy()
            frame.insert(0,'repetition',rep);frame.insert(0,'condition',cid)
            frames.append(frame)
            provenance.append({'condition':cid,'repetition':rep,'source':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'recorded_window_samples':len(frame)})
    data=pd.concat(frames,ignore_index=True)
    data.to_csv(HERE/'nullspace_displacement_samples.csv.gz',index=False,float_format='%.17g',compression={'method':'gzip','mtime':0})
    (HERE/'nullspace_displacement_provenance.json').write_text(json.dumps({'recorded_interval_s':[5,9],'columns':COLS,'sources':provenance},indent=2)+'\n')


def calculate():
    data=pd.read_csv(HERE/'nullspace_displacement_samples.csv.gz',float_precision='round_trip')
    runs=[]
    for cid,_,_,_ in CONDITIONS:
        for rep in ['r01','r02','r03']:
            d=data[(data.condition==cid)&(data.repetition==rep)]
            t=d.time.to_numpy();dq=d[COLS[2:]].to_numpy();speed=d.nullspace_speed.to_numpy()
            assert len(t)>2 and t[0]==5 and t[-1]==9 and np.all(np.diff(t)>0)
            assert np.isfinite(d[COLS].to_numpy()).all()
            dt=np.diff(t)
            vector=np.vstack([np.zeros((1,7)),np.cumsum(.5*(dq[:-1]+dq[1:])*dt[:,None],axis=0)])
            assert np.max(np.abs(np.linalg.norm(dq,axis=1)-speed))<2e-9
            cumulative=np.sum(.5*(speed[:-1]+speed[1:])*dt)
            runs.append({'condition':cid,'repetition':rep,'time':t,'dq':dq,'vector':vector,'cumulative_rad':cumulative})
    reference=np.mean([r['vector'][-1] for r in runs[:3]],axis=0)
    reference/=np.linalg.norm(reference)
    # Average only common, actually recorded timestamps. No missing samples
    # are reconstructed and no orientation or velocity signals are smoothed.
    common=runs[0]['time']
    for r in runs[1:]:common=np.intersect1d(common,r['time'])
    assert common[0]==5 and common[-1]==9
    curves=[]
    for r in runs:
        indices=np.searchsorted(r['time'],common)
        assert np.array_equal(r['time'][indices],common)
        curves.append(np.degrees(r['vector'][indices]@reference))
    curves=np.array(curves).reshape(4,3,-1)
    means=curves.mean(axis=1);sds=curves.std(axis=1,ddof=1)
    cumulative=np.array([r['cumulative_rad'] for r in runs]).reshape(4,3).mean(1)
    # Independent endpoint checks against the published, rounded summary.
    assert np.allclose(cumulative,EXPECTED_CUMULATIVE_RAD,rtol=0,atol=5e-10)
    assert np.allclose(np.radians(means[:,-1]),EXPECTED_NET_RAD,rtol=0,atol=5e-10)
    assert np.all(curves[:,:,0]==0)
    for r in runs:
        # Integrating a component and projecting the vector integral agree.
        scalar=r['dq']@reference;dt=np.diff(r['time'])
        assert np.isclose(np.sum(.5*(scalar[:-1]+scalar[1:])*dt),r['vector'][-1]@reference,atol=1e-13,rtol=0)
    rows=[]
    for i,(cid,_,_,_) in enumerate(CONDITIONS):
        for j,t in enumerate(common):rows.append((cid,t-5,means[i,j],sds[i,j]))
    pd.DataFrame(rows,columns=['condition','time_s','displacement_mean_deg','displacement_sample_sd_deg']).to_csv(HERE/'nullspace_displacement_curves.csv.gz',index=False,float_format='%.17g',compression={'method':'gzip','mtime':0})
    report={'definition':'Delta_eta(t) = v_ref^T integral_5^t dq_null(tau) d_tau','reference_direction':reference.tolist(),'positive_direction':'Mean net projected motion of the no-null-space-torque trials','recorded_interval_s':[5,9],'display_interval_s':[0,4],'recorded_samples_per_run':[len(r['time']) for r in runs],'common_recorded_timestamps':len(common),'interpolation':False,'averaging':'Three-trial mean and one sample standard deviation','endpoint_matches_published_net_displacement':True,'cumulative_matches_published_motion':True,'endpoint_means_deg':means[:,-1].tolist(),'endpoint_sample_sd_deg':sds[:,-1].tolist(),'conditioning_mean_ranges_deg':[[float(means[i].min()),float(means[i].max())] for i in [2,3]]}
    (HERE/'nullspace_displacement_analysis.json').write_text(json.dumps(report,indent=2)+'\n')
    return common-5,means,sds


def plot(time,means,sds,out):
    # Register the installed Latin Modern face when available on Windows.
    for path in Path(r'C:\Program Files\MiKTeX\fonts\opentype\public\lm').glob('lmroman10-regular.otf'):
        font_manager.fontManager.addfont(str(path))
    plt.rcParams.update({'font.family':'serif','font.serif':['Latin Modern Roman','CMU Serif','DejaVu Serif'],'mathtext.fontset':'cm','pdf.fonttype':42,'ps.fonttype':42,'font.size':13,'axes.labelsize':14,'xtick.labelsize':12,'ytick.labelsize':12,'axes.linewidth':.8,'axes.grid':True,'axes.grid.axis':'y','grid.alpha':.30,'grid.linewidth':.6,'legend.frameon':False,'axes.unicode_minus':True})
    fig=plt.figure(figsize=(9.3,4.0))
    axes=[fig.add_axes([.10,.35,.43,.57]),fig.add_axes([.69,.35,.28,.57])]
    # Select actual recorded times only. Full-resolution integration precedes
    # this display reduction, so the endpoint and all analyses are unchanged.
    indices=np.unique(np.linspace(0,len(time)-1,min(900,len(time))).round().astype(int))
    handles=[]
    for i,(_,label,colour,marker) in enumerate(CONDITIONS):
        for ax in ([axes[0],axes[1]] if i>=2 else [axes[0]]):
            line,=ax.plot(time[indices],means[i,indices],color=colour,linewidth=1.25,marker=marker,markevery=(10 if i==3 else 0,112),markersize=4.5,markerfacecolor='white',markeredgewidth=1.,label=label)
            ax.fill_between(time[indices],means[i,indices]-sds[i,indices],means[i,indices]+sds[i,indices],color=colour,alpha=.10,linewidth=0)
            if ax is axes[0]:handles.append(line)
    for ax in axes:
        ax.set_xlim(0,4);ax.set_xticks([0,1,2,3,4]);ax.set_xlabel(r'Time, $t$ [s]')
        ax.axhline(0,color='.4',linewidth=.8,zorder=0)
    axes[0].set_ylabel('Projected Displacement,\n'+r'$\Delta\eta$ [$^\circ$]')
    axes[0].set_ylim(-.3,8.7);axes[0].yaxis.set_major_locator(MultipleLocator(2))
    axes[1].set_ylabel(r'$\Delta\eta$ [$^\circ$]')
    axes[1].set_ylim(-.045,.085);axes[1].yaxis.set_major_locator(MultipleLocator(.04))
    axes[1].yaxis.set_major_formatter(FuncFormatter(lambda x,pos:'0' if abs(x)<1e-12 else f'{x:.2f}'))
    assert np.min(means[2:]-sds[2:])>-.045 and np.max(means[2:]+sds[2:])<.085
    order=[0,2,1,3]
    fig.legend([handles[i] for i in order],[CONDITIONS[i][1] for i in order],loc='lower center',bbox_to_anchor=(.53,.005),ncol=2,fontsize=11.5,handlelength=1.8,columnspacing=1.5,labelspacing=.45)
    out.mkdir(parents=True,exist_ok=True)
    for extension in ['pdf','png','svg']:fig.savefig(out/f'nullspace_displacement_time.{extension}',dpi=300,facecolor='white')
    svg=out/'nullspace_displacement_time.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf8').splitlines())+'\n',encoding='utf8')
    plt.close(fig)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-root',type=Path)
    parser.add_argument('--out-dir',type=Path,default=HERE.parent)
    args=parser.parse_args()
    if args.raw_root:archive(args.raw_root)
    t,mean,sd=calculate();plot(t,mean,sd,args.out_dir)
    print('Endpoint means [degrees]:',mean[:,-1].tolist())
    print('Verified the existing cumulative and net results. Shared recorded samples:',len(t))
