"""Lista componentes visiveis do jogador e dos atores MH no PIE."""
import traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_proto.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
try:
    w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
    p = unreal.GameplayStatics.get_player_pawn(w, 0)
    acts = [p, p.get_editor_property('MHWorld'), p.get_editor_property('MHArms')]
    for a in acts:
        for c in a.get_components_by_class(unreal.SkeletalMeshComponent):
            m = c.get_editor_property('skeletal_mesh_asset')
            log('%s.%s vis=%s ownerNoSee=%s onlyOwner=%s fp=%s tick=%s mesh=%s' % (
                a.get_name(), c.get_name(), c.is_visible(), c.get_editor_property('owner_no_see'),
                c.get_editor_property('only_owner_see'), c.get_editor_property('first_person_primitive_type'),
                c.get_editor_property('visibility_based_anim_tick_option'), m.get_name() if m else None))
except Exception:
    log('ERROR ' + traceback.format_exc())
