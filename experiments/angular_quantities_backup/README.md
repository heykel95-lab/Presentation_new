# Angular quantities thesis match and backup move

Restoration on 2026-09-22: the author selected the last committed thesis figure
PDF as the appearance to retain, in the thesis and on current B6 / physical
slide 32. The committed PDF from `be7aa4d` has its blue error arc inside,
at radius 2.8. Its matching editable source is from `33b7dc5`. The later
source-only move to radius 6.3 was not reflected in the committed PDF.
The shared editable source now matches the selected PDF again. The inset
retains n_s leftwards and t_2 upwards. The active standalone wrapper uses
the committed PDF's Computer Modern 10 pt base, and the thesis figure
inherits the thesis document typography. See
../media_update/committed_backup_figures_20260922.json. This supersedes the
source-only matching policy described in the historical record below.

After the subsequent Baseline angular error move to B11, Angular quantities
remains B10 at physical slide 33. The current deck has 23 main slides and eleven
hidden backups. See ../nullspace_narrative/baseline_to_backup_20260921.json for
the current order. The figure and verification of its thesis match below remain valid.

On 2026-09-21, Angular quantities moved from physical slide 12 (footer 11,
formerly footer 10) to hidden backup B10 at physical slide 34. The deck now
has 24 main slides and ten hidden backups. The full PDF contains all 34 pages,
and Supplementary_slides.pdf contains pages 25–34.

The presentation figure differed from the thesis source in the frame inset:
the presentation showed n_s upwards and t_2 rightwards. The current thesis
source shows n_s leftwards and t_2 upwards. The exact current source is copied
from MyOwn-thesis/figures/ch04/surface_reference_geometry.tex to the
presentation's figures_and_images/sources/originals/ch04 directory. The wrapper
uses the thesis's 12 pt document base, T1 encoding and Latin Modern fonts.
No geometry or labels from that source are changed. The slide retains the
previous picture width and centre, with proportional scaling.

The available Thesis.pdf predates the current source and still shows the
older contact-response diagram. The standalone thesis figure PDF also predates
the current angular-arc placement. The current LaTeX source is the authority
for this update. All thesis files remain unchanged.

Rebuild from Final Presentation/figures_and_images/sources with pdflatex:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -output-directory /tmp/angular-build angular_quantities.tex
pdftocairo -png -singlefile -r 300 /tmp/angular-build/angular_quantities.pdf /tmp/angular-build/angular_quantities
pdftocairo -svg /tmp/angular-build/angular_quantities.pdf /tmp/angular-build/angular_quantities.svg
```

Create the output directory first. The figure's PNG is embedded in PowerPoint,
and its vector PDF is placed in the full and supplementary PDFs. Both PDFs keep
the existing exported slide furniture. This is not a fresh PowerPoint export.

Native sections and metadata follow the new order. Overview is refreshed from
the six main sections. All 29 native equations remain mapped to their actual
slide shapes. Notes and speaking files are preserved byte for byte.

Previous presentation figure assets and source are retained in
archive/20260921_before. Verification, source hashes and slide order are in
verification_20260921.json.
