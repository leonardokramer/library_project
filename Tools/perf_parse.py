"""Le o ultimo bloco PERF_BEGIN..PERF_END do log e mostra o tempo total de GPU e os maiores passos."""
import re, sys
p = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\Logs\library_project.log'
t = open(p, encoding='utf-8', errors='ignore').read()
b = t.rfind('PERF_BEGIN')
e = t.find('PERF_END', b)
blk = t[b:e if e > 0 else None]
frames = blk.split('GPU Profile for Frame')[1:]
for i, f in enumerate(frames):
    rows = []
    for line in f.splitlines():
        m = re.search(r'([\d.]+)ms\s+.*?\s{2,}(\S.*)$', line)
        if m:
            rows.append((float(m.group(1)), m.group(2).strip()[:60]))
    tot = max((r for r in rows), default=(0, ''), key=lambda r: r[0])
    print('frame', i, 'max row', tot)
    for r in sorted(rows, reverse=True)[1:9]:
        print('   %.2f %s' % r)
    if 'hair' in sys.argv:
        for r in rows:
            if 'Hair' in r[1] or 'hair' in r[1]:
                print('   HAIR %.2f %s' % r)
