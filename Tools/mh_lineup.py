import sys, traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_lineup.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(s + '\n')
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
try:
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith('TEMP_Lineup_'):
            eas.destroy_actor(a)
    mode = sys.argv[1] if len(sys.argv) > 1 else 'place'
    sp = [a for a in eas.get_all_level_actors() if a.get_actor_label() == 'CustomerSpawner']
    if mode == 'clean':
        if sp:
            sp[0].set_editor_property('maxCustomers', 3)
        log('cleaned, maxCustomers 3')
    else:
        if sp:
            sp[0].set_editor_property('maxCustomers', 0)
        idle = unreal.load_asset('/Game/Library/Characters/Metahumans/MH_MM_Idle')
        names = ['Helena', 'Marcos', 'Beatriz', 'Tomas', 'Rafael', 'Clara', 'Otavio', 'Isadora', 'Joaquim']
        for n, nm in enumerate(names):
            cls = unreal.load_class(None, '/Game/Library/Characters/Metahumans/Customers/MH_%s/BP_MH_%s.BP_MH_%s_C' % (nm, nm, nm))
            a = eas.spawn_actor_from_class(cls, unreal.Vector(80 + n * 75, 230, 20), unreal.Rotator(roll=0, pitch=0, yaw=180))
            a.set_actor_label('TEMP_Lineup_' + nm)
            a.set_folder_path('TEMP_Lineup')
            for c in a.get_components_by_class(unreal.SkeletalMeshComponent):
                if c.get_name() == 'Body':
                    c.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
                    c.set_animation(idle)
                    c.play(True)
            log('placed ' + nm + ' comps ' + ','.join(c.get_name() for c in a.get_components_by_class(unreal.SkeletalMeshComponent)))
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    log('level saved')
except Exception:
    log('ERROR ' + traceback.format_exc())
