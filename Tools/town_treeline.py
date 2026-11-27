"""Linha de pinheiros em volta da cidade (entre as casas e a caixa de nevoa), para o horizonte parecer
preenchido (mata ao fundo, silhuetas na nevoa). L_Library_Street, rotulos 'TL_'. Sem sombra e sem vento.
Idempotente e deterministico (semente fixa). Rodar: py "<caminho>/town_treeline.py"
"""
import unreal, random, math, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_treeline.log'
TREES = ('SM_Spruce_Tree_NN_01d', 'SM_Spruce_Tree_NN_01f', 'SM_Spruce_Tree_NN_01g', 'SM_Spruce_Tree_NN_01i')
# faixas (x0, x1, y0, y1, quantidade): fora das ruas e das casas, dentro da caixa (X -4100..9100, Y +-9200)
BANDS = [
    (-3800, 8800, 7300, 8800, 26),     # norte, atras das casas da Elm Street
    (-3800, 8800, -8800, -6200, 24),   # sul
    # (oeste fica fora do volume de nevoa, que nao pode entrar na livraria: arvores ali sairiam nitidas)
    (6800, 8900, -6000, 7000, 16),     # leste, atras do King Wash
]

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def run():
    open(LOG, 'w').close()
    random.seed(1996)
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    paths = {str(a.asset_name): str(a.package_name) for a in ar.get_assets_by_path('/Game/MERIDIAN/VOL55_KingWashStrip/Meshes/NN', recursive=True)}
    meshes = [unreal.load_asset(paths[t]) for t in TREES if t in paths]
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.set_current_level_by_name('L_Library_Street')
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('TL_'):
            eas.destroy_actor(a)
    n = 0
    for x0, x1, y0, y1, k in BANDS:
        for i in range(k):
            sm = random.choice(meshes); b = sm.get_bounding_box()
            s = random.uniform(1.0, 1.6)
            x = random.uniform(x0, x1); y = random.uniform(y0, y1)
            a = eas.spawn_actor_from_object(sm, unreal.Vector(x, y, -11 - b.min.z * s), unreal.Rotator(roll=0, pitch=0, yaw=random.uniform(0, 360)))
            a.set_actor_scale3d(unreal.Vector(s, s, s))
            a.set_actor_label('TL_Spruce'); a.set_folder_path('Town/Treeline')
            c = a.static_mesh_component
            c.set_cast_shadow(False)
            c.set_editor_property('evaluate_world_position_offset', False)
            n += 1
    les.set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)
    log('trees', n, 'meshes', len(meshes))

try:
    run()
except Exception:
    log(traceback.format_exc())
