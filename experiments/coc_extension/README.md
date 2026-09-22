# CoC position extension, 2026-09-21

Measured +/-90 and +/-100 mm with three repetitions for each of the two t1
entry directions: 24 added trials, 78 trials in the position plot. All earlier
points are retained. Raw logs, effective parameters, provenance and the
standalone plot generator are in Thesis_Final_Control.

From that checkout, regenerate with:

```sh
git lfs pull
python3 analysis/make_coc_position_figure.py
```

Copy the resulting CoC_position LaTeX/PDF/PNG/SVG from figures/coc_position to
the corresponding Final Presentation figure paths. The slide is identified
by its title, Effect of CoC position. Its plot was enlarged proportionally to
700 pt width so every measured x position is legible. The vertical range
includes the measured errors at +/-100 mm. The main slide PDF uses the vector
figure. All other 33 PDF pages, every other PowerPoint part, 29 native
equations, all notes and speaking files were preserved. The required Overview
check confirmed the existing six entries match native sections.

The new-trial source audit and the exact plotted endpoints are copied here.
The measurements were acquired in a later session with matching saved
calibration and impedance parameters; original files remain in the control
archive. See measurement_audit.json and verification.json.
