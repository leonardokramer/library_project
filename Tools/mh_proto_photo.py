"""Coloca a protagonista temporaria em frente a camera (nao salva o mapa). Arg 'clean' remove."""
import sys, traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_proto.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
try:
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('TEMP_Proto'):
            eas.destroy_actor(a)
    if 'clean' not in sys.argv:
        P = '/Game/Library/Characters/Metahumans/Protagonist/MH_Protagonista/BP_MH_Protagonista'
        cls = unreal.load_class(None, P + '.BP_MH_Protagonista_C')
        a = eas.spawn_actor_from_class(cls, unreal.Vector(-350, 170, 20), unreal.Rotator(roll=0, pitch=0, yaw=-90))
        a.set_actor_label('TEMP_Proto')
        idle = unreal.load_asset('/Game/Library/Characters/Metahumans/MH_MM_Idle')
        for c in a.get_components_by_class(unreal.SkeletalMeshComponent):
            if c.get_name() == 'Body':
                c.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
                c.set_animation(idle)
                c.play(True)
        d = float(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1][0].isdigit() else 230
        z = float(sys.argv[2]) if len(sys.argv) > 2 else 110
        unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).set_level_viewport_camera_info(
            unreal.Vector(-350 + d, 170, z), unreal.Rotator(roll=0, pitch=-3, yaw=180))
        log('photo placed d=%s z=%s' % (d, z))
except Exception:
    log('ERROR ' + traceback.format_exc())
