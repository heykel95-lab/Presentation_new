# Parenthetical technical corrections in the speaking script

The user requested comments in parentheses directly inside the speaking text.
The original grammar-edited narration is retained. `annotations.json` supplies
short comments immediately after specific claims or at the end of their bullet.
“Correction” identifies an error, while “Suggested wording” qualifies a claim
that the evidence does not establish. Clarifications define the measured
quantity or experimental scope. These are review annotations for the presenter.

The comments appear in the speaking LaTeX/PDF, plain-text narration and native
PowerPoint speaker notes. The 34 visible slide pages, all 35 editable equations,
media, order and source/reference note blocks are unchanged. The existing
standalone display equations in the speaking script are preserved.

Evidence was checked against the local thesis chapters 02, 04 and 05, the
current plots and slide labels, `../coc_plot_check/verification.json`, and the
original source notes. The full sources are already listed in each slide's
technical reference block. This is a review of the supplied script against
the existing experiment records, not a new experiment.

`add_annotations.py` uses the ignored local `review/before.*` snapshot taken
after the grammar-only update. Do not rerun it over later changes without
updating the snapshot. It proves that removing the inserted comments restores
the complete previous speaking source and plain-text file exactly. All changes
inside the PowerPoint package are restricted to the affected note text nodes.
`verification.json` records preservation and build checks.

The grammar-only files under `../speaking_grammar/` are historical inputs.
Their builder predates these annotations and would remove them if rerun.
