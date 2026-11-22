"""Povoa as estantes de livros com um visual "usado" (2026-11-21, pedido do usuario).

Rodado via ProgrammaticToolset.execute_tool_script (cole o arquivo inteiro em `script`; ajuste ONLY).
Substitui o tools/shelf_populate.py para o layout atual (o antigo fica como historico).

O que faz, por genero (GENRES: estantes em ordem da esquerda para a direita, para quem olha de frente):
- O genero e uma sequencia so, em ordem de leitura: estante por estante, prateleira de cima para baixo,
  cada prateleira da esquerda para a direita (para quem olha de frente, a esquerda e o x local POSITIVO).
  Cada titulo recebe uma fatia igual da largura e so depois vem o proximo: o titulo fica num trecho so.
- Cada prateleira tem preenchimento sorteado (FULL_P cheia; senao FMIN..FMAX, terreo x GROUND_K) e o
  trecho comeca num ponto sorteado.
- "Uso": buracos de 1-2 livros (P_HOLE), livros um pouco para fora/dentro e levemente girados (P_JIT),
  livros perdidos de outro genero (P_STRAY) ou de outro titulo do mesmo genero (P_SWAP),
  um livro tombado encostado no vizinho no fim do trecho (P_LEAN / P_LEAN_L) e pilhas deitadas e tortas
  de 2-5 livros num vao (P_STACK; 30% de cada livro da pilha vem de outro genero).
- Revistas: escala 0,9 e ExtraShrink 0,1 (sao mais altas que o vao, docs/BOOK_COVERS.md).

Geometria do livro (malha): pivo no centro da espessura (X), na frente da lombada (Y 0) e na base (Z 0);
X = espessura (meia espessura hf), Y 0..D = profundidade, Z 0..H = altura; capa na face -X.
Estante: fundos das prateleiras em z relativo 20, 60, 95, 130, 165, 200, 235; vao livre ~30 cm
(35 na de baixo); largura util x de -66 a +66; frente dos livros em y local -16,6.
Pitch positivo levanta o +X: tombado para +x = pitch -a; deitado (capa para cima) = pitch -90.
"""
import json, math

SC = 'editor_toolset.toolsets.scene.SceneTools.'
AC = 'editor_toolset.toolsets.actor.ActorTools.'
O = 'editor_toolset.toolsets.object.ObjectTools.'

