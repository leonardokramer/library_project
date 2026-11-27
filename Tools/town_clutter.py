"""Preenchimento da rua (docs/TOWN_ART_PASS.md): lixo e folhas na sarjeta, sacos e caixas junto aos predios,
mato na base das paredes e cercas, entulho nos becos, brinquedos e bicicletas nos quintais, janelas acesas
(abajur dentro das casas), letreiro DINER piscando. L_Library_Street, rotulos 'CL_'. Deterministico e idempotente.
Rodar: py "<caminho>/town_clutter.py"
"""
import unreal, random, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_clutter.log'
FIND = {}

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def pick(prefix):
    ks = sorted(k for k in FIND if k.startswith(prefix))
    return random.choice(ks) if ks else None

def run():
    open(LOG, 'w').close()
    random.seed(27111996)
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for root in ('/Game/MERIDIAN', '/Game/FENCES', '/Game/LIGHTING'):
        for ad in ar.get_assets_by_path(root, recursive=True):
            if str(ad.asset_class_path.asset_name) == 'StaticMesh' and '/LP/' not in str(ad.package_name):
                FIND.setdefault(str(ad.asset_name), str(ad.package_name))
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.set_current_level_by_name('L_Library_Street')
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('CL_'):
            eas.destroy_actor(a)
    n = [0]; miss = set()
    def put(prefix, x, y, ground, yaw=None, s=1.0, label='Clutter'):
        name = pick(prefix)
        if not name:
            miss.add(prefix); return None
        sm = unreal.load_asset(FIND[name]); b = sm.get_bounding_box()
        a = eas.spawn_actor_from_object(sm, unreal.Vector(x, y, ground - b.min.z * s),
                                        unreal.Rotator(roll=0, pitch=0, yaw=random.uniform(0, 360) if yaw is None else yaw))
        a.set_actor_scale3d(unreal.Vector(s, s, s)); a.set_actor_label('CL_' + label); a.set_folder_path('Town/Clutter')
        c = a.static_mesh_component
        c.set_cast_shadow(False); c.set_editor_property('evaluate_world_position_offset', False)
        c.set_editor_property('can_ever_affect_navigation', False)
        n[0] += 1
        return a
    SIDE, ROAD = 10, -11
    def yr(a, b):
        return random.uniform(a, b)
    # Main Street densa (2026-11-27 noite): fileiras de predios dos dois lados (X 1048 e 2480), cruzamento
    # da Elm Street (Y 3100..4300), becos em Y +-575 (livraria), -3600 (os dois lados) e 1325 (leste).
    RUNS = ((-4400, 3000), (4400, 6200))
    DOOR = (-80, 500)
    def ok_w(y):
        return not (DOOR[0] < y < DOOR[1]) and not (450 < y < 700 or -700 < y < -450)
    # 1) sarjetas: folhas, lixo e entulho junto ao meio-fio (dos dois lados)
    for (y0, y1) in RUNS:
        y = y0
        while y < y1:
            for x in (yr(1372, 1400), yr(2128, 2156)):
                if random.random() < 0.7:
                    put(random.choice(['SM_Dead_Leaf_Pile', 'SM_Trash_Scatter', 'SM_Nature_Debris', 'SM_Trash_Debris_Ground']), x, y + yr(-60, 60), ROAD, label='Gutter')
            y += yr(200, 360)
    # 2) calcada da livraria: sacos, lixeiras, caixas, jornais junto as lojas
    for i in range(30):
        y = yr(*random.choice(RUNS))
        if not ok_w(y):
            continue
        put(random.choice(['SM_Trashbags_NN', 'SM_Cardboard_Box', 'SM_Cardboard_NN', 'SM_Paper_Bags', 'SM_Newspapers', 'SM_Trashcan_NN', 'SM_Recycle_Bin']),
            yr(1065, 1120), y, SIDE, label='Sidewalk')
    # 3) calcada da frente
    for i in range(30):
        put(random.choice(['SM_Trashbags_NN', 'SM_Trashcan_NN', 'SM_Recycle_Bin', 'SM_Cardboard_Box', 'SM_Newspaper_Stand', 'SM_Power_Boxes', 'SM_Mailbox_NN', 'SM_Paper_Bags']),
            yr(2400, 2460), yr(*random.choice(RUNS)), SIDE, label='FarSidewalk')
    # 4) capim baixo na base das fachadas e nas frestas (nada grande: atravessava a porta)
    for i in range(70):
        y = yr(*random.choice(RUNS))
        if random.random() < 0.5:
            if not ok_w(y):
                continue
            x = yr(1050, 1070)
        else:
            x = yr(2462, 2478)
        put(random.choice(['SM_WildGrass_NN', 'SM_FieldGrass']), x, y, SIDE, label='Weeds')
    # 5) becos: entulho, caixas, sacos, escada, cacamba, mato
    for (yc, x0, x1) in ((575, -50, 950), (-575, -50, 950), (-2000, -50, 950), (-2000, 2580, 3700)):
        for i in range(8):
            put(random.choice(['SM_Trashbags_NN', 'SM_Cardboard_Box_Set2', 'SM_Debris_Pile', 'SM_Rock_Debris_Pile', 'SM_Boxes_NN', 'SM_Trash_Set_NN', 'SM_Dead_Leaf_Pile', 'SM_Scraggly_Bush', 'SM_WildGrass_NN']),
                yr(x0, x1), yc + yr(-80, 80), SIDE - 1, label='Alley')
    put('SM_Metal_Ladder_NN', 300, 675, SIDE - 1, yaw=0, label='Alley')
    put('SM_Trash_Plastic_Dumpster', 500, -600, SIDE - 1, yaw=90, label='Alley')
    put('SM_Trash_Plastic_Dumpster', 3000, -2000, SIDE - 1, yaw=90, label='Alley')
    # 6) quintais das casas da Elm Street (a oeste)
    for (hx, hy) in ((-2700, 4650), (-4700, 4650)):
        for i in range(4):
            put(random.choice(['SM_Bicycle_NN', 'SM_Trashcans_NN', 'SM_Hose_Set_NN', 'SM_Recycle_Bin', 'SM_Kids_Bikes_NN']),
                hx + yr(-600, 600), hy + yr(-150, 150), ROAD, label='Yard')
    les.set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)
    log('placed', n[0], 'missing', sorted(miss))

try:
    run()
except Exception:
    log(traceback.format_exc())
