$proj = "C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\library_project.uproject"
$exe = "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
$py = "C:/Users/krame/OneDrive/Documentos/Unreal Projects/library_project/Tools/mh_build.py"
$log = "C:\Users\krame\OneDrive\Documentos\Unreal Projects\library_project\Saved\mh_build.log"
$p = Get-Process UnrealEditor -ErrorAction SilentlyContinue
if ($p) { $p | ForEach-Object { $_.CloseMainWindow() | Out-Null }; try { Wait-Process -Name UnrealEditor -Timeout 60 -ErrorAction Stop } catch { Get-Process UnrealEditor -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep 3 } }
foreach ($n in @('Tomas','Rafael','Clara','Otavio','Isadora','Joaquim')) {
  Get-Process CrashReportClientEditor -ErrorAction SilentlyContinue | Stop-Process -Force
  Add-Content $log "launch $n $(Get-Date -Format HH:mm)"
  $arg = '-ExecutePythonScript="' + $py + ' ' + $n + ' quit"'
  $proc = Start-Process $exe -ArgumentList ('"' + $proj + '"'), '/Engine/Maps/Entry', $arg -PassThru
  try { Wait-Process -Id $proc.Id -Timeout 2400 -ErrorAction Stop } catch { Add-Content $log "TIMEOUT $n"; Stop-Process -Id $proc.Id -Force; Start-Sleep 5 }
  Start-Sleep 5
}
Add-Content $log "ALL DONE $(Get-Date -Format HH:mm)"
