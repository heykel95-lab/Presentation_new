# Combined H-mode null-space experiment

Three robot trials completed on 2026-09-16. Mode 3 enables both terms:
`tau_null = -d_null N_tau dq + k_sigma N_tau n_best`, with
`d_null = 2 N m s/rad` and `k_sigma = 2 N m`.

The controller source is exactly MyController commit
`0210e7f2cca8d60ec72bf2e56e4a00d0440b037a`, archived in
`controller_source.tar`. The current Thesis_Final_Control controller omits
signals required by the existing study, so the original revision was built
in an isolated runtime. No live controller parameters were changed.

All effective parameters were copied from the original
`MAIN_NS8_ksigma_2p0_20N_200mm/r01` archive. The only changed parameter is
`nullspace_mode = 3` (previously 2). See `protocol.json` and each repeat's
`params_effective`, terminal transcript, raw CSVs and binary/source hashes.
`run_trial.py N` runs one repeat and refuses to overwrite an existing repeat.
It stops on failure and does not retry automatically.

The protocol retains the initial joint posture, Cartesian hold impedance,
5 s settling, virtual 20 N force at +200 mm on link 3, 5–7 s cosine ramp,
7–8 s hold, 8–9 s release, 3 N m disturbance torque limit, and 18 s recording.
Both null-space terms stay enabled before and during the disturbance.

The presentation analysis uses exactly 5–9 s, displayed as 0–4 s, three-trial
means and one sample SD. Cumulative motion integrates the projected speed.
Net motion projects the integrated seven-joint velocity onto the same fixed
baseline reference direction used in the original study. Joint-1 plots use
original 20 Hz measured angles relative to each trial's value at 5 s.
Means use common exact recorded times, without interpolation or smoothing.

Rebuild the figures with:

```sh
python 'Final Presentation/figures_and_images/sources/make_combined_nullspace.py'
```

Run this command from the presentation repository with numpy, pandas and
matplotlib installed. Add `--refresh` to verify and re-extract all 18 raw
trials from their local repositories. Original Windows hash records match
the Linux files after CRLF normalization. The portable compressed data,
source hashes, numerical checks and summary are beside the figure script.

All original endpoint metrics were independently reproduced. The new logs
also verify that the recorded total null-space torque norm matches the sum
of the logged conditioning torque and calculated damping torque.

Mean cumulative motion is 0.83127 degrees (sample SD 0.13792), versus
1.68699 degrees for conditioning alone at 2 N m, a 50.72% reduction.
Mean net motion is -0.01212 degrees (sample SD 0.02135). These are descriptive
comparisons. The combined trials were acquired in a later session with
matched saved settings and source revision, so session effects are not
independently controlled. No additional baseline trials were acquired.

The requested extension is limited to the final presentation. Existing thesis
figures and original four-condition presentation assets are preserved.

The additional combined setting at k_sigma = 1.5 and d_null = 2 is archived
in ../h_mode_combined_1p5. The shared generator now compares six conditions.

The approved presentation narrative now uses four conditions at fixed
`k_sigma = 2` in the main plots, followed by a compact 1.5-versus-2 comparison.
All six-condition views remain in hidden backups. See
[the narrative rebuild instructions](../nullspace_narrative/README.md).
`update_presentation.py` in this folder is the historical extension builder
and would restore the earlier slide layout.
