# Roadmap

Vamos avançar devagar, em etapas pequenas e jogáveis. Marque com [x] o que estiver pronto.

## Etapa 0 — Base
- [x] Mapear a cena L_Stationer ([SCENE_MAP.md](SCENE_MAP.md))
- [x] Duplicar a cena para `/Game/Library/Maps/L_Library` e definir como mapa padrão
- [x] PlayerStart atrás do balcão, NavMeshBoundsVolume e TargetPoints de NPC
- [x] Importar o Feature Pack **First Person**
- [x] `BP_LibraryGameMode` com o personagem de primeira pessoa, definido no World Settings de L_Library
- [x] Manequins de estand-in no balcão, no café e entre as estantes
- [x] PIE: o jogador nasce atrás do balcão em primeira pessoa
- [x] Teste manual: andar, subir a escada, chegar ao café, ver a NavMesh (tecla P)
- [x] NavMesh sem ilhas em cima dos móveis (NavModifierVolumes)
- [x] `BP_LibraryCharacter`: sem pulo, caminhada lenta (200)
- [ ] Talvez: balanço leve de cabeça (head bob) e passos com som. Isso ajuda muito no terror depois.
- [ ] Decidir se removemos o crosshair e a arma do template (o personagem é um atendente)

## Etapa 1 — Balcão (cozy)
- [x] `BP_Book` (malha Movable, estado estante, mão ou voltando, deslize suave)
- [x] Estante de teste History: 25 `BP_Book`, 13 livros removidos
- [x] Interagir olhando + E (line trace a partir da câmera): pegar e devolver
- [x] Pose do livro na mão (capa virada, canto inferior direito). Verificado pelo teste automático no PIE.
- [x] Mira (ponto no centro, `WBP_Crosshair`)
- [x] Etapa 1b: as fileiras fundidas da History foram trocadas por 113 livros unitários
- [x] Soltar com física (cai no chão) e pegar de volta do chão
- [x] Guardar na estante em qualquer espaço livre (encaixe ±6 cm), zonas `BP_PlaceZone` e fantasma amarelo
- [x] Colocar no balcão (deitado, empilhando por raio vertical, sem física)
- [x] Carregar até 3 livros (pilha em leque na mão)
- [x] Etapa 1c: capa para cima no balcão e na mão (pilha deitada), e E no balcão entrega a pilha inteira
- [ ] Teste do usuário com teclado do ciclo completo
- [ ] Destaque do livro sob a mira (outline ou ponto que muda de cor)
- [x] Leque para inspecionar os livros da mão (2026-10-24): Q segurado (`IA_Inspect`, controle: Y). Verificado no PIE com 3 livros: capas legíveis a 55 cm, espaçamento 18 cm entre livros (sem sobrepor, títulos do topo visíveis), inclinação de 14° por livro, e voltam para a pilha ao soltar. Ainda falta teste do usuário.
  - Anti-atravessar: `UpdateInspect` faz um `SphereTraceByChannel` (Visibility, raio 26) 70 cm à frente da câmera e escala o leque por `dist/62` (mín. 0,3). O primeiro trace usava só WorldStatic e **não pegava as pranchas da estante**: Visibility pega estante, pilar, parede e os livros da prateleira: o leque encolhe e chega perto em vez de entrar na estante/pilar.
  - Pilha **na mão** (estado 1): o mesmo trace dá `HoldScale = clamp((dist+26)/62, 0.3, 1)`, gravado em cada livro por `UpdateInspect`. No tick do `BP_Book`, `ScaleHoldTransform` (inserido entre `GetBookExtents` e o `SetActorTransform` do estado 1) escala a pose-alvo em torno da câmera. `Drop` volta a escala para 1 antes de ligar a física. Verificado no PIE colado na estante. Falta teste do usuário (inclusive soltar/guardar com a pilha encolhida).
