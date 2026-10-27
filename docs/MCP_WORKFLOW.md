# Unreal MCP — o que funciona neste projeto

Servidor `unreal-mcp` em `http://127.0.0.1:8000/mcp` (configurado em `.mcp.json`). O editor precisa estar aberto.

## Fluxo básico
1. `list_toolsets` e `describe_toolset` para ver os parâmetros de cada tool.
2. `call_tool` com `toolset_name` + `tool_name` + `arguments`.
3. Para muitas operações, use **`editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script`**. Ele roda um script Python que define `run()` e devolve um dict. Dentro do script, chame `execute_tool('<toolset completo>.<tool>', json.dumps(args))['returnValue']`. Só dá para importar `json`, `re`, `math`, `copy`, `time` e `datetime`.

## Tools mais usadas
- `SceneTools`: `find_actors`, `add_to_scene_from_class`, `add_to_scene_from_asset`, `set_actor_folder`, `rename_folder`, `get_folders`, `load_level`, `get_current_level`, `trace_world`.
- `ActorTools`: `get_label` e `set_label`, `get_actor_transform` e `set_actor_transform`, `get_actor_bounds`, `get_components`, `add_component`.
- `AssetTools`: `duplicate`, `create_folder`, `exists`, `save_assets`, `is_dirty`, `find_assets`.
- `ObjectTools`: `list_properties`, `get_properties`, `set_properties`. Use para editar propriedades de atores e componentes.
- `BlueprintTools`: criar e editar Blueprints.
- `EditorToolset.EditorAppToolset`: PIE, câmera do viewport, seleção. `EditorToolset.LogsToolset`: ler o Output Log.

## Pegadinhas já descobertas
- `find_actors` **exige** `name`, `tag` e `collision_channels`, mesmo vazios: `{'name':'','tag':'','collision_channels':[]}`. O filtro opcional `bounds` precisa de `isValid: true`.
- Caminho de classe errado em `actor_type` derruba o **script inteiro**, e o `try/except` dentro do script **não segura** o erro. Caminhos válidos:
  - `/Script/Engine.PlayerStart`, `/Script/Engine.TargetPoint`, `/Script/Engine.PostProcessVolume`
  - `/Script/CinematicCamera.CineCameraActor`
  - `/Script/LevelSequence.LevelSequenceActor` (**não** `/Script/Engine.`)
  - `/Script/NavigationSystem.NavMeshBoundsVolume`
- ⚠️ **`ActorTools.set_actor_transform` com só `rotation` ZERA a posição**, porque manda o ator para (0,0,0). A descrição diz que os campos omitidos "não mudam", mas isso não é verdade. **Sempre passe `location`, `rotation` e `scale` juntos.**
- Os manequins (`SKM_Manny_Simple` e `SKM_Quinn_Simple`) num SkeletalMeshActor ficam com a frente para **+Y**. Para o NPC olhar na direção do yaw θ desejado, use `yaw = θ + 90`. Exemplo: para olhar para -X, use yaw 90.
- Animação de pose parada num SkeletalMeshActor: `ObjectTools.set_properties` no SkeletalMeshComponent com `{"AnimationMode":"AnimationSingleNode","AnimationData":{"AnimToPlay":"/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle.MM_Idle","bSavedLooping":true,"bSavedPlaying":true}}`.
- Criar um Blueprint filho: `BlueprintTools.create` com `asset_type` igual à classe gerada do pai (`/Game/.../BP_X.BP_X_C`). Para mudar defaults: `get_default_object` + `ObjectTools.set_properties`.
- Para mexer em componentes herdados (como o CharacterMovement) no CDO de um Blueprint, use `{'refPath': cdo['refPath'] + ':CharMoveComp'}` com `ObjectTools.get_properties` e `set_properties`, e depois `compile_blueprint`. O `ActorTools.get_components` aceita o CDO, mas **não** o asset Blueprint.
- Não edite os Blueprints do template (`/Game/FirstPerson`). Crie filhos em `/Game/Library/Blueprints` e mude ali.
### Escrevendo lógica de Blueprint (`BlueprintTools.write_graph_dsl`)
- Leia `get_graph_dsl_docs` uma vez. Descubra os type_ids com `find_node_types` e os nomes de pinos com `get_node_type_pins`. O `get_node_type_pins` **cria um nó de verdade no grafo**: apague-o depois com `delete_node`.
- `(event X)` só funciona para eventos nativos (`EventBeginPlay`, `EventTick (DeltaSeconds)`). **Custom events e eventos de tecla (`Input|KeyboardEvents|E`) dão erro.** Para contornar:
  - Lógica chamável: use `(fn Nome () ...)` dentro de um grafo criado com `add_function_graph`. Ela é chamada de outro BP com `Class|BPBook|PickUp :self ref`; o nome da classe aparece sem underscore.
  - Tecla: `create_node` com `Input|KeyboardEvents|E`, outro `create_node` com `CallFunction|Interact`, e `connect_pins` de `Pressed` para `execute`.
- Saída com vários pinos: `(bind (a b) (Node ...))` segue a ordem dos pinos de saída. Para pegar o 10º (`HitActor` de `BreakHitResult`), escreva `(bind (b1 b2 ... b9 hitActor) ...)`.
- `Set` de variável sem argumento (`(Variables|Default|SetHeldBook)`) grava None.
- `read_graph_dsl` mostra nós puros "inline" e repetidos. É só exibição: confira as ligações reais com `find_nodes` + `get_node_infos`.
- ⚠️ **Valores default no CDO podem voltar ao padrão** depois de mudanças estruturais (nova função, variável ou nó) e recompilação. Sempre ajuste os defaults **por último**: compile, `set_properties` no CDO, `save_assets`, e confira com `get_properties`.
- Variáveis que você quer mudar por instância no nível precisam de `set_variable_instance_editable`. Sem isso, o `set_properties` no ator falha.
- Componente raiz de um BP: `add_component` cria o componente embaixo do DefaultSceneRoot. Para ele virar a raiz, chame `set_parent_component(component=DefaultSceneRoot, parent=NovoComp)`.

