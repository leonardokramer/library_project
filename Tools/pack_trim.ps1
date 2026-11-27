# Apaga dos pacotes de terceiros NOVOS tudo o que nao esta em Saved/pack_keep.txt (gerado por Tools/pack_deps.py).
# Rode SO com o editor FECHADO. Sem -Apply e uma simulacao (so conta).
# Uso: powershell -File Tools/pack_trim.ps1 [-Apply]
param([switch]$Apply)
$proj = Split-Path $PSScriptRoot -Parent
$content = Join-Path $proj 'Content'
$keepFile = Join-Path $proj 'Saved\pack_keep.txt'
if (Get-Process UnrealEditor -ErrorAction SilentlyContinue) { Write-Error 'Feche o Unreal antes.'; exit 1 }
$keep = @{}
Get-Content $keepFile | ForEach-Object { $keep[$_.Trim().ToLower()] = $true }
$packs = 'MERIDIAN', 'BUILDINGS', 'LIGHTING', 'REALISTIC_MATERIALS', 'Vehicles'
$del = 0; $bytes = 0; $kept = 0
foreach ($p in $packs) {
    $root = Join-Path $content $p
    if (-not (Test-Path $root)) { continue }
    Get-ChildItem $root -Recurse -File | ForEach-Object {
        $rel = $_.FullName.Substring($content.Length).Replace('\', '/')
        $pkg = ('/Game' + ($rel -replace '\.(uasset|umap|uexp|ubulk|uptnl)$', '')).ToLower()
        if ($keep.ContainsKey($pkg)) { $kept++ }
        else {
            $del++; $bytes += $_.Length
            if ($Apply) { Remove-Item $_.FullName -Force }
        }
    }
    if ($Apply) {
        Get-ChildItem $root -Recurse -Directory | Sort-Object { $_.FullName.Length } -Descending |
            Where-Object { -not (Get-ChildItem $_.FullName -Force) } | Remove-Item -Force
    }
}
'{0} arquivos mantidos; {1} {2} ({3:N1} GB)' -f $kept, $del, $(if ($Apply) { 'apagados' } else { 'seriam apagados' }), ($bytes / 1GB)
