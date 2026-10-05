# Thesis and presentation workspace

## Notes push storage preparation (2026-10-05)

Removed three abandoned Git LFS temporary files only after verifying each
was an exact prefix of a preserved complete presentation and confirming
that no Git process was active. Active files and historical presentations
are unchanged. Verification: tmp/push_notes_20261005/storage_cleanup.json.

## Speaker notes at 14 pt (2026-10-04)

The user selected 14 pt for all speaker notes. Increase the inherited notes
master from 12 pt to 14 pt at all nine paragraph levels. All 31 active notes
use the requested size, confirmed in native PowerPoint. Preserve every word,
bold opening, italic playback cue, paragraph spacing and placeholder geometry.
The removed felt-difference sentence remains absent. All 31 notes still match
168 full spoken sentences. Current speech remains 1,651 main words.

All 31 rendered note pages were visually checked; the maximum text height is
302 pt in the unchanged 540 pt body. Only the notes master changes in the
PPTX; every other package member is byte-identical. Slide PDFs, speech PDF
and editable speech remain unchanged. The active PPTX was installed atomically.
Verification: experiments/notes_font_14pt_20261004/verification.json.

For working space, slide7_expand_ee_20261004/updated.pptx and
remove_damping_felt_sentence_20261004/archive/original.pptx are preserved as
byte-exact deltas using plot_heading_match_20261002/updated.pptx. The historical
Speaking/build/coc-reference-order/before.pptx is similarly stored using
Speaking/build/nullspace-headings/before.pptx. Keep those bases and all existing
shared bases. Restore with experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>. See storage_cleanup.json in this experiment.

## Remove the felt-difference sentence from slide 19 notes (2026-10-04)

On Null-space damping demonstration, footer 19 / physical 20, remove this
complete sentence from the full note and matching after-video speech:
The difference cannot be seen in the video, but it can be felt when pushing the arm.
No replacement sentence is added. The after-video explanation now starts:
With null-space control off, the arm moves more easily.
The following same-push, harder-push and held-pose sentences, the opening,
OFF/ON introduction and video cue are unchanged. This supersedes the earlier
instruction adding the removed sentence.

The native note and speech page 6 were rendered and visually checked.
All 31 notes match 168 complete spoken sentences. The other nine speech
pages are pixel-identical; all visible slides, equations, media, slide PDF
and supplementary PDF are unchanged. Main speech: 1,651 words, about 14.80
minutes at 130 words/minute including videos and pauses. At least 128.0
words/minute is needed for 15 minutes. The active deck, speech PDF and editable
sources were installed atomically. Verification:
experiments/remove_damping_felt_sentence_20261004/verification.json.

For working space, Speaking/build/define-ee/before.pptx and
Speaking/build/jacobian-singularity/before.pptx are preserved as adjacent
byte-exact delta archives using Speaking/build/nullspace-headings/before.pptx.
Keep that base and the existing shared bases. Restore with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
The complete original ZIP headers and compressed payload bytes are retained.
See storage_cleanup.json and archive_old.py in this experiment.

## Slide 7 push storage preparation (2026-10-04)

For Git LFS upload space, joint3_terminology_20261004/updated.pptx and
slide7_expand_ee_20261004/archive/original.pptx are preserved as adjacent
byte-exact deltas using plot_heading_match_20261002/updated.pptx. Keep that
shared base. Restore with experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>. One abandoned Git LFS temporary file was removed only
after verifying it was an identical prefix of the complete active deck and
that no Git LFS process was active. An unmatched temporary file was preserved.
Active presentation outputs are unchanged. See tmp/push_ee_20261004/
verification.json and storage_cleanup.json.

## Expand EE on slide 7 (2026-10-04)

On Centre of compliance: a virtual reference, footer 7 / physical 8,
the existing TCP definition now reads:
Controlled reference point
on the end effector (EE).
This expands the abbreviation before its parenthetical use. Keep the
original two-paragraph layout, 20 pt Arial typography and text-box geometry.
The matching full note and current simple speech now say:
The tool centre point, or TCP, is our controlled point on the end effector, or EE.
Every other sentence, slide element, native equation and media item is unchanged.

The slide, full note and speech page 3 were rendered and visually checked.
The other 30 slide PDF pages and nine speech PDF pages are pixel-identical.
All 31 notes match 169 complete spoken sentences. Current speech: 1,668 main
words, about 14.93 minutes at 130 words/minute including videos and pauses;
at least 129.3 words/minute is needed for 15 minutes. The active PowerPoint,
slide PDF, speech PDF and editable sources were installed atomically.
Verification: experiments/slide7_expand_ee_20261004/verification.json.

For working space, speech_damping_felt_difference_20261004/updated.pptx and
joint3_terminology_20261004/archive/original.pptx are preserved as adjacent
byte-exact deltas using plot_heading_match_20261002/updated.pptx. An incomplete
alias archive was rebuilt from the verified complete delta before completion.
Speaking/build/nullspace-headings/staged.pptx is preserved as a byte-exact delta
using Speaking/build/nullspace-headings/before.pptx. Keep this additional base
as well as both existing shared bases. Restore using
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Six regenerable note/speech PNG previews listed in scratch_cleanup.json were
removed after confirming their complete source PDFs and verification remained.
See storage_cleanup.json and scratch_cleanup.json in this experiment.

## Joint 3 terminology on slide 21 (2026-10-04)

On Null-space experiment: setup and conditions, footer 21 / physical 22,
replace link 3 with joint 3 in the existing Disturbance description box:
Joint-torque equivalent of a virtual
20 N point force on joint 3.
The first spoken explanation and matching full note use acting on joint
three instead of acting on link three. This follows the user's clarification
that the referenced entity is a joint. Keep all other wording, two-paragraph
layout, 20 pt Arial typography, geometry, equations, plot/video assets and
slide order unchanged. No thesis or figure-source edit is required.

The native slide, note, updated slide PDF and speech page 7 were rendered
and visually checked. Only the existing description box changes in the
slide PDF; the other 30 pages are pixel-identical. The other nine speech
pages are pixel-identical. All 31 notes match 169 full spoken sentences.
Speech timing and word count are unchanged: 1,662 main words, about 14.88
minutes at 130 words/minute including videos and pauses. Active PPTX,
slide PDF, speech PDF and editable sources were installed atomically.
Verification: experiments/joint3_terminology_20261004/verification.json.

For working space, speech_estimated_emphasis_20261004/updated.pptx and
speech_damping_felt_difference_20261004/archive/original.pptx are preserved
as adjacent byte-exact deltas using plot_heading_match_20261002/updated.pptx.
Speaking/build/wrench-blocks/staged.pptx, nullspace-plots/staged.pptx and
equation-alignment/staged.pptx are similarly preserved using
Speaking/build/pose-arrow-rings/before.pptx. Keep both bases. Restore with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Six regenerable older preview PNGs listed in scratch_cleanup.json were
removed after checking their archived full deck/PDF and verification.
One incomplete new staged deck was regenerated from the intact original
after an out-of-space interruption. No historical source content was lost.

## Felt damping difference in slide 19 speech (2026-10-04)

On Null-space damping demonstration, footer 19 / physical 20, replace
The difference is easier to feel than to see. with:
The difference cannot be seen in the video, but it can be felt when pushing
the arm.
The full note and matching after-video speech use this exact sentence.
The following OFF/ON, same-push, harder-push and held-pose sentences remain
unchanged, as do the before-video text, playback cue, all visible slides,
equations, media and slide PDFs. The note and speech page 6 were rendered
and visually checked; the other nine speech pages are pixel-identical.
All 31 notes match 169 full sentences. Current speech: 1,662 main words,
about 14.88 minutes at 130 words/minute including 95.946 seconds of videos
and 30 seconds for pauses. At least 128.8 words/minute is needed for 15
minutes. Outputs and editable sources were installed atomically. Verification:
experiments/speech_damping_felt_difference_20261004/verification.json.

For working space, speech_gravity_however_20261004/updated.pptx and
speech_estimated_emphasis_20261004/archive/original.pptx are preserved as
adjacent byte-exact deltas using plot_heading_match_20261002/updated.pptx.
Speaking/build/conclusion-review/staged.pptx is similarly stored using
Speaking/build/pose-arrow-rings/before.pptx. Keep both bases. Restore with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Regenerable native-preview and authored PPTX outputs in the five older
plot/legend experiments listed in scratch_cleanup.json were removed only
after verifying their complete deck archives, generators and verification.
See storage_cleanup.json and scratch_cleanup.json here.

## Emphasis before estimated values in slide 11 notes (2026-10-04)

On Impedance response to manual displacement, footer 11 / physical 12,
the after-video full note and matching speech now say:
It is important to note that the estimated values are model-based measurements.
Only the requested opening phrase was added; all other words, visible slides,
equations, media and slide PDFs are unchanged. The note and speech page 4
were rendered and visually checked. The other nine speech pages are
pixel-identical. All 31 notes match 169 complete spoken sentences.
Current speech: 1,654 main words, about 14.82 minutes at 130 words/minute
including 95.946 seconds of videos and 30 seconds for pauses. About 128.2
words/minute is needed for 15 minutes. Outputs and editable sources were
installed atomically. Verification:
experiments/speech_estimated_emphasis_20261004/verification.json.

For working space, speech_motivation_moreover_20261004/updated.pptx and
speech_gravity_however_20261004/archive/original.pptx are preserved as
adjacent byte-exact deltas using plot_heading_match_20261002/updated.pptx.
Speaking/build/simplify-nullspace/staged.pptx is similarly stored using
Speaking/build/pose-arrow-rings/before.pptx. Keep both bases. Restore with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
An interrupted alias archive was rebuilt and verified before removing its
original. Regenerable slide preview PNGs in motivation_video,
contact_heading_spacing and coupling_labels_removed were removed, together
with motivation_passive_rotation/native_preview.pptx. Their source/output
archives and verification remain. See storage_cleanup.json and
scratch_cleanup.json here.

## However transition before gravity compensation (2026-10-04)

On Real-time impedance control loop, footer 6 / physical 7, the full note
and matching speech now say:
However, gravity compensation is handled internally by the robot.
Only However, was added and the following gravity lowercased. Every other
sentence, visible slide, equation, media asset and slide PDF is unchanged.
The native note and speech page 3 were rendered and visually checked;
the other nine speech pages are pixel-identical. All 31 notes still match
169 complete spoken sentences. Current speech: 1,648 main words, about
14.78 minutes at 130 words/minute including 95.946 seconds of videos and
30 seconds for pauses. Outputs and editable sources were installed atomically.
Verification: experiments/speech_gravity_however_20261004/verification.json.

For working space, speech_contact_moment_slide14_20261004/updated.pptx and
speech_motivation_moreover_20261004/archive/original.pptx are preserved as
adjacent byte-exact deltas using plot_heading_match_20261002/updated.pptx.
Speaking/build/motivation-question/staged.pptx is similarly stored using
Speaking/build/pose-arrow-rings/before.pptx. Keep both bases. Restore with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
The remaining regenerable heading_consistency_20261002/before PNG previews
were removed; source XML archives, full deck/PDF deltas and verification
remain. See storage_cleanup.json and scratch_cleanup.json here.

## Moreover transition in Motivation notes and speech (2026-10-04)

On Motivation, footer 1 / physical 2, the full note and speech now say:
Moreover, joint friction can also affect the orientation of the tool.
Only Moreover, was prepended and the following joint lowercased. All other
sentences, visible slides, equations, media and slide PDFs are unchanged.
The note and speech page 1 were rendered and visually checked; the other
nine speech pages are pixel-identical. All 31 notes match 169 full sentences.
Current speech: 1,647 main words, about 14.77 minutes at 130 words/minute,
including 95.946 seconds of videos and 30 seconds for pauses. Active outputs
and editable sources were installed atomically. Verification:
experiments/speech_motivation_moreover_20261004/verification.json.

For working space, Speaking/build/remote-figures/staged.pptx and
Speaking/build/video-backups/staged.pptx are preserved as adjacent byte-exact
deltas using Speaking/build/pose-arrow-rings/before.pptx. Keep that base.
Restore with experiments/storage_dedup_20261002/archive_generated.py restore
<delta-path>. One abandoned Git LFS temporary file was removed only after
confirming it exactly matched a prefix of the preserved complete deck and
LFS object, with no LFS process active. See storage_cleanup.json here.

## Push storage preparation (2026-10-04)

For Git LFS working space, plausibility_mean_alignment_20261004/updated.pptx
and speech_contact_moment_slide14_20261004/archive/original.pptx are preserved
as adjacent byte-exact deltas using plot_heading_match_20261002/updated.pptx.
Speaking/build/restructure/staged.pptx is preserved as an adjacent byte-exact
delta using Speaking/build/pose-arrow-rings/before.pptx. Keep both bases.
Restore with experiments/storage_dedup_20261002/archive_generated.py restore
<delta-path>. Only regenerable heading_consistency_20261002/before previews
slide-01.png, slide-11.png and slide-19.png were removed; the original archives,
updated deck/PDF deltas, source and verification remain. Active outputs are
unchanged. See tmp/push_20261004/storage_cleanup.json and scratch_cleanup.json.

## Clear contact-moment explanation in slide 14 speech (2026-10-04)

For Force and moment during contact alignment, footer 14 / physical 15,
replace the two explanation sentences in the speech and matching full note:
However, the model-estimated moment is larger during the alignment motion.
It includes the contact moment from the surface, which helps turn the tool
towards alignment.

This names the contact moment directly instead of saying consistent with.
The local thesis method defines the model-estimated quantity as external
wrench about TCP. Do not imply that the complete transient difference was
experimentally isolated. The preceding force comparison and following
settling sentence, all other speech and notes, visible slides, equations,
media and slide PDFs are unchanged.

All 31 notes match 169 full spoken sentences. The ten-page speech contains
1,646 main words across eight pages and 340 backup words across two pages.
Main duration is about 14.76 minutes at 130 words/minute, including 95.946
seconds of videos and 30 seconds for pauses; at least 127.6 words/minute
is needed for 15 minutes. Speech page 5 and the native PowerPoint note
were rendered and checked. The other nine speech pages are pixel-identical.
Active outputs and editable sources were installed atomically; the saved
open presentation was reopened at the same slide position. Verification:
experiments/speech_contact_moment_slide14_20261004/verification.json.

For working space, motivation_passive_rotation_20261004/updated.pptx and
plausibility_mean_alignment_20261004/archive/original.pptx are preserved
as adjacent byte-exact deltas using plot_heading_match_20261002/updated.pptx.
Speaking/build/coc-nullspace-layout/before-Thesis_Defense_gg0_v3.pptx is
similarly stored using Speaking/build/pose-arrow-rings/before.pptx. Keep
both bases. Restore with experiments/storage_dedup_20261002/
archive_generated.py restore <delta-path>. Only regenerable native-slide-1
and native-slide-2 PNG previews in motivation_video_20261002 were removed;
verified source/output archives remain. See storage_cleanup.json and
scratch_cleanup.json here.

## Symmetric mean values under plausibility plots (2026-10-04)

On Normal-force plausibility assessment and Moment plausibility assessment,
footer slides 12/13 and physical slides 13/14, center the existing commanded
and model-estimated mean boxes beneath the left and right halves of the
actual plotting area. Their pair is now symmetric around the plot/legend
center rather than the slide center. Derive the plotting-area bounds from
the canonical plot PDF clipping rectangle and the inherited picture frame.

Only four horizontal positions change. For force, TextBox 18/19 left edges
are 275.626772/540.432756 pt. For moment, they are 273.946142/539.872520 pt.
Keep y = 447 pt, width = 216.67 pt and height = 46 pt for all four boxes.
The titles, values, fonts, colors, paragraph alignment, plots, legends,
equations and slide structure are unchanged. Notes and speech still match
the unchanged content and are preserved.

Both slides were rendered in PowerPoint and the full PDF and visually
checked. PDF text matrices move only the existing mean text; all other
pixels on those pages and all other 29 pages are identical. All other PPTX
parts, native equations, videos, notes, speech, plot assets and supplementary
PDF are unchanged. Active PowerPoint/PDF were installed atomically and the
saved open PowerPoint window was restored at its prior slide position.
Verification: experiments/plausibility_mean_alignment_20261004/verification.json.
Exact plotting bounds and box positions are in moves.json.

For working space, speech_model_measurement_slide11_20261004/updated.pptx
and motivation_passive_rotation_20261004/archive/original.pptx are preserved
as adjacent byte-exact deltas using plot_heading_match_20261002/updated.pptx.
Speaking/build/wrench-layout/before-Thesis_Defense_gg0_v3.pptx is similarly
stored using Speaking/build/pose-arrow-rings/before.pptx. Keep both bases.
Restore using experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>. Only regenerable motivation.png previews in the two
older motivation_problem_wording and motivation_single_problem experiments,
and overview_theory_20261003/after_2.png, were removed. Verified source/output
archives remain. See storage_cleanup.json and scratch_cleanup.json here.

## Passive rotation in Motivation (2026-10-04)

On Motivation, footer 1 / physical 2, the existing Idea sentence now reads:
Rotational compliance allows the tool to turn passively towards alignment.
The matching speech and full note now say:
The controller therefore allows the tool to rotate passively during contact,
which helps it align with the real surface.
Only passively is added to each sentence. Preserve the existing after-video
sentence explaining that the desired orientation remains fixed. The user
wants to make clear that the alignment rotation is not commanded.

All other wording, native text formatting, box geometry, slide order,
equations and media remain unchanged. All 31 notes match 169 full spoken
sentences. The ten-page speech has 1,645 main words and 340 backup words;
including 95.946 seconds of videos and 30 seconds of pauses, it is about
14.75 minutes at 130 words/minute. At least 127.5 words/minute is needed
for 15 minutes. The Motivation slide, note and speech page 1 were rendered
and visually checked. Full-PDF changes are confined to the existing Idea
text box; the other 30 slide pages and nine speech pages are pixel-identical.
The supplementary PDF is unchanged. Active outputs and editable sources
were installed atomically; the saved PowerPoint window was restored.
Verification: experiments/motivation_passive_rotation_20261004/verification.json.

For working space, slide6_velocity_no_ee_20261004/updated.pptx and
speech_model_measurement_slide11_20261004/archive/original.pptx are preserved
in adjacent byte-exact delta archives using the plot_heading_match_20261002
shared base. Speaking/build/angular-title/before-rename.pptx is similarly
stored as a delta using Speaking/build/pose-arrow-rings/before.pptx. Keep
both bases; restore using experiments/storage_dedup_20261002/
archive_generated.py restore <delta-path>. Only regenerable native.png and
after.png in title_date_20261003 and after.png in motivation_requirement_20261003
were removed. Verified source/output archives remain. See storage_cleanup.json
and scratch_cleanup.json in this experiment.

## Explain estimated values on slide 11 (2026-10-04)

On the plausibility experiment, footer 11 / physical 12, add after the
sentence introducing the next two plots:
The estimated values are model-based measurements.
The full speaker note and simple speech use exactly the same sentence.
Continue using simple, clear, easy-to-remember wording for speech changes.
Keep every existing sentence and the video cue; visible slides are unchanged.

All 31 notes match 169 full spoken sentences. Current speech: ten pages,
1,644 main words and 340 optional backup words. Including 95.946 seconds
of videos and 30 seconds of pauses, duration is about 14.75 minutes at
130 words/minute; at least 127.4 words/minute is needed for 15 minutes.
Speech page 4 and the native note were rendered and visually checked.
The other nine speech pages are pixel-identical; all other PPTX parts,
native equations, media, full slide PDF and supplementary PDF are unchanged.
Outputs and editable sources were installed atomically; the saved open
PowerPoint window was restored. Verification:
experiments/speech_model_measurement_slide11_20261004/verification.json.

For working space, speech_damping_video_explanation_20261004/updated.pptx
and slide6_velocity_no_ee_20261004/archive/original.pptx are preserved in
adjacent byte-exact delta archives using the plot_heading_match_20261002
shared base. Speaking/build/realtime-layout/before-Thesis_Defense_gg0_v3.pptx
is likewise stored as a delta using Speaking/build/pose-arrow-rings/before.pptx.
Keep both bases. Restore with experiments/storage_dedup_20261002/
archive_generated.py restore <delta-path>. Only regenerable native.png in
motivation_requirement_20261003 and native_1.png in overview_theory_20261003
were removed; verified source/output archives remain. See storage_cleanup.json
and scratch_cleanup.json in this experiment.

## Remove EE from the velocity equation on slide 6 (2026-10-04)

On Real-time impedance control loop, footer 6 / physical 7, the Jacobian
equation now reads x-dot = J(q)q-dot. Remove only the EE subscript from
x-dot. Preserve the native editable Office equation, its 22 pt Cambria
Math typography and original frame. The geometric linear/angular velocity
interpretation remains unchanged; x-dot is not a vector of Euler-angle
derivatives. Other EE notation on other slides is outside this request.

The equation LaTeX source, PDF/PNG/SVG assets, native-equation catalog and
manifest are synchronized. The speech and full notes were checked: they
already use general wording without the EE subscript, so no wording
change is needed. All 31 notes, all speech files, the other 30 slides,
all 30 native equations and media are preserved. The slide and final PDF
were rendered and visually checked. The PDF replaces only the equation's
drawing block and matching font resources; pixel changes are confined
to the equation. Other 30 pages and the supplementary PDF are unchanged.
Active outputs and assets were installed atomically, and the saved open
PowerPoint window was restored. Verification:
experiments/slide6_velocity_no_ee_20261004/verification.json.

For working space, speech_nullspace_velocity_position_20261004/updated.pptx
and speech_damping_video_explanation_20261004/archive/original.pptx are
preserved as adjacent byte-exact delta archives using the shared
plot_heading_match_20261002/updated.pptx base. Speaking/build/clarity-revision/
before-revision.pptx is likewise preserved in its adjacent delta using
Speaking/build/pose-arrow-rings/before.pptx. Keep both bases. Restore with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Remaining regenerable PNG previews in nullspace_arrows_20261003 were removed;
its original sources and verified deck/PDF delta archives remain intact.
See storage_cleanup.json and scratch_cleanup.json in this experiment.

## Explain the damping video through the manual push (2026-10-04)

On the damping demonstration, footer 19 / physical 20, replace the former
As you can see sentence after playback with these five simple sentences:
The difference is easier to feel than to see.
With null-space control off, the arm moves more easily.
With damping on, the same push moves the arm more slowly.
I need to push harder to move it at the same speed.
The main controller still holds the tool pose.

The full speaker note contains the same five sentences, one per paragraph.
Keep the existing opening, OFF/ON introduction and video cue. This follows
the user's qualitative account of the manual disturbance; do not claim
that identical manual forces were measured between trials. Video, slide
body, equations, other speech and all other notes remain unchanged.

All 31 notes match 168 full spoken sentences. Current speech: ten pages,
1,637 main words and 340 optional backup words. Including 95.946 seconds
of videos and 30 seconds of pauses, duration is about 14.69 minutes at
130 words/minute; at least 126.9 words/minute is needed for 15 minutes.
Speech page 6 and the native note were rendered and visually checked.
The other nine speech pages are pixel-identical. All other PPTX parts,
full slide PDF and supplementary PDF are unchanged. Active outputs and
editable sources were installed atomically; the saved PowerPoint window
was restored at its previous slide position. Verification:
experiments/speech_damping_video_explanation_20261004/verification.json.

For working space, conclusion_rotation_sentence_20261004/updated.pptx and
speech_nullspace_velocity_position_20261004/archive/original.pptx are
preserved as adjacent byte-exact delta archives using the shared
plot_heading_match_20261002/updated.pptx base. Speaking/build/
before-remove-axis-definitions.pptx is likewise stored in its adjacent
delta using Speaking/build/pose-arrow-rings/before.pptx. Keep both bases.
Restore with experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>. Only regenerable nullspace_arrows_20261003/
native-2.png and native-3.png previews were removed; source files,
verified deck/PDF delta archives and verification are retained.
See storage_cleanup.json and scratch_cleanup.json in this experiment.

## Null-space torque explanation in speech and notes (2026-10-04)

On Null-space controller, footer 18 / physical 19, add this full sentence
immediately after introducing the two torque terms:
Damping is based on joint velocity, while conditioning is based on joint position.
The speech and matching notes are synchronized. This describes the dependency
of each term without implying that conditioning tracks a fixed joint-position
setpoint. The following existing sentences explain damping and improving
the minimum singular value. Every pre-existing spoken sentence is preserved.
The wording is supported by the local null_controller_damping.tex and
null_controller_conditioning.tex equations and existing explanatory material.

All 31 notes now match 164 full spoken sentences. The ten-page speech has
1,608 main words and 340 optional backup words. Including 95.946 seconds
of videos and 30 seconds of pauses, the main talk is about 14.47 minutes
at 130 words/minute or 14.96 minutes at 125 words/minute. Speech page 6
and the native note were rendered and visually checked; the other nine
speech pages are pixel-identical. Every other PPTX part, visible slide,
equation, media item, full slide PDF and supplementary PDF is unchanged.
Active outputs and editable sources were installed atomically; the saved
PowerPoint window was restored at its previous slide position. Verification:
experiments/speech_nullspace_velocity_position_20261004/verification.json.

For working space, slide7_moment_above_tcp_20261003/updated.pptx and
conclusion_rotation_sentence_20261004/archive/original.pptx are preserved
as adjacent byte-exact delta archives using the plot_heading_match_20261002
shared base. Speaking/build/pose-joints/staged.pptx is also preserved in
its adjacent delta archive using Speaking/build/pose-arrow-rings/before.pptx.
Keep both bases. Restore exact bytes using storage_dedup_20261002/
archive_generated.py restore <delta-path>. Only regenerable after/ PNGs
in heading_consistency_20261002 were removed; its original sources,
verified deck/PDF delta archives and verification remain intact.
See storage_cleanup.json and scratch_cleanup.json in this experiment.

## Wording corrections always update notes; conclusion sentence (2026-10-04)

Whenever the user asks to improve or correct presentation or speech wording,
also update the matching speaker notes. Keep the corresponding speech and
editable sources synchronized. This is an ongoing user preference.

The Conclusion and future work speech, footer 24 / physical slide 25, now says:
Allowing the tool to rotate during contact helps reduce the angular error.
This replaces the unclear sentence about contact with the surface reducing
the error. The matching full sentence in notesSlide24.xml is synchronized.
The original sentence was in the speech and notes only; visible slide wording
is unchanged. All other spoken sentences, notes, native equations, media,
visible slides, full slide PDF and supplementary PDF are unchanged.

The updated speech page 8 and conclusion note were rendered and visually
checked. The other nine speech pages are pixel-identical. All 31 notes
match all 163 full spoken sentences. The ten-page speech has 1,595 main
words and 340 optional backup words. Main timing is about 14.37 minutes at
130 words/minute, including 95.946 seconds of videos and 30 seconds of
pauses; at least 123.6 words/minute is needed for 15 minutes.
The active deck, speech PDF and editable sources were installed atomically.
The saved open PowerPoint file was refreshed at its previous slide position.
Verification: experiments/conclusion_rotation_sentence_20261004/verification.json.

