# Combined H-mode: k_sigma = 1.5, d_null = 2

Three successful real-robot trials were acquired on 2026-09-16 in mode 3,
with both conditioning and damping active before and during the disturbance.

The executable is identical to the preceding combined k_sigma = 2 campaign,
built from original controller commit 0210e7f2cca8d60ec72bf2e56e4a00d0440b037a.
Its exact source archive is ../h_mode_combined/controller_source.tar. Binary
hashes, raw-log hashes and acquisition checks are in each provenance.json.

The effective parameters were copied from original conditioning-only trial
MAIN_NS8_ksigma_1p5_20N_200mm/r01. Only nullspace_mode changes from 2 to 3.
The saved initial joint posture, Cartesian hold impedance, 20 N virtual force
on link 3 at +200 mm, 5 s settling, 5–7 s ramp, 7–8 s force hold, 8–9 s release,
3 N m disturbance torque limit, and 18 s recording are retained.

Results over the original 5–9 s interval, shown as 0–4 s:

| Metric | Three-trial mean | Sample SD |
| --- | ---: | ---: |
| Cumulative joint motion, degrees | 0.192175003 | 0.009410494 |
| Net joint motion, degrees | 0.002090280 | 0.010357055 |

Cumulative motion is 33.18% below the original conditioning-only 1.5 N m
mean of 0.287611011 degrees. This is a descriptive comparison. The combined
trials were acquired later, so session effects are not independently controlled.

The six-condition generator is:
Final Presentation/figures_and_images/sources/make_combined_nullspace.py
It preserves the original baseline reference direction, full-rate integration,
three-trial means and one sample SD. Joint-1 figures use original measured
samples, and averages use exact shared timestamps without interpolation.
All 15 previously plotted trial results are preserved. Six combined trials
are checked against their archived hashes and the sum of both torque terms.

Run from the presentation root with numpy, pandas and matplotlib installed:

```sh
python 'Final Presentation/figures_and_images/sources/make_combined_nullspace.py'
```

The additional condition is purple throughout all seven null-space plots.
The final PowerPoint, PDF, notes and speaking script include six settings.
The extension remains limited to the presentation.

The approved narrative presents the 1.5 and 2 results together in a compact
main-slide table. The detailed six-condition curves remain in hidden backups.
See [the narrative rebuild instructions](../nullspace_narrative/README.md).
