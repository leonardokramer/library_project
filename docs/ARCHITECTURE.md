# Arquitetura (mapa dos Blueprints)

Visão de manutenção: quem faz o quê, como se falam e o que precisa melhorar. Atualizado em 2026-10-29 (auditoria de limpeza).
Detalhes de gameplay e etapas: [ROADMAP.md](ROADMAP.md). Coordenadas da cena: [SCENE_MAP.md](SCENE_MAP.md).

## Convenções
- Pastas: `/Game/Library/{Maps,Blueprints,Characters,UI,Data,Input,Materials,Debug}`. Personagens e AnimBPs em `Characters/` (exceto `BP_LibraryCharacter`, que ainda está em `Blueprints/`).
- Prefixos: `BP_`, `WBP_`, `ABP_` (AnimBP), `DT_`, `DA_`, `M_`/`MI_`, `L_`, `E_`, `S_`, `IA_`/`IMC_` (Enhanced Input), `MM_` (animação do Lyra/template), `SK_`/`SKM_`.
- Nunca editar `/Game/Stationer`, `L_Stationer` nem os assets do template; criar filhos/cópias em `/Game/Library`.

## Blueprints de gameplay
| BP | Responsabilidade | Fala com |
|---|---|---|
| `BP_LibraryCharacter` | Jogador: mira/interação (E), carregar até 3 livros, leque Q, agachar, zoom. Filho de `BP_FirstPersonCharacter` | `BP_Book`, `BP_PlaceZone`, `BP_PlaceGhost`, `BP_Customer`, `BP_LibrarySystem`, `WBP_RequestList` |
| `BP_Book` | Livro unitário: estados de estante/mão/movendo/física/inspeção/emprestado; `GetBookInfo` lê título/autor da `DT_Books` pelo nome da malha | — |
| `BP_PlaceZone` / `BP_PlaceGhost` | Área onde se guarda livro (estante, balcão) e o fantasma amarelo | `BP_Book` |
| `BP_Customer` + `ABP_Customer` | Cliente: pedido ou devolução, andar até a fila, segurar livros, sair | `BP_CustomerSpawner`, `BP_LibrarySystem`, `BP_Book` |
| `BP_CustomerSpawner` | Cria clientes (180–360 s, até 3), gerencia a fila | `BP_Customer`, `BP_LibrarySystem` |
| `BP_LibrarySystem` | Regras do sistema: cadastro, catálogo, empréstimo, devolução, histórico (`SeedHistory`) | `BP_Book`, `BP_Customer`, `BP_CustomerSpawner` |
| `WBP_LibrarySystem` (shell) + `WBP_Screen{Books,Users,Loan,Return}` + `WBP_Row`/`WBP_KeyButton`/`WBP_VirtualKeyboard` | UI estilo Win95. O shell guarda o estado; as telas o chamam por `Owner` (`Bind`) | `BP_LibrarySystem`, `BP_LibraryCharacter`, `BP_BookPreview` |
| `ABP_Body_Library` / `ABP_FP_Library` | Corpo (agachar) e braços em primeira pessoa (pose do livro) | `CtrlRig_FPWarp` |
| `BP_TestDriver` (Debug) | Driver de regressão do ciclo empréstimo/devolução (ver CLAUDE.md), **não está na cena** | `BP_LibrarySystem`, `BP_Customer` |

## Como adicionar...
- **Um livro novo:** uma linha em `/Game/Library/Data/Tables/DT_Books` (nome da linha = nome da malha, ex. `SM_Book_01`; colunas `meshId`, `title`, `author`, `genre`, `synopsis`). Livros com o mesmo título compartilham gênero e sinopse. Consultas: `BP_Book.GetBookInfo` (por malha), `BP_LibrarySystem.GenreOf` / `SynopsisOf` (por título), `BuildCatalog` (lista).
- **Uma estante de livros:** `Tools/shelf_populate.py` (só estantes de madeira reta, `internalMeshType == 1`).
- **Uma tela no sistema:** novo `WBP_Screen*`, aba no `WidgetSwitcher` do shell, `Bind(Owner)`, e incluir os botões em `HlAll`/`SetLeftRules` (foco do controle).

## Dívida técnica (backlog priorizado, da auditoria de 2026-10-29)
Itens com risco médio/alto precisam de struct/enum/DataTable criados **no editor** (o MCP não cria).

