# Uso: .\Tools\mh_build_all.ps1 -Names Tomas,Clara [-NoRig]
# Monta cada MHC_<Nome> em Customers/MH_<Nome> com o editor fechado entre um e outro (feche o editor antes).
param([string[]]$Names, [switch]$NoRig)
$root = Split-Path $PSScriptRoot -Parent
$proj = Join-Path $root "library_project.uproject"
$exe = "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
$py = (Join-Path $root "Tools\mh_build.py") -replace '\\','/'
$log = Join-Path $root "Saved\mh_build.log"
$p = Get-Process UnrealEditor -ErrorAction SilentlyContinue
if ($p) { $p | ForEach-Object { $_.CloseMainWindow() | Out-Null }; try { Wait-Process -Name UnrealEditor -Timeout 60 -ErrorAction Stop } catch { Get-Process UnrealEditor -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep 3 } }
foreach ($n in $Names) {
  Get-Process CrashReportClientEditor -ErrorAction SilentlyContinue | Stop-Process -Force
  Add-Content $log "launch $n $(Get-Date -Format HH:mm)"
  $extra = ' quit'; if ($NoRig) { $extra = ' quit norig' }
  $arg = '-ExecutePythonScript="' + $py + ' ' + $n + $extra + '"'
  $proc = Start-Process $exe -ArgumentList ('"' + $proj + '"'), '/Engine/Maps/Entry', $arg -PassThru
  try { Wait-Process -Id $proc.Id -Timeout 2400 -ErrorAction Stop } catch { Add-Content $log "TIMEOUT $n"; Stop-Process -Id $proc.Id -Force; Start-Sleep 5 }
  Start-Sleep 5
}
Add-Content $log "ALL DONE $(Get-Date -Format HH:mm)"
