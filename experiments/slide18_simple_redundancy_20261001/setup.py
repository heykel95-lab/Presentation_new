from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
PREVIOUS=HERE.parent/'slide18_singular_value_20261001'
OLD='At full Jacobian rank, one null-space direction allows several joints to move together without changing the instantaneous motion of the (EE).'
NEW='The robot’s extra degree of freedom allows its posture to change while keeping the (EE) pose unchanged.'
script=(PREVIOUS/'prepare.py').read_text(encoding='utf-8')
start=script.index('    original=next(')
end=script.index("    (HERE/'slide10.xml')",start)
replacement=f'''    original=next(s for s in re.findall(r'<p:sp\\b[^>]*>.*?</p:sp>',xml,re.S) if 'name="Rank qualification"' in s)
    old={OLD!r}
    new={NEW!r}
    assert original.count(old)==1
    updated=xml.replace(original,original.replace(old,new,1),1)
    assert updated!=xml
    E.fromstring(updated)
    assert re.findall(r'<ns0:oMath>.*?</ns0:oMath>',updated,re.S)==re.findall(r'<ns0:oMath>.*?</ns0:oMath>',xml,re.S)
'''
script=script[:start]+replacement+script[end:]
script=script.replace("parent=HERE.parent/'ee_parentheses_20261001'","parent=HERE.parent/'slide18_singular_value_20261001'")
start=script.index("(HERE/'verification.json')")
script=script[:start]+f'''(HERE/'verification.json').write_text(json.dumps({{
    'date':'2026-10-01','physical_slide':19,'footer':18,
    'redundancy_bullet':{NEW!r},
    'conditioning_bullets_preserved':True,
    'native_equation_contents_preserved':True,'all_other_shapes_and_notes_preserved':True
}},indent=2))
print('Prepared the simplified redundancy explanation on footer 18.')
'''
(HERE/'prepare.py').write_text(script,encoding='utf-8')
shutil.copy2(PREVIOUS/'export.ps1',HERE/'export.ps1')
script=(PREVIOUS/'refresh_and_verify.py').read_text(encoding='utf-8')
script=script.replace("assert 'Seeks a larger minimum singular' in native.pages[0].extract_text()",
                      "assert 'extra degree of freedom' in native.pages[0].extract_text()\nassert 'At full Jacobian rank' not in native.pages[0].extract_text()")
(HERE/'refresh_and_verify.py').write_text(script,encoding='utf-8')
script=(PREVIOUS/'finalize.py').read_text(encoding='utf-8')
script=script[:script.index("readme=FINAL/'README.txt'")]
script+='''readme=FINAL/'README.txt'
entry=('2026-10-01: Simplified the redundancy bullet on Null-space controller (footer 18 / physical 19): '
       "The robot's extra degree of freedom allows its posture to change while keeping the (EE) pose unchanged. "
       'Removed the full-rank qualification and the several-joints wording at the user request. '
       'All other content, equations, notes and speech are unchanged. The full PDF is updated; '
       'the supplementary PDF is unchanged. See ../experiments/slide18_simple_redundancy_20261001/verification.json.\\n\\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
agents=ROOT/'AGENTS.md';contents=agents.read_text(encoding='utf-8');heading='# Thesis and presentation workspace\\n'
assert contents.startswith(heading)
rule=('\\n## Simple redundancy explanation (2026-10-01)\\n\\n'
      'On Null-space controller (footer 18 / physical slide 19), explain that\\n'
      "the robot's extra degree of freedom allows its posture to change while\\n"
      'keeping the (EE) pose unchanged. Do not restore the full-Jacobian-rank\\n'
      'qualification or the several-joints phrasing in this bullet. Preserve\\n'
      'the minimum-singular-value explanation, all equations, notes and speech.\\n'
      'See experiments/slide18_simple_redundancy_20261001/verification.json.\\n')
agents.write_text(heading+rule+contents[len(heading):],encoding='utf-8')
verification.update({'changed_package_parts':changed,'all_other_package_parts_byte_identical':True,
    'native_render_visually_checked':True,'speaking_files_unchanged':True,
    'supplementary_pdf_unchanged':True,'installed':True})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\\n')
print('Saved the simplified redundancy explanation in PowerPoint and PDF.')
'''
(HERE/'finalize.py').write_text(script,encoding='utf-8')
print('Prepared the targeted editing and verification scripts.')
