"""Export a skeletal mesh to FBX (run inside the Unreal editor: py "Tools/ue_export_body.py" <out.fbx> [asset path]).
Default asset: the monster body. For the face: /Game/Library/Characters/Metahumans/MH_Monster/Face/SKM_MH_Monster_FaceMesh

Used by Tools/blender/monster_flaps.py, which places the paper flaps on the real skin.
Result/log: Saved/ue_export_body.log
"""
import sys, traceback
import unreal

LOG = unreal.Paths.project_saved_dir() + 'ue_export_body.log'


def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')


try:
    args = [a for a in sys.argv[1:]]
    out = next((a for a in args if a.endswith('.fbx')), unreal.Paths.project_saved_dir() + 'MonsterBody.fbx')
    path = next((a for a in args if a.startswith('/Game/')), '/Game/Library/Characters/Metahumans/MH_Monster/Body/SKM_MH_Monster_BodyMesh')
    mesh = unreal.load_asset(path)
    task = unreal.AssetExportTask()
    task.object = mesh
    task.filename = out
    task.automated = True
    task.prompt = False
    task.replace_identical = True
    opt = unreal.FbxExportOption()
    opt.level_of_detail = False
    opt.collision = False
    opt.export_morph_targets = False
    opt.vertex_color = False
    task.options = opt
    ok = unreal.Exporter.run_asset_export_task(task)
    log('export %s -> %s' % (ok, out))
except Exception:
    log('ERROR ' + traceback.format_exc())
