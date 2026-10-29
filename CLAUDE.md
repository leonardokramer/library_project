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
- Prefixos de nome: `BP_`, `WBP_`, `ABP_` (AnimBP), `DT_` (DataTable), `DA_`, `M_`/`MI_`, `L_` (mapas), `E_` (enums), `S_` (structs), `IA_`/`IMC_` (input).

## Git
- **Nunca faça commit (nem push) por conta própria.** Só commite quando o usuário confirmar explicitamente, a cada vez.

## Como trabalhar no editor
- Use o MCP do Unreal (skill `unreal-mcp`). Os detalhes práticos e as pegadinhas estão em [docs/MCP_WORKFLOW.md](docs/MCP_WORKFLOW.md).
- O layout da cena (coordenadas do balcão, da porta, da escada, do café e as pastas do Outliner) está em [docs/SCENE_MAP.md](docs/SCENE_MAP.md). Consulte antes de posicionar qualquer coisa.
- Como clonar ou restaurar o projeto (o pacote Stationer fica fora do git) está em [docs/SETUP.md](docs/SETUP.md).
- Antes de mudanças em massa, confira que os assets estão salvos (`AssetTools.is_dirty`). Salve de novo ao terminar (`AssetTools.save_assets`).
- Os atores de gameplay ficam na pasta `Gameplay/` do Outliner; as câmeras e a sequência originais ficam em `Cinematic/`.

## Onde paramos (atualize ao fim de cada sessão)
Estado em 2026-10-29. Etapas 0, 1 e 2a–2e concluídas (detalhes no [docs/ROADMAP.md](docs/ROADMAP.md)); limpeza de manutenção concluída em 2026-10-29 (o que sobrou está em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), seção "Dívida técnica").
Mapa dos Blueprints, convenções e como adicionar livro/tela: **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.