- Para trocar um nó por outro mantendo as ligações: `create_node` do novo, depois `break_pins` e `connect_pins` de cada ligação do antigo, pelo nome do pino, e por fim `delete_node` do antigo.
- **Pino de array** (ex.: `ObjectTypes`) não aceita `set_pin_value`. Crie `Utilities|Array|MakeArray`, ligue `Array` no pino e use `set_pin_value` no item `[0]`.
- Mudar a **categoria** de uma variável muda o type_id dos nós dela: `Variables|Default|GetX` vira `Variables|<Categoria>|GetX`.
- Colisão via `set_properties`: `{"BodyInstance":{"collisionProfileName":"PhysicsActor","objectType":"ECC_PhysicsBody"}}`. Só o nome do perfil **não** muda o objectType, então passe os dois.
- Widget: `UMGToolSet.CreateWidgetBlueprint`, `AddWidget` (CanvasPanel como raiz, depois os filhos) e `ObjectTools.set_properties` no slot (`LayoutData` com anchors, alignment e offsets) e no widget (`Brush`, `ColorAndOpacity`). Termine com `CompileWidgetBlueprint`.

- ⚠️ **Nós puros são reavaliados a cada uso.** `Get` de array, `Length` e getters de variável são lidos de novo no momento em que o nó impuro que os consome executa. Por isso:
  - Use o valor **antes** de mudar o array: primeiro `PlaceAt` / `Drop`, depois `RemoveIndex`.
  - Para guardar um valor "antigo" (ex.: a zona do frame anterior), copie-o para uma variável com um `Set` **antes** de sobrescrever a original.
- ⚠️ **`if` e nós multi-exec (IsValid, Cast) encerram o fluxo:** nada depois deles no mesmo bloco roda. Para fazer duas coisas em sequência, use `(Utilities|FlowControl|Sequence (:then_0 ...) (:then_1 ...))`.
- ⚠️ **Apagar os nós `ReturnNode` de uma função apaga os parâmetros de saída dela.** Ao limpar uma função para reescrever, recrie as saídas com `add_function_param(input_param=False)` antes de rodar o DSL.
- Nós de **outra classe** (`Class|BPPlaceZone|...`) só aparecem no `find_node_types` depois que o BP tem uma variável daquele tipo.
- Variável bool `bAlgo`: o nó vira `Variables|Default|GetAlgo` (sem o "b"). Às vezes o nome também muda de caixa (`bPhysicsOnArrive` → `SetPhysicsonArrive`). Confira com `find_node_types`.
- `(bind x 15.0)` com um literal **falha** ("produced no output pin"). Use o literal direto na expressão.
- Variável **local** de função: `add_variable(..., graph=<função>)`. O nó continua sendo `Variables|Default|GetX` / `SetX`, e o valor volta ao padrão a cada chamada. Isso é útil para acumular valores num `for`.
- `(for i (range n) ...)` vira um ForLoop de 0 até `n-1`.
- Funções são impuras por padrão. `(bind (a b) (Class|X|Func :self obj))` funciona como statement.
- Uma exceção dentro de `execute_tool` **não** é capturada por try/except: o script inteiro para. Um `write_graph_dsl` que deixa o BP sem compilar (ex.: falta o MakeArray) ainda **grava o grafo**. Ligue o MakeArray num **segundo** script e compile.
- **Não use espera ocupada** (`while time.time()...`) no execute_tool_script: o script roda na game thread e congela o PIE.
- Retorno do `run()`: as chaves do dict precisam ser strings.
- **Canal de colisão novo:** precisa de `+DefaultChannelResponses=(Channel=ECC_GameTraceChannel1,...)` e, de preferência, um `+Profiles=(...)` no `DefaultEngine.ini`, seguidos de **reinício do editor**. Antes do reinício, o perfil não existe e o componente fica como "Custom" com respostas padrão. Depois, aplique de novo o `collisionProfileName`.
- `set_properties` de propriedades de **componente de instância** (ex.: BoxExtent) pode voltar ao padrão do template quando o construction script roda. Para valores por instância, use uma **variável do ator** (instance editable) e aplique no construction script.
- Física: um ator Movable com SimulatePhysics que nasce dentro de outro corpo é ejetado com uma velocidade absurda e atravessa o piso. Ignore o Pawn e zere as velocidades ao ligar a física.

### Aprendizados da Etapa 2a (cliente)
- **Assinaturas das tools que confundem:**
  - `ObjectTools.set_properties` recebe `{"instance": ref, "values": "<JSON em string>"}`, e não um dict `properties`.
  - `get_properties` recebe `{"instance": ref, "properties": [...]}`.
  - `find_assets` exige `folder_path` e `name`.
- **Não existe tool para criar UserDefinedStruct.** Sem struct, não dá para fazer um DataTable próprio. Alternativa usada: `add_variable(type_name='string', container_type='MAP')` (a chave do MAP é sempre string) e preencher no CDO com `set_properties` mandando um objeto JSON.
- **Valores de Map/Array no CDO propagam** para as instâncias já colocadas no nível que não sobrescreveram o valor.
- **`write_graph_dsl` que falha no meio deixa nós órfãos no grafo.** Uma segunda escrita **soma** nós, e não substitui. Depois de qualquer falha:
  - Varra os grafos procurando nós impuros com o exec de entrada desligado.
  - Ou apague tudo menos a entrada da função (`find_nodes` + `delete_node`) e escreva de novo.