For working space, slide17_horizontal_legend_20261003/updated.pptx and
slide7_moment_above_tcp_20261003/archive/original.pptx are preserved as
adjacent byte-exact delta archives. Keep plot_heading_match_20261002/updated.pptx
as their shared base. Restore using experiments/storage_dedup_20261002/
archive_generated.py restore <delta-path>. Two byte-identical Speaking/build
pairs were consolidated with hard links, retaining all original paths:
remove-last-future/staged.pptx with split-stiffness-conclusion/before.pptx;
restore-force-panel/before.pptx with split-stiffness-conclusion/staged.pptx.
See storage_cleanup.json and identical_copy_dedup.json in the experiment.
Continue replacing files atomically to preserve historical hard-linked copies.

## Slide 7 moment centred above TCP and force (2026-10-03)

On Centre of compliance: a virtual reference, footer 7 / physical 8, centre
the clockwise moment arc and m_TCP label directly above TCP and the force
arrow, following the arrangement on footer slide 8. In the editable
coc_force_shift_general.tex, M = T + (0,0.50), the radius is 0.95 cm,
and the label is at T + (0,2.00). The arc still runs clockwise, 150 to
30 degrees. Its arrangement is raised 0.20 cm relative to the slide-8
construction to keep the right arrowhead clear of the diagonal r_c label.
This supersedes the earlier left-shifted moment position on this diagram.

The force arrow remains at TCP. Surface, tool, normal axis, TCP/CoC points,
displacement, colours, line widths, labels, figure canvas and slide placement
are unchanged. Only three source lines change. The PDF/PNG/SVG diagram
assets and manifest are synchronized. The deck changes only the existing
diagram image payload; all native slide text, equations, notes, videos and
other objects retain their exact package bytes. Speech and thesis are unchanged.

The slide was rendered in PowerPoint and the final PDF and visually checked.
The full PDF replaces only this diagram image; all other 30 pages are
pixel-identical. The supplementary PDF is unchanged. Active files and
editable sources were installed atomically. Verification:
experiments/slide7_moment_above_tcp_20261003/verification.json.

For export space, plausibility_remove_repeated_prediction_20261003/updated.pptx
and slide17_horizontal_legend_20261003/archive/original.pptx are preserved in
adjacent byte-exact delta archives using plot_heading_match_20261002/updated.pptx.
Restore with experiments/storage_dedup_20261002/archive_generated.py restore
<delta-path>; keep that shared base. Two pairs of identical Speaking/build
copies were consolidated with hard links, preserving both original paths and
all bytes: nullspace-conclusion/staged.pptx with translation-conclusion/before.pptx;
remove-last-future/before.pptx with stiffness-one-sentence/staged.pptx.
See identical_copy_dedup.json. Continue installing changes atomically to
preserve historical hard-linked copies.

## Restore the horizontal legend on slide 17 (2026-10-03)

On Contact response at different CoC positions, footer 17 / physical 18,
the three legend entries are again side by side in one horizontal row.
Restore the existing contact_legend_balanced asset (ppt/media/image51.png),
with its original labels, black/red/blue swatches and 15 pt typography.
The visible entries are centred below the three plots at y = 410 pt.
Use the existing Legend - normal force picture; only its image relationship
and frame change. Original plot images, data, headings, notes and speech remain.

The slide was rendered in PowerPoint and the full PDF and visually checked.
The PDF changes only the legend image and its placement, preserving the
original footer-logo rendering. All other 30 PDF pages and all other PPTX
parts are unchanged. Existing legend assets and editable sources are reused
without modification. Thesis and supplementary PDF remain unchanged.
The active deck and PDF were installed atomically. Verification:
experiments/slide17_horizontal_legend_20261003/verification.json.

For export space, plausibility_two_curves_20261003/updated.pptx and its
matching plausibility_remove_repeated_prediction_20261003/archive/original.pptx
are preserved as adjacent byte-exact delta archives. Keep the shared
plot_heading_match_20261002/updated.pptx base. Restore with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Two pairs of identical Speaking/build copies were consolidated with hard
links, preserving both original paths and every byte: conclusion-plain-wording/
before.pptx with future-work-wording/staged.pptx; conclusion-review/pushed.pptx
with future-work-removal/last-pushed.pptx. See identical_copy_dedup.json.
Only verified scratch duplicates of thesis figure inputs were removed from
the preceding isolated thesis build; canonical sources and outputs remain.

## Remove repeated predictions below the plausibility plots (2026-10-03)

On footer slides 12 and 13 (physical 13 and 14), remove the complete
Quasi-static mean box below each plot, including -19.65 N and 1.72 N.m.
These predictions already appear in the equations above the plots. Keep
both upper Quasi-static prediction headings and native equations. This
supersedes the preceding instruction to keep the below-plot prediction means.
The existing Commanded mean and Model-estimated mean boxes are centred in
two columns beneath each plot, with unchanged wording, values and styles.
Both plots still contain only the commanded and model-estimated curves.

The force speech and full note now say The two values shown below the plot
are mean values calculated over the shaded steady-state interval. Only
three changes to two; every other spoken sentence and note is unchanged.
All 31 notes still match 163 full sentences. The speech remains ten pages,
1,597 main words and about 14.38 minutes at 130 words/minute including videos
and pauses. Its changed page 4 and the changed note were visually checked;
the other nine speech pages are pixel-identical.

Thesis Figures 5.2/5.3 were checked on PDF page 87 / printed page 62.
They have no duplicate prediction values beneath their plots. Each prediction
is already stated in the preceding prose; no thesis edit is needed or made.
Both revised slides were rendered and visually checked. All changes are
confined to the bottom value row; the other 29 slide PDF pages are identical.
Plots, equations, videos, other notes and supplementary PDF are preserved.
Active PPTX, full PDF, speech PDF and editable sources were installed atomically.
Verification: experiments/plausibility_remove_repeated_prediction_20261003/
verification.json.

For export space, speech_remove_contact_sentence_20261003/updated.pptx and
plausibility_two_curves_20261003/archive/original.pptx are preserved in
adjacent byte-exact delta archives, using plot_heading_match_20261002/updated.pptx.
Speaking/build/null-torque-symbols/staged.pptx and pose-ee/staged.pptx are
also preserved as exact adjacent deltas using Speaking/build/pose-arrow-rings/
before.pptx. Keep both shared bases. Restore with experiments/storage_dedup_
20261002/archive_generated.py restore <delta-path>. Two other candidate
build copies were kept because their deltas would not save space. Only
verified scratch duplicates of original withdrawn thesis figures were removed.

## Two curves in the force and moment plausibility plots (2026-10-03)

Footer slides 12 and 13 (physical slides 13 and 14) and thesis Figures 5.2
and 5.3 now show only Commanded (black) and Model-estimated (red).
Remove the blue Quasi-static prediction curve and its legend entry from
both shared plots. Keep the quasi-static equations, numerical predictions,
below-plot mean values, stationary shading, axes, ticks, limits and data.
The notes and speech remain unchanged.

The canonical generator is MyOwn/code/python/figures/
make_wrench_evaluation_figures.py. It retains the original spring analysis
and reported statistics, but no longer plots the prediction curve.
MyOwn/FIGURE_STYLE.md records the two-series convention. Matching vector
PDFs in both repositories and presentation PDF/PNG/SVG assets are synchronized.
The original generator reproduced both old plots pixel-exactly; checks confirm
that all remaining samples, colours, axis geometry and plot dimensions match.

Both slides and the thesis page were rendered and visually checked. Changes
on the slides are confined to the plot frames; the other 29 presentation
PDF pages and 117 thesis PDF pages are pixel-identical. Thesis.pdf has 118
pages; both figures are on PDF page 87 / printed page 62. All slide text,
native equations, 31 notes, media, speech, thesis prose and supplementary PDF
remain unchanged. Active files were installed atomically. Verification:
experiments/plausibility_two_curves_20261003/verification.json.

For export space, tcp_force_moment_20261003/updated.pptx and its matching
historical copy in speech_remove_contact_sentence_20261003/archive/original.pptx
are preserved in adjacent byte-exact .pptx.delta.zip archives. Keep the shared
plot_heading_match_20261002/updated.pptx base. Restore using
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.

## Remove the contact-point sentence from speech and notes (2026-10-03)

On physical slide 8 / footer 7, remove exactly this spoken sentence:
It is important to note that the physical contact point itself does not move.
Its full-sentence note paragraph is also removed. Do not add replacement
wording. Every other spoken sentence and note paragraph remains unchanged.

Current speech: Final Presentation/Simple_speech_updated.pdf, ten pages,
1,597 main spoken words, about 14.38 minutes at 130 words/minute including
95.946 seconds of videos and 30 seconds for pauses. Approximately 124
words/minute is needed for 15 minutes. All 31 notes match the 163 remaining
full spoken sentences; no Next slide cues or sources are present.

Speech page 3 and the changed note were rendered and visually checked.
The other nine speech pages have identical content streams and pixels.
Visible slides, equations, media, other 30 notes, full slide PDF and
supplementary PDF are unchanged. Editable speech sources, sentence mapping
and timing metadata are synchronized. Active files were installed atomically.
Verification: experiments/speech_remove_contact_sentence_20261003/verification.json.

For export space, tool_pose_generic_20261003/updated.pptx and its matching
historical copy in tcp_force_moment_20261003/archive/original.pptx are
preserved as adjacent byte-exact delta archives. Keep the shared base
plot_heading_match_20261002/updated.pptx. Restore with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.

## Forces at TCP and moment labels m_TCP on slides 7 and 8 (2026-10-03)

The latest user request supersedes the virtual-force arrow placement and
m_CoC labels on footer slides 7 and 8 (physical slides 8 and 9).
The force arrow f on slide 7 and both f_n arrows on slide 8 now act at TCP.
All three curved-arrow moment labels are m_TCP. The native slide 7 equation
is m_TCP = r_c cross f, under Additional moment about the TCP:. This remains
the additional coupling contribution. p_CoC and r_c stay unchanged, as do
the supporting/opposing moment directions and all other figure geometry.
The general moment arc moves slightly left to clear the force arrow.

The two existing captions now read The physical force acts at the TCP.
and Curved arrows show the additional moment about the TCP. These align
with the existing full speech and notes. All other slide wording, titles,
typography and image frames are preserved. Both diagrams retain their
original pixel dimensions; the cases source adds a small right border to
preserve its canvas after moving the former outer force label.

Editable TikZ/LaTeX and PDF/PNG/SVG assets for coc_force_shift_general,
coc_force_shift_cases and coc_added_moment are synchronized, together with
the figure manifest and native equation catalog. Both final slides were
rendered in PowerPoint and the full PDF and visually checked. Only the
two requested PDF pages change; the other 29 are pixel-identical. All 31
notes, speech, media/playback, other slides and supplementary PDF remain
unchanged. Active files were installed atomically. Verification:
experiments/tcp_force_moment_20261003/verification.json.

For export space, older notes_full_sentences_20261003/updated.pptx and
quasistatic_prediction_20261003/updated.pptx and their matching historical
hard-linked copies are preserved as adjacent byte-exact delta archives.
See experiments/tcp_force_moment_20261003/storage_cleanup.json for exact
paths. Keep plot_heading_match_20261002/updated.pptx as their shared base;
restore with experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>. No historical content was discarded.

## Slide 3 describes the tool with generic pose notation (2026-10-03)

On Cartesian pose, physical slide 4 / footer 3, use Cartesian pose of the
tool: and remove EE from the pose definition, position vector and forward
kinematics. The native equations are x = [x y z phi theta psi]^T and
x = x(q). The position vector is p. Both diagram labels read Tool.
This supersedes earlier EE-label/subscript requirements on this slide only.

Both diagrams now include the same schematic rectangular grinding tool
held by the original gripper. The marked tool reference point lies at the
centre of its working face. The shared sources/pose_tool.tikz macro reuses
pose_gripper.tikz; the existing gripper source is unchanged. Tool geometry
is illustrative, without experimental dimensions or an exact tool model.
Existing axes, projections, positive rotation curls, roll/pitch/yaw labels
and scientific colors remain. Figure widths and top placement are retained,
and their heights preserve the revised assets' proportions.

Both equations remain native editable Office Math in the original 22 pt
Cambria Math style. The four corresponding editable source files and their
PDF/PNG/SVG assets, equation catalog and figure manifest are synchronized.
The revised slide was rendered and visually checked in PowerPoint and the
full PDF. The other 30 PDF pages are pixel-identical. All 31 full-sentence
notes, speech files, other slide parts, media/playback and supplementary PDF
are unchanged. Active files were installed atomically. Verification:
experiments/tool_pose_generic_20261003/verification.json.

## Full sentences in speaker notes; no next-slide cues (2026-10-03)

The latest user request supersedes the short sentence-start/ellipsis format.
All 31 slides now have the full spoken sentences from the current simple
speech, including all six backup scripts. All 164 sentences match the speech
exactly. Each sentence has its own paragraph, with the spoken opening in bold.
All 24 [Next slide] cues are removed. Keep video cues and the final questions
cue in their existing gray italic style. Sources remain absent.

Only the 31 notes-body paragraph sequences change in the PPTX. Every other
package part is byte-identical: visible slides, native equations, plots,
media, playback, masters, layouts, slide order and hidden backup flags.
Simple_speech_updated.pdf, both slide PDFs, spoken script and readable text
remain unchanged. The sentence mapping now stores complete sentences as
its prompt values, and its verification/documentation are synchronized.

All 31 notes were rendered in PowerPoint, individually checked, and verified
against the speech PDF. All text fits the original notes geometry without
clipping. Active files were installed atomically. Verification:
experiments/notes_full_sentences_20261003/verification.json.

For working space, older speech_user_text_20261003/updated.pptx and
wrench_plot_heading_20261003/updated.pptx plus their matching historical
hard-linked copies are preserved as adjacent byte-exact delta archives.
See experiments/notes_full_sentences_20261003/storage_cleanup.json for
exact paths. Keep plot_heading_match_20261002/updated.pptx as the shared
base. Restore with experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>. Six regenerable authoring/preview PPTX files in
speech_user_text_20261003 and quasistatic_prediction_20261003 were removed;
their source archives, generators, PDFs and reviewed renders remain.

## Quasi-static prediction headings match the speech (2026-10-03)

On footer slides 12 and 13 (physical 13 and 14), replace the heading
Quasi-static calculation: with Quasi-static prediction: above the equations.
Keep the existing 19 pt bold navy Arial style and original box geometry.
Quasi-static mean: below both plots is unchanged. Equations, plot assets,
values, notes, speech, slide order and all other slide parts remain unchanged.
The two slides were rendered and visually checked; both labels fit on one
line. The full PDF is synchronized, and its other 29 pages are pixel-identical.
The supplementary PDF is unchanged. Active files were installed atomically.
Verification: experiments/quasistatic_prediction_20261003/verification.json.

For export space, speech_nullspace_torques_20261003/updated.pptx and the
matching speech_user_text_20261003/archive/original.pptx are now adjacent
byte-exact delta archives. Keep plot_heading_match_20261002/updated.pptx
as their shared base. Restore exact original bytes with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.

## Speech and notes follow the user's pasted script (2026-10-03)

The latest pasted speech supersedes previous wording for all 25 main slides.
Preserve its 1,611 spoken words exactly, apart from normalized whitespace.
Three nonspoken audio-download link lines are omitted; do not copy their
signed URLs into editable sources. All six existing backup scripts (340
words) and their notes remain unchanged.

Current speech: Final Presentation/Simple_speech_updated.pdf, ten pages:
eight main-talk pages and two optional backup pages. With 95.946 seconds
of videos and 30 seconds for pauses, the main talk is about 14.49 minutes
at 130 words/minute. Approximately 125 words/minute is required to meet
15 minutes; the previous 90-100 words/minute estimate no longer applies.

The 25 main speaker notes now follow every sentence of this supplied text
with its exact first 2-5 words and literal ellipses. All 31 notes match
164 sentence prompts. Opening prompts remain bold; existing delivery cues
are preserved and sources remain absent. Editable script, readable text,
sentence mapping and builder are synchronized. All ten speech pages and
25 changed note bodies were rendered and individually checked. Native
text and bounds checks passed for all 31 notes.

Only 25 notes parts changed in the PPTX. Visible slides, all equations,
media and playback, slide order, hidden backups, full slide PDF and
supplementary PDF are unchanged. Active files were installed atomically.
Verification: experiments/speech_user_text_20261003/verification.json.

For export space, twelve older Speaking/build before.pptx copies were
losslessly archived to adjacent .pptx.delta.zip files; the exact list is
experiments/speech_user_text_20261003/storage_cleanup.json. Keep their
shared base Speaking/build/pose-arrow-rings/before.pptx. Restore exact
original bytes with experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>. No historical content was discarded.

## Latest push storage preparation (2026-10-03)

The earlier nullspace_plain_terms_20261003/updated.pptx and matching
speech_nullspace_torques_20261003/archive/original.pptx are now adjacent
byte-exact delta archives. Keep the plot_heading_match_20261002/updated.pptx
base and restore with experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>. This frees Git working space without altering active
presentation or speech files. Local rollback archives remain ignored.

## Null-space speech opening and two implemented torques (2026-10-03)

On physical slide 19 / footer 18, the simple speech now opens:
Next, I will explain the null-space controller.
This replaces both That completes the contact results. and I will now
turn to extra arm motion. Before the existing damping explanation, add:
I added two torque terms: a damping torque and a conditioning torque.
All other spoken sentences and cues remain unchanged. The matching notes
use Next, I will explain ... and I added two torque terms ... . The opening
prompt stays bold, the new explanation prompt uses the existing regular
style, and all 31 notes still match 151 spoken-sentence prompts.

Current speech: Final Presentation/Simple_speech_updated.pdf, nine pages,
1,159 main words, about 13.69-14.98 minutes at 100-90 words/minute including
full videos and 30 seconds for pauses. Editable speech sources and notes
are synchronized. Speech page 6 and the changed note were rendered and
visually checked. The other eight speech page content streams are unchanged.
All visible slide parts, equations, media, other 30 notes, full slide PDF
and supplementary PDF remain unchanged. Files were installed atomically.
Verification: experiments/speech_nullspace_torques_20261003/verification.json.

For export space, nullspace_plain_heading_20261003/updated.pptx and its
matching nullspace_plain_terms_20261003/archive/original.pptx are preserved
as adjacent byte-exact delta archives. Keep the plot_heading_match_20261002
PPTX base. Regenerable authoring/preview decks and PNGs in the former folder
were removed; its exact source archives, final PDF, generator and verification
remain. Three older Speaking/build before.pptx files are also preserved as
adjacent delta archives: pose-ee, pose-base, and overview-titles. Keep their
pose-arrow-rings/before.pptx base. Restore all exact bytes using
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.

## Remove remaining redundant terminology (2026-10-03)

The repeated user request also applies to the remaining uses of redundant.
On Conclusion and future work, physical 25 / footer 24, use:
Null-space control reduced unwanted joint motion under disturbance
On Null-space torques and projector, physical 27 / backup B2, use:
Slows joint motion in the null space.
Keep the following sentence, Zero at zero joint velocity., unchanged.
The existing introduction heading remains Joint motion with a fixed tool
pose:. No visible slide now uses redundancy or redundant. Exactly two
additional text runs change, with original fonts, geometry and formatting.

Both edited slides were rendered and checked. All other PPTX parts,
equations, notes, speech, media, order and hidden flags are unchanged.
Full and supplementary PDFs are synchronized: 29 full-deck pages and five
backup pages retain identical content streams. Active files were installed
atomically. See experiments/nullspace_plain_terms_20261003/verification.json.

For export space, four older Speaking/build before.pptx files are now
byte-exact adjacent delta archives: simplify-nullspace, restructure,
remote-figures, and pose-joints. Keep their shared pose-arrow-rings/
before.pptx base. Restore via experiments/storage_dedup_20261002/
archive_generated.py restore <delta-path>. No historical content was lost.

## Simpler null-space introduction heading (2026-10-03)

On Null-space control: damping and conditioning, physical slide 19 /
footer 18, replace Redundancy and null-space motion: with
Joint motion with a fixed tool pose: . This directly summarizes the
existing explanation about changing arm posture while keeping EE pose
unchanged. Preserve the original 22 pt Arial navy bullet style and box.
Only this one text run changes. No other slide text, equations, notes,
speech, media, or supplementary PDF changes. The slide was rendered and
visually checked; the full PDF has one updated page and 30 identical
page content streams. Active PPTX/PDF were installed atomically. See
experiments/nullspace_plain_heading_20261003/verification.json.

For export space, three additional Speaking/build before.pptx copies
were preserved losslessly as adjacent .pptx.delta.zip files:
wrench-blocks, video-backups, and style-unification. Keep the shared
Speaking/build/pose-arrow-rings/before.pptx base. Restore exact bytes
with experiments/storage_dedup_20261002/archive_generated.py restore
<delta-path>. A failed partial export was removed before rebuilding;
all historical source files and active outputs remain preserved.

## Push storage preparation (2026-10-03)

PDF delta archives and full PDF ZIP archives under experiments are local
rollback assets and are ignored by Git, like PPTX delta archives.
For Git LFS working space, motivation_problem_wording_20261003/updated.pptx
and its identical wrench_plot_heading_20261003/archive/original.pptx are
preserved as adjacent byte-exact .pptx.delta.zip archives. Restore with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Keep experiments/plot_heading_match_20261002/updated.pptx as their base.
Active deliverables remain unchanged by this storage preparation.

## Consistent plot headings on slides 14-17 (2026-10-03)

Use the existing heading style from footer slides 16 and 17: 21 pt bold
Arial, navy #17365D, without a bullet. Footer 14 / physical 15 now has
Commanded and model-estimated wrench: centered above its original plot.
The plot moves down to y = 120 pt; its size, aspect ratio and asset are
unchanged. Footer 15 / physical 16 keeps Resistance to rotation about t_1:
with its mathematical run formatting, now in the same bold navy style
without its former bullet. Footer slides 16 and 17 remain unchanged.

All four slides were rendered and visually checked. Only two native slide
parts change; the other 29 slides, notes, equations, media, speech and
supplementary PDF are unchanged. The full PDF has two updated pages;
the other 29 page content streams are identical. Active PPTX and full PDF
were installed atomically. See experiments/wrench_plot_heading_20261003/
verification.json and qa-ledger.txt.

Storage: three additional Speaking/build before.pptx files are preserved
losslessly as adjacent .pptx.delta.zip files: pose-moment-style,
controller-headings, and conclusion-combined. Keep their shared base
Speaking/build/pose-arrow-rings/before.pptx. The earlier
motivation_single_problem_20261003/updated.pptx and its matching
motivation_problem_wording_20261003/archive/original.pptx are now adjacent
lossless delta archives using plot_heading_match_20261002/updated.pptx.
Keep both plot_heading_match PPTX/PDF bases. Restore exact bytes using
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Regenerable authoring/preview decks in the two Motivation experiment
folders and nullspace_arrows_20261003 were removed; original archives,
generators, final renders, PDFs and verification remain. The build-copy
archiver now uses streamed copying and skips archives with little saving.

## Motivation: calibration uncertainty and joint friction wording (2026-10-03)

The latest user revision supersedes the one-problem-only change below.
On Motivation, physical slide 2 / footer 1, the Problem bullets now read:
Orientation uncertainty after surface calibration
Joint friction can affect the tool orientation.
Use this exact wording; do not use blockage. The restored friction bullet
uses its original native 18 pt style and box. The original Idea group returns
48 pt down to its pre-removal position. Requirement, Idea wording, video,
titles, other slides, equations, media, and supplementary PDF are unchanged.

The earlier simple speech sentence Joint friction can also affect the tool
orientation. and its Joint friction can also affect ... note prompt are
restored. All other spoken sentences and prompts are unchanged. The 31 notes
again match 151 sentence prompts. Current speech: Simple_speech_updated.pdf,
nine pages, 1,152 main words, about 13.62-14.90 minutes at 100-90 words/minute
including the full videos and 30 seconds for pauses. Editable speech sources
and documentation are synchronized. The changed slide, note, and speech page
were rendered and checked; the other 30 slide PDF pages and eight speech PDF
pages are unchanged. All active outputs were installed atomically. See
experiments/motivation_problem_wording_20261003/verification.json.

Storage: restore_original_slide_text_20261003/updated.pptx and its matching
motivation_single_problem_20261003/archive/original.pptx are now byte-exact
adjacent delta archives. Additional older full/supplementary PDFs under
experiments are preserved as adjacent .pdf.delta.zip files, each recording
its original path and SHA-256. Regenerable restore_original_slide_text PNGs
were removed after preserving its full PDF and exact PPTX archive.

To recover export space, six older Speaking/build before.pptx files were
losslessly archived in their original folders: pose-linked-solid, pose-clarity,
null-torque-symbols, future-work-removal, pose-gripper-left-3d, and
angular-positive-arc. KEEP Final Presentation/Speaking/build/pose-arrow-rings/
before.pptx as their shared base, plus both existing plot_heading_match bases.
The reusable archiver is experiments/storage_dedup_20261002/
archive_build_copies_20261003.py. All PPTX/PDF deltas restore exact original
bytes with archive_generated.py restore <delta-path>. No historical content
was discarded.

## One problem in Motivation and the simple speech (2026-10-03)

Motivation, physical slide 2 / footer 1, now presents one problem:
The surface used in the controller may not match the real surface.
This reuses the simple speech wording. The separate joint-friction bullet
is removed. Keep Requirement and its aligned-tool-face statement, and both
original Idea bullets. The Idea group is moved upward 48 pt to close the
removed bullet gap. All other slide objects, including the contact video,
are preserved. This targeted user-requested change supersedes the restored
two-problem wording on Motivation only.

The matching speech removes only Joint friction can also affect the tool
orientation. Its corresponding Joint friction can also affect ... note
prompt is removed. Every remaining spoken sentence, prompt, and cue is
unchanged. All 31 notes match the 150 sentence prompts. The current speech
PDF remains Final Presentation/Simple_speech_updated.pdf; its updated
editable sources are under Final Presentation/Speaking/simple_speech.
The nine-page speech has 1,144 main spoken words, about 13.54-14.81 minutes
at 100-90 words/minute, including all main videos and 30 seconds for pauses.

The Motivation slide, its notes, and speech page 1 were rendered and checked.
The other 30 slide/PDF pages and eight speech PDF pages remain unchanged;
native equations, all media, and the supplementary PDF are preserved.
PowerPoint, full slide PDF, updated speech PDF, and editable sources were
installed atomically. See experiments/motivation_single_problem_20261003/
verification.json and speech_verification.json.

