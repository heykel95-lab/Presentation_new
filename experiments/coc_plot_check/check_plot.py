"""Audit the apparent intersection on numbered slide 16 without editing the deck."""
from pathlib import Path
import csv
import hashlib
import json
import re
import statistics
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTROL = ROOT.parent / 'Thesis_Final_Control'
THESIS = ROOT.parent / 'MyOwn-thesis'
SOURCE = 'Final Presentation/figures_and_images/sources/CoC_position.tex'


def points(text):
    blocks = re.findall(r'coordinates\s*\{(.*?)\};', text, re.S)
    return [
        {int(x): (float(y), float(sd)) for x, y, sd in
         re.findall(r'\(([-\d.]+),([-\d.]+)\)\s*\+-\s*\(0,([-\d.]+)\)', block)}
        for block in blocks
    ]


current = points((ROOT / SOURCE).read_text())
previous = points(subprocess.check_output(
    ['git', 'show', '082196a^:' + SOURCE], cwd=ROOT, text=True))
thesis = points((THESIS / 'figures/ch05/results_case_d_panels.tex').read_text())
assert current == thesis
assert all(current[i][x] == previous[i][x] for i in [0, 1] for x in previous[i])
assert len(previous[0]) == len(previous[1]) == 7
per_trial = list(csv.DictReader((THESIS / 'code/python/figures/contact_angular_error/per_trial_results.csv').open()))
trial_index = {(row['run_id'], row['repeat']): row for row in per_trial}
rows = []
hashes = []
for curve, direction in enumerate(['pos', 'neg']):
    for x, (plotted_mean, plotted_sd) in current[curve].items():
        run = f'P2_t1_{direction}_{"m" if x < 0 else "p"}{abs(x):03d}'
        values = []
        for repeat in ['r01', 'r02', 'r03']:
            report = CONTROL / 'experiments/results' / run / repeat / 'terminal.log'
            data = report.read_bytes()
            content = data.decode(errors='replace')
            match = re.search(r'deviation components.*?before=\[(.*?)\].*?after=\[(.*?)\]', content)
            assert match and 'stop: time | t=5.0 s' in content, report
            # Same angular-error convention as the documented full-vector audit.
            value = -float(match[2].split(',')[0])
            record = trial_index[(run, repeat)]
            assert abs(value - float(record['final_t1_deg'])) < 1e-10
            digest = hashlib.sha256(data).hexdigest()
            crlf_digest = hashlib.sha256(data.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')).hexdigest()
            assert record['report_sha256'] in [digest, crlf_digest], report
            hashes.append({'run': run, 'repeat': repeat, 'sha256': digest,
                           'archived_windows_sha256': record['report_sha256'],
                           'archive_matches_allowing_line_endings': True})
            values.append(value)
        mean, sd = statistics.mean(values), statistics.stdev(values)
        assert abs(mean - plotted_mean) < 1e-8 and abs(sd - plotted_sd) < 1e-8
        rows.append({'direction': direction, 'position_mm': x, 'r01_deg': values[0],
                     'r02_deg': values[1], 'r03_deg': values[2],
                     'mean_deg': mean, 'sample_sd_deg': sd})

xs = sorted(current[0])
gaps = {x: current[0][x][0] - current[1][x][0] for x in xs}
assert all(value > 0 for value in gaps.values())
assert 'smooth' not in (ROOT / SOURCE).read_text()
# Both curves connect the same ascending x coordinates with straight segments.
# A strictly positive endpoint difference implies no crossing on any segment.
closest = min(gaps, key=gaps.get)
report = {
    'slide_footer': 16, 'slide_title': 'Effect of CoC position',
    'original_reports_verified': len(hashes), 'points_recomputed': len(rows),
    'three_repeats_and_sample_sd_match': True,
    'thesis_and_presentation_points_identical': True,
    'all_14_points_inside_previous_range_unchanged': True,
    'earlier_range_revision': '082196a^',
    'curves_intersect': False,
    'reason': 'Positive-entry means exceed negative-entry means at every common x. Both use straight line segments.',
    'closest_position_mm': closest,
    'closest_gap_deg': gaps[closest],
    'at_closest_position': [r for r in rows if r['position_mm'] == closest],
    'older_metric_revision': '2a87355^',
    'older_metric': 'Contact response gamma relative to entry orientation',
    'current_metric': 'Angular error theta_err,t1 relative to calibrated surface normal',
    'visible_overlap': 'Marker outlines overlap at -10 mm. The means and their one-SD intervals do not intersect there.',
    'source_reports': hashes,
}
(HERE / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
with (HERE / 'checked_points.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), gridspec_kw={'width_ratios': [1, 1.2, .8]})
for ax, limits, title in zip(axes[:2], [(-45, 45), (-88, 88)],
                            ['Previous range: same angular-error values', 'Current range: added endpoints only']):
    for curve, color, marker, label in [(0, 'black', 'o', 'Positive entry tilt'),
                                       (1, '#17365D', 's', 'Negative entry tilt')]:
        selected = [x for x in xs if limits[0] < x < limits[1]]
        ax.errorbar(selected, [current[curve][x][0] for x in selected],
                    yerr=[current[curve][x][1] for x in selected],
                    color=color, marker=marker, mfc='white', ms=5, capsize=3, label=label)
    ax.set(xlim=limits, ylim=(-11, 11), xlabel='CoC position along t₂ [mm]', title=title)
    ax.grid(alpha=.2)
axes[0].set_ylabel('Angular error about t₁ [°]')
for curve, color, marker, label in [(0, 'black', 'o', 'Positive entry'),
                                   (1, '#17365D', 's', 'Negative entry')]:
    y, sd = current[curve][-10]
    axes[2].errorbar(curve, y, yerr=sd, color=color, marker=marker,
                     mfc='white', ms=7, capsize=5, ls='none')
    axes[2].annotate(f'{y:.3f}°', (curve, y), xytext=(0, 13),
                     textcoords='offset points', ha='center', color=color)
axes[2].set(xticks=[0, 1], xticklabels=['Positive\nentry', 'Negative\nentry'],
            xlim=(-.5, 1.5), ylim=(1.78, 1.94), title='At −10 mm: separate means')
axes[2].set_ylabel('Angular error about t₁ [°]')
axes[2].grid(axis='y', alpha=.2)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=2, frameon=False)
fig.tight_layout(rect=(0, .09, 1, 1))
fig.savefig(HERE / 'comparison.png', dpi=180)
fig.savefig(HERE / 'comparison.pdf')
print(json.dumps({key: val for key, val in report.items() if key != 'source_reports'}, indent=2))
