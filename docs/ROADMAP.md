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
- [x] Converter outras estantes (2026-10-27): 24 estantes por gênero, exemplares iguais agrupados, margem para não atravessar a lateral, mais livros no meio/baixo. Script em `Tools/shelf_populate.py`. Verificado no PIE (roteiro automático): pegar um livro da S16 e guardar em outra prateleira funciona. Falta teste do usuário com teclado e as ilhas (corpo 02) continuam cenário.
- [x] Gênero de cada livro mostrado na UI e no papel do pedido, catálogo revisado pelas lombadas e histórico inicial de empréstimos (seed, devolução possível desde o início) (2026-10-27). Verificado no PIE: papel, abas LIVROS/CLIENTES/DEVOLUÇÃO e preview. Falta teste do usuário com teclado do ciclo de devolução completo.
- [ ] Gêneros novos (Poetry, Design, Informática) com placa própria: hoje só há 8 placas; os 19 títulos foram encaixados nelas (veja SCENE_MAP). Criar a arte das placas e a coluna `genre` na `DT_Books`.
- [x] Balcão → entregar o livro ao NPC (primeiro passo do ciclo de empréstimo). Veja a Etapa 2.
- [x] Migrar a tecla E para Enhanced Input (`IA_Interact`, `IMC_Library`)
- [x] Agachar (C / B, alternar; a câmera desce 50 cm suavemente)
- [x] Zoom para ler lombadas (botão direito / LT segurado, FOV 90 → 50)
- [x] **Animação de agachar** (Lyra, 2026-10-29): `ABP_Body_Library` + `ABP_FP_Library` (Alpha do `CtrlRig_FPWarp` lê `RigAlpha`). "Ficou ótimo" no teste do usuário. Detalhes e armadilhas em [ANIMATION_NOTES.md](ANIMATION_NOTES.md).
- [x] **Polimento do NPC** (2026-10-29): ombro estável com livro e "olhar em volta" na fila (`IdleBreak_Fidget/Scan`). Aprovado pelo usuário. Detalhes em [ANIMATION_NOTES.md](ANIMATION_NOTES.md).
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
  - `BP_CustomerSpawner` cria clientes a cada 180–360 s (até 3 na loja; o primeiro em 5 s).
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
  - **Sinopses:** coluna `synopsis` da `DT_Books` (19 textos curtos em pt-BR, tom cozy); `GetSynopsis(Title)` no shell chama `BP_LibrarySystem.SynopsisOf`.
  - Verificado no PIE com "Classic Poems" e "Cities".
  - **Layout do detalhe (ajuste pós-teste):** título, autor, cópias, **botão de adicionar (no topo)**, prévia (Fill) e **sinopse embaixo**, dentro de `SizeBox` (`bOverride_MaxDesiredHeight` + 150) + `ScrollBox` (`SynScroll`): sinopse longa rola em vez de estourar o painel (testado com texto de ~600 caracteres). Câmera da prévia em 3,9 × o raio, para o livro não cortar.
  - **Rolagem no controle:** o analógico direito (eixo Y) rola a sinopse (aba Livros) e o histórico (aba Clientes) via `OnAnalogValueChanged` → `ScrollContent`. Não testado com controle de verdade.
  - Ao adicionar livros novos: acrescente uma linha na `DT_Books` (nome da linha = nome da malha).
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
- [x] Devolução de livros + histórico de empréstimos (Etapa 2e, 2026-10-26):
  - **Histórico por livro** no `BP_LibrarySystem`: `HNos` (nº do empréstimo), `HDocs`, `HTitles`, `HReturned`, `HBooks` (o ator do livro). `ConfirmLoan` chama `RecordLoan`, que grava um registro por exemplar emprestado (acha o ator no balcão por título). Os antigos `LoanDocs/LoanTitles` não são mais gravados.
  - **Livros emprestados não são mais destruídos:** ao sair, o cliente chama `BP_Book.Stash` (solta da mão, oculto, sem colisão, `State 6`). `BuildRequest` agora só pede livros com `State 0`. Estoque (`BuildCatalog`) continua contando `State 0` fora do balcão.
  - **Cliente de devolução** (`BP_Customer.Mode = 1`): no `OnSpawned`, `PickReturner` (no sistema) sorteia quem tem livro em aberto e não está na loja; com chance `ReturnChance` (0,4) vira devolução (`SetupReturn`). Ao chegar ao balcão (`Arrive`), `PutReturnBooks` desoculta os livros (`Unstash`) e os coloca no balcão (`GetCounterStack` + `PlaceAt`), esperando o balcão ficar vazio. O papel mostra "DEVOLUÇÃO". `CompleteReturn` faz o cliente sair sem levar nada.
  - **Aba DEVOLUÇÃO** (`WBP_ScreenReturn`): cliente, resumo do balcão, lista de empréstimos em aberto do cliente (clique seleciona/tira) e "A devolver" (até 3); `REGISTRAR DEVOLUÇÃO` com confirmação. `ConfirmReturn` confere: cliente do balcão é de devolução e é o mesmo documento, livros do balcão = seleção = o que o cliente trouxe, e todos constam em aberto. Em Clientes há o botão "USAR NA DEVOLUÇÃO".
  - **Histórico em Clientes:** "Nº 3 · Título · em aberto / devolvido ✓" e "N registros, M em aberto".
  - O jogador guarda o livro devolvido na estante (zonas existentes): só aí o estoque volta.
  - Controle: 4 abas (LB/RB), foco, ←/→ e destaques estendidos à nova aba. **Não testado com controle/teclado de verdade.**
  - Testado por script no PIE: empréstimo → histórico → cliente de devolução → `ConfirmReturn` ok → `HReturned`. **Ainda não testado:** caminhos de erro do `ConfirmReturn` (título errado), guardar o livro devolvido e conferir o estoque, balcão ocupado na hora da devolução. Sobra `LoanDocs/LoanTitles` sem uso (remover depois).
