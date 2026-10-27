# Mapa da cena — L_Library (cópia de L_Stationer)

Unidades em cm, coordenadas do mundo. +X aponta para a porta de entrada (lado leste).

## Visão geral
- É um nível comum, **sem World Partition**. São cerca de 8 mil atores: 7.692 StaticMeshActor, 223 GroupActor, cerca de 40 `BP_BookShelfs`, cerca de 40 luzes `BP_Light_0X` (as pendentes), 17 CineCameras e 1 LevelSequence (`Sequence_01`).
- Limites da construção: X de -838 a 1082, Y de -538 a 537, Z de -118 a 870.
- **Térreo:** piso em Z≈10. Papelaria, tintas, cavaletes e estantes.
- **Mezanino e café:** piso em Z≈330. Estantes por gênero (Economy, Fantasy, Biography...), mesas e o balcão do café.
- A iluminação vem das luzes pendentes, das calhas fluorescentes e do PostProcessVolume em (510, 180, 110). Ficam na pasta `Lights/`: SkyAtmosphere, ExponentialHeightFog, DirectionalLight, PostProcessVolume, SkyLight e SM_Sky_Box. Há também 1 BoxReflectionCapture.

## Pontos importantes
| Coisa | Ator | Onde |
|---|---|---|
| Porta de entrada | `WallwDoor01` | X≈1038, Y de 149 a 427 |
| **Balcão do atendente** | `CheckoutBlock_2` | X de -538 a -472, Y de 44 a 292, altura 134 |
| Caixa registradora | `GroupActor250` (`SM_PAD_CashRegister_*`) | (-500, 255, 135) |
| Placa "Cashier" | `CashierSign` | X -506, Y de 150 a 221, Z de 261 a 290 |
| Escada para o mezanino | `StairHalf_02` | X de -450 a -164, Y de 292 a 443, sobe de Z 10 até 434 |
| Paredes atrás do balcão | `Wall24`, `Wall25` | X≈-740 |
| Máquina de café | `SM_CS1_CoffeeMachine_01a_*` | (985, 166, 454) |
| Mesas do café | `TableBig_01`, `TableSmall_*` | X de 559 a 1015, Z de 330 a 415 |

**Espaço do atendente:** fica entre o balcão e a parede, X de -730 a -538, Y de 44 a 292.
**O cliente fica** do lado +X do balcão, em X≈-420.

## Atores de gameplay que adicionamos (pasta `Gameplay/`)
| Ator | Posição | Para quê |
|---|---|---|
| `PlayerStart` | (-640, 170, 102), yaw 0 | Jogador nasce atrás do balcão, olhando para a loja |
| `NavMeshBounds` | centro (122, 0, 220), escala (9.8, 5.5, 2.6) | NavMesh nos dois andares |
| `NPC_Spawn` (`Gameplay/NPCPoints`) | (1000, 207, 20), yaw 180 | Porta: o NPC surge e some aqui (a folha da porta fica por volta de Y 165–245) |
| `NPC_Entry` | (820, 207, 20) | Primeiro passo: entra em linha reta pela porta |
| `NPC_Counter` | (-438, 170, 20), yaw 180 | Posição 0 da fila, colada no balcão (a frente do balcão fica em X -472) |
| `NPC_Exit` | (-380, 255, 20) | Começo da faixa de saída (Y≈250, paralela à fila) |
| `CustomerSpawner` (`Gameplay/NPCs`) | (900, 207, 20) | Gera os clientes e controla a fila |
| `LibrarySystem` (`Gameplay/`) | (-506, 256.5, 148), sobre a caixa registradora | "Computador": banco de usuários/empréstimos e a caixa de colisão que o E encontra |

**Corredor de clientes:** os traces mostram livre o trecho de Y 170 a 290 entre o balcão e a porta. Há expositores baixos em Y 10–166 (ex.: `Bookshelf_6`); a escada começa em Y 292 e a `Column3` fica em (-460, 300). A fila fica em Y 170 e a saída em Y 250–255.

### NavMesh sem ilhas em cima dos móveis (pasta `Gameplay/NavModifiers`)
O Recast gera NavMesh em qualquer superfície plana, inclusive mesas, balcões e estantes. Para evitar isso, há 8 `NavModifierVolume` com `AreaClass = NavArea_Null` (`NavBlock_{Ground,Upper}_{A..D}`):
- No térreo eles cobrem Z de 40 a 300, e no mezanino Z de 360 a 850. A navegação só existe rente aos pisos (Z≈10 e Z≈330).
- O retângulo da escada (X de -480 a -134, Y de 262 a 473) fica **de fora** dos volumes. Por isso os volumes são 4 caixas por andar em volta dele.
- Se aparecer outra área elevada que precise ser andável (rampa, palco), abra um buraco nos volumes ali.

