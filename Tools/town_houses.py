"""Casas do Meridian 55 Elm Street (copias L_Town_House_A/B/C) como subniveis da L_Library, com transform,
e enxugadas para o desempenho (so a casca e o quintal). Idempotente: se o subnivel ja existe, so enxuga.
Rodar: py "<caminho>/town_houses.py"
A casa original tem a frente para -Y (caixa de correio em y -1264), X -901..819, Y -1358..1381, altura ~12 m.
"""
import unreal, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_houses.log'
HOUSES = {
    # Elm Street, lado norte, a oeste da Main Street, frente para a rua (-Y). Desde 2026-11-27 (noite, Main Street densa)
    # as casas C e D e o trailer ficaram fora do mundo (veja town_sublevels.py); os mapas continuam no projeto.
    'L_Town_House_A': ((-2700, 5750, 0), 0),
    'L_Town_House_B': ((-4700, 5750, 0), 0),
}
KEEP = ('Roof', 'Wall', 'Floor', 'Window', 'Door', 'Glass', 'Siding', 'Trim', 'Gutter', 'Chimney', 'Porch', 'Stair',
        'Foundation', 'Column', 'Railing', 'Building_55a', 'Exterior', 'Fence', 'Mailbox', 'Blinds', 'Curtain')

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def run():
    open(LOG, 'w').close()
    w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    have = [l.get_outermost().get_name() for l in unreal.EditorLevelUtils.get_levels(w)]
    for name, (loc, yaw) in HOUSES.items():
        pk = '/Game/Library/Maps/Town/' + name
        if pk not in have:
            t = unreal.Transform(location=unreal.Vector(*loc), rotation=unreal.Rotator(roll=0, pitch=0, yaw=yaw), scale=unreal.Vector(1, 1, 1))
            unreal.EditorLevelUtils.add_level_to_world_with_transform(w, pk, unreal.LevelStreamingAlwaysLoaded, t)
            log('added', name)
        acts = [a for a in eas.get_all_level_actors() if a.get_level().get_outermost().get_name() == pk]
        roofs = []
        for a in acts:
            if isinstance(a, unreal.StaticMeshActor) and a.static_mesh_component.static_mesh and 'Roof' in a.static_mesh_component.static_mesh.get_name():
                o, e = a.get_actor_bounds(False)
                if o.z > 450:
                    roofs.append((o, e))
        if not roofs:   # trailer: o "telhado" e a propria casca Mobile_Home_14a
            for a in acts:
                if isinstance(a, unreal.StaticMeshActor) and a.static_mesh_component.static_mesh and 'Mobile_Home_14a' in a.static_mesh_component.static_mesh.get_name():
                    roofs.append(a.get_actor_bounds(False))
        x0 = min(o.x - e.x for o, e in roofs); x1 = max(o.x + e.x for o, e in roofs)
        y0 = min(o.y - e.y for o, e in roofs); y1 = max(o.y + e.y for o, e in roofs)
        kl = kp = kd = ns = 0
        for a in acts:
            c = a.get_class().get_name()
            islight = isinstance(a, unreal.Light) or ('Light' in c and c.startswith('BP_')) or c.startswith('BP_Lamp') or 'Ceiling' in c
            if islight and 'Exterior' not in c:
                eas.destroy_actor(a); kl += 1; continue
            if isinstance(a, unreal.DecalActor):
                eas.destroy_actor(a); kd += 1; continue
            o, e = a.get_actor_bounds(False)
            inside = (x0 + 60 < o.x < x1 - 60) and (y0 + 60 < o.y < y1 - 60)
            if inside and isinstance(a, unreal.StaticMeshActor) and a.static_mesh_component.static_mesh:
                n = a.static_mesh_component.static_mesh.get_name()
                if not any(k in n for k in KEEP) and max(e.x, e.y, e.z) < 220:
                    eas.destroy_actor(a); kp += 1; continue
            for comp in a.get_components_by_class(unreal.PrimitiveComponent):
                if comp.get_editor_property('cast_shadow'):
                    comp.set_editor_property('cast_shadow', False); ns += 1
            for comp in a.get_components_by_class(unreal.LightComponent):
                comp.set_cast_shadows(False)
            if isinstance(a, unreal.StaticMeshActor):
                a.static_mesh_component.set_editor_property('evaluate_world_position_offset', False)
            a.modify()
        log(name, 'lights', kl, 'props', kp, 'decals', kd, 'noshadow', ns, 'roof box', round(x0), round(x1), round(y0), round(y1))
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)
    log('saved')

try:
    run()
except Exception:
    log(traceback.format_exc())
