"""Estaciona carros na rua copiando os carros montados (grupos de pecas) do estacionamento do King Wash.
Os carros novos vao para o L_Library_Street com rotulo 'CAR_'. Idempotente. Rodar: py "<caminho>/town_cars.py"
"""
import unreal, math, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_cars.log'
BODIES = ('SM_Car_24a', 'SM_Wagon_01a', 'SM_Van_02a')
# (corpo, x, y, yaw do carro na rua). Rua: X 1364..2164; meio-fio da livraria em 1364, do outro lado 2164.
TARGETS = [('SM_Car_24a', 1560, -1050, 90), ('SM_Wagon_01a', 1600, 2400, 90), ('SM_Van_02a', 2045, -2350, -90)]

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def run():
    open(LOG, 'w').close()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    acts = eas.get_all_level_actors()
    for a in acts:
        if a.get_actor_label().startswith('CAR_'):
            eas.destroy_actor(a)
    acts = eas.get_all_level_actors()
    mall = [a for a in acts if a.get_level().get_outermost().get_name().endswith('L_Town_StripMall')]
    bodies = {}
    for a in mall:
        if isinstance(a, unreal.StaticMeshActor) and a.static_mesh_component.static_mesh:
            n = a.static_mesh_component.static_mesh.get_name()
            if n in BODIES and n not in bodies:
                bodies[n] = a
    log('bodies', {k: v.get_actor_label() for k, v in bodies.items()})
    les.set_current_level_by_name('L_Library_Street')
    for name, tx, ty, tyaw in TARGETS:
        body = bodies.get(name)
        if not body:
            log('no body', name); continue
        bl = body.get_actor_location(); byaw = body.get_actor_rotation().yaw
        # pecas do carro: atores de malha do mesmo pacote de veiculo a ate 3,5 m do corpo
        prefix = name.rsplit('_', 1)[0]
        parts = [a for a in mall if isinstance(a, unreal.StaticMeshActor) and a.static_mesh_component.static_mesh
                 and a.static_mesh_component.static_mesh.get_name().startswith(prefix)
                 and (a.get_actor_location() - bl).length() < 350]
        dyaw = tyaw - byaw
        c, s = math.cos(math.radians(dyaw)), math.sin(math.radians(dyaw))
        for p in parts:
            pl = p.get_actor_location() - bl
            nl = unreal.Vector(tx + pl.x * c - pl.y * s, ty + pl.x * s + pl.y * c, -11 + (p.get_actor_location().z - bl.z) + (bl.z - 0))
            r = p.get_actor_rotation()
            sm = p.static_mesh_component.static_mesh
            n = eas.spawn_actor_from_object(sm, nl, unreal.Rotator(roll=r.roll, pitch=r.pitch, yaw=r.yaw + dyaw))
            n.set_actor_scale3d(p.get_actor_scale3d())
            for i in range(p.static_mesh_component.get_num_materials()):
                n.static_mesh_component.set_material(i, p.static_mesh_component.get_material(i))
            n.set_actor_label('CAR_%s_%s' % (name, sm.get_name()))
            n.set_folder_path('Town/Cars')
        log(name, 'parts', len(parts), 'body z', round(bl.z))
    les.set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)  # so o que e nosso (nunca Stationer/pacotes)
    log('done')

try:
    run()
except Exception:
    log(traceback.format_exc())