## Clientes: `BP_Customer` (`/Game/Library/Characters/`, pasta `Gameplay/NPCs`)
Não há clientes colocados na cena: todos nascem pelo `BP_CustomerSpawner`.
- **Porta falsa por enquanto:** a porta está fundida na malha `SM_WallwDoor01` e não abre. O cliente surge em `NPC_Spawn`, logo do lado de dentro, e some quando volta lá. `PlayBell()` é um gancho vazio para o som do sininho, porque o projeto não tem nenhum som ainda.
- **Configuração:**
  - Pai `Character`, malha `SKM_Quinn_Simple` com **`AnimClass = ABP_Customer`** (`/Game/Library/Characters/`), offset Z -89 e yaw -90.
  - O `ABP_Customer` é uma cópia do `ABP_Unarmed` em que `ShouldMove = GroundSpeed > 3`, sem exigir aceleração.
  - No original, a aceleração da IA chega zerada em quadros alternados. O `ShouldMove` piscava e a caminhada ficava picotada, "como W apertado aos toquinhos".
  - `AIController` com `AutoPossessAI = PlacedInWorldOrSpawned`.
  - **Colisão entre clientes:** no BeginPlay, a cápsula vira ObjectType **Vehicle** e passa a **ignorar Vehicle**. Os clientes atravessam uns aos outros (sem isso, quem saía e quem entrava travavam na porta), mas continuam sólidos para o jogador, porque o perfil Pawn bloqueia Vehicle. Por isso o `TraceCustomer` do personagem procura `ObjectTypeQuery5` (Vehicle).
  - `bUseControllerRotationYaw = false` e `bOrientRotationToMovement = true`, porque senão o `SetActorRotation` é ignorado. `MaxWalkSpeed` é 150.
  - **`NavMovementProperties.bUseAccelerationForPaths = true`** no CDO (os spawnados herdam). Sem isso, o NPC desliza em pose idle: o `ABP_Unarmed` só ativa a caminhada (`ShouldMove`) com aceleração ≠ 0, e o movimento por IA não gera aceleração por padrão.
- **Variáveis:**
  - `State`: 0 recém-criado, 1 andando, 2 no balcão (pode pedir), 3 pedido mostrado, 4 indo embora, **5 esperando na fila**.
  - `RequestedTitles` e `RequestedAuthors` (arrays de string), `CarriedBooks`.
  - Caminho: `Path` (Array Vector), `PathIdx`, `QueueIndex`, `Leaving`, `FineApproach`, `FineTime`.
  - Preenchidas pelo spawner: `Spawner`, `CounterZone` e `ExitPoints`.
- **BeginPlay:** só `BuildRequest()`. Ele sorteia de 1 a 3 **títulos distintos** entre os `BP_Book` da cena que estão no catálogo, **excluindo títulos já pedidos por outros clientes vivos** (via `GetRequested()` de cada um). Se não sobrar nada, o pedido fica vazio e o spawner descarta o cliente.
- **`StartPath(Points)`:** grava o caminho, zera o `PathIdx`, vai para State 1 (ou 4 se `Leaving`) e faz `SimpleMoveToLocation(Points[0])`.
- **`UpdateWalk(Delta)`**, chamado no Tick em State 1 ou 4:
  - Ponto intermediário a menos de 60 cm: passa para o próximo ponto.
  - Último ponto e saindo, a menos de **120 cm** (ou travado): `PlayBell`, destrói os `CarriedBooks` e se destrói. É assim que ele some na porta. Com 60 cm, às vezes ele parava antes, porque o navmesh acaba antes da parede, e ficava preso.
  - **Detector de travado:** `StuckTime` soma enquanto a velocidade XY for < 5 cm/s e zera quando ele anda (também zera no `StartPath`). Passou de 1,5 s: num ponto intermediário, avança para o próximo; no último ponto, some (saindo) ou entra na aproximação fina (chegando).
  - Último ponto e chegando, a menos de 60 cm: entra em **aproximação fina**. Chama `StopMovement` no controller e depois `AddMovementInput(Normalize2D(alvo - posição), 0.5)` até ficar a menos de 6 cm ou passar 1,5 s.
  - Chegou: `Arrive()` → State 2 se `QueueIndex == 0`, senão State 5. É isso que cola o NPC no balcão (para em X≈-437).
- **`GoToSlot(Index, Loc)`**, chamado pelo spawner quando a fila anda:
  - State 5: `StartPath([Loc])`.
  - State 1: troca o último ponto do caminho e, se já está indo para ele, refaz o `SimpleMove`.
  - States 2, 3 e 4: ignora.
- **Tick:** os States 2, 3 e 5 giram suavemente para yaw 180.
- **Identidade:** `CustomerName` e `CustomerDoc` (string), lidos por `GetIdentity() → (Name, Doc)`. São preenchidos em **`OnSpawned()`**, que o spawner chama logo depois do spawn: ela toca o `PlayBell` e chama `BP_LibrarySystem.PickPerson()` (via `GetActorOfClass`).
- **`Interact() → (Result int, Message text)`.** Quem cuida da UI é o personagem. O cliente não conhece o `BP_LibraryCharacter`.
  - **State 2 ou 3:** vai para State 3 e devolve `1` + `BuildListText()`. O texto é `Nome: X`, `Documento: Y`, uma linha em branco e depois uma linha por livro: `- Título  (Autor)`. Com o pedido já mostrado, o E só mostra o papel de novo.
  - **O E não entrega mais os livros.** A entrega acontece só pelo sistema (`BP_LibrarySystem.ConfirmLoan` → `CompleteLoan()`).
  - Os outros States (inclusive quem está na fila) devolvem `0`.
- **`CompleteLoan()`:** `TakeBooks()`, `Leaving = true`, `StartPath(ExitPoints)` e `Spawner.OnCustomerServed(self)`.
- **`CheckDelivery()`** (não é mais chamado; a mesma lógica agora está em `BP_LibrarySystem.TitlesMatch`): pega `CounterZone.GetBooksInZone()`.
  - Se a quantidade for diferente da pedida, a entrega está errada.
  - Senão, para cada livro, procura o título numa cópia de `RequestedTitles` e remove (multiconjunto). Se algum título não bater, a entrega está errada.
  - A comparação é **por título**, e não por malha: `SM_Book_02` e `SM_Book_07` são os dois "Diary of Ms. Rose".