1. **Arrays paralelos do histórico** (`HNos/HDocs/HTitles/HReturned/HBooks` + `Seed*`) → `S_LoanRecord` + `DT_SeedLoans`. `HReturned` é gravado como string `"true"`.
2. ~~Catálogo nos mapas do CDO do `BP_Book`~~ **feito (2026-10-29):** `DT_Books` (`S_BookInfo`). Resta `BuildCatalog` e `BuildRequest` ainda varrerem todos os `BP_Book` com `GetAllActorsOfClass`.
3. **Estados numéricos soltos** → enums: `BP_Book.State` (0 estante, 1 mão, 2 movendo, 3 física, 4 inspeção, 6 guardado), `BP_Customer.State/Mode`, `BP_PlaceZone.ZoneType`, `WBP_LibrarySystem.CurTab`.
4. **Pool de pessoas e cadastro duplicados** (`PersonNames/Docs` vs `UserNames/Docs`) → `S_Person` + `DT_People`.
5. **"3 livros" em 6 lugares** (`MaxHeld`, `BuildRequest`, `PickReturner`, `AddBookToLoan`, `OnAddToLoan`, textos) → uma variável/`DA_GameplayConfig`. Números dentro do `TrySpawn` (altura +80, faixa Y 250), poses e tempos do `BP_Customer`, cores do tema Win95.
6. **Telas duplicadas:** `WBP_ScreenLoan` ≈ `WBP_ScreenReturn` (`OnPickUser`, `OnViewRequest`, `Bind` idênticos), `ScreenBooks` ≈ `ScreenUsers` (ordenação). Destaque de foco em 3 lugares (`Hl/HlAll` no Tick, `WBP_Row.HlOn`, `WBP_KeyButton.HlOn`). Sugestão: interface `BPI_ScreenHost`, `WBP_ConfirmDialog`, `WBP_Win95Button`.
7. **Acoplamento:** `GetAllActorsOfClass` varrendo ~1.700 livros em `BuildRequest`/`PreviewTitle`/`BuildCatalog`; `GetActorOfClass` dentro de loops (`BuildListText`); cast no jogador em `WBP_LibrarySystem.Open/CloseSystem`; `OnInteractPressed` com 3 traces/casts (candidato a `BPI_Interactable`); cliente usa o canal `ECC_Vehicle` como gambiarra de colisão.
8. **Responsabilidades demais:** `BP_LibrarySystem` (cadastro + catálogo + empréstimo + devolução + seed + ordenação) → `AC_LoanLedger`/`AC_UserRegistry`; `BP_LibraryCharacter` (livros, inspeção, câmera, interação) → `AC_BookCarrier`/`AC_Interactor`. O tamanho em disco (1,1–1,4 MB) **não** vem da lógica (~400–700 nós): investigar com um Save As depois da limpeza.
9. **Pose de segurar livros repetida** em `ABP_Customer`, `ABP_FP_Library`, `BP_Customer.TakeBooks/HoldReturnBooks` e `BP_LibraryCharacter.SyncHold` (offsets diferentes). `AttachBooksToHand` (re-anexa na `hand_r` após 1,2 s) provavelmente sobrou da primeira versão: testar antes de remover.
10. **Performance leve:** `SyncHold` roda todo Tick mesmo sem livros; `HlAll` no Tick da janela.

## Código morto
**Removido (2026-10-29, compilado e testado no PIE):** os mapas `BookTitles/BookAuthors/BookSynopses/BookGenres` do `BP_Book`; `SetKbdVisible` (2 telas); `CurrentHitLoc`; variáveis do `BP_TestDriver`; `BP_LibrarySystem.LoanDocs/LoanTitles`; `BP_Book.BookTitle/Genre/bInspect`; `BP_Customer.CheckDelivery` e `IsHolding`; animações órfãs de arma/morte/ataque dos manequins.

**Pendente (ainda têm nós que os usam, então exige editar o grafo):**
- `BP_LibraryCharacter.CurrentHitLoc` (só é gravada em `UpdatePlacementPreview`); `CrouchCamOffset`/`CrouchCamDrop` (valem 0; usados em `UpdateCameraEffects`, que ainda chama `SetRelativeLocation` na malha com Z = 0 todo frame).
- `WBP_LibrarySystem.UsingPad` (só gravada em `SetPadMode`); `WBP_ScreenBooks/Users.SetKbdVisible` (nunca chamadas) e os botões `BtnKbd*` escondidos, com eventos ligados.
- `BP_Customer.PlayBell` (corpo vazio, chamada em `OnSpawned` e `UpdateWalk`; gancho do sininho).
- 13 variáveis sem uso do `BP_TestDriver`; `MM_Unarmed_Crouch_Entry/Exit` (sem referências).

## Avisos conhecidos
- 15 avisos `CreateDynamicMaterialInstance ... Bookshelf_Label: Material index 2 is invalid` vêm do pacote Stationer (`BP_BookShelfs_C`): só visual, não editar.
- `SK_Mannequin_Lyra` ainda aponta o preview mesh para `/Game/Characters/Heroes/Mannequin/Meshes/SKM_Manny` (inexistente): só afeta a pré-visualização no editor; corrigir pela UI (Skeleton → Preview Mesh → `SKM_Manny_Simple`), pois o MCP não expõe essa propriedade.
