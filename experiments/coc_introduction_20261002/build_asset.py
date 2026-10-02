from pathlib import Path
import subprocess,sys
HERE=Path(__file__).resolve().parent;asset=sys.argv[1]
with (HERE/(asset+'-build.txt')).open('w',encoding='utf-8') as log:
    subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory=..',asset+'.tex'],cwd=HERE/'assets/sources',stdout=log,stderr=subprocess.STDOUT,check=True)
    subprocess.run(['pdftocairo','-png','-singlefile','-r','300',asset+'.pdf',asset],cwd=HERE/'assets',stdout=log,stderr=subprocess.STDOUT,check=True)
    subprocess.run(['pdftocairo','-svg',asset+'.pdf',asset+'.svg'],cwd=HERE/'assets',stdout=log,stderr=subprocess.STDOUT,check=True)
print('Built '+asset+' as PDF, PNG and SVG.')
