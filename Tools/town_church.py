"""Igreja Sacred Pines (Meridian VOL12) como subnivel L_Town_Church, atras da fileira leste da Main Street:
a torre aparece por cima dos telhados (marco/bussola na nevoa, TOWN_PLAN). Enxuga como as casas
(sem luzes de dentro, sem decalques, sem moveis, sem sombra).
Antes: a copia do mapa e feita numa chamada separada (duplicar + abrir na mesma chamada derruba o editor).
Rodar: py "<caminho>/town_church.py"
"""
import unreal, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_church.log'
PK = '/Game/Library/Maps/Town/L_Town_Church'
LOC, YAW = (7300, -1800, 0), 0   # terreno X 4030..10720, Y -4227..645; torre (29 m) em (7616, -1654)
KEEP = ('Roof', 'Wall', 'Floor', 'Window', 'Door', 'Glass', 'Siding', 'Trim', 'Gutter', 'Chimney', 'Porch', 'Stair', 'Steeple', 'Tower',
        'Foundation', 'Column', 'Railing', 'Church', 'Exterior', 'Fence', 'Brick', 'Bell', 'Cross', 'Spire', 'Stained')

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def run():
    open(LOG, 'w').close()
    w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    have = {l.get_outermost().get_name(): l for l in unreal.EditorLevelUtils.get_levels(w)}
    if PK in have:
        unreal.EditorLevelUtils.remove_level_from_world(have[PK])
    t = unreal.Transform(location=unreal.Vector(*LOC), rotation=unreal.Rotator(roll=0, pitch=0, yaw=YAW), scale=unreal.Vector(1, 1, 1))
    unreal.EditorLevelUtils.add_level_to_world_with_transform(w, PK, unreal.LevelStreamingAlwaysLoaded, t)
    acts = [a for a in eas.get_all_level_actors() if a.get_level().get_outermost().get_name() == PK]
    big = [a.get_actor_bounds(False) for a in acts if isinstance(a, unreal.StaticMeshActor)]
    big = [(o, e) for (o, e) in big if e.x < 5000 and e.y < 5000]
    x0 = min(o.x - e.x for o, e in big); x1 = max(o.x + e.x for o, e in big)
    y0 = min(o.y - e.y for o, e in big); y1 = max(o.y + e.y for o, e in big)
    z1 = max(o.z + e.z for o, e in big)
    top = max(big, key=lambda b: b[0].z + b[1].z)
    log('bounds', round(x0), round(x1), round(y0), round(y1), 'top z', round(z1), 'top at', round(top[0].x), round(top[0].y))
    kl = kp = kd = ns = 0
    for a in acts:
        c = a.get_class().get_name()
        islight = isinstance(a, unreal.Light) or ('Light' in c and c.startswith('BP_')) or c.startswith('BP_Lamp')
        if islight:
            eas.destroy_actor(a); kl += 1; continue
        if isinstance(a, unreal.DecalActor):
            eas.destroy_actor(a); kd += 1; continue
        o, e = a.get_actor_bounds(False)
        inside = (x0 + 80 < o.x < x1 - 80) and (y0 + 80 < o.y < y1 - 80)
        if inside and isinstance(a, unreal.StaticMeshActor) and a.static_mesh_component.static_mesh:
            n = a.static_mesh_component.static_mesh.get_name()
            if not any(k in n for k in KEEP) and max(e.x, e.y, e.z) < 250:
                eas.destroy_actor(a); kp += 1; continue
        for comp in a.get_components_by_class(unreal.PrimitiveComponent):
            if comp.get_editor_property('cast_shadow'):
                comp.set_editor_property('cast_shadow', False); ns += 1
        if isinstance(a, unreal.StaticMeshActor):
            a.static_mesh_component.set_editor_property('evaluate_world_position_offset', False)
        a.modify()
    log('lights', kl, 'props', kp, 'decals', kd, 'noshadow', ns, 'left', len(acts) - kl - kp - kd)
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).set_current_level_by_name('L_Library')
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)
    log('saved')

try:
    run()
except Exception:
    log(traceback.format_exc())
