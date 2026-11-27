"""Monta a rua em frente a livraria no subnivel /Game/Library/Maps/Town/L_Library_Street.
Idempotente: apaga os atores com rotulo 'ST_' do subnivel e recria tudo.
Rodar no console do editor: py "<caminho>/town_street.py"
Coordenadas: fachada leste da livraria em X 1048, soleira Z 10. A rua corre em Y (norte = +Y).
"""
import unreal, traceback

LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_street.log'
STREET_LVL = '/Game/Library/Maps/Town/L_Library_Street'
MAT_DIR = '/Game/Library/Materials/Town'

FIND = {}

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

SW = '/Game/BUILDINGS/VOL13_Sidewalks/Meshes/'
RM = '/Game/REALISTIC_MATERIALS/VOL6_RoadSidewalk/Materials/'
PLANE = '/Engine/BasicShapes/Plane'

# --- geometria (cm) ---
FACADE_X = 1048
SIDE_Z = -11          # base das placas de calcada (topo = Z 10, na soleira)
STREET_Z = -11        # superficie do asfalto
CURB_X = 1349         # comeco do meio-fio da calcada da livraria
STREET_X0, STREET_X1 = 1364, 2164
Y0, Y1 = -3200, 3200  # extensao das calcadas
STREET_Y0, STREET_Y1 = -8000, 8000


def mi(name, parent, scalars):
    """Cria (ou atualiza) um MI nosso filho de um MI da Dekogon."""
    path = MAT_DIR + '/' + name
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        m = unreal.load_asset(path)
    else:
        tools = unreal.AssetToolsHelpers.get_asset_tools()
        m = tools.create_asset(name, MAT_DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    m.set_editor_property('parent', unreal.load_asset(parent))
    for k, v in scalars.items():
        unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(m, k, v)
    unreal.EditorAssetLibrary.save_asset(path, False)
    return m


def run():
    open(LOG, 'w').close()
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for root in ('/Game/BUILDINGS', '/Game/MERIDIAN', '/Game/LIGHTING'):
        for ad in ar.get_assets_by_path(root, recursive=True):
            if '/LP/' not in str(ad.package_name):
                FIND[str(ad.asset_name)] = str(ad.package_name)
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    # subnivel
    lvls = {l.get_outermost().get_name(): l for l in unreal.EditorLevelUtils.get_levels(world)}
    if STREET_LVL not in lvls:
        if unreal.EditorAssetLibrary.does_asset_exist(STREET_LVL):
            unreal.EditorLevelUtils.add_level_to_world(world, STREET_LVL, unreal.LevelStreamingAlwaysLoaded)
        else:
            unreal.EditorLevelUtils.create_new_streaming_level(unreal.LevelStreamingAlwaysLoaded, STREET_LVL, False)
        lvls = {l.get_outermost().get_name(): l for l in unreal.EditorLevelUtils.get_levels(world)}
    lvl = lvls[STREET_LVL]
    les.set_current_level_by_name('L_Library_Street')

    for a in eas.get_all_level_actors():
        if a.get_level() == lvl and a.get_actor_label().startswith('ST_'):
            eas.destroy_actor(a)

    m_road = mi('MI_Town_Road', RM + 'MI_Road_01a', {'Texture Coord': 2.0})
    m_ground = mi('MI_Town_Ground', RM + 'MI_Asphalt_Cracked_01a', {'Texture Coord': 6.0})

    n = [0]
    def put(mesh, loc, yaw=0.0, scale=(1, 1, 1), label='piece', mat=None, folder='Town/Street'):
        sm = unreal.load_asset(mesh if mesh.startswith('/Engine') else FIND[mesh.split('/')[-1]])
        a = eas.spawn_actor_from_object(sm, unreal.Vector(*loc), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_scale3d(unreal.Vector(*scale))
        n[0] += 1
        a.set_actor_label('ST_%s_%03d' % (label, n[0]))
        a.set_folder_path(folder)
        if mat:
            a.static_mesh_component.set_material(0, mat)
        return a

    # calcada da livraria (yaw 90: a peca ocupa X [x0, x0+largura], Y [y0-400, y0])
    for y in range(Y0 + 400, Y1 + 1, 400):
        put(SW + 'SM_GS_Sidewalk_400_04a', (FACADE_X, y, SIDE_Z), 90, label='SideA')
        put(SW + 'SM_GS_Sidewalk_400_01a', (FACADE_X + 201, y, SIDE_Z), 90, label='SideA')
        put(SW + 'SM_GS_Sidewalk_400_05a', (CURB_X, y, SIDE_Z), 90, label='CurbA')
    # calcada do outro lado (yaw -90: X [x0-largura, x0], Y [y0, y0+400])
    for y in range(Y0, Y1, 400):
        put(SW + 'SM_GS_Sidewalk_400_05a', (STREET_X1 + 15, y, SIDE_Z), -90, label='CurbB')
        put(SW + 'SM_GS_Sidewalk_400_04a', (STREET_X1 + 15 + 201, y, SIDE_Z), -90, label='SideB')
        put(SW + 'SM_GS_Sidewalk_400_01a', (STREET_X1 + 15 + 201 + 100, y, SIDE_Z), -90, label='SideB')

    # asfalto da rua: placas de 8 x 8 m
    w = STREET_X1 - STREET_X0
    for y in range(STREET_Y0, STREET_Y1, 800):
        put(PLANE, ((STREET_X0 + STREET_X1) / 2.0, y + 400, STREET_Z), 0, (w / 100.0, 8.0, 1), 'Road', m_road)
    # chao geral (estacionamento, terrenos), um pouco abaixo da rua
    put(PLANE, (6000, 0, STREET_Z - 1), 0, (90.0, 160.0, 1), 'Ground', m_ground)

    les.set_current_level_by_name('L_Library')
    log('spawned', n[0])
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)  # so o que e nosso (nunca Stationer/pacotes)
    log('saved')

try:
    run()
except Exception:
    log(traceback.format_exc())



