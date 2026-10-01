from pathlib import Path
import subprocess,shutil
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ASSETS=ROOT/'Final Presentation/figures_and_images'
ARCHIVE=HERE/'archive'
for name in ['cartesian_pose_position','cartesian_pose_orientation']:
    source=ASSETS/'sources'/f'{name}.tex'
    old=source.read_text(encoding='utf-8')
    assert old.count('{EE};')==1
    (ARCHIVE/source.name).write_bytes(source.read_bytes())
    (HERE/source.name).write_text(old.replace('{EE};','{(EE)};'),encoding='utf-8')
    for ext in ['pdf','png','svg']:
        shutil.copy2(ASSETS/f'{name}.{ext}',ARCHIVE/f'{name}.{ext}')
    result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
        '-output-directory='+str(HERE),str(HERE/source.name)],cwd=source.parent,capture_output=True)
    (HERE/f'{name}-build.txt').write_bytes(result.stdout+result.stderr)
    assert result.returncode==0,result.stdout[-3000:]
    for args in [['pdftocairo','-png','-singlefile','-r','300',str(HERE/f'{name}.pdf'),str(HERE/name)],
                 ['pdftocairo','-svg',str(HERE/f'{name}.pdf'),str(HERE/f'{name}.svg')]]:
        subprocess.run(args,capture_output=True,check=True)
print('Updated both diagram labels in their original LaTeX sources.')
