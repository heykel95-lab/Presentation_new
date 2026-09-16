# Null-space presentation narrative

The user approved this structure on 2026-09-16. No new trials or signal
processing were introduced by this presentation edit. The same 18 recorded
trials support both the main comparison and the detailed backups.

The deck has 25 main slides and 9 hidden backups. The first 20 slides retain
their order. The four main result slides are:

1. Cumulative joint motion: no torque, damping alone, conditioning alone,
   and combined control. When enabled, conditioning is 2 N m and damping
   is 2 N m s/rad.
2. Jacobian conditioning, using the same four conditions.
3. Joint motion over time, using three-trial mean onset-relative joint-1
   histories and one sample standard deviation.
4. Effect of conditioning torque: an editable table compares cumulative
   motion at 1.5 and 2 N m, with and without damping at 2 N m s/rad.

Conclusion follows at physical slide 25. Physical slides 26–34 are hidden
backups B1–B9: torque equations, disturbance video, then all seven original
six-setting result views. The full PDF contains all 34 slides, and
Supplementary_slides.pdf contains these nine backups.

The same recorded 5–9 s interval is displayed as 0–4 s. Main plots reuse the
six-setting generator's calculations, colours and uncertainty conventions.
The parameter table explicitly contains three-trial means. Complete curves
and sample standard deviations remain available in backup. Mean cumulative
motion is 0.29° versus 0.19° at 1.5 N m and 1.69° versus 0.83° at 2 N m,
for conditioning alone versus combined control. These are descriptive
comparisons. The combined trials were acquired in a later session.

## Rebuild

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
videos. The table is a native editable PowerPoint table. The matching PDF
reorders original PowerPoint-exported pages and redraws changed regions,
inserting the plot PDFs as vectors. It is not a fresh PowerPoint export.
The six native chapter sections and Overview are refreshed by a portable
equivalent of Speaking/build/update-overview.ps1.

Rebuild Speaking/Thesis_Defense_Speaking_Script.tex with the existing
Speaking/build.ps1 on Windows, or pdflatex with Speaking/build as output
directory on Linux. Copy the compiled PDF to both speaking PDFs directly
under Final Presentation. The script and notes follow all 34 slide titles
and retain technical source blocks separately from spoken points.

Validation is recorded in validation.json and verification.json. Review
images and the pre-edit snapshots stay in the ignored review directory.

The later user-requested title, Motivation and video changes are documented
in ../media_update/README.md. This directory's snapshot and validation describe
the narrative before those media changes. Do not run the older restructure
script over the current deck without preserving the newer media changes.
