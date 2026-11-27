"""Compila todos os Blueprints de /Game/Library e lista os que ficam com erro ou aviso.
Nao salva nada. Saida: Saved/audit_compile.txt. Rodar: py "<caminho>/audit_compile.py"
"""
import unreal
OUT = r'C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\audit_compile.txt'
ar = unreal.AssetRegistryHelpers.get_asset_registry()
rows = []
n = 0
for ad in ar.get_assets_by_path('/Game/Library', recursive=True):
    c = str(ad.asset_class_path.asset_name)
    if c not in ('Blueprint', 'WidgetBlueprint', 'AnimBlueprint'):
        continue
    bp = unreal.load_asset(str(ad.package_name))
    try:
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        st = str(bp.get_editor_property('status'))
    except Exception as e:
        st = 'EXC ' + str(e)[:120]
    n += 1
    if 'UP_TO_DATE' not in st.upper():
        rows.append('%s\t%s' % (st, str(ad.package_name)))
with open(OUT, 'w') as f:
    f.write('compiled %d\n' % n)
    f.write('\n'.join(rows))