For export space, speech_rotation_clarity_20261003/updated.pptx and the
identical restore_original_slide_text_20261003/archive/original.pptx are
stored losslessly as adjacent .pptx.delta.zip files. Three older archived
full PDFs are likewise preserved in adjacent .pdf.delta.zip files:
motivation_video_20261002/archive/Thesis_Defense_gg0_v3.pdf,
reference_arrow_20261002/archive/original.pdf, and
slide17_proportions_20261001/archive/Thesis_Defense_gg0_v3.pdf.
Restore exact original bytes using storage_dedup_20261002/archive_generated.py
restore <delta-path>; retain the existing shared PPTX/PDF bases. The PDF
archiver now accepts any .pdf within experiments, with its original path
recorded. Regenerable previews and old blue-style/internal-divider PNGs
were removed; original archives, generators, and verification remain.

## Restore original wording; styling must not rewrite content (2026-10-03)

The user rejected the rewording and added claims introduced while making the
slides look nicer. Styling requests must preserve the existing words and
technical meaning. Do not add explanations, takeaways, captions, or synonyms
unless the user specifically requests those content changes.

The slide body and footer wording has been restored from
experiments/visual_structure_20261003/archive/original_slides_and_notes.zip,
the exact version before the visual refresh and concise academic copy pass.
This restores 72 rewritten text boxes and 33 deleted original text boxes,
and removes 37 newly added text boxes. The removed additions include plot
interpretations, video commentary, conclusion summaries, and supplementary
chapter labels. Original definitions, sentences, punctuation, and mathematical
text runs are retained verbatim. Title-page line breaks were adjusted without
changing any words. Layouts were adjusted only to fit the restored material
and recenter figures/videos after removing added captions.

Keep the separately requested current slide titles, date, Requirement block,
Theory chapter, forward-kinematics label, separate Surface frame, quasi-static
mean labels, null-space arrows and OFF/ON labels, backup order, and Point-shift
adjoint matrix caption. Keep continuous navy title lines, no added green
styling, no internal decorative dividers, and only the left Overview list.
Original scientific media and colours remain intact. One archived Motivation
sentence, Pressing a tilted tool creates a contact moment., remains omitted
to respect the earlier no-tilt instruction; an optional question about restoring
that exact sentence was left unanswered. Do not invent replacement wording.

There remain 25 main slides and six hidden backups, 31 total. All 30 native
equations, five videos, media assets, 31 speaker-note parts, and speech files
are unchanged. Every slide was rendered and individually checked. PowerPoint,
the 31-page full PDF, and six-page supplementary PDF were installed by atomic
path replacement. See experiments/restore_original_slide_text_20261003/
verification.json, restoration_audit.json, and visual_review.json.