- **`TakeBooks()`:** desliga a colisão de cada livro do balcão e faz `AttachActorToComponent(Mesh, "hand_r", SnapToTarget, SnapToTarget, KeepWorld)`. Depois aplica `SetActorRelativeTransform`:
  - Rotação relativa fixa **(Roll -86.16, Pitch -3.04, Yaw 85.99)**: o livro fica **em pé ao lado da coxa**, preso pela borda de cima (4 cm abaixo do topo), com a capa para fora e a lombada para trás.
  - Posição = `RotateVector((s - c.x, -c.y, (4 - h.z) - c.z), rot)`, em que `(c, h)` = `GetBookExtents` e `s = ((n-1)/2 - i) * 4.6`. A pilha fica centrada na mão.
  - Valores calculados com a rotação do osso `hand_r` no idle (lida no Simulate) e conferidos com foto.
  - Ajuste fino: mude a rotação/offset no grafo do `TakeBooks`. Para testar rápido, use o modo Simulate + `set_actor_transform(worldspace=false)` nos livros presos.
  - **Não há reposição na estante.**

## Fila: `BP_CustomerSpawner` (`/Game/Library/Blueprints/`, ator `CustomerSpawner`)
- **Instance-editable:**
  - Pontos: `DoorPoint = NPC_Spawn`, `EntryPoint = NPC_Entry`, `CounterPoint = NPC_Counter`, `ExitLanePoint = NPC_Exit` e `CounterZone = Zone_Counter`.
  - Tempo: `FirstDelay` 5 s, `MinInterval` **180 s** e `MaxInterval` **360 s**. Antes eram 60–120 s; com o sistema, o ciclo ficou longo e a ideia é o jogador esperar um pouco, com fila só às vezes.
  - Fila: `MaxCustomers` 3 e `SlotStep` (90, 0, 0).
- `Queue` (Array BP_Customer) guarda os clientes na ordem da fila. A posição i fica em `CounterPoint + SlotStep * i`, ou seja, X -438, -348, -258 e -168 em Y 170.
- **BeginPlay:** `SetTimerbyFunctionName("TrySpawn", FirstDelay)`.
- **`TrySpawn()`:**
  - Primeiro rearma o timer com `RandomFloatInRange(Min, Max)`.
  - Se a `Queue` tiver menos que `MaxCustomers`: spawna o `BP_Customer` em `DoorPoint + (0, 0, 80)`, yaw 180. Depois preenche `Spawner`, `CounterZone` e `ExitPoints = [ExitLanePoint, (EntryPoint.x, 250), DoorPoint]`.
  - Se o pedido veio vazio, destrói o cliente.
  - Senão: entra na `Queue`, recebe o `QueueIndex`, chama `OnSpawned` (sininho + identidade) e `StartPath([EntryPoint, posição da vez])`.
  - Os arrays de pontos são montados em **variáveis locais com `Add`**, porque o MakeArray do DSL só aceita 1 elemento.
- **`OnCustomerServed(c)`:** tira `c` da `Queue` e chama `GoToSlot(i, posição i)` em todos os outros. A fila anda assim que o da frente pega os livros, enquanto ele sai pela faixa Y≈250.
- **Verificado no PIE:**
  - Intervalos de 2–4 s formam a fila de 4, com o da frente em State 2 em X -437 e os outros em State 5.
  - Livro errado + E: nada acontece.
  - Livros certos + E: o da frente sai e some na porta, os outros avançam uma posição e um 5º cliente entra no fim da fila.

## Sistema da livraria: `BP_LibrarySystem` (`/Game/Library/Blueprints/`, ator `LibrarySystem`)
É o "computador". Por enquanto fica na caixa registradora; quando houver um monitor de verdade, basta mover o ator.
- **Colisão:** a raiz é o `Collision` (BoxComponent, extent (30, 22, 16), perfil `OverlapAllDynamic`, ObjectType **WorldDynamic** = `ObjectTypeQuery2`, oculto no jogo). Ele cobre a caixa registradora (X de -533 a -479, Y de 237 a 276, Z de 134 a 161), logo ao lado da `Zone_Counter`.
- **Instance-editable:** `Spawner = CustomerSpawner` e `CounterZone = Zone_Counter`.
- **Dados** (arrays paralelos, porque o MCP não cria struct; seeds no CDO):
  - `PersonNames[]`/`PersonDocs[]`: pool de 10 pessoas (Helena Duarte 48.213.907, Marcos Vieira 31.774.520, Beatriz Nakamura 52.908.163, Tomás Albuquerque 27.461.398, Lúcia Ferraz 63.085.214, Rafael Monteiro 19.630.842, Clara Bittencourt 44.517.069, Otávio Reis 38.902.475, Isadora Lins 57.246.381, Joaquim Prado 22.358.716).
  - `UserNames[]`/`UserDocs[]`: o cadastro. Começa com Helena, Tomás, Clara, Otávio e Joaquim; os outros cinco precisam ser cadastrados. O cadastro vive só durante a sessão (não há SaveGame ainda).
  - `LoanDocs[]`, `LoanTitles[]` (títulos juntados por ` | `) e `LoanCount`.
  - Rascunho: `DraftDoc`, `DraftTitles[]` e `DraftStatus`.