- [x] **Pose de segurar livros nos NPCs (2026-10-26):** o `ABP_Customer` tem, entre o Slot e o Control Rig, `LocalToComponent → Transform (Modify) Bone` (`upperarm_r`, `lowerarm_r`, `hand_r`) `→ ComponentToLocal`, com o Alpha ligado à variável `HoldAlpha`. `UpdateHold` (chamada no fim do `EventBlueprintUpdateAnimation`) lê `BP_Customer.HoldingBooks` e leva o `HoldAlpha` a 1 ou 0 com `FInterpTo` (transição suave). Os três nós estão em **Replace** (espaço do osso pai), com a rotação **absoluta**, para o braço ficar fixo e não balançar com a caminhada. A rotação vem das variáveis `PoseUA`/`PoseLA`/`PoseHA` do ABP (instance editable; podem ser mexidas ao vivo no Simulate com `set_properties` em `<ator>.CharacterMesh0.ABP_Customer_C_0`): upperarm `-72,20,4`, lowerarm `-5,103,-15`, hand `-5.0,-9.9,168` (pitch,yaw,roll; roll -12 deixava a palma para baixo, +180 vira para cima). Pose final = **livros deitados sobre o antebraço/mão, na frente do lado direito do corpo** (antebraço quase horizontal, mão sob os livros). Os livros ficam presos ao **Mesh** (sem socket), com `SetActorRelativeTransform` de local `(-17, 14, 119 + 3*i)` (espaço do mesh: +Y = frente do NPC, -X = direita, z = altura do actor + 89) e rotação pitch -90 (deitados, capa para cima), sem colisão (com colisão eles empurravam o NPC, que andava de lado e travava). Vale em `HoldReturnBooks` e `TakeBooks`.
  - **Tentativa descartada (2026-10-26): livro no peito (como a foto da moça).** O manequim é largo e o braço é uma pose única por cima da animação, então a mão e o livro entravam no peito. Se for retomada, precisa de um osso/IK de verdade ou de uma animação própria. `HoldingBooks` é ligado em `HoldReturnBooks`/`CompleteLoan` (`MarkHolding`) e desligado em `PutReturnBooks`. Falta: conferir com mais de 2 livros (a pilha cresce para a frente do peito) e livros de tamanhos diferentes (o pivô de cada livro foi tratado como o centro).
