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
| `BP_CustomerSpawner` | Cria clientes (180–360 s, até 3), gerencia a fila. **Ritmo adaptativo:** quando um cliente sai e a loja fica vazia, `AfterServed` (chamada no fim de `OnCustomerServed`) reagenda o próximo spawn para `EmptyMinInterval`–`EmptyMaxInterval` (20–40 s, nunca menos de 5 s). **Cuidado:** variáveis novas em um ator já salvo no mapa nascem com 0 (não herdam o padrão da classe); com tempo 0 o timer seria cancelado, por isso a instância do mapa foi ajustada para 20/40. Os valores 180/360 e 5 s estão **na instância do mapa**, e prevalecem sobre o padrão da classe. `ShuffleSeed` (no `BeginPlay`) consome de 0 a ~1.000 sorteios conforme o relógio, porque o gerador global do Blueprint começava igual a cada partida e o primeiro cliente saía sempre o mesmo | `BP_Customer`, `BP_LibrarySystem` |
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

1. ~~Arrays paralelos do histórico e do seed~~ **feito (2026-10-29):** `BP_LibrarySystem.Loans` (`S_LoanRecord`); só `AddHistory` e `MarkReturned` escrevem; o seed vem da `DT_SeedLoans`.
2. ~~Catálogo nos mapas do CDO do `BP_Book`~~ **feito (2026-10-29):** `DT_Books` (`S_BookInfo`). Resta `BuildCatalog` e `BuildRequest` ainda varrerem todos os `BP_Book` com `GetAllActorsOfClass`.
3. **Estados numéricos soltos** (`BP_Book.State`, `BP_Customer.State/Mode`, `BP_PlaceZone.ZoneType`, `WBP_LibrarySystem.CurTab`) → enums: ver a seção "Enums" abaixo (bloqueado pelo MCP).
4. ~~Pool de pessoas e cadastro duplicados~~ **feito (2026-10-29):** pool na `DT_People` (10 linhas `P01`–`P10`, struct `S_Person`) e cadastro em `BP_LibrarySystem.Users` (array de `S_Person`, 5 iniciais no CDO). **Limitação do MCP:** o `DataTableTools.set_rows`/`get_rows` não enxerga o campo `name`; a tabela foi criada por CSV (`import_file`).
5. ~~"3 livros" em 6 lugares~~ **feito (2026-10-29):** `BP_LibrarySystem.MaxBooks` (padrão 3) é lido por `PickReturner`, `WBP_LibrarySystem.AddBookToLoan`/`ToggleReturn` e `WBP_ScreenBooks.OnAddToLoan`; as mensagens ficaram genéricas ("Limite de livros por empréstimo atingido."). `BP_Customer.MaxRequestBooks` (padrão 3) limita o pedido do cliente (ele não guarda referência ao sistema): **mantenha os dois iguais**. `BP_LibraryCharacter.MaxHeld` (livros na mão) continua separado. Pendem os números de cena do `TrySpawn` (altura +80, faixa Y 250), as poses (`TakeBooks`/`HoldReturnBooks`/`SyncHold`) e as cores do tema Win95.
6. **Telas duplicadas:** `WBP_ScreenLoan` ≈ `WBP_ScreenReturn` (`OnPickUser`, `OnViewRequest`, `Bind` idênticos), `ScreenBooks` ≈ `ScreenUsers` (ordenação). Destaque de foco em 3 lugares (`Hl/HlAll` no Tick, `WBP_Row.HlOn`, `WBP_KeyButton.HlOn`). Sugestão: interface `BPI_ScreenHost`, `WBP_ConfirmDialog`, `WBP_Win95Button`.
7. **Acoplamento:** `GetAllActorsOfClass` varrendo ~1.700 livros em `BuildRequest`/`PreviewTitle`/`BuildCatalog`; `GetActorOfClass` dentro de loops (`BuildListText`); cast no jogador em `WBP_LibrarySystem.Open/CloseSystem`; `OnInteractPressed` com 3 traces/casts (candidato a `BPI_Interactable`); cliente usa o canal `ECC_Vehicle` como gambiarra de colisão.
8. **Responsabilidades demais:** `BP_LibrarySystem` (cadastro + catálogo + empréstimo + devolução + seed + ordenação) → `AC_LoanLedger`/`AC_UserRegistry`; `BP_LibraryCharacter` (livros, inspeção, câmera, interação) → `AC_BookCarrier`/`AC_Interactor`. O tamanho em disco (1,1–1,4 MB) **não** vem da lógica (~400–700 nós): investigar com um Save As depois da limpeza.
9. **Pose de segurar livros repetida** em `ABP_Customer`, `ABP_FP_Library`, `BP_Customer.TakeBooks/HoldReturnBooks` e `BP_LibraryCharacter.SyncHold` (offsets diferentes). `AttachBooksToHand` (re-anexa na `hand_r` após 1,2 s) provavelmente sobrou da primeira versão: testar antes de remover.
10. **Performance leve:** `SyncHold` roda todo Tick mesmo sem livros; `HlAll` no Tick da janela.

## Código morto
**Removido (2026-10-29, compilado e testado no PIE):** os mapas `BookTitles/BookAuthors/BookSynopses/BookGenres` do `BP_Book`; `SetKbdVisible` (2 telas); `CurrentHitLoc`; `WBP_LibrarySystem.UsingPad` e `SetPadMode`; variáveis do `BP_TestDriver`; `LoanDocs/LoanTitles`; `BookTitle/Genre/bInspect`; `CheckDelivery`/`IsHolding`; animações órfãs de arma/morte/ataque dos manequins e `MM_Unarmed_Crouch_Entry/Exit`.

**Pendente (decisão consciente):**
- `BP_LibraryCharacter.CrouchCamOffset/CrouchCamDrop` (valem 0, mas fazem parte da cadeia do agachar aprovada pelo usuário em `UpdateCameraEffects`).
- Botões `BtnKbd*` escondidos, com eventos ligados (`OnKbdSearch/Name/Doc`).
- `BP_Customer.PlayBell` (corpo vazio; gancho do sininho).

## Enums (`/Game/Library/Data/Enums`): criados, ainda não usados
`E_BookState` (6 entradas), `E_CustomerMode` (2) e `E_ZoneType` (2) existem, com os nomes internos padrão (`NewEnumerator0…`). **O MCP não cria variáveis do tipo enum** (só primitivos, structs e objetos), então a migração precisa ser feita no editor: trocar o tipo de `BP_Book.State`, `BP_Customer.Mode` e `BP_PlaceZone.ZoneType` quebra os nós que os leem/gravam (BP_Book: 7 funções + `EventGraph`; BP_Customer: 5; BP_PlaceZone/BP_LibraryCharacter: 3). Cuidados: o valor de `ZoneType` é definido **por instância** no mapa (169 zonas) e se perderia na troca de tipo; no `BP_Book`, o estado "guardado" é hoje `6` e viraria a 6ª entrada (índice 5).

## Avisos conhecidos
- 15 avisos `CreateDynamicMaterialInstance ... Bookshelf_Label: Material index 2 is invalid` vêm do pacote Stationer (`BP_BookShelfs_C`): só visual, não editar.
- `SK_Mannequin_Lyra` ainda aponta o preview mesh para `/Game/Characters/Heroes/Mannequin/Meshes/SKM_Manny` (inexistente): só afeta a pré-visualização no editor; corrigir pela UI (Skeleton → Preview Mesh → `SKM_Manny_Simple`), pois o MCP não expõe essa propriedade.
