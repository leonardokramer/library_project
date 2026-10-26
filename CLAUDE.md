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

## Git
- **Nunca faça commit (nem push) por conta própria.** Só commite quando o usuário confirmar explicitamente, a cada vez.

## Como trabalhar no editor
- Use o MCP do Unreal (skill `unreal-mcp`). Os detalhes práticos e as pegadinhas estão em [docs/MCP_WORKFLOW.md](docs/MCP_WORKFLOW.md).
- O layout da cena (coordenadas do balcão, da porta, da escada, do café e as pastas do Outliner) está em [docs/SCENE_MAP.md](docs/SCENE_MAP.md). Consulte antes de posicionar qualquer coisa.
- Como clonar ou restaurar o projeto (o pacote Stationer fica fora do git) está em [docs/SETUP.md](docs/SETUP.md).
- Antes de mudanças em massa, confira que os assets estão salvos (`AssetTools.is_dirty`). Salve de novo ao terminar (`AssetTools.save_assets`).
- Os atores de gameplay ficam na pasta `Gameplay/` do Outliner; as câmeras e a sequência originais ficam em `Cinematic/`.

## Onde paramos (atualize ao fim de cada sessão)
Estado em 2026-10-24. Etapas 0, 1, 1b, 1c, 1d, **2a (primeiro cliente, empréstimo)**, **2b (spawn + fila)**, **2c (sistema no computador)** e **2d (sistema em subtelas)** estão concluídas (detalhes no [docs/ROADMAP.md](docs/ROADMAP.md)).
- **Personagem `BP_LibraryCharacter`:**
  - Primeira pessoa, sem pulo, caminhada lenta.
  - Mira de ponto central.
  - Carrega até 3 livros (pilha deitada, capa para cima).
  - **E** (`OnInteractPressed`): mirando num livro ou numa área válida, cuida dos livros; mirando num cliente, fala com ele; mirando na **caixa registradora**, abre o sistema; senão solta livros. **Q** (segurado) abre os livros da mão em leque na frente da câmera para ler as capas (`SetInspectMode`/`UpdateInspect` no personagem, `GetInspectTransform` no `BP_Book`; os livros ficam no State 4 enquanto abertos); **C** agacha (alterna); **botão direito** segurado dá zoom.
  - O input é Enhanced Input (`/Game/Library/Input/IMC_Library`), com controle já mapeado mas não testado.
- **Livros `BP_Book`:**
  - Só a estante **History** (`BP_BookShelfs10`, topo da escada) tem livros unitários pegáveis (138). As outras estantes ainda são o cenário original do pacote.
  - Áreas amarelas `BP_PlaceZone`: 7 na History e 1 no balcão. No balcão, o E entrega a pilha inteira.
  - Cada livro tem título e autor pela malha (`GetBookInfo`, mapas no CDO do BP_Book).
- **Clientes `BP_Customer`, criados pelo `CustomerSpawner`:**
  - Chegam a cada 180–360 s, até 3 na loja (o primeiro em 5 s).
  - Surgem do lado de dentro da porta (a porta é falsa por enquanto), entram em linha reta e fazem fila em frente ao balcão.
  - Cada um tem **nome e documento**, sorteados de um pool de 10 pessoas no `BP_LibrarySystem` (5 já cadastradas).
  - Só o da frente responde. O E mostra o papel `WBP_RequestList` com nome, documento e 1 a 3 livros. O E **não entrega** mais os livros.
  - Sem devolução e sem reposição na estante.
- **Sistema `BP_LibrarySystem` + `WBP_LibrarySystem`** (E na caixa registradora, tela cheia), **redesenhado em subtelas (Etapa 2d)**:
  - `WBP_LibrarySystem` é o shell: barra lateral + `WidgetSwitcher` com `WBP_ScreenBooks` (busca, A→Z/Z→A, detalhe), `WBP_ScreenUsers` (busca, ordenação, histórico, cadastro) e `WBP_ScreenLoan` (lançar, confirmar, limpar). O estado fica no shell; as telas o chamam por `Owner` (`Bind`).
  - O papel do pedido virou **modal** (botão PEDIDO, P / Y). O papel do jogo fica escondido enquanto o sistema está aberto e volta ao sair sem concluir.
  - O sistema confere usuário, livros no balcão e pedido; se algo não bate, mostra um aviso e não registra nada. Com tudo certo, a tela fecha e o cliente leva os livros e sai sozinho. Sair guarda um rascunho.
  - Esc/B (`HandleBack`) fecha o pedido e depois o sistema, e P/Y abre o pedido (`OnPreviewKeyDown`). **Não testado com teclado/controle de verdade.**
  - Ainda falta: teclado virtual, prévia 3D da capa + sinopses, destaque visual do foco, histórico com data/devolvido, SaveGame do cadastro e um computador de verdade no lugar da caixa registradora.
- **Problema conhecido:** o agachar desce a FirstPersonMesh inteira, e os pés atravessam o chão. Falta uma animação de agachar (já está no ROADMAP).
- **Próximos passos naturais** (ROADMAP Etapa 2): teste do usuário com teclado do ciclo completo (papel → estante → balcão → sistema), Esc para fechar o sistema, porta que abre, sininho, devolução e reposição de estoque.
- O `BP_TestDriver` (`/Game/Library/Debug/`) ficou com o roteiro de teste do sistema no EventGraph. Ele **não está na cena**. Reescreva o grafo antes de reutilizar.
- ⚠️ Não apague assets pelo MCP logo depois de um PIE: isso já derrubou o editor (veja o MCP_WORKFLOW).

## Como trabalhar bem aqui (aprendizados)
- Leia o [docs/MCP_WORKFLOW.md](docs/MCP_WORKFLOW.md) **antes** de editar Blueprints pelo MCP. Ele tem várias armadilhas já resolvidas: nós puros reavaliados, `if` que encerra o fluxo, defaults do CDO que se perdem, pinos de array, eventos de input, perfis de colisão etc.
- **Teste sozinho antes de pedir teste ao usuário:** monte um roteiro temporário no BeginPlay (Delay → SetControlRotation/FindLookAt → chamadas), rode o PIE, confira o estado com `find_actors`/`get_properties` e tire fotos com `CaptureEditorImage`. **Remova o roteiro no fim.** Tecla simulada não chega ao PIE.
- Sempre confira as coordenadas no [docs/SCENE_MAP.md](docs/SCENE_MAP.md) antes de posicionar algo.
- Salve (`save_assets`) depois de cada etapa. O usuário versiona no git (veja [docs/SETUP.md](docs/SETUP.md)). `/Content/Stationer` **não** vai para o git.

## Mantenha estes docs vivos
Quando descobrir algo que funciona (ou que não funciona), registre no `.md` certo dentro de `docs/`.
Quando uma etapa do roadmap for concluída, atualize o [docs/ROADMAP.md](docs/ROADMAP.md).
