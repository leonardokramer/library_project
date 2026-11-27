# Plano da cidade (aprovado em 2026-11-27)

## A ideia do jogo completo (do usuário)
- O jogador resolve puzzles da livraria para conseguir sair dela. Lá fora há uma cidadezinha para explorar (escala pequena; o foco do jogo continua sendo os ambientes internos).
- Na cidade ele resolve puzzles fixos, escapa ou luta com os monstros e descobre a história.
- **Não linear:** ele escolhe em que casa entrar e por qual caminho ir.
- **Morreu → volta preso na livraria.** Cada forma de sair da livraria funciona **uma vez só**, e as formas são limitadas. Gastou todas → pior final.
- O que ele abriu e liberou na cidade **continua aberto** nas próximas saídas (progresso no mundo, poucos upgrades). Tipo um roguelike de terror.

## Como a geografia serve a isso
1. **Cada saída da livraria leva a uma parte diferente da cidade** (é o que dá a não linearidade):
   - porta da frente → Main Street;
   - porta dos fundos → viela atrás dos prédios (os becos ao lado da livraria);
   - janela do mezanino → escada de incêndio e telhados, descendo perto da Elm Street;
   - porão / bueiro → esgoto que sai perto do lago, ao sul.
2. **4 áreas pequenas em volta da livraria, ligadas em anel** (sempre mais de um caminho entre duas áreas):
   - **Main Street** (centro): livraria, King Wash, lojas fechadas. Rua norte–sul (Y).
   - **Elm Street** (residencial, norte): a rua transversal do cruzamento (Y 3300–4100), casas com quintais e cercas. Portões entre quintais que o jogador destrava e que ficam abertos.
   - **Igreja Sacred Pines** (leste, atrás do King Wash): a torre aparece de qualquer lugar e serve de bússola na névoa; cemitério depois.
   - **Sul:** a Main Street desce até um lago na névoa (Moose's Dock House); a escola Cedar Point fica como área futura.
3. **Limites com motivo:** água, mata fechada, rua bloqueada (cavalete, árvore caída), névoa densa. Nunca parede invisível sem justificativa.
4. **Desempenho:** cada área é um subnível próprio, carregado por distância; a livraria é o nível base. Por dentro, só o que tiver puzzle.

## Recorte da demo (o que se vê saindo pela porta da frente)
Só o lado de fora, já no lugar definitivo: cruzamento com semáforos, casas da Elm Street depois dele, torre da igreja por cima do King Wash, a Main Street descendo para o sul na névoa, a boca da viela dos fundos, cercas, árvores secas e placa de STOP. Nenhum interior.

Pacotes da Fab usados (todos da biblioteca do usuário): Meridian 1988 (King Wash, 55 Elm Street, 14 Widow Street, Sacred Pines Church; depois Moose's Dock House e Cedar Point School), Fences VOL.4, Foliage VOL.26 (bétulas secas), Signage VOL.4, Lighting VOL.5, Buildings VOL.13, Realistic Materials VOL.6.

## Estado do recorte (2026-11-27, tarde)
Feito: cruzamento da Elm Street com semáforos, 3 casas (2 na Elm Street, 1 na Main Street), trailer ao sul, cercas, névoa cinza do SH2, asfalto molhado. Falta: torre da igreja (o download da Sacred Pines foi cancelado pelo editor 2×), bétulas secas (idem), boca da viela dos fundos aberta para uma rua de trás, carregamento por distância das áreas. Medidas no SCENE_MAP ("Bairro").
