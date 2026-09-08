# Thesis and presentation workspace

## Repository locations

Verified on 2026-09-07.

| Repository | Local path | GitHub remote | Purpose |
| --- | --- | --- | --- |
| Presentation_new | `C:\Users\USER\Desktop\Presentation_new` | https://github.com/heykel95-lab/Presentation_new.git | Defense presentation and speaking script |
| MyOwn | `C:\Users\USER\Desktop\MyOwn` | https://github.com/heykel95-lab/MyOwn.git | The user's thesis LaTeX repository |
| Thesis_Final_Control | `C:\Users\USER\Desktop\Thesis_Final_Control` | https://github.com/heykel95-lab/Thesis_Final_Control.git | Final controller, experiments, analysis, and figures |

The thesis entry point is `C:\Users\USER\Desktop\MyOwn\Thesis.tex`; its compiled document is `C:\Users\USER\Desktop\MyOwn\Thesis.pdf`. Consult `chapters`, `figures`, and `code` for supporting material.

The control repository contains `surface_grinding_controller`, `experiments`, `analysis`, and `figures`. Use these sources when checking implementation details or experimental results. Read each repository's own instructions before making changes there.

## Active files and theme

- Edit `Final Presentation\Thesis_Defense_gg0_v3.pptx` and regenerate the matching PDF in that folder.
- Keep all final PDFs directly under `C:\Users\USER\Desktop\Presentation_new\Final Presentation`.
- Other folders (`Final`, `gg0`, `good1`, `good2`, `one`, `two`) are earlier versions, not the active deck.
- Preserve the existing dark blue `#17365D`, Arial body text, white background, continuous title rule, small HM logo, and footer. Use serif typography for mathematics.
- Use descriptive slide titles rather than questions. The measurement slide is titled `Angular quantities`.
- Use formal academic wording and actual experimental results, without invented numerical examples. Avoid "inferred" / "infered" and the adjective "signed" in audience-facing material. Preserve positive/negative angle conventions. Describe the angular quantities as calculated from measured end-effector orientation.
- Use rotations/rotation for the rotational compliance directions, as requested. Keep the title slide labelled Presentation and its date blue.

## Current structure and automatic Overview maintenance

The latest September 2026 review supersedes the earlier request to list every slide title. The Overview now has four broad sections:

1. Cartesian impedance and centre of compliance
2. Contact experiments and results
3. Null-space study
4. Conclusion and future work

Keep the numbers and text dark blue, with right-aligned numbers in a fixed-width column so their periods align. Exclude video titles, slide numbers, timings, and backup topics from the Overview. Run `Final Presentation\Speaking\build\update-overview.ps1` after each presentation edit. It reads actual visible slide order and derives section order at the Experimental procedure, Secondary study, and Conclusion boundaries. Review these boundaries if those titles change. This is an editing workflow, not a PowerPoint macro or watcher for manual deck edits.

The deck currently has **17 main slides and 6 hidden backups**, in this order:

1. Master Thesis Presentation
2. Motivation
3. Overview
4. Cartesian impedance wrench
5. Real-time control
6. Surface-relative compliance
7. Centre of compliance (CoC)
8. Experimental procedure
9. Angular quantities
10. Baseline contact response
11. Effect of stiffness
12. Effect of CoC position
13. Contact response and interaction moment
14. Contact demonstration
15. Secondary study: null-space motion
16. Disturbance demonstration
17. Conclusion
18. Commanded and estimated wrench (B1)
19. Normal-force plausibility assessment (B2)
20. Moment plausibility assessment (B3)
21. End-effector pose representation (B4)
22. Null-space kinematics (B5)
23. Contact response, normal force and moment (B6)

The full presentation PDF must include **all 23 slides**. Keep B1--B6 hidden in the PowerPoint slideshow. For PowerPoint SaveAs PDF, temporarily unhide them in memory, export, and close without saving the visibility changes to the PPTX. Regenerate `Supplementary_slides.pdf` from the six backup pages. Distinguish physical slide index from footer number: main footer numbers are one lower; backups use B1--B6.