- [~] Precisão de pegar/devolver (2026-10-24): `TraceBook` com raio 0.5 (era 5), `SlotOffsets` em passos de 0,25 cm até ±8 (65 valores). A tolerância do overlap em `GetPlacement` ficou em 0.4 (original): 1.2 deixava o livro atravessar o vizinho. Aplicado, **falta teste do usuário com o mouse** (Open Office Design vs Cities; devolver livro em vão apertado).
- [ ] Empilhar no balcão mirando em cima de outro livro (hoje mirar num livro = pegar)
- [ ] Converter outras estantes (livros unitários + zonas, script em lote igual ao da History)
- [x] Balcão → entregar o livro ao NPC (primeiro passo do ciclo de empréstimo). Veja a Etapa 2.
- [x] Migrar a tecla E para Enhanced Input (`IA_Interact`, `IMC_Library`)
- [x] Agachar (C / B, alternar; a câmera desce 50 cm suavemente)
- [x] Zoom para ler lombadas (botão direito / LT segurado, FOV 90 → 50)
- [ ] **Animação de agachar** (Fab/Mixamo) no Animation Blueprint da FirstPersonMesh. Hoje a malha inteira desce 50 cm e os pés atravessam o chão (veja SCENE_MAP → Agachar)
- [ ] Testar no controle (os mapeamentos já existem)
- [ ] Talvez: reduzir a sensibilidade do mouse durante o zoom
- [x] Catálogo de livros (título + autor por malha). Saiu como mapas no CDO do `BP_Book` (`GetBookInfo`), porque o MCP não cria struct/DataTable.
- [ ] Talvez: migrar o catálogo para um `DT_Books` de verdade (struct criado à mão no editor) e adicionar gênero
- [x] Computador no balcão para registrar empréstimo. Saiu como `WBP_LibrarySystem` na caixa registradora (Etapa 2c). A devolução ainda falta.

## Etapa 2 — Clientes
- [x] Etapa 2a, empréstimo com um cliente:
  - `BP_Customer` (Quinn + AIController + ABP_Unarmed) entra por `NPC_Spawn` e anda até `NPC_Counter`.
  - E no cliente mostra o papel (`WBP_RequestList`) com 1 a 3 livros (título + autor).
  - O jogador busca os livros e coloca no balcão. E de novo: se os livros estiverem certos, o cliente leva tudo e sai por `NPC_Exit`; se estiverem errados, aparece um aviso no papel.
  - Os manequins parados foram removidos.
  - Verificado por teste automático no PIE (pedido, entrega errada, entrega certa e saída).
- [ ] Teste do usuário com teclado do ciclo de empréstimo
- [x] Etapa 2b, spawn e fila:
  - `BP_CustomerSpawner` cria clientes a cada 60–120 s (até 3 na loja).
  - Eles entram em linha reta pela porta e fazem fila em Y 170. A fila anda quando o da frente é atendido, e quem sai vai pela faixa Y≈250 e some na porta.
  - O cliente para colado no balcão (X -437).
  - Entrega errada não faz nada (a frase de erro saiu).
  - Clientes não pedem títulos já pedidos por outro.
  - Verificado por teste automático no PIE.
- [ ] Teste do usuário com teclado da fila
- [x] Etapa 2c, sistema da livraria no computador:
  - E mirando na caixa registradora abre `WBP_LibrarySystem` em tela cheia. O papel do pedido fica visível à esquerda.
  - O papel agora tem **nome e documento** do cliente. Há um pool de 10 pessoas no `BP_LibrarySystem`, 5 já cadastradas.
  - O sistema tem: acervo com cópias na estante e busca por título/autor, busca de usuário por nome ou documento, cadastro de usuário novo, até 3 livros lançados e confirmação.
  - Ao confirmar, o sistema confere usuário = cliente do balcão, livros do balcão = lançamento e lançamento = pedido. Se algo não bate, aparece um aviso e nada é registrado. Se bate, a tela fecha e o cliente pega os livros e sai sozinho.
  - O segundo E no cliente **não entrega mais**: só mostra o papel de novo.
  - Sair do sistema guarda um **rascunho** (usuário + itens + aviso). Dá para corrigir o balcão e voltar.
  - Clientes a cada 180–360 s (o primeiro em 5 s).
  - Verificado por teste automático no PIE.
