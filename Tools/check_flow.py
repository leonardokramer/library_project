"""Confere se a L_Library esta no fluxo normal de jogo e corrige o que nao estiver. Arg 'quit' fecha o editor."""
import sys, traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\check_flow.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
NORMAL = {
    'BP_GameClock_C': {'DebugStartMinutes': 0.0, 'SecondsPerGameMinute': 2.0, 'bShowDebugClock': False},
    'BP_CustomerSpawner_C': {'maxCustomers': 3},
    'BP_Scare_Door_C': {'bDoorTest': False},
    'BP_ScareManager_C': {'bSkipCalmDays': False, 'bDebugHUD': False},
}
try:
    unreal.EditorLoadingAndSavingUtils.load_map('/Game/Library/Maps/L_Library')
    changed = False
    for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
        cn = a.get_class().get_name()
        if a.get_actor_label().startswith('TEMP_'):
            log('TEMP actor ' + a.get_actor_label())
        for prop, want in NORMAL.get(cn, {}).items():
            try:
                v = a.get_editor_property(prop)
            except Exception as e:
                log('%s.%s ? %s' % (a.get_actor_label(), prop, e)); continue
            ok = (abs(v - want) < 1e-3) if isinstance(want, float) else (v == want)
            log('%s.%s = %s %s' % (a.get_actor_label(), prop, v, 'ok' if ok else 'FIX'))
            if not ok:
                a.set_editor_property(prop, want); changed = True
    if changed:
        unreal.EditorLoadingAndSavingUtils.save_current_level()
        log('saved fixes')
    log('done')
except Exception:
    log('ERROR ' + traceback.format_exc())
if 'quit' in sys.argv:
    unreal.SystemLibrary.quit_editor()
