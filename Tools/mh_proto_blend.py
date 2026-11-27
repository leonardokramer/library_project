"""Mistura numerica do rosto: py mh_proto_blend.py <PresetB> <pesoB>"""
import sys, traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_proto.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
DST = '/Game/Library/Characters/Metahumans/Protagonist/MHC_Protagonista'
PRE = '/MetaHumanCharacter/Optional/Presets/'
try:
    b_name = sys.argv[1] if len(sys.argv) > 1 else 'Lani'
    w = float(sys.argv[2]) if len(sys.argv) > 2 else 0.35
    log('--- blend %s + %.2f' % (b_name, w))
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
    a = unreal.load_asset(PRE + (sys.argv[3] if len(sys.argv) > 3 else 'Tuya'))
    b = unreal.load_asset(PRE + b_name)
    ch = unreal.load_asset(DST)
    for o in (a, b):
        log('add %s %s' % (o.get_name(), sub.try_add_object_to_edit(o)))
    ca = sub.get_face_model_coefficients(a)
    cb = sub.get_face_model_coefficients(b)
    log('coef type %s' % type(ca))
    try:
        log('len %d %d' % (len(ca), len(cb)))
    except Exception as e:
        log('no len ' + str(e) + ' ' + str([m for m in dir(ca) if not m.startswith('_')][:30]))
    mix = [x * (1 - w) + y * w for x, y in zip(ca, cb)]
    sub.set_face_model_coefficients(ch, mix)
    log('set ok')
    try:
        sub.commit_face_state(ch, sub.get_face_state(ch)) if hasattr(sub, 'get_face_state') else None
    except Exception as e:
        log('commit skip ' + str(e))
    log('fs ' + str([m for m in dir(sub) if 'state' in m]))
    unreal.EditorAssetLibrary.save_loaded_asset(ch, False)
    log('saved')
    for o in (a, b):
        sub.remove_object_to_edit(o)
except Exception:
    log('ERROR ' + traceback.format_exc())