# [malha, meia espessura, profundidade, altura] (medidas da malha, StaticMeshTools.get_bounds)
GEN = {
    'Biography': [['SM_Book_02', 2.2, 17.2, 26.5], ['SM_Book_07', 2.1, 18.0, 26.5], ['SM_Book_29', 2.5, 18.9, 29.3],
                  ['SM_BookX_Runaway', 2.7, 20.0, 28.8]],
    'Economy': [['SM_BookX_DontBother', 2.2, 17.9, 26.5], ['SM_BookX_LeadingFromTheBack', 2.7, 20.0, 28.6]],
    'Fantasy': [['SM_Book_21', 2.7, 20.0, 28.8], ['SM_BookX_JesterVampire', 2.4, 18.5, 28.4],
                ['SM_BookX_SkylandTales', 2.7, 20.0, 28.8], ['SM_BookX_SkylandStory', 2.7, 20.0, 28.8],
                ['SM_BookX_FinalLight', 2.2, 17.1, 26.9]],
    'History': [['SM_Book_11', 2.2, 17.2, 26.5], ['SM_Book_20', 2.7, 20.0, 28.8], ['SM_Book_10', 2.2, 17.9, 26.5]],
    'Guides': [['SM_Book_01', 2.2, 17.2, 26.5], ['SM_Book_08', 2.2, 17.2, 26.5], ['SM_Book_14', 2.4, 19.0, 28.4],
               ['SM_BookX_DSharpForBeginners', 2.5, 17.6, 27.1], ['SM_BookX_HuntingTechniques', 2.2, 17.2, 26.5],
               ['SM_BookX_Fuerteventura', 2.2, 17.2, 26.5]],
    'Novels': [['SM_Book_03', 2.2, 17.1, 26.9], ['SM_Book_04', 2.2, 17.2, 26.5], ['SM_Book_26', 2.7, 20.0, 28.6],
               ['SM_Book_05', 2.2, 17.2, 26.5], ['SM_Book_09', 2.2, 17.9, 26.5],
               ['SM_BookX_CurveInThePlane', 2.4, 19.0, 28.4], ['SM_BookX_TheAttic', 2.2, 17.2, 26.5],
               ['SM_BookX_SadRiseMountain', 2.2, 17.2, 26.5], ['SM_BookX_PilotDreams', 2.2, 17.9, 26.5],
               ['SM_BookX_PeepingTim', 2.7, 20.0, 28.8], ['SM_BookX_MorningDew', 2.2, 17.2, 26.5],
               ['SM_BookX_HoustonMurders', 2.7, 20.0, 28.8], ['SM_BookX_Highways', 2.7, 20.0, 28.8],
               ['SM_BookX_FinalGamble', 2.2, 17.2, 26.5], ['SM_BookX_Escapee', 2.2, 17.2, 26.5],
               ['SM_BookX_Polaroid', 2.5, 18.9, 29.3], ['SM_BookX_LakeMurdersII', 2.2, 17.2, 26.5],
               ['SM_BookX_HareApparent', 2.7, 19.2, 28.8]],
    'Sci-Fi': [['SM_Book_15', 2.4, 18.5, 28.4], ['SM_Book_22', 2.5, 17.6, 27.1],
               ['SM_BookX_FourthTarget', 2.7, 20.0, 28.8], ['SM_BookX_SaturnRecoiling', 2.4, 19.0, 28.4],
               ['SM_BookX_Mars', 2.2, 17.2, 26.5]],
    'Science': [['SM_Book_13', 2.4, 19.0, 28.4], ['SM_Book_17', 2.7, 19.2, 28.8], ['SM_Book_12', 2.2, 17.2, 26.5],
                ['SM_BookX_Weather', 2.7, 20.0, 28.8], ['SM_BookX_Symmetry', 2.2, 17.9, 26.5],
                ['SM_BookX_Framboise', 2.7, 20.0, 28.8]],
    'Magazines': [['SM_BookX_Mag_%s' % n, 1.3, 24.3, 32.3] for n in
                  ('Matsulki', 'BringWaterproofs', 'IntlGeography', 'Glass', 'Business', 'Liquid', 'Species',
                   'EngineDoctor', 'Africa', 'MedicineToday')],
}
GENRES = {
    'Novels': ['S28', 'S29', 'S30', 'S31', 'S4'],
    'Biography': ['S33'],
    'Magazines': ['S26'],
    'Science': ['S10', 'S9', 'S7', 'S8'],
    'History': ['S11', 'S14'],
    'Sci-Fi': ['S15', 'S16', 'S17', 'S18'],
    'Guides': ['S19'],
    'Fantasy': ['S20', 'S21', 'S22', 'S23', 'S24'],
    'Economy': ['S36'],
}
IDX = {'Biography': 1, 'Economy': 3, 'Fantasy': 4, 'History': 5, 'Novels': 6, 'Sci-Fi': 7, 'Science': 8,
       'Magazines': 9, 'Guides': 10}
LEVELS = [235, 200, 165, 130, 95, 60, 20]  # de cima para baixo
GAP = {20: 35.0}  # vao livre de cada prateleira; as outras 30
FULL_P = 0.10
FMIN, FMAX = 0.08, 0.6
GROUND_K = 0.85
P_HOLE = 0.05
P_JIT = 0.30
P_STRAY = 0.025
P_SWAP = 0.02
P_LEAN = 0.35
P_LEAN_L = 0.15
P_STACK = 0.33
STACK_OTHER = 0.30
EFF = 0.85  # fracao da largura que vira livro do titulo da vez (o resto: buracos, perdidos, trocas)
SEED = 7
ONLY = ['Fantasy']


class R:
    def __init__(s, seed): s.v = seed * 7919 + 13
    def f(s):
        s.v = (s.v * 1103515245 + 12345) % 2147483648
        return s.v / 2147483648.0
    def i(s, a, b): return a + int(s.f() * (b - a + 1))
    def u(s, a, b): return a + s.f() * (b - a)
    def pick(s, lst): return lst[int(s.f() * len(lst)) % len(lst)]