- **Parâmetros novos de função só aparecem nos nós `CallFunction|X` depois de `compile_blueprint`.** Escreva e compile primeiro as funções chamadas, e só então as que chamam.
- O `switch int` do DSL só tem os pinos 0–2. Para mais casos, use `if`/`elif`.
- `Math|Vector|vector+vector` **não** existe como type_id na escrita (ele só aparece no read-back). Use `(+ a b)` e `(* v s)`.
- O read-back mostra chamadas de outra classe como `CallFunction|Interact`, o que é ambíguo. Confira o pino `self` com `get_node_infos`.
- Separador de string com quebra de linha: escreva um marcador no DSL e depois faça `set_pin_value(pin, "\n")` no pino `Separator` do `JoinStringArray`.
- `Utilities|FlowControl|Delay x` funciona como statement em sequência, dentro de eventos.
- `Actor|GetAllActorsOfClass "<classe>_C"` devolve o array já tipado (dá para chamar funções do BP direto em cada elemento).
- **Character + IA:**
  - `AutoPossessAI = PlacedInWorldOrSpawned` e `AIController` (é o padrão do Character).
  - `AI|Navigation|SimpleMovetoLocation :Controller (Pawn|GetController) :Goal loc`.
  - Para girar com `SetActorRotation`, desligue `bUseControllerRotationYaw` no CDO.
  - Subobjetos no CDO: `:CharacterMesh0` (`SkeletalMeshAsset`, `AnimClass`, `RelativeLocation/Rotation`) e `:CharMoveComp`.
- **Dobrar um osso no ABP por código:** `BlueprintTools.create_node` com `Animation|SkeletalControls|Transform(Modify)Bone` (precisa de `Animation|ConvertSpaces|LocalToComponent` antes e `ComponentToLocal` depois) e `connect_pins` (pino 0 = pose, 1 = Alpha, 3 = Rotation). A rotação **não** vem do `set_properties` (o pino exposto manda): use `set_pin_value` com a string `"pitch,yaw,roll"`. Alvo da animação: `ObjectTools.set_properties` em `{"node":{"boneToModify":{"boneName":"lowerarm_r"},"rotationMode":"BMM_Additive","rotationSpace":"BCS_ParentBoneSpace"}}`. No `lowerarm_r` do Manny, o yaw (2º valor) é a dobra do cotovelo (80 = antebraço horizontal para a frente) e o pitch (1º) abre/fecha o antebraço para os lados.
- **Medir a pose em números:** uma função do ABP que lê `GetSocketLocation(hand_r)` e converte com `InverseTransformLocation(GetActorTransform)` numa variável vetor, lida no Simulate com `get_properties` em `<ator>.CharacterMesh0.ABP_Customer_C_0`. Depois de compilar o ABP durante a simulação, o AnimInstance muda e o valor para de atualizar: pare e inicie o Simulate de novo antes de ler.
- **Objeto "na mão" do jogador sempre atrás da mão (UE 5.8):** a `FirstPersonMesh` do template usa `FirstPersonPrimitiveType = FirstPerson` e é desenhada na frente do mundo. Qualquer objeto segurado precisa do mesmo tipo (`Rendering|SetFirstPersonPrimitiveType`, valor `FirstPerson`) enquanto está na mão, e voltar a `None` ao soltar. Antes de mexer em offsets, meça as posições reais (sockets + bounds do objeto); aqui o livro já estava sobre a palma e o problema era só a renderização.
- **Testar o jogador com objetos na mão:** `BP_TestDriver` no BeginPlay (Delay → `PickUp` + `Array|Add` em `HeldBooks` → Delay → `Pawn|SetControlRotation` com o pitch desejado) e `CaptureEditorImage` durante o PIE; espere ~2 s depois do warmup (a primeira captura sai borrada de motion blur).
- **Ajustar pose/livros ao vivo no Simulate:** (1) o ABP só avalia a pose do NPC quando ele é **renderizado**; chame `CaptureViewport` (dentro de um `execute_tool_script`, que devolve só a imagem) antes de ler medidas; (2) variáveis do ABP `instance editable` podem ser mudadas com `set_properties` em `<ator>.CharacterMesh0.ABP_Customer_C_0`; (3) para prender um livro de teste: `ActorTools.get_root_component` + `set_parent_component(root, mesh)` e `set_actor_transform(..., worldspace=False)` dá o transform relativo ao Mesh (espaço do mesh: +Y frente, -X direita); (4) imagens do `CaptureViewport` dentro de script saem em base64 num arquivo grande: decodifique com Python (maior string base64 do arquivo).
- Compilar o `BP_Customer` com um Simulate recente pode devolver o erro "REINST_BP_Customer_C ... not valid" como exceção, abortando o script; é só um aviso. Rode os passos seguintes (salvar, etc.) em outra chamada.
- **Caminhada picotada com `bUseAccelerationForPaths`:** a aceleração do path following chega zerada em quadros alternados, por causa da ordem de tick. O `ShouldMove` (que exige aceleração ≠ 0) pisca, e o state machine fica alternando Idle/Walk. A correção foi uma cópia do ABP (`/Game/Library/Characters/ABP_Customer`) com o pino B do AND do `ShouldMove` em `true` (o `NotEqual(Acceleration)` foi apagado) e o limiar de velocidade em 3. Não edite o `ABP_Unarmed` do template.
- **NPCs travando uns nos outros (porta, corredor):** um jeito simples é trocar o ObjectType da cápsula no BeginPlay (`Collision|SetCollisionObjectType :Channel "ECC_Vehicle"`) e mandar ignorar esse canal (`Collision|SetCollisionResponsetoChannel :Channel "ECC_Vehicle" :NewResponse "ECR_Ignore"`). Eles se atravessam, mas o jogador (Pawn) continua batendo neles. Mapeamento dos ObjectTypeQuery: 1 WorldStatic, 2 WorldDynamic, 3 Pawn, 4 PhysicsBody, 5 Vehicle, 6 Destructible, 7 PlaceZone (nosso).
- **Fotografar NPCs em jogo:** durante o PIE, o `CaptureViewport` renderiza o mundo do **editor** (sem os atores spawnados), e o `ControlRotation` do jogador não é editável. Use **Simulate** (`StartPIE` com `bSimulate: true, playMode: PlayMode_Simulate`): a IA, as animações e os drivers rodam, e `SetCameraTransform` + `CaptureViewport(captureTransform)` fotografam o mundo simulado de qualquer ângulo. Drivers que dependem do jogador (cast do PlayerCharacter) falham no Simulate.
- **Ajustar um objeto preso a um osso:** prenda com `SnapToTarget` (posição e rotação). Assim, a rotação do objeto no mundo é a do osso. Leia essa rotação, calcule a rotação relativa desejada com matriz (Python local: eixos do FRotator, `rel = Hᵀ·desejado`), aplique com `set_actor_transform(worldspace=false)` e confira com foto. Variáveis que não são instance-editable (ex.: `State`) não aceitam `set_properties` na instância.
- **Driver de teste reutilizável:** `/Game/Library/Debug/BP_TestDriver`. Reescreva o EventGraph dele (apague todos os nós antes), coloque na cena, rode o PIE e depois tire o ator da cena. **Não apague o asset.**
- Para pôr livros na mão do jogador por script: `Class|BPBook|PickUp :self b :Index i :StackZ (i*4.5)` + `Utilities|Array|Add (Class|BPLibraryCharacter|GetHeldBooks :self pc) b`.
- **NPC deslizando sem animar:** o `ABP_Unarmed` (e o ABP do Third Person) calcula `ShouldMove = GroundSpeed > 0 && CurrentAcceleration != 0`. Movimento por IA só gera aceleração com `CharMoveComp.NavMovementProperties.bUseAccelerationForPaths = true` (no UE 5.8 isso fica dentro desse struct, e não solto no componente).
  - ⚠️ Mudar um **struct** de componente no CDO **não propagou** para a instância já colocada no nível. Aplique também na instância (`<ator>.CharMoveComp`) e salve o mapa.
  - Para depurar no PIE, leia o AnimInstance: `<ator>.CharacterMesh0.ABP_Unarmed_C_0`, propriedades `GroundSpeed`/`ShouldMove`. (`AnimScriptInstance` não é legível pelo get_properties.)
