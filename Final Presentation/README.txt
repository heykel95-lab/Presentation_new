Thesis presentation, gg0 theme - September clarity revision

Active deck: Thesis_Defense_gg0_v3.pptx
Full PDF: Thesis_Defense_gg0_v3.pdf (17 main slides + 6 backups = 23 pages).
Supplementary_slides.pdf contains B1--B6. Backups stay hidden in the PowerPoint slideshow.
The original navy titles, continuous rule, white background, Arial body, and HM footer are preserved.

The Overview lists every subsequent slide title through Conclusion, excluding videos. Refresh it after slide edits with
Speaking\build\update-overview.ps1, then export the full presentation PDF.

The main controller introduction combines pose and wrench, followed by Real-time control.
Detailed pose and null-space mathematics and the full contact response/force/moment figure are in backups.
The contact-results sequence is followed by Contact demonstration, the combined null-space study,
Disturbance demonstration, then Conclusion with Future work underneath.
Both videos are embedded, start on click, and have visible viewing cues. PDF shows poster frames.

Speaking\Thesis_Defense_Speaking_Script.tex follows all 23 slides, with narration and equations only.
PowerPoint speaker notes follow the same text. Speaking\build.ps1 builds the speaking PDF directly
in Final Presentation; -Watch rebuilds after LaTeX edits. It does not rewrite text after slide changes.
Future editing agents must update the text and notes with each deck edit; see root AGENTS.md.

The review's 18:10 target includes both videos (51 s and 66 s); confirm the duration by rehearsal.
Sources and figure provenance are recorded in figures_and_images\manifest.json and root AGENTS.md.