- **Funções:**
  - `NormDoc(Doc)` tira pontos, traços e espaços. Toda comparação de documento passa por ela, então "27461398" acha "27.461.398".
  - `FindDocIndex(Doc) → int`.
  - `PickPerson() → (PName, PDoc)` sorteia do pool alguém que não esteja na loja (lê `GetIdentity` de todos os `BP_Customer`).
  - `BuildCatalog() → (Titles, Authors, Counts)`:
    - Os títulos e autores vêm dos mapas `BookTitles`/`BookAuthors` de um `BP_Book` qualquer da cena, sem repetir título, então todos os 19 títulos aparecem, mesmo com 0 cópias.
    - `Counts` = livros com `State == 0` que **não** estão no balcão (na estante, ou parados em outro lugar).
  - `FindUsers(Query) → (Names, Docs)`: com `Query` vazia, lista todos. Senão, `Contains` (sem diferenciar maiúsculas) no nome **ou** no documento normalizado.
  - `RegisterUser(NewName, NewDoc) → (Ok, Msg)`: recusa vazio ou documento repetido.
  - `CounterTitles()` e `TitlesMatch(A, B)` (multiconjunto, mesma lógica do antigo `CheckDelivery`).
  - **`ConfirmLoan(Doc, Titles) → (Ok, Msg)`**, nesta ordem:
    1. Sem itens: "Nenhum livro lançado."
    2. Documento fora do cadastro: "Selecione um usuário cadastrado."
    3. Sem cliente da frente em State 2/3: "Não há cliente no balcão."
    4. Documento ≠ o do cliente: "Este usuário não é o cliente do balcão."
    5. Balcão ≠ lançamento: "Os livros no balcão não conferem com o lançamento."
    6. Lançamento ≠ pedido: "Estes não são os livros do pedido."
    7. Tudo certo: registra o empréstimo, `ClearDraft()`, `Cust.CompleteLoan()` e devolve "Empréstimo registrado."
  - `ClearDraft()`.

## Tela do sistema: `WBP_LibrarySystem` (`/Game/Library/UI/`)
- **Layout:**
  - Tela cheia, com fundo quase preto esverdeado (alfa 0,97) e texto verde de terminal.
  - **Padding esquerdo de 470 px**, para o papel do pedido (`WBP_RequestList`, x 40) ficar visível ao lado.
  - Três colunas: **ACERVO** (`SearchBox` + `BookList`), **USUÁRIO** (`UserSearch` + `UserList` + "Cadastrar novo usuário" → `NewUserPanel` com `NewName`, `NewDoc`, Salvar e Cancelar) e **NOVO EMPRÉSTIMO** (`SelectedUserText`, `LoanItems`, `StatusText` em âmbar, "Lançar empréstimo" → `ConfirmPanel` com Confirmar e Voltar, "Limpar lançamento" e "Sair do sistema").
- **Linhas:** `WBP_Row` (Button + TextBlock `Label`), com `Setup(InOwner, InKind, InValue, InValue2, InIndex, InLabel, InEnabled)`. O clique chama `Owner.OnRowClicked(Kind, Value, Value2, Index)`.
  - Kind 0 = livro (adiciona aos itens, máximo de 3; a linha fica desabilitada com 0 cópias).
  - Kind 1 = usuário (seleciona).
  - Kind 2 = item lançado (remove).
- **Variáveis:** `System`, `SelDoc`, `SelName`, `Items[]` e `Status`.
- **`Open(Sys)`** carrega o rascunho do sistema, esconde os painéis, faz `ResolveName` e depois `RefreshAll`. Cada mudança chama `SaveDraft()`, que grava de volta no sistema.
- **Eventos (`BindToEventProperty`):** `OnTextChanged` do `SearchBox` → `RefreshBooks` e do `UserSearch` → `RefreshUsers`. `OnClicked` dos 8 botões → `OnNewUser`, `OnSaveUser`, `OnCancelUser`, `OnLaunch`, `OnConfirm`, `OnBack`, `OnClear` e `OnExit`.
- **`OnConfirm`:** chama `System.ConfirmLoan(SelDoc, Items)`.
  - Se der certo: limpa as variáveis e chama `CloseSystem(true)`, que esconde o papel (`HideRequest` do personagem).
  - Se der errado: mostra o aviso e salva o rascunho.
- **`CloseSystem(Done)`:** `SaveDraft`, `RemoveFromParent`, `SetInputModeGameOnly` e esconde o cursor.
- **Ainda falta:** Esc/B não fecham a tela (só o botão "Sair do sistema"). O controle navega pelos botões do UMG, mas ainda não foi testado.

## Game setup
- World Settings → GameMode Override = `/Game/Library/Blueprints/BP_LibraryGameMode`, que é filho de `BP_FirstPersonGameMode`. Controller: `BP_FirstPersonPlayerController`.
- Pawn: **`/Game/Library/Blueprints/BP_LibraryCharacter`**, filho de `BP_FirstPersonCharacter`. Configuração:
  - **Sem pulo:** `JumpMaxCount = 0` e `JumpZVelocity = 0`.
  - **Caminhada lenta:** `MaxWalkSpeed = 200` (o template usa 600).
  - `MaxAcceleration = 800` e `BrakingDecelerationWalking = 1200`, para começar e parar com suavidade.
  - Para ajustar o ritmo, mude isso no CharMoveComp do CDO.
- Animações de andar para NPCs: `/Game/Characters/Mannequins/Anims/Unarmed/BS_Idle_Walk_Run` (blendspace por velocidade) e `.../Unarmed/Walk/MF_Unarmed_Walk_*`.
- O template First Person também trouxe `/Game/FirstPerson`, `/Game/Input`, `/Game/Characters/Mannequins`, `/Game/LevelPrototyping` e `/Game/Weapons`. As armas não serão usadas.

