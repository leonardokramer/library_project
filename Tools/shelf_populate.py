"""Povoa uma estante BP_BookShelfs (corpo 01, 150x44) com BP_Book + BP_PlaceZone.

Rodado via ProgrammaticToolset.execute_tool_script (veja MCP_WORKFLOW.md): cole o conteúdo no
argumento `script`, ajuste PLAN ({'S16': ('Fantasy', 0.6)}: id do rótulo sem "BP_BookShelfs",
gênero, escala de enchimento) e rode poucas estantes por vez (as do térreo apagam ~190 tintas).
Gerou as 24 estantes de livro (Etapa 1d de estantes, 2026-10-27).

ATENÇÃO: só use em estantes com `internalMeshType == 1` (madeira reta). Os tipos 2 (arame/adega) e
3 (pegboard) e o corpo 02 (ilhas) são para produtos, não livros. Confira antes com
ObjectTools.get_properties(['internalMeshType', 'bookshelf_BodyType']).

Para recuperar atores apagados por engano: o mapa original está no git (LFS). `git show
HEAD:Content/Library/Maps/L_Library.umap | git lfs smudge > Content/Library/Maps/_Orig_Temp.umap`,
depois AssetTools.load_asset + SceneTools.load_level no temporário, leia os atores e volte ao
mapa real (apague o temporário no fim, não commite).

Geometria (espaço local da estante, yaw = yaw da estante):
- larguraútil lx de -66 a +66 (interno vai a ±69.6); frente em ly = -16.6; livro com a mesma yaw da estante.
- fundos das 7 prateleiras em z relativo 20, 60, 95, 130, 165, 200, 235.
- A placa vem das variáveis bookshelf_LabelType (1) e bookshelf_LabelMaterial (índice do gênero).
"""
import json, math

SC = 'editor_toolset.toolsets.scene.SceneTools.'
AC = 'editor_toolset.toolsets.actor.ActorTools.'
O = 'editor_toolset.toolsets.object.ObjectTools.'
MD = '/Game/Stationer/Meshes/Books/'
IDX = {'Biography': 1, 'Dictionaries': 2, 'Economy': 3, 'Fantasy': 4, 'History': 5, 'Novels': 6, 'Sci-Fi': 7, 'Science': 8}
# [malha, meia espessura, profundidade]
GEN = {
    'Biography': [['SM_Book_02', 2.2, 17.2], ['SM_Book_07', 2.1, 18.0], ['SM_Book_29', 2.5, 18.9]],
    'Dictionaries': [['SM_Book_01', 2.2, 17.2], ['SM_Book_05', 2.2, 17.2]],
    'Economy': [['SM_Book_08', 2.2, 17.2], ['SM_Book_14', 2.4, 19.0]],
    'Fantasy': [['SM_Book_09', 2.2, 17.9], ['SM_Book_21', 2.7, 20.0], ['SM_Book_12', 2.2, 17.2]],
    'History': [['SM_Book_11', 2.2, 17.2], ['SM_Book_20', 2.7, 20.0]],
    'Novels': [['SM_Book_03', 2.2, 17.1], ['SM_Book_04', 2.2, 17.2], ['SM_Book_26', 2.7, 20.0]],
    'Sci-Fi': [['SM_Book_15', 2.4, 18.5], ['SM_Book_22', 2.5, 17.6]],
    'Science': [['SM_Book_10', 2.2, 17.9], ['SM_Book_13', 2.4, 19.0], ['SM_Book_17', 2.7, 19.2]],
}
PLAN = {'S16': ('Fantasy', 0.6)}
# (z relativo, fração da largura ocupada): meio e baixo cheios, topo quase vazio
LEVELS = [(20, 0.6), (60, 0.65), (95, 0.65), (130, 0.5), (165, 0.25), (200, 0.12), (235, 0.08)]


def rot(yaw, x, y):
    c = math.cos(math.radians(yaw)); s = math.sin(math.radians(yaw))
    return (c * x - s * y, s * x + c * y)


class R:  # LCG determinístico, para repetir o mesmo layout
    def __init__(s, seed): s.v = seed * 7919 + 13
    def f(s):
        s.v = (s.v * 1103515245 + 12345) % 2147483648
        return s.v / 2147483648.0
    def i(s, a, b): return a + int(s.f() * (b - a + 1))


