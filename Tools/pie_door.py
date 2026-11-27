"""Atalhos de teste dos sustos da porta no PIE.
pull  : abre a porta, forca o puxao (ForceVar 1) e poe o jogador no vao olhando a rua.
push  : liga bDoorTest e poe o jogador na frente da porta; depois chame 'try' ate abrir.
try   : uma tentativa de abrir a porta (o mesmo que apertar E nela)."""
import sys, traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_proto.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
def find(w, cls):
    c = unreal.load_class(None, cls)
    a = unreal.GameplayStatics.get_all_actors_of_class(w, c)
    return a[0] if a else None
try:
    w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
    p = unreal.GameplayStatics.get_player_pawn(w, 0)
    pc = unreal.GameplayStatics.get_player_controller(w, 0)
    door = find(w, '/Game/Library/Blueprints/BP_ShopDoor.BP_ShopDoor_C')
    scare = find(w, '/Game/Library/Blueprints/Horror/BP_Scare_Door.BP_Scare_Door_C')
    cmd = sys.argv[1]
    if cmd == 'pull':
        for o in (scare, door):
            try:
                o.set_editor_property('ForceVar', 1); log('ForceVar on ' + o.get_name())
            except Exception:
                pass
        scare.set_editor_property('bDoorTest', True)
        door.call_method('OpenTo', (95.0, 0.4))
        p.set_actor_location(unreal.Vector(1040, 207, 100), False, False)
        pc.set_control_rotation(unreal.Rotator(roll=0, pitch=0, yaw=0))
    elif cmd == 'push':
        scare.set_editor_property('bDoorTest', True)
        p.set_actor_location(unreal.Vector(960, 207, 100), False, True)
        pc.set_control_rotation(unreal.Rotator(roll=0, pitch=0, yaw=0))
    elif cmd == 'try':
        door.call_method('TryOpen')
    log('door ' + cmd + ' ok')
except Exception:
    log('ERROR ' + traceback.format_exc())