## Livros e estantes
- As estantes são instâncias de `BP_BookShelf_01` (só o móvel e a plaquinha). O gênero vem do material da placa (`MI_Bookshelf_Label_<Genero>`).
- Cada estante tem 7 prateleiras. Em geral **2 têm livros soltos** (`SM_Book_XX`, um ator por livro) e **5 são fileiras fundidas** (`SM_BookStack_XX`, um modelo só de cerca de 80 cm). As fileiras fundidas não dá para separar.
- No total são 883 livros soltos e 108 fileiras fundidas. As capas vêm todas de uma única textura (`MI_BookCoversCC0`), então os títulos se repetem ("Lost Souls", "Colorblind", "Diary of Ms. Rose", "The Attic"...).

### Estantes por gênero
- **Regra: só estantes com `internalMeshType == 1` (prateleira de madeira reta) recebem livros.** O tipo 2 (arcos de arame tipo adega: S3, S27) e o tipo 3 (pegboard com ganchos: S5, S6, S41) ficam só com tintas/produtos, porque livros ali ficam estranhos. As ilhas (corpo 02: S, S13, S37–S40) e as de tintas S2, S34, S35 também ficaram como cenário.
- **Layout (2026-10-27).** 24 estantes de livro (1 corpo 01, tipo 1):

  | Gênero | Estantes (rótulo `BP_BookShelfsN`) | Títulos (malhas) |
  |---|---|---|
  | Sci-Fi | 11, 8 (mezanino), 30, 31 (térreo) | First Contact (15), Space Walk (22) |
  | Science | 7, 9, 22 | Colorblind (10), Theoretical Calculus (13), Analytic Geometry (17) |
  | History | 10, 23 | Cities (11), The Illusion of Democracy (20) |
  | Novels | 14, 15, 24 (mezanino), 28, 29 (térreo) | L'homme (03), Summer's End (04), The Lake Murders (26) |
  | Fantasy | 16, 17 (mezanino), 4, 33 (térreo) | Lost Souls (09), Treasures of Al-Saban (21), Chrysanthemums (12) |
  | Economy | 18, 36 | Open Office Design (08), Data Structures (14) |
  | Dictionaries | 19 (mezanino), 26 (térreo) | Book Covers Guide (01), Classic Poems (05) |
  | Biography | 20, 21 | Diary of Ms. Rose (02, 07), Cats and Their Humans (29) |

  Alguns encaixes são provisórios (Data Structures em Economy, Classic Poems em Dictionaries) porque só existem as 8 placas de gênero da Fab.
- **Placa:** o BP `BP_BookShelfs` monta a placa pelas variáveis `bookshelf_LabelType` (1 = com placa) e `bookshelf_LabelMaterial` (índice em `boolshelf_Label_MaterialType`: 1 Biography, 2 Dictionaries, 3 Economy, 4 Fantasy, 5 History, 6 Novels, 7 Sci-Fi, 8 Science). Mudar o material direto no componente não funciona (o construction script refaz).
- **Geometria (espaço local da estante):** prateleiras em z relativo 20, 60, 95, 130, 165, 200 e 235; frente dos livros em y local -16,6 (livro com o mesmo yaw da estante); largura útil x de -66 a +66 (o interior vai a ±69,6, e o layout antigo da History passava disso, por isso os livros atravessavam a lateral). Livros têm 17–20 cm de profundidade e até 29 cm de altura.
- **Povoamento:** blocos de 3–6 exemplares iguais (2–3 nas prateleiras de cima), enchimento de 60/65/65/50/25/12/8% da largura nas 7 prateleiras (escala 0,5 no térreo), resto livre para devolução. Script: `docs/shelf_populate.py`. Cada livro é `Book_<Genero>_S<n>_R<z>_NN` (pasta `Gameplay/Books`) e cada zona `Zone_<Genero>_S<n>_R<z>` (pasta `Gameplay/PlaceZones`).
- Nas estantes do térreo, as tintas (`PaintContainer`, até 192 por estante) e seus grupos foram apagados.

### Estante de teste: History (`BP_BookShelfs10`) — *histórico, refeita no layout acima*
- Parede oeste do mezanino, logo no topo da escada. Vai de X -730 a -687, Y de 279 a 429, Z de 314 a 644, com a frente virada para +X.
- O fundo das 7 prateleiras fica em Z **350, 390, 425, 460, 495, 530 e 565**. Os livros vão de Y 281 a 423, a frente fica em x = -693,4 e a rotação é yaw 90.
- **Só tem livros unitários (`BP_Book`):**
  - **Z 460 e 495:** são os 25 livros originais (`Book_History_01..25`). Faltam 13, que foram removidos, e isso deixa espaços.
  - **Z 350, 390, 425, 530 e 565:** são 113 livros gerados por script (`Book_History_R<z>_NN`), com malhas `SM_Book_01..29` sorteadas e encostados da esquerda. Cada prateleira tem cerca de 20% livre no fim (y de ~397 a 423).
  - As fileiras fundidas (`BookStack_106/107/110/111/112`) foram **apagadas**.
- Para o jogador ficar de frente para ela: posição (-600, 338, 430), yaw 180, pitch -10.

### Áreas de colocação: `BP_PlaceZone` (pasta `Gameplay/PlaceZones`)
- **Componentes:**
  - `Area` (BoxComponent, raiz): perfil **`PlaceZone`**, que é só Query, tem ObjectType `PlaceZone` = `ECC_GameTraceChannel1` = **`ObjectTypeQuery7`** e ignora todos os canais.
  - `Highlight` (cubo com `MI_PlaceHighlight_Zone`): sem colisão e invisível por padrão.
