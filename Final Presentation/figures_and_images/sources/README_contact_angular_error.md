# Calibrated-normal contact angular-error figures

The endpoint panels (`baseline_response`, `rotation_stiffness`,
`translation_stiffness`, `CoC_position`) contain the regenerated means and
sample standard deviations from 93 terminal endpoint reports over 31 settings.
Terminal values were archived to 0.01 degree. A standard deviation displayed
as 0.00 degree represents repeated rounded values, not zero uncertainty.

`angular_quantities` shows explicit normal arrows for the inward calibrated
surface reference and the measured tool directions at entry and end. Both
angle arcs begin at `-n_s`. The corresponding frame inset has `t2` upward,
`n_s` leftward and `t1` out of the page, with positive rotation anticlockwise.
The geometry is schematic and the common origin is not a contact point.
The symbol asset is `symbol_thetaerr`. Keep the three descriptive arrow labels,
without the normal-vector symbols beneath them. The angle label is
`theta_err,t1`, without an end-time argument. The separate frame inset retains
its coordinate symbols. Use this same label treatment in the thesis figure.

`contact_wrench_three_panels.tex` contains three panels with the same grid as
thesis Figure 5.7: light solid horizontal lines and darker dotted vertical
lines at the existing ticks. `results_grid.py` supplies the shared style.
The angular-error panel reads the three `contact_error_*_r01.csv` files.
The force and moment panels read `contact_wrench_samples.csv.gz`, exported
from the same three archived r01 contact trials by the thesis's
`plot_coc_case.load` and `thin` functions. The cache retains every sample
used by those curves, with round-trip floating-point precision. It adds
no interpolation or smoothing. Axes retain their previous ranges and ticks.
All three panel PDFs use the native 224 by 231.826087 pt slide dimensions.

To rebuild the time-history panels and their containing figure:

```powershell
python make_contact_error_panel.py
python make_contact_wrench_panels.py
pdflatex -interaction=nonstopmode -halt-on-error contact_wrench_three_panels.tex
```

Each other `.tex` file compiles directly from this folder with `pdflatex`.
Export matching bitmap/vector variants with `pdftocairo -png -singlefile -r
300` and `pdftocairo -svg`. The source metric audit, endpoint summaries and
generators live in `MyOwn/code/python/figures/contact_angular_error/` and
`MyOwn/code/python/figures/make_contact_angular_error_figures.py`.

Angular error is the shortest rotation from the inward calibrated
surface normal to the calibrated tool-face normal obtained from measured
end-effector orientation, projected on the first tangent. It reverses the
archived tool-to-reference normal-error component. It is not a subtraction of
finite orientation-angle components. Zero refers to the calibrated normal,
with residual calibration and mounting limitations.

The CoC comparison includes thirteen positions from -100 to +100 mm,
including +/-90 mm, with three-repeat means and sample SD. The 24 trials
at +/-90 and +/-100 mm were acquired on 2026-09-21 in a later session with
matching saved calibration and impedance parameters. All original points
remain unchanged. See experiments/coc_extension/README.md and its audit.
Representative wrench traces remain at -40 mm, TCP and +40 mm.

Regenerate both plot variants from the control checkout with
`python3 analysis/make_coc_position_figure.py` after `git lfs pull`.