Pose and wrench are combined in the main controller explanation. On the Cartesian impedance wrench slide (footer 3), use two balanced columns for position/force and orientation/moment, with a compact symbol key below. The user removed the small pose-frame illustration; do not restore it. Show measured/desired position and orientation, pose errors, and both spring-damper equations. The homogeneous transformation and SO(3) definitions belong in backup B4. Real-time control (footer 4) uses a concise four-step loop: Pose error, Wrench, Joint torques, Robot, with Measured pose on the feedback return. Keep the Cartesian mapping `F = [f; m]`, `tau_cart = J^T(q) F` prominent and the implementation in one short line (1 kHz control loop; C++ / libfranka). Keep detailed symbol definitions in the speaking text and notes; do not restore the former explanatory rows, long bullets, or complete torque command on that slide. C++/libfranka and the nominal 1 kHz loop are supported by MyOwn/chapters/03_software_implementation.tex.

The null-space introduction is combined with its results after the contact demonstration. Explain seven joints for six tool-pose degrees of freedom and coordinated joint motion. Do not call a particular seventh physical joint the null-space joint. Detailed rank, velocity, and torque decomposition equations belong in B5, retaining the full-rank qualification. Damping opposes redundant joint velocity; conditioning steers the configuration and can initiate motion. Do not describe conditioning as another damping term.

Conclusion has three brief Arial bullet points; Future work is beneath them on the same slide, with no second Conclusion title and no rule under Future work. Retain tilt-dependent CoC selection, return to the TCP after alignment, and direct angle measurement with sustained grinding. Do not restore Scope and next steps. The review proposes an 18:10 rehearsal target including videos; this is not a measured talk duration.

## Scientific figure and interpretation rules

Avoid duplicate axis glossaries around result figures, including backups. Retain short stiffness headings with physical directional descriptions and the `r_c,t2` CoC displacement definition. The user removed the `est: robot's model-based estimate` line from the contact-response and interaction-moment slide (footer 12); keep that explanation in the speaking text and notes. Preserve figure axes, legends, units, data, and uncertainty information.

Use achieved entry angles instead of commanded offsets. Baseline categories are Nominal zero offset, Positive tilt (+9.31 degrees), and Negative tilt (-9.41 degrees), with horizontal-axis title Entry condition. Responses remain -0.97, +7.57, -10.83 degrees. The nominal-zero total-mismatch magnitude `phi_0 = 0.74 degrees` is retained in speaker notes only; never relabel it as an achieved t1 component. Case-D CoC curves instead use +9.32 and -9.36 degrees. Sources: MyOwn/chapters/05_results_and_discussion.tex and backmatter/appendix_additional_plots.tex, Table D.1.

The angular sketch distinguishes achieved entry tilt from response relative to the held entry orientation. Gamma is calculated from end orientation back to entry; under that convention an aligning response has the same sign as entry tilt. Response magnitude is not an independent measurement of final physical alignment error.

On the CoC slide (footer 6), keep concise definitions and the commanded-moment equation across the top, the two sketches prominent below, and one short statement about moment reversal at the bottom. Describe CoC as a virtual reference point; do not restore the removed physical-hinge phrase. Both sketches must visibly show the surface-normal arrow `n_s`. Rasterize `CoC_moment.pdf` with `pdftocairo -png -singlefile -r 300` to preserve the thin arrow shafts. Label `m = m_R + r_c cross f` as commanded TCP moment. The shifted normal force adds a moment contribution; reversing displacement reverses that contribution. At the TCP, the additional contribution vanishes while rotational spring-damper torque remains active.