- **Widget em PIE:** o widget criado fica em `/Engine/Transient.UnrealEdEngine_0:GameInstance_1.WBP_X_C_0`. Leia as variáveis dele (ex.: `ListText`) para pegar a referência do TextBlock e depois `get_properties(['Text'])`.
- **Roteiro de teste sem mexer no personagem:** crie um ator temporário `BP_TestDriver` com o roteiro no BeginPlay (Delay → cast do player → SetControlRotation → chamadas). Coloque na cena, rode o PIE e consulte o estado. No fim, **apague o ator e o asset**. É mais seguro do que reescrever o BeginPlay do personagem.
- ⚠️ **CRASH:** `AssetTools.delete` de um Blueprint que acabou de ser usado no PIE (logo depois de `StopPIE` e de remover o ator) derrubou o editor com EXCEPTION_ACCESS_VIOLATION no "Force Deleting". **Salve antes** e apague o asset temporário **numa chamada separada, bem depois do PIE**. Melhor ainda: deixe o asset de teste para o usuário apagar, ou reaproveite-o.
- **Reescrever um grafo sem duplicar:** antes do `write_graph_dsl`, apague todos os nós menos a entrada (`|NomeDaFuncao`) e o `|ReturnNode` (`find_nodes(title='')` + `delete_node`). No EventGraph, apague tudo, inclusive os eventos.
- `Utilities|Array|MakeArray` no DSL aceita **1 elemento só**. Para arrays maiores, use uma variável local e vários `Utilities|Array|Add`.
- O getter de variável **da própria classe** (`Variables|Default|GetX`) não tem pino de alvo, então não dá para ler a variável de **outra instância** da mesma classe. Crie uma função (ex.: `GetRequested()`), que tem `self`. Entre classes diferentes use `Class|BPX|GetY :self obj`, que funciona.
- Setters entre classes funcionam com `(Class|BPCustomer|SetSpawner :self c :Spawner self)`. O read-back mostra `Variables|Default|SetX`, mas o `self` do nó aponta para o alvo certo (confira com `get_node_infos`).
- `Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "F" :Time t :bLooping false` funciona para timers que se rearmam sozinhos (intervalos variáveis).
- `Game|SpawnActorfromClass :Class "<BP>_C" :SpawnTransform ... :CollisionHandlingOverride "AdjustIfPossibleButAlwaysSpawn"` devolve a referência já tipada. O BeginPlay do ator spawnado roda **antes** dos setters; o que depende de referências fica para uma chamada explícita depois (aqui, `StartPath`).
- `ActorTools.set_actor_transform` usa o parâmetro **`xform`**, e não `transform`.
- **NPC parando antes do alvo:** o `SimpleMoveToLocation` para por volta de 40 cm antes. Para encostar (ex.: no balcão), faça a aproximação fina: `AI|Navigation|StopMovement :self (Pawn|GetController)` + `Pawn|Input|AddMovementInput` a cada tick até ficar a menos de 6 cm, com timeout.
- `CaptureViewport` aceita `captureTransform` e fotografa de qualquer ponto **sem mover a câmera do editor**. Foi assim que lemos as lombadas dos livros.