- [ ] Teste do usuário com teclado/mouse do sistema
- [x] Etapa 2d, redesenho do sistema em subtelas (fases 1, 3, 5 e 6 do plano; fases 2 e 4 abaixo):
  - `WBP_LibrarySystem` virou o **shell**: barra lateral (LIVROS · CLIENTES · EMPRÉSTIMO · PEDIDO · SAIR) + `WidgetSwitcher` com `WBP_ScreenBooks`, `WBP_ScreenUsers` e `WBP_ScreenLoan`. O estado (usuário, itens, status, rascunho) continua no shell; as telas chamam o shell por `Owner`.
  - **Livros:** busca, A→Z / Z→A, lista grande, detalhe (título, autor, cópias, "ADICIONAR AO EMPRÉSTIMO"). Sinopse e prévia 3D ainda são placeholders.
  - **Clientes:** busca, A→Z / Z→A, detalhe com **histórico de empréstimos**, cadastro novo, "USAR NO EMPRÉSTIMO".
  - **Empréstimo:** cliente, resumo do pedido, livros lançados, lançar/confirmar/limpar (mesmas regras de conferência de antes).
  - **Pedido:** o papel saiu da coluna. Virou um modal por cima do sistema (botão PEDIDO, P / Y). O papel do jogo fica escondido enquanto o sistema está aberto e volta ao sair sem concluir.
  - `BP_LibrarySystem` ganhou `StrLess` e `SortOrder` (ordenação alfabética sem tool de sort).
  - Verificado no PIE por roteiro (`BP_TestDriver`): as 3 telas, ordenação, detalhe, histórico, modal do pedido e saída.
- [x] Ajustes pós-teste do usuário (2026-10-26):
  - **Balcão não deixa mais atravessar livros:** `BP_PlaceZone.StackFree(Center, HalfSize)` (BoxOverlap contra `BP_Book`) entra antes do `Return` de `GetCounterStack` e define o `Valid`. Pilha que invade livros já no balcão fica inválida (fantasma some e o E solta). Verificado no PIE: pilha 1 válida, sobreposta (16 cm) inválida, livre (45 cm) válida.
  - **Feedback do "Adicionar ao empréstimo":** o botão vira "✓ ADICIONADO AO EMPRÉSTIMO" (desativado) e aparece "Adicionado! Livros no empréstimo: N de 3". Ao voltar para a aba Livros o botão se atualiza (`RefreshAddButton`), e o limite de 3 mostra aviso.
- [ ] Teste do usuário com teclado/controle do novo sistema: **P / Y** abre o pedido, **Esc / B** fecha o pedido e depois o sistema, e foco por setas/D-pad (a tecla simulada não chega ao PIE, então não foi testada)
- [x] Fase 2 do redesenho: **teclado virtual** (`WBP_VirtualKeyboard` + `WBP_KeyButton`), pensado **só para o controle**:
  - Overlay no shell (`KeyboardOverlay`), grade 0-9 / QWERTY / acentos (ÁÉÍÓÚÃÕÂÊÔÇ), ESPAÇO, APAGAR, LIMPAR e OK. Auto-capitaliza a primeira letra de cada palavra. Tem prévia do texto.
  - Botões "TECLADO" ao lado da busca de livros, da busca de clientes e dos campos do cadastro (`OpenKeyboard(Target, Title, Mode)`). A busca filtra a lista a cada tecla (`KeyboardTyped`).
  - **Os botões só aparecem quando o último input foi do controle** (`SetPadMode`, via `OnPreviewKeyDown` com `IsGamepadKey`; mouse volta a escondê-los). Com teclado/mouse, o campo de texto normal basta.
  - Esc/B fecha o teclado primeiro (`HandleBack`).
  - Verificado no PIE (digitar "Cit" filtra para "Cities"; botões escondidos sem controle e visíveis com ele). **Falta testar com um controle de verdade** (foco por D-pad nas teclas, e a detecção de controle).