- **Variáveis:**
  - `ZoneType`: 0 = estante, 1 = balcão.
  - **`Extent`:** meio-tamanho da caixa, **editável por instância**. O construction script aplica esse valor no BoxExtent e na escala do Highlight. Não mude o BoxExtent direto no componente, porque ele volta ao padrão.
  - `SlotOffsets`: [0, ±1.5, ±3, ±4.5, ±6].
- **`GetPlacement(HitLocation, Book) → (Placement, Valid)`:**
  - **Estante:** em espaço local, X é a fileira, Y negativo é a frente e Z negativo é o fundo. O livro é colocado em pé, com a rotação da zona, e o pivô vai na linha frente-baixo. A busca usa `BoxOverlapActorsWithOrientation` (BP_Book, PhysicsBody) nos SlotOffsets.
  - **Balcão (um livro):** o livro vai deitado com a **capa para cima**: pitch **-90** combinado com a rotação da zona, com o topo do livro apontando para +X da zona, ou seja, para longe do atendente. O centro fica limitado à área, com margem de max(meia profundidade, meia altura) + 1. Um `LineTraceByChannel` (Visibility) de cima para baixo acha o tampo **ou o livro de cima**, e o livro empilha ali. Fica **sem física**.
- **`GetCounterStack(HitLocation, Books[]) → (Placements[], StackCenter, StackHalfSize, Valid)`:** calcula a pilha inteira para o balcão. Usa o mesmo raio vertical para achar a superfície e empilha `Books[0]` embaixo, somando `2*HalfSize.x` de cada livro (variável local `Acc`). Devolve também a caixa da pilha, para o fantasma.
- **Orientação do livro:** a **capa é a face -X local**, a lombada é -Y (o pivô fica na frente-baixo, do lado da lombada) e o topo é +Z.
- `SetHighlight(On)`.
- **`GetBooksInZone() → Books (Array Actor)`:** `BoxOverlapActorsWithOrientation` no centro da zona, com caixa `Extent + (2, 2, 30)` (para pegar pilhas), `[PhysicsBody]` e classe BP_Book. Livros na mão ou em movimento estão sem colisão, então só entram os que estão parados na zona. Quem usa é o `BP_Customer` para ler o balcão.
- **Zonas na cena:**
  - `Zone_History_R350 … R565`: 7 zonas, centro (-702,36, 352, z+15), yaw 90, Extent (72, 9, 15).
  - `Zone_Counter`: centro (-505, 176.5, 140.4), yaw 0, Extent (31, 58.5, 6). Cobre o tampo inteiro do `CheckoutBlock_2` em X. Se a zona for estreita, a mira de quem está atrás do balcão passa por baixo dela. A `BookStack_121` foi apagada.
- `BP_PlaceGhost`: cubo com `MI_PlaceHighlight_Ghost` e sem colisão. O personagem cria um no BeginPlay e o posiciona e escala no lugar exato onde o livro vai ficar.
- **Materiais** (`/Game/Library/Materials/`): `M_PlaceHighlight` (Unlit Translucent, parâmetros `Color` e `Opacity`) e duas instâncias, `MI_PlaceHighlight_Zone` (0,12) e `MI_PlaceHighlight_Ghost` (0,45).

### `BP_Book` (`/Game/Library/Blueprints/BP_Book`)
- O componente raiz é `Mesh` (StaticMeshComponent, Movable, `bCanEverAffectNavigation = false`). Para trocar a malha, mude `StaticMesh` no componente da instância.
- **Colisão:** perfil `PhysicsActor`, ou seja, ObjectType **PhysicsBody**. Os livros novos herdam isso do template, mas os antigos guardam a própria cópia e precisaram receber a mudança um por um.
- **BeginPlay:**
  - `SetCollisionResponseToChannel(Pawn, Ignore)`: o livro ignora o jogador. Sem isso, ao soltar, o livro nasce dentro da cápsula, é ejetado e atravessa o piso.
  - `SetUseCCD(true)`.
- **Tick (desempenho, 2026-10-27):** com ~1.700 livros, o tick de Blueprint de cada um pesava à toa. O CDO agora tem `bStartWithTickEnabled = false`. `PickUp` e `PlaceAt` ligam o tick (`SetActorTickEnabled true`), e o ramo "nem State 1 nem 2" do `EventTick` chama `SleepIfIdle`, que desliga o tick no State 0. Os livros já colocados no mapa guardam `bStartWithTickEnabled = true` na instância: fazem 1 tick e dormem. **Se criar outra função que ponha um livro em State 1 ou 2, ligue o tick nela.**
- **State:**
  - 0: parado (estante ou balcão), sem física e com colisão.
  - 1: na mão.
  - 2: indo para o lugar.
  - 3: com física (solto).
- **Funções:**
  - `PickUp(Index, StackZ)`: desliga a física e a colisão, guarda o `HeldIndex` e o `HoldStackZ` (a altura da base deste livro na pilha da mão) e passa para State 1.
  - `Drop()`: liga a colisão e a física, zera as velocidades e passa para State 3.
  - `PlaceAt(Target, PhysicsOnArrive)`: guarda o `TargetTransform` e passa para State 2. Hoje sempre recebe `false`.
  - `GetBookExtents() → (Center, HalfSize)`: vem do bounding box da malha, no espaço local do livro.
