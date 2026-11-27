"""Otimiza a cidade de fora:
1) no L_Town_StripMall, apaga os objetos pequenos de dentro da loja (so se ve a casca pela janela, na nevoa);
2) tira a sombra de todas as luzes dos subniveis da cidade.
Rodar: py "<caminho>/town_optimize.py" [dry]
"""
import unreal, sys, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_optimize.log'
DRY = 'dry' in sys.argv
KEEP = ('LM_', 'Roof', 'Wall', 'Floor', 'Column', 'Door', 'Window', 'Glass', 'Neon', 'King_Wash', 'Sign', 'Gutter', 'Blinds', 'Drop_Ceiling', 'Awning')

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def run():
    open(LOG, 'w').close()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    acts = eas.get_all_level_actors()
    sm_lvl = '/Game/Library/Maps/Town/L_Town_StripMall'
    town = [a for a in acts if '/Town/' in a.get_level().get_outermost().get_name()]
    mall = [a for a in town if a.get_level().get_outermost().get_name() == sm_lvl]
    roofs = []
    for a in mall:
        if isinstance(a, unreal.StaticMeshActor) and a.static_mesh_component.static_mesh:
            n = a.static_mesh_component.static_mesh.get_name()
            o, e = a.get_actor_bounds(False)
            if 'LM_Roof' in n and 'Pole' not in n and o.z > 250:
                roofs.append((o, e))
    x0 = min(o.x - e.x for o, e in roofs); x1 = max(o.x + e.x for o, e in roofs)
    y0 = min(o.y - e.y for o, e in roofs); y1 = max(o.y + e.y for o, e in roofs)
    ztop = min(o.z - e.z for o, e in roofs)
    log('footprint', round(x0), round(x1), round(y0), round(y1), 'roof z', round(ztop), 'roofs', len(roofs))
    m = 60
    killed = 0
    for a in mall:
        o, e = a.get_actor_bounds(False)
        inside = (x0 + m < o.x < x1 - m) and (y0 + m < o.y < y1 - m) and o.z < ztop
        if not inside:
            continue
        name = a.get_actor_label()
        mesh = ''
        if isinstance(a, unreal.StaticMeshActor) and a.static_mesh_component.static_mesh:
            mesh = a.static_mesh_component.static_mesh.get_name()
        elif not isinstance(a, (unreal.DecalActor,)) and not a.get_class().get_name().startswith('BP_'):
            continue
        if any(k in mesh for k in KEEP):
            continue
        if max(e.x, e.y, e.z) > 220:
            continue
        killed += 1
        if not DRY:
            eas.destroy_actor(a)
    log('interior props removed', killed, 'dry' if DRY else '')
    ns = 0
    for a in town:
        for c in a.get_components_by_class(unreal.LightComponent):
            if c.cast_shadows:
                ns += 1
                if not DRY:
                    c.set_cast_shadows(False)
                    a.modify()
    log('lights shadow off', ns)
    # decalques do strip mall (passo CompositionBeforeBasePass) e vegetacao sem sombra nem vento
    nd = nf = 0
    for a in mall:
        if isinstance(a, unreal.DecalActor):
            nd += 1
            if not DRY:
                eas.destroy_actor(a)
            continue
        if isinstance(a, unreal.StaticMeshActor) and a.static_mesh_component.static_mesh:
            n = a.static_mesh_component.static_mesh.get_name()
            if any(k in n for k in ('Spruce', 'Shrub', 'Scraggly', 'Grass', 'Dandelion', 'Elm_Seedling', 'Leaf', 'Nature', 'Root', 'Palm', 'Plants')):
                nf += 1
                if not DRY:
                    c = a.static_mesh_component
                    c.set_editor_property('cast_shadow', False)
                    c.set_editor_property('evaluate_world_position_offset', False)
                    a.modify()
    log('decals removed', nd, 'foliage no-shadow/no-wpo', nf)
    # o relogio move o sol a cada quadro: a sombra de tudo que projeta e refeita sempre.
    # O strip mall fica a 20-40 m na nevoa: sem sombra.
    ns2 = 0
    for a in mall:
        for c in a.get_components_by_class(unreal.PrimitiveComponent):
            if c.get_editor_property('cast_shadow'):
                ns2 += 1
                if not DRY:
                    c.set_editor_property('cast_shadow', False)
                    a.modify()
    log('stripmall primitives no-shadow', ns2)
    if not DRY:
        unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)  # so o que e nosso (nunca Stationer/pacotes)
        log('saved')

try:
    run()
except Exception:
    log(traceback.format_exc())

