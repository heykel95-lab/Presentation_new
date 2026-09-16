# Separate factual review of the supplied narration

The speaking text preserves the user's explanations and numerical claims, as
requested for a grammar-only edit. The points below are **not corrections
silently applied to the narration**. They should be resolved before presenting.

- **Perfect alignment:** the plotted angular errors remain nonzero. The reported
  first-tangent component alone cannot establish a completely flat tool. The
  experiments do not isolate friction as the cause of asymmetry, or establish
  that all remaining error comes from pose/surface measurement uncertainty.
- **Controller checks:** agreement in the two quasi-static tests supports the
  predicted response. It does not by itself prove the complete controller is
  correct. The moment calculation uses 6.565 degrees, approximately 6.6 degrees,
  rather than exactly 6 degrees, to obtain approximately 1.72 N m.
- **Commanded versus estimated wrench:** the existing slide reports stationary
  mean differences of 2.32% for force and 4.87% for moment. “Exactly equal” is not
  supported. These are model estimates, rather than independent force/torque
  sensor measurements. The causal statements about friction and the transient
  differences have not been established by those curves alone.
- **Rotational stiffness:** increasing stiffness from 5 to 50 changes the error
  from 1.75 to 6.58 degrees, approximately 3.76 times, rather than three times.
- **CoC sweep:** the negative-entry error magnitude improves from 1.41 degrees
  at 0 mm to its minimum of 0.94 degrees at +10 mm, then worsens. It does not
  become progressively worse immediately after 0 mm. For positive entry, error
  is already 8.33 degrees at −20 mm, versus 1.89 degrees at −10 mm. Thus “flat
  until −20 mm” is misleading. All values are three-trial means. See the audit
  in `../coc_plot_check/verification.json` and `checked_points.csv`.
- **Time histories:** the reported 2.5 s versus 3.6 s compares settling within
  0.1 degree of each trace's own endpoint. It is not a measured time to perfect
  flatness. Final estimated forces are approximately −83, −79 and −78 N, which
  are similar rather than identical. Lower transients in one trial do not alone
  establish that a configuration generally needs less force or contact moment.
- **Null-space meaning:** the redundant motion is a combination of joint
  motions, not one separate redundant joint. The virtual link-three force is
  mapped into joint torques, with the largest equivalent disturbance torque
  on joint one. Cumulative joint motion is a projection using all seven joint
  velocities, not the absolute angle travelled by joint one.
- **Conditioning comparison:** combined control reduces cumulative motion, but
  small absolute singular-value differences do not establish better conditioning.
  Reversals remain with damping. Lower cumulative motion does not, by itself,
  establish a smoother response.

Sources are the unchanged slide content, original speaking notes and technical
reference blocks, and the CoC trial audit. No new experiment or factual change
to the presentation was made in this grammar edit.
