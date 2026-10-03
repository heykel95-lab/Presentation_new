Editable source for Final Presentation/Simple_speech_updated.pdf.

script.json contains all spoken sentences, openings and video timings.
Simple_speech.txt is the readable text version. build.py renders the nine-page PDF using ReportLab and Windows Arial fonts. Run python build.py build in this folder. Inspect the rendered pages before installing a new PDF by atomic replacement. Do not overwrite the active PDF in place: it may share hard links with historical copies.

The speech contains no slide-advance cues. Main speech: 1,159 words, about 13.69-14.98 minutes at 90-100 words/minute including full videos and pauses.

The null-space section opens: Next, I will explain the null-space controller. It explicitly states: I added two torque terms: a damping torque and a conditioning torque. The matching short prompts follow the same order in the PowerPoint notes. All 31 notes match the 151 spoken-sentence prompts. Speech page 6 and the matching note were rendered and checked; the other eight speech pages are unchanged. Verification: ../../../experiments/speech_nullspace_torques_20261003/verification.json.

Use angular offset for the starting condition and angular error for the remaining difference. The deliberately introduced offset represents the mismatch between the surface used in the controller and the real surface. sentence_prompts.json maps every spoken sentence to its short PowerPoint note prompt.

Motivation presents orientation uncertainty after surface calibration and the effect of joint friction on tool orientation. The earlier simple joint-friction sentence and its matching note are restored; do not use blockage. Motivation explains: The controller allows the tool to rotate during contact, helping it align with the surface. Its short note starts The controller allows the tool ... .

The current deliverable is Simple_speech_updated.pdf. Windows blocked replacing the older Simple_speech.pdf, which remains unchanged. The builder still generates Simple_speech.pdf as its local output; use atomic replacement when installing it to the intended final path.
