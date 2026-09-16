# User narration: grammar-only edit

On 2026-09-16 the user supplied replacement speaking text and explicitly asked
to correct grammar while keeping everything else the same. The corrected text
is in `corrected_narration.json`, organized under the existing slide titles.
Spelling, punctuation, sentence boundaries and obvious wording slips were
corrected. In the motivation, “can achieve perfect alignment” was interpreted
as “cannot” because the user describes friction as the second alignment problem.
The unfinished baseline sentence was completed by stating the three starting
orientations without adding result values.

The 22 matching sections were replaced in the speaking LaTeX source, plain-text
narration and PowerPoint notes. The 12 sections not supplied by the user retain
their previous text. Existing displayed equations, slide order, every visible
slide, images, videos and equation styles were preserved. Both final speaking
PDFs were rebuilt with pdfLaTeX. The visible-slide PDF did not need regeneration
because no visible slide changed.

Scientific claims were retained as requested. `technical_review.md` separately
identifies statements that conflict with the plots or overstate their evidence.
Those review notes are not part of the speaking PDF or slide narration.

`update_speaking.py` uses the ignored local `review/before.*` snapshot. Do not
rerun it after further edits without updating that snapshot. It changes only
the affected speaker-note XML parts inside the PowerPoint package, preserving
the original source and technical-reference paragraphs. `verification.json`
records the package, narration and PDF checks. All eight PDF pages were visually
reviewed, and the LaTeX build produced no warnings or overfull boxes.
