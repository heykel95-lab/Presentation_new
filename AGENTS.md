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

## Active presentation and output location

Use "calculated from measured end-effector orientation" for the angular quantities. Avoid "inferred" (including the misspelling "infered") in the presentation and speaking text.

On results slides, keep axis labels and symbol definitions inside the figures; do not add separate duplicate symbol/explanation rows above or beside them (for example, t, M_t1,est, E_N, stiffness symbols, or CoC position). Preserve the scientific plots, their legends, and the result takeaway text. The speaking script may still explain the plotted quantities verbally.

Use achieved entry angles rather than commanded offsets in the presentation and speaking script. The Angular quantities slide explains achieved angle and contact response only. The baseline figure on the Baseline contact response slide uses the MyOwn thesis Case-A values: phi_0 = 0.74 degrees (total angular-mismatch magnitude), theta_ach,t1 = +9.31 degrees and -9.41 degrees (signed achieved components); corresponding responses remain -0.97, +7.57 and -10.83 degrees. Never relabel phi_0 as a signed t1 component. Sources: MyOwn/chapters/05_results_and_discussion.tex and backmatter/appendix_additional_plots.tex, Table D.1. Do not substitute the different Case-D angles (+9.32/-9.36) into this baseline figure.

- Work on `Final Presentation\Thesis_Defense_gg0_v3.pptx` unless the user selects another deck.
- Keep the matching presentation PDF at `Final Presentation\Thesis_Defense_gg0_v3.pdf`.
- The `Final`, `gg0`, `good1`, `good2`, `one`, and `two` folders contain other versions; do not confuse them with the active final deck.
- Save final deliverables directly in `C:\Users\USER\Desktop\Presentation_new\Final Presentation`.

## Automatically keep the presentation Overview synchronized

As part of every presentation edit, update the Overview without requiring a separate user request:

1. Locate the slide titled `Overview` (currently slide 3).
2. Read the actual slide titles from every subsequent visible slide, in deck order, excluding video demonstration slides. The user explicitly does not want the videos mentioned in the Overview. Include all other main presentation slides through Conclusion. Hidden supplementary slides are outside the main agenda; include them if they become visible.
3. Replace the Overview list with those exact titles. Recalculate it after adding, deleting, renaming, hiding, unhiding, or reordering slides; do not maintain a separate hard-coded title list.
4. Display a numbered list of titles, starting at 1 and following agenda order. Right-align the numbers in a fixed-width column so the periods align vertically, including for two-digit numbers; align all titles at a common left edge. Use numbers instead of dot bullets. Do not add slide/footer numbers, durations, cumulative times, or other metadata.
5. Use the presentation's existing dark blue, `#17365D`, for both list numbers and title text. Preserve the deck's Arial typography, heading, full-width rule, logo, and footer styling.
6. Check the rendered Overview for clipping, wrapping, and overlap. Adjust its layout as needed to accommodate all titles clearly.
7. Save the updated PowerPoint and regenerate its matching PDF in `Final Presentation`. The presentation PDF must include all 21 slides: 18 main slides (including two videos omitted from the Overview) plus 3 backup slides. Keep the backups hidden in the PowerPoint slideshow, but include them when exporting the PDF. For PowerPoint SaveAs PDF, temporarily unhide them in memory and close without saving those visibility changes to the PPTX. The separate `Supplementary_slides.pdf` may also be retained.

The separate `Scope and next steps` slide has been removed. Keep its next steps in the `Future work` section below the Conclusion section on the same slide; both sections use bullet points: independent tool-angle measurement, selecting the CoC from entry tilt, returning it to the TCP after alignment, and testing sustained grinding. The former 17:45 main-talk estimate predates the new Null-space control introduction and excludes video playback; re-time the talk before quoting an updated total.

This rule concerns the presentation Overview, not the Overview page or timing table in the speaking script. Do not apply presentation-only formatting requests to the speaking script.

This file instructs future editing agents to perform the synchronization as part of their work. It is not a PowerPoint macro or a background watcher for manual PowerPoint edits. Run `Speaking\build\update-overview.ps1` to refresh the numbered agenda from the actual subsequent visible slide titles, then export the presentation PDF and inspect the result.

