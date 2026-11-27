"""Chama uma funcao do jogador no PIE: knock | dragbegin | dragend | crouch | uncrouch"""
import sys, traceback, unreal
LOG = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_proto.log'
def log(s):
    with open(LOG, 'a') as f:
        f.write(str(s) + '\n')
try:
    w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
    p = unreal.GameplayStatics.get_player_pawn(w, 0)
    cmd = sys.argv[1]
    if cmd == 'knock':
        p.call_method('KnockDown', (unreal.Vector(-1, 0, 0),))
    elif cmd == 'dragbegin':
        p.call_method('DragBegin')
    elif cmd == 'dragend':
        p.call_method('DragEnd')
    elif cmd == 'books':
        books = unreal.GameplayStatics.get_all_actors_of_class(w, unreal.load_class(None, '/Game/Library/Blueprints/BP_Book.BP_Book_C'))
        loc = p.get_actor_location()
        books = sorted(books, key=lambda b: (b.get_actor_location() - loc).length())[:3]
        held = []
        for b in books:
            try:
                b.call_method('PickUp', (len(held), len(held) * 3.0))
            except Exception as e:
                log('pickup err ' + str(e))
            held.append(b)
        p.set_editor_property('HeldBooks', held)
        pc = unreal.GameplayStatics.get_player_controller(w, 0)
        pc.set_control_rotation(unreal.Rotator(roll=0, pitch=float(sys.argv[2]) if len(sys.argv) > 2 else -35, yaw=0))
    elif cmd == 'pitch':
        pc = unreal.GameplayStatics.get_player_controller(w, 0)
        pc.set_control_rotation(unreal.Rotator(roll=0, pitch=float(sys.argv[2]), yaw=float(sys.argv[3]) if len(sys.argv) > 3 else 0))
    elif cmd == 'crouch':
        p.crouch()
    elif cmd == 'uncrouch':
        p.un_crouch()
    log('called ' + cmd + ' drag=' + str(p.get_editor_property('MHDragView')))
except Exception:
    log('ERROR ' + traceback.format_exc())
