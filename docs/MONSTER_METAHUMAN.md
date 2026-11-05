# MH_Monster — receita do MetaHuman monstro

Asset: `/Game/Library/Characters/Metahumans/MH_Monster` (montado e buildado em 2026-11-04, ~200 MB).
**Fora do git** (veja `.gitignore` e [SETUP.md](SETUP.md)); esta página é o que permite refazê-lo.
Feito no **MetaHuman Character** (modelo **Parametric**), sem tocar nos 9 `MH_*` das personas.

Ideia de design: **quase humano, não monstro óbvio.** Rosto neutro, encarando, de idoso desnutrido, com olhos errados e
boca torta. Serve tanto para aparição sutil quanto para o clímax (escala do terror: veja ROADMAP, Etapa 4).

## Armadilhas do editor (valem para qualquer MetaHuman novo)
- Em **Body Params** marque **Unlock Body Ranges** (multiplicador 2,5) *antes* de digitar: sem isso o Creator trava os
  valores no limite plausível (ex.: Chest 80 virou 88). Deixe **Scale Ranges by Height** ligado e defina a **Height primeiro**.
- **Masculine/Feminine negativo = feminino** (0 = masculino neutro). O corpo "virou feminino" por isso.
- O sinal "(x actual)" ao lado do campo é o valor que o modelo realmente atingiu.
- **Head Sculpt/Head Transform** são editados arrastando pontos no viewport, não têm número por região. **Desmarque
  Symmetric Manipulation** para a assimetria (o que mais incomoda no rosto). Cada ponto tem limite de plausibilidade;
  para passar disso, subir o outro lado, inclinar a cabeça inteira (Head Transform) ou o Mesh to MetaHuman.
- **Jaw Open** (aba Teeth) é só prévia: não abre a boca do personagem final.
- Depois de trocar índice de textura, o status volta a "Needs download": clique em **Download Texture Sources**.
- Cores de **Skin Tone** e **Iris** abrem uma paleta U/V (sem hex); **Tint da esclera, dentes, gengiva, cílios,
  maquiagem** abrem o color picker normal (campo **Hex sRGB**).

## Corpo (Body Params, centímetros)
Altura **205**, Muscularity e Fat no mínimo (ou abaixo, com Unlock). Proporção Gaunt: tronco comprido
(Neck to Waist ~46), pescoço longo (Neck Length ~14, Neck ~28-31), braços longos (Upper Arm ~44, Lower Arm ~38),
mãos grandes (Hand Circumference ~25), cintura/quadril finos, coxa/panturrilha finas. Cabeça com **Head Scale ~0,88**
(menor que o corpo reforça a altura). Clique em **Align Neck to Body** depois de mexer na cabeça.

## Pele (Materials > Skin)
Skin Tone pálido (canto de cima, U 0), **Face Texture Index 20** (rugas de idoso), **Body Texture Index 8**,
Roughness 0,8, **Show Top Underwear desligado**, Freckles Density 0,8 / Strength 0,6 / Saturation 0,2 / Tone Shift 1,0
(máscara densa), Palm Cavity Darkness 0,8, unhas com Tint Intensity 0,8 (cor roxo-acinzentada `2A1F2E`, não vinho).
**Accents:** baixar Redness de orelhas e nariz (ficam vermelhos demais), olheira com Lightness baixa.

## Olhos (Materials > Eyes)
Íris pálida acinzentada (a mais clara da lista), Global Saturation 0,1, **Limbal Ring Size 0,2 / Softness 0,85**
(sem o anel escuro o olhar fica morto), esclera com **Custom Tint amarelo-esverdeado `D8D08A`**, **Vascularity Intensity 0,9 /
Coverage 0,8**. Aba **Left/Right** deixa fazer os dois olhos diferentes: pupila minúscula (Dilation ~0,05) de um lado e
grande (0,6 a 1,0) do outro; cobertura de veias 0,5 num dos olhos.
**Maquiagem de olho não serve** (a máscara "Dramatic Smudge" parece guaxinim); olheira vem dos Accents.

