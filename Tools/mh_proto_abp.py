"""Cria ABP_MH_FromManny (esqueleto MetaHuman) e lista os componentes do BP_MH_Protagonista."""
import traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_proto.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
try:
    log('--- abp')
    body = [p for p in unreal.EditorAssetLibrary.list_assets('/Game/Library/Characters/Metahumans/Protagonist/MH_Protagonista/Body', True) if 'Body' in p.split('/')[-1]]
    log('body assets ' + str(body))
    sk = None
    for p in body:
        a = unreal.load_asset(p.split('.')[0])
        if isinstance(a, unreal.SkeletalMesh):
            sk = a.skeleton
            log('mesh %s skel %s' % (a.get_path_name(), sk.get_path_name()))
            break
    dst = '/Game/Library/Characters/Metahumans/ABP_MH_FromManny'
    if not unreal.EditorAssetLibrary.does_asset_exist(dst):
        f = unreal.AnimBlueprintFactory()
        f.set_editor_property('target_skeleton', sk)
        f.set_editor_property('parent_class', unreal.AnimInstance)
        abp = unreal.AssetToolsHelpers.get_asset_tools().create_asset('ABP_MH_FromManny', '/Game/Library/Characters/Metahumans', unreal.AnimBlueprint, f)
        unreal.EditorAssetLibrary.save_loaded_asset(abp, False)
        log('created ' + str(abp))
    cls = unreal.load_class(None, '/Game/Library/Characters/Metahumans/Protagonist/MH_Protagonista/BP_MH_Protagonista.BP_MH_Protagonista_C')
    cdo = unreal.get_default_object(cls)
    sub = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handles = sub.k2_gather_subobject_data_for_blueprint(unreal.load_asset('/Game/Library/Characters/Metahumans/Protagonist/MH_Protagonista/BP_MH_Protagonista'))
    for h in handles:
        d = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h)
        o = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(d)
        extra = ''
        if isinstance(o, unreal.SkeletalMeshComponent):
            m = o.get_editor_property('skeletal_mesh_asset')
            ac = o.get_editor_property('anim_class')
            extra = ' mesh=%s anim=%s' % (m.get_name() if m else None, ac.get_name() if ac else None)
        log('comp %s %s%s' % (o.get_name() if o else None, type(o).__name__, extra))
except Exception:
    log('ERROR ' + traceback.format_exc())