- [x] Fase 4 do redesenho (2026-10-26): **prévia 3D da capa + sinopses**:
  - `BP_BookPreview` (`/Game/Library/Blueprints/`): `Pivot` → `BookMesh`, `Cap` (SceneCaptureComponent2D, `ShowOnlyActorComponents` só dele, sem atmosfera/fog/bloom, fundo preto) e 2 luzes. No `BeginPlay` cria um RenderTarget 512×512. `ShowMesh(Mesh, Yaw)` centraliza a malha pelos bounds, gira o pivô, afasta a câmera (3,1 × o raio) e chama `CaptureScene`.
  - O shell **gera o ator** em (0, 0, -30000) no `Open` (`Preview`) e o destrói no `CloseSystem` (`KillPreview`). `ShowPreview(Title, Img)` acha um `BP_Book` da cena com aquele título, copia a malha para a prévia e liga o RenderTarget ao `PreviewImage` (via `SetBrushResourceObject`).
  - **Pose: yaw -38°. Mostra a FRENTE da capa com a lombada à esquerda** (conferido em "Cities": ilustração e título na frente, título na lombada). Cuidado ao mudar o yaw: a +142° apareceria o verso.
  - **Sinopses:** `BP_Book.BookSynopses` (mapa título → sinopse, 19 textos curtos em pt-BR, tom cozy) no CDO; `GetSynopsis(Title)` no shell; "Sem descrição." se faltar.
  - Verificado no PIE com "Classic Poems" e "Cities".
  - **Layout do detalhe (ajuste pós-teste):** título, autor, cópias, **botão de adicionar (no topo)**, prévia (Fill) e **sinopse embaixo**, dentro de `SizeBox` (`bOverride_MaxDesiredHeight` + 150) + `ScrollBox` (`SynScroll`): sinopse longa rola em vez de estourar o painel (testado com texto de ~600 caracteres). Câmera da prévia em 3,9 × o raio, para o livro não cortar.
  - **Rolagem no controle:** o analógico direito (eixo Y) rola a sinopse (aba Livros) e o histórico (aba Clientes) via `OnAnalogValueChanged` → `ScrollContent`. Não testado com controle de verdade.
  - Ao adicionar livros novos: crie a entrada em `BookTitles`, `BookAuthors` **e** `BookSynopses`.
- [ ] Histórico com data/dia de jogo e status "devolvido" (hoje `LoanDocs`/`LoanTitles` guardam só documento e títulos)
- [x] **Navegação por foco (controle/teclado), 2026-10-26:**
  - Ao abrir o sistema o foco vai para a aba LIVROS (`FocusTab`, com timer de 0,2 s). Ao fechar o papel ou o teclado, o foco volta para a aba atual. Ao abrir o teclado, o foco vai para a primeira tecla; ao abrir o papel, para o botão Fechar.
  - **Destaque do foco:** o botão do UMG não muda de aparência com foco, então o shell chama `HlAll` no Tick e `Hl(Btn)` clareia o botão com foco (`SetBackgroundColor` ×7 sobre o estilo escuro com moldura). `WBP_Row` e `WBP_KeyButton` fazem o mesmo em `OnAddedToFocusPath`/`OnRemovedFromFocusPath` (`HlOn`/`HlOff`). O destaque some no modo mouse (`MouseMode`, ligado por clique, desligado por qualquer tecla).
  - **LB / RB** trocam de aba (`HandleShoulder`).
  - Verificado no PIE: foco inicial no LIVROS (`HasKeyboardFocus = YES`) e o botão fica destacado. **Falta testar com controle de verdade:** D-pad/setas entre botões, linhas da lista e teclas, e o A apertando.
