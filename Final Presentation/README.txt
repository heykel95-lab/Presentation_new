Active defense presentation

Thesis_Defense_gg0_v3.pptx contains 25 main slides and nine hidden backups.
Thesis_Defense_gg0_v3.pdf contains all 34 slides. Supplementary_slides.pdf contains all nine backups from physical pages 26–34.
Contact demonstration is visible at physical slide 3, immediately after Motivation, with no viewing-cue text beneath the video. Overview follows at physical slide 4.
The hidden backups begin with Null-space torques and projector (B1) and Disturbance demonstration (B2) at physical slides 26 and 27. The seven complete six-setting result views follow as B3–B9.
Native chapter sections, six-entry Overview, original theme, equations and embedded videos are retained. All three embedded videos start on click.

The contact results use angular error relative to the calibrated surface normal.
The plotted quantity is the first-tangent component theta_err,t1. It comes from measured end-effector orientation and the calibrated tool normal.
The entry value is theta_meas,t1. The angular error replaces the former end-to-entry contact response.
Endpoint means and sample standard deviations use all 69 original terminal-report records at 0.01-degree precision. The CoC comparison includes the completed -80 mm and +80 mm conditions for both entry directions.
The three representative full time histories retain model-estimated normal force and TCP moment.
Timing compares entry into and remaining within 0.1 degree of the angular error: approximately 2.5 s at +40 mm and 3.6 s at the TCP.
Calibration and mount uncertainty affects the estimate of physical alignment. A zero first-tangent component alone does not establish complete alignment.

Speaking/Thesis_Defense_Speaking_Script.tex and PowerPoint notes are synchronized with all 34 slides.
Speaking/build.ps1 builds Thesis_Defense_Speaking_Script.pdf. No talk duration has been measured.
Speaker_notes_and_timing.txt now contains the same spoken points without obsolete timings.

Figure assets and editable sources are in figures_and_images. Provenance is in figures_and_images/manifest.json.
Reproducible data: MyOwn/code/python/figures/contact_angular_error/.
After editing slides, refresh Overview from native sections using Speaking/build/update-overview.ps1 or the portable equivalent in ../experiments/nullspace_narrative/restructure_presentation.py. Rebuild the speaking script and include all 34 slides in the PDF.

Equations (uniform typography updated 2026-09-16)
All 35 standalone formula and symbol shapes use 22 pt Cambria Math, regular weight and black, including the backup equations. Mathematical subscripts and superscripts retain their normal scaling. Bold matrix zeros have been replaced with regular zeros, oversized equations reduced and related equals signs aligned. The formulas remain native editable PowerPoint equations, so IguanaTex is not required.
Click inside a formula to edit it using PowerPoint Equation tools. The LaTeX sources remain in figures_and_images/sources. native_equations.json maps each equation to its slide, shape name and exact LaTeX. Each equation also has the source in its alternative text.
Keep formula changes synchronized between the LaTeX source, native PowerPoint equation, source catalog, speaking script and notes. Editing a .tex file alone does not automatically update the PowerPoint equation. Graphs and schematic illustrations retain their editable figure sources.
The matching equation PDF/PNG/SVG assets use vectors from the native PowerPoint export at the uniform size. Source wrappers declare Cambria Math and require LuaLaTeX with the font installed. See ../experiments/equation_style/README.md for validation and reproduction details. Earlier deck builders predate this formatting update.

Controller error sketches (2026-09-15): position error and axis-angle correction are illustrated separately. The rotational equation is e_R = phi u. The rotation-matrix identity was removed. Both new images and their LaTeX/PDF/PNG/SVG sources are in figures_and_images.

Review update: the separate null-space theory, experiment and four main result slides follow all contact results. Displayed numbers use at most two decimal places or scientific notation. The shared surface-frame sketch includes the tool.

The PDF retains the original PowerPoint-exported pages, with changed regions redrawn and vector plots inserted. It includes all nine hidden backups. This revision is not a fresh PowerPoint export.
Null-space label formatting is reproducible with figures_and_images/sources/format_nullspace_for_presentation.py using the thesis analysis and archived results.

Approved null-space narrative (2026-09-16)
----------------------------------------
Physical slides 21–24 present cumulative joint motion, Jacobian conditioning,
the three-trial mean joint-motion history, and a compact parameter comparison.
Conclusion is physical slide 25. The main plots compare no null-space torque,
damping alone, conditioning alone and combined control. Enabled settings are
fixed at k_sigma = 2 N m and d_null = 2 N m s/rad.

The editable comparison table shows three-trial mean cumulative motion:
                          Conditioning alone    Combined
k_sigma = 1.5 N m               0.29 deg         0.19 deg
k_sigma = 2 N m                 1.69 deg         0.83 deg
Damping is 2 N m s/rad in both combined cases. Its addition reduced motion
at both conditioning values. The lower tested conditioning value produced
less motion in both cases. Near-zero net motion can coexist with reversals.