For the representative contact traces, the final-second estimated normal-force means are -82.9, -79.0, -78.0 N at CoC displacements -40 mm, TCP, +40 mm. Show rounded values -83, -79, -78 N on the main slide. Approximate steady-response times are 2.3 s and 3.6 s; retain the 1.3 s comparison as an observation from these traces. Force and moment are the robot's model-based estimates, not independent sensor measurements. Keep the full three-panel figure in B6. Source: MyOwn/chapters/05_results_and_discussion.tex, contact response and model-estimated interaction wrench discussion.

On the null-space study slide (footer 14), use one brief redundancy introduction and aligned Damping/Conditioning columns: graph and table, each followed by its result. Retain the position-error criterion at the bottom. For the null-space study, distinguish accumulated projected motion in the damping graph from mean net projected displacement in the table. Values in degrees are 7.517 (no null-space torque), 5.609 (damping), 0.015 (conditioning gain 1.5), -0.006 (conditioning gain 2). Each setting has three trials; graph shading is one sample standard deviation. Small net displacement can coexist with back-and-forth motion. Maximum measured TCP position error is 1.304 mm, below the 2 mm criterion. Sources: Thesis_Final_Control/experiments/derived/MAIN_NS_automatic_summary.csv, analysis/make_nullspace_figure.py, and MyOwn/chapters/05_results_and_discussion.tex.

Keep figure PDF/PNG/SVG variants synchronized with their LaTeX sources under `figures_and_images\sources`; record provenance in `figures_and_images\manifest.json`.

## Videos and narration

The videos remain embedded and start on click. Contact demonstration follows the contact results. Secondary study: null-space motion follows that video, then Disturbance demonstration, then Conclusion. Both videos are omitted from the Overview.

- Contact uses `Video\Contact.mp4` (approximately 51 seconds). Its visible cue is Pre-grinding hold / fixed desired orientation / CoC at TCP. Narration covers pickup, approach, contact, and manually changing the surface during the hold. Normal pressing remains active; do not claim precisely constant measured force from video. Surface contact moment drives adaptation while the rotational spring-damper remains active. The held reference is not a commanded alignment trajectory. Sources: MyOwn/chapters/03_software_implementation.tex, Pre-Grinding Hold, and chapters/02_theoretical_background.tex, moment decomposition.
- Disturbance uses `Video\Disturbance_trimmed.mp4` (approximately 66 seconds), with original 00:00--00:16 and 00:50--00:59 removed. The user-confirmed sequence and visible cue are no null-space torque, damping, conditioning. Do not invent numerical controller settings or phase timestamps for the video. Conditioning guides configuration and can generate motion.

Narration belongs in both the speaking PDF and PowerPoint notes and can accompany playback. PDF slides show static video poster frames.

## Speaking script and automatic PDF build

After **every slide change**, update `Final Presentation\Speaking\Thesis_Defense_Speaking_Script.tex` in the same task. Use the actual deck as source of truth for titles, order, visible content, notation, and transitions. Include all 23 slide sections, including both videos and six backups. Keep PowerPoint speaker notes synchronized too.

The speaking PDF contains only each slide's title, spoken text, and equations. Do not add timing, tables, cover/maps, slide-number labels, rehearsal cues, source appendices, headers, or footers. Let paragraphs and sections flow continuously without forced page breaks or blank paragraph spacing.

- Source: `Final Presentation\Speaking\Thesis_Defense_Speaking_Script.tex`.
- Build: `Final Presentation\Speaking\build.ps1`.
- Output: `Final Presentation\Thesis_Defense_Speaking_Script.pdf`.
- Logs/intermediate files: `Final Presentation\Speaking\build`.

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\USER\Desktop\Presentation_new\Final Presentation\Speaking\build.ps1"
```

Add `-Watch` to rebuild when the LaTeX source changes. Check `Speaking\build\watch.pid` and logs before starting another watcher. Do not assume the watcher survives a restart. The watcher **compiles LaTeX; it does not rewrite speaking text after PowerPoint edits**. The editing agent must do that synchronization, then build and visually verify the PDFs. MiKTeX/pdfLaTeX, latexmk, and Perl are available locally.
