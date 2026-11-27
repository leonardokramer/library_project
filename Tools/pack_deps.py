"""Lista os pacotes dos pacotes de terceiros NOVOS (MERIDIAN, BUILDINGS, LIGHTING, REALISTIC_MATERIALS,
Vehicles) dos quais algo de /Game/Library depende (recursivo, dura + leve).
Saida: Saved/pack_keep.txt (um /Game/... por linha). Depois, com o editor FECHADO, rode
Tools/pack_trim.ps1 (simulacao primeiro) para apagar o resto.
Rodar: py "<caminho>/pack_deps.py"
"""
import unreal
OUT = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\pack_keep.txt'
PACKS = ('/Game/MERIDIAN/', '/Game/BUILDINGS/', '/Game/LIGHTING/', '/Game/REALISTIC_MATERIALS/', '/Game/Vehicles/')
ar = unreal.AssetRegistryHelpers.get_asset_registry()
opts = unreal.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True,
                                             include_searchable_names=False, include_soft_management_references=False,
                                             include_hard_management_references=False)
roots = sorted({str(a.package_name) for a in ar.get_assets_by_path('/Game/Library', recursive=True)})
seen, stack = set(), list(roots)
while stack:
    p = stack.pop()
    if p in seen:
        continue
    seen.add(p)
    for d in (ar.get_dependencies(p, opts) or []):
        d = str(d)
        if d.startswith('/Game/') and d not in seen:
            stack.append(d)
keep = sorted(p for p in seen if p.startswith(PACKS))
with open(OUT, 'w') as f:
    f.write('\n'.join(keep))
print('pack_keep', len(keep))