- [x] **Pose de segurar livros no jogador (2026-10-26, não testada em jogo):** `/Game/Library/Characters/ABP_FP_Library` é uma cópia do `ABP_FP_Copy` (CopyPoseFromMesh → **LocalToComponent → Modify Bone ×3 (Replace) → ComponentToLocal** → Control Rig), com as mesmas variáveis `PoseUA/LA/HA` e `HoldAlpha` do NPC. `UpdateHold` (no `EventBlueprintUpdateAnimation`) liga a pose quando `BP_LibraryCharacter.HeldBooks` tem itens, com transição suave. A `FirstPersonMesh` do `BP_LibraryCharacter` usa esse ABP (override de `AnimClass` no componente do filho; o template `BP_FirstPersonCharacter` não foi alterado). (Antes os livros ficavam fixos na frente da câmera.) **Como testar o jogador sozinho (feito em 2026-10-26):** um `BP_TestDriver` temporário no BeginPlay (Delay 1,5 → `PickUp` de 3 livros + `Array|Add` em `HeldBooks` do personagem → Delay 1 → `Pawn|SetControlRotation` com pitch -35) e `CaptureEditorImage` durante o PIE mostram a tela de primeira pessoa; ajuste o pulso ao vivo com `set_properties` em `BP_LibraryCharacter_C_0.FirstPersonMesh.ABP_FP_Library_C_0` (`PoseHA`, etc.). O roteiro foi removido da cena. **Correção do atravessamento ao olhar para baixo:** os offsets do `SyncHold` agora são aplicados em **eixos do mundo** (mão + `11` à frente (yaw da câmera) + `-3` à direita + `6` em Z — livro sobre a palma, borda de trás no punho (com o braço em V o antebraço sai de baixo da pilha; antes, com o antebraço horizontal, precisava de +19 a +28 e o livro voava ou o braço furava). **Causa real do "braço atravessando":** a `FirstPersonMesh` usa `FirstPersonPrimitiveType = FirstPerson` (renderização de primeira pessoa do UE 5.8, sempre na frente do mundo), e os livros eram objetos do mundo — a mão aparecia por cima mesmo com o livro geometricamente sobre a palma. **Correção:** `BP_Book.PickUp` põe o `Mesh` em `SetFirstPersonPrimitiveType(FirstPerson)` e `PlaceAt`/`Drop` voltam para `None`; assim livro e mão dividem o mesmo espaço de profundidade e o livro cobre a palma. O `TInterpTo` do State 1 no `BP_Book` agora usa velocidade fixa 45 (antes `MoveSpeed*2`), para o livro acompanhar a mão ao andar sem se desconectar) e só depois convertidos para o espaço da câmera; antes o `+13` era no eixo "para cima" da câmera e, olhando para baixo, o livro andava para a frente em vez de subir e a mão entrava nele. **Ajustes finais (2026-10-26):** livros **inclinados para o rosto** (pitch do `MakeRotator` do State 1 no `BP_Book`, de -90 para -72), braço um pouco mais baixo (lowerarm yaw 54) e **braço abaixa quando o leque (Q) está aberto** (`UpdateHold` do `ABP_FP_Library` usa `HeldBooks > 0 and not bInspecting`). **Livros seguem a mão (corrigido após o teste do usuário, em que livro e mão se separavam ao olhar para baixo):** `BP_LibraryCharacter.SyncHold` (chamada no fim do Tick) mede o `hand_r` da `FirstPersonMesh` em espaço da câmera e grava em cada livro da mão `HoldForward = x - 10`, `HoldRight = y`, `HoldUp = z + 13` (com +8 o braço atravessava os livros; com +17 a pilha saía da tela); o `BP_Book` (State 1) segue calculando a posição pelo caminho da câmera, só que agora o ponto é a mão. Ajuste fino: os offsets -10 e +13 em `SyncHold`. Valores atuais (pitch,yaw,roll): upperarm `-72,85,-55`, lowerarm `-5,85,-15` (braço em V aberto: cotovelo baixo, mão alta), hand `-5,-40,168` (palma plana e para cima: ponta dos dedos na altura do punho, polegar para fora, medido). Medidos no PIE com o jogador real, em **espaço da câmera** (a mesma base do `HoldForward/Right/Up`): a mão fica em ≈(37, 11, -29), logo abaixo dos livros em (40, 14, -22). (Primeira tentativa, `-72,20,4` / `-5,103,-15`, deixava a mão em (20, 16, -40), abaixo da tela, e o livro parecia "sem mão".) Se a pose ficar estranha na primeira pessoa, ajuste `PoseUA/LA/HA` no CDO do `ABP_FP_Library`. Como medir: variáveis `instance editable` + `DbgForce`/`DbgHand` (hand_r em espaço da câmera) lidas com `get_properties` em `BP_LibraryCharacter_C_0.FirstPersonMesh.ABP_FP_Library_C_0`; no jogador o ABP avalia sozinho, não precisa de captura. Para os livros acompanharem a mão seria preciso trocar o cálculo do `BP_Book` (State 1) para usar o `hand_r` da `FirstPersonMesh`.
- [x] **Visual do sistema em estilo Windows 95/98 (2026-10-27):** o `WBP_LibrarySystem` virou uma janela sobre fundo teal. Árvore nova: `Bg` (teal) > `WinDark` > `WinLight` > `WinFace` (cinza) > `WinBox` (VerticalBox) com `TitleBar` (azul, `TitleText` + botões decorativos `_ [] X`), `MenuBar` (Arquivo/Exibir/Ajuda, só visual), `Main` (a sidebar e o `Switcher` de antes) e `StatusBar` (`StatusLeft` "Pronto" e `StatusRight`, ainda textos fixos). O relevo vem de Borders aninhados (`WinDark` com padding direita/baixo 2 deixa a cor escura aparecer nesses lados; `WinLight` com padding esquerda/cima 2 mostra o branco). Paleta (valores **lineares**): teal `0,0.216,0.216`; cinza janela/botões `0.527`; cards `0.6`; título azul `0,0,0.216`; texto preto. Botões usam `WidgetStyle` com `RoundedBox` de raios 0 e contorno de 2 px; linhas (`WBP_Row`) são brancas e azul-marinho no hover. O papel do pedido virou diálogo (barra azul `PaperTitleBar` + fundo branco). Nenhuma lógica foi alterada, exceto `WBP_Row.HlOn` (foco do controle agora azul-claro `0.45,0.6,1`, porque o ×7 antigo não aparecia em linha branca). Sem texto-dica nos campos originais além do da busca de livros: os de `UserSearch`/`NewName`/`NewDoc` foram **recriados por palpite** ("Buscar por nome ou documento...", "Nome completo", "Documento"). **Ajustes pós-teste do usuário (2026-10-29):** (1) a **barra de menu** (Arquivo/Exibir/Ajuda) foi escondida (`MenuBar` Collapsed), pois não tinha ação; (2) o **papel do pedido não mostra mais o gênero** (`BP_Customer.BuildListText` agora gera "- Título  (Autor)"; o gênero continua nas telas do sistema, para o jogador ter que consultar lá); (3) **"(até 3)" saiu** do título "LIVROS LANÇADOS" e o " de 3" saiu do "Adicionado! Livros no empréstimo: N" (a regra de 3 livros segue valendo e a mensagem "Máximo de 3 livros por empréstimo/devolução" ainda aparece **ao tentar passar do limite**); (4) cores dos avisos mais fortes: `AddFeedback` verde-escuro, `StatusText` (Empréstimo/Devolução) e `NewStatus` laranja-escuro; (5) **Empréstimo quebrava** ao clicar em lançar (a lista `LoanItems` e o cartão eram "Fill" e as linhas vazavam por cima dos botões quando o painel de confirmação aparecia): `LoanItems` agora está dentro de uma `ScrollBox` (`LoanScroll`, Fill) e a lista rola dentro do cartão; (6) linhas (`WBP_Row`) com rótulo em largura total (`HAlign_Fill`, padding 16/10), então o "×" não fica mais sozinho numa linha; linhas desabilitadas (histórico) ficaram brancas com texto cinza em vez de verde-escuro; `HistTitle` agora quebra linha; (7) a **mensagem amarela do Virtual Shadow Map** ("One Pass Projection max lights overflow") cobria o título: `r.Shadow.Virtual.AllowScreenOverflowMessages=0` em `[SystemSettings]` do `DefaultEngine.ini` (vale ao **reiniciar o editor**, ou digitar o cvar no Cmd; o overflow em si continua no log e pode causar artefato de sombra). **Mais ajustes (2026-10-29):** (8) **campos do Novo Cadastro** com moldura escura de 2 px (`NewNameFrame`/`NewDocFrame`, Borders em volta de `NewName`/`NewDoc`), porque o campo branco sumia no painel branco; (9) **confirmação virou modal** nas telas Empréstimo e Devolução: o `ConfirmPanel` foi movido para a raiz (`Root`, Canvas) em tela cheia, escurecido (preto 55%), com a caixa no centro (`ConfirmFrame` > `ConfirmFace` > `ConfirmSize` 620 px > `ConfirmBox`) e barra de título azul (`ConfirmTitleBar`: "Confirmar empréstimo"/"Confirmar devolução"). A visibilidade continua sendo ligada/desligada pelas funções de antes; (10) **barra de título só com o X** (`BtnTitleClose`, botão real que chama `HandleBack`, o mesmo do Esc: fecha o pedido e depois o sistema). Testado por script no PIE (empréstimo com confirmação e Novo Cadastro); o modal da **Devolução** tem a mesma estrutura mas **não foi aberto em jogo**, e o X não foi clicado de verdade. **Pendente:** a `ScrollBox` da lista pode ficar baixa em telas pequenas (confira no jogo), olhar o diálogo do pedido e o teclado virtual no jogo, fontes do campo de busca ainda pequenas, `StatusLeft/Right` dinâmicos (cliente atual / nº de livros no balcão) e testar com controle.
- [x] ~~Animação de andar agachado com Mixamo (2026-10-27)~~: descartada; substituída pelo Lyra. Histórico em [ANIMATION_NOTES.md](ANIMATION_NOTES.md).
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