- **Catálogo (título e autor):** os mapas `BookTitles` e `BookAuthors` (Map string→string) ficam nos **defaults do CDO** do BP_Book. A chave é o **nome da malha** (`SM_Book_07`).
  - `GetBookInfo() → (Title, Author, Known)` lê `GetObjectName(Mesh.StaticMesh)` nos mapas.
  - Os títulos foram transcritos das lombadas na estante. Os autores vêm da lombada quando dá para ler; os outros são inventados.
  - `SM_Book_06` (lombada escura, sem título) fica **fora** do catálogo de propósito e nunca é pedida.
  - Plano B: não dá para criar struct/DataTable pelo MCP (não há tool para UserDefinedStruct). As variáveis antigas `BookTitle`/`Genre` existem, mas não são usadas.

  | Malha | Título | Autor |
  |---|---|---|
  | 01 | A Universal Guide to Creating Book Covers | Bernhard R. Painter |
  | 02, 07 | Diary of Ms. Rose | Eleanor Whitby* |
  | 03 | L'homme qui vivait au loin | Beaujolie |
  | 04 | Summer's End | Arthur Heinlein |
  | 05 | Classic Poems, Volume I | J. A. Stover |
  | 08 | Open Office Design | Johnny Matthews |
  | 09 | Lost Souls | Gregg Tielms |
  | 10 | Colorblind | Kevin Reich |
  | 11 | Cities | Hanna Lindqvist* |
  | 12 | Chrysanthemums | Xiaobing Zhao |
  | 13 | Theoretical Calculus | Dr. Albert Faraday |
  | 14 | Data Structures and Programming | John M. Matthews |
  | 15 | First Contact | Patric J. Picard |
  | 17 | Analytic Geometry | Dr. C. Marie Mathews |
  | 20 | The Illusion of Democracy | Thomas Varga* |
  | 21 | Treasures of Al-Saban | Samira Haddad* |
  | 22 | Space Walk | Alex Leonov |
  | 26 | The Lake Murders | Ingrid Holm* |
  | 29 | Cats and Their Humans | Freya Malcolm |

  \* autor inventado. Para adicionar uma malha nova, acrescente a chave nos dois mapas do CDO.
- **Pose na mão:** é uma **pilha deitada, com a capa para cima e sempre horizontal no mundo**.
  - A base fica em `câmera + fwd*HoldForward(40) + right*HoldRight(14) + up*HoldUp(-22)`.
  - A rotação é `CombineRotators((pitch -90, yaw HoldYaw 10 + HeldIndex*HoldStackYaw 6), (0, yawDaCâmera, 0))`.
  - O centro do livro fica em `base + Z*(HoldStackZ + meia espessura)`, e o pivô é `centro - RotateVector(Center, rot)`.

### Input (Enhanced Input, `/Game/Library/Input/`)
- `IMC_Library` é adicionado no BeginPlay do personagem com prioridade 1, por cima do `IMC_Default` do template (Move/Look/Jump, que não alteramos).

  | Action | Teclado/mouse | Controle | Evento → função |
  |---|---|---|---|
  | `IA_Interact` | E | Gamepad_FaceButton_Left (X/□) | Started → `Interact` |
  | `IA_Crouch` | C | Gamepad_FaceButton_Right (B/○) | Started → `ToggleCrouch` |
  | `IA_Zoom` | RightMouseButton | Gamepad_LeftTrigger | Started → `SetZoom(true)`, Completed → `SetZoom(false)` |

- O antigo nó de tecla E crua foi **removido**.

### Agachar e zoom
- **Agachar (alternar):** `ToggleCrouch` chama Crouch ou UnCrouch.
  - No CharMoveComp: `NavAgentProps.bCanCrouch = true`, `MaxWalkSpeedCrouched = 110` e `CrouchedHalfHeight = 45`.
  - ⚠️ O Crouch nativo **não** baixa a câmera, porque o Unreal reposiciona a malha para manter os pés no chão e a câmera está presa na `FirstPersonMesh`. Por isso, o `UpdateCameraEffects` baixa a **`FirstPersonMesh` inteira** (`SetRelativeLocation(0, 0, CrouchCamOffset)`). O `CrouchCamOffset` vai suavemente até `-CrouchCamDrop` (50) quando agachado, com FInterpTo e velocidade 8.
  - Mexer no RelativeLocation da câmera não funciona, porque ela está num socket da cabeça e o offset é ignorado.
  - ⚠️ **Problema conhecido:** como a malha inteira desce, **os pés do corpo atravessam o chão** quando o jogador agacha e olha para baixo. Não existe animação de agachar no projeto (só `IA_Crouch` tem "Crouch" no nome). **Decisão do usuário:** manter o corpo visível e, numa próxima etapa, importar uma animação de agachar (Fab/Mixamo) e ligá-la ao Animation Blueprint da `FirstPersonMesh`. Com a animação, a malha **não** precisa mais descer: a câmera, presa na cabeça, desce junto com a pose. Nesse momento, remova o `SetRelativeLocation` da FirstPersonMesh no `UpdateCameraEffects`.
- **Zoom (segurar):** com `bIsZooming`, o `CurrentFOV` vai suavemente de `DefaultFOV` 90 para `ZoomFOV` 50 (`ZoomSpeed` 10), e o `UpdateCameraEffects` aplica isso com `Camera.SetFieldOfView`.
- **Tick do personagem:** Sequence → `UpdatePlacementPreview` e `UpdateCameraEffects(Delta)`.

