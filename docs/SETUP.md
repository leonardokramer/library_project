# Setup — clonar e abrir o projeto

## Requisitos
- **Unreal Engine 5.8** (`EngineAssociation: 5.8` no `.uproject`).
- **Git + Git LFS.** Rode `git lfs install` uma vez por máquina. Os `.uasset`/`.umap` vão pelo LFS (veja `.gitattributes`).
- **Pacote da Fab "Stationer" (Barrel & Bark):** https://www.fab.com/listings/367b3203-faa7-4f94-8302-0d87f7768c25
- **Pacote da Fab "1996 Police Headquarters" (Dekogon):** https://www.fab.com/listings/ca315ca8-0bee-4e2c-846e-6995f029c797 (classificação Mature: precisa liberar o filtro de conteúdo maduro na conta). Só usamos o computador do balcão.
- **Pacote da Fab "Jobsite VOL.12 - Office" (Dekogon):** https://www.fab.com/listings/c657df25-2ce6-4a62-a147-58778e3085ac (ainda não usado na cena).

## O que NÃO está no git
- `/Content/Stationer/` (cerca de 2 GB). Ignorado de propósito: a licença da Fab não permite redistribuir os assets, e o tamanho estoura a cota de LFS. **Todo o nível `L_Library` depende dele.**
- `/Content/PoliceDepartment/` (cerca de 57 MB, só os meshes e materiais do computador, telefone e mouse pad migrados do projeto da delegacia) e `/Content/JOBSITE/` (Jobsite VOL.12). Ignorados pelo mesmo motivo. **O computador do balcão (`Computer_Counter`) e o `MI_ComputerScreen` dependem do `PoliceDepartment`**; sem ele a tela e o computador aparecem como referência quebrada.
- Pastas geradas: `Binaries/`, `DerivedDataCache/`, `Intermediate/` e `Saved/`.

## Restaurar numa máquina nova
1. `git clone <repo>` e depois `git lfs pull`.
2. Pela Fab, no launcher ou no próprio editor, adicione o pacote **Stationer** a este projeto. Ele precisa ficar exatamente em **`/Content/Stationer/`**, sem renomear a pasta.
2b. Para o computador do balcão: baixe o projeto **1996 Police Headquarters** como projeto separado (versão 5.7 ou abra com a 5.8 e converta uma cópia) e use *Asset Actions → Migrate* de `SM_ComputerMonitor_01a`, `SM_ComputerCPU_01a`, `SM_ComputerKeyboard_01a`, `SM_ComputerMice_01a`, `SM_Computer_01a` e `SM_Telephone_01a` para `/Content/` deste projeto (vai para `/Content/PoliceDepartment/`, com o `MasterMaterial`). O Jobsite VOL.12 entra por *Add to Project*, em `/Content/JOBSITE/`.
3. Abra o `library_project.uproject`. O mapa padrão é `/Game/Library/Maps/L_Library`.
4. Se o Unreal perguntar sobre `GameFeatureData` no Asset Manager, aceite. A entrada já está no `Config/DefaultGame.ini`.

## O que está no repo e veio do template First Person
`/Content/FirstPerson`, `/Content/Input` e `/Content/Characters/Mannequins` (cerca de 95 MB). Entram no git
normalmente: o template é da Epic. O `BP_LibraryCharacter` e o `BP_LibraryGameMode` herdam dos Blueprints
do `FirstPerson`, então essas pastas **não podem ser apagadas** sem reparentar os dois.
As armas (`/Content/Weapons`), o `LevelPrototyping`, o mapa `Lvl_FirstPerson` e as animações de arma foram
removidos na limpeza de 2026-10-29 (estão no histórico do git se precisar).

## Configs importantes (já no repo)
- `Config/DefaultEngine.ini`:
  - Mapa padrão = L_Library.
  - Object Channel **`PlaceZone`** (`ECC_GameTraceChannel1` = `ObjectTypeQuery7`) e o perfil de colisão `PlaceZone`.
  - Lumen.
  - **Mudanças de canal ou perfil exigem reiniciar o editor.**
- `.mcp.json`: servidor MCP do Unreal em `http://127.0.0.1:8000/mcp`. Depende dos plugins `ModelContextProtocol` e `AllToolsets` (habilitados no `.uproject`). O AllToolsets liga o plugin GameFeatures.
