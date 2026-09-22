Active defense presentation

2026-09-22: The null-space evaluation uses cumulative projected joint motion across all seven joints, minimum singular value and measured joint-1 angle change. The slide deck, notes, speaking material and active figure sources follow this three-quantity narrative.

2026-09-22: Opposing moment is now hidden B1 / physical slide 27, immediately after Conclusion. The other backups retain their relative order: torque equations, cumulative motion, conditioning, individual trials, angular quantities, baseline angular error, and sources of angular offset. Only order and footer numbers changed. Video, figures and notes remain unchanged. There are still 26 main slides and eight backups. Both PDFs and the equation catalog follow the new order. See ../experiments/media_update/opposing_moment_first_20260922.json.

2026-09-22: Removed the former backup B2 Disturbance demonstration and archived its original slide, notes and recording. The two main clips retain their videos and now read Demonstration · Part 1 / Demonstration · Part 2, without the recording identifier 2 or time ranges. The deck has 26 main slides and eight hidden backups, 34 slides in total. Later backups are renumbered, with the restored Angular quantities and Sources of angular offset figures unchanged at B5 and B8. The supplementary PDF has eight pages. See ../experiments/media_update/backup_demo_removed_20260922.json. These counts supersede earlier records below.

2026-09-22: Restored B6 and B9 to the author-selected committed thesis figure designs, in both presentation and thesis. B6 uses the committed angular PDF with the blue error arc inside and the matching earlier source. B9 has its original single-row Configured surface / Physical surface / Tool face legend. The original dashed desired datum and difference arcs remain. Slide order, nine backups, all other slide contents and speaking material are unchanged. See ../experiments/media_update/committed_backup_figures_20260922.json. This supersedes the earlier source-only angular match and four-entry legend update.

2026-09-22: Real-time control (footer 7 / physical slide 8) uses Reference state, Pose and velocity errors, and Measured state as its signal labels. State: pose and velocity is defined once beneath the feedback line. The native diagram, matching PDF and standalone assets are synchronized. Equations, other slides, thesis and speaking material remain unchanged. See ../experiments/controller_feedback_diagram/verification_20260922.json.

2026-09-22: The former Motivation diagram is hidden backup B13, Sources of angular offset, at physical slide 39. Its four legend entries now clearly distinguish the configured surface, physical surface, dashed desired tool orientation and solid achieved tool orientation. The identical correction is in thesis Figure 1.1. Motivation retains its robot photograph. There are 26 main slides and thirteen hidden backups at 27–39. Existing slide content and speaking material are unchanged. See ../experiments/media_update/surface_entry_correction_20260922.json.

2026-09-21: Contact experiment (footer 10 / physical slide 11) again shows the shared surface/tool image on the left, with the unchanged contact settings on the right. The earlier Surface frame slide retains the same image and its definitions. All slide counts, notes, equations and backup pages remain unchanged. See ../experiments/media_update/contact_surface_copy_20260921.json.

2026-09-21: Plausibility experiment is physical slide 12 / footer 11, immediately before the normal-force and moment plausibility plots. Opposing moment is hidden backup B12 at physical slide 38. Both full recordings are embedded, upright and playable on click. Original sources and audio are preserved. There are now 26 main slides and twelve hidden backups, with Conclusion at 26 and B1–B12 at 27–38. The split demonstration 2 is at 20–21, Null-space experiment at 22, and the three main null-space plots at 23–25. These positions supersede earlier update records below. See ../experiments/media_update/contact_videos_20260921.json.

2026-09-21: Disturbance demonstration 2 is split at 00:23 across two consecutive main slides, physical slides 19 and 20, immediately before Null-space experiment at 21. Each part plays on click. Demonstration 1 remains in B2, centred at its existing size. The original recordings are retained. There are now 25 main slides and eleven hidden backups, with Conclusion at 25 and B1–B11 at 26–36. The main null-space plots are at 22–24. These positions supersede the earlier update records below. See ../experiments/media_update/nullspace2_split_20260921.json.

2026-09-21: Baseline angular error moved to hidden backup B11 at physical slide 34. Its chart, layout and notes are unchanged. Angular quantities remains B10 at physical slide 33. There are now 23 main slides and eleven hidden backups. See ../experiments/nullspace_narrative/baseline_to_backup_20260921.json.