def process(sid, genre, scale):
    out = {}
    a = [x for x in execute_tool(SC + 'find_actors', json.dumps({'name': 'BookShelfs' + sid[1:], 'tag': '', 'collision_channels': []}))['returnValue'] if 'BP_BookShelfs_C_' in x['refPath']]
    a = [x for x in a if execute_tool(AC + 'get_label', json.dumps({'actor': x}))['returnValue'] == 'BP_BookShelfs' + sid[1:]][0]
    t = execute_tool(AC + 'get_actor_transform', json.dumps({'actor': a}))['returnValue']
    L = t['location']; yaw = t['rotation']['yaw']
    b = execute_tool(AC + 'get_actor_bounds', json.dumps({'actor': a}))['returnValue']
    execute_tool(O + 'set_properties', json.dumps({'instance': a, 'values': json.dumps({'bookshelf_LabelType': 1, 'bookshelf_LabelMaterial': IDX[genre]})}))
    # limpeza: livros/fileiras antigas, tintas, cadernos, zonas e grupos que cabem dentro da estante
    cands = execute_tool(SC + 'find_actors', json.dumps({'name': '', 'tag': '', 'collision_channels': [], 'bounds': b}))['returnValue']
    deleted = 0
    for x in cands:
        l = execute_tool(AC + 'get_label', json.dumps({'actor': x}))['returnValue']
        if not (l.startswith('Book_') or l.startswith('BookStack_') or l.startswith('PaintContainer') or l.startswith('Notebook') or l.startswith('Zone_') or l.startswith('GroupActor')):
            continue
        p = execute_tool(AC + 'get_actor_transform', json.dumps({'actor': x}))['returnValue']['location']
        lx, ly = rot(-yaw, p['x'] - L['x'], p['y'] - L['y'])
        if l.startswith('GroupActor'):
            continue  # os grupos das tintas sumiram junto com os filhos (groups: 0 na prática)
        if abs(lx) <= 80 and -26 <= ly <= 24 and -2 <= p['z'] - L['z'] <= 300:
            execute_tool(SC + 'remove_from_scene', json.dumps({'actor': x})); deleted += 1
    out['deleted'] = deleted
    T = GEN[genre]; rnd = R(int(sid[1:]))
    n = 0; counts = []
    for (zl, frac) in LEVELS:
        target = frac * scale / 0.6 * 132.0
        lx = -66.0 + rnd.i(0, 6); used = 0.0; k = rnd.i(0, len(T) - 1); cnt = 0
        while used < target:  # blocos de 3-6 (baixo) ou 2-3 (cima) exemplares do mesmo título
            m = T[k % len(T)]; k += 1
            nb = rnd.i(3, 6) if zl <= 130 else rnd.i(2, 3)
            for j in range(nb):
                th = m[1] * 2 + 0.25
                if lx + th > 66.0: break
                cx = lx + th / 2
                wx, wy = rot(yaw, cx, -16.6)
                nm = 'Book_%s_%s_R%d_%02d' % (genre, sid, zl, cnt)
                act = execute_tool(SC + 'add_to_scene_from_asset', json.dumps({'asset_path': '/Game/Library/Blueprints/BP_Book', 'name': nm, 'xform': {'location': {'x': L['x'] + wx, 'y': L['y'] + wy, 'z': L['z'] + zl}, 'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}, 'scale': {'x': 1, 'y': 1, 'z': 1}}}))['returnValue']
                execute_tool(O + 'set_properties', json.dumps({'instance': {'refPath': act['refPath'] + '.Mesh'}, 'values': json.dumps({'StaticMesh': MD + '%s.%s' % (m[0], m[0])})}))
                execute_tool(AC + 'set_label', json.dumps({'actor': act, 'label': nm}))
                execute_tool(SC + 'set_actor_folder', json.dumps({'actor': act, 'folder_path': 'Gameplay/Books'}))
                lx += th; used += th; cnt += 1; n += 1
                if used >= target: break
            lx += 1.0; used += 1.0
            if lx >= 62.0: break
        counts.append(cnt)
        wx, wy = rot(yaw, -1.0, -7.6)
        zn = 'Zone_%s_%s_R%d' % (genre, sid, zl)
        z = execute_tool(SC + 'add_to_scene_from_asset', json.dumps({'asset_path': '/Game/Library/Blueprints/BP_PlaceZone', 'name': zn, 'xform': {'location': {'x': L['x'] + wx, 'y': L['y'] + wy, 'z': L['z'] + zl + 15}, 'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}, 'scale': {'x': 1, 'y': 1, 'z': 1}}}))['returnValue']
        execute_tool(O + 'set_properties', json.dumps({'instance': z, 'values': json.dumps({'Extent': {'x': 68, 'y': 9, 'z': 15}})}))
        execute_tool(AC + 'set_label', json.dumps({'actor': z, 'label': zn}))
        execute_tool(SC + 'set_actor_folder', json.dumps({'actor': z, 'folder_path': 'Gameplay/PlaceZones'}))
    out['books'] = n; out['levels'] = counts
    return out


def run():
    return {s: process(s, g, sc) for s, (g, sc) in PLAN.items()}