### Interação no `BP_LibraryCharacter`
- **Variáveis:** `HeldBooks` (array de BP_Book), `MaxHeld` 3, `InteractDistance` 250, `Ghost`, `CurrentZone`, `PrevZone`, `CurrentPlacement`, `bPlacementValid`, `RequestWidget` e `SystemWidget`.
- `TraceBook()`: SphereTraceForObjects com raio 5 e `[ObjectTypeQuery4]`, depois cast para BP_Book.
- `TraceZone()`: SphereTraceForObjects com raio 2 e `[ObjectTypeQuery7]`, depois cast para BP_PlaceZone. Devolve Zone, HitLoc e Found.
- **`UpdatePlacementPreview()`, a cada Tick:**
  - Se carrega livros, não está mirando num livro e há uma zona na mira: chama `GetPlacement` para o livro de cima, acende a zona e posiciona o fantasma.
  - Caso contrário, esconde o fantasma e apaga a zona.
- **No preview, quando a zona é o balcão (ZoneType 1):** chama `GetCounterStack(HitLoc, HeldBooks)`, guarda `CurrentStack` e o fantasma vira a caixa da **pilha inteira**. Na estante, o fantasma continua sendo só o livro de cima.
- **Tecla E → `OnInteractPressed()`** (é o que o `IA_Interact` Started chama):
  - **Prioridade:** se `TraceBook` acha um livro **ou** `bPlacementValid` está ligado (mirando numa área válida com livros na mão), o E vai direto para o `Interact()` dos livros.
  - Só depois disso ele procura cliente. O motivo: com o NPC colado no balcão, o raio de 2,5 m passava pelo tampo e acertava o NPC atrás dele, então o livro nunca era colocado.
  - Para falar com o cliente, mire no **rosto** dele (acima do tampo).
  - `TraceCustomer()`: SphereTraceForObjects com raio 10, `[ObjectTypeQuery5 = Vehicle]` (o tipo da cápsula dos clientes) e `InteractDistance`, depois cast para BP_Customer. O próprio jogador é ignorado (IgnoreSelf).
  - Se achou um cliente: `HandleCustomer(c)` chama `c.Interact()`, e o resultado decide o que fazer: 1 → `ShowRequest(Msg)`, 3 → `HideRequest()`, 0 → nada. O caso 2 → `SetRequestStatus(Msg)` continua no código, mas o cliente não usa mais (o `StatusText` do papel fica vazio).
  - Se não achou cliente: `TraceTerminal()` (SphereTraceForObjects com raio 5, `[ObjectTypeQuery2 = WorldDynamic]` e `InteractDistance`, depois cast para `BP_LibrarySystem`). Se achou, chama **`OpenSystem(sys)`**:
    - Cria um `WBP_LibrarySystem` novo, chama `Open(sys)`, `AddToViewport` (ZOrder 5), `SetInputModeUIOnly` e mostra o cursor.
    - Se o papel está aberto, ele é re-adicionado com ZOrder 10, por cima da tela.
    - O estado não se perde ao recriar o widget, porque fica no rascunho do sistema.
  - Se não achou nada: chama o `Interact()` dos livros, descrito abaixo e sem mudanças.
- **Papelzinho `WBP_RequestList`** (`/Game/Library/UI/`):
  - Estrutura: CanvasPanel → Border bege (`Paper`), ancorado à esquerda (x 40, 40% da altura) → VerticalBox com `Header` "Pedido:", `ListText` e `StatusText` (vermelho).
  - Funções `SetList(NewText)` e `SetStatus(NewText)`.
  - O personagem guarda o widget em `RequestWidget`. `ShowRequest` cria o widget na primeira vez (Sequence + IsValid), chama SetList e limpa o status. `HideRequest` faz RemoveFromParent e zera a variável.
- **`Interact()` (livros):**
  - Mirando num livro e com menos de 3 na mão: **pega**. Soma a espessura dos livros já na mão (variável local `StackSum`), chama `PickUp(n, StackSum)` e adiciona o livro ao array.
  - Com livros na mão e preview válido no **balcão**: coloca **todos** (`PlaceAt(HeldBooks[i], CurrentStack[i])`) e depois faz `Clear`. O loop fica no then_0 de um Sequence e o Clear no then_1.
  - Com livros na mão e preview válido na **estante**: coloca o de cima.
  - Com livros na mão e fora de uma zona: **solta** o de cima (`Drop`). Nos dois últimos casos, remove o último do array.
  - Mirando num livro com 3 na mão: não faz nada.
- **Por que não usar Visibility:** a colisão simples de `BP_BookShelf_01` cobre a frente dos livros, então um raio de Visibility acerta a estante. O raio por objetos ignora estantes e paredes. Por isso ele também atravessa paredes, mas o alcance é de só 2,5 m.
- **Por que esfera:** um livro tem cerca de 4 cm de largura, e um raio fino passa pelos espaços entre eles.
- **Mira:** `/Game/Library/UI/WBP_Crosshair`, um ponto branco de 6 px com 75% de opacidade, centralizado. O BeginPlay do personagem faz CreateWidget e AddToViewport. O BP_FirstPersonCharacter não tem BeginPlay próprio; o mapping de input fica no PlayerController, então é seguro sobrescrever.

## Pastas do Outliner
`Blockout` (pisos e paredes), `Props`, `Pipes`, `HangingLights`, `Lights`, `Cinematic/Cameras`
(as CineCameras originais), `Cinematic` (Sequence_01) e `Gameplay`.
Muitos props estão soltos, fora de pastas, e agrupados em GroupActors.

## Outros mapas do pacote (só referência)
- `/Game/Stationer/Levels/L_Stationer`: a original. Não editar.
- `L_Stationer_Overview` e `L_Lighting`: mapas de demonstração do pacote.
