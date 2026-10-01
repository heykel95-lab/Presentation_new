from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
PREVIOUS=HERE.parent/'slide18_nullspace_condition_label_20261001'
script=(PREVIOUS/'prepare.py').read_text(encoding='utf-8')
start=script.index('    def shape(name):')
end=script.index("    (HERE/'slide10.xml')",start)
replacement='''    original=next(s for s in re.findall(r'<p:sp\\b[^>]*>.*?</p:sp>',xml,re.S) if 'name="Conditioning role"' in s)
    phrase='Seeks postures away from singularities, where the (EE) loses a motion direction.'
    run=next(s for s in re.findall(r'<a:r>.*?</a:r>',original,re.S) if phrase in s)
    def text_run(text,font='Arial',size=2000,baseline=None,italic=False):
        r=re.sub(r'<a:t>.*?</a:t>','<a:t>'+text+'</a:t>',run,flags=re.S)
        if font!='Arial':
            r=r.replace('typeface="Arial"','typeface="'+font+'"')
            r=re.sub(r' panose="[^\"]*"| pitchFamily="[^\"]*"| charset="[^\"]*"','',r)
        r=r.replace('sz="2000"','sz="'+str(size)+'"')
        attributes=(' baseline="'+str(baseline)+'"' if baseline is not None else '')+(' i="1"' if italic else '')
        r=r.replace('<a:rPr ','<a:rPr'+attributes+' ',1)
        return r
    new_runs=(text_run('Seeks a larger minimum singular value ')+
              text_run('σ','Cambria Math')+text_run('min','Cambria Math',2000,-25000)+
              text_run(' of ')+text_run('J','Cambria Math',italic=True)+
              text_run(', moving away from singularities.'))
    updated=xml.replace(original,original.replace(run,new_runs,1),1)
    assert updated!=xml
    E.fromstring(updated)
    assert re.findall(r'<ns0:oMath>.*?</ns0:oMath>',updated,re.S)==re.findall(r'<ns0:oMath>.*?</ns0:oMath>',xml,re.S)
'''
script=script[:start]+replacement+script[end:]
script=script.replace("parent=HERE.parent/'slide17_single_legend_20261001'","parent=HERE.parent/'ee_parentheses_20261001'")
start=script.index("(HERE/'verification.json')")
script=script[:start]+'''(HERE/'verification.json').write_text(json.dumps({
    'date':'2026-10-01','physical_slide':19,'footer':18,
    'conditioning_bullet':'Seeks a larger minimum singular value σ_min of J, moving away from singularities.',
    'first_conditioning_bullet_preserved':True,
    'native_equation_contents_preserved':True,'all_other_shapes_and_notes_preserved':True
},indent=2))
print('Prepared the minimum singular value explanation on footer 18.')
'''
(HERE/'prepare.py').write_text(script,encoding='utf-8')
shutil.copy2(PREVIOUS/'export.ps1',HERE/'export.ps1')
script=(PREVIOUS/'refresh_and_verify.py').read_text(encoding='utf-8')
script=script.replace("assert 'Null-space condition:' in native.pages[0].extract_text()","assert 'Seeks a larger minimum singular' in native.pages[0].extract_text()")
(HERE/'refresh_and_verify.py').write_text(script,encoding='utf-8')
script=(PREVIOUS/'finalize.py').read_text(encoding='utf-8')
script=script[:script.index("readme=FINAL/'README.txt'")]
script+='''readme=FINAL/'README.txt'
entry=('2026-10-01: On Null-space controller (footer 18 / physical 19), conditioning now '
       'explicitly seeks a larger minimum singular value sigma_min of J, moving away from singularities. '
       'This matches the minimum-singular-value quantity used in the results plot. '
       'All other content, equations, notes and speech are unchanged. The full PDF is updated; '
       'the supplementary PDF is unchanged. See ../experiments/slide18_singular_value_20261001/verification.json.\\n\\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
agents=ROOT/'AGENTS.md';contents=agents.read_text(encoding='utf-8');heading='# Thesis and presentation workspace\\n'
assert contents.startswith(heading)
rule=('\\n## Conditioning and minimum singular value (2026-10-01)\\n\\n'
      'On Null-space controller (footer 18 / physical slide 19), the second\\n'
      'conditioning bullet reads: Seeks a larger minimum singular value sigma_min\\n'
      'of J, moving away from singularities. Display sigma_min with a native\\n'
      'Greek sigma and subscript min, matching the metric in the conditioning\\n'
      'plot. Retain the first posture-adjustment bullet and all native equations.\\n'
      'Speaking files and notes remain unchanged. See\\n'
      'experiments/slide18_singular_value_20261001/verification.json.\\n')
agents.write_text(heading+rule+contents[len(heading):],encoding='utf-8')
verification.update({'changed_package_parts':changed,'all_other_package_parts_byte_identical':True,
    'native_render_visually_checked':True,'speaking_files_unchanged':True,
    'supplementary_pdf_unchanged':True,'installed':True})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\\n')
print('Saved the minimum singular value explanation in PowerPoint and PDF.')
'''
(HERE/'finalize.py').write_text(script,encoding='utf-8')
print('Prepared the targeted editing and verification scripts.')
