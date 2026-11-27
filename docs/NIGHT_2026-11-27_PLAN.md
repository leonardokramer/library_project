# Noite de 2026-11-26 → 27: plano de trabalho sem supervisão

Pedido do usuário (antes de dormir): enriquecer o interior, montar o exterior (vislumbre do vilarejo no fim da demo), dar realidade à fachada da livraria e, se sobrar, revisar o código dos Blueprints.

## Decisões do usuário (respondidas antes de dormir)
- Vilarejo: **cidade pequena americana, estilo Silent Hill** (anos 80/90, névoa, postes, casas de madeira).
- Pode colocar e mudar objetos (interior e exterior) **sem aprovação prévia**, deixando fotos antes/depois e a lista do que mudou.
- Autorizado: baixar pacotes da Fab (só itens dele ou grátis, nunca compra) em projetos temporários; commit e push no fim; desligar o PC no fim; apagar código/assets mortos nossos (`/Game/Library`, nunca pacotes).
- Desempenho: **vista pela janela leve** (fachadas próximas sempre visíveis, névoa escondendo o fundo, cidade longe por streaming no final). Meta ≤ +1,5 ms de GPU (RTX 2070 Super, High).

## Limite
- Reset da janela de 5 h às 04:10 (horário local) de 27/11; semanal em 12 %, reseta domingo 29/11 14:59.
- Regra: acima de ~85 % na janela, salvar e esperar o reset em segundo plano. Se o limite bater a menos de 2–3 h do reset seguinte, fechar tudo, commitar/push e desligar.

## Ordem
1. Levantar a cena de fora (fachada leste, porta, `BP_OutsideFog`, janelas) e fotos "antes".
2. Escolher e baixar pacotes da Fab (Meridian 1988 / Dekogon ruas, calçadas, postes, sinalização, fachadas) em projeto temporário; copiar só o usado para o library_project.
3. Fachada da livraria (letreiro, toldo, calçada, vitrine, Blender se precisar).
4. Rua e vilarejo em volta, névoa, luz de poste; medir GPU.
5. Interior: detalhes com fotos antes/depois.
6. Revisão de código (só se sobrar).
7. Docs, salvar, fechar Unreal limpo, commit/push, desligar.

## Acessos
- Controle de tela liberado: Epic Games Launcher, Unreal Editor, Blender 5.3, Explorador (só clique). O usuário liberou também o navegador e o uso livre do PC.
- Claude in Chrome conectado (contas do usuário logadas; Fab, uso do Claude). Se algo fugir do controle: abortar, salvar o que der, desligar.
- Economizar token, mas priorizar a beleza do resultado (ser criterioso). Downloads da Fab pelo Epic Launcher (já aberto e logado).
- Crash do editor: fechar o Crash Reporter, `Start-Process library_project.uproject`, conferir o diálogo de restaurar pacotes (nada do Stationer), retomar do último save. Dois crashes seguidos na mesma coisa = pular a tarefa e anotar.

## Pacotes da biblioteca Fab (conferidos em 27/11, todos já do usuário)
- **Casas/prédios:** Meridian 1988 — 55 Elm Street (VOL 21), 14 Widow Street (VOL 31), King Wash Stripmall (VOL 55), Sacred Pines Church (VOL 12), Cedar Point School (VOL 57), Moose's Dock House (VOL 1). City Sample Buildings (Epic; grande, evitar).
- **Rua:** Buildings VOL.13 Sidewalks, Realistic Materials VOL.6 Roads & Sidewalks, Decals VOL.2 Roads and Streets, Road Cracks VOL., Roadside Construction (Megascans).
- **Luz e fachada:** Lighting VOL.5 Exterior Lights, Buildings VOL.2 Electric & Air (postes de fiação, ar-cond.), VOL.3 e VOL.15 Attachments, VOL.9 Pipes & Gutters, VOL.12 Town Doors, VOL.16 Flower Beds.
- **Placas:** Signage VOL.3/VOL.4 Small Town, VOL.5 Letters (letreiro).
- **Carros:** Vehicles VOL.4 e VOL.7 Retro Cars.
- **Vegetação:** Foliage VOL.26 Dead Birch, VOL.28 Ash Trees, VOL.13 Southern Oak, VOL.19 Scraggly Bushes, VOL.22 Wild Grass, VOL.23 Ivy.
- **Cercas:** Fences VOL.4 Old Fences, Fences and Gates VOL.3.

