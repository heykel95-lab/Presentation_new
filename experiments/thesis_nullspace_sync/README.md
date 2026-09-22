# Thesis null-space plots synchronized on 2026-09-21

The user limited the update to the null-space experiment and selected the main
presentation plots only. The thesis now includes exact PDF copies of:

- nullspace_cumulative_main (main physical slide 20)
- nullspace_conditioning_main (main physical slide 21)
- joint_motion_mean_main (main physical slide 22)

The two older thesis figure files, MAIN_NS_nullspace_automatic.pdf and
joint_motion_time.pdf, are archived under figures/withdrawn/nullspace_20260921
and excluded from the compiled thesis. Backup plots were not added.

The selected comparison uses four settings at fixed enabled values of
k_sigma = 2 N m and d_null = 2 N m s/rad. The corresponding null-space
methods, results, captions and summaries were updated to describe the combined
condition and three-trial means with one sample SD. Non-null-space plot assets
and contact-results text are unchanged. New CoC results saved during this task
were retained when the null-space changes were merged.

The thesis includes portable copies of the original presentation generators,
compressed measured samples, analysis summaries and provenance under
code/python/figures/nullspace_presentation_main. Raw logs for the twelve selected
trials were checked against their saved hashes. The three presentation PNGs
were also checked against the actual embedded images on the active slides.

Verification is in verification_20260921.json. The compiled thesis has 122
pages, with the three figures on printed pages 71–73 (physical pages 98–100).
The final LaTeX pass has no unresolved references or overfull boxes. A temporary
current PGFPlots package was used to satisfy the existing compat=1.18 setting.
The presentation, speaking script and speaker notes were not edited.
