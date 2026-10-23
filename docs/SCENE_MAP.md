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
| `NPC_Spawn` (`Gameplay/NPCPoints`) | (960, 290, 20) | NPC entra pela porta |
| `NPC_Counter` | (-420, 170, 20), yaw 180 | NPC para de frente pro balcão |
| `NPC_Exit` | (960, 380, 20) | NPC sai pela porta |

### NavMesh sem ilhas em cima dos móveis (pasta `Gameplay/NavModifiers`)
O Recast gera NavMesh em qualquer superfície plana, inclusive mesas, balcões e estantes. Para evitar isso, há 8 `NavModifierVolume` com `AreaClass = NavArea_Null` (`NavBlock_{Ground,Upper}_{A..D}`):
- No térreo eles cobrem Z de 40 a 300, e no mezanino Z de 360 a 850. A navegação só existe rente aos pisos (Z≈10 e Z≈330).
- O retângulo da escada (X de -480 a -134, Y de 262 a 473) fica **de fora** dos volumes. Por isso os volumes são 4 caixas por andar em volta dele.
- Se aparecer outra área elevada que precise ser andável (rampa, palco), abra um buraco nos volumes ali.

## Manequins de estand-in (pasta `Characters/`)
SkeletalMeshActors em pose idle (`MM_Idle`). Lembre que a frente da malha é +Y, então o yaw do ator é a direção do olhar + 90.
| Ator | Malha | Posição | Olha para |
|---|---|---|---|
| `Customer_Counter` | SKM_Quinn_Simple | (-420, 170, 10), yaw 90 | o atendente (-X) |
| `Customer_Cafe` | SKM_Manny_Simple | (620, -70, 330), yaw 0 | a mesa grande (+Y) |
| `Customer_Browsing` | SKM_Manny_Simple | (300, 250, 10), yaw -90 | a porta (+X) |

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

### Estante de teste: History (`BP_BookShelfs10`)
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
- **Variáveis:** `HeldBooks` (array de BP_Book), `MaxHeld` 3, `InteractDistance` 250, `Ghost`, `CurrentZone`, `PrevZone`, `CurrentPlacement` e `bPlacementValid`.
- `TraceBook()`: SphereTraceForObjects com raio 5 e `[ObjectTypeQuery4]`, depois cast para BP_Book.
- `TraceZone()`: SphereTraceForObjects com raio 2 e `[ObjectTypeQuery7]`, depois cast para BP_PlaceZone. Devolve Zone, HitLoc e Found.
- **`UpdatePlacementPreview()`, a cada Tick:**
  - Se carrega livros, não está mirando num livro e há uma zona na mira: chama `GetPlacement` para o livro de cima, acende a zona e posiciona o fantasma.
  - Caso contrário, esconde o fantasma e apaga a zona.
- **No preview, quando a zona é o balcão (ZoneType 1):** chama `GetCounterStack(HitLoc, HeldBooks)`, guarda `CurrentStack` e o fantasma vira a caixa da **pilha inteira**. Na estante, o fantasma continua sendo só o livro de cima.
- **Tecla E → `Interact()`:**
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