### Aprendizados da Etapa 2c (sistema no computador, UI interativa)
- **Botões e campos de texto funcionam pelo MCP:**
  - `UMGToolSet.BindToEventProperty(widgetBlueprint, eventName "OnClicked", propertyName "BtnX", propertyClass "/Script/UMG.Button")` cria no EventGraph um nó `K2Node_ComponentBoundEvent` com type_id `AddEvent|OnClicked(BtnX)`.
  - Depois, `create_node("CallFunction|MinhaFuncao")` e `connect_pins` do pino `then` do evento para o `execute`. Para EditableTextBox, use `OnTextChanged` com `propertyClass "/Script/UMG.EditableTextBox"`.
  - O widget precisa ser variável (`ToggleWidgetAsVariable`) antes do bind.
- **Linhas dinâmicas:** use um widget de linha (`WBP_Row`) com uma variável `Owner` tipada como o widget pai e uma função `Setup(...)`. O `OnClicked` dele chama `Owner.OnRowClicked(...)`. A referência circular WBP_Row ↔ WBP_LibrarySystem compila sem problema. Crie o pai (com a função vazia) e compile **antes** de criar o filho.
- **Type_ids de UMG:**
  - `Variables|<NomeDoWBP>|GetX` para os widgets-variável (com underscore, ex.: `Variables|WBP_Row|GetLabel`).
  - `Widget|SetText(Text)` (TextBlock), `Widget|GetText(TextBox)` / `Widget|SetText(TextBox)` (EditableTextBox), `Widget|Panel|ClearChildren`, `Widget|Panel|AddChild :Content`, `Widget|SetVisibility :InVisibility "Collapsed"`, `Widget|SetIsEnabled :bInIsEnabled`, `Widget|RemovefromParent`.
  - `UserInterface|CreateWidget :Class "<WBP>_C" :OwningPlayer pc` devolve a referência já tipada.
  - `UserInterface|Viewport|AddtoViewport :ZOrder n`, `Input|SetInputModeUIOnly :PlayerController :InWidgetToFocus`, `Input|SetInputModeGameOnly` e `Class|PlayerController|SetShowMouseCursor :bShowMouseCursor`.
- **Propriedades de widget via `set_properties`:**
  - TextBlock: `Text` (string simples), `Font: {Size}`, `ColorAndOpacity: {SpecifiedColor: {R,G,B,A}}` e `WrapTextAt`.
  - Border: `BrushColor` e `Padding`. EditableTextBox: `HintText`. Qualquer widget: `Visibility: "Collapsed"`.
  - Slots de VerticalBox/HorizontalBox: `Size: {SizeRule: "Fill", Value}` e `Padding`.
  - CanvasPanelSlot em tela cheia: `LayoutData` com Anchors 0..1 e Offsets 0.
- **`==` entre strings não liga** ("Could not connect pin Out to A"). Use `Utilities|String|EqualExactly(String)`. Para "diferente", use `(not (EqualExactly a b))`. `select` funciona com strings.
- **Parâmetros de `fn` são usados pelo nome:** `(fn F (Doc Titles) ... Doc ...)`. Parâmetros declarados com `add_function_param`/`add_object_function_param` antes.
- **`compile_blueprint` sempre devolve `None`**, mesmo com erro. Confira com `LogsToolset.GetLogEntries(pattern "LogBlueprint: Error")`. Já o `CompileWidgetBlueprint` devolve `true`/`false`.
- **"Unclosed parenthesis"** em DSL longo: conte os parênteses localmente (Python, ignorando o que está entre aspas) antes de mandar. O erro de parse não cria nós.
- **Ler mapas do catálogo de outra classe:** existe `Class|GetClassDefaults`, mas é mais simples ler `Class|BPBook|GetBookTitles` de qualquer `BP_Book` da cena (as instâncias herdam o mapa do CDO) e usar `Utilities|Map|Keys` / `Utilities|Map|Find`.
- **Trocar um nó de um grafo grande sem reescrever:** foi assim que o `PlayBell` do `TrySpawn` virou `OnSpawned`. Leia os pinos com `get_node_infos`, crie o nó novo, refaça as ligações de `execute`, `self` e `then` e apague o antigo.
- **Roteiro de teste:** `SetControlRotation` seguido de um trace **no mesmo frame** ainda usa a câmera antiga. Ponha `Delay 0.5` entre a mira e o `OnInteractPressed`.
- **`CaptureEditorImage` com `{}`** fotografa a janela do editor **com o PIE e a UI** (widgets aparecem). O base64 vem salvo em `tool-results/`. Decodifique com Python.
- **Espera no Bash:** `sleep` solto é bloqueado. Use `run_in_background: true` (você é avisado quando termina) e, enquanto isso, consulte `GetLogEntries`.

