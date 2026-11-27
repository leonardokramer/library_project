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
    # 1) sarjetas: folhas, lixo e entulho junto ao meio-fio (dos dois lados), antes e depois do cruzamento
    for (y0, y1) in ((-3100, 3150), (4150, 7600)):
        y = y0
        while y < y1:
            for x in (yr(1372, 1400), yr(2128, 2156)):
                if random.random() < 0.75:
                    put(random.choice(['SM_Dead_Leaf_Pile', 'SM_Trash_Scatter', 'SM_Nature_Debris', 'SM_Trash_Debris_Ground']), x, y + yr(-60, 60), ROAD, label='Gutter')
            y += yr(180, 320)
    # 2) calcada do lado da livraria: sacos, lixeiras, caixas junto as lojas fechadas e aos becos
    for (y0, y1, k) in ((470, 690, 5), (-690, -470, 5), (760, 1650, 7), (-1750, -760, 7)):
        for i in range(k):
            put(random.choice(['SM_Trashbags_NN', 'SM_Cardboard_Box', 'SM_Cardboard_NN', 'SM_Paper_Bags', 'SM_Newspapers', 'SM_Trashcan_NN', 'SM_Recycle_Bin']),
                yr(1060, 1130), yr(y0, y1), SIDE, label='Sidewalk')
    # 3) calcada do outro lado
    for i in range(14):
        put(random.choice(['SM_Trashbags_NN', 'SM_Trashcan_NN', 'SM_Recycle_Bin', 'SM_Cardboard_Box', 'SM_Newspaper_Stand', 'SM_Power_Boxes', 'SM_Mailbox_NN']),
            yr(2390, 2460), yr(-3000, 3100), SIDE, label='FarSidewalk')
    # 4) mato na base das paredes, das cercas e nos terrenos
    for i in range(60):
        side = random.random()
        if side < 0.35:
            x, y, g = yr(1050, 1075), yr(-3100, 3150), SIDE           # base das fachadas
        elif side < 0.6:
            x, y, g = yr(2465, 2490), yr(-3100, 3100), SIDE           # beira da calcada da frente
        else:
            x, y, g = yr(-1600, 1000), random.choice([yr(-5500, -1900), yr(1750, 3250)]), ROAD  # terrenos
        if side < 0.6:
            # base das fachadas e beira da calcada: so capim baixo (arbusto grande atravessava a porta);
            # nunca na frente da porta da livraria (Y -60..480)
            if side < 0.35 and -60 < y < 480:
                continue
            put(random.choice(['SM_WildGrass_NN', 'SM_FieldGrass']), x, y, g, label='Weeds')
            continue
        put(random.choice(['SM_WildGrass_NN', 'SM_FieldGrass', 'SM_Scraggly_Bush', 'SM_Shrub_NN', 'SM_Boxwood_Bush', 'SM_HederaShrub']), x, y, g, label='Weeds')
    # 5) becos: entulho, caixas, sacos, escada, cacamba plastica
    for yc, sgn in ((575, 1), (-575, -1)):
        for i in range(9):
            put(random.choice(['SM_Trashbags_NN', 'SM_Cardboard_Box_Set2', 'SM_Debris_Pile', 'SM_Rock_Debris_Pile', 'SM_Boxes_NN', 'SM_Trash_Set_NN', 'SM_Dead_Leaf_Pile']),
                yr(-50, 950), yc + yr(-90, 90), SIDE - 1, label='Alley')
        put('SM_Metal_Ladder_NN', 300, yc + sgn * 100, SIDE - 1, yaw=0, label='Alley')
    put('SM_Trash_Plastic_Dumpster', 500, -600, SIDE - 1, yaw=90, label='Alley')
    # 6) quintais: trailer (sul) e casas (bicicletas, brinquedos, churrasqueira, lixeiras)
    for i in range(12):
        put(random.choice(['SM_Kids_Bikes_NN', 'SM_Old_Bike_NN', 'SM_Toys_NN', 'SM_Toy_Set_NN', 'SM_Grill_NN', 'SM_Laundry_Bins_NN', 'SM_Garden_Boxes_NN', 'SM_Chair_Outdoor_NN', 'SM_Trashcans_NN']),
            yr(-900, 900), yr(-5200, -2200), ROAD, label='Yard')
    for (hx, hy) in ((-300, 4600), (3500, 4600), (800, 2500)):
        for i in range(4):
            put(random.choice(['SM_Bicycle_NN', 'SM_Trashcans_NN', 'SM_Hose_Set_NN', 'SM_Recycle_Bin', 'SM_Flower_Boxes_NN']),
                hx + yr(-500, 500), hy + yr(-200, 200), ROAD, label='Yard')
    # 7) janelas acesas: abajur + luz quente fraca dentro de algumas casas (luz com luminaria visivel)
    lamps = [(-300, 5250, 300), (3500, 5250, 300), (180, 2510, 280), (3300, -3900, 280)]
    for (x, y, z) in lamps:
        put('SM_Lamp_Standing_NN', x, y, z - 150, label='WindowLamp')
        l = eas.spawn_actor_from_class(unreal.PointLight, unreal.Vector(x, y, z))
        c = l.get_component_by_class(unreal.PointLightComponent)
        c.set_intensity(60.0); c.set_attenuation_radius(700); c.set_light_color(unreal.LinearColor(1.0, 0.62, 0.32, 1)); c.set_cast_shadows(False)
        l.set_actor_label('CL_WindowLight'); l.set_folder_path('Town/Clutter')
    les.set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)
    log('placed', n[0], 'missing', sorted(miss))

try:
    run()
except Exception:
    log(traceback.format_exc())
