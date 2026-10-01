"""Restore a generated PDF archive from its lossless .pdf.delta.zip file."""
from pathlib import Path
from zipfile import ZipFile
import argparse, hashlib, json

parser = argparse.ArgumentParser()
parser.add_argument('delta', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
delta = args.delta.resolve()
assert delta.is_relative_to(root / 'experiments')
with ZipFile(delta) as archive:
    metadata = json.loads(archive.read('manifest.json'))
    literal = archive.read('literal.bin')
base = (root / metadata['base']).read_bytes()
assert hashlib.sha256(base).hexdigest() == metadata['base_sha256']
restored = b''.join((base if kind == 'copy' else literal)[offset:offset+count]
                    for kind, offset, count in metadata['operations'])
assert len(restored) == metadata['original_size']
assert hashlib.sha256(restored).hexdigest() == metadata['original_sha256']
destination = delta.with_name(delta.name.removesuffix('.delta.zip'))
with destination.open('xb') as output:
    output.write(restored)
print(destination)
