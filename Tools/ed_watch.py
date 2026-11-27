"""Vigia de comandos para o editor (economiza digitação no console).
Rode uma vez por sessão do editor:  py "<projeto>/Tools/ed_watch.py"
Depois, qualquer processo pode escrever o caminho de um .py em Saved/ed_cmd.txt
(uma linha); o vigia executa o arquivo no próximo tick, grava a saída/erro em
Saved/ed_out.txt e apaga o comando. Uma linha "STOP" desliga o vigia.
"""
import unreal, os, io, traceback, contextlib, time

ROOT = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved'
CMD = os.path.join(ROOT, 'ed_cmd.txt')
OUT = os.path.join(ROOT, 'ed_out.txt')

_state = {'t': 0.0}

def _tick(dt):
    _state['t'] += dt
    if _state['t'] < 0.5:
        return
    _state['t'] = 0.0
    if not os.path.exists(CMD):
        return
    try:
        with open(CMD, 'r', encoding='utf-8') as f:
            path = f.read().strip()
        os.remove(CMD)
    except Exception:
        return
    if path == 'STOP':
        unreal.unregister_slate_post_tick_callback(_state['h'])
        with open(OUT, 'w') as f:
            f.write('watcher stopped\n')
        return
    buf = io.StringIO()
    t0 = time.time()
    try:
        with contextlib.redirect_stdout(buf):
            g = {'__name__': '__main__', '__file__': path}
            with open(path, 'r', encoding='utf-8') as f:
                code = compile(f.read(), path, 'exec')
            exec(code, g)
        status = 'OK'
    except Exception:
        buf.write(traceback.format_exc())
        status = 'ERROR'
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('%s %s %.1fs\n' % (status, path, time.time() - t0))
        f.write(buf.getvalue()[-6000:])

if 'ED_WATCH_HANDLE' in dir(unreal):
    try:
        unreal.unregister_slate_post_tick_callback(unreal.ED_WATCH_HANDLE)
    except Exception:
        pass
_state['h'] = unreal.register_slate_post_tick_callback(_tick)
unreal.ED_WATCH_HANDLE = _state['h']
with open(OUT, 'w') as f:
    f.write('watcher started\n')