def rot(yaw, x, y):
    c = math.cos(math.radians(yaw)); s = math.sin(math.radians(yaw))
    return (c * x - s * y, s * x + c * y)


def mesh_path(n):
    return ('/Game/Library/Meshes/Books/' if n.startswith('SM_BookX_') else '/Game/Stationer/Meshes/Books/') + '%s.%s' % (n, n)


def is_mag(m): return m[0].startswith('SM_BookX_Mag_')


def dims(m):  # (meia espessura, profundidade, altura, escala) ja com a escala das revistas
    k = 0.9 if is_mag(m) else 1.0
    return m[1] * k, m[2] * k, m[3] * k, k


def shelf_info(sid):
    a = [x for x in execute_tool(SC + 'find_actors', json.dumps({'name': 'BookShelfs' + sid[1:], 'tag': '', 'collision_channels': []}))['returnValue'] if ('BP_BookShelfs_C_' in x['refPath'] or 'BP_BookShelf_Library_C_' in x['refPath'])]
    a = [x for x in a if execute_tool(AC + 'get_label', json.dumps({'actor': x}))['returnValue'] == 'BP_BookShelfs' + sid[1:]][0]
    t = execute_tool(AC + 'get_actor_transform', json.dumps({'actor': a}))['returnValue']
    b = execute_tool(AC + 'get_actor_bounds', json.dumps({'actor': a}))['returnValue']
    return {'sid': sid, 'a': a, 't': t, 'b': b, 'L': t['location'], 'yaw': t['rotation']['yaw']}


def clear_shelf(inf):
    L = inf['L']; yaw = inf['yaw']; t = inf['t']; deleted = 0
    cands = execute_tool(SC + 'find_actors', json.dumps({'name': '', 'tag': '', 'collision_channels': [], 'bounds': inf['b']}))['returnValue']
    for x in cands:
        l = execute_tool(AC + 'get_label', json.dumps({'actor': x}))['returnValue']
        if not (l.startswith('Book_') or l.startswith('BookStack_') or l.startswith('PaintContainer') or l.startswith('Notebook') or l.startswith('Zone_')):
            continue
        p = execute_tool(AC + 'get_actor_transform', json.dumps({'actor': x}))['returnValue']['location']
        lx, ly = rot(-yaw, p['x'] - L['x'], p['y'] - L['y'])
        if abs(lx) <= 80 * max(1.0, t['scale']['x']) and -26 <= ly <= 24 and -2 <= p['z'] - L['z'] <= 300:
            execute_tool(SC + 'remove_from_scene', json.dumps({'actor': x})); deleted += 1
    return deleted


class Placer:
    def __init__(s, genre):
        s.genre = genre; s.count = {}; s.n = 0

    def put(s, inf, zl, m, x, y, z, pitch, dyaw, tag):
        """x, y, z em espaco local da estante (z relativo ao pe)."""
        L = inf['L']; yaw = inf['yaw']
        hf, D, H, k = dims(m)
        wx, wy = rot(yaw, x, y)
        s.n += 1
        nm = 'Book_%s_%s_R%d_%s%03d' % (s.genre, inf['sid'], zl, tag, s.n)
        act = execute_tool(SC + 'add_to_scene_from_asset', json.dumps({'asset_path': '/Game/Library/Blueprints/BP_Book', 'name': nm, 'xform': {'location': {'x': L['x'] + wx, 'y': L['y'] + wy, 'z': L['z'] + z}, 'rotation': {'pitch': pitch, 'yaw': yaw + dyaw, 'roll': 0}, 'scale': {'x': k, 'y': k, 'z': k}}}))['returnValue']
        execute_tool(O + 'set_properties', json.dumps({'instance': {'refPath': act['refPath'] + '.Mesh'}, 'values': json.dumps({'StaticMesh': mesh_path(m[0])})}))
        if is_mag(m):
            execute_tool(O + 'set_properties', json.dumps({'instance': act, 'values': json.dumps({'ExtraShrink': 0.1})}))
        execute_tool(AC + 'set_label', json.dumps({'actor': act, 'label': nm}))
        execute_tool(SC + 'set_actor_folder', json.dumps({'actor': act, 'folder_path': 'Gameplay/Books'}))
        s.count[m[0]] = s.count.get(m[0], 0) + 1


