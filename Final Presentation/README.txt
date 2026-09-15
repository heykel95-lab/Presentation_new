Active defense presentation

Thesis_Defense_gg0_v3.pptx contains 26 main slides and two hidden backups.
Thesis_Defense_gg0_v3.pdf contains all 28 slides. Supplementary_slides.pdf contains the two backups from physical pages 27 and 28.
Contact demonstration is visible at physical slide 3, immediately after Motivation, with no viewing-cue text beneath the video. Overview follows at physical slide 4.
Null-space torques and projector (B1) and Disturbance demonstration (B2) remain hidden at physical slides 27 and 28.
Native chapter sections, six-entry Overview, original theme, equations and embedded videos are retained. Both videos start on click.

The contact results use angular error relative to the calibrated surface normal.
The plotted quantity is the first-tangent component theta_err,t1. It comes from measured end-effector orientation and the calibrated tool normal.
The entry value is theta_meas,t1. The angular error replaces the former end-to-entry contact response.
Endpoint means and sample standard deviations use all 69 original terminal-report records at 0.01-degree precision. The CoC comparison includes the completed -80 mm and +80 mm conditions for both entry directions.
The three representative full time histories retain model-estimated normal force and TCP moment.
Timing compares entry into and remaining within 0.1 degree of the angular error: approximately 2.5 s at +40 mm and 3.6 s at the TCP.
Calibration and mount uncertainty affects the estimate of physical alignment. A zero first-tangent component alone does not establish complete alignment.

Speaking/Thesis_Defense_Speaking_Script.tex and PowerPoint notes are synchronized with all 28 slides.
Speaking/build.ps1 builds Thesis_Defense_Speaking_Script.pdf. No talk duration has been measured.
Speaker_notes_and_timing.txt now contains the same spoken points without obsolete timings.

Figure assets and editable sources are in figures_and_images. Provenance is in figures_and_images/manifest.json.
Reproducible data: MyOwn/code/python/figures/contact_angular_error/.
After editing slides, run Speaking/build/update-overview.ps1, rebuild the speaking script and export all 28 PDF pages.

Equations (2026-09-15)
All 37 standalone formula and symbol pictures have been replaced with native editable PowerPoint equations from their existing LaTeX sources. Direct conversion succeeded, so IguanaTex is not required.
Click inside a formula to edit it using PowerPoint Equation tools. The LaTeX sources remain in figures_and_images/sources. native_equations.json maps each equation to its slide, shape name and exact LaTeX. Each equation also has the source in its alternative text.
Keep formula changes synchronized between the LaTeX source, native PowerPoint equation, source catalog, speaking script and notes. Editing a .tex file alone does not automatically update the PowerPoint equation. Graphs and schematic illustrations retain their editable figure sources.

Controller error sketches (2026-09-15): position error and axis-angle correction are illustrated separately. The rotational equation is e_R = phi u. The rotation-matrix identity was removed. Both new images and their LaTeX/PDF/PNG/SVG sources are in figures_and_images.

Review update: the separate null-space theory, experiment and five result slides follow all contact results. Displayed numbers use at most two decimal places or scientific notation. The shared surface-frame sketch includes the tool.

The reviewed PDF was exported directly from PowerPoint. The full PDF includes both hidden backups.
Null-space label formatting is reproducible with figures_and_images/sources/format_nullspace_for_presentation.py using the thesis analysis and archived results.

Directional motion history: Null-space displacement over time is footer 21, immediately after the cumulative plot at footer 20. The four-setting plot and enlarged conditioning view retain movement direction and use the same reference axis as the net-displacement bars. Rebuild with figures_and_images/sources/make_nullspace_displacement.py. Its portable recorded-sample archive, source hashes and numerical checks are stored beside the generator.

Joint motion over time is footer 22, immediately after the directional projected-displacement history. The same measured joint-1 figure is used in the thesis. All three trials of each setting are shown, with a first-second conditioning close-up. Rebuild with figures_and_images/sources/make_joint_motion.py. Portable 20 Hz samples, source hashes and validation are stored beside it.