### Aprendizados da Etapa 2d (subtelas, shell + telas filhas)
- **Slot de VerticalBox/HorizontalBox:** o tamanho "auto" é `Size: {SizeRule: "Automatic", Value: 1.0}`. `"Auto"` falha em silêncio ("could not be set: Size").
- **Cor de Button:** `WidgetStyle: {Normal/Hovered/Pressed/Disabled: {TintColor: {SpecifiedColor}}}`. A tinta é **linear** e a tela mostra sRGB, então valores como 0.07 aparecem bem mais claros (≈0.3). Para fundo escuro use ~0.01–0.04.
- **EditableTextBox:** só tem `WidgetStyle` (`BackgroundColor`, `ForegroundColor`, `FocusedForegroundColor`, `TextStyle: {Font: {Size}}`). `BackgroundColor` solto dá erro.
- **Widget filho em outro widget:** `AddWidget` aceita `widgetClass` = `/Game/.../WBP_X.WBP_X_C`, e `ToggleWidgetAsVariable` expõe `Variables|<Pai>|GetX`.
- **Setter `SetOwner` entre classes vira `Actor|SetOwner`** (AActor::SetOwner) e liga errado. Crie uma função `Bind(InOwner)` dentro de cada tela e chame `Class|WBPScreenX|Bind :self ... :InOwner self`. Evite variáveis com nome de função de AActor (Owner, Name, Tag…) se for escrever setter de outra classe.
- **Ordem de criação (tela filha ↔ pai):** crie função/variável stub, **compile os dois**, e só então escreva os corpos. Antes do compile o nó `Class|WBPScreenX|Refresh` vira `ControlActor|Refresh` no read-back e na prática liga errado.
- **O read-back mente nos nomes** (`Baseline|GetSystem`, `ControlActor|Refresh`, `Class|ComboBox(Object)|GetItems`): o que vale é o pino `self` em `get_node_infos` (tipo "WBP Library System Object Reference" etc.).
- **`write_graph_dsl` não substitui, soma.** Limpe antes: apague tudo menos os nós `K2Node_FunctionEntry`/`K2Node_FunctionResult` (pelo refPath). Use um helper `clear(graph)`. `write_graph_dsl` também compila: se **outra** função ainda aponta para widget removido, a escrita grava mas devolve erro. Limpe/neutralize essas funções antes.
- **`remove_function_graph(blueprint, graph_name)`** e `RemoveWidget` (apaga a subárvore) funcionam. Ao trocar uma tela inteira: limpe o EventGraph (`find_nodes title=''` + `delete_node`), apague as funções, remova a árvore e recrie.
- **Override de função de widget:** `add_function_graph` com o nome do evento nativo (`OnPreviewKeyDown`) cria o override com `MyGeometry`, `InKeyEvent` e retorno `EventReply`. Use `Widget|EventReply|Handled` / `Unhandled` no `return`.
- **Comparar tecla:** `==` entre `Key` e `MakeKey` não liga. Funciona comparar `Input|Key|GetKeyDisplayName` (convertido com `ToString(Text)`) com `"Escape"`, `"P"`, `"Gamepad Face Button Right"`. `==` com enum literal (`EUINavigationAction`) também não liga.
- **Teclado/controle exigem widget focável:** com `SetInputModeUIOnly(widget)`, o `bIsFocusable` do shell precisa estar `true` (CDO via `ObjectTools.set_properties`, depois compile e salve). Senão `OnPreviewKeyDown` nunca dispara.
- **Atenção com atalhos de letra:** `OnPreviewKeyDown` tunela antes do campo de texto. Use um guard (`Widget|HasAnyUserFocusedDescendants` nos EditableTextBox) para não roubar a digitação.
- **Tipos de variável em `add_variable`:** `bool` (não `boolean`), `int`, `string`. Array: `container_type: "ARRAY"`. Variável local de função: passe `graph`.
- **`Utilities|Operators|Less(<)` com string não liga.** Foi preciso escrever `StrLess` (loop de `GetCharacterAsNumber` sobre `ToLower`) e `SortOrder` (rank por contagem). Os ids no DSL podem ficar com minúsculas diferentes (`AddBooktoLoan`).
- **Nós de outra classe ficam desatualizados** no catálogo de um BP já aberto (o personagem e o `BP_TestDriver` ainda listavam funções antigas). Prefira que o widget novo busque o que precisa (ex.: o shell lê o texto do papel pelo `RequestWidget` do personagem) em vez de editar o personagem.
- **`GetLogEntries`:** passe `category: ""` (o padrão é "LogsToolset", que não existe).
- **Teste de tela:** driver com `ShowRequest` + `OpenSystem` do personagem (caminho real), delays de 8 s e `CaptureEditorImage` a cada etapa. `PressKey` do SlateInspector **não** aciona o `OnPreviewKeyDown` no PIE.
- Para ler a imagem do `CaptureEditorImage`: o arquivo em `tool-results/` tem o base64 dentro; extraia com `re.search(r'[A-Za-z0-9+/=]{5000,}', s)` e grave o PNG no scratchpad.