## Dentes (Teeth & Eyelashes)
Tooth Length e Variation no máximo; Tooth Spacing, Overbite, Overjet, Polycanine, Receding Gums, Narrowness no máximo;
Worn Down 0. Em Materials: dentes `C9B98A`, gengiva `7A4A52`, placa `5B4A22` com Plaque Amount 0,8.
Boca aberta escancarada (Jaw Open na prévia) lê como cômico; fechada, com os dentes só pela fresta, assusta mais.

## No jogo: aparições (2026-11-05, em andamento)
Tudo em `/Game/Library/Blueprints/Horror/`. Atores na pasta `Gameplay/` (Director) e `Gameplay/Apparitions` (spots).
- **`BP_ApparitionDirector`** (1 na cena): só age com `BP_GameClock.GameMinutes` entre 1170 (19:30) e 1340; orçamento
  por noite = número do dia (1, 2, 3… até 5); cooldown 45–90 s. Escolhe um spot cujo `SpotOK` passe: distância entre
  `MinDist`/`MaxDist` do spot, ponto da cabeça na **visão periférica** (dot 0,35–0,9 com a câmera) e linha de visão livre
  (o raio começa 60 cm à frente da câmera, senão bate no próprio corpo do jogador). `Watch`, a cada Tick:
  aproximação olhando fixo (dot > 0,95, > 150 cm/s, < 9 m, por 0,3 s) → **apagão** (`StartBlackout` → `BlinkStep` ×14 →
  `DarkPhase` com o `DarkPP` unbound, exposição −9 → `EndBlackout`; liga/desliga as LightComponents dos atores
  `Light_*` do `L_Lighting` só em runtime); desviou o olhar e voltou → some na hora (`VanishNow`); olhou 0,35 s, chegou a
  < 4,5 m ou veio andando na direção dele sem olhar → **recuo com flicker** (`React` → `BP_Apparition.FlickRetreat`);
  9 s sem nada → some. Debug (instance editable): `bForceDark`, `ForceSpotIndex`, `bDebugLog`, `bDebugBlackout`.
- **`BP_Apparition`**: o `MH_Monster` (`BP_MH_Monster`) num Child Actor `Visual` com RelativeLocation (−4, 0, −190):
  **a origem do ator é a cabeça**, então girar/inclinar o ator gira em volta da cabeça. No BeginPlay fica invisível;
  0,1 s depois `ApplyPose` troca o Body para `ABP_MonsterPeek`, esconde as pernas (`HideBonebyName thigh_l/r`) e mostra.
  No Tick a cabeça acompanha a câmera (yaw ±`MaxTurn` 40° em volta da rotação do spot, guardada no 1º Tick).
  `FlickRetreat`: 6 passos de 50–100 ms alternando escondido/visível e andando 5+3n cm na `FleeDir` (= `EscapeDir` do
  spot, para trás do pilar), depois `Vanish`. `DebugFlickDelay` (instance editable) dispara o recuo sozinho, para teste.
- **`ABP_MonsterPeek`** (cópia limpa do `MH_ABP_Customer`): `MH_MM_Idle` → Two Bone IK na `hand_r` (alvo de mundo
  `HandTarget`) → rotação do pulso (`HandRot`, mundo) → 12 nós de dedo (`FingerCurl`). **Desligado** (nenhum spot tem
  `HandTarget`): a mão agarrando a quina não ficou boa (o IK deixava a mão no peito; o eixo de dobra dos dedos não foi
  achado). Para fazer de verdade: uma pose de "agarrar borda" feita no editor de animação.
- **`BP_ApparitionSpot`**: transform = posição e rotação da **cabeça**; `SpotKind` (0 livre, 1 jogador vindo na direção,
  2 mezanino/olhando para cima, 3 no mezanino, 4 na escada, 5 voltando para o balcão), `MinDist`/`MaxDist`, `EscapeDir`,
  `HeadZ` (0 desde que o pivô é a cabeça), `HandTarget`.
- **Spots colocados:** 3 nas quinas das gôndolas do térreo, vistas do balcão. A "quina" é um **pilar preto 20×20**
  (o 1º em X −470…−450, Y −170…−150). Os vãos vistos do balcão: X −455…−265, −45…145, 255…455 (Y −146 é a frente).
  Receita: cabeça 28 cm atrás da quina na linha câmera→quina, ~6 cm para o lado visível, roll −28° (o pescoço some atrás
  do pilar). Spot 1 em pé (−433,9; −166,2; 165), spot 2 rente ao chão (−14; −155; 45), spot 3 de cabeça para baixo
  (283,4; −149,6; 250, roll −152).