For export space, overview_left_only_20261003/updated.pptx and the identical
speech_rotation_clarity_20261003/archive/original.pptx are preserved losslessly
as adjacent .pptx.delta.zip files. Historical experiments/*/updated.pdf files
with one filesystem link have been compacted into adjacent .pdf.delta.zip
files using archive_pdf_streams_20261003.py. All restore exact original bytes
with experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Keep BOTH plot_heading_match_20261002/updated.pptx and its updated.pdf as
shared bases. No source archives or historical content were discarded.

## Clear rotational-compliance sentence in the speech (2026-10-03)

The current speech PDF is Final Presentation/Simple_speech_updated.pdf.
Windows denied atomic replacement of Simple_speech.pdf (WinError 5), also
outside the sandbox, so that older PDF remains unchanged. Use the updated
PDF together with the synchronized editable sources and PowerPoint notes.

On Motivation, physical slide 2 / footer 1, the simple speech now says:
The controller allows the tool to rotate during contact, helping it align
with the surface. This replaces I let the tool give way in rotation, so
contact helps alignment. The corresponding note prompt is The controller
allows the tool ... . All other speech sentences and notes are unchanged.
The editable script, readable text, sentence-prompts mapping and speech
PDF are synchronized. All 31 notes still match every sentence opening.

The nine-page speech has 1,152 main spoken words, about 13.62-14.90 minutes
at 100-90 words/minute including full videos and 30 seconds for pauses.
The changed first speech page and note were rendered and visually checked;
speech pages 2-9 retain identical content streams. Visible slides, equations,
videos, full slide PDF and supplementary PDF remain unchanged. Active
PPTX/speech PDF and sources were installed atomically. Verification:
experiments/speech_rotation_clarity_20261003/verification.json.

For export space, remove_internal_dividers_20261003/updated.pptx and its
matching overview_left_only_20261003/archive/original.pptx are now stored
losslessly in adjacent .pptx.delta.zip files. Five historical updated.pdf
files are preserved in adjacent .pdf.delta.zip files: pose_forward_kinematics_20261003,
overview_theory_20261003, title_date_20261003, motivation_requirement_20261003,
and joint_motion_phrases_20261002. Restore all these exact bytes/paths with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
The PDF deltas use plot_heading_match_20261002/updated.pdf as their shared
base; keep both that PDF and its updated.pptx base. The reusable PDF archiver
is storage_dedup_20261002/archive_pdf_streams_20261003.py. Regenerable old
slide PNGs in visual_structure_20261003, meaningful_titles_20261003,
precise_titles_20261003 and concise_academic_text_20261003/renders were
removed; their exact archived decks, generators and verification remain.

## Overview keeps only the left chapter list (2026-10-03)

On Overview, physical slide 3 / footer 2, remove all six right-hand Chapter
purpose descriptions. Keep the six chapter names and numbers on the left
at their existing positions, with their original typography, spacing and
wording. Keep the title, continuous navy title line and footer unchanged.
The slide and full PDF were rendered and visually checked. Pixel changes
are confined to the six removed descriptions; the remaining 30 PDF pages,
all other slides, notes, speech, equations, videos and supplementary PDF
are unchanged. Active PPTX/PDF were installed atomically. Verification:
experiments/overview_left_only_20261003/verification.json.

For export space, adjoint_matrix_label_20261003/updated.pptx and its matching
remove_internal_dividers_20261003/archive/original.pptx were losslessly
compacted into adjacent .pptx.delta.zip files. The archived removed contact
demonstration at motivation_video_20261002/archive/removed_contact_demonstration.pptx
is likewise preserved as an adjacent .pptx.delta.zip, using identical compressed
media payloads from the shared base. All three restore exact original bytes
with experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Keep plot_heading_match_20261002/updated.pptx. Historical updated.pdf files in
contact_heading_spacing_20261003 and coupling_labels_removed_20261003 were
preserved byte-for-byte in adjacent updated.pdf.zip archives; extract their
single updated.pdf member to restore. The regenerable internal-divider
native_preview.pptx was removed; source archives, PDFs and renders remain.

## Remove added internal slide dividers (2026-10-03)

The user dislikes the new separation lines inside slides. Remove all 23
pale #DCE4E8 internal horizontal and vertical dividers introduced during
the visual refresh, on physical slides 2, 3, 6, 11, 13, 14, 19, 22, 25 and
27. Keep all 31 continuous navy title rules, existing diagram arrows and
lines, plot axes, native equations and other slide objects unchanged.
Retain the Point-shift adjoint matrix caption on footer 9. Do not re-add
decorative internal section or column dividers.

Every final slide was rendered. Pixel comparisons confirm that all changes
are confined to the removed divider rectangles; all other pixels match
the previously reviewed slides. All ten affected slides were individually
checked. Native equations, media, notes, speech and slide order are unchanged.
Full and supplementary PDFs are synchronized, and active files were installed
atomically. Verification:
experiments/remove_internal_dividers_20261003/verification.json.

To recover export space, three generated updated.pptx copies were archived
losslessly into adjacent .pptx.delta.zip files: overview_speech_opening_20261003,
speech_angular_mismatch_20261003 and blue_style_no_tilt_20261003. Their matching
hard-linked archive/original.pptx copies in speech_angular_mismatch_20261003,
blue_style_no_tilt_20261003 and adjoint_matrix_label_20261003 are also preserved
in adjacent .pptx.delta.zip files. Restore each exact original path with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Keep the shared plot_heading_match_20261002/updated.pptx base. Only a
regenerable blue-style native_preview.pptx was removed; renders and PDFs remain.

## Name the adjoint matrix on slide 9 (2026-10-03)

On Translation-rotation coupling, physical slide 10 / footer 9, label
A = Ad(r_c) with Point-shift adjoint matrix. The native editable caption
matches the displacement description above: regular 19 pt Arial, #687680,
at (285, 232) pt in a 600 x 28 pt box. This supersedes the earlier removal
of the adjoint label. All original shapes, equations, notes, media and
other slides remain unchanged. The slide and full PDF were rendered and
visually checked; the other 30 PDF page content streams are unchanged.
Supplementary PDF and all speech files are unchanged. Active PPTX/PDF
were installed atomically. Verification:
experiments/adjoint_matrix_label_20261003/verification.json.

## Continuous blue title lines and presentation terminology (2026-10-03)

The user clarified that removing green applies only to the styling added
during the visual refresh. Preserve original scientific plot and diagram
colors, including their existing green elements. Keep all current slide
titles, typography and geometry. Remove each short Header accent segment.
The Continuous title rule is solid navy #17365D, 1 pt high, x = 42 pt,
width = 876 pt; y = 59 pt on the title slide and 67 pt on other slides.
The newly introduced #197E83 accents are navy, with selective #C00000 red
for key result statements. The three #F1F6F7 control-loop block fills are
neutral #F2F2F2. This supersedes the earlier teal visual-refresh palette.

Do not use tilt or its derivatives in the visible presentation or simple
speech. Four text boxes on physical slides 16, 17, 29 and 30 now use angle
error, angular error or entry offset. The CoC-position plot legend uses
Positive entry offset (+9.33 degrees) and Negative entry offset (-9.38
degrees). Its editable LaTeX, PDF/PNG/SVG and embedded picture agree; data,
axes, error bars, colors, canvas and slide placement are unchanged. The
PNG is 300 dpi. The thesis legend already uses Measured Angular Offset.
Retain this terminology if regenerating the presentation-specific plot.

The deck still has 25 main slides and six hidden backups. All 30 native
equations, five videos/playback, notes and speech files are unchanged.
All 31 slides were rendered and visually checked, and changed text bounds
pass. Full and supplementary PDFs are synchronized. Active files were
installed by atomic replacement. Build, originals and verification:
experiments/blue_style_no_tilt_20261003.

## Remove gray introductory text from the speech (2026-10-03)

Simple_speech.pdf begins directly with Title slide | Opening and the spoken
greeting below its normal document header. Remove both first-page gray
paragraphs: the reading instructions and the timing/backup-page guidance.
All spoken sentences, page grouping, video/end cues, backup introduction,
headers and footers remain unchanged. PDF pages 2-9 have identical content
streams. The revised first page was rendered and visually checked. The
PowerPoint including notes, slide PDFs, script.json and speech text remain
unchanged. The editable builder and verification are synchronized. The
active PDF was installed by atomic replacement. Build and verification:
tmp/pdfs/speech_no_intro_20261003.

## Angular mismatch explained in the simple speech (2026-10-03)

Do not use tilt, tilted or tilts in the active simple speech. Use angular
offset for the starting condition and angular error for the remaining
difference, with rotation/alignment where more natural. Motivation now
explains that the real surface angle is not known exactly and the surface
used in the controller may not match it. Joint friction remains a separate
contribution to tool-orientation error.

On Contact experiment, physical 11 / footer 10, the speech explicitly says:
I deliberately start the tool with an angular offset. This represents the
mismatch between the surface used in the controller and the real surface.
The same purpose is reinforced in backup B5. The deliberate offset is a
test representation of surface mismatch. Preserve the distinction between
configured offset, measured entry offset and angular error relative to the
calibrated surface. Do not claim exact knowledge of the real surface angle
or that zero in one angular component guarantees perfect physical alignment.

Ten speech entries changed (physical 2, 9, 11, 16, 17, 18, 25, 28, 29, 30).
Seven notes bodies changed (2, 9, 11, 17, 18, 25, 30). All 31 notes still
follow every spoken sentence with its exact first 2-5 words plus ellipses.
Sources remain absent. All other PPTX parts, slide bodies, equations,
diagrams, videos/playback, full slide PDF and supplementary PDF are unchanged.
The speech PDF still omits slide-advance cues and retains nine pages.
The main speech is 1,149 words: about 13.59-14.87 minutes at 90-100 wpm,
including full videos and 30 seconds for pauses. All nine speech pages and
seven changed notes were visually reviewed; all 31 note text boxes fit.
Editable speech files in Final Presentation/Speaking/simple_speech are
synchronized, including sentence_prompts.json. Active PPTX/PDF and source
files were installed by atomic replacement. Build, originals and verification:
experiments/speech_angular_mismatch_20261003.

## Versioned simple-speech source and push storage cleanup (2026-10-03)

The current editable simple-speech package is also versioned at
Final Presentation/Speaking/simple_speech: build.py, script.json,
Simple_speech.txt and verification.json. It matches the final speech PDF,
including the new Overview opening and removal of slide-advance cues.
Generated previews and local lossless delta archives remain ignored.

For Git working space, five Speaking/build staged.pptx copies were archived
losslessly into adjacent .pptx.delta.zip: pose-grippers, future-work-removal,
pose-clarity, pose-gripper-side and terminology. Restore exact bytes with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Their base is Speaking/build/pose-arrow-rings/before.pptx; keep that base.
Regenerable native_export.pdf previews were removed from older experiment
folders after confirming their generator and updated-deck archive exist.
Final PDFs, source archives and reviewed renders are preserved.

## Remove slide-advance cues from the speech (2026-10-03)

Remove all 24 [Advance to the next slide.] cues from Simple_speech.pdf.
The editable text also omits its corresponding [Next slide.] cues, and
the canonical builder is synchronized. Preserve all spoken sentences,
openings/transitions, video cues, ending cue, nine-page grouping and timing.
The PowerPoint including its notes, full slide PDF and supplementary PDF
are unchanged. All nine speech pages were rendered and reviewed; all other
PDF text is identical and backup pages have identical content streams.
Latest build and verification: tmp/pdfs/speech_without_advance_20261003.
The active PDF was installed by atomic replacement.

For working space, precise_titles_20261003/updated.pptx was losslessly
archived into its adjacent .pptx.delta.zip using the standard shared
plot_heading_match_20261002/updated.pptx base. Restore exact bytes with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Keep that shared base. Regenerable native previews were removed from
nullspace_arrows_20261003 and the 17 folders listed in
tmp/pdfs/speech_without_advance_20261003/storage_cleanup.json; their
sources, updated-deck archives and final renders remain.

## Natural Overview opening in the simple speech (2026-10-03)

The Overview opening in Simple_speech.pdf now reads: First, I will give
you a short overview of my presentation. This replaces With that problem
in mind, here is the plan for my talk. The matching note on physical
slide 3 / footer 2 starts First, I will give ... in its original bold style.
All other speech sentences and note prompts are unchanged. Sources remain
absent. All visible slide bodies, equations, media and playback, the full
slide PDF and supplementary PDF remain unchanged. Speech PDF pages 2-9
have identical content streams; the changed first page and Overview note
were rendered and visually checked. The main speech contains 1,134 words,
about 13.44-14.70 minutes at 90-100 words/minute including videos and pauses.
The editable speech script and text are synchronized. Build, originals and
verification: experiments/overview_speech_opening_20261003. Active PPTX and
speech PDF were installed by atomic path replacement.

For working space, meaningful_titles_20261003/updated.pptx was losslessly
archived into its adjacent .pptx.delta.zip using the standard shared
plot_heading_match_20261002 base. Final Presentation/Speaking/build/
pose-gripper-solid/staged.pptx was losslessly archived into its adjacent
.pptx.delta.zip using Speaking/build/pose-arrow-rings/before.pptx. Restore
with experiments/storage_dedup_20261002/archive_generated.py restore
<delta-path>; keep both shared bases. The regenerable
precise_titles_20261003/native_preview.pptx was removed; source and final
renders remain.

## More precise titles for methods and CoC results (2026-10-03)

A second targeted title review updates physical slides 7, 11, 12, 13, 14,
17, 18, 26, 28 and 29. The titles now read, respectively:
Real-time impedance control loop; Contact phases and stiffness settings;
Impedance response to manual displacement; Normal-force plausibility
assessment; Moment plausibility assessment; Effect of CoC position on
angular error; Contact response at different CoC positions; Opposing CoC
moment during contact; Entry offset and remaining angular error; Angular
error with CoC at the TCP. These supersede the earlier titles on those
ten slides. The remaining 21 titles are unchanged.

This identifies manual displacement as the input, stiffness as the displayed
contact setting, and the actual angular/contact quantities in the results.
Titles retain the original typography and geometry and fit on one line.
Only title text and PowerPoint title metadata change. All slide bodies,
equations, diagrams, plots, videos/playback, short sentence-start notes,
speaking files, slide order and hidden backups remain unchanged. All final
slides were rendered; the ten edited slides were visually reviewed, and
the other 21 are pixel-identical to the previously reviewed slides. All body
pixels are identical. The full and supplementary slide PDFs are synchronized.
Exact title changes, reasons, original slides and verification are in
experiments/precise_titles_20261003. Install active files atomically.

For working space, notes_sentence_starts_20261003/updated.pptx was losslessly
archived into its adjacent .pptx.delta.zip with the standard shared
plot_heading_match_20261002 base. Final Presentation/Speaking/build/
pose-linked-solid/staged.pptx was losslessly archived into its adjacent
.pptx.delta.zip using Speaking/build/pose-arrow-rings/before.pptx. Both
restore exactly with experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>; retain both shared bases. The regenerable
meaningful_titles_20261003/native_preview.pptx was removed; source and final
renders remain.

## Titles matched to actual slide content (2026-10-03)

After reviewing all 31 slides, twenty titles were made more specific and
appropriate to their content. This supersedes earlier title wording on
the slides listed in experiments/meaningful_titles_20261003/title_changes.json.
The exact physical slide list is 7, 9, 11, 12, 13, 14, 15, 16, 17, 18,
19, 20, 21, 22, 23, 24, 25, 26, 28 and 29.

The two former Disturbance demonstration slides are now Null-space damping
demonstration and Null-space conditioning demonstration. The joint-history
title explicitly names Joint 1, and the Jacobian title explicitly names
the minimum singular value. The contact comparison titles name force,
moment, rotational stiffness, CoC position and entry tilt as appropriate.
Conclusion and future work now covers both closing columns. Existing clear
titles, including the formal thesis title, remain unchanged.

Only native title text and corresponding PowerPoint title metadata change.
All title typography and geometry, bodies, diagrams, plots, 30 equations,
five videos/playback, 25-main/six-backup order and hidden flags are preserved.
All 31 short sentence-start notes and all speaking files, including
Simple_speech.pdf, remain byte-identical. All slides were rendered and
individually checked. Titles fit on one line with no overlap or overflow;
pixels below the title area are identical. The 31-page full slide PDF and
six-page supplementary PDF are synchronized. Build, originals, reasons
and verification: experiments/meaningful_titles_20261003.
All three active deliverables were installed by atomic replacement.

For working space, notes_ellipsis_20261003/updated.pptx was losslessly
archived into its adjacent .pptx.delta.zip with the standard shared
plot_heading_match_20261002 base. Final Presentation/Speaking/build/
pose-gripper-left-3d/staged.pptx was losslessly archived into its adjacent
.pptx.delta.zip using Speaking/build/pose-arrow-rings/before.pptx. Restore
with experiments/storage_dedup_20261002/archive_generated.py restore
<delta-path>; retain both shared bases. The regenerable
notes_sentence_starts_20261003/native_preview.pptx was removed; its source
and final notes renders remain.

## Every note sentence starts with a few words and ellipses (2026-10-03)

All 31 slides now use brief sentence-start prompts in their speaker notes.
Every one of the 146 spoken sentences from the full simple speech is
represented by its exact first two to five words followed by literal "...".
This includes all openings and transitions. Opening prompts remain bold;
each sentence prompt occupies its own paragraph. Short grey italic video
and slide-change cues preserve the delivery sequence. Sources remain absent.

This supersedes the earlier rule to retain full opening sentences and the
27-sentence-only ellipsis pass. The notes intentionally contain memory
prompts, not complete explanations. Simple_speech.pdf remains unchanged as
the complete read-aloud script. All visible slide contents, equations,
plots/media, playback, order and all other PPTX parts are byte-identical;
the full/supplementary PDFs and all other speaking files remain unchanged.
All 31 notes pages were rendered, visually reviewed and checked for complete
prompt text and no overflow. Exact sentence-to-prompt mapping, prior notes,
build and verification: experiments/notes_sentence_starts_20261003.
The active deck was installed by atomic replacement.

For working space, notes_follow_speech_20261003/updated.pptx was losslessly
archived into its adjacent .pptx.delta.zip using the standard shared
plot_heading_match_20261002 base. Final Presentation/Speaking/build/
before-achieved-offset.pptx was archived into its adjacent .pptx.delta.zip
using Speaking/build/pose-arrow-rings/before.pptx. Restore exact bytes with
storage_dedup_20261002/archive_generated.py restore <delta-path>; retain
both shared bases. The regenerable notes_ellipsis_20261003/native_preview.pptx
was removed; its source and final notes renders remain.

## Shorter note cues with ellipses (2026-10-03)

The user permits "..." for long sentences in speaker notes. Twenty-seven
longer explanation sentences now use short memory cues with literal
three-dot ellipses. Explanations are separated into one sentence or cue per
paragraph for easy scanning. The full spoken openings, transitions between
topics, video play cues and slide-advance cues are preserved. Other short
sentences retain the simple speech wording. All 31 notes keep the same
content order and key technical meaning, including signs, approximate
numerical values and comparison baselines. Sources remain absent.

This supersedes exact word-for-word matching to the full speech for the
27 shortened sentences only. Simple_speech.pdf remains the complete
read-aloud script and is unchanged. All visible slide contents, equations,
plots/media, playback, order and all other PPTX parts are byte-identical;
the full/supplementary PDFs and all other speaking files are unchanged.
All 31 notes pages were rendered, visually checked and verified for complete
text and no overflow. Build, before/after wording and previous notes:
experiments/notes_ellipsis_20261003. Installed by atomic replacement.

For working space, concise_academic_text_20261003/updated.pptx was losslessly
archived into its adjacent .pptx.delta.zip using the standard shared
plot_heading_match_20261002 base. Speaking/build/before-nullspace-torque-
components.pptx was archived into its adjacent .pptx.delta.zip using
Speaking/build/pose-arrow-rings/before.pptx. Restore with the existing
storage_dedup_20261002/archive_generated.py restore <delta-path> command;
keep both shared bases. The obsolete notes_follow_speech_20261003/
native_preview.pptx was removed; its source and final renders remain.

## Speaker notes follow the full simple speech (2026-10-03)

All 31 notes now match Simple_speech.pdf word-for-word: the 25 main-slide
scripts and six optional backup scripts. Each note has the spoken opening
in bold, complete spoken paragraphs, and grey italic video/slide-advance
cues. Both before-video and after-video speech are included. This supersedes
the former main-sentence-plus-summary-bullets format. Source blocks remain
absent, as requested. Existing notes font inheritance and geometry remain.

Only the 31 notes-body text parts change. Every other PPTX part is
byte-identical, including visible slides, all native equations, plot assets,
videos/playback, masters, sections, order and six hidden-backup flags.
Simple_speech.pdf, full/supplementary slide PDFs, original speaking files and
the equation catalog are unchanged. All notes were checked in PowerPoint,
rendered, visually reviewed and compared with the delivered speech PDF.
Build, archived previous notes and verification:
experiments/notes_follow_speech_20261003. Installed by atomic replacement.

For working space, visual_structure_20261003/updated.pptx was losslessly
archived to its adjacent .pptx.delta.zip using the standard shared
plot_heading_match_20261002 base. Speaking/build/before-nullspace-intro.pptx
was archived to its adjacent .pptx.delta.zip using Speaking/build/
pose-arrow-rings/before.pptx. Both restore with the existing
storage_dedup_20261002/archive_generated.py restore <delta-path> command;
keep both shared bases. The obsolete simple_slide_notes_20261003/
native_preview.pptx was removed; its final renders and source archive remain.

## Full simple speech with transitions (2026-10-03)

Simple_speech.pdf is now a complete read-aloud script, replacing the former
four-page bullet script. Each of the 25 main slides has a bold spoken
opening that links naturally to the previous slide, followed by complete
simple paragraphs. All four main videos have explicit play cues and words
to say before and after playback. Grey bracketed directions are not spoken.
Slide labels follow the visible footers (Title, then slides 1-24).

The main talk is pages 1-7, 1,135 spoken words. Full videos total 95.946
seconds; with 30 seconds for pauses, estimated duration is 13.45 minutes
at 100 words/minute and 14.71 minutes at 90 words/minute. Pages 8-9 contain
complete optional scripts for B1-B6, outside the 15-minute main-talk budget.
All nine pages were rendered with Poppler and visually checked. No slide's
speech splits across pages. Previous PDF, editable script, build and checks:
tmp/pdfs/simple_speech_read_aloud_20261003.

Only the active Simple_speech.pdf deliverable changes. The presentation,
all 31 speaker notes, full/supplementary slide PDFs, original speaking files
and equation catalog remain byte-identical. Installed by atomic replacement.
The regenerable concise_academic_text_20261003/native_preview.pptx was
removed to provide working space; its source deck and final renders remain.

## Concise academic slide wording (2026-10-03)

The user requested shorter, faster-to-read academic slide text. 54 visible
text boxes now use concise phrases with key information first and arrows
where they clarify a relationship. The revised boxes contain 388 words
instead of 481. This supersedes earlier exact body-sentence wording where
the concise pass changes it, including the surface-axes and conditioning
explanations. Native Greek/subscript notation, the minimum-singular-value
definition, non-zero coupling qualification, means, experimental settings
and all numerical findings are preserved. The formal thesis title and the
Requirement statement remain unchanged. The only changed slide title is
CoC shift: effect depends on entry tilt (physical 17 / footer 16).

All shape positions, dimensions and existing typography remain unchanged.
The deck retains 25 main slides, six hidden backups, 30 native equations,
all plots/assets and five videos with original playback. All 31 speaking
notes and all speaking files, including Simple_speech.pdf, are byte-identical.
All slides were rendered and reviewed; the final full and supplementary
PDFs are synchronized. Build, before/after copy, originals and verification:
experiments/concise_academic_text_20261003. Install by atomic replacement.

For working space, simple_slide_notes_20261003/updated.pptx was losslessly
compacted into its adjacent .pptx.delta.zip with the usual plot_heading_match
base. Final Presentation/Speaking/build/before-cartesian-torque-slide.pptx
is now in its adjacent .pptx.delta.zip, using Speaking/build/pose-arrow-rings/
before.pptx as the shared base. Both restore byte-for-byte with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Keep both shared bases. The obsolete visual_structure native_preview.pptx
was removed; its final source and renders are retained and can regenerate it.

## Visual structure and aesthetic refresh (2026-10-03)

The user authorized a deck-wide improvement to aesthetics, structure and
self-explanatory content. The current design evolves the existing university
template: navy 26 pt slide titles, a small grey chapter line above the title,
a fine grey rule with a teal accent, shorter footer text, consistent bold
section headings and open aligned columns. Teal emphasizes interpretations
and key observations. This supersedes earlier fixed geometry, heading/bullet
styles and exact slide-title wording where the visual refresh changes them.

The Overview keeps its six chapter names and now explains each chapter's
purpose. Motivation is shorter and retains Requirement before Problem.
The theory slides have clearer equation/diagram groupings. Video slides have
short purpose and observation text alongside the recording. Result titles
state the supported finding, and selected plots have explanatory captions.
Conclusion separates the four findings from future work. All six backups
use the same visual system and provide context for their diagrams/results.

The deck still has 25 main slides and six hidden backups. All 30 native
equations retain their mathematics and dimensions. All image/video assets,
picture aspect ratios, five embedded videos, playback settings, masters,
sections, slide order and all 31 speaking notes are preserved. The equation
catalog and speaking PDFs, including Simple_speech.pdf, are unchanged.
The full 31-page PDF and six-page supplementary PDF match the new slides.
PowerPoint opened the complete deck and read all video metadata. All slides
were rendered and reviewed; content text has no unintended overflow/overlap.
Build, editable design specification, originals and verification are under
experiments/visual_structure_20261003. Install files by atomic replacement.

To provide export space, nullspace_results_reorder_20261003/updated.pptx was
losslessly archived to its adjacent .pptx.delta.zip using the usual shared
plot_heading_match_20261002 base. Historical before.pptx files under
Final Presentation/Speaking/build/coupling-simple, pose-gripper-solid,
review-fixes, pose-gripper-side and pose-grippers were also archived to
adjacent .pptx.delta.zip files. All restore byte-for-byte using
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
The latter four use Final Presentation/Speaking/build/pose-arrow-rings/
before.pptx as their shared base; keep this base and the usual shared base.

## Simple speaking notes on every slide (2026-10-03)

All 31 slides now have a bold main sentence followed by two to four native
bullet points with the most important things to say. Main-slide notes follow
the new Simple_speech.pdf; all six hidden backups also have concise speaking
notes for questions. The user explicitly requested removal of source
references: all source blocks, file paths and editing-history blocks have
been removed from the active notes. This supersedes earlier instructions
to keep the previous notes unchanged or include source blocks there.

The original notes and their provenance are preserved in
experiments/simple_slide_notes_20261003/archive/original_notes.zip. Editable
new notes and the build/verification are in the same experiment directory.
Existing notes-page placeholders have explicit bounds so each slide's
sentence and bullets stay together. PowerPoint rendered 31 notes pages;
every note was checked for complete text, correct order and no overflow.

Only the 31 notes XML parts changed. All other PPTX parts, including visible
slides, equations, media, masters, slide order and backup visibility, are
byte-identical. The full PDF, supplementary PDF, Simple_speech.pdf and
original speaking files are unchanged. The active PPTX was installed by
atomic path replacement. See the experiment's verification.json.

## Separate simple speech PDF (2026-10-03)

Final Presentation/Simple_speech.pdf is a new standalone four-page speaking
script for the current 25 main slides. It uses simple sentences, short
spoken bullets and bold memory cues. The six backups are excluded. Its
1,140 spoken words take about 13.5 minutes at 100 words/minute, including
all four main-slide videos (95.947 seconds) and 30 seconds for pauses.
At 90 words/minute the same budget is about 14.8 minutes. Actual delivery
pace determines duration; the requested limit is 15 minutes.

The existing presentation, slide notes and original speaking files remain
unchanged. Editable source, PDF build and verification are under
tmp/pdfs/simple_speech_20261003. The superseded generated
experiments/nullspace_arrows_20261003/updated.pptx is preserved losslessly
in its adjacent updated.pptx.delta.zip; restore using the existing
storage_dedup_20261002/archive_generated.py command and shared base.

## Joint-motion result order and joint 1 explanation (2026-10-03)

Cumulative joint motion is now hidden backup B6, physical slide 31. Its
plot, data, result phrases, typography and notes are unchanged; the main
chapter label is removed and its footer is B6. It is also the sixth page
of Supplementary_slides.pdf, whose original five pages are unchanged.

Joint motion over time now follows Null-space experiment immediately,
at physical slide 23 / footer 22. Jacobian conditioning follows at
physical 24 / footer 23. Conclusion is physical 25 / footer 24. Existing
backups B1-B5 occupy physical slides 26-30. The deck has 25 main slides
and six hidden backups, 31 total. All main footers, native sections and
the 30-entry equation catalog follow this order. These are the user's
earlier-numbered slides 21 (Cumulative joint motion) and 23 (Joint motion
over time), before the Surface frame slide was restored.

Null-space experiment, physical slide 22 / footer 21 (formerly footer
20), adds: Joint 1 motion is shown because it receives the largest peak
disturbance torque. This is a native black 20 pt Arial sentence at
(60, 274) pt in an 840 x 34 pt box, matching the task-description style.
The thesis's experimental-method chapter reports this largest peak
absolute disturbance-torque component for joint 1 in all twelve trials.
Keep the distinction between the measured joint 1 motion and the virtual
force applied on link 3. All existing slide elements retain their positions.

All original native equations, plot data/assets, five videos, notes and
speaking files remain unchanged. Both PDFs are synchronized. See
experiments/nullspace_results_reorder_20261003/verification.json.

The superseded quasistatic_mean_labels_20261003/updated.pptx is preserved
losslessly in its adjacent updated.pptx.delta.zip. Restore with the
storage_dedup_20261002/archive_generated.py command documented below.

## Null-space arrows and OFF/ON video captions (2026-10-03)

On Null-space controller, physical slide 19 / footer 18 (formerly footer
17), use three native editable navy #17365D right arrows. The reading-flow
arrow beside the null-space condition is at (435, 228) pt, 68 x 10 pt.
The damping and conditioning explanation arrows are at (75, 309) and
(525, 309) pt, each 19 x 10 pt, replacing those two round body bullets.
Retain the original wording, text origins, fonts, box dimensions, all
native equations, sigma_min formatting, notes and speaking material.

The two Disturbance demonstration captions now read Null-space control
OFF → Damping ON and Conditioning ON, on physical slides 20 and 21 /
footers 19 and 20 (formerly footers 18 and 19). The arrow in the first
caption identifies the recorded sequence. Preserve the exact video
streams, posters, 23 s split, audio, sizes, playback and notes. Other
slides and the supplementary PDF are unchanged. The full PDF is
synchronized. See experiments/nullspace_arrows_20261003/verification.json.

To recover export space, additional historical PPTX copies were losslessly
compacted to adjacent .pptx.delta.zip files: motivation_video_20261002/
archive/Thesis_Defense_gg0_v3.pptx, overview_theory_20261003/archive/
original_slides.pptx, motivation_requirement_20261003/archive/original_slide.pptx
under experiments; and both before_Thesis_Defense_gg0_v3.pptx and updated.pptx
under tmp/remove_b5_20260922 and tmp/remove_b3_b4_20260922. They retain every
original byte using shared compressed ZIP payloads and reconstruct with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Keep the shared plot_heading_match_20261002/updated.pptx base intact.

## Quasi-static mean labels below plausibility plots (2026-10-03)

On Normal-force plausibility assessment and Moment plausibility assessment,
physical slides 13 and 14 / footers 12 and 13 (formerly footers 11 and 12),
the lower comparison label is Quasi-static mean:. The analysis computes
the mean quasi-static spring force/moment over the shaded stationary
interval, matching the other two mean comparisons. Keep Quasi-static
calculation: above each native equation. Preserve the displayed values,
original label typography and box geometry, equations, plots, all other
slide contents, notes, speaking files and supplementary PDF. The full PDF
is synchronized. See
experiments/quasistatic_mean_labels_20261003/verification.json.

The earlier experiments/reference_arrow_20261002/archive/original.pptx
was losslessly compacted to adjacent original.pptx.delta.zip. Restore its
exact bytes with experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>. Keep the shared plot_heading_match_20261002 base.
The superseded surface_frame_split_20261003/updated.pptx is also preserved
in its adjacent updated.pptx.delta.zip and restores with the same command.

## Separate Cartesian pose and Surface frame again (2026-10-03)

Cartesian pose is physical slide 4 / footer 3. Surface frame is again a
separate slide immediately after it, physical slide 5 / footer 4. This
supersedes the earlier combined-slide requirement. The pose slide retains
the compact native x_EE vector, position/orientation branch, both original
diagrams and Forward kinematics: x_EE = x_EE(q). The pose group is centred,
both diagrams are 240 pt wide with their original aspect ratios, and the
forward-kinematics row is at y = 447 pt. Native equations remain 22 pt
Cambria Math and their contents and dimensions are unchanged.

Surface frame contains the original surface illustration at 360 pt width,
the native n_s and t_1, t_2 symbols, upward surface normal and perpendicular
tangents definitions, and the requested sentence: Surface axes define force
and moment components and the directions for impedance gains. The sentence
is a native 20 pt body bullet. This explicit wording supersedes the older
general ban on the word gains for this sentence. Keep the diagram source,
asset bytes and aspect ratio unchanged. Original Surface frame notes have
been restored from the archived slide and already match the speaking script.
All retained notes and all speaking files are unchanged.

There are now 26 main slides and five hidden backups, 31 total. Conclusion
is physical 26 / footer 25; backups B1-B5 are physical 27-31. Chapter starts
are physical 2, 4, 11, 13, 19 and 26. Native sections, main footers and the
30-entry equation catalog follow this order. All five videos, remaining
slide bodies, media and supplementary PDF are unchanged. The full PDF has
31 pages and is synchronized. See
experiments/surface_frame_split_20261003/verification.json.

Generated updated.pptx copies in coupling_labels_removed_20261003,
coc_introduction_20261002 and contact_heading_spacing_20261003 are stored
losslessly in adjacent .pptx.delta.zip files. The CoC introduction archive
also preserves its ZIP prefix. All reconstruct byte-for-byte with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Keep experiments/plot_heading_match_20261002/updated.pptx as the shared base.

## Contact-settings heading spacing (2026-10-03)

On Contact experiment, physical slide 10 / footer 9, Compliant contact
settings: starts at y = 155 pt, 12 pt below its former position. Keep its
x = 480 pt, 440 x 30 pt box, text and native navy heading style unchanged.
All phases, setting labels, equations, diagram and other slide contents
remain in their previous positions. Notes and speaking files are unchanged.
The full PDF is synchronized. See
experiments/contact_heading_spacing_20261003/verification.json.

Generated updated.pptx copies in pose_forward_kinematics_20261003,
motivation_video_20261002 and pose_surface_merge_20261002 are now stored
losslessly as adjacent .pptx.delta.zip files via storage_dedup_20261002.
Keep the shared plot_heading_match_20261002/updated.pptx base intact.

## Coupling-slide label removals (2026-10-03)

On Translation-rotation coupling, physical slide 9 / footer 8, remove
Shifting the impedance reference point:, Point-shift adjoint, the standalone
native p_CoC symbol, and Virtual centre of compliance (CoC): new reference.
Keep p_CoC within the displacement equation. The displacement equation and
caption now start at y = 120 and 121.07 pt, the adjoint equation at 185 pt,
the wrench equation at 276 pt, and the coupling result at 412 pt. All retain
their original horizontal positions, dimensions, contents and typography.
The remaining three equations stay native and editable. The active equation
catalog now has 30 entries; the deleted symbol's source/assets are preserved.
Other slides, notes, speaking material, media and supplementary PDF are
unchanged. The full PDF is synchronized. See
experiments/coupling_labels_removed_20261003/verification.json.

The older generated overview_theory_20261003/updated.pptx was losslessly
compacted to its adjacent .pptx.delta.zip using storage_dedup_20261002.

## Forward kinematics label and pose-slide cleanup (2026-10-03)

On Cartesian pose and surface frame, physical slide 4 / footer 3, remove
the two bottom sentences about the robot base frame and the surface axes.
Replace Pose depends on all 7 joint angles: with Forward kinematics: in
the original black 19 pt Arial style. Its box remains at (42, 396) pt and
is 198 x 28 pt. The unchanged native x_EE = x_EE(q) equation starts at
(250, 396) pt with its original dimensions and 22 pt Cambria Math styling.
All other diagrams, native equations, slide contents, notes and speaking
files are preserved. The full PDF is synchronized. See
experiments/pose_forward_kinematics_20261003/verification.json.

Generated updated.pptx copies in title_date_20261003, pose_vector_20261002
and realtime_velocity_20261002 were also losslessly compacted to adjacent
.pptx.delta.zip files using the existing storage_dedup_20261002 workflow.
The shared plot_heading_match_20261002/updated.pptx base remains intact.

## Theory in the Overview (2026-10-03)

The first Overview chapter is Theory, replacing Introduction. Keep the
corresponding native PowerPoint section and the Motivation chapter label
1. Theory synchronized with this name. Preserve the six-item Overview,
chapter membership, numbering, original text styles and geometry, all other
slide contents, notes and speaking files. The full PDF is synchronized. See
experiments/overview_theory_20261003/verification.json.

Six more generated updated.pptx copies were losslessly compacted into adjacent
.pptx.delta.zip files to free export space: motivation_requirement_20261003,
joint_motion_phrases_20261002, nullspace_result_phrases_20261002,
conditioning_sentence_20261002, coc_case_moment_labels_20261002, and
model_compensation_cycle_20261002. Restore exact bytes with
experiments/storage_dedup_20261002/archive_generated.py restore <delta-path>.
Keep experiments/plot_heading_match_20261002/updated.pptx as the shared base.

## Title date (2026-10-03)

The title slide date is Date: 05.10.2026. Retain its original blue 12 pt
Arial styling and text-box geometry. The full PDF is synchronized and all
other slide content, notes and speaking files are unchanged. See
experiments/title_date_20261003/verification.json.

## Requirement before Problem on Motivation (2026-10-03)

On Motivation, physical slide 2 / footer 1, put Requirement: above Problem:.
The existing Grinding requires an aligned tool face. statement belongs beneath
Requirement:, followed by the two existing Problem bullets and the Idea block.
Use the matching native navy 22 pt Arial bullet heading and retain all original
18 pt body wording and formatting. The left text column is spaced to fit all
three sections. Preserve the contact video, poster, playback, notes, speech,
other slides and supplementary PDF. The full PDF is synchronized. See
experiments/motivation_requirement_20261003/verification.json.

## Concise joint-motion result phrases (2026-10-02)

On Joint motion over time (physical slide 24 / footer 23), use the short
result phrases Conditioning (2 N m): repeated joint-motion reversals and
Added damping: less total motion, remaining reversals. Omit final periods.
Preserve the original 20 pt body font, bullet style, text-box geometry,
both plots and their data, native equations, notes, speaking files, other
slides and supplementary PDF. The full PDF is synchronized. This extends
the concise result-phrase style of footers 21 and 22 to footer 23. See
experiments/joint_motion_phrases_20261002/verification.json.

## Concise null-space result phrases (2026-10-02)

On Cumulative joint motion (physical slide 22 / footer 21), use two short
result phrases: approximately 25% less cumulative motion with damping alone;
approximately 50% less cumulative motion with damping added to conditioning.
Display the approximation sign before each percentage. The original precise
values are 25.1% and 50.7%; their comparisons remain damping versus no null-space
torque and combined versus conditioning alone at 2 N m, respectively.

On Jacobian conditioning (physical slide 23 / footer 22), use Decreasing
sigma_min: no null-space torque / damping alone and Nearly constant sigma_min:
conditioning / combined control. Use native Greek sigma with subscript min.
All four phrases omit final periods and retain the existing 20 pt bullet style
and text-box geometry. Keep every plot, value, legend, all equations, notes,
speaking material, other slides and supplementary PDF unchanged. The full PDF
is synchronized. See experiments/nullspace_result_phrases_20261002/verification.json.

## One-sentence conditioning explanation (2026-10-02)

On Null-space controller (physical slide 18 / footer 17), combine the two
conditioning-role bullets into one: Adjusts the joint configuration through
null-space motion to increase the minimum singular value sigma_min of J and
move away from singularities. Retain the native Greek sigma, subscript min,
italic J, original 20 pt body style and existing text-box dimensions.
This supersedes the earlier two-bullet conditioning wording. Preserve the
redundancy explanation, damping bullet, all equations, notes, speaking files,
figures, videos, other slides and supplementary PDF. The full PDF is updated.
See experiments/conditioning_sentence_20261002/verification.json.

## Matching moment labels in the CoC cases (2026-10-02)

On Centre of compliance (CoC), physical slide 8 / footer 7, both Supporting
moment and Opposing moment use m_CoC with upright CoC subscript above their
curved arrows, matching the general introduction on footer 6. This replaces
the visible r_c cross f_n labels. The arrows still depict the additional
moment about TCP produced by the force at the virtual CoC; their supporting
counterclockwise and opposing clockwise directions are unchanged.

Keep all diagram geometry, displacement and force labels, figure dimensions,
slide layout, notes and speech unchanged. The presentation-specific editable
coc_force_shift_cases TikZ and PDF/PNG/SVG assets match the embedded figure.
An invisible vertical strut retains the original 328.663 x 110.13 pt canvas.
The thesis and historical CoC_moment assets remain unchanged. All 31 native
equations, other slides, videos and supplementary PDF are preserved; the
full PDF is synchronized. See
experiments/coc_case_moment_labels_20261002/verification.json.

## Model-compensation examples and cycle heading (2026-10-02)

On Real-time control (physical slide 6 / footer 5), introduce the block
diagram with Real-time control with a 1 ms cycle: as a navy 22 pt Arial
bullet at (52, 201) pt, size 865 x 30 pt. The block diagram is translated
down by 38 pt, preserving every original element's dimensions and topology.

The additive-input label reads Model compensation: at 15.5 pt, followed by
Coriolis; gravity internal to robot at 14.5 pt and + null-space torques at
14.5 pt. The example row is (591, 276, 250, 18) pt. The null-space row is
(622, 297, 188, 20) pt; the input arrow runs from (716, 323) to (716, 341).
This explicitly distinguishes externally added Coriolis compensation from
the gravity compensation supplied internally by FCI, following the thesis
and implemented controller. Do not depict external gravity added twice.

The native diagram, editable source, DrawingML and PDF/PNG/SVG assets agree.
The standalone crop is (30, 243, 900, 243) pt in slide coordinates. Preserve
all 31 native equations, notes, speech, videos, other slides and supplementary
PDF. The full PDF is synchronized. This supersedes the earlier Coriolis-only
label and the cycle statement beneath the diagram. See
experiments/model_compensation_cycle_20261002/verification.json.

## Compact pose notation and Cartesian impedance law (2026-10-02)

On Cartesian pose and surface frame (physical slide 4 / footer 3), show the
single horizontal row x_EE = [x y z phi theta psi]^T, with upright EE and T,
as a native editable 22 pt regular Cambria Math equation. Omit the former
intermediate p_EE and eta_EE vectors. The angles remain roll-pitch-yaw
coordinates. Retain the position/orientation branch and original diagrams.
The position-only diagram retains p_EE, since it depicts position.

The lower statement reads Pose depends on all 7 joint angles: and its native
equation is x_EE = x_EE(q). The surface legend reads n_s: upward surface
normal and t_1, t_2: perpendicular tangents. The colons are separate editable
ordinary text; the native surface-axis symbols remain unchanged. Upward
describes the surface normal shown in the existing surface-frame diagram.
Remove the blue Next: force f, moment m, stiffness K and damping D sentence.
The following slide, physical 5 / footer 4, is titled Cartesian impedance law.
Its remaining body is unchanged. The chapter name stays Cartesian controller.

Both changed equation sources, catalog entries and PDF/PNG/SVG assets agree
with the deck and full PDF. Preserve all other equations, diagrams, notes,
speaking files, videos and supplementary PDF. The 30-slide structure and
31-native-equation count remain. This supersedes the two-row pose vector
and p_EE = p_EE(q) requirements on this slide. See
experiments/pose_simplified_20261002/verification.json.

To free working space, seven earlier generated updated.pptx copies were
losslessly compacted to adjacent .pptx.delta.zip files. They reconstruct
byte-for-byte with experiments/storage_dedup_20261002/archive_generated.py
restore <delta-path>. Keep experiments/plot_heading_match_20261002/updated.pptx
intact as their shared binary base. This does not affect the separately
archived removed slides or source assets. Install all future active PPTX/PDF
files by atomic path replacement because archived copies may share hard links.

## Matching headings above result plots (2026-10-02)

On Effect of rotational stiffness and Effect of CoC position, physical
slides 15 and 16 / footers 14 and 15, match the heading style on footer 16:
navy #17365D, 22 pt regular Arial, a native round navy bullet at 80 percent,
and a full-size normal-baseline colon. The headings read Resistance to
rotation about t_1: and CoC displacement along t_2:. Keep the italic t and
14 pt numerical subscripts. The colon is a separate ordinary Arial run.

The rotational heading retains its centred (220, 57, 520, 27) pt box. The
CoC heading uses (307, 81, 291, 30) pt, followed by the unchanged native
r_c,t2 symbol at (610, 84) pt. This group is centred above the plot.
Both original plot boxes, data, legends, assets, all 31 native equations,
notes, speech, other slides and supplementary PDF are unchanged. The full
PDF is synchronized. See experiments/plot_heading_match_20261002/verification.json.

Storage note: active deliverables and archived generated copies may share
hard links. Always install a new PPTX/PDF by atomic replacement of its path;
never truncate or overwrite an existing active file in place. Preserve
archived versions when freeing generated working-file storage.

## Quasi-static calculations before the plausibility plots (2026-10-02)

On Normal-force plausibility assessment and Moment plausibility assessment,
physical slides 12 and 13 / footers 11 and 12, show the native force/moment
equation before the plot. Introduce it with Quasi-static calculation: as an
editable navy 22 pt Arial bullet, matching the manual-input heading.
The new heading is at (40, 100) pt with size 300 x 30 pt. The unchanged
equation starts at (350, 96) pt. The unchanged 650 x 269.611 pt plot starts
at (155, 174) pt. Retain the original manual-input heading above this row
and the three numerical comparison labels/values below the plot.

Keep every native equation's content, typography and dimensions, each plot's
data, dimensions, legend, colours and asset bytes, and the existing notes
and speaking files. The 30-page full PDF is synchronized; the other 28
slides/pages, all 31 native equations and supplementary PDF are unchanged.
This supersedes the earlier plot-before-equation placement for these two
slides. See experiments/quasistatic_before_plots_20261002/verification.json.

## Explicit Coriolis compensation label (2026-10-02)

On Real-time control (physical slide 6 / footer 5), the additive torque input
reads Coriolis compensation on the first row and + null-space torques on the
second. This replaces Model + null-space / Torques. Preserve the first row's
Arial 15.5 pt and the second row's Arial 14.5 pt, both centred over the
unchanged torque-summing arrow at x = 716 pt. The second textbox is widened
to (622, 239, 188, 20) pt so the wording fits on one line.

The model contribution here is the implemented Coriolis/centrifugal torque
compensation; gravity and motor-friction compensation are internal to FCI.
The native slide, standalone DrawingML, generator and PDF/PNG/SVG agree.
The full PDF is synchronized. All other shapes, 31 native equations, notes,
speaking files, videos, other slides and supplementary PDF are unchanged.
See experiments/coriolis_label_20261002/verification.json.

## CoC parameter reference and additional moment notation (2026-10-02)

On Centre of compliance (CoC), physical slide 7 / footer 6, define the CoC
as Virtual reference point for / Cartesian stiffness and damping. Preserve
the navy bullet heading and two-line black 20 pt Arial definition.

Use m_CoC = r_c cross f in the editable native equation and m_CoC on the
diagram's curved arrow, with upright CoC subscripts. This notation names the
CoC-induced additional moment about the TCP. Keep the heading Additional
moment about the TCP: to make the reference point explicit. It is the
coupling contribution, not the complete rotational-impedance moment.
Preserve the diagram geometry, the force location at the virtual CoC, the
physical contact location and all existing shape positions and styles.

The equation source/catalog and both affected PDF/PNG/SVG asset sets agree
with the deck and full PDF. This supersedes Delta m on this introduction
slide only. The other 29 slides/pages, remaining 30 native equations,
speaker notes, speaking files, videos, supplementary PDF and thesis remain
unchanged. See experiments/coc_reference_moment_20261002/verification.json.

## Consistent blue headings and CoC introduction layout (2026-10-02)

On Centre of compliance (CoC), physical slide 7 / footer 6, use native navy
22 pt Arial bullet headings Tool centre point (TCP):, Centre of compliance
(CoC):, and Additional moment about the TCP:. The two definitions are 20 pt
black Arial, indented below their headings. The virtual-force explanation is
a 20 pt dark body bullet. Keep the original diagram proportions and content,
now at (440, 88) pt, and the unchanged native added-moment equation at
(540, 439) pt. The text and figure form aligned left/right columns.

Throughout the deck, retain the audited colons on section and parameter
headings that introduce content, including the controller, contact settings,
result panels, experiment settings, Future work, and the torque backup.
Use navy #17365D for subtitles. The validation summary labels are navy with
colons while numerical values stay black. Native heading bullets are round,
navy, 80 percent, with a 20 pt hanging indent. Existing embedded diagram
labels, mathematical definitions, captions, full statements and slide titles
retain their own roles and styles; do not indiscriminately append colons.

The formatting pass affects physical slides 2, 4, 5, 7, 8, 9, 10, 12, 13,
15, 16, 17, 18, 21, 25 and 27. All 31 native equations, all media and diagram
assets, notes and speaking material are unchanged. The 30-page full PDF and
five-page supplementary PDF are synchronized; only supplementary page B2
changes. See experiments/heading_consistency_20261002/verification.json.

## Coupling-slide text cleanup (2026-10-02)

On Translation-rotation coupling (physical slide 9 / footer 8), remove the
three repeated statements: Tool centre point (TCP): controlled reference point
on the (EE), Choosing an impedance reference point away from the TCP couples
force and moment, and The commanded force acts as if applied at the virtual
point p_CoC. Retain the shifting-reference heading, virtual-CoC definition,
displacement and adjoint definitions, all four native equations and the final
off-diagonal-block statement. The retained rows are spaced more evenly while
preserving their contents, fonts, sizes and horizontal alignments. Preserve
speaker notes and speaking files. The earlier CoC introduction remains intact.
The 30-slide deck and full PDF agree, and the other 29 slides/pages and the
supplementary PDF are unchanged. See
experiments/coupling_text_cleanup_20261002/verification.json.

## Horizontal desired-reference input (2026-10-02)

On Real-time control (physical slide 6 / footer 5), keep only the horizontal
desired-reference input arrow into the first summing junction. The Desired
reference rectangle and its vertical connector are removed. Its editable
signal label now reads Desired reference state in regular black Arial 14.5 pt
at (36, 272) pt, in a 158 x 23 pt box, above the unchanged horizontal arrow.
Preserve every other diagram shape, both native equations, notes and speaking
material. The 30-slide deck and full PDF agree, and the standalone diagram's
source and PDF/PNG/SVG/DrawingML assets match. The other 29 slides/pages and
supplementary PDF are unchanged. This supersedes the earlier desired-reference
block and Reference state label requirement. See
experiments/reference_arrow_20261002/verification.json.

## Contact phase heading and directional labels (2026-10-02)

On Contact experiment (physical slide 10 / footer 9, called slide 8 by the
user), introduce the unchanged phase sequence with Experiment phases: as
an editable navy 22 pt bullet, matching the contact-settings heading.
Keep the four existing phase names and arrows in navy 20 pt beneath it.
The heading box is (60, 68, 840, 30) pt and phase box (80, 109, 840, 30) pt.

The four 18 pt navy setting headings read Normal translation (compliant),
Tangential translation (stiff), Rotation about the surface normal (stiff),
and Rotations about the surface tangents (compliant). These directional
labels follow the thesis Contact Establishment design. Preserve all four
native equations, values, positions, the surface figure, notes and speaking
material. The 30-slide structure and all other slides remain unchanged;
the full PDF is synchronized and supplementary PDF is unchanged. See
experiments/contact_phase_labels_20261002/verification.json.

## General CoC introduction and shifted-force cases (2026-10-02)

A new Centre of compliance (CoC) introduction is physical slide 7 / footer 6,
before the existing two-case slide, now physical 8 / footer 7. It defines
the TCP and virtual CoC, shows force f as if applied at p_CoC, the offset
r_c from p_TCP, and the resulting additional moment about TCP. The new native
equation is Delta m = r_c cross f, 22 pt regular Cambria Math. This is the
additional coupling contribution, not the complete rotational-impedance
moment. The physical contact location is not moved by this virtual depiction.

Both Supporting moment and Opposing moment now show f_n at the virtual CoC.
The curved arrows show the resulting moment about TCP, not a second applied
moment. Preserve the supporting counterclockwise and opposing clockwise
directions for the illustrated downward force and left/right displacements.
Use p_CoC (upright CoC subscript) in both cases and throughout the following
Translation-rotation coupling slide, now physical 9 / footer 8: the native
position symbol, displacement equation and inline force-interpretation text.
Keep r_c unchanged. Retain the original tool tilt, surface, normal arrows,
displacement signs and Supporting/Opposing labels.

The active diagrams are presentation-specific coc_force_shift_general and
coc_force_shift_cases, with matching editable TikZ and PDF/PNG/SVG assets.
The historical shared CoC_moment source/assets and thesis files remain intact.
The general and case diagrams deliberately portray virtual-force equivalence;
do not infer unchanged commanded force across different controller settings.

There are now 25 main slides and five hidden backups, 30 total. Conclusion
is physical 25 / footer 24; backups B1-B5 are physical 26-30. Chapter starts
are physical 2, 4, 10, 12, 18 and 25. Native sections, main footers and the
31-entry equation catalog follow this order. All retained notes, speaking
files, videos and other slide bodies remain unchanged. The new notes contain
source information only. The full PDF has 30 pages; the five-page supplementary
PDF is unchanged. This supersedes the earlier force-at-TCP and p_c depiction
on the active CoC slides. See experiments/coc_introduction_20261002/verification.json.

## Compact Cartesian velocity and motor-torque mapping (2026-10-02)

On Real-time control (physical slide 6 / footer 5, referred to by the user
as slide 7), the two bullet headings are Commanded joint torques (motors):
and Jacobian:, including their colons. Keep only tau = J^T(q)F in the
left native equation. Both headings match the existing 22 pt navy style;
the Jacobian heading's stale 20 pt black native override is corrected.
The repeated F = [f; m] definition is removed.
Its caption is Cartesian contribution, since the unchanged diagram adds
model and null-space torques before the motor command tau_cmd.

The right native equation uses x-dot_EE = J(q)q-dot. Its caption identifies
Linear and angular velocity (geometric). Here x-dot_EE is shorthand for
the geometric Cartesian velocity [p-dot_EE; omega_EE]; do not reinterpret
it as derivatives of the roll-pitch-yaw coordinates on the pose slide.
The notation convention is recorded in the equation source, catalog and
alternative description. Both equations remain editable 22 pt regular
Cambria Math with synchronized LaTeX and PDF/PNG/SVG assets.

All native feedback-diagram shapes, arrows, labels, signs, the model and
null-space summation, and the 1 ms cycle statement remain unchanged.
Keep all other slides, 28 other equations, notes, speaking files, videos
and the supplementary PDF unchanged. The deck/full PDF retain 29
slides/pages, five hidden backups and 30 native equations. See
experiments/realtime_velocity_20261002/verification.json.

## Full Cartesian pose and end-effector position (2026-10-02)

On Cartesian pose and surface frame (physical slide 4 / footer 3), write
Cartesian pose of the end-effector (EE) once above the position/orientation
area. Show the native two-row coordinate vector x_EE = [p_EE; eta_EE],
expanded as [(x,y,z)^T; (phi,theta,psi)^T], centred above the split into
Position: 3 translations and Orientation: 3 rotations. Eta_EE denotes the
roll-pitch-yaw coordinates illustrated by the existing orientation diagram.
Retain the native branch lines and the two original diagrams, scaled
proportionally to this new layout.

Use p_EE in the position diagram and in both sides of p_EE = p_EE(q).
Mathematical EE subscripts remain upright without parentheses; standalone
diagram labels remain (EE). The position diagram's editable TikZ and its
PDF/PNG/SVG assets match the embedded image. Preserve its other geometry.
Both revised/new equations use native editable 22 pt regular Cambria Math,
with matching LaTeX, catalog and PDF/PNG/SVG assets. There are now 30 native
equations; the other 28 are unchanged.

Retain the surface-frame figure and definitions, the distinction between
surface-relative gain directions and base-frame calculations, and the
preview of force, moment, stiffness and damping before the controller.
All notes and speaking files remain unchanged. The deck/full PDF still
contain 29 slides/pages, including five hidden backups. The supplementary
PDF and the other 28 slides are unchanged. This supersedes the former
plain p = p(q) notation and fixed sizes/positions on this slide. See
experiments/pose_vector_20261002/verification.json.

## Force and moment before controller errors (2026-10-02)

On Cartesian impedance controller (physical slide 5 / footer 4 after the
pose/surface merge), introduce Force and Moment in the top row, followed by
Positional error and Rotational error with their original diagrams in the
middle row. Cartesian wrench and the decoupling statement remain below.
Use the original editable bullet-heading style. Preserve all five native
equations exactly, at their original dimensions and 22 pt Cambria Math,
and preserve the original diagram assets and proportions. This changes
placement and adds the matching error headings; it does not change the
mathematics, speaker notes or speaking files. The slide is the controller
slide the user referred to by its former number 6. Slide count, numbering,
chapter labels, all other slides and the supplementary PDF are unchanged.
The full PDF matches the reordered slide. See
experiments/controller_force_first_20261002/verification.json.

## Combined Cartesian pose and surface frame (2026-10-02)

The user combined physical slides 4 and 5 into Cartesian pose and surface
frame at physical slide 4 / footer 3. Keep the three original diagrams in
three columns: position, orientation and surface frame. The position figure
is 240 pt wide, the orientation figure 220 pt and the surface figure 266 pt;
all retain their original aspect ratios, asset bytes and editable sources.
Preserve the native p = p(q), n_s and t_1, t_2 equations at 22 pt Cambria Math.
The merged layout supersedes the separate Surface frame slide requirement
and the former Cartesian pose takeaway/equation box positions.

The merged slide introduces force f, moment m, stiffness K and damping D,
leading directly to Cartesian impedance controller at physical 5 / footer 4.
Distinguish the frames: surface axes define force/moment components and the
directions for impedance gains; pose and the evaluated controller equations
use the robot base frame. This follows the thesis's theoretical-background
chapter. Do not claim that the implemented controller wrench is evaluated
only in surface coordinates.

There are 24 main slides and five hidden backups, 29 slides total. Conclusion
is physical 24 / footer 23, and B1-B5 are physical 25-29. Chapter starts are
physical 2, 4, 9, 11, 17 and 24; preserve their existing chapter-label styles.
All other original slides retain their contents, with later main footers and
the native-equation catalog renumbered. There remain 29 native equations and
five embedded videos. Speaking files and all retained speaker notes are
unchanged. The original two slides and notes are archived in
experiments/pose_surface_merge_20261002/archive/original_pose_and_surface.pptx
and its matching PDF. The full PDF has 29 pages; the five-page supplementary
PDF is unchanged. See experiments/pose_surface_merge_20261002/verification.json.

## Visible chapter labels on existing slides (2026-10-02)

The user wants to see the current Overview chapter while advancing through
the existing slides. Keep the top-right chapter label on each main content
slide. Do not insert chapter divider slides. Use the exact six chapter names
and numbers from Overview. On the first content slide of each chapter, the
label is Arial 14 pt bold navy (#17365D); subsequent slides use Arial 12 pt
regular grey (#696969). The editable textbox is at (660, 21) pt with size
261.6 x 24 pt, aligned right and vertically centred above the title rule.

Chapter starts are physical slides 2 (Introduction), 4 (Cartesian controller),
10 (Contact experiments), 12 (Contact results), 18 (Null-space control and
experiments), and 25 (Conclusion and future work). Keep the title slide,
Overview and five hidden backups without this label. The 30-slide structure,
all original slide content and numbering, 29 native equations, five videos,
speaker notes and speaking files remain unchanged. The full PDF includes the
labels; Supplementary_slides.pdf is unchanged. See
experiments/chapter_labels_20261002/verification.json.

## Title photograph and Motivation contact video (2026-10-02)

The robot photograph is back on the title slide, on the right at (592, 103) pt
with width 329.6 pt and its original uncropped aspect ratio. Keep the title
text, university logos and date unchanged. On Motivation, retain Problem and
Idea on the left and the original Contact.mp4 demonstration on the right in
a 400 pt square at (521.6, 75) pt. Preserve its original poster, complete
51.003-second recording, audio, 80% playback volume and click-to-play setting.
This supersedes the earlier requirement to show the photo on Motivation.

The separate Contact demonstration slide was removed at the user's request.
Its original slide, notes and media are archived in
experiments/motivation_video_20261002/archive/removed_contact_demonstration.pptx
and its matching PDF. Do not restore that separate slide automatically.

There are now 25 main slides and five hidden backups, 30 slides total.
Overview is physical slide 3 / footer 2, Conclusion is physical 25 / footer 24,
and B1-B5 occupy physical slides 26-30. All slides formerly at physical 4-31
shift down by one; main footer numbers shift down by one. Backup B labels
and the six Overview chapters are unchanged. In particular, Null-space
controller is physical 18 / footer 17, the two disturbance videos are physical
19-20 / footers 18-19, and Null-space experiment is physical 21 / footer 20.
Keep every retained slide's body, all 29 native equations, all five original
video streams, the retained notes and the speaking files unchanged. The
30-page full PDF matches the edited deck; the five-page supplementary PDF
remains unchanged. See experiments/motivation_video_20261002/verification.json.

## Simple redundancy explanation (2026-10-01)

On Null-space controller (footer 18 / physical slide 19), explain that
the robot's extra degree of freedom allows its posture to change while
keeping the (EE) pose unchanged. Do not restore the full-Jacobian-rank
qualification or the several-joints phrasing in this bullet. Preserve
the minimum-singular-value explanation, all equations, notes and speech.
See experiments/slide18_simple_redundancy_20261001/verification.json.

## Conditioning and minimum singular value (2026-10-01)

On Null-space controller (footer 18 / physical slide 19), the second
conditioning bullet reads: Seeks a larger minimum singular value sigma_min
of J, moving away from singularities. Display sigma_min with a native
Greek sigma and subscript min, matching the metric in the conditioning
plot. Retain the first posture-adjustment bullet and all native equations.
Speaking files and notes remain unchanged. See
experiments/slide18_singular_value_20261001/verification.json.

## Parenthesized end-effector labels (2026-10-01)

Write standalone EE in slide prose and diagram labels as (EE), including
hidden backups. Keep mathematical EE subscripts unchanged. The two pose
diagram sources and their PDF/PNG/SVG assets match the embedded figures.
On Cartesian pose, the takeaway textbox is 630 pt wide and the unchanged
native equation starts at x=715 pt, so the bottom row stays on one line.
Preserve the revised speech and notes. See
experiments/ee_parentheses_20261001/verification.json.

## Null-space condition label (2026-10-01)

On Null-space controller (footer 18 / physical slide 19), retain the
editable label Null-space condition: before J(q) qdot_null = 0. The
label is regular black Cambria Math, 22 pt, matching the adjacent
dimension label. Its box starts at (530, 218) pt, with width 205 pt;
the unchanged native equation starts at (741, 218) pt. The label is
separate from the equation asset. Preserve all equation contents and
the revised speaking material. See
experiments/slide18_nullspace_condition_label_20261001/verification.json.

## Minimal speech alignment after slide edits (2026-10-01)

The user explicitly requested reorganizing the current speech with minimal
wording changes. Only physical sections 19-22 / footers 18-21 changed:
the null-space controller explanation is grouped by the current bullets,
the videos identify no null-space control followed by damping and then
conditioning only, and the experiment introduces the pose hold before
the disturbance and lists conditioning before damping. All four conditions
include the disturbance. The other 27 sections and every equation remain
unchanged. The LaTeX source, both seven-page speaking PDFs, plain-text
copy and PowerPoint spoken notes agree. Preserve the revised speech
during unrelated slide edits. See
experiments/speech_alignment_20261001/verification.json.

## Disturbance video and baseline labels (2026-10-01)

The user identified the first disturbance clip as the sequence without
null-space control followed by damping, and the second as conditioning
only. The captions are Without null-space control → Damping only on
footer 19 / physical slide 20 and Conditioning only on footer 20 /
physical slide 21. This replaces the earlier generic Part 1 / Part 2
caption requirement. Do not infer numerical controller gains. Preserve
the exact clips, 23 s split, audio, posters, dimensions and playback.

On Null-space experiment (footer 21 / physical slide 22), the baseline
condition is Disturbance without null-space control torque, as one
two-line bullet. All four conditions include the commanded disturbance.
Keep the lower settings row at y = 435 pt to allow room for that label.
At the user request, conditioning is top-right at (510, 365) pt and
damping is bottom-left at (60, 435) pt; the baseline and combined
conditions retain their positions. See
experiments/slide21_swap_settings_20261001/verification.json.
Equations, parameter values, speaking files and notes remain unchanged.
See experiments/disturbance_labels_20261001/verification.json.

## Centred contact plots on footer 17 (2026-10-01)

Angular error and interaction wrench (footer 17 / physical slide 18) now uses
three equal landscape plot areas, 224 x 168 pt (4:3). Keep the native Latin
Modern label sizes, recorded data, limits, colours, grids and timing guides.
The 900 x 310 pt figure box is at (30, 135) pt. The three headings start at
107 pt vertically. Keep only the existing middle three-row legend, with
black -40 mm, red TCP, and blue +40 mm labels. Its centre is x = 506 pt,
its top is y = 398 pt, and its natural size is 126.382 x 60.159 pt.
The left and right legend copies were removed at the user request.
Use the unchanged contact_legend_per_plot assets. This supersedes the
three-legend layout; do not restore the duplicates. See
experiments/slide17_single_legend_20261001/verification.json.
This replaces the earlier near-square contact-panel proportions
and fixed placement for this slide only. Preserve the reorganized speaking
text and notes. See experiments/slide17_proportions_20261001/verification.json.

## Results grid follows Figure 5.7 (2026-09-30)

All shared Results plots use the grid of thesis Figure 5.7: light solid
horizontal lines (`gray!25`, `very thin`) and darker densely dotted vertical
lines (`gray!65`, `thin`). Draw them behind the data at the existing major
ticks, preserving limits, values and labels. This applies to every panel of
the contact-wrench and joint-motion figures as well as single-axis plots.
`figures_and_images/sources/results_grid.py` supplies the Matplotlib style;
the native endpoint sources use the equivalent pgfplots settings. Keep this
helper identical to its copies in the thesis figure directory and portable
null-space bundle. Synchronise source assets, embedded PowerPoint images and
both presentation PDFs. See experiments/media_update/results_grid_20260930.json.


## Complete y-axis label match (2026-09-30)

Thesis Figures 5.8--5.11 and their shared presentation figures use LaTeX
with lmodern for the entire axis label, including names, symbols, subscripts
and units. Generate thesis plots at 160 mm width with 10 pt labels, so both
the printed size and optical font faces match Figures 5.4 and 5.6. Preserve
the quantity names and equal joint-motion panels.

The three-panel contact figure uses the full thesis quantity names and Latin
Modern labels on its existing 900 x 310 pt slide canvas. Scale its plot
geometry to that canvas without stretching the label glyphs. Keep the
original recorded data, timing guides, slide headings, legend and picture box.
Both presentation PDFs and the embedded images must reflect the new rendering.
See experiments/media_update/results_ylabels_20260930.json.

## Results figure styling (2026-09-30)

Use thesis Figures 5.4 and 5.6 as the visual reference for the shared main
null-space plots: thin rectangular axis frames, inward ticks, Latin Modern
text and mathematics rendered by LaTeX with lmodern at the final 160 mm
thesis width. Match the actual 10-point optical font faces in both parts of
each axis label; a Latin Modern text font alone does not match its mathematics. Axis labels and ticks print at about
10 pt, with 8 pt legends in the thesis. Keep the four-condition legend below
each figure. Joint motion over time (physical slide 25 / thesis Figure 5.11)
has equal panel widths and heights, aligned titles and axis labels, and the
full 0--4 s interval in both panels. The right panel retains its enlarged
vertical scale. Measured curves, bands, colours, markers and limits are
unchanged. Use the same regenerated PDF/PNG/SVG assets in both documents.

Baseline angular error (B4 / physical slide 30 / thesis Figure 5.4) now has
a blue legend swatch labelled CoC at TCP, r_c,t2 = 0. Preserve its existing
axis style. Update the embedded PowerPoint images, full PDF and supplementary
PDF together. Notes, native equations, videos and slide order are unchanged.
See experiments/media_update/results_figure_style_20260930.json.

## Figure 4.2 frame orientation (2026-09-29)

In thesis Figure 4.2 and Angular quantities (B3 / physical slide 29),
the separate frame inset has n_s upwards and t_2 rightwards. Keep t_1
out of the page and the positive arc from t_2 towards n_s. The main
normal-arrow comparison retains its orientation, angles and labels.
Use the exact updated thesis crop in the embedded PowerPoint figure
and both presentation PDFs. Preserve the image box and text scale.
This replaces the earlier leftward-n_s/upward-t_2 inset instructions.

## Compact Figure 4.2 (2026-09-23)

The three normal arrows in thesis Figure 4.2 and Angular quantities (B3 / physical
slide 29) are 5.4 drawing units long instead of 7.5. Keep the schematic angles,
colours, line styles, descriptions and label sizes. Move both angle arcs, their
labels and the surface-frame inset closer: the red arc radius is 3.6 and the
inner blue radius is 2.1. Use the exact compiled thesis crop and reduce the slide
image's width and height at unchanged text scale, preserving its centre. This
supersedes the older fixed-width and fixed-radius instructions for this figure.
Synchronize both presentation PDFs and editable source copies. See
`experiments/media_update/figure_4_2_compact_20260923.json`.

## All-settings backups B3 and B4 removed (2026-09-22)

Remove Cumulative joint motion: all settings and Jacobian conditioning: all
settings, formerly B3/B4 at physical slides 29/30, at the user's request.
Preserve their original slides and notes in
`experiments/nullspace_narrative/archive/removed_B3_B4_all_settings_20260922.pptx`
and its matching archive PDF. Keep their figure assets, data and generators.
Do not restore these slides automatically.

The active deck now has 26 main slides and five hidden backups, 31 slides in
total. The backups are B1 Opposing moment, B2 Null-space torques and projector,
B3 Angular quantities, B4 Baseline angular error, and B5 Sources of angular
offset, at physical slides 27–31. The full PDF has 31 pages and
Supplementary_slides.pdf has five. Preserve remaining content, notes, videos,
all 29 native equations, speaking files and thesis files. Refresh native
sections, backup footers and the six-chapter Overview. This supersedes the
earlier backup counts and requirements to retain these two all-settings slides.
See `experiments/nullspace_narrative/all_settings_removed_20260922.json`.

## Individual-trials backup B5 removed (2026-09-22)

Remove Joint motion: all individual trials, formerly B5 / physical slide 31,
from the active deck at the user's request. Preserve the original slide and
notes in `experiments/nullspace_narrative/archive/removed_B5_individual_trials_20260922.pptx`
and its matching archive PDF. Keep its figure assets, data and generators.
Do not restore this slide automatically.

The deck now has 26 main slides and seven hidden backups, 33 slides in total.
The backup order is B1 Opposing moment, B2 Null-space torques and projector,
B3 Cumulative joint motion: all settings, B4 Jacobian conditioning: all settings,
B5 Angular quantities, B6 Baseline angular error, and B7 Sources of angular
offset. They occupy physical slides 27–33. The full presentation PDF has
33 pages and Supplementary_slides.pdf has seven. Update backup footers and
native sections, and refresh the six-chapter Overview. Preserve every remaining
slide's content, notes, videos, all 29 native equations, the speaking files and
the thesis. This supersedes earlier backup counts and the requirement to retain
the individual-trials slide below. See
`experiments/nullspace_narrative/individual_trials_removed_20260922.json`.

## Directional displacement metric removed from active deliverables (2026-09-22)

The null-space evaluation in both the thesis and presentation uses only
cumulative projected joint motion (E_N) across all seven joints, minimum
singular value \(\sigma_{\min}\), and measured joint-1 angle change
\(\Delta q_1(t)\). Keep the three-slide presentation sequence Cumulative joint
motion, Jacobian conditioning, and Joint motion over time. Do not restore the
superseded directional-displacement derivation, symbols, plots, backup slides,
speaker-note text, speaking-script sections, figure assets, or generator paths
to any active document. Historical raw records may remain only in the external
experiment archive for provenance.

## Preserve the user's speaking text (2026-09-16)

Keep the current speaking script and PowerPoint speaker notes unchanged until the user explicitly asks for changes. Do not rewrite, shorten, correct, or automatically synchronize the spoken wording during other presentation work. This instruction takes precedence over the earlier narration-editing and synchronization requirements below.

## Copy the backup figures directly from the thesis (2026-09-22)

For Angular quantities (B6 / physical slide 32) and Sources of angular offset (B8 / physical slide 34), use complete figure crops directly from the compiled thesis PDF. Do not reconstruct their diagrams independently. Preserve all labels, arrows, colours and relative geometry. Their current sources are thesis Figure 4.2 on PDF page 79 and Figure 1.1 on PDF page 28. Keep the existing slide figure widths and centres and scale proportionally. Figure 1.1 uses a two-row legend below the geometry: Configured surface and Physical surface, then Desired orientation and Tool face. The Desired orientation swatch is black and dashed. Keep the perpendicular tool tip and both difference arcs. This legend ruling was updated on 2026-09-23 for both the thesis and presentation. The angular figure retains its inner blue arc and existing frame inset.

In Figure 1.1, shorten the red configured surface and blue physical surface so both left and right endpoints share the dashed desired-orientation line's horizontal limits, x = -2.40 and +2.40. Keep the blue surface's 19-degree schematic tilt and all other drawing elements unchanged. Make this shared change in the thesis TikZ source, retain the original canvas, rebuild the thesis, and use that exact compiled rendering in B8. Synchronize source copies and PDF/PNG/SVG assets in both repositories. Keep thesis prose, all speaker notes, speaking files, other slides and slide order unchanged. The deck remains 26 main slides and eight hidden backups. See `experiments/media_update/direct_thesis_backup_figures_20260922.json` and `direct_thesis_backup_figures.py`. This supersedes the independent restoration/export methods below.

## Opposing moment is the first backup (2026-09-22)

Place Opposing moment at B1 / physical slide 27, immediately after Conclusion. Keep it hidden and preserve its complete video, audio, poster, dimensions, click-to-play behaviour and notes. The backup order is now B1 Opposing moment, B2 Null-space torques and projector, B3 Cumulative joint motion: all settings, B4 Jacobian conditioning: all settings, B5 Joint motion: all individual trials, B6 Angular quantities, B7 Baseline angular error, and B8 Sources of angular offset. There remain 26 main slides and eight hidden backups, 34 slides in total. Update backup footers, native section order, the three equation catalog entries on the torque backup, and both presentation PDFs. Keep all slide contents, figure assets, speaking material and the thesis unchanged. This supersedes earlier backup placements below. See `experiments/media_update/opposing_moment_first_20260922.json`.

## Backup demonstration removed and main captions simplified (2026-09-22)

Remove the former hidden B2 Disturbance demonstration / physical slide 28, containing demonstration 1, from the active deck. Preserve its original slide, notes and embedded recording in `experiments/media_update/archive/removed_backup_demo_20260922.pptx` and its matching archive PDF. Source recordings remain unchanged.

The two main Disturbance demonstration slides remain at physical slides 20–21 / footers 19–20. Their captions are now Demonstration · Part 1 and Demonstration · Part 2. Remove the recording identifier 2 and the displayed time ranges from both captions. Preserve the original two clips, exact split at 00:23, playback, audio, poster images, dimensions, titles and notes. Do not remove the part numbers or alter the clips themselves.

There are 26 main slides and eight hidden backups at physical slides 27–34. The full PDF has 34 pages and Supplementary_slides.pdf has eight. B1 is Null-space torques and projector, B2 Cumulative joint motion: all settings, B3 Jacobian conditioning: all settings, B4 Joint motion: all individual trials, B5 Angular quantities, B6 Baseline angular error, B7 Opposing moment, and B8 Sources of angular offset. The restored angular and surface-entry figures are unchanged and have moved only in numbering, from B6/B9 to B5/B8. Keep all 29 native equations, five active embedded videos, remaining speaker notes and speaking files unchanged. Native sections and Overview follow this order. This supersedes the earlier B2 demonstration requirement and backup counts below. See `experiments/media_update/backup_demo_removed_20260922.json`.

## B6 and B9 restored to committed thesis figure designs (2026-09-22)

The user selected the last committed thesis figures as the restoration reference and explicitly requested the same restoration in the presentation and thesis. On Angular quantities (B6 / physical slide 32), use the exact committed `figures/ch04/surface_reference_geometry.pdf` from thesis commit `be7aa4d`. It has the blue angular-error arc inside the red measured-offset arc, at radius 2.8, with its label at (2.70, -0.18). The matching editable source is from `33b7dc5`. The later source-only move to radius 6.3 had not been applied to the committed figure PDF and must not be reapplied. Keep the frame inset with n_s upwards, t_2 rightwards and t_1 out of the page, following the 2026-09-29 update. Preserve the figure width and centre, using proportional scaling.

On Sources of angular offset (now B5 / physical slide 31), use the 2026-09-23 legend below the geometry: Configured surface and Physical surface, then Desired orientation and Tool face. Retain the original black dashed desired-direction datum, perpendicular tool tip, two difference arcs and their labels. The 2026-09-23 legend ruling replaces the earlier three-entry restoration. Match both restored sources and PDF/PNG/SVG assets in the thesis and presentation, and rebuild the two documents. The source/compiled-figure mismatch is resolved in favour of the author-selected committed appearance. Other slide contents, 35-slide order, nine hidden backups, speaking material and thesis prose remain unchanged. See `experiments/media_update/committed_backup_figures_20260922.json`. This supersedes the earlier angular source-only match, rotated inset, and four-entry legend instructions below.

## Redundant null-space backups removed (2026-09-22)

Remove the former B5 Joint motion: mean of three trials, B7 Joint motion: one trial per setting, B8 Net joint motion over time, and B9 Net joint motion from the active presentation. The mean view overlaps the main joint-1 comparison, the single-trial view is contained in the all-individual-trials plot, and the two net-motion views add an unnecessary second motion explanation to the cumulative-motion and joint-1 narrative. Preserve the four original slides, plots and notes in `experiments/nullspace_narrative/archive/removed_nullspace_backups_20260922.pptx` and its matching archive PDF. Retain their source assets and data, but do not restore these slides automatically.

Keep the three useful null-space plot backups: Cumulative joint motion: all settings (B3), Jacobian conditioning: all settings (B4), and Joint motion: all individual trials (B5). The first two extend the main comparison to both conditioning magnitudes, and the third retains trial variation. The other backups are B1 Null-space torques and projector, B2 Disturbance demonstration, B6 Angular quantities, B7 Baseline angular error, B8 Opposing moment, and B9 Sources of angular offset. There are 26 unchanged main slides and nine hidden backups, physical slides 27–35. The full PDF has 35 pages and the supplementary PDF nine. All remaining notes, speaking files, 29 native equations, six embedded videos and thesis files are unchanged. Update backup footers and native sections to this order. These counts and placements supersede earlier records below. See `experiments/nullspace_narrative/backup_cleanup_20260922.json`.

## Simplified controller signal labels (2026-09-22)

On Real-time control (footer 7 / physical slide 8), label the desired signal Reference state, the combined controller input Pose and velocity errors, and the Cartesian feedback Measured state. Define State: pose and velocity once beneath the left feedback line. Keep velocity explicit, since damping acts on velocity error. The combined input is one editable textbox with two lines, Pose and / velocity errors. Preserve all operation blocks, summing circles, signs, parameters, signal connections, the measured q branch, both native equations and the 1 ms cycle statement. This is a presentation-only label simplification. Keep the thesis, speaking script and speaker notes unchanged. Matching diagram PDF/PNG/SVG/DrawingML come from the shared generator. See `experiments/controller_feedback_diagram/verification_20260922.json`.

## Surface-entry figure in backup and thesis (2026-09-22)

The former Motivation diagram is now hidden backup B13, Sources of angular offset, at physical slide 39. Keep Motivation's robot photograph unchanged. The shared diagram and thesis Figure 1.1 explicitly identify four legend entries: Configured surface (solid red), Physical surface (solid blue), Desired orientation (dashed black), and Tool face (solid green). The existing horizontal dashed desired reference remains parallel to the configured surface. Preserve the original object geometry, schematic tilts, tool tip, and both labelled difference arcs. Arrange the four legend entries below the geometry in two rows, with the surfaces in the first row. The previous three-entry legend left the desired reference unnamed and must not be restored.

Keep the thesis source `MyOwn-thesis/figures/ch01/surface_entry_concept.tex` and presentation source `figures_and_images/sources/thesis_figure_1_1_source.tex` identical, with matching PDF/PNG/SVG assets and compiled documents. The earlier presentation assets are archived. The deck has 26 main slides and thirteen hidden backups at physical slides 27–39. The full PDF has 39 pages and the supplementary PDF thirteen. All previous slide contents, speaking files, speaker notes, 29 native equations and six videos remain unchanged. The new backup has blank notes. These counts supersede earlier records below. See `experiments/media_update/surface_entry_correction_20260922.json`.

## Surface image also on Contact experiment (2026-09-21)

Keep the shared surface/tool diagram on both Surface frame (footer 5 / physical slide 6) and Contact experiment (footer 10 / physical slide 11). On Contact experiment, the unchanged `surface_directions.png` image is on the left at 360 pt width, with the existing contact-settings block translated 220 pt to the right. Preserve the process sequence, native equation contents and alignment, numerical values, title, footer and notes. The earlier Surface frame slide and its symbol definitions remain unchanged. This supersedes the instruction to leave Contact experiment without the figure and centre its settings. Only the image is repeated, without adding another symbol glossary. There are still 26 main slides, twelve hidden backups and 29 active native equations. See `experiments/media_update/contact_surface_copy_20260921.json`.

## Plausibility and opposing-moment videos (2026-09-21)

Plausibility experiment is physical slide 12 / footer 11, immediately after Contact experiment and before the Normal-force and Moment plausibility assessment plot slides. It belongs to the Contact experiments section. Opposing moment is hidden backup B12 at physical slide 38. Both videos are embedded, start on click, and appear upright and uncropped in a centred 420 pt square. Preserve their complete recordings and original audio. The source files `Video/Plausibility Experiment.mp4` and `Video/Opposing Moment.mp4` remain unchanged. The presentation copies `Plausibility_experiment_presentation.mp4` and `Opposing_moment_presentation.mp4` normalize rotation into the pixels, retaining all 419 and 311 video frames respectively and copying the AAC audio unchanged. Do not infer numerical controller settings from the recordings.

The deck now has 26 main slides and twelve hidden backups at physical slides 27–38. Conclusion is physical slide 26. The split demonstration 2 is now at physical slides 20–21 before Null-space experiment (22), with the main null-space plots at 23–25. B2, containing demonstration 1, is at physical slide 28. The full PDF has 38 pages and the supplementary PDF twelve. Native sections, Overview, main footers and the 29-entry equation catalog follow this order. Existing slide content, notes, speaking files and earlier embedded videos remain unchanged. The two new slides have empty notes. These positions and counts supersede earlier records below. See `experiments/media_update/contact_videos_20260921.json`.

## Disturbance demonstration 2 before the null-space experiment (2026-09-21)

The second recording from backup B2 is split at exactly 00:23 and introduced in the main sequence immediately before Null-space experiment. Physical slides 19 and 20 (footers 18 and 19) show the two consecutive parts, each centred at its original size and playing independently on click. Their captions identify Demonstration 2, Part 1 / Part 2, and the original intervals 00:00–00:23 / 00:23–end. The embedded files are `Video/Nullspace2_part1_0000-0023.mp4` and `Video/Nullspace2_part2_0023-end.mp4`. All 928 original video frames are retained across the two clips, with the second beginning at original frame 690 / 23.000 s. Audio is retained and re-encoded for the cut. Original source videos remain unchanged. Do not assign unverified controller settings to the recordings.

Null-space controller remains physical slide 18. Null-space experiment is now physical slide 21, the three main null-space result plots are at 22–24, and Conclusion is at 25. The deck has 25 main slides and eleven hidden backups, with B1–B11 at physical slides 26–36. B2 at physical slide 27 retains only demonstration 1, centred at its existing size. The full PDF has 36 pages and the supplementary PDF eleven. Native sections, Overview and the 29-entry equation catalog follow this order. All existing notes and speaking files are unchanged, and the new slides have blank notes. These counts and video placements supersede earlier records below. See `experiments/media_update/nullspace2_split_20260921.json`.

## Main null-space plots shared with the thesis (2026-09-21)

The user limited thesis plot synchronization to the null-space experiment and explicitly selected main presentation plots only. The thesis includes the exact `nullspace_cumulative_main.pdf`, `nullspace_conditioning_main.pdf` and `joint_motion_mean_main.pdf` from current main slides 20–22. Its older combined three-panel null-space figure and individual-trial joint-motion figure are archived and excluded. The comparison uses no torque, damping alone, conditioning alone at k_sigma = 2 N m, and combined control with d_null = 2 N m s/rad. Related null-space descriptions follow these four settings and three-trial means with one sample SD. Other thesis plots, including all contact results, remain unchanged. This supersedes earlier instructions limiting the combined-control main plots to the presentation. Presentation content, speaking text and notes remain unchanged by this thesis-only synchronization. See `experiments/thesis_nullspace_sync/verification_20260921.json`.

## Baseline angular error moves to backup (2026-09-21)

Baseline angular error is now hidden backup B11 at physical slide 34, immediately after Angular quantities (B10, now physical slide 33). Preserve its chart, dimensions, position, data, labels, title and notes. Do not restore it to the main sequence. Update main footers, native sections, Overview and the equation catalog to follow the move. There are now 23 main slides and eleven hidden backups, with Conclusion at physical slide 23 and B1–B11 at physical slides 24–34. The full PDF remains 34 pages and the supplementary PDF contains all eleven backups. Speaking text and speaker notes remain unchanged. These positions and counts supersede the earlier records below.

## Angular quantities matches thesis and moves to backup (2026-09-21)

Angular quantities, formerly footer 10 and then footer 11 / physical slide 12 after the Surface frame insertion, is now hidden backup B10 at physical slide 34. Its diagram uses the exact current thesis LaTeX in `MyOwn-thesis/figures/ch04/surface_reference_geometry.tex`, copied to `figures_and_images/sources/originals/ch04/surface_reference_geometry.tex`. Match the thesis's 12 pt document base and Latin Modern fonts. The frame inset has n_s upwards, t_2 rightwards and t_1 out of the page, following the 2026-09-29 update, with the positive-rotation arc and main angle geometry from the thesis source. This supersedes the older rotated-inset instructions. The existing full thesis PDF and standalone figure PDF contain older renderings, so the current LaTeX source is authoritative for this match. Preserve the image width and centre at (480 pt, 275 pt), scaling proportionally. Keep the removed definition blocks and bottom statements absent. Archive the previous presentation assets and synchronize the local LaTeX, PDF, PNG, SVG and embedded image. The thesis files, speaking script and speaker notes remain unchanged. The presentation now contains 24 main slides and ten hidden backups, with Conclusion at physical slide 24 and B1–B10 at physical slides 25–34. The full PDF has 34 pages and the supplementary PDF has ten pages. This supersedes earlier main/backup counts and Angular quantities placement.

## Robot photograph moved to Motivation (2026-09-21)

The user moved the full `title_robot.jpg` photograph from the title slide to Motivation, replacing thesis Figure 1.1. Do not display this photograph on the title slide. On Motivation, keep the uncropped photograph on the right and the unchanged Problem and Idea text stacked on the left, retaining the existing fonts, bullets and line breaks. Preserve the title slide's text, university logos and date. Retain the unused thesis Figure 1.1 assets for provenance. This supersedes the earlier title-photo placement and Motivation figure layout. Speaking text and speaker notes remain unchanged.

## Surface frame before the controller (2026-09-21)

The user explicitly chose to split the surface-frame material out of Contact experiment. Surface frame is now footer 5 / physical slide 6, immediately after Cartesian pose (footer 4) and before Cartesian impedance controller (now footer 6). It retains the shared tool/surface-frame diagram, Surface-relative compliance heading, and both native normal/tangent symbols and definitions. Contact experiment remains later, now footer 10 / physical slide 11, with its process sequence and four stiffness settings. Centre its retained settings block beneath the process sequence. Do not recombine the two slides. The diagram asset, equations, scientific values and existing speaking material remain unchanged. The new slide has blank speaker notes. All later main footers increase by one. There are now 25 main slides and nine hidden backups, with Conclusion at physical slide 25 and B1–B9 at physical slides 26–34. This supersedes earlier slide-number references and the earlier combined-slide requirement. There are still 29 active native equations and symbols.

## Torque subscript removal (2026-09-21)

On Real-time control, now footer 7 / physical slide 8 (formerly footer 6), show the torque mapping as tau = J^T(q) F, with no cart subscript on tau. Preserve the native equation's other mathematical contents, 22 pt regular black Cambria Math, placement and the rest of the slide. Keep its LaTeX source, alternative description, catalog and PDF/PNG/SVG assets synchronized. Speaking text, speaker notes and the thesis remain unchanged by this presentation-only notation edit.

## Classical feedback diagram on Real-time control (2026-09-21)

Use the thesis Figure 3.2 block-diagram conventions on Real-time control (footer 7 / physical slide 8, formerly footer 6): black rectangular operations, crossed circular summing junctions with explicit signs, labelled signals and orthogonal connections ending at block boundaries. Desired reference and negative measured feedback enter the first junction. Pose and velocity errors enter the impedance controller, with K and D shown as parameter inputs. Its wrench F passes through J^T(q), receiving measured q, to the torque sum. The second positive input collects model and null-space torque terms. The resulting commanded torque drives the robot. Keep the measured-state feedback and its branch explicit. All blocks, labels, circles and connectors are native editable PowerPoint shapes. Retain both unchanged native equations above the diagram, under Joint-torque mapping and Jacobian, and the 1 ms cycle line below. This presentation-only simplification uses the thesis style without modifying the thesis figure. Sources and matching diagram PDF/PNG/SVG/DrawingML are generated by `figures_and_images/sources/make_controller_feedback_diagram.py`. Speaking material stays unchanged. This supersedes the earlier four unboxed stage labels and their disconnected arrows, as well as the previous equation positions on this slide.

## CoC illustration before coupling (2026-09-21)

Introduce the Centre of compliance (CoC) illustration before the Translation–rotation coupling equations. The complete CoC slide is now footer 8 / physical slide 9, immediately after Real-time control. Translation–rotation coupling follows at footer 9 / physical slide 10. Preserve both slides' contents and layouts, including the Supporting moment and Opposing moment panels and the internal introduction-before-definitions order on the coupling slide. Keep both slides in the Cartesian controller section and update the native equation catalog to the new positions. This supersedes the earlier instruction to introduce coupling before the geometric CoC sketch. Speaking text and speaker notes remain unchanged.

## Impedance-reference slide order (2026-09-18)

On Translation–rotation coupling, footer 7 / physical slide 8, introduce the reference-point change before its mathematical definitions. Use Shifting the impedance reference point as the heading, retain the full TCP definition, and identify p_c as Virtual centre of compliance (CoC): new reference. Place Choosing an impedance reference point away from the TCP couples force and moment. and The commanded force acts as if applied at the virtual point p_c. directly below this introduction. Follow them with the displacement definition and the A = Ad(r_c) definition labelled Point-shift adjoint, matching the thesis terminology. Use Displacement from TCP to CoC only on the displacement row and do not repeat TCP → CoC on the adjoint row. Keep the full native wrench matrix below these definitions and the off-diagonal-block result underneath it. Preserve the equation contents and typography, including the italic serif p and subscript c in the moved sentence. Speaking text and speaker notes remain unchanged. This order supersedes the earlier instruction to keep the two moved explanations at the bottom of this slide.

## Controller symbol-key removal (2026-09-16)

On Cartesian impedance controller (footer 5, physical slide 6), keep the four symbol-definition pairs below the decoupling sentence removed: stiffness, damping, linear/angular velocity, and desired/measured indices. Retain the decoupling sentence, headings, controller equations, sketches and footer. This supersedes earlier instructions to retain the compact symbol key. Preserve the unused source assets for provenance and remove only these four active entries from `native_equations.json`. This removal left 31 active native equations and symbols. The later Angular quantities definition removal reduces the current count to 29. Speaking text and notes remain unchanged.

## Shared CoC moment panel labels (2026-09-16)

On Centre of compliance (CoC), footer 8 / physical slide 9, label the two figure panels (a) Supporting moment and (b) Opposing moment. Keep the matching thesis figure labels and editable sources synchronized. Preserve the existing arrows, geometry and symbols. Speaking text and notes remain unchanged.

## CoC slide sentence placement (2026-09-16)

On Centre of compliance (CoC), footer 8 / physical slide 9, omit Opposite displacement reverses the added moment. and Commanded force and moment can change. Move The commanded force acts as if applied at the virtual point p_c. to Translation-rotation coupling, footer 7 / physical slide 8, below its other two result bullets. Preserve the original italic serif p and subscript c. Do not duplicate the moved sentence on slide 8. Keep the shared figure and the frozen speaking material unchanged.

## Angular quantities statement removal (2026-09-16)

On Angular quantities, footer 10 / physical slide 11, remove all three bottom statements: Smaller magnitude means less angular error about the first tangent. Calculated from measured EE orientation and the calibrated tool normal. Positive and negative values indicate opposite tilt directions. Keep the angular diagram and its rotated frame inset unchanged. Also remove both right-hand definition blocks, Measured angular offset / Entry tilt relative to the calibrated surface and Angular error / Tool-normal tilt relative to the calibrated surface, and their two standalone theta symbols, as requested next on 2026-09-16. Preserve the symbols embedded in the shared diagram. Remove only these two active symbol entries from native_equations.json and retain their unused sources. The active native-equation count is now 29. These statements and definition blocks must not be restored on the slide. Speaking text, speaker notes and the thesis remain unchanged by this slide-only removal.

Angular figure placement (2026-09-18): centre the existing figure on Angular quantities, footer 10 / physical slide 11, horizontally on the slide and vertically in the content area between the title and footer. Its centre is at 480 pt horizontally and 275 pt from the slide top. Preserve its size, crop, embedded image, labels, inset and shared thesis assets. Speaking text and notes remain unchanged.

## Validation-slide layout (2026-09-16)

On Normal-force plausibility assessment and Moment plausibility assessment, footers 11 and 12 / physical slides 12 and 13, remove the separate Measured error change lines. Place the unchanged plots above the Manual push / Manual rotation sentence and the unchanged native calculation equation. Keep the two mean-comparison bullets alongside the lower explanation, with clear wrapping and the same result-statement style. Preserve measured values inside equations, plot dimensions, data, units, legends, thesis figures, speaking text and notes. This supersedes the earlier instruction to retain the measured-error labels and place the manual-action sentence and equation above the plot.

Validation quantity summaries (2026-09-18): on Normal-force plausibility assessment and Moment plausibility assessment, footers 11 and 12 / physical slides 12 and 13, show three matching result bullets on the lower right: Quasi-static prediction, Commanded mean, and Model-estimated mean. Put each value on its own continuation line. Force values are −19.65 N, −19.64 N and −22.29 N. Moment values are 1.72 N m, 1.72 N m and 1.85 N m. Omit the previous parenthetical percentage comparisons and calculation wording from these visible summaries. Keep the plots, native equations, manual-action headings, speaking text and notes unchanged. This supersedes the earlier requirement for only two mean-comparison bullets.

Wrench comparison sentence removal (2026-09-18): on Commanded and estimated wrench, footer 13 / physical slide 14, omit both Stationary force difference: 2.32% and Stationary moment difference: 4.87%. Remove the complete sentences, not only their percentages. Preserve the existing plot, its size and position, the title, footer, speaking text and notes.

## Centred validation-slide layout (2026-09-18)

On Normal-force plausibility assessment and Moment plausibility assessment, footers 11 and 12 / physical slides 12 and 13, keep the lower section centred beneath the unchanged plot. The manual-action sentence is centred above the native equation. The three comparisons form one evenly spaced horizontal row below the equation, with each value beneath its label. Use unbulleted, regular 18 pt Arial in black for the manual-action sentence, labels and values on these two slides only. Use 20 pt regular black Cambria Math for these two native equations, preserving their mathematical structures and equals-sign alignment. Their editable LaTeX, catalog entries and PDF/PNG/SVG assets match this size. All other native equations retain 22 pt. On the moment slide, keep each numerical value together with N.m using a nonbreaking space. The native equation uses compact upright N.m and N.m/rad units. Preserve all numerical values, plot dimensions and contents, title and footer styling, speaking text and notes. This supersedes the lower-right bullet layout and the general blue-bullet/22 pt equation rules only for these two lower sections.

Baseline chart-only layout (2026-09-18): on Baseline angular error, footer 14 / physical slide 15, remove the three right-hand notes: Centre of compliance at the TCP, Both larger entry tilts ended closer to zero, and Negative entry error changed sign. Centre the unchanged chart at 480 pt horizontally and 275 pt from the slide top. Preserve its dimensions, bars, values, error bars, axes, labels and shared thesis assets. Keep speaking text and notes unchanged.

Wrench figure centring (2026-09-18): on Commanded and estimated wrench, footer 13 / physical slide 14, centre the existing two-panel figure at 480 pt horizontally and 275 pt from the slide top. Preserve its dimensions, curves, labels, legend, shaded intervals and shared thesis assets. Keep the two removed comparison sentences absent and leave speaking text and notes unchanged. This supersedes the earlier instruction to retain the figure's original position.

Rotational-stiffness sentence removal (2026-09-18): on Effect of rotational stiffness, footer 15 / physical slide 16, omit Angular error increased from 1.75° to 6.58°. Keep the chart and the Resistance to rotation about t1 heading unchanged, including their positions and dimensions. Speaking text, notes and thesis assets remain unchanged.

## CoC-position result layout (2026-09-18)

On Effect of CoC position, footer 16 / physical slide 17, remove the three result statements and the heading Smallest tested error magnitude. Centre the existing chart and its retained native r_c,t2 symbol with the CoC displacement along t2 definition above it. Preserve chart dimensions, data, axes, grid, labels, legend and source assets. Keep speaking text and speaker notes unchanged. This supersedes earlier instructions to retain those result statements.

## Interaction-wrench plot layout (2026-09-18)

On Angular error and interaction wrench, footer 17 / physical slide 18, remove the three result sentences about moment reversal, response timing and final normal force. Use the presentation layout variants contact_wrench_three_panels_balanced and contact_legend_balanced. Give the three plots matching near-square data areas, independently reflowed tick and axis labels, headings centred over their axes, and a compact shared legend centred beneath them. Do not stretch the entire plot image or its lettering. Retain the original shared vector data panels, recorded values, limits, units, colours and timing annotations. These are presentation composition variants, with the original assets and thesis figure retained. Keep speaking text and speaker notes unchanged.

## Null-space explanation and bullet hierarchy (2026-09-18)

On Null-space controller, footer 18 / physical slide 19, use Redundant direction: and Primary Cartesian task: as the two introductory headings. Explain that there is one null-space direction at full Jacobian rank, several joints move together, and null-space motion preserves the instantaneous EE motion. Follow with Damping torque and Conditioning torque, retaining their native torque symbols and placing a colon after each complete heading. Remove bullets from all four headings and place native round navy bullets on the explanations below them, with 20 pt regular Arial body text and 20 pt hanging indents. State that damping opposes and damps null-space velocity, while conditioning adjusts the joint configuration to improve Jacobian conditioning. Keep the short singularity consequences, both native kinematic equations, and the full-rank qualification. Do not describe conditioning as tracking a prescribed null-space position. Preserve native mathematical contents and typography, speaking text and speaker notes. This supersedes the earlier bullet-heading style and wording on this slide only.

## Null-space plot consistency and table-slide removal (2026-09-18)

Remove Effect of conditioning torque, formerly footer 23 / physical slide 24. Retain its archived slide, notes and source values for provenance, but do not restore it to the active deck. Conclusion becomes footer 23 / physical slide 24. The deck now has 24 main slides and nine hidden backups at physical slides 25–33, and the full PDF has 33 pages. The nine-page supplementary PDF and all remaining speaking text and notes stay unchanged.

On Joint motion over time, footer 22 / physical slide 23, both panels use the identical y-axis label Joint 1 Motion, Delta q_1 [degrees]. Panel (b) shows the full 0–4 s interval with all original common recorded samples and the complete one-sample-SD bands. Remove First second from its title. Match the colours, solid lines, line widths, marker shapes and sizes to Jacobian conditioning, footer 21 / physical slide 22, using spaced markers rather than a marker on every sample. Remove (SI) from the combined-control legend on footers 21 and 22. Preserve data, limits on the full-range panel, uncertainty calculations, other slide content, the shared thesis figures and six-setting backup assets. Regenerate these presentation-only main plots with make_nullspace_narrative.py --only conditioning joint. This supersedes the former first-second main-panel view and instruction to retain the conditioning-torque table.

Cumulative-motion percentage comparisons (2026-09-18): on Cumulative joint motion, footer 20 / physical slide 21, replace the two absolute-value comparisons with: Damping alone reduced cumulative motion by 25.1% compared with no torque. At 2 N m, adding damping to conditioning reduced cumulative motion by 50.7%. Calculate each reduction as 100 times (1 minus comparison mean divided by reference mean), using the full-precision three-trial cumulative means in nullspace_narrative_analysis.json. The first reference is no null-space torque, and the second is conditioning alone at 2 N m. Preserve the existing plot and its assets, regular 20 pt Arial, native navy bullets, textbox positions, speaking script and speaker notes.

Null-space experiment parameter symbols (2026-09-18): on Null-space experiment, footer 19 / physical slide 20, show the conditioning value as k_sigma = 2 N m and the damping value as d_null = 2 N m s/rad, including both symbols in the combined setting. Use italic Cambria Math k and d with a mathematical sigma subscript and an upright null subscript. These are editable inline text symbols with a 22 pt base, 15.4 pt subscripts and a -25 percent subscript baseline. Preserve the existing 20 pt Arial wording, values, units, native navy bullets, positions, combined-setting line break, disturbance equation, speaking text and notes. No standalone equation entry or figure asset is added.

## Conclusion wording follows the speaking text (2026-09-18)

On Conclusion, footer 23 / physical slide 24, retain four conclusion sentences and two future-work sentences. Use: Compliant rotation allowed contact moments to reduce angular error. Higher rotational stiffness left a larger angular error. The CoC could support or oppose the contact moment. Null-space control reduced redundant motion under disturbance. Under Future work, use: Use a more rigid tool mount for better measurements. Adapt the CoC to support the contact moment, then return it to the TCP after alignment. Retain the regular 22 pt Arial treatment and native navy bullets. The final point has one continuation line after the comma, not a second bullet or sentence. This visible-slide wording follows the user's closing speech while preserving the qualification against guaranteed perfect alignment. Keep the speaking script and speaker notes unchanged. These sentences supersede the earlier visible Conclusion wording.

## Repository locations

Verified on 2026-09-07.

| Repository | Local path | GitHub remote | Purpose |
| --- | --- | --- | --- |
| Presentation_new | `C:\Users\USER\Desktop\Presentation_new` | https://github.com/heykel95-lab/Presentation_new.git | Defense presentation and speaking script |
| MyOwn | `C:\Users\USER\Desktop\MyOwn` | https://github.com/heykel95-lab/MyOwn.git | The user's thesis LaTeX repository |
| Thesis_Final_Control | `C:\Users\USER\Desktop\Thesis_Final_Control` | https://github.com/heykel95-lab/Thesis_Final_Control.git | Final controller, experiments, analysis, and figures |

The thesis entry point is `C:\Users\USER\Desktop\MyOwn\Thesis.tex`; its compiled document is `C:\Users\USER\Desktop\MyOwn\Thesis.pdf`. Consult `chapters`, `figures`, and `code` for supporting material.

The control repository contains `surface_grinding_controller`, `experiments`, `analysis`, and `figures`. Use these sources when checking implementation details or experimental results. Read each repository's own instructions before making changes there.

## Active files and theme

- Keep shared plots and figures synchronized with the thesis by default. A change to their geometry, data, uncertainty, symbols, labels, axes, tick orientation, limits, grid or visual conventions must be applied to the corresponding sources and generators in both repositories in the same task. Update the rendered assets and both compiled documents, then inspect the affected slide and thesis page. This includes the symmetric tool figure, angular-error illustration and result plots. Respect any explicit instruction limiting a change to one document. Check the existing files first so an already synchronized figure is not rebuilt unnecessarily.
- Edit `Final Presentation\Thesis_Defense_gg0_v3.pptx` and regenerate the matching PDF in that folder.
- Keep all final PDFs directly under `C:\Users\USER\Desktop\Presentation_new\Final Presentation`.
- Other folders (`Final`, `gg0`, `good1`, `good2`, `one`, `two`) are earlier versions, not the active deck.
- Preserve the existing dark blue `#17365D`, Arial body text, white background, continuous title rule, small HM logo, and footer. All standalone native equations and mathematical symbol keys use 22 pt Cambria Math, regular weight and black, with normal mathematical subscript/superscript scaling.
- Use native round navy bullets for blue subsection and parameter headings, including Future work. Match the existing controller-heading bullet style: Arial, 80 percent bullet size, and a 20 pt hanging indent. Preserve heading text positions by extending the textbox 20 pt to the left and increasing its left paragraph margin by 20 pt. Keep the existing centered alignment for paired figure headings and preserve the equation/figure positions. Main slide titles, Overview chapter numbers, diagram-node labels, figure legends and video cues retain their own styles.
- Align vertically related equations at the equals signs within each column or equation group, using the actual glyph positions using native equation placement. Keep paired columns symmetric and retain consistent spacing. This includes the Cartesian error/wrench equations, the compact CoC stiffness and damping transformations, null-space equations, contact settings, and null-space kinematics. Preserve equation contents and native mathematical structures.
- Format result statements and figure takeaways consistently: regular 20 pt Arial in `#141414`, native round bullets in the theme blue `#17365D`, a 20 pt hanging indent, and 1.1 line spacing. Apply this to normal-force evidence, null-space findings and qualifications, and backup result statements as well. Do not leave one finding as a smaller unbulleted footnote or emphasize isolated results with bold text. Conclusion and Future work bullets share the same treatment at 22 pt. Keep headings, symbol definitions, figure legends, and video cues in their own established styles.
- Use descriptive slide titles rather than questions. The measurement slide is titled `Angular quantities`.
- Do not use the words "gain" or "gains" in slides, figure labels, speaking text, or speaker notes. Use stiffness, damping, matrices, coefficients, or settings according to the quantity being described.
- Use concise statements and short parallel phrases in the style of the Conclusion from commit 558d22e. Do not use semicolons in audience-facing slide text, speaking text, or notes. Split ideas into short sentences or join them naturally with words.
- Use formal academic wording and actual experimental results, without invented numerical examples. Avoid "inferred" / "infered" and the adjective "signed" in audience-facing material. Preserve positive/negative angle conventions. Describe the angular quantities as calculated from measured end-effector orientation.
- Use rotations/rotation for the rotational compliance directions, as requested. Keep the title slide labelled Presentation and its date blue.
- Introduce abbreviations as the full term followed by the abbreviation in parentheses, such as end effector (EE), in slides, speaking text, and notes. Use the abbreviation after it has been defined.

## Current structure and automatic Overview maintenance

The Overview is a single slide listing only six chapter names: Introduction, Cartesian controller, Contact experiments, Contact results, Null-space control and experiments, and Conclusion and future work. Do not restore individual slide titles, a second Overview page, or the word continued.

The presentation uses native PowerPoint sections for these chapters. Introduction contains the title, Motivation, Contact demonstration, and Overview. Cartesian controller contains Cartesian pose, Surface frame, and the controller material through Translation–rotation coupling, with the Centre of compliance (CoC) illustration immediately before coupling. Contact experiments contains Contact experiment and the three consistency checks. Contact results contains Effect of rotational stiffness through Angular error and interaction wrench. Null-space control and experiments contains physical slides 18–22. Conclusion and future work contains Conclusion at physical slide 23. A separate Backup section holds B1–B11, including Angular quantities at B10 and Baseline angular error at B11, and is omitted from Overview.

Use one column of 22 pt Arial, with right-aligned dark-blue numbers in a fixed-width column and consistent row spacing. Run `Final Presentation/Speaking/build/update-overview.ps1` after each presentation edit, or its portable XML equivalent in `experiments/nullspace_narrative/restructure_presentation.py` when PowerShell is unavailable. Both derive the six chapter rows from native PowerPoint sections and exclude Backup. Maintain chapter assignments when adding or moving slides.

The user approved the following narrative on 2026-09-16, with the conditioning-torque table removed on 2026-09-18, the Surface frame introduction split out, the CoC illustration moved before coupling, and Angular quantities and Baseline angular error moved to backup on 2026-09-21. It supersedes earlier slide orders and backup counts. The deck has **23 main slides and 11 hidden backups**:

1. Master Thesis Presentation
2. Motivation
3. Contact demonstration
4. Overview
5. Cartesian pose
6. Surface frame
7. Cartesian impedance controller
8. Real-time control
9. Centre of compliance (CoC)
10. Translation–rotation coupling
11. Contact experiment
12. Normal-force plausibility assessment
13. Moment plausibility assessment
14. Commanded and estimated wrench
15. Effect of rotational stiffness
16. Effect of CoC position
17. Angular error and interaction wrench
18. Null-space controller
19. Null-space experiment
20. Cumulative joint motion
21. Jacobian conditioning
22. Joint motion over time
23. Conclusion
24. Null-space torques and projector (B1)
25. Disturbance demonstration (B2)
26. Cumulative joint motion: all settings (B3)
27. Jacobian conditioning: all settings (B4)
28. Joint motion: mean of three trials (B5)
29. Joint motion: all individual trials (B6)
30. Joint motion: one trial per setting (B7)
31. Net joint motion over time (B8)
32. Net joint motion (B9)
33. Angular quantities (B10)
34. Baseline angular error (B11)

The full presentation PDF includes **all 34 slides**. Keep B1–B11 hidden in the PowerPoint slideshow at physical slides 24–34. For PowerPoint SaveAs PDF, temporarily unhide all eleven backups in memory, export, and close without saving those visibility changes. `Supplementary_slides.pdf` contains physical pages 24–34, giving eleven pages. Main footer numbers are one lower than physical slide indices. The title slide retains its original furniture and no added number.

The main null-space story holds enabled settings fixed at k_sigma = 2 N m and d_null = 2 N m s/rad: no torque, damping alone, conditioning alone, then combined. Its three plots show cumulative motion, Jacobian conditioning and the mean joint-1 history with one sample SD, followed directly by Conclusion. The former conditioning-torque comparison table is archived and omitted from the active deck. Its source values remain 0.29° and 0.19° at 1.5, then 1.69° and 0.83° at 2. Explain that near-zero net motion can coexist with repeated reversals. Keep all seven complete six-setting views in B3–B9. The original four-setting thesis figures remain unchanged because this extension is presentation-only.

Rebuild the complete six-setting figures with `figures_and_images/sources/make_combined_nullspace.py`, then the main subset with `make_nullspace_narrative.py`. See `experiments/nullspace_narrative/README.md` for deck rebuilding and validation. The older `experiments/h_mode_combined/update_presentation.py` restores the superseded 30-slide structure and must not be run directly on the active narrative.

The introduction shows Contact demonstration immediately after Motivation, followed by Overview. The presentation then introduces the Cartesian controller, contact experiments, validation and contact results. Null-space theory, experiment and results form a separate block after the contact results. The consistency checks proceed in this order: normal-force plausibility, moment plausibility, commanded and estimated wrench. All three use TCP-centred configurations where described in the thesis. Main results proceed through rotational stiffness, CoC location, angular-error/wrench traces, null-space damping, and Jacobian conditioning. Baseline angular error is retained in backup B11.

Above the normal-force and moment plausibility plots, retain the short manual-push heading with about 20 mm, the manual-rotation heading, and the measured rotational error change of 6.565 degrees. Remove the visible setup lines `Along the surface normal`, `Fixed pose reference · CoC at TCP`, and `Normal push held · Fixed pose reference`. Do not restore them. Keep their scientific details in the speaking text and notes. The normal push is about 20 mm (2 cm), not 2 mm. The measured EE movement is +19.650 mm along the surface normal, giving a normal position-error change of -19.650 mm because the controller uses desired minus measured position. The moment test manually rotates the tool about surface tangent t1 while retaining the normal push. Label 6.565 degrees as the measured rotational error change relative to the loaded baseline, not as a commanded angle or a physical rotation direction. Both checks keep the captured desired position and orientation fixed, with CoC at TCP. Keep the existing plots and equation dimensions, with the remaining setup headings and measured error on the left and the equation on the right above each plot. Introduce these actions first in the speaking bullets and notes. Sources: MyOwn chapters 04 and 05, professoremail/T_MODE_MANUAL_D_REPEAT_PROTOCOL.md, analyse_t_mode_consistency.py and T_MODE_MANUAL_D_REPEAT_r01_controller_log.csv. These validation displacements are separate from the removed null-space position-error subplot and its former 2 mm criterion. On Commanded and estimated wrench (physical slide 14, footer 13), omit the Separate trial during contact establishment bullet, as requested on 2026-09-15. Its stationary force and moment comparisons come from a separate TCP-centred contact trial, not the preceding manual perturbations. Keep that transition clear in the narration.

Motivation explains why surface grinding needs an aligned tool face, while the configured and physical surface orientations have an unknown mismatch because exact matching cannot be assured in practice. Present Problem and Idea below the wide thesis Figure 1.1, Sources of angular offset at surface entry. Use the exact thesis figure in `Final Presentation/figures_and_images/thesis_figure_1_1.pdf` with matching PNG/SVG assets and archived source. The figure replaces the earlier robot photograph on Motivation, as requested on 2026-09-16. Keep both source images available for provenance. Keep the three Idea bullets in causal order: Cartesian impedance makes position and rotation compliant. Pressing a tilted tool creates a contact moment. Rotational compliance allows the tool to turn towards alignment. Do not restore the removed Main thesis question heading or its question on this slide or in its narration. Explain that compliance permits rotation in response to contact moments, while the rotational spring and damper remain active. Do not describe compliance as creating the contact moment. Keep the slide title Motivation. The older contact-rig sketch and robot photograph remain source assets but are not displayed on Motivation. Do not revert to edge-first contact or rigid tracking as the primary problem statement. Describe motion towards alignment without claiming that perfect physical alignment is guaranteed.

The `Cartesian pose` slide follows Overview immediately (physical slide 5, footer 4). The user removed both introductory definition sentences on 2026-09-16. Keep the Pose scope textbox and those two bullets off this slide. Preserve the remaining headings, figures, equation and takeaway. This visible-slide edit does not authorize changes to the speaking script or speaker notes. Use balanced position and orientation columns, showing x, y, z and roll phi, pitch theta, yaw psi with the two original schematic illustrations. Both figures use the identical solid 3D two-finger gripper defined in figures_and_images/sources/pose_gripper.tikz at the EE origin. Keep the fingers pointing downward and turn the front towards the right through a further positive rotation about z (+110 degrees total in the illustrative drawing). Use one continuous opaque filled body with light depth shading and no internal edge strokes. Do not restore separate outlined finger, palm or wrist boxes or the transparent wireframe. The position illustration includes a schematic chain of five circular joints connected by thin links from the base-frame origin to the gripper wrist; keep this line-and-circle style rather than solid shaded tubes. Fan the link inclinations out steadily, at roughly 74, 68, 54 and 26 degrees above the horizontal and then about 20 degrees below it, so no run of links looks straight and the last one drops onto the wrist. Cut the links square at the origin and draw no circle there, so the base frame stays visible, and route the chain between the z axis and the position vector, letting it rise to a peak at the second-to-last joint and descend from there onto the wrist so the last joint circle rests tangentially on the gripper and no joint circle overlaps an axis, the vector p or a projection line. Retain the separate position vector p and coordinate projections. Apply the yaw before the same reference-axis projection to keep its direction consistent. Use smooth rotation arcs with tangent-aligned arrowheads following the right-hand rule: +x sends y toward z, +y sends z toward x, and +z sends x toward y. Draw each rotation arc as a closed ring around its axis: plot it as a finely sampled polyline rather than a smoothed curve so the arrow tip stays exactly tangent, keep the ring radius well above the arrowhead length, and split the ring where it crosses its own axis so the far half is drawn before the axes and the near half after them over a white casing. Keep the rings and their labels clear of the axis tips and of the gripper. For pitch, terminate the visible curve at the exact centre of the triangular arrowhead base and extend the triangle forwards along the endpoint tangent. Do not centre the triangle on a later point of the circular path, which makes the shaft meet its base off-centre. Keep the existing roll and yaw arrows unchanged. Avoid path-shortening end arrows, which produced hooked tips. The orientation axes start at EE; keep the gripper geometry and rendering scale identical. Compile these two LaTeX figures with figures_and_images/sources as the working directory so the shared gripper input resolves. The position figure places it at the end of p, and the orientation figure places it at the rotation-frame origin. Center Position: 3 translations and Orientation: 3 rotations directly above their respective figures, on the same horizontal baseline, in theme blue #17365D and 22 pt Arial. Use End effector (EE) on this introductory slide, with EE labelling the position sketch; do not use TCP here. Label the axes Reference base frame and state that the pose is expressed relative to the robot base frame. State that the EE position depends on the configuration of all 7 joint angles, p = p(q), with q collecting the seven joint angles. Render p = p(q) using the same LaTeX serif equation style as the controller equations, not inline Cambria Math; the narration identifies forward kinematics and also notes the orientation dependence. These are introductory pose coordinates; the controller uses a rotation matrix. The notes distinguish the roll symbol from the later axis-angle error angle and specify R = R_z(psi) R_y(theta) R_x(phi). Preserve the editable LaTeX sources and matching PDF/PNG/SVG variants. This separate introduction does not restore the removed pose-frame illustration on the controller slide.

On `Cartesian impedance controller` (footer 5, physical slide 6), the main message is position correction by force and orientation correction by moment. Use Positional error and Rotational error as the two balanced navy bullet headings. Align the first visible e_p and e_R glyphs with their heading text (after the hanging bullet indent), shifting each complete equation group together to preserve equals-sign alignment. Add a matching third bullet heading, Cartesian wrench, above the matrix equation; align the first F glyph with that heading text. Reuse the former scope-line space for the two upper groups rather than retaining a redundant scope sentence. Remove the redundant Desired / measured label row and its standalone reference-symbol pairs; the desired and measured quantities remain in the pose-error equations and compact symbol key. Show the position error and rotational correction in the balanced columns, then combine the force and moment spring-damper laws into one full-width block-matrix wrench equation. Underbraces identify K_c = [K_p, 0; 0, K_R] and D_c = [D_p, 0; 0, D_R]. Each is 6 by 6 with 3 by 3 blocks. Show the zero off-diagonal blocks and state that translation and rotation are decoupled in this form. Keep the actual linear/angular velocity differences; do not replace the angular velocity difference with the derivative of the finite axis-angle error. Retain the separate force equation directly below e_p and the separate moment equation directly below e_R, with equals signs aligned within each column. The combined block wrench follows underneath and remains unchanged. Preserve the compact symbol key and explain matrix dimensions in the narration. Do not mention CoC or CoC at TCP on this introductory slide or in its narration, because the centre of compliance is introduced later. Keep the compact symbol key below. The former End-effector pose representation backup has been removed at the user's request. Do not restore it. Do not restore the removed pose-frame illustration. `Real-time control` (physical slide 7, footer 6) introduces joint-torque commands before the feedback loop. Place the navy Joint-torque commands from Cartesian wrench heading and the unchanged F = [f; m], tau_cart = J^T(q) F equation above the loop. The four steps are Pose error / Wrench / Commanded joint torques / Robot, with Commanded joint torques on two centered lines. Keep Measured pose feedback. The implementation line reads Real-time control with a 1 ms cycle, as requested on 2026-09-16. Keep C++ and libfranka off this slide. This visible-text change does not authorize changes to the speaking script or speaker notes. The narration identifies joint torques as the robot command and tau_cart as the Cartesian contribution. Below the torque equation, retain the Jacobian label and show the native editable equation [p_dot_EE; omega_EE] = J(q) q_dot in place of the verbal joint-velocity-to-EE-velocity mapping, as requested on 2026-09-16. The matrix depends on joint angles, but does not map joint angles directly to velocities. Repeat this mapping briefly in the backup Jacobian key. Explain that the complete command also includes model compensation and enabled null-space terms, without adding the full torque-command equation to the slide.

Introduce `Translation–rotation coupling` before the geometric `Centre of compliance (CoC)` sketch, at footers 7 and 8 respectively. The transformation slide begins with the navy Impedance reference point heading. Introduce Tool centre point (TCP): controlled reference point on the EE before defining the virtual CoC. Define p_c as the virtual centre of compliance (CoC) position and r_c = p_c - p_TCP as the displacement from TCP to CoC before A = Ad(r_c). Label A with Impedance reference: TCP → CoC. Left-align the Displacement from TCP to CoC and Impedance reference: TCP → CoC descriptions at the same horizontal position. The shift concerns the reference point of the whole impedance model. Keep the small-rotation qualification in narration. Do not restore the Error at the CoC and Wrench at the TCP headings or their standalone e_c = A e and F_TCP = A^T F_c equations. Keep expanded point-shift matrices, the redundant S definition, and the removed local-model label off the slide. Show the full matrix wrench law beneath the impedance-reference definitions, using the same force/moment, error and velocity columns as footer 5. Underbrace A^T [K_p, 0; 0, K_R] A as K_TCP and A^T [D_p, 0; 0, D_R] A as D_TCP. These replace the separate Stiffness/Damping headings and compact transformation equations. Retain the non-zero off-diagonal K/D blocks result bullet and the requested reference-point explanation: Choosing an impedance reference point away from the TCP couples force and moment. Remove the bullet CoC displacement links the commanded force f and moment m., as requested on 2026-09-16. Place the remaining reference-point explanation directly below the off-diagonal-blocks bullet. Keep the full tool centre point (TCP) definition above. This slide-only addition leaves the speaking script and speaker notes unchanged. Moving the virtual CoC changes the impedance law and may change both commanded force and moment. Re-expressing the same wrench at another point instead leaves its force unchanged and changes its moment by the lever-arm term. Keep these operations distinct.

`Null-space controller` (footer 18, physical slide 19) opens the separate null-space block after the contact results. Keep the removed arm-disturbance purpose sentence off this slide. Use four matching native navy bullet headings in regular 22 pt Arial: Redundancy and Cartesian task preservation above the two introductory paragraphs, then Damping and Conditioning above their explanations. Keep the upper headings aligned, the paragraphs indented with the heading text, and the equations directly below the paragraphs. Shift the torque symbols with the heading text so their spacing remains unchanged. Place the redundancy equation below its left explanatory text and J(q) qdot_null = 0 below its right explanatory text. Keep Damping and Conditioning as aligned headings with qualitative explanations below. Append the torque symbols tau_d and tau_sigma respectively, using the same LaTeX serif equation style and navy heading colour. These are symbols only; do not restore the full torque formulas. Do not show the specific tau_d, tau_sigma, N_tau, or total null-space torque equations on this main slide; the user removed them. Show J(q) qdot_null = 0 as an instantaneous kinematic relation and 7 - 6 = 1 with the full-rank qualification. Several joints generally move together. Define a singularity through its physical consequence: the EE loses at least one instantaneous motion direction. Add that near a singularity some EE motions need very large joint velocities. Keep the Jacobian rank-loss definition and the resulting tracking/velocity-limit difficulty in the short narration. Damping opposes redundant joint velocity. Explain conditioning with the two short visible lines: Seeks easier motion in the weakest tool direction. Can initiate joint motion. The narration connects this active objective to seeking better local Jacobian conditioning. Do not describe conditioning as damping or promise global singularity avoidance. The former Null-space kinematics backup has been removed at the user's request. Do not restore it. The hidden backup Null-space torques and projector (B1, physical slide 26) defines N_tau = I_7 - J^T J^{+T}, tau_null = tau_d + tau_sigma, tau_d = -d_null N_tau qdot, and tau_sigma = k_sigma N_tau(s_sigma v_7). Reuse the matching null_controller equation assets. Define the pseudoinverse and identity matrix, damping coefficient, measured joint velocity, conditioning torque magnitude, unit null-space direction, and direction selector. The selector compares the minimum singular values at q plus or minus alpha_probe v_7 and is zero within the deadband. Keep this derivation in the backup and retain the qualitative main controller slide. This backup precedes the hidden Disturbance demonstration video, B2.

The combined `Contact experiment` slide (physical slide 11, footer 10) replaces the former separate Surface-relative compliance and Contact experiment slides. Keep the process sequence across the top, the original surface-frame sketch and compact normal/tangent definitions on the left, and the four common contact stiffness rows on the right. The qualitative compliance explanation remains in the narration. Do not restore the Controlled comparisons heading, Cases A–D list, or the removed planar-contact/tool-dimensions/reference-duration sentence on this slide. The `Contact experiment` parameter rows appear in this order, each with its blue directional label: Normal translation (K_p,n), Tangential translation (K_p,t1 = K_p,t2), Rotation about the surface normal (K_R,n), then Rotations about the surface tangents (K_R,t1 = K_R,t2). Move each label together with its equation, retaining the equation sizes and equals-sign alignment. The narration follows this order. The process sequence at the top reads Tool orientation, Surface approach, Contact establishment, and Surface grinding. Keep Surface grinding as the final label. The narration identifies this process sequence and states that the presented contact experiments evaluate the five-second Contact Establishment phase. `Contact experiment` introduces the planar contact, approach and five-second contact-establishment phase, common contact settings, and the surface-relative compliance directions. Common contact settings are K_p,n = 350 N/m, K_R,t1 = K_R,t2 = 5 N m/rad, K_p,t1 = K_p,t2 = 2000 N/m, with inertia-scaled damping factor zeta = 1. Case C varies translational stiffness along t2 while t1 remains fixed. Do not claim a separately measured t1 stiffness effect.

`Null-space experiment` (physical slide 20, footer 19) follows Null-space controller and introduces the repeatable internally commanded disturbance, implemented as the joint-torque equivalent of a virtual 20 N point force on link 3, and the Cartesian pose hold. State that conditioning is active for 5 s before disturbance onset. The selected null-space law remains active during the disturbance, so conditioning can already alter the entry configuration during settling. Identify the measured quantities as Total motion, conditioning and net joint motion. State Disturbance interval: 5–9 s, displayed as 0–4 s. Keep this slide focused on the commanded pose hold and the redundant-motion comparison. Do not include a position-error criterion or claim measured full-pose retention. Keep the null-space experiment in its separate block after the contact results.

Conclusion combines the user's earlier presentation ideas with MyOwn/chapters/07_conclusion.tex in concise, parallel statements. Keep one slide with four regular 22 pt Arial findings at the 72 pt left margin: Contact reduced angular error for the larger entry tilts. Higher rotational stiffness left a larger angular error. CoC displacement changes the angular error. Combined damping and conditioning reduced redundant motion. Place these at 83, 133, 183 and 233 pt with 34 pt text-box heights. The tangential-stiffness result has been removed from the presentation and conclusion. Preserve the 22 pt font and native hanging bullets. The navy Future work heading is at 297 pt with no rule underneath. Two matching bullets at 338 and 378 pt cover a more rigid tool mount and adaptive CoC selection with return to the TCP after alignment. The user removed the damping and conditioning under physical disturbance future-work proposal. Do not restore it in the slide or narration. Keep the short writing style and avoid semicolons. Do not show axis symbols such as t2 on the Conclusion slide or in its Future work bullets. Retain directional qualifications in the narration using plain words. Do not restore the direct-angle-measurement or sustained-grinding future-work item. The narration gives the recalculated final-error effects, explains the neutral TCP reference and active rotational spring-damper, qualifies the calibration-based physical-alignment estimate, and identifies a more rigid mount and adaptive CoC as future work. Frame the null-space conclusion around the disturbance response. Damping reduced cumulative joint motion and conditioning countered the disturbance effect in the tested direction, leaving near-zero net joint motion. Distinguish conditioning from damping and retain the qualification that small net joint motion can coexist with back-and-forth motion. Retain the explanation of the observed back-and-forth motion in the results narration. Do not add an unmeasured talk duration.

## Scientific figure and interpretation rules

Contact metric update (2026-09-15): all 69 contact trials have original terminal-report normal-error endpoints at 0.01-degree precision. Three representative trials also have full time histories. Endpoint plots use three-trial means and one sample standard deviation of those reported endpoints. Do not invent extra endpoint precision or interpret repeated rounded values as zero measurement uncertainty. The reproducible calculation, source hashes, data tables and full-3D validation are stored in MyOwn/code/python/figures/contact_angular_error/.

Avoid duplicate axis glossaries around result figures, including backups. Retain short stiffness headings with physical directional descriptions and the `r_c,t2` CoC displacement definition. The user removed the `est: robot's model-based estimate` line from the contact-response and interaction-moment slide; keep that explanation in the speaking text and notes. Preserve figure axes, legends, units, data, and uncertainty information.

Use measured pose-based entry-offset notation `theta_meas,t1`. The baseline horizontal axis is Measured Angular Offset, with 0.69, 9.31 and -9.41 degrees. The main contact metric is now final angular error `theta_err,t1(t_end)` relative to the calibrated surface normal. The three baseline mean final components are 1.65, 1.75 and 1.41 degrees. Both larger entry tilts have smaller final error magnitude, and the negative entry error changes sign. The nominal-zero component increases. Rotational stiffness 5, 15 and 50 N m/rad gives final errors 1.75, 2.04 and 6.58 degrees. Case-D legends retain the across-setting entry means +9.33 and -9.38 degrees. Its lowest tested final-error magnitude is 0.83 degrees at +100 mm for positive entry tilt and 0.94 degrees at +10 mm for negative entry tilt. More rotation can carry the error component through zero and increase its magnitude. Do not restore gamma-based response values or their old percentage comparisons. Sources: MyOwn/code/python/figures/contact_angular_error, chapters/04_experimental_setup_and_evaluation.tex, chapters/05_results_and_discussion.tex and backmatter/appendix_additional_plots.tex.

`Angular quantities` (physical slide 12, footer 11) follows Contact experiment. Define Measured angular offset as entry tilt relative to the calibrated surface. Define Angular error as tool-normal tilt relative to the calibrated surface. The angular-error vector is the shortest rotation from the inward configured normal `-n_s` to `R_EE(t) n_Tool,EE`, resolved about the first surface tangent. It is the negative of the logged normal-error vector and equals the measured angular offset at entry. Smaller component magnitude means less error about that tangent. Positive and negative values indicate opposite tilt directions. The configured surface normal comes from plate-seated calibration. The calibrated tool normal, transformed by measured EE orientation, estimates the physical tool direction. Calibration and tool-mount uncertainty remains unquantified. A zero first-tangent component alone does not establish zero total normal-angle error. Keep this metric distinct from controller orientation error e_R relative to the held pose. Do not use scalar entry-offset minus gamma as the calculation.

The angular sketch is the Chapter 4 `surface_reference_geometry.tex` illustration. Draw explicit normal arrows: inward calibrated surface normal `-n_s` in red, tool normal at contact entry in solid green, and tool normal at contact end in dashed blue. Both tool normals use the calibrated tool-to-EE relation and measured EE orientation. The common origin compares orientations and is not a contact point. The red `theta_meas,t1` arc runs from `-n_s` to entry. The blue `theta_err,t1` arc runs from `-n_s` to contact end. The main angular comparison keeps `-n_s` rightwards. Rotate only the small coordinate-frame inset clockwise by 90 degrees, as explicitly requested on 2026-09-16, so `n_s` points upwards and `t2` rightwards. The inset uses its own view, separate from the unchanged main comparison. Keep `t1` out of the page and positive rotation anticlockwise. Rotate the black positive-rotation arrow with the inset, from `+t2` towards `+n_s`. Preserve the main arrows, angle arcs, labels and drawing bounds. Apply the identical inset edit to the thesis figure. The geometry is schematic and illustrates a pure first-tangent rotation. Keep editable LaTeX and synchronized PDF/PNG/SVG assets, including symbol_thetaerr.

On the CoC sketch slide (footer 8), use Effect of CoC displacement as the left navy heading, followed by two matching native navy result bullets: Added moment can support or oppose rotation. Commanded force and moment can change. Keep these at 20 pt Arial, with a 20 pt hanging indent and their text starting at 60 pt. Do not state that force stays the same when changing the controller CoC setting. The narration specifies that f in the moment equation is calculated by the shifted controller. The position and displacement have already been defined on footer 7. Retain Commanded TCP moment and m = m_R + r_c cross f on the right, at the existing mathematical scale. Align the visible first m and m_R glyphs at 551 pt under the left-aligned heading. Keep the rotational spring-damper definition. Preserve both prominent sketches and their surface-normal arrows. Retain the two bottom bullets: the commanded force acts as if applied at the virtual point p_c, and opposite displacement reverses the added moment. This describes a virtual commanded-wrench equivalence, not a movement of the physical contact point. Referenced at the CoC, the same wrench has m_c = m - r_c cross f. At zero displacement only the added moment vanishes, while rotational impedance remains active. Do not restore the removed physical-hinge phrase. Rasterize CoC_moment.pdf with pdftocairo -png -singlefile -r 300 when needed to preserve thin arrow shafts.

For the representative contact traces, final-second model-estimated normal-force means remain -82.9, -79.0 and -78.0 N at CoC displacements -40 mm, TCP and +40 mm. Show rounded values -83, -79 and -78 N. Time to the final-error band means the earliest time the first-tangent angular error enters and remains within 0.1 degree of its own final value through contact end. The +40 mm and TCP traces give 2.489 and 3.601 s, displayed as about 2.5 and 3.6 s, a 1.1 s comparison. This is a representative-trace result with an explicit criterion. Do not restore the older 2.3/3.6 s or 1.3 s response timing. Force and moment are model estimates. Keep all three panels on Angular error and interaction wrench. Source: MyOwn/code/python/figures/contact_angular_error/audit.json and chapters/05_results_and_discussion.tex.

Present the four main null-space result slides in the approved order listed above. Preserve units, legends, panel letters and uncertainty. Each figure is followed by two consistently formatted 20 pt result bullets. All reported null-space metrics use the exact recorded interval t = 5 to 9 s, inclusive, displayed from 0 to 4 s. Keep raw logs and diagnostic calculations unchanged. On Jacobian conditioning (physical slide 22, footer 21), show absolute sigma_min(t) for the four main conditions with three-trial means and one sample SD, using the same Jacobian convention. The six-setting version remains in B4. Explain that the indicator decreases with no torque and damping alone, while conditioning and combined control keep it nearly constant. Do not claim an appreciable increase or meaningful conditioning superiority from tiny absolute differences. Keep the Cartesian position-error subplot, criterion and numerical error results out of the presentation. Full pose retention also involves orientation error. The endpoint-only Delta sigma_min plot remains supplementary, and between-trial SD does not quantify within-trial back-and-forth motion.

Distinguish cumulative joint motion in panel (a) from mean net joint motion in panel (c). Use the concise one-line figure axis Cumulative Joint Motion, E_N [degrees], with a degree symbol, in both the thesis and presentation. Keep the full quantity definition in the methodology and narration. The main panel (a) includes the four fixed-parameter conditions, while B3 includes all six settings. Both use matching three-trial means, sample-standard-deviation bands, colors and labels. Compare both conditioning magnitudes on the separate parameter slide. Over the exact 5 to 9 s interval, cumulative joint motion is 7.598 degrees with no null-space torque and 5.689 degrees with damping, a 25.1 percent reduction. Mean net joint motion values in degrees are 7.516, 5.609, 0.015, and -0.011 for no torque, damping, conditioning parameter 1.5, and conditioning parameter 2. Preserve all three panels and the underlying raw measurements. Show the stronger setting's negative value with a visible mathematical minus, using scientific notation to retain at most two decimal places. Render bar labels directly in the figure generator with mathematical text. Do not mask labels with a fixed LaTeX overlay. Each setting has three trials. Shading and error bars show one sample standard deviation. Small net joint motion can coexist with back-and-forth motion. On Net joint motion, qualify the takeaway as Conditioning left nearly zero net joint motion in this test. Conditioning cumulative motions are 0.288 and 1.687 degrees. Keep the position-error diagnostic out of the presentation. Sources: MyOwn/figures/ch05/MAIN_NS_nullspace_automatic.pdf, MyOwn/code/python/figures/make_nullspace_figure.py, MyOwn/chapters/05_results_and_discussion.tex, and Thesis_Final_Control/experiments/derived/MAIN_NS_automatic_summary.csv.

Keep figure PDF/PNG/SVG variants synchronized with their LaTeX sources under `figures_and_images\sources`; record provenance in `figures_and_images\manifest.json`.

## Videos and narration

The videos remain embedded and start on click. Contact demonstration is a visible main slide immediately after Motivation, at physical slide 3 with footer 2, within Introduction. Overview follows it at physical slide 4 with footer 3. Disturbance demonstration is hidden as B2 at physical slide 27, after Null-space torques and projector (B1). The approved null-space sequence and all nine backups are listed in Current structure above. Overview continues to list only six chapter names, without individual video entries.

- Contact uses `Video\Contact.mp4` (approximately 51 seconds). Remove the visible `Video viewing cue` heading and its explanatory text beneath the video. Keep the video and its poster frame. The short introduction covers pickup, approach, contact, and manually changing the surface during the hold before grinding. Describe it as a qualitative demonstration of compliant contact. Do not introduce TCP or CoC abbreviations in the spoken bullets before the controller slides define them. The desired orientation stays fixed and normal pressing remains active. Do not claim precisely constant measured force or quantified angular alignment from video. Preserve the technical reference notes: the centre of compliance is at the tool centre point, the additional displacement moment is zero, and the rotational spring and damper remain active. Surface contact moments drive the rotation. The held reference is not a commanded alignment trajectory. Sources: MyOwn/chapters/03_software_implementation.tex, Pre-Grinding Hold, and chapters/02_theoretical_background.tex, moment decomposition.
- Disturbance demonstration (B2) now embeds both user-supplied `Video/Nullspace1.mp4` and `Video/Nullspace2.mp4`, side by side, each starting independently on click. The presentation copies `Nullspace1_presentation.mp4` and `Nullspace2_presentation.mp4` normalize the original 90-degree rotation metadata into upright video frames and copy the original audio. Preserve all frames and the original recordings. Use the neutral labels Null-space demonstration 1 and 2. The old no-torque / damping / conditioning cue belongs to the replaced clip and must not be assigned to these two recordings without user confirmation. Keep numerical settings out of their labels and narration unless verified. The old disturbance video is no longer embedded.

Narration belongs in both the speaking PDF and PowerPoint notes and can accompany playback. PDF slides show static video poster frames.

## Speaking script and automatic PDF build

Keep the full speaking script short, clear, and easy to say aloud. Open by stating that a surface grinding controller was developed for a seven-joint robot, then explain the motivation: an unknown difference between the configured and physical surface, normal pressing that produces a contact moment when the tool is tilted, and low rotational stiffness that permits rotation towards alignment. Follow the actual slide order, introducing end-effector position and orientation before the controller equations. Give each slide its main idea and key evidence in a few short sentences. Avoid describing slide furniture, reading every symbol or plot value, and repeating long transitions. Keep necessary scientific qualifications brief. Synchronize this concise spoken text in the PowerPoint notes, retaining source blocks and essential technical reference details separately.

After **every slide change**, update `Final Presentation\Speaking\Thesis_Defense_Speaking_Script.tex` in the same task. Use the actual deck as source of truth for titles, order, visible content, notation, and transitions. Include all 34 slide sections, with Contact demonstration third, Overview fourth, Conclusion at 25 and the nine hidden backups at 26–34 in their actual order. Keep PowerPoint speaker notes synchronized too.

The speaking PDF contains only each slide's title, spoken text, and equations. Use short bullet points for the spoken text, with at most two short sentences per bullet. Keep only the most important points for each slide. Most slides need two or three bullets, with more only for the Conclusion or essential backup equations. Keep the same spoken bullets in PowerPoint notes, and preserve source/reference notes separately. Do not add timing, tables, cover/maps, slide-number labels, rehearsal cues, source appendices, headers, or footers. Let bullet lists and sections flow continuously without forced page breaks or blank paragraph spacing.

- Source: `Final Presentation\Speaking\Thesis_Defense_Speaking_Script.tex`.
- Build: `Final Presentation\Speaking\build.ps1`.
- Output: `Final Presentation\Thesis_Defense_Speaking_Script.pdf`.
- Logs/intermediate files: `Final Presentation\Speaking\build`.

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\USER\Desktop\Presentation_new\Final Presentation\Speaking\build.ps1"
```

Add `-Watch` to rebuild when the LaTeX source changes. Check `Speaking\build\watch.pid` and logs before starting another watcher. Do not assume the watcher survives a restart. The watcher **compiles LaTeX; it does not rewrite speaking text after PowerPoint edits**. The editing agent must do that synchronization, then build and visually verify the PDFs. MiKTeX/pdfLaTeX, latexmk, and Perl are available locally.

Figure typography: stiffness legends use Measured angular offset and theta_meas,t1. Plot labels remain large on Effect of rotational stiffness and Angular error and interaction wrench. The first contact panel now uses the recorded normal-error vector, while the force/moment plots retain their data, scales and colours. Blue subsection headings use regular 22 pt Arial and smaller directional parameter labels use blue 18 pt Arial. Keep all figure PDF/PNG/SVG variants and LaTeX wrappers synchronized.

Contact figure structure: footer 19 (physical slide 20), Angular error and interaction wrench, shows all three thesis panels in order: angular error, estimated normal force and estimated TCP moment. Use contact_wrench_three_panels with the common legend. Keep three centred navy 22 pt headings and existing 20 pt result bullets. Do not omit the force plot or replace it with numerical averages alone. The former duplicate contact-response/wrench backup remains removed.

Plausibility calculation clarification (2026-09-14): retain the manual perturbation headings. The normal-force slide shows the measured error change beside its heading. On the moment slide, use one navy 22 pt bullet heading, Manual rotation: about 6.5 degrees, matching the manual-push heading. Show the degree symbol in the slide text. Show the separate black label Measured error change: 6.565 degrees beside the moment heading, using the degree symbol and the same position, font and style as the normal-force measured-error label. Keep the exact 6.565-degree error change and its conversion to radians in the calculation and narration. The two slides show the spring law followed by numerical substitution, including stiffness and units. Use (1000 N/m) times (-0.019650 m) = -19.650 N for normal force and (15 N m/rad) times (6.565 pi/180 rad), rounded to 1.719 N m, for moment. The force error change is -19.650 mm, and 6.565 degrees is the measured rotational error change relative to the loaded baseline. Below each unchanged plot, give the stationary commanded and model-estimated means with their comparisons. Force: -19.640 N, 0.05 percent from calculation, and -22.292 N, 13.50 percent from command. Moment: 1.719 N m, matching calculation at the reported precision, and 1.852 N m, 7.75 percent from command. Retain the original axes, curves, legend, shaded stationary interval, and the native 20 pt result-bullet style. The narration identifies the shaded interval and the respective unloaded and loaded reference states.

Null-space time-axis wording (2026-09-14): use Time, t [s] on both Cumulative joint motion and Jacobian conditioning, matching the thesis. Remove Time After Disturbance Onset and the t_d index from the axis labels. Keep the recorded 5-9 s analysis interval displayed as 0-4 s. The experiment narration retains the time-origin explanation. This is a label-only change.

## Editable presentation equations (2026-09-15)

The user requested equations instead of photos. The 35 active standalone formula and symbol shapes are native editable Office Math equations in PowerPoint, directly converted from the original LaTeX. Use 22 pt Cambria Math, regular weight and black for every native equation and symbol key, including backups. Keep matrices, fractions, accents, underbraces and aligned equation arrays as mathematical structures. Do not restore formula pictures or use IguanaTex unless native editing fails. The preserved LaTeX sources are under `Final Presentation/figures_and_images/sources`, and `native_equations.json` maps the 35 equation shapes to exact LaTeX. Shapes are named `Equation - <asset>` and contain source text in their alternative descriptions. Update the source, native equation and catalog together. Matching PNG/PDF/SVG equation assets use the same typography. Diagram and plot labels remain part of their editable figure sources. Preserve narration and scientific notation when changing only equation representation.

## Position and rotation error sketches (2026-09-15)

On Cartesian impedance controller, keep one position-error sketch and one axis-angle rotation-error sketch beside their native error equations. Position error points from measured EE position to desired position. Rotation error is `e_R = phi u`, where phi is the correction angle and u is its unit axis. Do not restore the removed `R_d R_EE^T = R(u,phi)` identity. The rotational sketch compares the same tool face about one fixed origin, with a filled navy measured face and dashed blue desired outline. It is viewed along u, which points out of the page. Keep the u symbol and circle-dot axis marker, but omit the sentence Axis u out of page from the figure. The correction arc phi runs from measured to desired orientation. Use the paired headings Positional error and Rotational error. Its phi is distinct from the roll coordinate on Cartesian pose. The two new sketches supersede the earlier instruction prohibiting a controller error illustration. Keep all remaining force, moment and block-wrench equations editable, and preserve the compact key. Sources: position_error_sketch.tex and rotation_error_sketch.tex, with matching PDF/PNG/SVG. The source catalog, notes and speaking script must match.


Disturbance Jacobian notation (2026-09-15): use J(q) without a p index in the Null-space experiment equation and the matching thesis disturbance formulas. Here J is the translational Jacobian of the selected point on link 3. Preserve its local meaning, the transpose and all other indices.


## Presentation review decisions, 2026-09-15
The separate null-space block follows all contact results. Its current main
results and detailed backups follow the approved 2026-09-16 structure above.
The main six chapter names are
Introduction, Cartesian controller, Contact experiments, Contact results,
Null-space control and experiments, Conclusion and future work.
Keep these chapter assignments synchronized with the structure list above.
Remove the arm-disturbance purpose sentence from Null-space controller.
Keep all schedule and duration text off Null-space experiment. Its scientific
timeline remains documented in the thesis. Place the singularity explanation
as unbulleted text within Conditioning, without a separate Singularity heading.
Damping reduces null-space motion. Conditioning chooses
a local direction with larger minimum singular value.
Use angular error without final throughout the slides, figures and narration.
Display presentation values with at most two decimal places, using powers of
ten or suitable units for small quantities. Preserve full-precision source data.
The coupling slide omits the standalone e_c = A e and F_TCP = A^T F_c equations and their Error at the CoC and Wrench at the TCP headings, as requested on 2026-09-16. Keep the full shifted wrench matrix and the A = Ad(r_c) definition.
The Cartesian controller states that K and D are diagonal in the surface frame.
The CoC sketch slide has no commanded-moment equation or separate m_R key.
Use the shared surface_tool_frame.tikz core for the tool/surface-frame drawing
in the presentation and thesis direction-rule figure.

Wider CoC comparison (extended 2026-09-21): show -100, -90, -80, -40, -20, -10, 0, 10, 20, 40, 80, 90 and 100 mm for both entry directions. Use three-repeat means and sample SD from 78 plotted terminal reports within the 93-trial/31-setting main-contact summary. The 24 new trials at +/-90 and +/-100 mm completed the five-second contact phase in a later session with matching saved calibration and impedance parameters. Preserve every original point and the representative -40/TCP/+40 mm time histories. Positive-entry minimum: 0.83 degrees at +100 mm, 52.6% below TCP. Negative-entry minimum: 0.94 degrees at +10 mm, 33.7% below TCP. Across-position entry means: +9.33/-9.38 degrees. Regenerate with Thesis_Final_Control/analysis/make_coc_position_figure.py. The plot has a 15.5 cm source axis width, a vertical range containing every error bar, and 10-degree y ticks. Its slide image is 700 pt wide, centred and scaled proportionally. Sources, assets, embedded picture and slide PDF match the thesis data. Speaking material stays frozen.

CoC axis grid (2026-09-15): the plot on footer 16 (physical slide 17) labels every measured r_c,t2 position: -100, -90, -80, -40, -20, -10, 0, 10, 20, 40, 80, 90 and 100 mm. Draw a visible dotted vertical gridline through each tested position and preserve proportional spacing, all measured points and their error bars. Keep every x tick label horizontal and centred below its tick. Use 8 pt x tick text so the nearby central values remain separate, with normal spacing between the tick row, axis title and legend. Apply the same grid to the thesis Case-D figure.

Shared tool geometry (2026-09-15): on Contact experiment (footer 9) and in the thesis direction-rule figure, draw the 120 mm tool length along t2 and the 40 mm width along t1. Place the tool-face centre and shaft at the frame origin, with the long centreline on t2 and equal half-lengths in both t2 directions. Draw the axes behind the opaque tool and retain their visible arrows, with n_s continuing above the shaft. Keep the identical surface_tool_frame.tikz core in both repositories.

Directional motion history (2026-09-15, moved to B8 on 2026-09-16): retain Net joint motion over time in B8 (physical slide 33). It plots the time-dependent net joint motion, retaining positive and negative movement, with the same fixed reference direction as the net joint motion bars. Use the original recorded 5-9 s samples, displayed as 0-4 s, three-trial means and sample SD. Show all six settings plus a separate enlarged conditioning view, both in degrees. Curves begin at zero and may decrease when motion reverses. Do not call this a tool rotation or a complete seven-joint posture difference. The cumulative plot stays unchanged. The generator, portable sample archive, provenance and endpoint checks are under figures_and_images/sources.

Angular-figure labels (2026-09-15): on Angular quantities (footer 10), retain Tool normal at entry, Tool normal at end, and Calibrated surface normal. Remove only their three normal-vector symbols. Label the angular error theta_err,t1 without its end-time argument. Place its blue arc at a larger radius to the right of the red theta_meas,t1 arc, with the label beneath it. Preserve arrows, angles, and n_s/t1/t2 in the separate coordinate-frame inset. Use the same simplified figure in the thesis.

Joint motion history (2026-09-15, all-trial view moved to B6 on 2026-09-16): The complete measured-history figure is in B6 (physical slide 31). Preserve the original shared joint_motion_time asset and extend it only for the presentation. Plot measured joint-1 angle change from disturbance onset for all three trials of all six settings. Joint 1 receives the largest equivalent disturbance torque. Keep each trial, the original nominal-20-Hz timestamps and positive/negative values. Show all settings over 0--4 s and conditioning and combined settings over the first second. Repeated reversals are visible at k_sigma = 2.0 N m. These raw joint-angle changes are distinct from projected seven-joint displacement and cumulative joint motion. Preserve the earlier result panels. Rebuild from figures_and_images/sources/make_joint_motion.py and its portable samples/provenance.

Tangential-stiffness result removed (2026-09-15): omit the K_p,t2 sweep plot, its directional heading and takeaway, and the corresponding Conclusion finding and spoken points from the presentation. Physical slide 16 (footer 15) is now Effect of rotational stiffness, with the original rotational-stiffness plot enlarged and centred. Keep the common contact stiffness settings in the experimental-method slide. This presentation edit does not remove Case C from the thesis. Retain the unused translation_stiffness source assets for provenance.

Full shifted wrench matrix (2026-09-15): on Translation–rotation coupling, footer 7 (physical slide 8), show F_TCP = [f; m] = underbrace(A^T [K_p, 0; 0, K_R] A, K_TCP) [e_p; e_R] + underbrace(A^T [D_p, 0; 0, D_R] A, D_TCP) [pdot_d - pdot_EE; omega_d - omega_EE]. This follows the matrix form on footer 5 and combines the two former compact K/D transformation equations into one native editable wrench equation. Remove the separate e_c = A e and F_TCP = A^T F_c equations and their two headings above it, as requested on 2026-09-16. Preserve the actual velocity differences and small-rotation qualification. The native equation count is now 35. Source: figures_and_images/sources/coupling_wrench_blocks.tex.

## Consistent joint-motion names (2026-09-15)

Use cumulative joint motion for E_N and net joint motion for Delta eta in
plots, captions, text, the symbol list and the presentation. Retain cumulative
and net because the quantities differ: the former accumulates projected
velocity magnitude, while the latter projects the integrated joint velocity
onto the common reference direction and permits cancellation. Use Net joint
motion over time for its directional history, and Joint motion over time for
the individual measured joint-angle histories. Define the projection and the
measured angle change in the methodology. Do not alternate motion and
displacement as short names for these quantities. Keep symbols, calculations,
data, units, signs, uncertainty, filenames and internal identifiers unchanged.

Additional joint-motion views (2026-09-16, full six-setting mean in B5 and one-trial view in B7): Retain the all-repetitions view in B6, repetition r01 for every setting in B7, and the full six-setting mean in B5. The main Joint motion over time slide uses the four-condition mean. All corresponding joint-motion figures use the same axes, colours, 0--4 s interval and first-second conditioning close-up. The mean is calculated after subtracting each trial's onset angle, using exact recorded times common to the three trials within each setting. Shading is one sample standard deviation, never a confidence interval. No interpolation or smoothing is applied. The new views and generator are presentation additions. The shared original figure stays unchanged in both documents.

## Blue robot and end-effector illustrations (2026-09-16)

On presentation footers 4 and 5 only (Cartesian pose and Cartesian impedance controller), use theme blue #17365D for the drawn robot and gripper bodies, with lighter blue shading for depth. Apply this palette to the two pose figures and the positional-error grippers. Retain the line-and-circle robot chain, continuous opaque gripper geometry, reference-axis colours. In the rotational-error figure, use a solid theme-blue measured face and a lighter-blue (#4472C4) dashed desired outline, with matching blue labels and direction arrows. Keep the correction angle and axis black. This request is limited to those two presentation slides.

## Combined H-mode extension (2026-09-16)

The user requested a fifth null-space condition in the final presentation:
mode 3, k_sigma = 2 N m and d_null = 2 N m s/rad, with both torque terms active.
Three real trials are archived under experiments/h_mode_combined/results.
The exact original campaign controller revision and archived settings were
used, changing only mode 2 to mode 3. All seven null-space plots now include
the green combined condition, with the same 5–9 s interval, three repeats,
sample SD and fixed net-motion reference direction. Rebuild the presentation
extension with figures_and_images/sources/make_combined_nullspace.py.
The _combined assets are retained in the six-setting backups. The _main assets show the approved four-condition subset.
This requested extension is presentation-only. Preserve the original thesis
and four-condition assets. The combined mean cumulative motion is 0.83127 deg,
50.72% below conditioning alone at 2 N m; mean net motion is -0.01212 deg.
Acquisition was in a later session, documented in the protocol and notes.
The approved narrative now has 25 main slides, nine hidden backups and six Overview chapters.

Additional combined condition (2026-09-16): mode 3 at k_sigma = 1.5 N m
and d_null = 2 N m s/rad has three completed trials in
experiments/h_mode_combined_1p5/results. All seven plots now show six settings.
Use purple for the 1.5 combined condition and green for the 2.0 combined
condition. Mean cumulative motion at 1.5 is 0.192175 deg, 33.18% below
conditioning alone at 1.5. Mean net motion is 0.00209028 deg. Retain the
same recorded interval, sample SD, baseline projection and all earlier data.

## Title and Motivation media update (2026-09-16)

The title slide displays the full user-supplied `title_robot.jpg` on the right, without cropping or distortion. It is the original `20260916_150937.jpg` attachment, 2858 by 2908 pixels. Retain the thesis title, university, presenter, degree, supervisors and blue date on the left. Motivation is the slide numbered 1 (physical slide 2). It uses thesis Figure 1.1 above two Problem / Idea columns, with its existing wording and a short explanation of both angular-offset contributions in the narration. This presentation edit does not modify the thesis. See `experiments/media_update/README.md` for the exact assets, source hashes and validation. Earlier narrative rebuild scripts predate this media update and must not overwrite it.

Motivation Problem update (2026-09-16): retain the third Problem bullet, "Joint friction can prevent the desired tool alignment with the configured surface." Keep the existing figure and the other Problem / Idea wording. This slide-only addition does not authorize changes to the speaking script or speaker notes.

## Uniform equation typography (2026-09-16)

The user requested consistent equation font, size and weight throughout the PowerPoint, specifically correcting the oversized wrench on footer 5. All 35 native equation and symbol shapes now use **22 pt Cambria Math, regular weight, black**. This supersedes earlier requests to retain individual equation sizes or use blue mathematical heading tokens. Preserve normal italic variables, upright operators and units, and automatic subscript/superscript scaling. Matrix zero blocks use regular zeros. Keep AutoFit disabled so equations cannot silently shrink. Match font settings in all run and control properties, retain native Office Math structures and align related equals signs. The contact symbol rows and captions sit 6 pt higher to leave footer clearance. This typography request applies to the presentation only.

`experiments/equation_style/README.md` documents the update and validation. Its builder uses the local snapshot taken after the title/figure/video edits. Earlier media and narrative builders predate this formatting and must not overwrite the active deck. The equation LaTeX wrappers declare Cambria Math through unicode-math and require LuaLaTeX with that font installed. Current equation assets and slide PDF reuse the original native PowerPoint vector glyphs, scaled to 22 pt, with regular Cambria Math zeros replacing bold zeros. Source formulas, native equations, catalog, notes, speaking source and final PDFs are synchronized.
