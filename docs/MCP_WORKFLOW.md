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