## Autorizações explícitas extras (00:20)
- Push e `shutdown` autorizados explicitamente pelo usuário no chat.
- Diálogo "Substituir arquivos" do Launcher: responder "Sim, substituir" (pacotes da Dekogon dividem pastas; é só o projeto de staging).
- No fim: apagar o projeto `FabStaging` inteiro e o cache de downloads do Launcher (o usuário pediu; os pacotes são pesados).

## Diário
- 00:00 — permissões, lista de pacotes. (Horário local = UTC−4; o reset é às 03:10 local.)
- 00:12 — projeto vazio `Unreal Projects/FabStaging` (5.8) criado; 14 pacotes na fila do Epic Launcher para ele (Meridian 55 Elm / King Wash / 14 Widow, Lighting VOL.5, Sidewalks VOL.13, Roads Materials VOL.6, Signage VOL.3/4, Retro Cars VOL.4, Dead Birch VOL.26, Electric & Air VOL.2, Old Fences VOL.4, Attachments VOL.15/VOL.3). O launcher baixa um por vez; pausar um passa para o próximo. **55 Elm Street ficou pausado (retomar).** Esperando o reset.
- 03:15–04:40 — cidade de fora montada e medida (detalhes no SCENE_MAP, "Rua e vilarejo"):
  King Wash (cópia enxuta `L_Town_StripMall`) do outro lado da rua; rua/calçadas/meio-fio (`L_Library_Street`);
  fachada nova no Blender (cornija, pilastras, faixa "PUBLIC LIBRARY", toldo, caixa de devolução); lanternas,
  holofotes do letreiro, 5 postes com luminária; hidrante, banca, banco, lixeira, placa; vizinhos (loja fechada
  ao norte, térreo ao sul) com becos; névoa estilo Silent Hill (volume local + paredes de névoa a ~55 m).
  Desempenho (vista do balcão para as janelas, High): 14,2 ms sem a cidade → 16,5 ms com (+2,2 ms) depois de
  apagar 1.008 objetos internos do King Wash, 53 decalques, sombras das luzes e do strip mall, vento da vegetação.
  Crash 1x: duplicar mapa + abrir na mesma chamada (vazamento de mundo). `open_application` do Unreal abre outra
  instância: não usar.
- 04:40–04:55 — letreiro trocado para "LANTERN & LETTERS" (nome da placa da porta); carrinho de devolução e capacho
  na entrada; 3 carros e 21 fios entre os postes; cliente testado entrando pela porta nova (ok); 72 Blueprints
  compilam sem erro; M_BulbGlow e M_OutsideGround (documentados sem uso) apagados; fluxo normal conferido
  (`check_flow.py`); commit `3fbf61c` + push.
- Limpeza: downloads cancelados; pacotes novos enxutos de 33 GB para 12 GB (`Tools/pack_deps.py` + `pack_trim.ps1`,
  editor reaberto sem nenhuma referência quebrada); projeto `FabStaging` (34 GB) e cache do Launcher (49 GB) apagados.

## Tarde de 2026-11-27 (usuário saiu de novo)
Autorizado no fim: commit e push, fechar o Unreal, desligar o PC, **manter o `WalkOutTest_TEMP` na cena** para o teste dele.
Tarefa: recorte da demo do [TOWN_PLAN.md](TOWN_PLAN.md) (casas da Elm Street, igreja, sul na névoa, viela, cercas, árvores, STOP).
Feito: 3 casas + trailer, cruzamento com semáforos em cabo fixo, cercas, gramado, calçadas depois do cruzamento, STOP (Blender; o pacote de placas não tem STOP), névoa cinza estilo SH2 (`EmissiveDay` 0,3), asfalto molhado. Não feito: igreja e bétulas (o Fab do editor cancela a fila quando um download termina; baixar um por vez), carregamento por distância. 17,4 ms na vista do balcão. Pacotes novos (55 Elm, 14 Widow, FENCES, SIGNAGE) ficaram inteiros (interiores servem para os puzzles depois).

## Para o usuário testar / decidir
- Fotos em `Saved/NightPhotos` (antes/depois da fachada e da entrada, rua de dia e de noite).
- Andar lá fora (calçada e rua) e olhar pela janela em horários diferentes; dizer se a névoa está densa demais ou de menos.
- Custo: +2,2 ms de GPU. Se pesar, dá para trocar o King Wash por cartões (impostores) ou carregá-lo só no final.
- O carrinho de devolução está vazio (livros decorativos confundiriam com os interativos). Pode virar parte da reposição.
- Não feito: casas do Meridian ao longe (downloads de 16–20 GB cada estavam lentos; cancelados), árvores secas, revisão
  profunda dos Blueprints (só auditoria: compilação limpa e assets mortos).
