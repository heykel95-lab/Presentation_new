# Final presentation: files, figures and automatic updates

The authoritative presentation is
[Thesis_Presentation_Final.pptx](two/Thesis_Presentation_Final_Package/Thesis_Presentation_Final/Thesis_Presentation_Final.pptx).
Its matching export is
[Thesis_Presentation_Final.pdf](two/Thesis_Presentation_Final_Package/Thesis_Presentation_Final/Thesis_Presentation_Final.pdf).
Both live in `two/Thesis_Presentation_Final_Package/Thesis_Presentation_Final/`.
The deck contains 17 slides, including the title slide. `good2.pptx`, `good1.pptx`
and the other variants are not the final presentation; do not select them by
filename ordering or modification time.

## Required automatic update workflow

Whenever the final presentation is changed, regenerate its matching PDF in the
same task, automatically and without waiting for a separate request. Whenever
a thesis figure used by the presentation changes, synchronise the figure asset,
the embedded PowerPoint picture and the PDF together. Updating a loose PNG alone
does not update a picture already embedded in PowerPoint.

Keep the existing `preview/Thesis_Presentation_Final.pdf` and
`preview2/Thesis_Presentation_Final.pdf` copies identical to the main export.
Check the affected slides in the rendered PDF before finishing. This workflow
is a standing instruction for every agent editing the presentation or its
shared thesis figures.

Export the saved PowerPoint with LibreOffice, using a temporary output directory,
then install the checked PDF beside the deck and in both preview directories:

```sh
libreoffice --headless --convert-to pdf --outdir /tmp/final-presentation-export \
  two/Thesis_Presentation_Final_Package/Thesis_Presentation_Final/Thesis_Presentation_Final.pptx
```

## Measured entry angle and contact response

Slide 8, **Contact sequence and experiment design** (displayed slide number 7),
uses the approved thesis Figure 4.2. Its source is
`MyOwn-thesis/figures/ch04/surface_reference_geometry.tex`.

- The configured reference is the horizontal red line.
- Contact entry is solid green and labelled `t_start`.
- Contact end is dashed blue and labelled `t_end`.
- The outer red arc is `theta_meas,t1`, from the configured reference to entry.
- The inner blue arc is `gamma_t1`, from contact end back to entry.
- Show only these two angle arcs. Do not restore the separate left-hand
  entry-to-end rotation arrow or the extra tool-normal arrows.

Both quantities use measured end-effector poses but compare different references.
The entry offset also uses the calibrated tool normal. The contact response
compares the end-effector orientations at entry and end; its direction is opposite
to the actual entry-to-end rotation.

The diagram is a schematic rotation about `t1`. In this planar case, the angle
between the plane traces equals the angle between their normals. The thesis
calculation remains the `t1` component of a three-dimensional rotation vector.
The configured reference is not an independently measured physical plate normal.

## Case-A baseline: thesis Figure 5.4

Slide 11, **Main results I — baseline and stiffness** (displayed slide number 10),
uses the exact current thesis Figure 5.4 from
`MyOwn-thesis/figures/ch05/results_case_a_bars.tex`.
Its horizontal axis is **Measured Angular Offset**, `theta_meas,t1 [degrees]`.

| Condition | Measured entry offset | Contact response |
|---|---:|---:|
| Nominal zero configured offset | 0.69° | −0.97° |
| Positive-offset condition | 9.31° | 7.57° |
| Negative-offset condition | −9.41° | −10.83° |

The first horizontal tick must be **0.69**, not `0`, `zero offset`, or the old
total-angle value `0.74`. The configured command is still zero; the measured
entry condition is 0.69°. This is the mean of 0.70°, 0.68° and 0.68° from
`P6_zero_p000/r01`–`r03`, using the negatives of `deviation_before_t1` in the
contact experiment archive. The bar height remains −0.97°.

## Consistent notation and source mapping

Use `theta_meas,t1` for the measured entry condition throughout the presentation.
Its name is **Measured Angular Offset**. Omit `Initial` in every heading,
axis, legend and sentence naming this quantity; its definition fixes contact entry.
Do not restore `theta_ach,t1`, `theta_init,t1`, `theta_0,t1`, or `phi_0` for that
condition. Keep `theta_offset,t1` for the configured pre-contact command and
`gamma_t1` for the contact response.

| Thesis source basename | Embedded image in `figures_and_images/` | Slide |
|---|---|---:|
| `surface_reference_geometry` | `fig_4_2_measured_angles.png` | 8 |
| `results_case_a_bars` | `fig_5_4_baseline.png` | 11 |
| `results_case_b_stiffness` | `fig_5_5_rotational_stiffness.png` | 11 |
| `results_case_c_stiffness` | `fig_5_6_translational_stiffness.png` | 11 |
| `results_case_d_panels` | `fig_5_7_coc_position.png` | 12 |

Slide numbers in this table count the title slide. The printed footer numbers
are one lower. The Case-B, Case-C and Case-D plots use the current thesis
figures with the same measured-angle notation.

## Editable assets and rendering

The final package's `figures_and_images/vector_pdf_sources/` directory contains
identical copies of the five thesis `.tex` sources, standalone rendering wrappers
and vector PDFs. Keep the thesis sources authoritative; copy changes from them
before rendering. Do not redraw or relabel the presentation plots independently.

Render with LaTeX, Latin Modern, TikZ and PGFPlots 1.18 or later. From the vector
source directory, for example:

```sh
pdflatex -halt-on-error -jobname=surface_reference_geometry render_surface_reference_geometry.tex
pdftoppm -r 300 -png -singlefile surface_reference_geometry.pdf ../fig_4_2_measured_angles
```

Use the table above for the other output names. Replace the actual embedded
PowerPoint image, preserve its aspect ratio, save the final deck and regenerate
all its PDF copies as part of the same update.
