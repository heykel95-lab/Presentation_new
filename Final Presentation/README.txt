Thesis presentation, gg0 theme - September clarity revision

Active deck: Thesis_Defense_gg0_v3.pptx
Full PDF: Thesis_Defense_gg0_v3.pdf (24 main slides + 3 backups = 27 pages).
Supplementary_slides.pdf contains B1--B3. Backups stay hidden in the PowerPoint slideshow.
The original navy titles, continuous rule, white background, Arial body, and HM footer are preserved.

The single Overview lists six chapter names only. Native PowerPoint sections group the detailed slides within each chapter. Refresh it after slide edits with
Speaking\build\update-overview.ps1, then export the full presentation PDF.

Cartesian pose follows Overview, illustrating x, y, z and roll, pitch, yaw.
The subsequent controller introduction combines pose error and wrench, followed by the real-time loop, surface directions,
CoC geometry and moment interpretation followed by the coupling matrices, and null-space control. Both experiments precede the consistency checks.
Normal-force and moment plausibility precede commanded-versus-estimated wrench, then the baseline and parameter results.
The contact-results sequence is followed by all three thesis null-space panels: cumulative motion, conditioning/Cartesian retention, and net displacement,
then Conclusion with Future work underneath. The full contact response/force/moment figure is backup B1.
The former pose-representation and null-space-kinematics backups have been removed.
The videos are consecutive hidden backups: Contact demonstration (B2), then Disturbance demonstration (B3).
Both videos are embedded, start on click, and have visible viewing cues. PDF shows poster frames.

Speaking\Thesis_Defense_Speaking_Script.tex follows all 27 slides, with narration and equations only.
PowerPoint speaker notes follow the same text. Speaking\build.ps1 builds the speaking PDF directly
in Final Presentation; -Watch rebuilds after LaTeX edits. It does not rewrite text after slide changes.
Future editing agents must update the text and notes with each deck edit; see root AGENTS.md.

The earlier 18:10 rehearsal target predates this expanded sequence; the revised talk duration has not been measured.
Sources and figure provenance are recorded in figures_and_images\manifest.json and root AGENTS.md.
Angular quantities and the baseline plot use MyOwn main commit 0fea99b: measured angular offset theta_meas,t1,
contact-entry/contact-end orientation sketch, and baseline offsets 0.69, 9.31, -9.41 degrees.

Review corrections: measured angular-offset legends throughout; visible -0.006 degree net-displacement label; larger plot labels; separate tangential-translation parameter label; consistent blue subsection headings.

Conclusion combines five contact and null-space findings from the earlier presentation and thesis in the concise style of commit 558d22e. Future work covers a more rigid tool mount and adaptive CoC selection with return to the TCP after alignment. Audience-facing slide text and narration contain no semicolons.

Footer slide 19 shows contact response, estimated normal force, and estimated TCP moment together, using the original thesis curves and a shared legend. The matching LaTeX source and PDF/PNG/SVG figure variants are included.
