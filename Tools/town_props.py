"""Luminarias, postes e objetos de calcada no subnivel L_Library_Street (rotulos 'PR_').
Idempotente. Rodar: py "<caminho>/town_props.py"
Cada objeto e apoiado no chao pelo bounding box (z = chao - min.z).
"""
import unreal, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_props.log'
SIDE_TOP = 10      # topo da calcada
STREET = -11       # asfalto
FIND = {}

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def pick(prefix):
    ks = sorted(k for k in FIND if k.startswith(prefix) and FIND[k].count('/LP/') == 0) or sorted(k for k in FIND if k.startswith(prefix))
    log('pick', prefix, ks[:6])
    return ks[0]

def mesh(n):
    return unreal.load_asset(FIND[n])

def run():
    open(LOG, 'w').close()
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for root in ('/Game/BUILDINGS', '/Game/MERIDIAN', '/Game/LIGHTING', '/Game/Library/Meshes/Town', '/Game/Vehicles'):
        for ad in ar.get_assets_by_path(root, recursive=True):
            n = str(ad.asset_name)
            if str(ad.asset_class_path.asset_name) != 'StaticMesh':
                continue
            if '/LP/' not in str(ad.package_name) or n not in FIND:
                FIND[n] = str(ad.package_name)
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les.set_current_level_by_name('L_Library_Street')
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('PR_') or a.get_actor_label() == 'FC_SM_BookReturn':
            eas.destroy_actor(a)
    cnt = [0]
    def put(n, x, y, yaw=0.0, ground=SIDE_TOP, z=None, label=None, folder='Town/Props', scale=1.0):
        sm = mesh(n)
        b = sm.get_bounding_box()
        zz = z if z is not None else ground - b.min.z * scale
        a = eas.spawn_actor_from_object(sm, unreal.Vector(x, y, zz), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_scale3d(unreal.Vector(scale, scale, scale))
        cnt[0] += 1
        a.set_actor_label('PR_%s_%02d' % (label or n.replace('SM_', ''), cnt[0]))
        a.set_folder_path(folder)
        return a, b
    def light(kind, loc, rot, intensity, radius, color=(1.0, 0.78, 0.5), shadows=False, label='Light', cone=None):
        cls = unreal.SpotLight if kind == 'spot' else unreal.PointLight
        a = eas.spawn_actor_from_class(cls, unreal.Vector(*loc), unreal.Rotator(roll=0, pitch=rot[0], yaw=rot[1]))
        c = a.get_component_by_class(unreal.SpotLightComponent if kind == 'spot' else unreal.PointLightComponent)
        c.set_mobility(unreal.ComponentMobility.MOVABLE)
        c.set_editor_property('intensity_units', unreal.LightUnits.CANDELAS)
        c.set_intensity(intensity)
        c.set_attenuation_radius(radius)
        c.set_light_color(unreal.LinearColor(*color, 1))
        c.set_cast_shadows(shadows)
        if cone:
            c.set_inner_cone_angle(cone[0]); c.set_outer_cone_angle(cone[1])
        cnt[0] += 1
        a.set_actor_label('PR_%s_%02d' % (label, cnt[0]))
        a.set_folder_path('Town/Lights')
        return a

    WX = 1050
    # lanternas de carruagem dos dois lados da porta (porta: Y 164..251)
    for y in (128, 290):
        put('SM_Lights_Outdoor_NN_18a', WX, y, 0, z=205, label='DoorLantern', folder='Town/Facade')
        light('point', (WX + 14, y, 222), (0, 0), 30, 700, label='DoorLanternLight')
    # holofotes do letreiro (pequenos, presos na capa da faixa)
    for y in (-300, 0, 300):
        put('SM_Light_Set_NN_61a', WX + 14, y, 0, z=375, label='SignLamp', folder='Town/Facade')
        light('spot', (WX + 30, y, 372), (-100, 0), 90, 360, label='SignLampLight', cone=(30, 55))

    # postes de madeira com luminaria de rua (lado da livraria e lado de la)
    poles = [(1325, -1500, 0), (1325, 1700, 0), (2200, 250, 180), (2200, -3000, 180), (2200, 3300, 180)]
    for x, y, yaw in poles:
        a, b = put('SM_Electric_Poles_Set_01a', x, y, yaw, label='Pole')
        top = SIDE_TOP + (b.max.z - b.min.z)
        hz = top - 260
        sgn = 1 if yaw == 0 else -1
        put('SM_Light_Set_NN_61e', x + sgn * 10, y, yaw, z=hz, label='StreetHead')
        light('spot', (x + sgn * 95, y, hz - 15), (-80, yaw), 900, 2600, color=(1.0, 0.72, 0.42),
              shadows=(y == 250 or y == -1500), label='StreetLight', cone=(30, 62))
    # objetos de calcada (lado da livraria)
    put('SM_BookReturn', 1105, 330, 0, label='BookReturn', folder='Town/Facade')
    put(pick('SM_Fire_Hydrant'), 1300, -620, 30, label='Hydrant')
    put(pick('SM_Newspaper_Stand_Set_NN_01a'), 1290, -260, -90, label='NewsStand')
    put(pick('SM_Trashcan_Set_NN'), 1300, 620, 0, label='Trash')
    put(pick('SM_Bench_Wooden_NN'), 1110, -300, 90, label='Bench')
    put(pick('SM_Signs_Street_NN'), 1320, 900, 0, label='StreetSign')
    # carros: ver Tools/town_cars.py (copia os grupos montados do estacionamento do King Wash)
    les.set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)  # so o que e nosso (nunca Stationer/pacotes)
    log('done', cnt[0])

try:
    run()
except Exception:
    log(traceback.format_exc())



