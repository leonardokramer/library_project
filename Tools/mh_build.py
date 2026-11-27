import sys, traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_build.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(s + '\n')

def pick(enum_cls, *keys):
    for k in dir(enum_cls):
        if all(x in k for x in keys):
            return getattr(enum_cls, k)
    raise RuntimeError('enum %s %s not in %s' % (enum_cls, keys, [k for k in dir(enum_cls) if k.isupper()]))

name = sys.argv[1]
base = '/Game/Library/Characters/Metahumans/Protagonist' if name == 'Protagonista' else '/Game/Library/Characters/Metahumans/Customers'
try:
    log('--- ' + name)
    ch = unreal.load_asset('%s/MHC_%s' % (base, name))
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
    log('add ' + str(sub.try_add_object_to_edit(ch)))
    rp = unreal.MetaHumanCharacterAutoRiggingRequestParams()
    rp.set_editor_property('rig_type', pick(unreal.MetaHumanRigType, 'BLEND'))
    rp.set_editor_property('blocking', True)
    rp.set_editor_property('report_progress', False)
    if 'norig' in sys.argv:
        log('rig skipped')
    else:
        sub.request_auto_rigging(ch, rp)
        log('rigged')
    tp = unreal.MetaHumanCharacterTextureRequestParams()
    try:
        tp.set_editor_property('blocking', True)
    except Exception as e:
        log('tex params: ' + str(e) + ' ' + str([p for p in dir(tp) if not p.startswith('_')][:40]))
    sub.request_texture_sources(ch, tp)
    log('textures')
    unreal.EditorAssetLibrary.save_loaded_asset(ch, False)
    log('can_build ' + str(sub.can_build_meta_human(ch, True)))
    bp = unreal.MetaHumanCharacterEditorBuildParameters()
    bp.set_editor_property('pipeline_type', pick(unreal.MetaHumanDefaultPipelineType, 'OPTIMIZED'))
    bp.set_editor_property('pipeline_quality', pick(unreal.MetaHumanQualityLevel, 'MEDIUM'))
    bp.set_editor_property('absolute_build_path', base)
    bp.set_editor_property('name_override', 'MH_' + name)
    sub.build_meta_human(ch, bp)
    log('built')
    unreal.EditorAssetLibrary.save_directory('%s/MH_%s' % (base, name), only_if_is_dirty=True, recursive=True)
    unreal.EditorAssetLibrary.save_loaded_asset(ch, False)
    sub.remove_object_to_edit(ch)
    log('saved ' + str(unreal.EditorAssetLibrary.does_asset_exist('%s/MH_%s/BP_MH_%s' % (base, name, name))))
except Exception:
    log('ERROR ' + traceback.format_exc())
if len(sys.argv) > 2 and sys.argv[2] == 'quit':
    log('quit')
    unreal.SystemLibrary.quit_editor()