- **`SetText` por código não dispara `OnTextChanged`** do EditableTextBox. Depois de alterar o texto pelo teclado virtual, chame a função de refresh da lista manualmente (`KeyboardTyped`).
- **Ocultar por dispositivo:** `Input|Key|IsGamepadKey` no `OnPreviewKeyDown` e `OnPreviewMouseButtonDown` (override via `add_function_graph`) bastam para saber se o jogador está no controle.
- **Pôr um campo ao lado de um botão:** `UMGToolSet.WrapWidgets(widgetBlueprint, widgets=[campo], wrapperClass=/Script/UMG.HorizontalBox)` cria o HBox em volta do campo, e depois `AddWidget` no wrapper. Ajuste o slot do campo para `Fill`.
- **`SizeBox`:** `Layout|SizeBox|SetWidthOverride` (e `WidthOverride`/`HeightOverride` via `set_properties`) para teclas de largura fixa.
- **Widget criado em loop** (`UserInterface|CreateWidget` + `Widget|Panel|AddChild`) funciona para montar as teclas; `BuildKeys` com flag `Built` evita duplicar.
- **`BoxOverlapActorsWithOrientation` no DSL:** o pino `ObjectTypes` não aceita `MakeArray` do DSL. Escreva a chamada sem ele, depois `create_node Utilities|Array|MakeArray`, `set_pin_value` no item `[0]` (`ObjectTypeQuery4`) e `connect_pins` para `ObjectTypes`. `Math|Vector|vector-vector` não existe na escrita: use `(- a b)`.
- **Inserir uma checagem no meio de uma função grande** (ex.: `StackFree` em `GetCounterStack`): crie a função auxiliar com DSL e depois, no grafo grande, `break_pins` da ligação `then → Return`, crie o `CallFunction`, ligue `exec`, as entradas e a saída ao pino `Valid` do `Return`.

- **Foco em UMG:** `Widget|SetUserFocus (widget, PlayerController)` coloca o foco (confirme com `Widget|HasKeyboardFocus`/`HasAnyUserFocus` + `PrintString`). Chame depois do widget estar na viewport (use `Utilities|Time|SetTimerbyFunctionName ... 0.1–0.2 s`). **O Button do UMG não muda de aparência com foco**; faça o destaque por conta própria (`Button|Appearance|SetBackgroundColor` com `Utilities|Struct|MakeLinearColor`).
- **Eventos nativos sem retorno** (`OnAddedToFocusPath`, `OnRemovedFromFocusPath`) **não** podem ser criados com `add_function_graph` (erro "must be placed as an event node"). Use `add_event(blueprint, event_name, position)`, crie funções próprias (`HlOn`/`HlOff`) e ligue `then` → `CallFunction|...`. Funções com retorno (`OnPreviewKeyDown`, `OnPreviewMouseButtonDown`) sim, via `add_function_graph`.
- **Tick num widget** criado do zero: `create_node('AddEvent|UserInterface|EventTick')` e ligue `then` a um `CallFunction`.
- **Foto do PIE:** se uma janela flutuante (ex.: "Message Log") abrir na frente, `CaptureEditorImage` fotografa ela. Use `SlateInspectorToolset.Windows(action: "list")` e `action: "close", index: N` para fechá-la.

- **Prévia 3D em UMG (SceneCapture → Image), sem material:** `Rendering|CreateRenderTarget2D` (sem pino de world context: não passe `self`), `Class|SceneCaptureComponent2D|SetTextureTarget :self cap :TextureTarget rt`, `Rendering|SceneCapture|ShowOnlyActorComponents cap self` e `Appearance|SetBrushResourceObject (Image) rt`. Configure no componente (`set_properties`): `CaptureSource: SCS_FinalColorLDR`, `bCaptureEveryFrame/bCaptureOnMovement: false`, `PrimitiveRenderMode: PRM_UseShowOnlyList` e `ShowFlagSettings: [{ShowFlagName, Enabled:false}]` para Atmosphere/Fog/VolumetricFog/Cloud/Bloom (senão o fundo sai claro). Chame `Rendering|SceneCapture|CaptureScene` depois de trocar a malha.
- **Bounds de malha:** `StaticMesh|GetBounds` devolve uma struct; use `Math|BoxSphereBounds|BreakBoxSphereBounds` (`(bind (_origin _extent _radius) ...)`).
- **Criar Actor BP com componentes:** `BlueprintTools.create(folder_path, asset_name, asset_type=/Script/Engine.Actor)` + `ActorTools.add_component(owner=<BP>, component_type, name)` e `set_properties` em `<BP>_C:<Nome>_GEN_VARIABLE`. `set_parent_component` cria o pivô.
- **Mudar propriedade de widget (ex.: Visibility) exige recompilar o WBP** para valer no PIE.
- **Mapa título→sinopse:** `add_variable(type_name='string', container_type='MAP')` + `set_properties` no CDO com um objeto JSON (conferido: 19 entradas).
- **Fotos do PIE:** o `CaptureEditorImage` demora a refletir o estado; tire a foto alguns segundos depois do evento do roteiro e use `sleep` em background para sincronizar.

- **Surgery em função grande (ConfirmLoan, UpdateWalk):** liste os nós com `find_nodes` + `get_node_infos` e mostre só `type_id`, pinos `Exec` e vizinhos. Para trocar uma chamada: `delete_node` dos antigos, `create_node` do novo, `connect_pins` de `then`/`execute`/entradas. `ForEachLoop` de `GetAllActorsOfClass` dá elemento **Actor**: para chamar função do BP, ponha um `Utilities|Casting|CastToBP_X` entre o loop e a chamada.
- **`DestroyActor` do cliente destrói os livros presos na mão?** Para não perder o ator, solte (`DetachFromActor`), oculte e dê um `State` próprio (6 = emprestado) antes. Foi como o livro emprestado sobrevive para a devolução.
- **DSL entre classes:** `(!= a b)` funciona para objetos (o id `Utilities|NotEqual(Object)` do read-back **não** existe na escrita). Dentro do próprio BP use `(CallFunction|Fn :self x ...)` para chamar função em outro objeto da mesma classe.
- **Pino `Apply` (bool) literal:** `(Utilities|Array|SetArrayElem arr i true)` grava, mas o read-back mostra `"true"`.
- **Teste integrado longo (empréstimo → devolução):** o roteiro do `BP_TestDriver` rodou em tempo real (o jogo não fica lento sem foco). Combine `Delay` generosos (30–40 s) com `PrintString` rotulado (`T0 … T6`) e leia com `GetLogEntries`. O devedor ainda **está na loja** enquanto sai, e `PickReturner` o exclui de propósito: espere ele sumir (~30 s) antes de forçar `TrySpawn`.
- **Timer do sistema:** use `Bash sleep N` em `run_in_background` para sincronizar; cada notificação chega depois (consulte o log com `GetLogEntries` mesmo assim).

