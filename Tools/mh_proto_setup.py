import traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_proto.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
DST = '/Game/Library/Characters/Metahumans/Protagonist'
try:
    log('--- setup')
    if not unreal.EditorAssetLibrary.does_asset_exist(DST + '/MHC_Protagonista'):
        src = unreal.EditorAssetLibrary.find_package_referencers_for_asset  # noqa (probe)
        paths = [p for p in unreal.EditorAssetLibrary.list_assets('/MetaHumanCharacter/Optional/Presets', False) if 'Aoi' in p]
        log('src ' + str(paths))
        ok = unreal.EditorAssetLibrary.duplicate_asset(paths[0].split('.')[0], DST + '/MHC_Protagonista')
        log('dup ' + str(ok))
        unreal.EditorAssetLibrary.save_asset(DST + '/MHC_Protagonista', False)
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
    log('SUB ' + ', '.join(m for m in dir(sub) if not m.startswith('_')))
    ch = unreal.load_asset(DST + '/MHC_Protagonista')
    log('CH ' + ', '.join(m for m in dir(ch) if not m.startswith('_')))
except Exception:
    log('ERROR ' + traceback.format_exc())
