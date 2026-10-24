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
