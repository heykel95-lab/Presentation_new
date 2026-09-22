# Real-time control feedback diagram

The 2026-09-22 label update uses Reference state, Pose and velocity errors,
and Measured state. The controller input is one textbox, wrapped as Pose and /
velocity errors. State: pose and velocity is defined once below the left
feedback line. All blocks, parameters, summing junctions, connectors, native
equations and the 1 ms cycle statement retain their previous content and
placement. The right-side Measured robot state label and measured q branch
are retained.

`simplify_labels.py` stages this update from an explicit deck snapshot and the
regenerated DrawingML. It replaces four text shapes while preserving their
IDs, refreshes Overview from the native sections, and updates only the
corresponding PDF labels. `verification_20260922.json` records that the other
38 PDF pages are pixel-identical and all other objects on the affected slide
are unchanged. The deck has 26 main slides and thirteen hidden backups.
Speaker notes, speaking files, the supplementary PDF, equation catalog and
thesis remain unchanged.

The 2026-09-21 presentation update replaces the four unboxed stage labels with
an editable classical block diagram on Real-time control, footer 7 / physical
slide 8. It follows the rectangles, crossed summing circles, signs and signal
routing of thesis Figure 3.2, on physical page 57 of MyOwn-thesis/Thesis.pdf.

The main path is desired reference minus measured feedback, impedance
controller, Jacobian transpose, additive torque sum, then robot. K and D enter
the impedance block. Measured q enters the Jacobian operation. Model and
null-space torque contributions are represented by one additional input to the
positive torque sum. Their internal calculations remain outside this simplified
presentation diagram. The Cartesian torque symbol remains tau without a cart
subscript. The commanded output has the cmd subscript.

Both original native equations remain unchanged above the diagram. All diagram
objects are editable PowerPoint rectangles, circles, connectors and text. The
existing 1 ms cycle line, theme, header, footer, notes and speaking files are
preserved. The thesis is unchanged. At the time of that initial update, the
deck had 25 main slides plus nine hidden backups, and the full PDF had 34 pages.

The generator and its PDF, SVG and DrawingML outputs share one scene:

```sh
python "Final Presentation/figures_and_images/sources/make_controller_feedback_diagram.py"
pdftoppm -r 180 -singlefile -png \
  "Final Presentation/figures_and_images/controller_feedback_diagram.pdf" \
  "Final Presentation/figures_and_images/controller_feedback_diagram"
```

The generator requires PyMuPDF, lxml, an Arial font file, and the current deck
PDF as a source of its embedded Cambria Math glyphs. Use `--arial` and
`--pdf-source` to override those inputs. It generates the standalone diagram
and editable DrawingML without overwriting the deck or notes. Its DrawingML
coordinates are slide coordinates in points converted to EMUs.

The full slide PDF preserves the two equation vector regions, redraws the
diagram from the same scene, and retains all other pages. Verification is in
`verification_20260921.json`: all other 33 pages are pixel-identical, the native
equations are unchanged, and all original notes, media, speaking files and
supplementary pages are preserved.