2026-09-21: Angular quantities moved to hidden backup B10, now physical slide 33. Its diagram now matches the current thesis LaTeX source, including the frame inset and Latin Modern typography. The thesis PDFs contain older renderings and were not used to override the current source. Thesis files, speaking script and all slide notes remain unchanged. See ../experiments/angular_quantities_backup/README.md.

2026-09-21: Centre of compliance (CoC) now precedes Translation–rotation coupling, so the supporting/opposing moment illustration introduces the idea before the equations. Their new positions are footer 8 / physical slide 9 and footer 9 / physical slide 10 respectively. Both slide layouts and all speaking material are preserved. The native sections, Overview, equation catalog and full PDF reflect this order.

2026-09-21: Surface frame is a separate introduction after Cartesian pose (footer 4), before Cartesian impedance controller. It is footer 5 / physical slide 6. Contact experiment remains later at footer 10 / physical slide 11, with its process sequence and centred stiffness settings. The diagram and both native direction symbols were moved, preserving 29 active native equations. All existing speaking text and notes remain frozen. The new slide's notes are blank. This update supersedes historical narration-synchronization instructions below.

Thesis_Defense_gg0_v3.pptx contains 26 main slides and thirteen hidden backups.
Thesis_Defense_gg0_v3.pdf contains all 39 slides. Supplementary_slides.pdf contains all thirteen backups from physical pages 27–39.
Contact demonstration is visible at physical slide 3, immediately after Motivation, with no viewing-cue text beneath the video. Overview follows at physical slide 4.
The hidden backups begin with Null-space torques and projector (B1) and Disturbance demonstration (B2) at physical slides 27 and 28. B2 contains only demonstration 1. The seven complete six-setting result views follow as B3–B9, then Angular quantities as B10, Baseline angular error as B11, Opposing moment as B12 and Sources of angular offset as B13.
Native chapter sections, six-entry Overview, original theme and equations are retained. All six embedded video clips start on click.

The contact results use angular error relative to the calibrated surface normal.
The plotted quantity is the first-tangent component theta_err,t1. It comes from measured end-effector orientation and the calibrated tool normal.
The entry value is theta_meas,t1. The angular error replaces the former end-to-entry contact response.
Endpoint means and sample standard deviations use 93 terminal-report records at 0.01-degree precision over the main contact settings. The CoC comparison uses 78 of these reports and includes the completed +/-90 mm and +/-100 mm extension for both entry directions. The 24 extension trials were acquired on 2026-09-21 in a later session; all earlier points remain unchanged. See experiments/coc_extension/README.md.
The three representative full time histories retain model-estimated normal force and TCP moment.
Timing compares entry into and remaining within 0.1 degree of the angular error: approximately 2.5 s at +40 mm and 3.6 s at the TCP.
Calibration and mount uncertainty affects the estimate of physical alignment. A zero first-tangent component alone does not establish complete alignment.

Speaking/Thesis_Defense_Speaking_Script.tex and all existing PowerPoint notes are preserved unchanged. The speaking script has not been expanded for the new Surface frame slide.
Speaking/build.ps1 builds Thesis_Defense_Speaking_Script.pdf. No talk duration has been measured.
Speaker_notes_and_timing.txt now contains the same spoken points without obsolete timings.

Figure assets and editable sources are in figures_and_images. Provenance is in figures_and_images/manifest.json.
Reproducible data: MyOwn/code/python/figures/contact_angular_error/.
After editing slides, refresh Overview from native sections using Speaking/build/update-overview.ps1 or the portable equivalent. Preserve the frozen speaking script and notes unless the user requests changes. The full slide PDF includes all 39 slides.

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
less motion in both cases.

The hidden backups are:
B1 (27) Opposing moment
B2 (28) Null-space torques and projector
B3 (29) Cumulative joint motion: all settings
B4 (30) Jacobian conditioning: all settings
B5 (31) Joint motion: all individual trials
B6 (32) Angular quantities
B7 (33) Baseline angular error
B8 (34) Sources of angular offset

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

Original four-setting joint-motion sources remain available for provenance:
make_joint_motion.py and make_joint_motion_views.py.
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
