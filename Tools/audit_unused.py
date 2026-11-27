"""Lista os assets de /Game/Library sem nenhuma referencia (dura ou leve), para revisao.
Nao apaga nada. Saida: Saved/audit_unused.txt. Rodar: py "<caminho>/audit_unused.py"
Atencao: um asset carregado por caminho em texto (string) nao aparece como referencia.
"""
import unreal
OUT = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\audit_unused.txt'
ar = unreal.AssetRegistryHelpers.get_asset_registry()
opts = unreal.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True,
                                             include_searchable_names=True, include_soft_management_references=True,
                                             include_hard_management_references=True)
rows = []
for ad in ar.get_assets_by_path('/Game/Library', recursive=True):
    pk = str(ad.package_name)
    if '/Maps/' in pk:
        continue
    refs = [str(r) for r in (ar.get_referencers(pk, opts) or []) if str(r) != pk]
    if not refs:
        rows.append('%s\t%s' % (str(ad.asset_class_path.asset_name), pk))
rows.sort()
with open(OUT, 'w') as f:
    f.write('\n'.join(rows))