def others(genre):
    out = []
    for g, lst in GEN.items():
        if g != genre and g != 'Magazines':
            out += lst
    return out


def lean(P, inf, zl, m, x0, side, rnd):
    """Livro tombado encostado no vizinho. side +1: vizinho em x > x0 (topo tomba para +x)."""
    hf, D, H, k = dims(m)
    a = rnd.u(14.0, 28.0); ar = math.radians(a)
    z = zl + hf * math.sin(ar)
    if side > 0:
        p = x0 - 0.15 - hf * math.cos(ar) - H * math.sin(ar)
        if p - hf * math.cos(ar) < -66.0: return None
        P.put(inf, zl, m, p, -16.6 - rnd.u(-0.5, 1.0), z, -a, 0.0, 'L')
        return p - hf * math.cos(ar)
    p = x0 + 0.15 + hf * math.cos(ar) + H * math.sin(ar)
    if p + hf * math.cos(ar) > 66.0: return None
    P.put(inf, zl, m, p, -16.6 - rnd.u(-0.5, 1.0), z, a, 0.0, 'L')
    return p + hf * math.cos(ar)


def stack(P, inf, zl, pool_same, pool_other, cx, rnd):
    """Pilha deitada e torta centrada em cx (largura reservada ~34 cm)."""
    gap = GAP.get(zl, 30.0) - 2.0
    n = rnd.i(2, 5); base = float(zl); placed = 0
    for i in range(n):
        m = rnd.pick(pool_other) if (pool_other and rnd.f() < STACK_OTHER) else rnd.pick(pool_same)
        hf, D, H, k = dims(m)
        if base + 2 * hf - zl > gap: break
        j = rnd.u(-9.0, 9.0); jr = math.radians(j)
        c = (cx + rnd.u(-1.5, 1.5), -16.6 + D / 2 + rnd.u(-0.5, 1.5))
        ux, uy = math.cos(jr), math.sin(jr)
        vx, vy = -math.sin(jr), math.cos(jr)
        px = c[0] - H / 2 * ux - D / 2 * vx
        py = c[1] - H / 2 * uy - D / 2 * vy
        P.put(inf, zl, m, px, py, base + hf, -90.0, j, 'P')
        base += 2 * hf + 0.05; placed += 1
    return placed


