# Requested presentation media changes

## Surface-entry diagram in B13 and thesis, 2026-09-22

The former Motivation diagram is added as hidden B13, Sources of angular
offset, at physical slide 39. Motivation retains the robot photograph.
The corrected diagram explicitly identifies all four elements in a two-row
legend: configured surface (solid red), physical surface (solid blue), desired
tool orientation (dashed black), and achieved tool orientation (solid green).
The existing desired reference was already dashed but had no legend entry.
The original object geometry, tool tip, schematic tilts and difference arcs
are unchanged.

The correction is shared with thesis Figure 1.1. The identical TikZ sources
are `MyOwn-thesis/figures/ch01/surface_entry_concept.tex` and
`figures_and_images/sources/thesis_figure_1_1_source.tex`. Matching PDF/PNG/SVG
assets are generated with 12 pt document defaults and Latin Modern fonts.
Use `sources/render_thesis_figure_1_1.tex` to compile the presentation asset
from its source directory, then render the PDF with Poppler. The thesis also
includes a standalone wrapper beside its source. The original presentation
figure and provenance remain under `../surface_entry_correction/archive/`.

`add_surface_entry_backup.py` appends B13 from an explicit 38-slide snapshot
and prepared figure assets. It stages outputs without overwriting the active
deck. The presentation now has 26 main slides and thirteen hidden backups.
Its full PDF has 39 pages and the supplementary PDF thirteen. All existing
slides, notes, media, equations and speaking files are unchanged. The backup
has blank notes. The new page contains the vector figure; existing PDF pages
are retained from the PowerPoint export.

`surface_entry_correction_20260922.json` records the synchronized source and
asset hashes, clean thesis compilation, visual review, and preservation checks.
The thesis remains 122 pages and its prose and other figure sources are unchanged.

## Surface diagram repeated on Contact experiment, 2026-09-21

The user requested the surface image on Contact experiment as well as on the
earlier Surface frame introduction. Footer 10 / physical slide 11 now shows
the identical embedded `surface_directions.png` on the left at 360 pt width.
The nine existing settings headings, labels and native equations move 220 pt
to the right, retaining their contents, typography and relative alignment.
The process sequence and earlier Surface frame slide are unchanged. No symbol
glossary was duplicated. All notes, media, source assets, slide numbering,
equation catalog and supplementary pages remain unchanged.

`restore_contact_surface.py` stages this single-slide edit from an explicit
pre-edit snapshot. `contact_surface_copy_20260921.json` records image identity,
native XML preservation, exact PDF translation of the settings, and the other
37 PDF pages remaining pixel-identical. The full PDF retains its existing
PowerPoint-exported content and composes only this changed region.

## Plausibility and opposing-moment videos, 2026-09-21

Plausibility experiment is a visible main slide at physical slide 12 / footer 11,
immediately before the Normal-force and Moment plausibility assessment plots.
It follows Contact experiment within the Contact experiments section.
Opposing moment is hidden backup B12 at physical slide 38. Both videos play
on click and use centred, uncropped 420 pt square frames with their first video
frame as the PDF poster. No numerical settings are assigned to the recordings.

The original `Video/Plausibility Experiment.mp4` and `Video/Opposing Moment.mp4`
remain unchanged. Both have 90-degree rotation metadata. The presentation
copies `Plausibility_experiment_presentation.mp4` and
`Opposing_moment_presentation.mp4` render that rotation into upright pixels,
using H.264, CRF 18, medium preset, yuv420p, `-vsync 0`, 90000 video timescale,
and `-movflags +faststart`. AAC audio is copied without re-encoding. All 419
and 311 original video frames are preserved, as are the complete durations.

There are now 26 main slides and twelve hidden backups at 27–38. The full PDF
contains all 38 slides and the supplementary PDF all twelve backups. Earlier
slide content, embedded media, speaker notes and speaking files are unchanged.
The new slides have blank notes. These counts supersede earlier records below.

`add_contact_videos.py` stages the deck and PDF changes from a supplied
36-slide `before_*` snapshot and prepared clips/posters. It does not overwrite
the active deck and must be adapted before applying it to later slide orders.
Existing PowerPoint-exported PDF pages are preserved, with the two new poster
pages composed and affected main footers updated. This is not a fresh
PowerPoint PDF export. `contact_videos_20260921.json` records source/output
hashes, full decoding, frame counts, identical compressed audio, upright
orientation, preserved notes/media/equations, and PDF comparisons.