- [x] Correções após o teste do usuário com controle (2026-10-26):
  - Aviso "WBP_KeyButton does not support focus": `FocusFirst` pedia foco para o `UserWidget` da tecla. Agora a tecla tem `FocusMe` (foco no botão interno) e o teclado usa `Cast` para chamá-la. O foco entra no teclado e volta para a aba ao fechar (verificado).
  - **Voltar com ←:** regra de navegação explícita "esquerda → aba atual" nos controles da borda esquerda de cada tela (`SetLeftRules`, chamada em `ShowTab`) e em todas as linhas (`WBP_Row.Setup`, via `TabButton`).
  - Com o teclado virtual ou o papel abertos, o fundo (`Bg`) fica desabilitado, então o foco não escapa para a tela de trás.
  - **Falta confirmar com o controle:** ← na lista volta para a aba; navegação em todas as direções no teclado virtual.
- [x] Ajustes do controle, rodada 2 (2026-10-26):
  - **→ das linhas** vai para o botão de ação da aba (`ContentButton`: "ADICIONAR AO EMPRÉSTIMO" nos Livros, "USAR NO EMPRÉSTIMO" nos Clientes), por regra explícita em `WBP_Row.Setup`.
  - **A num campo de texto abre direto o teclado virtual** (`OnPreviewKeyDown` → `PadOpenKeyboard`). Os botões "TECLADO" ficam sempre escondidos (o código `SetKbdVisible` ainda existe, mas `SetPadMode` não o chama mais).
  - Verificado: campo focado + `PadOpenKeyboard` abre o teclado com o foco dentro. **Falta confirmar com o controle:** → da lista de clientes até "USAR NO EMPRÉSTIMO".
- [ ] Talvez: cursor virtual controlado pelo analógico, se o foco por D-pad não bastar nas listas longas
- [ ] Sistema no controle: navegação por foco nos botões e **teclado virtual** do console. No console, o `EditableTextBox` com foco abre o teclado nativo da plataforma. A busca é opcional, porque a lista é navegável sem digitar.
- [ ] Fechar o sistema com Esc / B (hoje é pelo botão "Sair do sistema"; no PIE, o Esc encerra o jogo)
- [ ] Trocar a caixa registradora por um computador/monitor de verdade (asset da Fab) e mover o `BP_LibrarySystem` para lá
- [ ] Talvez: histórico de empréstimos visível no sistema (os dados já ficam em `LoanDocs`/`LoanTitles`)
- [ ] Salvar cadastro e empréstimos entre sessões (SaveGame)
- [ ] Porta que abre de verdade: hoje a folha está fundida na `SM_WallwDoor01`, e o NPC surge e some do lado de dentro
- [ ] Som do sininho da porta (gancho `PlayBell` vazio, o projeto não tem sons)
- [ ] Devolução de livros (cliente traz um livro, o jogador guarda na estante)
- [ ] Reposição/estoque: hoje os livros levados somem da estante. Com o tempo, a History esvazia e o spawner passa a descartar clientes sem pedido.
- [ ] Talvez: clientes em espera olhando em volta, impaciência, ou ir embora se esperarem demais
- [ ] Animação de entregar/receber os livros (hoje eles grudam na mão `hand_r`)
- [ ] Diálogos simples

## Etapa 3 — Ciclo de dias
- [ ] Abrir e fechar a loja, contagem de clientes, transição entre dias
- [ ] Ambiente sonoro cozy (chuva, café, música)

## Etapa 4 — Inquietação (início do terror)
- [ ] Anomalias pequenas entre os dias: livro fora do lugar, luz piscando, cliente repetido
- [ ] Variações de mapa ou de iluminação (`L_Library_Night`?)

## Etapa 5 — Loop no estilo P.T.
- [ ] Corredor ou loja em loop, porta que leva de volta ao início, escalada do horror

## Etapa 6 — Personagens finais
- [ ] Trocar os manequins por MetaHumans
