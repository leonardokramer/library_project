"""Le o estado do BP_GameClock e do spawner no PIE."""
import traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_proto.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
try:
    w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
    for cls in ('/Game/Library/Blueprints/BP_GameClock.BP_GameClock_C', '/Game/Library/Blueprints/BP_CustomerSpawner.BP_CustomerSpawner_C'):
        acts = unreal.GameplayStatics.get_all_actors_of_class(w, unreal.load_class(None, cls))
        for a in acts:
            out = []
            c = a.get_class()
            for p in c.get_editor_property('ChildProperties') if False else []:
                pass
            for n in ['State', 'Minutes', 'CurMinutes', 'GameMinutes', 'NowMinutes', 'Day', 'bOpen', 'Accum', 'T', 'IntroT', 'Elapsed', 'DebugStartMinutes', 'SecondsPerGameMinute', 'Blocked', 'maxCustomers', 'NextSpawn', 'Timer']:
                try:
                    out.append('%s=%s' % (n, a.get_editor_property(n)))
                except Exception:
                    pass
            log('%s %s ticks=%s' % (a.get_name(), ' '.join(out), a.is_actor_tick_enabled()))
    log('time %.1f' % unreal.GameplayStatics.get_time_seconds(w))
except Exception:
    log('ERROR ' + traceback.format_exc())
