"""Le ou ajusta as medidas de corpo de um MHC: py mh_body.py <Nome> [Constraint=valor ...] (sem pares: so lista)."""
import sys, traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_proto.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
try:
    name = sys.argv[1]
    path = '/Game/Library/Characters/Metahumans/Customers/MHC_%s' % name
    ch = unreal.load_asset(path)
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
    log('--- body %s add %s' % (name, sub.try_add_object_to_edit(ch)))
    cons = sub.get_body_constraints(ch)
    pairs = dict(a.split('=') for a in sys.argv[2:])
    cons = list(cons)
    for c in cons:
        n = str(c.get_editor_property('name'))
        if n in pairs:
            c.set_editor_property('target_measurement', float(pairs[n]))
            c.set_editor_property('is_active', True)
    if pairs:
        sub.set_body_constraints(ch, cons)
        sub.commit_body_state(ch, sub.get_body_state(ch)) if hasattr(sub, 'get_body_state') else None
        unreal.EditorAssetLibrary.save_loaded_asset(ch, False)
        log('saved')
    for c in sub.get_body_constraints(ch):
        log(str(c))
    sub.remove_object_to_edit(ch)
except Exception:
    log('ERROR ' + traceback.format_exc())
