Editable source for Final Presentation/Simple_speech_updated.pdf.

Revision of 9 October 2026: return to the original fallback wording with
small linking edits and concise impedance, CoC and null-space explanations.
Twenty-four of the 31 scripts match the fallback exactly, including all six
backup scripts. Seven scripts have limited changes. No additional examples
or extended theory are included.

script.json contains the spoken wording. Simple_speech.txt is the readable
version. build.py produces ten PDF pages, with eight main-talk pages and two
optional-backup pages. The four improved presentations contain matching
notes, grouped into connected paragraphs, at the existing 18 pt size.
Bold openings, italic playback cues, spacing and geometry are preserved.

01_MP4_Light_Silent.pptx and 01_Fallback_Original_Speech.pdf remain unchanged.
Use 02_03_Improved_Speech.pdf for WebM and WMV. The main deck and earlier
silent deck use the same revised wording.

Main speech: 1,646 words, compared with 1,651 in the original fallback.
Estimated duration including videos and 30 seconds for pauses is 14.76
minutes at 130 words per minute or 15.27 minutes at 125 words per minute.
The six original backup scripts contain 340 words, outside this estimate.

Run python build.py build, review the PDF, and synchronize deck notes before
installing by atomic replacement. Files can share historical hard links.
sentence_prompts.json maps individual sentences in the connected paragraphs.

Verification and preserved originals:
experiments/fallback_light_notes_20261009/verification.json
experiments/fallback_light_notes_20261009/archive/
