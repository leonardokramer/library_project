"""Reposiciona os componentes do BP_OutsideFog para a rua aberta (vilarejo na nevoa).
Edita os templates do Blueprint (SCS), compila e salva. Rodar no console: py "<caminho>/town_fog.py"
Posicoes relativas ao ator (que fica em X 1050, Y 0, Z 0).
"""
import unreal, traceback
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\town_fog.log'
BP = '/Game/Library/Blueprints/BP_OutsideFog'

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

# nome: (rel_loc, rel_scale, extra)
LAYOUT = {
    # paredes e teto de nevoa dentro do volume de nevoa (ate 30 m), para tudo fundir na mesma cor
    'FogFar':   ((6400, 0, 1250),     (26.0, 150.0, 1.0)),
    'FogNorth': ((3000, 6800, 1250),  (72.0, 26.0, 1.0)),
    'FogSouth': ((3000, -6800, 1250), (72.0, 26.0, 1.0)),
    'FogTop':   ((3000, 0, 2500),     (72.0, 150.0, 1.0)),
    # elipsoide: a borda oeste encosta na fachada (X 1050), as paredes ficam dentro
    'LocalFog': ((5200, 0, 0),        (52.0, 78.0, 30.0)),
}
BLOCKS = {
    # caixas que limitam onde o jogador anda la fora: calcadas e a rua ate a calcada da frente
    'BlockEast':  ((1500, 0, 200),   (60, 2400, 200)),
    'BlockNorth': ((700, 2400, 200), (760, 60, 200)),
    'BlockSouth': ((700, -2400, 200), (760, 60, 200)),
}

def run():
    open(LOG, 'w').close()
    bp = unreal.load_asset(BP)
    sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handles = sds.k2_gather_subobject_data_for_blueprint(bp)
    lib = unreal.SubobjectDataBlueprintFunctionLibrary
    for h in handles:
        data = lib.get_data(h)
        obj = lib.get_object(data)
        if obj is None:
            continue
        name = obj.get_name().replace('_GEN_VARIABLE', '')
        if name in LAYOUT:
            loc, sc = LAYOUT[name]
            obj.set_editor_property('relative_location', unreal.Vector(*loc))
            obj.set_editor_property('relative_scale3d', unreal.Vector(*sc))
            log('set', name, loc, sc)
        if name in BLOCKS:
            loc, ext = BLOCKS[name]
            obj.set_editor_property('relative_location', unreal.Vector(*loc))
            obj.set_editor_property('box_extent', unreal.Vector(*ext))
            log('set', name, loc, ext)
        if name == 'Ground':
            obj.set_editor_property('visible', False)
            obj.set_editor_property('hidden_in_game', True)
            log('hide Ground (o chao agora e a rua de verdade)')
        if name == 'LocalFog':
            obj.set_editor_property('radial_fog_extinction', 0.45)
            obj.set_editor_property('height_fog_extinction', 0.5)
            obj.set_editor_property('height_fog_falloff', 500.0)
            for p in ('radial_fog_extinction', 'height_fog_extinction', 'height_fog_falloff', 'height_fog_offset', 'fog_albedo', 'fog_phase_g'):
                try:
                    log('  LocalFog', p, obj.get_editor_property(p))
                except Exception as e:
                    log('  noprop', p, e)
    unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    # a instancia na cena pode ter valores proprios gravados: iguala aos do BP
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        if a.get_class().get_name() != 'BP_OutsideFog_C':
            continue
        for c in a.get_components_by_class(unreal.SceneComponent):
            n = c.get_name()
            if n in LAYOUT:
                c.set_editor_property('relative_location', unreal.Vector(*LAYOUT[n][0]))
                c.set_editor_property('relative_scale3d', unreal.Vector(*LAYOUT[n][1]))
            if isinstance(c, unreal.LocalFogVolumeComponent):
                c.set_radial_fog_extinction(0.45); c.set_height_fog_extinction(0.5); c.set_height_fog_falloff(500.0)
        a.modify()
        log('instance synced', a.get_actor_label())
    unreal.EditorLoadingAndSavingUtils.save_packages([p for p in list(unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + list(unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()) if p.get_name().startswith('/Game/Library')], True)  # so o que e nosso (nunca Stationer/pacotes)
    log('saved', unreal.EditorAssetLibrary.save_asset(BP, False))

try:
    run()
except Exception:
    log(traceback.format_exc())


