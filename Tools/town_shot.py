"""Fotos da cidade sem MCP: py town_shot.py  (ou exec com SHOTS definido).
SHOTS = [(nome, (x,y,z), (pitch,yaw)), ...]; tira uma foto por vez (fila no tick do Slate),
grava em Saved/TownShots/<nome>.png (960x540) e escreve Saved/TownShots/done.txt no fim.
"""
import unreal, os, glob, shutil

OUTDIR = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\TownShots'
SSDIR = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\Screenshots\WindowsEditor'
os.makedirs(OUTDIR, exist_ok=True)

DEFAULT = [
    ('porta',      (1150, 207, 170),  (0, 0)),      # na porta olhando a rua
    ('rua_norte',  (1700, 0, 170),    (0, 90)),     # meio da rua olhando norte
    ('rua_sul',    (1700, 0, 170),    (0, -90)),    # meio da rua olhando sul
    ('cruzamento', (1700, 3700, 170), (0, 0)),      # cruzamento olhando leste
    ('ceu',        (1700, 0, 170),    (35, 30)),    # olhando para cima
    ('telhado',    (600, -1500, 1400),(-12, 40)),   # por cima da livraria
    ('balcao',     (700, 207, 170),   (0, 0)),      # do balcao para a porta
]

def run(shots=None, w=960, h=540):
    shots = shots or DEFAULT
    for f in glob.glob(os.path.join(OUTDIR, 'done.txt')):
        os.remove(f)
    ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    st = {'i': 0, 'phase': 0, 'wait': 0, 'h': None, 'before': set()}

    def tick(dt):
        if st['wait'] > 0:
            st['wait'] -= 1
            return
        i = st['i']
        if st['phase'] == 0:
            if i >= len(shots):
                unreal.unregister_slate_post_tick_callback(st['h'])
                with open(os.path.join(OUTDIR, 'done.txt'), 'w') as f:
                    f.write('\n'.join(s[0] for s in shots))
                return
            name, loc, rot = shots[i]
            ues.set_level_viewport_camera_info(unreal.Vector(*loc), unreal.Rotator(rot[0], rot[1], 0) if False else unreal.Rotator(pitch=rot[0], yaw=rot[1], roll=0))
            st['before'] = set(glob.glob(os.path.join(SSDIR, '*.png')))
            st['phase'] = 1
            st['wait'] = 20   # deixa o streaming/TSR assentar
        elif st['phase'] == 1:
            unreal.SystemLibrary.execute_console_command(None, 'HighResShot %dx%d' % (w, h))
            st['phase'] = 2
            st['wait'] = 15
        else:
            new = set(glob.glob(os.path.join(SSDIR, '*.png'))) - st['before']
            if not new:
                st['wait'] = 5
                return
            src = max(new, key=os.path.getmtime)
            dst = os.path.join(OUTDIR, shots[i][0] + '.png')
            try:
                shutil.move(src, dst)
            except Exception:
                st['wait'] = 5
                return
            st['i'] += 1
            st['phase'] = 0

    st['h'] = unreal.register_slate_post_tick_callback(tick)

if __name__ == '__main__':
    run(globals().get('SHOTS'))
