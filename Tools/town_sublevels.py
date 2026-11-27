"""Reposiciona os subniveis da cidade para a Main Street densa (2026-11-27, noite):
King Wash vai para a Elm Street (lado norte, a leste da Main), casas A e B para a Elm Street a oeste,
casas C e D e o trailer saem do mundo (os mapas continuam no projeto).
Rodar: py "<caminho>/town_sublevels.py"
"""
import unreal, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_sublevels.log'
TOWN = '/Game/Library/Maps/Town/'
PLACE = {   # nome: (x, y, yaw) ; None = fora do mundo
    'L_Town_StripMall': (6500, 5400, 180),
    'L_Town_House_A': (-2700, 5750, 0),
    'L_Town_House_B': (-4700, 5750, 0),
    'L_Town_House_C': None,
    'L_Town_House_D': None,
    'L_Town_Trailer': None,
}

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def run():
    open(LOG, 'w').close()
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    have = {}
    for lv in unreal.EditorLevelUtils.get_levels(world):
        have[lv.get_outermost().get_name().split('/')[-1]] = lv
    for name, p in PLACE.items():
        if name in have:
            ok = unreal.EditorLevelUtils.remove_level_from_world(have[name])
            log('removed', name, ok)
        if p is None:
            continue
        x, y, yaw = p
        t = unreal.Transform(location=unreal.Vector(x, y, 0), rotation=unreal.Rotator(roll=0, pitch=0, yaw=yaw), scale=unreal.Vector(1, 1, 1))
        s = unreal.EditorLevelUtils.add_level_to_world_with_transform(world, TOWN + name, unreal.LevelStreamingAlwaysLoaded, t)
        log('added', name, p, s)
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).set_current_level_by_name('L_Library')
    pk = [p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() if p.get_name().startswith('/Game/Library')]
    unreal.EditorLoadingAndSavingUtils.save_packages(pk, True)
    log('saved', [p.get_name() for p in pk])

try:
    run()
except Exception:
    log(traceback.format_exc())
