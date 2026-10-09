"""Install validated outputs, refreshing only unmodified matching open PDFs."""
import os, json
import win32com.client
from workflow import ROOT, F, S, H, install

targets = [F / 'Simple_speech_updated.pdf', F / 'Projector_Test_Versions/02_03_Improved_Speech.pdf', S / 'Simple_speech.pdf']
normalize = lambda p: os.path.normcase(os.path.abspath(str(p)))
target_names = {normalize(p) for p in targets}
app = win32com.client.Dispatch('AcroExch.App')
matches = []
for i in range(app.GetNumAVDocs()):
    av = app.GetAVDoc(i)
    js = av.GetPDDoc().GetJSObject()
    path = str(js.path)
    if len(path) > 3 and path[0] == '/' and path[2] == '/':
        path = path[1] + ':' + path[2:]
    if normalize(path) in target_names:
        assert not js.dirty, 'Matching open PDF has unsaved changes. Preserve it.'
        matches.append((av, path, av.GetAVPageView().GetPageNum()))
closed = []
try:
    for av, path, page in matches:
        assert av.Close(True), 'Could not close the unmodified matching PDF'
        closed.append((path, page))
    install()
finally:
    for path, page in closed:
        av = win32com.client.Dispatch('AcroExch.AVDoc')
        assert av.Open(path, '')
        av.GetAVPageView().GoTo(page)
report = json.loads((H / 'verification.json').read_text())
report['open_pdfs_refreshed_without_unsaved_changes'] = [{'path': str(__import__('pathlib').Path(path).relative_to(ROOT)), 'page': page + 1} for path, page in closed]
(H / 'verification.json').write_text(json.dumps(report, indent=2))
