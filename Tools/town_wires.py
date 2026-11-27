"""Fios entre os postes de madeira (CableActor) no L_Library_Street (rotulos 'WR_') e postes extras
que levam os fios para dentro da nevoa. Idempotente. Rodar: py "<caminho>/town_wires.py"
"""
import unreal, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_wires.log'

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def run():
    open(LOG, 'w').close()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.set_current_level_by_name('L_Library_Street')
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('WR_'):
            eas.destroy_actor(a)
    poles = [a for a in eas.get_all_level_actors() if a.get_actor_label().startswith('PR_Pole')]
    if not poles:
        log('no poles'); return
    sm = poles[0].static_mesh_component.static_mesh
    b = sm.get_bounding_box()
    log('pole bounds', b.min, b.max)
    # postes extras para os fios sumirem na nevoa
    extra = [(1325, -4700, 0), (1325, 4900, 0), (2200, -6300, 180), (2200, 6600, 180)]
    for x, y, yaw in extra:
        a = eas.spawn_actor_from_object(sm, unreal.Vector(x, y, 10 - b.min.z), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_label('WR_PoleFar'); a.set_folder_path('Town/Props')
        poles.append(a)
    top = 10 + (b.max.z - b.min.z)
    sides = {}
    for p in poles:
        l = p.get_actor_location()
        sides.setdefault(round(l.x), []).append(l)
    wire_mat = unreal.load_asset('/Game/Library/Materials/Town/MI_Town_Metal')
    n = 0
    for x, pts in sides.items():
        pts.sort(key=lambda v: v.y)
        for i in range(len(pts) - 1):
            a0, a1 = pts[i], pts[i + 1]
            for k, (dz, dx) in enumerate(((-45, -35), (-45, 35), (-85, 0))):
                start = unreal.Vector(a0.x + dx, a0.y, top + dz)
                end = unreal.Vector(a1.x + dx, a1.y, top + dz)
                c = eas.spawn_actor_from_class(unreal.CableActor, start)
                comp = c.get_component_by_class(unreal.CableComponent)
                span = (end - start).length()
                comp.set_editor_property('end_location', end - start)
                comp.set_editor_property('cable_length', span * 1.015)
                comp.set_editor_property('num_segments', 16)
                comp.set_editor_property('cable_width', 1.6)
                comp.set_editor_property('num_sides', 4)
                comp.set_editor_property('solver_iterations', 2)
                comp.set_editor_property('cast_shadow', False)
                comp.set_editor_property('enable_stiffness', False)
                try:
                    comp.set_editor_property('b_attach_start', True)
                except Exception:
                    pass
                if wire_mat:
                    comp.set_material(0, wire_mat)
                c.set_actor_label('WR_Wire'); c.set_folder_path('Town/Wires')
                n += 1
    les.set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)
    log('wires', n, 'sides', {k: len(v) for k, v in sides.items()})

try:
    run()
except Exception:
    log(traceback.format_exc())