### Enhanced Input pelo MCP (funciona)
- Input Action: `DataAssetTools.create(asset_type=/Script/EnhancedInput.InputAction)`. O padrão já é ValueType Boolean.
- Mapping Context: `DataAssetTools.create(asset_type=/Script/EnhancedInput.InputMappingContext)`, depois `set_properties(imc, {"DefaultKeyMappings":{"mappings":[{"action":"/Game/.../IA_X.IA_X","key":"E","triggers":[],"modifiers":[]}, ...]}})`. Nomes de tecla: `E`, `C`, `RightMouseButton`, `Gamepad_FaceButton_Left/Right/Bottom`, `Gamepad_LeftTrigger`...
- Adicionar ao jogador: `(Input|AddMappingContext :self (PlayerController|LocalPlayerSubsystems|GetEnhancedInputLocalPlayerSubsystem (Game|GetPlayerController 0)) :MappingContext "/Game/.../IMC_X.IMC_X" :Priority 1)`.
- **Evento:** o DSL não cria. Use `create_node` com `Input|EnhancedActionEvents|IA_X`, que tem saídas `Started`, `Triggered`, `Ongoing`, `Canceled`, `Completed` e `ActionValue`, depois `connect_pins` para um `CallFunction|...`.
- Ao chamar função com argumento no DSL, use **keyword** (`(CallFunction|F :Delta x)`). O argumento posicional cai no `self`.
- Eventos nativos de Character disponíveis no DSL: `EventOnStartCrouch` / `EventOnEndCrouch (HalfHeightAdjust ScaledHalfHeightAdjust)`.

### Testes de input
- O `SlateInspectorToolset.PressKey` **não chega** ao pawn do PIE: o raio de debug nem é disparado. O teste de gameplay com teclado precisa ser feito pelo usuário. Pelo MCP dá para conferir o estado durante o PIE (`find_actors` + `get_properties` enxergam o mundo do PIE).
- `StartPIE` aceita `startTransform`, o que é útil para nascer já de frente para algo.
- **Roteiro de teste completo:**
  - No BeginPlay, escreva via DSL uma sequência de `Delay`, depois `Pawn|SetControlRotation` com `FindLookatRotation` (câmera → alvo), depois `CallFunction|Interact`. Para teleportar, use `SetActorLocation`.
  - Guarde referências que vão mudar (ex.: o livro que será solto) numa variável de debug **antes** da ação.
  - Depois do teste, reescreva o BeginPlay sem o roteiro e apague a variável de debug.
- **Teste automático de interação (funciona):** ligue temporariamente `EventBeginPlay → Delay 1.5 → Interact`, com `startTransform` de frente para o alvo e o pitch em -10. Depois de `StartPIE`, leia o estado com `find_actors` + `get_properties` e tire foto com `CaptureEditorImage`. Para fotografar o livro na mão, deixe um intervalo longo (cerca de 12 s) antes de um segundo `Interact`. **Remova o teste ao terminar.**
- O `GetLogEntries` com o padrão `BlueprintUserMessages` mostra os PrintString do PIE.

- GameMode do mapa: no ator `/Script/Engine.WorldSettings`, use `set_properties` com `{"DefaultGameMode": "/Game/.../BP_Y.BP_Y_C"}`.
- `CaptureViewport` exige `annotations` (pode ir com tudo zerado e `classFilter: null`). A imagem vem em base64 grande demais e é salva num arquivo em `tool-results/`. Decodifique com Python para PNG no scratchpad e abra com Read. `CaptureEditorImage` funciona do mesmo jeito.
- `StartPIE` costuma retornar "PIE ended before warmup completed" mesmo **com o PIE rodando**, porque o editor sem foco roda a 3 fps. Confirme com `IsPIERunning` e use `warmupSeconds: 0`. Durante o PIE, o `find_actors` enxerga o mundo do PIE.
- O contador de atores do Outliner pode mostrar bem menos que o `find_actors` (2.559 contra 8.038), porque ele não conta os filhos de GroupActor. Não é perda de atores.
- `add_to_scene_from_class` usa o `name` como nome do objeto, mas o label nem sempre fica igual. Sempre chame `set_label` depois.
- `AssetTools.duplicate` de um mapa cria o asset **na memória**. O `.umap` só aparece no disco depois de `save_assets`. O `_BuiltData` **não** é duplicado, mas com Lumen isso não pesa muito.
- O NavMeshBoundsVolume tem um brush padrão de 200 cm. Para cobrir uma área, use a escala do ator (tamanho desejado ÷ 200).
- Os labels podem enganar. Conferir as dimensões com `get_actor_bounds` é o jeito mais confiável de entender o que um ator é (`CheckoutBlock_2`, por exemplo, é o balcão).
- O comando `find_actors` sem filtro devolve cerca de 8 mil atores. Agregue tudo dentro de um script e devolva só o resumo.

## O que só dá para fazer pela interface do editor (peça ao usuário)
- Adicionar Feature Packs (First Person, Third Person): Content Drawer → **Add** → *Add Feature or Content Pack*.
- Baixar assets da Fab ou do Quixel Bridge e criar MetaHumans (MetaHuman Creator).