### Poses do Mixamo e fuga por caminho (2026-11-05)
- **Poses:** `/Game/Library/Characters/Anims/Mixamo/` (FBX em `Content/Library/Imports/Mixamo/`, retargetadas para `MH/MH_A_Mixamo_*` pelo `MH/RTG_AutoGenerated`). Cada spot guarda `PoseAnim` + `PoseTime` (quadro ÷ 30); o `ABP_MonsterPeek` avalia essa pose parada (Sequence Evaluator). Em uso: **Low Crawl q0** (chão) e **Running Crawl q7** (teto). Left/Right Cover Sneak foram testadas e descartadas por enquanto (o ponto 1 foi removido; refazer depois).
- **Centralizar pela cabeça:** `BP_Apparition.CenterOnHead` mede o socket `head` e desloca o visual para que a origem do ator seja a cabeça, qualquer que seja a pose.
- **Fuga em curva ("de ré"):** `FlickRetreat` liga `bFlicking`; `ReversePose` toca a animação de trás para frente a `RetreatAnimRate` (3×), `PathTurn` gira o corpo para o próximo ponto (`YawOffset` 180 = pés na frente) e `PathMove` segue `PathPts` do spot a `RetreatSpeed` (150). `ClampSurface` cola mãos/pés ao piso (`SurfaceZ`) ou, no teto (`bCeiling`), mede o teto com raio sob cada mão/pé (há luminárias penduradas). Some quando a cabeça sai da vista (`IsHidden`, depois de `MinRetreat`) ou ao fim do tempo.
- **Caminhos testados** registrando ~12 ossos por quadro (`DumpBones`, ligar `bDumpPath` + um nó `DumpBones` no fim de `CenterOnHead`) e testando cada segmento com `trace_world`: sem colisão. Medidas úteis: corredor dos spots tem ~2,3 m de fundo; teto do térreo em Z 310; piso em Z 10.
- **Sem erro de "not valid":** `Vanish` agora esconde, marca `bDying` e usa `SetLifeSpan 0.1` (destruir na hora deixava `ClampSurface`/`IsHidden` rodando num ator morto).
- **Modo de teste do Director:** `bApproachTest` alterna chão (`TestOrder` 0) → teto (`TestOrder` 1) via `TestSpawn`/`TestStage`, sem timeout e só com as regras de aproximação (< 4,5 m ou aproximando sem olhar → recua; olhar fixo + aproximar a > 150 cm/s dentro de 9 m → apagão). `bTestMode` acelera o cooldown ×12; `bStaticDisplay` mostra todos parados. Verificado no PIE com o ator `BP_ApproachDriver` (`/Game/Library/Debug/`, anda o jogador até o teto): o apagão disparou. Desligar tudo para o jogo normal: `bTestMode`, `bApproachTest`, `bStaticDisplay` e `BP_GameClock.DebugStartMinutes` = 0.

### Armadilhas encontradas
- **Ajustar pela vista do jogador**, não de perto: câmera do balcão = (−640, 170, 178) yaw 0. Para julgar sem a
  cabeça ficar minúscula, fotografar **na mesma linha** câmera→cabeça, ~170 cm antes dela.
- O Child Actor não aceita edição por instância (`cac.ExperimentalAllowPerInstanceChildActorProperties`, ligar só para
  prévia pelo campo Cmd do editor e desligar depois); `bUpdateAnimationInEditor` não é editável: AnimBP só aparece no
  **Simulate**.
- **Editar propriedade de um ator no Simulate recria o Child Actor** sem o AnimBP (a mão "sumia"). Mude no editor e
  reinicie o Simulate; variáveis da **instância de animação** (`…Body.ABP_MonsterPeek_C_0`) podem ser mudadas ao vivo.
- O `GetActorRotation` no BeginPlay voltou zerado no Simulate; por isso a rotação base é lida no primeiro Tick.
- Medidas da pose de referência (editor) não valem para a pose idle (jogo): reconferir no Simulate.