## Speaking script and automatic PDF build

Two video slides are embedded in the presentation: `Disturbance demonstration` uses `Video\Disturbance_trimmed.mp4` (original 00:00--00:16 and 00:50--00:59 removed), and `Contact demonstration` uses `Video\Contact.mp4`. Place both video slides immediately before Conclusion, in this order: Contact demonstration, Disturbance demonstration, Conclusion. Keep them out of the Overview. The user explicitly deferred writing their speaking text; do not invent video scripts until requested. Existing script sections still follow the order of the non-video slides. The videos add approximately 1:57 if played in full; the earlier 17:45 talk estimate excludes them.

Keep the speaking PDF simple: only each slide's name, its spoken text, and its equations. Include the backup slide scripts in deck order. Do not add a cover/map, timing, tables, slide-number labels, rehearsal cues, source guides, headers, footers, or a separate symbol-pronunciation appendix. Keep transition sentences as ordinary spoken text. Let slide sections flow continuously, without forced page breaks or extra blank space between paragraphs; retain modest spacing around slide headings and equations.

After every slide change, check and update `Final Presentation\Speaking\Thesis_Defense_Speaking_Script.tex` as part of the same task, without waiting for a separate request. Use the current PowerPoint as the source of truth for slide titles, order, visible content, terminology, equations, and the order of explanations. Add or remove script sections when slides are added or removed, and adjust transitions and references to slide layout when needed. Preserve correct scientific qualifications and equations. Rebuild and verify `Final Presentation\Thesis_Defense_Speaking_Script.pdf` before delivering the presentation changes. The LaTeX watcher only compiles changes to the `.tex` file; it does not rewrite the speaking text when the PowerPoint changes.

Distinguish the physical slide index from its printed footer number when resolving requests. For example, `Surface-relative compliance` is currently physical slide 6 with footer 5; the user originally referred to it as footer 4 before the torque slide was added. Use rotations/rotation instead of tilting/turning when describing the rotational compliance directions there.

- LaTeX source: `Final Presentation\Speaking\Thesis_Defense_Speaking_Script.tex`.
- Build script: `Final Presentation\Speaking\build.ps1`.
- PDF output: `Final Presentation\Thesis_Defense_Speaking_Script.pdf`.
- Compiler diagnostics and intermediate files: `Final Presentation\Speaking\build`.
- Run a build from any directory with:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\USER\Desktop\Presentation_new\Final Presentation\Speaking\build.ps1"
```

- Add `-Watch` to rebuild whenever the LaTeX source changes. A watcher was started during this session; do not assume it survives a restart. Check `Speaking\build\watch.pid` and the watcher logs before starting a duplicate process.
- The speaking build uses MiKTeX/pdfLaTeX and latexmk with Perl. It automatically performs the necessary compilation passes and keeps the final PDF directly in `Final Presentation`.

The introductory Null-space control slide appears immediately before Experimental procedure. Explain redundancy, projected torques, damping, and configuration conditioning before describing the studies; keep the detailed null-space results later in the deck.

The null-space introduction uses dim(ker J) = 7 - rank(J) = 1 at rank 6 and J(q) qdot_null = 0, with J of size 6 by 7. Explain 3 position plus 3 orientation degrees of freedom and one redundant instantaneous motion direction. Do not describe a particular seventh physical joint as the null-space joint: the motion generally coordinates several joints. Preserve the full-rank qualification and the distinction between instantaneous kinematics and measured pose retention.

The null-space introduction also shows tau_null = tau_d + tau_sigma and explains the two projected joint-torque contributions. Damping torque counters null-space joint motion; conditioning torque steers towards a configuration with better motion capability and can initiate motion at rest. Do not describe both terms as opposing or cancelling motion. Source: MyOwn/chapters/02_theoretical_background.tex, Projected Damping and Conditioning and Complete Null-Space Torque.

Cartesian impedance torque follows Cartesian impedance. It shows only F = [f; m] and tau_cart = J^T F. The user removed the complete torque command and its null-space/model-term explanations from this slide; keep those out of its speaking section as well. The earlier talk-duration estimate also excludes this additional slide.