## Demonstration 2 split and main-slide placement, 2026-09-21

The recording labelled Null-space demonstration 2 has moved from B2 into two
consecutive main slides immediately before Null-space experiment. Physical
slides 19 and 20 show 00:00–00:23 and 00:23–end. Each embedded clip starts on
click, retains the upright square framing and has its own first-frame poster.
Demonstration 1 remains in B2 (physical slide 27), centred at its original size.
No controller settings have been assigned to these qualitative recordings.

The main sequence is Null-space controller (18), the two demonstration parts
(19–20), Null-space experiment (21), the three main result plots (22–24), and
Conclusion (25). There are 25 main slides and eleven hidden backups. The full
PDF contains all 36 slides and the supplementary PDF all eleven backups.
Existing speaker notes and speaking files are byte-identical. The two new
slides have empty notes. These counts supersede historical records below.

The original `Nullspace2.mp4`, upright `Nullspace2_presentation.mp4`, and their
source posters remain available. The two new clips in `Final Presentation/Video`
contain 690 and 238 frames at 30 fps, totalling all 928 source frames. Part 2
starts at original frame 690, exactly 23.000 s. The video durations are 23.000 s
and 7.933 s. AAC encoder priming can make container durations slightly longer.
Both clips fully decode, have H.264 video with yuv420p pixels and AAC audio,
and preserve the original audio content through re-encoding at the cut.

Prepare the split using FFmpeg's `split` and `asplit` filters, followed by
`trim=end=23` / `trim=start=23` and `atrim=end=23` / `atrim=start=23`, then
reset timestamps with `setpts=PTS-STARTPTS` and `asetpts=PTS-STARTPTS`.
Each output uses `-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p
-vsync 0 -video_track_timescale 90000 -c:a aac -b:a 256k -metadata:s:v:0
rotate=0 -movflags +faststart`. The clips are named
`Nullspace2_part1_0000-0023.mp4` and `Nullspace2_part2_0023-end.mp4`.
Their matching `_poster.png` files are each clip's first decoded frame.

`split_nullspace2.py` builds the deck and PDFs from an explicitly supplied
pre-edit snapshot directory. It stages outputs and does not overwrite the
active deck. The snapshot must contain `before_Thesis_Defense_gg0_v3.pptx`,
`before_Thesis_Defense_gg0_v3.pdf`, `before_native_equations.json`, and the two
prepared clips/posters. Do not run it against a later deck without adapting
its placement assertions. The PDF preserves original PowerPoint pages and
updates the three video compositions and affected footers. It is not a fresh
PowerPoint export.

`nullspace2_split_20260921.json` records the resulting order, file hashes,
decoding and cut-boundary checks, preserved notes and other media, unchanged
scientific slide content, all 29 native equations, and PDF comparisons.

## Earlier media changes

On 2026-09-21, the user moved the full `title_robot.jpg` photograph from the
title slide to Motivation, replacing thesis Figure 1.1. The photo is on the
right, with the unchanged Problem and Idea text stacked on the left. Its
original bytes and aspect ratio are preserved. The title slide retains its
text and logos. The figure assets remain archived. The 33-page PDF matches
these two slide changes, and all other pages, notes, speaking files and the
supplementary PDF are unchanged. See `motivation_photo_move_20260921.json`.
This placement supersedes the historical media layout described below.

The user requested these changes on 2026-09-16:

- The supplied robot photo on the right of the title slide.
- Thesis Figure 1.1 replacing the image on slide numbered 1, Motivation.
- Both Nullspace1 and Nullspace2 replacing the existing disturbance video.

The presentation still has 25 main slides and nine hidden backups. B2 contains
the two videos side by side, each starting independently on click. The original
contact video is unchanged. The former disturbance video is no longer embedded.

`figures_and_images/title_robot.jpg` preserves the original attachment bytes
from `20260916_150937.jpg`, including its full 2858 × 2908 image. The photograph
is displayed without cropping or distortion.

