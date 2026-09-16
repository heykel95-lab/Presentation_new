# Requested presentation media changes

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