def fill(genre):
    infos = [shelf_info(s) for s in GENRES[genre]]
    out = {'deleted': 0}
    rows = []
    for inf in infos:
        if IDX[genre] <= 8 and 'BP_BookShelf_Library_C_' not in inf['a']['refPath']:
            execute_tool(O + 'set_properties', json.dumps({'instance': inf['a'], 'values': json.dumps({'bookshelf_LabelType': 1, 'bookshelf_LabelMaterial': IDX[genre]})}))
        out['deleted'] += clear_shelf(inf)
        rnd = R(int(inf['sid'][1:]) * 31 + SEED)
        gk = GROUND_K if inf['L']['z'] < 100 else 1.0
        for zl in LEVELS:
            f = 0.95 if rnd.f() < FULL_P else (FMIN + rnd.f() * (FMAX - FMIN)) * gk
            target = f * 132.0
            start = 66.0 - 0.5 - rnd.f() * max(0.0, 131.0 - target)
            rows.append((inf, zl, target, start))
    T = GEN[genre]; OT = others(genre)
    # cota de cada titulo recalculada a cada troca (buracos, perdidos e cortes no fim da prateleira
    # consomem largura; com cota fixa os ultimos titulos ficavam sem exemplares)
    rem_rows = sum(r[2] for r in rows)
    quota = rem_rows * EFF / len(T)
    ti = 0; tused = 0.0
    P = Placer(genre); g = R(SEED * 977 + len(genre))
    stats = {'lean': 0, 'stack': 0, 'stray': 0}
    for (inf, zl, target, start) in rows:
        rem_rows -= target
        target = min(target, start + 66.0)  # nao conta largura que nao cabe
        lx = start; used = 0.0; first = None; last_m = None; last_face = start
        while used < target:
            if used > 0 and g.f() < P_HOLE:
                hole = g.u(4.0, 10.0); lx -= hole; used += hole
                continue
            main = True; m = T[ti]
            r = g.f()
            if r < P_STRAY and OT:
                m = g.pick(OT); main = False; stats['stray'] += 1
            elif r < P_STRAY + P_SWAP and len(T) > 1:
                m = g.pick(T); main = False
            hf, D, H, k = dims(m)
            jit = g.f() < P_JIT
            th = 2 * hf + (0.8 if jit else 0.25)
            if lx - th < -66.0:
                break
            y = -16.6 - (g.u(-1.5, 2.5) if jit else 0.0)
            dy = g.u(-1.5, 1.5) if jit else 0.0
            P.put(inf, zl, m, lx - th / 2, y, zl, 0.0, dy, '')
            if first is None: first = start
            lx -= th; used += th; last_m = m; last_face = lx
            if main:
                tused += th
                if tused >= quota and ti < len(T) - 1:
                    ti += 1; tused = 0.0; lx -= 1.0; used += 1.0
                    quota = (rem_rows + max(0.0, target - used)) * EFF / (len(T) - ti)
        left_free = (start, 66.0) if first is not None else (-66.0, 66.0)
        right_free = (-66.0, lx) if first is not None else (-66.0, 66.0)
        # tombados no fim (direita) e as vezes no comeco (esquerda) do trecho
        if first is not None and g.f() < P_LEAN and last_face - right_free[0] > 12.0:
            # encosta na face do ultimo livro em pe (nao no fim do trecho, que pode ter buraco)
            e = lean(P, inf, zl, last_m if g.f() < 0.6 else g.pick(T), last_face, +1, g)
            if e is not None:
                right_free = (-66.0, min(e, lx) - 0.5); stats['lean'] += 1
        if first is not None and g.f() < P_LEAN_L and left_free[1] - left_free[0] > 12.0:
            e = lean(P, inf, zl, T[min(ti, len(T) - 1)] if g.f() < 0.5 else g.pick(T), left_free[0], -1, g)
            if e is not None:
                left_free = (e + 0.5, 66.0); stats['lean'] += 1
        # pilha deitada num vao largo
        if g.f() < P_STACK:
            for fr in sorted([left_free, right_free], key=lambda v: -(v[1] - v[0])):
                if fr[1] - fr[0] >= 36.0:
                    cx = g.u(fr[0] + 17.5, fr[1] - 17.5)
                    if stack(P, inf, zl, T, OT, cx, g) > 0: stats['stack'] += 1
                    break
        # zona de guardar da prateleira
        L = inf['L']; yaw = inf['yaw']
        wx, wy = rot(yaw, -1.0, -7.6)
        zn = 'Zone_%s_%s_R%d' % (genre, inf['sid'], zl)
        z = execute_tool(SC + 'add_to_scene_from_asset', json.dumps({'asset_path': '/Game/Library/Blueprints/BP_PlaceZone', 'name': zn, 'xform': {'location': {'x': L['x'] + wx, 'y': L['y'] + wy, 'z': L['z'] + zl + 15}, 'rotation': {'pitch': 0, 'yaw': yaw, 'roll': 0}, 'scale': {'x': 1, 'y': 1, 'z': 1}}}))['returnValue']
        execute_tool(O + 'set_properties', json.dumps({'instance': z, 'values': json.dumps({'Extent': {'x': 68, 'y': 9, 'z': 15}})}))
        execute_tool(AC + 'set_label', json.dumps({'actor': z, 'label': zn}))
        execute_tool(SC + 'set_actor_folder', json.dumps({'actor': z, 'folder_path': 'Gameplay/PlaceZones'}))
    out['books'] = P.n; out['stats'] = stats; out['per_mesh'] = P.count
    return out


def run():
    return {g: fill(g) for g in ONLY}
