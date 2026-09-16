# Uniform presentation equations

The 2026-09-16 update gives all 35 standalone equations and mathematical symbol
keys the same base style: **22 pt Cambria Math, regular weight, black**. This
includes the main controller wrench, the shifted wrench and the backup formulas.
Normal italic variables, upright units and subscript/superscript scaling remain.

The active presentation still contains native editable Office Math structures.
No formula pictures replace them. Run and control properties specify the same
font, size and weight, with AutoFit disabled. The eight bold matrix-zero runs
are regular. Related equation groups align at their equals signs. Surface-normal
and tangent symbol rows, including captions, move up 6 pt for footer clearance.

The equation sources, `native_equations.json`, alternative text, asset manifest,
PDF/PNG/SVG equation assets, slide notes and speaking source are synchronized.
Spoken content, scientific formulas, data, slide order and all media are unchanged.
The full PDF contains 34 pages and the supplementary PDF contains nine backups.

## Reproduction

`standardize_equations.py` starts from the local ignored `review/` snapshot:
`before.pptx`, `before.pdf`, `before_equations.json` and `before_script.tex`.
That snapshot includes the new title photo, thesis Figure 1.1 and both null-space
videos. Do not run this or an older media/narrative builder over later edits
without rebasing its snapshot. The script preserves original equation sources
in `review/sources/` before rewriting their font wrappers.

Run from the repository root with Python containing PyMuPDF and lxml:

```bash
/tmp/hmode-python/bin/python experiments/equation_style/standardize_equations.py
/tmp/hmode-python/bin/python experiments/equation_style/validate_equations.py
```

The source wrappers now use `unicode-math` and explicitly select Cambria Math
at 22 pt. To compile them independently, use LuaLaTeX on a machine where
Cambria Math is installed. That font is not installed in this Linux environment,
so these wrappers were not locally compiled. Instead, the matching assets and
slide PDF preserve the original PowerPoint export's native Cambria Math vector
glyphs and mathematical paths, scaled to the requested base size. Bold zeros
are replaced using the regular zero from the PDF's embedded Cambria Math font.
The active PowerPoint is edited directly as OOXML, without a LibreOffice or
python-pptx save round trip.

Rebuild the speaking PDF after updating the source. On this Linux workstation:

```bash
pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory='Final Presentation/Speaking/build' \
  'Final Presentation/Speaking/Thesis_Defense_Speaking_Script.tex'
```

Copy the built PDF to both speaking PDFs in `Final Presentation`.

## Verification

`update.json` records old/new sizes and geometry. `verification.json` records:

- All 35 native equation shapes use 22 pt regular black Cambria Math.
- Mathematical tokens and structures are unchanged, including matrices,
  fractions, accents, limits and operators.
- All package relationships resolve. Sections, order and 25 visible / nine
  hidden slides are preserved.
- Every media payload and playback relationship is byte-identical, including
  the three embedded videos, title photo and thesis figure.
- All 22 unaffected PDF pages are pixel-identical. On the 12 changed pages,
  differences are confined to equation and moved-caption regions.
- Headers and footers are pixel-identical on all pages. The nine supplementary
  pages match the corresponding full-deck pages.
- Equation sources and assets exist, and spoken content remains unchanged.

The 12 affected pages were visually reviewed, including both wrench matrices,
contact symbols, plausibility equations and the backup torque formulas.