The hidden backups are:
B1 (26) Null-space torques and projector
B2 (27) Disturbance demonstration
B3 (28) Cumulative joint motion: all settings
B4 (29) Jacobian conditioning: all settings
B5 (30) Joint motion: mean of three trials
B6 (31) Joint motion: all individual trials
B7 (32) Joint motion: one trial per setting
B8 (33) Net joint motion over time
B9 (34) Net joint motion

All result plots use the same 18 recorded trials and recorded 5–9 s interval,
displayed as 0–4 s. Bands show one sample standard deviation across three
trials. Joint-angle means use exact shared recorded timestamps, without
interpolation or smoothing. The single-trial backup uses r01 for every setting.
The combined runs were acquired in a later session with matched archived
settings and original source revision. Session effects are not independently
controlled. The original thesis figures and data remain unchanged.

Rebuild six-setting plots with figures_and_images/sources/make_combined_nullspace.py.
Rebuild main plots with figures_and_images/sources/make_nullspace_narrative.py.
Deck restructuring and validation: ../experiments/nullspace_narrative/README.md.
The older h_mode_combined/update_presentation.py restores the superseded
30-slide structure. Do not use it directly for the active narrative.


Stiffness results: physical slide 16 (footer 15) shows only Effect of rotational stiffness. The K_p,t2 sweep plot, its takeaway and the tangential-stiffness conclusion/narration have been removed from the presentation. The common contact settings remain part of the experimental method.

Full wrench matrix: footer 7 uses the force/moment and error/velocity columns from footer 5, with A-transpose and A around both stiffness and damping blocks. Underbraces identify K_TCP and D_TCP. The full equation replaces the two compact transformation equations and remains natively editable. Source: figures_and_images/sources/coupling_wrench_blocks.tex.

## Consistent joint-motion names (2026-09-15)

Use cumulative joint motion for E_N and net joint motion for Delta eta in
plots, captions, text, the symbol list and the presentation. Retain cumulative
and net because the quantities differ: the former accumulates projected
velocity magnitude, while the latter projects the integrated joint velocity
onto the common reference direction and permits cancellation. Use Net joint
motion over time for its directional history, and Joint motion over time for
the individual measured joint-angle histories. Define the projection and the
measured angle change in the methodology. Do not alternate motion and
displacement as short names for these quantities. Keep symbols, calculations,
data, units, signs, uncertainty, filenames and internal identifiers unchanged.

Original four-setting joint-motion sources remain available for provenance:
make_joint_motion.py, make_joint_motion_views.py and make_nullspace_displacement.py.
The active main and backup views use the generators described above.

Coupling slide simplification (2026-09-16): removed Error at the CoC, Wrench at the TCP and their standalone equations from footer 7. Retained the full shifted wrench matrix. Notes and speaking text describe the transformed stiffness and damping directly.

Jacobian velocity equation (2026-09-16): Real-time control, footer 6, displays [p_dot_EE; omega_EE] = J(q) q_dot as an editable equation instead of the verbal velocity mapping. The thesis uses this same differential-kinematics equation.

Robot illustration palette (2026-09-16): on footers 4 and 5 only, the pose and positional-error figures use theme blue for the robot and grippers, with lighter blue depth shading. Their three figure asset sets are regenerated from the existing LaTeX/TikZ sources. Geometry and axis/reference colours are preserved.

Rotational-error palette (2026-09-16): the slide-5 tool face is filled theme blue, with a lighter-blue dashed desired orientation. Solid and dashed outlines distinguish the orientations. Geometry and the black correction angle and axis are preserved.

Combined null-space extension (2026-09-16)
-----------------------------------------
The final deck now compares six settings with three trials each. The added
H-mode setting uses mode 3, k_sigma = 1.5 or 2 N m and d_null = 2 N m s/rad.
All seven detailed null-space result plots include the measured extension
and remain in hidden backups. The main subset, parameter table, experiment
slide, conclusion, notes, speaking script and PDFs follow the approved narrative.
The combined curves are purple at 1.5 N m and green at 2 N m.
Protocol, raw logs and provenance: ../experiments/h_mode_combined/README.md
and ../experiments/h_mode_combined_1p5/README.md
Rebuild figures: figures_and_images/sources/make_combined_nullspace.py
The extension is presentation-only; the original thesis assets are retained.

Title, Motivation and disturbance media (2026-09-16)
-------------------------------------------------
The title slide now shows the full user-supplied title_robot.jpg on the right.
Motivation, numbered 1, uses thesis Figure 1.1, Sources of angular offset at
surface entry, above the Problem and Idea text. The exact vector figure was
extracted from printed thesis page 1.

B2 now contains Nullspace1 and Nullspace2 side by side, each starting on click.
The presentation copies play upright and retain the original audio and all
frames. The supplied source MP4s are preserved. The previous disturbance clip
and its phase-sequence cue have been replaced. No controller settings are
assigned to the new videos without supporting information.

The deck remains 25 main slides and nine hidden backups. The PDF, supplementary
PDF, speaking script and notes match these media changes. Rebuild and checks:
../experiments/media_update/README.md. The earlier narrative validation records
refer to the pre-media-update version.
