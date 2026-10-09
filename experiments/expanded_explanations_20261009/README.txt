Editable source for Final Presentation/Simple_speech_updated.pdf.

Revision of 9 October 2026: expanded explanations after approval of a slightly longer talk.

script.json contains all 31 spoken scripts, including openings, connected
paragraphs, playback timings and after-video explanations. The notes in the
main presentation, Thesis_Defense_Projector_Silent.pptx, 02_WebM_Silent.pptx
and 03_WMV_Silent.pptx match this speech. Their notes inherit 18 pt and retain
the bold opening, italic playback cue, paragraph spacing and page geometry.
Related sentences now share a paragraph. Only notes XML changes in the decks.

01_MP4_Light_Silent.pptx remains byte-identical as the original-notes fallback.
Its matching speech is Projector_Test_Versions/01_Fallback_Original_Speech.pdf.
Use Projector_Test_Versions/02_03_Improved_Speech.pdf for WebM and WMV.

Simple_speech.txt is the readable version. build.py produces an eleven-page
PDF: nine main-talk pages and two optional-backup pages. The extra page keeps
the technical explanations comfortably readable at the existing font size.
Run python build.py build, then inspect all pages before installing the PDF.
Install by atomic replacement; existing files may share historical hard links.

Main speech: 1,813 words. Estimated duration is 16.05 minutes at 130 words per
minute, or 16.60 minutes at 125 words per minute, including 95.946 seconds of
videos and 30 seconds for pauses. The user explicitly allowed slightly longer
explanations. Plan roughly 16-17 minutes and rehearse the equation sections.
Backup scripts contain 330 words and are outside this estimate.

sentence_prompts.json retains its historical filename and keys. It maps each
spoken sentence to the same text within the connected note paragraphs; it no
longer means one sentence per paragraph. Playback and question cues remain
unspoken. Every spoken paragraph is verified in the native PowerPoint export.

The equations are spoken in readable form, using the symbols on the slides:
force and moment spring/damping terms; tau = J transpose F; tool velocity;
the CoC lever moment; A = Ad(r_c), K_TCP = A transpose K_c A and the equivalent
damping transformation; and the existing null-space velocity condition.
Full secondary-torque formulas remain in backup B2. No visible slide changes.

Use angular offset for the starting condition and angular error for the
remaining difference. Conditioning depends on joint configuration; it does
not track a fixed joint-position target. The manual damping video provides a
qualitative comparison and does not establish measured identical push forces.

Verification and preserved originals:
experiments/expanded_explanations_20261009/verification.json
experiments/expanded_explanations_20261009/archive/
