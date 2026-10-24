# Library Project — guia para agentes

## O jogo
Começa como um **cozy game** em primeira pessoa: o jogador é o atendente de uma livraria e biblioteca
com café no mezanino. Ele recebe pessoas que vêm pegar ou devolver livros e registra cada operação.
Com o tempo, o jogo vai **se transformando em terror psicológico**, inspirado no teaser jogável *P.T.*
e em *Silent Hill*: anomalias sutis, repetição, um espaço que fica estranho aos poucos.
Avançamos devagar, em muitas etapas pequenas. Veja [docs/ROADMAP.md](docs/ROADMAP.md).

## Decisões fixas
- **Unreal Engine 5.8.** O projeto é **só Blueprints** (não tem pasta `Source/`). Não crie C++ sem o usuário pedir.
- **Câmera em primeira pessoa**, baseada no template First Person.
- Personagens: por enquanto usamos os manequins (Manny/Quinn). **MetaHumans** entram depois.
- Lumen ligado (`r.DynamicGlobalIlluminationMethod=1`, `r.ReflectionMethod=1`).

## Regras de conteúdo
- `/Game/Stationer/` é o pacote de assets da Fab ("Stationer" / Barrel & Bark). **Não edite nem salve nada nele.** Se precisar mudar um asset, duplique para `/Game/Library/`.
- `/Game/Stationer/Levels/L_Stationer` é a **cena original de referência**. Não mexa nela.
- O jogo é montado em **`/Game/Library/Maps/L_Library`**, uma cópia de L_Stationer. Ela é o mapa padrão do jogo e do editor.
- Todo conteúdo nosso fica em `/Game/Library/{Maps,Blueprints,Characters,UI,Data,Input,Materials}`.
- Não edite os assets do template First Person (`/Game/FirstPerson`, `/Game/Input`). Crie filhos ou cópias em `/Game/Library`.
- Prefixos de nome: `BP_`, `WBP_`, `DT_` (DataTable), `DA_`, `M_`/`MI_`, `L_` (mapas), `E_` (enums), `S_` (structs).

## Como trabalhar no editor
- Use o MCP do Unreal (skill `unreal-mcp`). Os detalhes práticos e as pegadinhas estão em [docs/MCP_WORKFLOW.md](docs/MCP_WORKFLOW.md).
- O layout da cena (coordenadas do balcão, da porta, da escada, do café e as pastas do Outliner) está em [docs/SCENE_MAP.md](docs/SCENE_MAP.md). Consulte antes de posicionar qualquer coisa.
- Como clonar ou restaurar o projeto (o pacote Stationer fica fora do git) está em [docs/SETUP.md](docs/SETUP.md).
- Antes de mudanças em massa, confira que os assets estão salvos (`AssetTools.is_dirty`). Salve de novo ao terminar (`AssetTools.save_assets`).
- Os atores de gameplay ficam na pasta `Gameplay/` do Outliner; as câmeras e a sequência originais ficam em `Cinematic/`.

## Onde paramos (atualize ao fim de cada sessão)
Estado em 2026-10-23. Etapas 0, 1, 1b, 1c, 1d, **2a (primeiro cliente, empréstimo)** e **2b (spawn + fila)** estão concluídas (detalhes no [docs/ROADMAP.md](docs/ROADMAP.md)).
- **Personagem `BP_LibraryCharacter`:**
  - Primeira pessoa, sem pulo, caminhada lenta.
  - Mira de ponto central.
  - Carrega até 3 livros (pilha deitada, capa para cima).
  - **E** (`OnInteractPressed`): mirando num cliente, fala com ele; senão pega / guarda / solta livros. **C** agacha (alterna); **botão direito** segurado dá zoom.
  - O input é Enhanced Input (`/Game/Library/Input/IMC_Library`), com controle já mapeado mas não testado.
- **Livros `BP_Book`:**
  - Só a estante **History** (`BP_BookShelfs10`, topo da escada) tem livros unitários pegáveis (138). As outras estantes ainda são o cenário original do pacote.
  - Áreas amarelas `BP_PlaceZone`: 7 na History e 1 no balcão. No balcão, o E entrega a pilha inteira.
  - Cada livro tem título e autor pela malha (`GetBookInfo`, mapas no CDO do BP_Book).
- **Clientes `BP_Customer`, criados pelo `CustomerSpawner`:**
  - Chegam a cada 60–120 s, até 3 na loja (o primeiro em 3 s).
  - Surgem do lado de dentro da porta (a porta é falsa por enquanto), entram em linha reta e fazem fila em frente ao balcão.
  - Só o da frente responde. O E mostra o papel `WBP_RequestList` com 1 a 3 livros.
  - Com os livros certos no balcão, o segundo E faz ele levar os livros, sair pela faixa lateral e sumir na porta, e a fila anda. Livro errado não faz nada.
  - Sem devolução e sem reposição na estante.
- **Problema conhecido:** o agachar desce a FirstPersonMesh inteira, e os pés atravessam o chão. Falta uma animação de agachar (já está no ROADMAP).
- **Próximos passos naturais** (ROADMAP Etapa 2): teste do usuário com teclado, porta que abre, sininho, devolução e reposição de estoque.
- ⚠️ Não apague assets pelo MCP logo depois de um PIE: isso já derrubou o editor (veja o MCP_WORKFLOW).

## Como trabalhar bem aqui (aprendizados)
- Leia o [docs/MCP_WORKFLOW.md](docs/MCP_WORKFLOW.md) **antes** de editar Blueprints pelo MCP. Ele tem várias armadilhas já resolvidas: nós puros reavaliados, `if` que encerra o fluxo, defaults do CDO que se perdem, pinos de array, eventos de input, perfis de colisão etc.
- **Teste sozinho antes de pedir teste ao usuário:** monte um roteiro temporário no BeginPlay (Delay → SetControlRotation/FindLookAt → chamadas), rode o PIE, confira o estado com `find_actors`/`get_properties` e tire fotos com `CaptureEditorImage`. **Remova o roteiro no fim.** Tecla simulada não chega ao PIE.
- Sempre confira as coordenadas no [docs/SCENE_MAP.md](docs/SCENE_MAP.md) antes de posicionar algo.
- Salve (`save_assets`) depois de cada etapa. O usuário versiona no git (veja [docs/SETUP.md](docs/SETUP.md)). `/Content/Stationer` **não** vai para o git.

## Mantenha estes docs vivos
Quando descobrir algo que funciona (ou que não funciona), registre no `.md` certo dentro de `docs/`.
Quando uma etapa do roadmap for concluída, atualize o [docs/ROADMAP.md](docs/ROADMAP.md).
