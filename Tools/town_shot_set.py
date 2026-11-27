"""Conjunto padrao de fotos da Main Street (porta, ruas, cruzamento, ceu, por cima). Usa town_shot.run."""
import importlib.util, os
spec = importlib.util.spec_from_file_location('town_shot', os.path.join(os.path.dirname(__file__), 'town_shot.py'))
ts = importlib.util.module_from_spec(spec); spec.loader.exec_module(ts)
SHOTS = [
    ('porta',      (1150, 207, 170),   (0, 0)),
    ('rua_norte',  (1750, -2300, 170), (0, 90)),
    ('rua_sul',    (1750, 2300, 170),  (0, -90)),
    ('cruz_leste', (1750, 2300, 170),  (0, 50)),
    ('cruz_oeste', (1750, 2300, 170),  (0, 130)),
    ('ceu',        (1750, 0, 170),     (32, 15)),
    ('telhado',    (-400, -2500, 1900), (-14, 40)),
    ('calcada',    (1200, -1500, 170), (0, 70)),
    ('igreja',     (1500, 1500, 170),  (20, -27)),
    ('hotel',      (1750, 4800, 170),  (4, 90)),
    ('cinema',     (1750, -2600, 170), (4, -90)),
    ('caixa_agua', (1750, -1000, 170), (36, -138)),
]
import unreal
ts.run(SHOTS, delay=float(getattr(unreal, 'SHOT_DELAY', 0.0)))
unreal.SHOT_DELAY = 0.0
