"""No PIE ejetado (F8): poe a camera do editor olhando o jogador. Args: dist yawOffset z"""
import sys, math, traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_proto.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
try:
    w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
    p = unreal.GameplayStatics.get_player_pawn(w, 0)
    loc = p.get_actor_location()
    yaw = p.get_actor_rotation().yaw
    d = float(sys.argv[1]) if len(sys.argv) > 1 else 200
    off = float(sys.argv[2]) if len(sys.argv) > 2 else 0
    z = float(sys.argv[3]) if len(sys.argv) > 3 else 20
    a = math.radians(yaw + off)
    cam = unreal.Vector(loc.x + math.cos(a) * d, loc.y + math.sin(a) * d, loc.z + z)
    unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).set_level_viewport_camera_info(
        cam, unreal.Rotator(roll=0, pitch=-5, yaw=yaw + off + 180))
    log('look player %s yaw %.0f' % (loc, yaw))
except Exception:
    log('ERROR ' + traceback.format_exc())
