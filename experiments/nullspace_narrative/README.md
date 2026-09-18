# Null-space presentation narrative

The user approved this structure on 2026-09-16. No new trials or signal
processing were introduced by this presentation edit. The same 18 recorded
trials support both the main comparison and the detailed backups.

After the 2026-09-18 removal of the conditioning-torque table, the deck has 24 main slides and 9 hidden backups. The first 20 slides retain
their order. The three main result slides are:

1. Cumulative joint motion: no torque, damping alone, conditioning alone,
   and combined control. When enabled, conditioning is 2 N m and damping
   is 2 N m s/rad.
2. Jacobian conditioning, using the same four conditions.
3. Joint motion over time, using three-trial mean onset-relative joint-1
   histories and one sample standard deviation.

Conclusion follows at physical slide 24. Physical slides 25–33 are hidden
backups B1–B9: torque equations, disturbance video, then all seven original
six-setting result views. The full PDF contains all 33 slides, and
Supplementary_slides.pdf contains these nine backups.

The same recorded 5–9 s interval is displayed as 0–4 s. Main plots reuse the
six-setting generator's calculations, colours and uncertainty conventions.
The removed parameter table is preserved in archive/removed_conditioning_torque_slide_20260918.pptx with its original notes. It contains three-trial means. Complete curves
and sample standard deviations remain available in backup. Mean cumulative
motion is 0.29° versus 0.19° at 1.5 N m and 1.69° versus 0.83° at 2 N m,
for conditioning alone versus combined control. These are descriptive
comparisons. The combined trials were acquired in a later session.

## Main-plot update on 2026-09-18

Footers 21 and 22 omit the (SI) legend suffix. Both panels on footer 22 use
the same Joint 1 Motion y-axis label. The detail panel covers 0–4 s with all
original common samples and full sample-SD bands. Its line colours, widths,
markers and marker sizes match footer 21, with markers spaced along the lines.
Rebuild only these assets with make_nullspace_narrative.py --only conditioning joint.
The generator preserves audited reports byte-for-byte and checks numerical
identity within floating-point roundoff across platforms.
Speaking text and notes are frozen. Do not synchronize them during slide edits.

## Reproduce the current Matplotlib plots

The generator and all required data are versioned together under
`Final Presentation/figures_and_images/sources/`. Normal plotting runs use
only these files and do not require the original controller repository:

- `make_nullspace_narrative.py` selects the four main-slide settings.
- `make_combined_nullspace.py` supplies the shared calculations and styles.
- `combined_nullspace_samples.csv.gz` contains the recorded null-space
  velocities and Jacobian conditioning for all 18 trials over 5–9 s.
- `combined_joint_samples.csv.gz` contains the recorded joint positions
  over that interval.
- `combined_nullspace_analysis.json` and `combined_nullspace_summary.csv`
  provide the audited reference results checked and preserved by the generator.
- `combined_nullspace_provenance.json` records the original trial paths,
  hashes and acquisition checks.

With Python 3.11 or later, run these commands from the repository root:

```sh
python -m pip install -r "Final Presentation/figures_and_images/sources/requirements-nullspace.txt"
python "Final Presentation/figures_and_images/sources/make_nullspace_narrative.py" --only conditioning joint
```

This rebuilds `nullspace_conditioning_main` and `joint_motion_mean_main`
as PDF, PNG and SVG files in `Final Presentation/figures_and_images/`.
Omit `--only conditioning joint` to also generate the main cumulative-motion
plot. These commands generate assets only. They do not update the deck or
its speaker notes. The six-setting generator's `--refresh` option is solely
for re-importing original acquisition logs and is unnecessary for reproduction.

The pinned package versions are those used for the current plots. Means use
the recorded timestamps shared by the three trials, and uncertainty is one
sample standard deviation (`ddof=1`). There is no interpolation or smoothing.
An isolated rebuild with Python 3.12.13 and these package versions reproduced
both current PNGs pixel for pixel, with input data and audited reports unchanged.

## Historical rebuild

Run from the repository root, with numpy, pandas, matplotlib, lxml,
python-pptx and PyMuPDF available:

```sh
python 'Final Presentation/figures_and_images/sources/make_combined_nullspace.py'
python 'Final Presentation/figures_and_images/sources/make_nullspace_narrative.py'
python experiments/nullspace_narrative/restructure_presentation.py
python experiments/nullspace_narrative/validate_presentation.py
```

The restructure script requires the local pre-edit snapshot in ignored
`review/`: before.pptx, before.pdf, before_script.tex and before_equations.json.
It rebuilds from that snapshot, so do not run it over later deck edits without
first adapting the script and snapshot. The older updater in
`experiments/h_mode_combined/` restores the earlier 30-slide structure.

PowerPoint XML is edited directly to preserve native equations and embedded
videos. The archived table is a native editable PowerPoint table. The matching PDF
reorders original PowerPoint-exported pages and redraws changed regions,
inserting the plot PDFs as vectors. It is not a fresh PowerPoint export.
The six native chapter sections and Overview are refreshed by a portable
equivalent of Speaking/build/update-overview.ps1.

Only if the user explicitly requests changes to the frozen speaking material, rebuild Speaking/Thesis_Defense_Speaking_Script.tex with the existing
Speaking/build.ps1 on Windows, or pdflatex with Speaking/build as output
directory on Linux. Copy the compiled PDF to both speaking PDFs directly
under Final Presentation. The frozen script retains the earlier 34-slide
order and technical source blocks separately from spoken points.

Validation is recorded in validation.json and verification.json. Review
images and the pre-edit snapshots stay in the ignored review directory.

The later user-requested title, Motivation and video changes are documented
in ../media_update/README.md. This directory's snapshot and validation describe
the narrative before those media changes. Do not run the older restructure
script over the current deck without preserving the newer media changes.