**O que já funciona**
- **Jogador `BP_LibraryCharacter`:** primeira pessoa, sem pulo, caminhada lenta, mira de ponto. **E** interage (livro, área de guardar, cliente, caixa registradora, ou solta livros); **Q** segurado abre os livros da mão em leque; **C** agacha (alterna); **botão direito** dá zoom. Carrega até 3 livros. Input em `/Game/Library/Input/IMC_Library` (Enhanced Input; controle mapeado, não testado).
- **Livros `BP_Book`:** ~1.700 unitários em 24 estantes por gênero (tabela em [docs/SCENE_MAP.md](docs/SCENE_MAP.md#estantes-por-gênero)); áreas `BP_PlaceZone` (7 por estante + balcão); título/autor/sinopse/gênero na `DT_Books` (`/Game/Library/Data/Tables`, uma linha por malha). O `BP_Book` só liga o tick em State 1/2 (`PickUp`/`PlaceAt` ligam, `SleepIfIdle` desliga): se criar outra função que ponha um livro em State 1 ou 2, ligue o tick nela.
- **Clientes `BP_Customer` + `BP_CustomerSpawner`:** chegam a cada 180–360 s (primeiro em 5 s), até 3 na loja, fazem fila; só o da frente responde. Empréstimo (papel `WBP_RequestList`) ou devolução (`ReturnChance` 0,4; vêm com os livros na mão). O jogo já começa com histórico (`SeedHistory`: 11 registros).
- **Dados em `/Game/Library/Data`:** structs `S_LoanRecord`/`S_Person`/`S_BookInfo`, tabelas `DT_Books` (catálogo), `DT_People` (pool de clientes) e `DT_SeedLoans` (histórico inicial); no sistema, `Loans` e `Users` são arrays de struct e o limite de livros é `MaxBooks` (e `BP_Customer.MaxRequestBooks`). Os enums `E_*` existem mas não são usados (o MCP não cria variável de enum).
- **Sistema `BP_LibrarySystem` + `WBP_LibrarySystem`** (E na caixa registradora): janela estilo Win95 com abas LIVROS, CLIENTES, EMPRÉSTIMO e DEVOLUÇÃO (LB/RB), pedido em modal (P/Y), Esc/B fecha, teclado virtual só no controle, prévia 3D da capa (`BP_BookPreview`, pose yaw -38°: não troque sem conferir que não vira o verso).
- **Animações:** agachar com assets do Lyra (`ABP_Body_Library`, `ABP_FP_Library`) e polimento do NPC (`ABP_Customer`: olhar em volta na fila). Detalhes e armadilhas (o Alpha do `CtrlRig_FPWarp` é um pino) em [docs/ANIMATION_NOTES.md](docs/ANIMATION_NOTES.md).

**Ainda falta:** teste do usuário com teclado/controle de verdade (ciclo completo, Esc, foco por D-pad); data no histórico; SaveGame do cadastro/histórico (zera ao reiniciar o mapa); computador de verdade no lugar da caixa registradora; porta que abre e sininho; reposição de estoque. Próximo: Etapa 3 (ciclo de dias).

**Armadilhas que custaram caro**
- ⚠️ **Nunca use "Adicionar ao projeto" do Lyra no `library_project`:** sobrescreve `Config/`, traz `Source/` e `Plugins/` e o editor deixa de abrir. O Lyra fica como projeto separado (`LyraStarterGame`, ao lado deste em `Unreal Projects`); copiamos só os `.uasset` (veja o ANIMATION_NOTES).
- ⚠️ **Não apague assets pelo MCP logo depois de um PIE:** já derrubou o editor. Reabra o editor antes ou apague pelo Content Browser.
- **Teste de regressão do ciclo empréstimo/devolução:** `BP_TestDriver` (`/Game/Library/Debug/`) tem o roteiro pronto (`Poll` a cada 1 s → `Phase0/1/2`: cliente da frente, `ConfirmLoan`/`ConfirmReturn`, `Stats` do histórico). Ele **fica fora da cena**: ponha um ator temporário, rode o PIE, leia `LogBlueprintUserMessages` e remova o ator. Para forçar o tipo de cliente, mude `ReturnChance` no CDO do `BP_Customer` (0 = empréstimo, 1 = devolução) e **restaure 0,4**.
- Estados numéricos (`State`/`Mode`/`ZoneType`) ainda são inteiros: ao mexer neles, confira todos os `==` (veja ARCHITECTURE, seção Enums).
- Reescrever função com `write_graph_dsl` pode deixar nós órfãos, e o read-back mostra `type_id` falsos: veja o MCP_WORKFLOW ("Aprendizados da migração para structs").

## Como trabalhar bem aqui (aprendizados)
- Leia o [docs/MCP_WORKFLOW.md](docs/MCP_WORKFLOW.md) **antes** de editar Blueprints pelo MCP. Ele tem várias armadilhas já resolvidas: nós puros reavaliados, `if` que encerra o fluxo, defaults do CDO que se perdem, pinos de array, eventos de input, perfis de colisão etc.
- **Teste sozinho antes de pedir teste ao usuário:** monte um roteiro temporário no BeginPlay (Delay → SetControlRotation/FindLookAt → chamadas), rode o PIE, confira o estado com `find_actors`/`get_properties` e tire fotos com `CaptureEditorImage`. **Remova o roteiro no fim.** Tecla simulada não chega ao PIE.
- Sempre confira as coordenadas no [docs/SCENE_MAP.md](docs/SCENE_MAP.md) antes de posicionar algo.
- Salve (`save_assets`) depois de cada etapa. O usuário versiona no git (veja [docs/SETUP.md](docs/SETUP.md)). `/Content/Stationer` **não** vai para o git.

## Mantenha estes docs vivos
Quando descobrir algo que funciona (ou que não funciona), registre no `.md` certo dentro de `docs/`.
Quando uma etapa do roadmap for concluída, atualize o [docs/ROADMAP.md](docs/ROADMAP.md).