`figures_and_images/thesis_figure_1_1.pdf` is the exact vector figure extracted
from MyOwn-thesis/Thesis.pdf, physical page 27 / printed page 1. Its title is
“Sources of angular offset at surface entry.” The PNG and SVG match that PDF.
The original TikZ source is copied to sources/thesis_figure_1_1_source.tex.
Source hashes and the PDF extraction rectangle are recorded in sources.json.
The figure is above the unchanged Problem and Idea text for readability.

The original videos remain at `Final Presentation/Video/Nullspace1.mp4` and
`Nullspace2.mp4`. They carry a 90-degree rotation flag. The presentation copies
normalize that rotation into upright frames using H.264, retain every frame,
and copy the original AAC audio without re-encoding. No interval was trimmed.
The neutral labels do not assign unverified controller settings to either clip.

The video preparation used this command for each input, with the corresponding
output basename:

```sh
ffmpeg -i Nullspace1.mp4 -map 0:v:0 -map '0:a?' -c:v libx264 \
  -preset medium -crf 18 -pix_fmt yuv420p -vsync 0 \
  -video_track_timescale 90000 -c:a copy -metadata:s:v:0 rotate=0 \
  -movflags +faststart Nullspace1_presentation.mp4
ffmpeg -i Nullspace1_presentation.mp4 -frames:v 1 Nullspace1_poster.png
```

`update_media.py` edits selected PowerPoint XML parts directly, preserving
editable equations and the existing slide order. It requires the local
pre-edit deck, PDF and speaking script in ignored `review/`. Do not run it over
later edits without updating its snapshot. The matching PDF retains original
pages and inserts the photo, vector thesis figure and video poster frames.
It is not a fresh PowerPoint export. PowerPoint contains the playable videos.

Run the update and validation from the repository root with python-pptx,
PyMuPDF, lxml and imageio-ffmpeg available:

```sh
python experiments/media_update/update_media.py
python experiments/media_update/validate_media.py
```

Rebuild the speaking LaTeX using the existing Speaking/build.ps1 on Windows
or pdflatex on Linux. Keep the two final speaking PDFs directly under
Final Presentation. The PowerPoint notes and script now explain both angular
offsets in Figure 1.1 and describe the new recordings without the old video's
phase-sequence claims.

Validation checks every internal media relationship, both click triggers,
video frame counts, upright orientation, identical compressed audio payloads,
and full decoding of both presentation clips. It also verifies preserved
equations, unrelated slide XML, unchanged PDF pages, all nine supplementary
pages and speaking-script order. Results are in verification.json. Earlier
nullspace_narrative validation records describe the preceding deck version.
# Backup demonstration removal, 2026-09-22

The former hidden B2 / physical slide 28 is removed. Its original slide, notes,
video and required dependencies are preserved in
`archive/removed_backup_demo_20260922.pptx`, with a matching archive PDF.
The source recordings remain unchanged.

The main clips stay at physical slides 20–21. Their captions are now
Demonstration · Part 1 and Demonstration · Part 2. The recording identifier 2
and time ranges are removed from the visible captions. Both clips retain their
exact 00:23 split, full frames, audio, posters and click-to-play behaviour.

The active deck and full PDF contain 34 slides: 26 main slides and eight hidden
backups. The supplementary PDF has eight pages. The restored angular figure
and surface-entry figure are unchanged, now numbered B5 and B8. Remaining
notes, all speaking files and 29 native equations are unchanged.
`remove_backup_demo.py` stages and verifies the edit. See
`backup_demo_removed_20260922.json` for the current order and preservation checks.
# Opposing moment first, 2026-09-22

Opposing moment is now B1 / physical slide 27. It remains hidden, with the
same full video, audio, poster, dimensions and click-to-play behaviour. The
other backups retain their relative order, placing torque equations at B2,
cumulative motion at B3, conditioning at B4, individual trials at B5, angular
quantities at B6, baseline angular error at B7 and sources of angular offset
at B8. No content changes accompany this move.

`opposing_moment_first.py` stages the reorder, footers, native sections,
Overview refresh, equation-catalog indices and full/supplementary PDFs.
`opposing_moment_first_20260922.json` records that all page contents are
pixel-identical apart from footer labels. The deck remains 26 main slides
plus eight hidden backups. Notes, speaking files and figure assets are unchanged.
