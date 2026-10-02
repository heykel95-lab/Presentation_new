from pathlib import Path
HERE=Path(__file__).resolve().parent
source=(HERE/'archive/assets/sources/CoC_moment.tex').read_text(encoding='utf-8')
source=source.replace('{$p_c$}',r'{$p_{\mathrm{CoC}}$}')
source=source.replace(r'\node[lbl, left, black] at (P)',r'\node[lbl, below, black] at ($(P)+(0,-0.02)$)')
source=source.replace(r'\node[lbl, right, black] at (P2)',r'\node[lbl, below, black] at ($(P2)+(0,-0.02)$)')
for t,p in [('T','P'),('T2','P2')]:
    old=rf'\draw[frc] ($({t})+(0,1.05)$) -- ($({t})+(0,0.14)$);'
    new=rf'\draw[frc] ($({p})+(0,1.05)$) -- ($({p})+(0,0.14)$);'
    assert old in source;source=source.replace(old,new)
    old=rf'\node[lbl, right, black] at ($({t})+(0.72,0.60)$) {{$f_n$}};'
    new=rf'\node[lbl, right, black] at ($({p})+(0.13,0.65)$) {{$f_n$}};'
    assert old in source;source=source.replace(old,new)
source=source.replace('% ---- normal component of the commanded force, pressing into the plane --','% ---- normal force shown as acting at the virtual CoC -------------------')
source=source.replace('% ---- the contribution it makes through the displacement ----------------','% ---- resulting moment ABOUT TCP; not a second independent moment -------')
source=source.replace('% Elevation sketch of the contribution the normal component of the commanded','% Presentation-specific variant: force acts as if applied at virtual p_CoC.\n% The curved arrows show its resulting moment about TCP. No physical contact\n% relocation or second independently applied moment is implied.\n% Elevation sketch of the contribution the normal component of the commanded')
(HERE/'assets/sources/coc_force_shift_cases.tex').write_text(source,encoding='utf-8')
print('Created the shifted-force case figure with p_CoC labels and unchanged moment signs.')
