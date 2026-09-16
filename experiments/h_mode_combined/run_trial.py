#!/usr/bin/env python3
"""Run one isolated H-mode repeat using the original campaign controller."""
import csv
import argparse
import hashlib
import json
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('repeat', type=int, choices=[1, 2, 3])
parser.add_argument('--campaign-dir', type=Path, default=Path(__file__).resolve().parent)
args = parser.parse_args()
HERE = args.campaign_dir.resolve()
RUNTIME = HERE / 'runtime/surface_grinding_controller'
repeat = args.repeat
protocol = json.loads((HERE/'protocol.json').read_text())
expected_k = protocol['k_sigma_Nm']
expected_d = protocol['d_null_Nms_per_rad']
values = {}
for path in (RUNTIME/'params').glob('*.txt'):
    for line in path.read_text().splitlines():
        line = line.split('#')[0].strip()
        if '=' in line:
            key, value = line.split('=', 1)
            values[key.strip()] = value.strip()
assert int(values['nullspace_mode']) == 3
assert float(values['nullspace_k_sigma']) == expected_k
assert float(values['nullspace_damping']) == expected_d
out = HERE / 'results' / ('r%02d' % repeat)
out.mkdir(parents=True, exist_ok=False)
shutil.copytree(RUNTIME / 'params', out / 'params_effective')
binary = RUNTIME / 'surface_grinding_controller'
meta = {'repeat': repeat, 'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
        'controller_commit': protocol['controller_commit'],
        'condition': protocol['condition'], 'k_sigma_Nm': expected_k,
        'd_null_Nms_per_rad': expected_d}
logs = RUNTIME / 'logs'
logs.mkdir(exist_ok=True)
assert not list(logs.glob('*.csv')), 'Archive existing runtime logs first'
proc = subprocess.Popen(['stdbuf', '-o0', '-e0', str(binary)], cwd=RUNTIME,
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, start_new_session=True)
patterns = [(b'Press Enter to recover and configure the robot.', b'\n'),
            (b'Choice [s/h/t/g/q/o/c/r/f/b/e]: ', b'h\n'),
            (b'Choice [0/1/2/3', b'3\n')]
sel = selectors.DefaultSelector()
sel.register(proc.stdout, selectors.EVENT_READ)
buf = b''
deadline = time.monotonic() + 120
try:
    with (out / 'terminal.log').open('wb') as transcript:
        while True:
            if time.monotonic() > deadline:
                raise TimeoutError('Controller did not finish in 120 seconds')
            ready = sel.select(1)
            if not ready:
                if proc.poll() is not None:
                    break
                continue
            chunk = os.read(proc.stdout.fileno(), 8192)
            if not chunk:
                break
            transcript.write(chunk)
            transcript.flush()
            sys.stdout.buffer.write(chunk)
            sys.stdout.buffer.flush()
            buf += chunk
            if patterns and patterns[0][0] in buf:
                pattern, reply = patterns.pop(0)
                proc.stdin.write(reply)
                proc.stdin.flush()
                buf = buf.split(pattern, 1)[1]
            buf = buf[-16384:]
    meta['exit_code'] = proc.wait(timeout=5)
finally:
    if proc.poll() is None:
        os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(timeout=10)
    meta['exit_code'] = proc.returncode
    meta['files'] = {}
    for f in logs.glob('*.csv'):
        target = out/f.name
        shutil.move(str(f), target)
        meta['files'][f.name] = hashlib.sha256(target.read_bytes()).hexdigest()
    (out/'provenance.json').write_text(json.dumps(meta, indent=2)+'\n')
if meta['exit_code'] != 0:
    sys.exit('Controller failed. Preserved attempt. No automatic retry.')
with (out/'surface_grinding_controller_log.csv').open() as f:
    rows = list(csv.DictReader(f))
window = [r for r in rows if 5 <= float(r['time']) <= 9]
assert len(window) > 3500 and float(window[0]['time']) == 5 and float(window[-1]['time']) == 9
assert all(int(r['nullspace_mode']) == 3 for r in rows)
assert all(float(r['nullspace_damping']) == expected_d for r in rows)
assert all(float(r['sigma_k_sigma']) == expected_k for r in window)
assert max(float(r['time']) for r in rows) >= 17.9
assert min(float(r['disturbance_torque_scale']) for r in window) >= .999
assert (out/'surface_grinding_controller_sigma_debug.csv').is_file()
meta['acquisition_checks_passed'] = True
(out/'provenance.json').write_text(json.dumps(meta, indent=2)+'\n')
print('Trial archived and acquisition checks passed:', out)
