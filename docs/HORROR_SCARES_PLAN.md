# Plano dos sustos: *The Mortuary Assistant* → biblioteca

Escrito em 2026-11-06 a partir da análise quadro a quadro de 6 trechos do vídeo
[The Mortuary Assistant jumpscares](https://www.youtube.com/watch?v=NKyn91Vs75Y), escolhidos pelo usuário.
**É para ser implementado em várias sessões, possivelmente por outro modelo.** Nada daqui foi implementado ainda.

**Leia antes de começar:**
- [MONSTER_METAHUMAN.md](MONSTER_METAHUMAN.md): como o monstro, o `BP_ApparitionDirector`, o apagão e a entrada andando funcionam hoje.
- [MCP_WORKFLOW.md](MCP_WORKFLOW.md): armadilhas do `write_graph_dsl`.
- [SCENE_MAP.md](SCENE_MAP.md): coordenadas.
- [ANIMATION_NOTES.md](ANIMATION_NOTES.md): MetaHumans, retarget, Child Actor.
- A seção "Onde paramos" do `CLAUDE.md`.

Status das fases: ☐ a fazer · ◐ em andamento · ☑ feito. **Atualize aqui ao terminar cada fase.**

---

## 0. Regras que valem para todas as fases
- **Projeto só Blueprint.** Tudo novo vai em:
  - `/Game/Library/Blueprints/Horror/` (BPs e ABPs);
  - `/Game/Library/Materials/Horror/` (materiais);
  - `/Game/Library/Characters/Anims/Mixamo/` (animações).
- **Não edite:** `/Game/Stationer`, `L_Lighting` e os pacotes de terceiros. A luz do `L_Lighting` só recebe comandos em runtime; **nunca salve alteração nela**.
- **Antes de colocar qualquer ator na cena:** proponha o lugar com coordenadas e **fotos da vista do jogador** (antes e depois) e espere o usuário aprovar.
  - Faça os ajustes de posição **com a cena parada**; use o Simulate só quando precisar de animação.
  - Câmera do balcão: (−640, 170, 178), yaw 0.
- **Funções pequenas no DSL:**
  - o `if` encerra o fluxo;
  - o `Sequence` só tem `then_0/then_1` (aninhe);
  - o getter de bool se escreve sem o `b` (`Variables|Default|GetX`);
  - o `LineTraceByChannel` precisa de `(bind (_outhit _bool) ...)`;
  - não há módulo (use `select`);
  - depois de reescrever uma função, confira os nós soltos.
- **`ActorTools.set_actor_transform` zera o que não for passado:** mande sempre location + rotation + scale.
- **Não apague assets pelo MCP logo depois de um PIE.**
- **Teste sozinho antes de pedir ao usuário.** O `BP_ScenDriver` (`/Game/Library/Debug/`) segura e vira o jogador e loga `[SD]`; o log fica em `Saved/Logs/library_project.log`. Remova os atores temporários no fim e rode `save_assets` ao fim de cada fase.
- **Docs:** a cada fase, atualize o [MONSTER_METAHUMAN.md](MONSTER_METAHUMAN.md) (o que foi feito, valores, armadilhas) e o status aqui.
- **Antes de mandar para testadores, desligue:** todas as flags `bTest*`/`bDebug*` novas, além das já listadas no `CLAUDE.md`.

## 1. O que o vídeo mostra e a adaptação

| # | Trecho | O que acontece no vídeo | Por que funciona | Na biblioteca |
|---|---|---|---|---|
| A | 0:28–0:43 | Mulher de costas na pia de um banheiro escuro. Em 0:32,4 a câmera passa por ela, que **anda de ré muito rápido**: ~1,5 m em ~0,3 s (de 32,5 a 32,75 já saiu do quadro). Em 0:33 já está parada no canto, **braço esticado apontando** para um depósito escuro. Fica ali enquanto o jogador entra; de perto (0:38) o cabelo cobre o rosto e a mão aponta. Depois o jogador acha a pista (uma foto no espelho). | Movimento humano reconhecível (andar de ré), mas rápido demais e um pouco "pulado". O gesto dá uma ordem ao jogador. | Monstro de pé perto de um **livro bizarro**; recua de ré acelerado e **aponta para o livro**, parado e com a cabeça baixa. |
| B | 0:53–1:00 | Sala clara. Num **vão estreito e escuro entre um armário de parede e a parede**, à altura da cabeça, aparece **só um rosto** (pálido, olhos pretos, cabelo escuro) entre 0:56,0 e 0:56,4, enquanto a câmera passa. Em 0:56,4 já está meio escondido; depois some. | O vão não cabe um corpo. Só a cabeça, no escuro, vista de relance na periferia. | **Rosto num canto escuro** (vão entre estante e parede/pilar), só a cabeça. |
| C | 1:00–1:10 | Porta aberta para um cômodo **totalmente preto**. No batente, deslocado para um lado, um rosto pálido mal visível (1:03). Depois some. Quando o jogador chega à porta (1:09), leva um **empurrão** e cai (tela preta em 1:10). | Escuro absoluto: o olho procura e acha só o rosto. A punição vem quando o jogador já relaxou. | **Parado numa passagem escura**, some e depois **empurra** o jogador, que cai. |
| D | 2:20–2:35 | Figura parada no corredor, no caminho do jogador (2:26). O jogador avança e **atravessa o corpo** (sem colisão). Colado nela, a **cabeça vira de sopetão** para ele (2:31,8) e **todas as luzes apagam** (2:32,5, preto total). | Quebra a regra "ele foge quando você chega". A virada de cabeça é o único movimento. | **Parado na escada**, sem colisão; virada de cabeça brusca e apagão; quando a luz volta, não tem nada. |
| E | 5:30–5:50 | Corredor comprido, ela parada **no fim** (5:39). O jogador anda até lá; ela fica (5:43–5:46), então **anda de ré e vira na curva** do recuo do fundo (5:46,5). Em 5:47 o recuo está vazio, e é raso demais para caber alguém. | O espaço não comporta, mas ela some ali mesmo. | **Fim de um corredor entre estantes**: recua de ré e some atrás da quina. |
| F | 5:50–6:00 | O jogador vai até o fim sem saída, olha a parede e vira; no canto aparece uma **mão** (5:57,6). Segundo o usuário, ao virar, o bicho está bem na frente. | Ele estava atrás o tempo todo. | Num **beco sem saída**: ao virar, o monstro está a ~1,3 m; **apagão absoluto** e, quando a luz volta, nada. |

**Ponto em comum de B, C, E e F: a área do bicho está MUITO escura.** A biblioteca hoje é clara demais, mesmo com as luzes apagadas. Por isso a **Fase 0 (escuridão) é pré-requisito** de quase tudo.

## 2. Por que a cena não escurece (medido no editor em 2026-11-06)
Valores lidos do `L_Lighting`. **Não edite; servem de referência.**
- **`SkyLight_1`:** **Intensity 2,0** no editor (de dia), Stationary, cubemap fixo. À noite o `BP_GameClock` já o baixa para 0,2 (ver 2.1).
- **`PostProcessVolume_1`** (unbound):
  - `AutoExposureMethod` Histogram com **Min = Max Brightness = 1**: a exposição é fixa, e isso é bom (o olho não "se acostuma" com o escuro);
  - `AutoExposureBias` **+1**;
  - **Local Exposure Bilateral com `ShadowContrastScale` 0,8**, que clareia as sombras;
  - vinheta 0,4, grão 0,3, bloom FFT, `bMegaLights` ligado.
- **Luminárias:** ~40 atores `Light_02/04/05/06/07/WIP_C_*`, cada um com as malhas `Lamp_01..03` e 1 a 3 `SpotLight`.
- **Sol:** o `DirectionalLight_0`; o `BP_GameClock` já o gira e baixa à noite.
- **Apagão atual** (`BP_ApparitionDirector.StartBlackout`/`DarkPhase`): usa o `DarkPP` próprio (unbound, exposição −9) e desliga as `LightComponent` dos `Light_*`. Dá preto total, mas é global e não serve para "um canto escuro".

### 2.1 Teste feito no PIE em 2026-11-06 (21:00, dia 1, vista do balcão; só em runtime, nada salvo)
Fotos em [img/scares/](img/scares/).

**Inventário das luzes** (68 componentes em 40 atores, todos com `IntensityUnits` Unitless):

| Atores | Componentes | Intensidade | Raio | Altura (Z) |
|---|---|---|---|---|
| `Light_04_C_*` (13, pendentes) | 3 `SpotLight` cada | 1000 | 300 | 313 (térreo) ou 800 (mezanino) |
| `Light_07_C_1` | 3 `SpotLight` | 1000 | 300 | 320 |
| `Light_02_C_*` (11, calhas) | 1 `RectLight` cada | 5000 | 400 | 682 (mezanino) |
| `Light_WIP_C_*` (6) | 1 `RectLight` cada | 5000 | 400 | 310 (térreo) |
| `Light_06_C_*` (6) | 1 `PointLight` cada | 2000 | 350 | 632–636 |
| `Light_05_C_*` (3) | 1 `PointLight` cada | 4000 | 350 | 338 |

Os raios são curtos (3–4 m), por isso **zonas locais funcionam**. Use distância **3D** (ou uma caixa com Z): luzes do térreo ficam em Z 310–340 e as do mezanino em Z 630–800. Com distância só em XY, apagar uma área do térreo apaga também o mezanino em cima.

**Resultados:**
1. **`f0_21h_atual.png`:** às 21:00 a loja está tão clara quanto de dia.
2. **O SkyLight não é o culpado:** o `BP_GameClock` **já baixa o `SkyLight` para 0,2 à noite**, e baixar mais quase não mudou a foto. **Não** é preciso mexer no SkyLight.
3. **`f0_21h_bias0.png`:** `AutoExposureBias` **0** (hoje +1) + `LocalExposureShadowContrastScale` **1,0** + vinheta **0,65** é **o ponto de partida recomendado para a noite**. A loja fica sombria, os cantos escuros, e o balcão, o cliente e o computador continuam legíveis.
4. **`f0_21h_bias-1.5.png`:** com bias −1,5 fica escuro demais para trabalhar no balcão. Serve como alvo de "noite avançada" nos dias finais, ou durante um susto.
5. **`f0_21h_tudo_apagado.png`** (as 68 luzes com Intensity 0, bias 0):
   - fica escuro, e o cliente vira **silhueta** (ótimo efeito para usar depois);
   - mas **sobra luz dos materiais emissivos**: as calhas, os bulbos das pendentes e as fitas das prateleiras continuam brilhando e iluminando em volta pelo Lumen.
   - Para um canto ficar preto de verdade, **o emissivo das luminárias também tem que apagar** (0.1).
6. **`f0_21h_zona_escada.png`:** apagando só as 9 luzes a < 450 cm em XY de (−400, 330), a **escada e o canto do balcão ficam quase pretos**, e o resto da loja segue aceso. O efeito de "área escura" que os sustos pedem funciona.
   - Efeito colateral: o balcão fica sem luz própria. O jogador precisa de uma luz no balcão (a luminária laranja com uma `PointLight` nossa) para a zona da escada não "desligar o trabalho".
   - As 9 luzes, da mais próxima para a mais longe: `Light_04_C_11`, `_04_C_12`, `_06_C_5`, `_02_C_9`, `_WIP_C_0`, `_05_C_2`, `_02_C_6`, `_06_C_6`, `_04_C_4`.

**Como o teste foi feito** (para repetir): PIE com `DebugStartMinutes` 1260. `ObjectTools.set_properties` nos atores do mundo PIE: `/Game/Stationer/Levels/UEDPIE_0_L_Lighting.L_Lighting:PersistentLevel.<ator>.<componente>` com `{"Intensity": x}` e, no `PostProcessVolume_1`, `{"Settings":{"bOverride_AutoExposureBias":true,"AutoExposureBias":0,...}}`. Para ver o resultado, `CaptureEditorImage`. O `ProgrammaticToolset.execute_tool_script` faz o laço nas 68 luzes de uma vez. Ao parar o PIE tudo volta; confira depois que o `SkyLight` do editor continua 2,0.

## 3. Fases (ordem recomendada)
Cada fase termina com: teste próprio no PIE, fotos, `save_assets`, docs atualizadas e um pedido de teste ao usuário.

### Fase 0 ☑ (núcleo pronto, aprovado pelo usuário em 2026-11-09; faltam só 2 itens que dependem de outras fases)
**Feito e aprovado:** `BP_LightRig` (zona por caixa, fade, flicker, `Blackout`, `RestoreAll`, emissivo apagando junto), noite global (`NightPP` com bias 0,35 / shadow 0,85 / vinheta 0,6), luminárias acesas à noite (balcão e mezanino), escada menos escura via pendentes reais (`StairBoost`) e fog volumétrico atenuado (`VolScatter`). Tudo em MONSTER_METAHUMAN.md ("Fase 0 de escuridão") com valores e armadilhas.
**Fica para depois, quando uma fase precisar:** (a) `BP_DarkZone` + `M_DarkVoid`/`M_DarkVoidFade` (0.3), a criar junto da Fase 2 (B, rosto no canto) com plano + fotos do lugar; (b) `FaceLight` (0.4), na Fase 1 com o `BP_MonsterStand`. (c) Migrar o Director (`StartBlackout`/`ChargeFlicker`/`IdleTick`) para o `BP_LightRig` (hoje o Director usa a própria lista de luzes e religa tudo com `Light_` no nome, inclusive as luzes de luminária).
**Regras que o usuário reforçou:** toda luz nova precisa de fonte visível (luminária); nunca uma luz avulsa. **Próximo:** Fase 1 (infraestrutura: monstro em pé, `BP_ScareManager`, pose de apontar).

**Objetivo:** à noite a loja fica mais escura de verdade, e certas **zonas** podem ficar quase pretas sob comando, sem mexer no `L_Lighting`.

**0.1 `BP_LightRig`** (ator novo, 1 na cena, pasta `Gameplay/`): centraliza o comando das luzes.
- **`BeginPlay`:**
  - Ache as luzes **com a mesma lógica que o Director usa hoje** (reaproveite): atores cujo nome começa com `Light_`, ou os que têm `SpotLightComponent`/`PointLightComponent`.
  - Guarde por componente, em arrays paralelos: `LightComps[]`, `LightBase[]` (intensidade original) e `LightOwner[]`.
  - Guarde também as malhas emissivas das luminárias (`Lamp_*` e as malhas dos `Light_02`/`Light_WIP`) e os materiais originais, para o apagar/acender do emissivo.
  - O `SkyLight` fica com o `BP_GameClock`; o LightRig não mexe nele.
- **Funções:**
  - `SetLightScale(Comp, Scale)` → `SetIntensity(LightBase[i] * Scale)`.
  - `ZoneLights(Center, Extent, Scale, FadeTime)`: escala só as luzes **dentro da caixa** (pela posição do componente). O fade roda no Tick (lista `Fades[]` com alvo e velocidade); com `FadeTime` 0 é instantâneo.
  - `AllLights(Scale, FadeTime)`.
  - `FlickerZone(Center, Extent, Duration, Chance)`: liga e desliga aleatoriamente (mesma ideia do `ChargeFlicker` do Director).
  - `Blackout(Duration)`: tudo apagado + `DarkPP.BlendWeight` 1 (exposição −9), sem piscar. Ao fim, restaura e dispara `OnLightsBack`. **Reaproveite o `DarkPP` do Director** (por referência) ou crie um igual; só um pode estar ativo.
  - `RestoreAll()`.
- **Zonas por distância 3D** ou caixa com Z (ver 2.1: térreo Z 310–340, mezanino Z 630–800).
- **Lâmpadas acesas sem luz: obrigatório** (confirmado no teste 2.1). Com a luz apagada, o vidro (`Lamp_01..03` e as malhas das calhas `Light_02`/`Light_WIP`) continua emissivo, brilha e ainda ilumina em volta pelo Lumen. Confira o material dessas malhas:
  - se tiver parâmetro de emissivo, use `SetScalarParameterValueOnMaterials` em runtime;
  - senão, troque o material em runtime por um `MI_LampOff` (cópia escura em `/Game/Library/Materials/Horror/`) e devolva o original ao religar.
  - Isso **nunca** é salvo no `L_Lighting`.
- **Depois**, num passo separado e só com o LightRig já testado: migrar o Director para usar o `BP_LightRig` (`StartBlackout`, `ChargeFlicker`, `IdleTick`), para não haver dois donos das luzes.

**0.2 Noite mais escura (global).** `PP_Night` é um `PostProcessVolume` **nosso** no `L_Library`: unbound, `Priority` 5 (acima do `PostProcessVolume_1`; o `DarkPP` fica com prioridade maior ainda). O `BlendWeight` é controlado pelo `BP_GameClock`: 0 até 19:00, subindo até 1 às 20:00.

Overrides (testados no PIE, ver 2.1):
- `AutoExposureBias` **0** (hoje +1). Nos dias finais, pode descer até −0,75. Com −1,5 o balcão fica escuro demais. Mantenha Min = Max Brightness (exposição fixa).
- `LocalExposureShadowContrastScale` **1,0**, para parar de clarear as sombras. O `HighlightContrastScale` 0,8 pode ficar.
- `VignetteIntensity` **0,65**; `FilmGrainIntensity` 0,35–0,45 (este não foi testado).
- Opcional (não testado): leve dessaturação e tom frio, com `ColorSaturation` 0,85 e `WhiteTemp` 6500 (hoje 8000).
- **SkyLight: não mexer.** O `BP_GameClock` já o deixa em 0,2 à noite, e baixar mais não muda nada.
- **Luz do balcão:** uma `PointLight` nossa na luminária laranja `Prop_DeskLamp_1` (−712, 137,5, 114): intensidade baixa, quente, raio ~250. Assim o trabalho continua possível quando a zona da escada apaga (2.1, foto da zona).

**Teste:**
- Defina `BP_GameClock.DebugStartMinutes` 1260 (21:00) **no editor, antes do PIE**.
- Tire fotos da vista do balcão, do corredor central, da escada e do mezanino, com e sem o `PP_Night`, e peça ao usuário para aprovar o nível.
- Cuidado: escuro demais atrapalha o trabalho no balcão (o computador e o papel do pedido precisam ser legíveis). A luminária laranja do balcão pode ganhar uma `PointLight` própria (ideia antiga do ROADMAP: estado de luz acesa).

**0.3 Zonas escuras (`BP_DarkZone`):** um ator com `Box` (a área) + uma lista de "vãos".
- Ao ativar, chama `LightRig.ZoneLights(Box, 0..0,15, 0,5 s)`.
- **Material de vazio:**
  - `M_DarkVoid`: Unlit, cor preta, Opaque;
  - `M_DarkVoidFade`: variante Translucent com `DepthFade`, para a borda não ficar dura;
  - vai numa malha simples (`/Engine/BasicShapes/Plane` ou `Cube`) posta **atrás** de um vão ou de uma porta, para o fundo virar preto absoluto;
  - fica escondida (`SetHiddenInGame`) com a zona desligada;
  - use só onde o usuário aprovar. Num vão fino ela não aparece, porque preto contra escuro não se destaca.
- Uma zona fica "armada" só enquanto um susto que depende dela está ativo, e volta ao normal depois. A troca nunca acontece na frente do jogador: só com a zona fora da vista (dot < 0,3) ou durante um apagão/piscar.

**0.4 Luz do rosto (`FaceLight`).** No ator do monstro (Fase 1), um `SpotLightComponent` pequeno preso ao socket `head`, ou a ~40 cm à frente do rosto apontando para ele.
- Intensidade baixa, raio de 60–90 cm, sem sombra, cor fria levemente esverdeada.
- Serve para o rosto pálido "aparecer" no escuro, como no vídeo (B, C).
- É ligada por susto, com fade.

**Pronto quando:**
- à noite a loja está visivelmente mais escura e ainda jogável;
- `ZoneLights` deixa um canto quase preto sem afetar o resto;
- `Blackout` dá preto total e restaura;
- nada foi salvo no `L_Lighting`.

### Fase 1 ☑: Infraestrutura (concluída em 2026-11-09, aprovada pelo usuário) (monstro em pé, gerenciador, animações, pose de apontar)
**Estado (2026-11-09):** os 4 BPs novos existem, compilam e estão salvos: `ABP_MonsterStand`, `BP_MonsterStand`, `BP_Scare`, `BP_ScareManager` (+ `BP_ApparitionDirector` com `ScareBusy`/`FindMgr` no `IdleTick`). Todas as funções do `BP_MonsterStand` estão escritas (incluindo `WalkPath`/`WalkStep`, `GroundSnap`, `SnapLook`, `IsSeen`, `HeadVisible`, `MeasureStart/Step`). **Testado no Simulate** (ator temporário em (−300, 215), já removido): calibração (`TestDot` 1,0; `FwdC` +Y, `RightC` −X, `UpC` +Z), pose parada, apontar (braço estendido para o alvo, conferido em foto de perfil), andar de ré por caminho, só-rosto + `FaceLight` + olhar. **Fechamento:** mão do Mixamo descartada, dedos calculados; apontar aprovado pelo usuário em jogo; `ScareManager` colocado em `Gameplay/` (−600, 170, 100) e testado no Simulate (armou um `BP_Scare` temporário, `bBusy` true, Director sem spawn enquanto ocupado, regra do cliente no balcão confirmada). O que segue abaixo é histórico do que faltava na época: olhar a mão de perto (indicador esticado e dedos fechados do Mixamo; escuro demais nas fotos, o usuário vai conferir), cabeça baixa (`NodDeg` 1, modo 6, só numérico), clipe a rate 3/15 fps (modo 2, só rodou sem foto), `VClip` confiável (medição dá 290–340 cm/s, suspeita; o teste de andar usou 210), o critério numérico completo do 1.6, teclas 5–0 com `bScareTest` e um susto filho real (Fase 2). Detalhes e armadilhas em MONSTER_METAHUMAN.md ("Fase 1").
**1.1 Animações.** O usuário baixa do Mixamo, como já fez antes.
- **Formato:** "Without Skin", 30 fps, FBX em `Content/Library/Imports/Mixamo/`; nas caminhadas, **In Place**.
- **Pipeline:** importar com o `SK_Mixamo` e retargetar com o `MH/RTG_AutoGenerated` para `MH/MH_A_Mixamo_*` (mesmo caminho das poses de rastejar; receita em MONSTER_METAHUMAN, "Poses do Mixamo").
- **O que baixar:**
  - **Empurrão com as duas mãos** (usado em C). Pesquisado no Mixamo em 2026-11-06:
    - os resultados de "Push" são empurrar caixa ou objeto andando;
    - os de "Shove" são só reações (quem leva o empurrão);
    - "Zombie Attack" e "Knock Off Assailant" não servem.
    - **Escolhida pelo usuário: "Standing 2H Magic Attack 03"** (129 quadros a 30 fps, ~4,3 s). Recolhe as mãos e lança **os dois braços retos para a frente**, que é exatamente o golpe. Quadros medidos na prévia do Mixamo:

      | Quadro | Pose |
      |---|---|
      | 1 | parado, braço levemente à frente |
      | 14 | mãos recolhidas perto do rosto |
      | 25–28 | mãos no alto, ao lado da cabeça (**pico do preparo**) |
      | 30 | braços já vindo para a frente |
      | 33 | quase esticados |
      | **34–36** | **braços totalmente esticados (contato)** |
      | 36–90 | segura os braços esticados |
      | 105 | recolhendo |
      | 129 | volta ao parado |

    - **Trecho a usar:** do **quadro 22** (fim do recolher; tempo 0,73 s) ao **quadro 45** (1,50 s). Contato no **quadro 35** (1,17 s).
      - A rate 1,0, o golpe (28 → 35) leva 0,23 s, que já é seco. Com rate 1,2–1,4, o preparo fica mais curto.
      - O `KnockDown` dispara quando `PoseTime` ≥ 1,17 s. Depois do 45 o clipe não interessa: o corte para o preto acontece antes.
    - Baixe o clipe **inteiro** (Trim 0–100): o recorte é feito no Unreal pelo `StartTime`/`EndTime` do `PlayClip`.
  - **☑ Importadas e retargetadas em 2026-11-06** (conferido pelo MCP):
    - FBX em `Content/Library/Imports/Mixamo/Push.fbx` e `Pointing.fbx`;
    - `A_Mixamo_Push`/`A_Mixamo_Pointing` (esqueleto `SK_Mixamo_Skeleton`);
    - `MH/MH_A_Mixamo_Push` (4,30 s = 129 quadros) e `MH/MH_A_Mixamo_Pointing` (2,77 s = 83 quadros), ambas no `metahuman_base_skel`, sem root motion, com 342 trilhas de osso (inclui os dedos).
    - O editor de animação avisa que o corpo MH roda o post-process `ABP_Body_PostProcess` (corretivos e torções): os ossos `*_twist`/`*_corrective` são resolvidos por ele, então **não** os gire à mão.
    - Dedos do `MH_A_Mixamo_Pointing` **conferidos pelo usuário**: o indicador fica esticado depois do retarget. O caminho principal do passo 4 da 1.6 (a mão do Mixamo) está liberado.
    - **Reserva 1:** "Release Hostage – Villain": no fim (≈ quadro 34 de 52) ele empurra o refém com as duas mãos. Use só esse trecho.
    - **Reserva 2:** "Standing 2H Magic Attack 02" (as duas mãos para a frente, mas com avanço do corpo).
    - No Mixamo, ajuste o `Character Arm Space` se as mãos se cruzarem no corpo magro do monstro.
  - Opcional: um idle "parado esquisito" ("Zombie Idle", ou "Standing Idle" com a cabeça baixa) para D e E. Sem ele, use `MH_MM_Idle`.
- **Apontar:** o corpo **não** vem de animação, porque todas as de apontar do Mixamo mexem demais o corpo. O braço e a cabeça são **calculados** (seção **1.6**). **A mão vem do Mixamo:**
  - Animação **"Pointing"**: de pé, braço direito para a frente, 83 quadros. Na busca "pointing" é a 3ª da 2ª linha; há várias com o mesmo nome. A certa tem o indicador esticado e os outros dedos fechados entre os **quadros 20 e 35** (conferido de perto no quadro 22).
  - Usamos **um quadro só (25, tempo 0,83 s) e só os ossos dos dedos**, misturados por cima da pose (1.6, passo 4). Com isso a mão fica natural e a parte mais arriscada da conta (dobrar os dedos) deixa de ser necessária.
  - A dobra calculada dos dedos fica como plano B.
- **Já existe, no esqueleto MH** (`/Game/MetaHumans/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel`, o mesmo do `MH_Monster`): `MH_MF_Unarmed_Walk_Bwd` (2,13 s, com root motion; amostra de **150 cm/s** no `MH_BS_Idle_Walk_Run`), `_Bwd_Left/_Right` e `MH_MF_Unarmed_Jog_Bwd` (amostra de 600 cm/s), em `/Game/Library/Characters/Metahumans/`. São a base do "andar de ré acelerado".

**1.2 `ABP_MonsterStand`:** cópia do `ABP_MonsterPeek`, que já avalia `PoseAnim`/`PoseTime` num Sequence Evaluator. Acrescentar:
- **Tempo em degraus:** o `PoseTime` é calculado no BP (1.3); o ABP só o avalia.
- **Cabeça:** `Transform (Modify) Bone` em `neck_02` e `head`, com rotação somada (Add to Existing, Component Space) e as variáveis `RotLookNeck`, `RotLookHead` e `LookAlpha`. Calcule as rotações no BP com a mesma técnica da 1.6.
  - Confira no Simulate se o rosto (`Face`) acompanha: no MetaHuman o rosto segue a pose do corpo.
  - Se não acompanhar, aplique em `neck_01`.
- **Nós da pose de apontar** (1.6), depois do Evaluator e antes do olhar.
- Desligar o IK da mão herdado (ou deixar o Alpha em 0).

**1.3 `BP_MonsterStand`.** Ator novo; **não** reaproveite o `BP_Apparition`, que é feito para espiar rastejando e tem a origem na cabeça.
- Raiz = pés (origem no chão). Child Actor `Visual` = `BP_MH_Monster`, o mesmo do `BP_Apparition`. Mantenha a troca de asset fácil, porque o usuário pode trocar o monstro.
- **`BeginPlay`:**
  - começa invisível;
  - após 0,1 s, `ApplyAnim` troca o Body para o `ABP_MonsterStand`, **desliga toda a colisão** (`SetCollisionEnabled NoCollision` no Body, Face, cabelo, roupas e na raiz) e mostra;
  - `VisibilityBasedAnimTickOption = AlwaysTickPoseAndRefreshBones` no Body (sem isso, partes escondidas param de animar);
  - 0,3 s depois, `CalibratePose` (1.6).
- **Variáveis** (instance editable quando fizer sentido): `PoseAnim`, `PoseTime`, `RawT`, `PlayRate`, `StepFPS` (0 = suave), `bLoop`, `bPlaying`, `MoveSpeed`, `PathPts[]`, `PathIdx`, `YawOffset`, `bHeadOnly`, `bDying`.
- **Funções** (cada uma pequena):
  - `SetPose(Anim, Time)`: pose parada (`bPlaying` falso).
  - `PlayClip(Anim, Rate, Loop, StepFPS)`: liga `bPlaying`. No Tick, `ClipStep(Dt)`:
    - `RawT += Dt * Rate`;
    - com `StepFPS` > 0, `PoseTime = floor(RawT * StepFPS) / StepFPS` (o "pulado" que dá o aspecto não natural); senão `PoseTime = RawT`;
    - com loop, volta ao início; sem loop, para no fim e dispara `OnClipEnd`.
  - `WalkPath(Pts, Speed, Anim, Rate, StepFPS, bBackwards)`:
    - segue os pontos como o `PathMove`/`PathTurn` do `BP_Apparition` (copie a lógica), com `YawOffset` 180 quando de ré (o corpo olha para longe do destino);
    - **para o pé não patinar**, use `Speed = VClip * Rate`. `VClip` é a velocidade natural do clipe no corpo do monstro: ~150 cm/s pela amostra do blend space, mas o monstro tem 205 cm e pernas mais longas, então **meça** com `MeasureClipSpeed`.
  - `MeasureClipSpeed(Anim) → cm/s` (uso de teste):
    - toque o clipe a rate 1 e amostre a 60 Hz, num ciclo inteiro, a posição em espaço do componente de `foot_l` e `foot_r` (`GetSocketLocation` + `InverseTransformLocation`);
    - em cada amostra, pegue o pé **mais baixo** (o apoiado) e a sua velocidade horizontal `|dXY/dt|`;
    - a **mediana** dessas velocidades é o `VClip`. Grave o valor no MONSTER_METAHUMAN.
  - `GroundSnap()`: raio para baixo a partir da pelve; acerta o piso ou o degrau (importante na escada) e corrige o Z.
  - `SnapLook(TargetLoc, Dur)`: calcula as rotações de pescoço e cabeça até o alvo, com limite de ±80° de yaw e ±30° de pitch, e sobe o `LookAlpha` de 0 a 1 em `Dur` (0,06–0,1 s = "de sopetão"). `LookHold` segue o alvo devagar depois.
  - `HeadOnly(On)`: esconde (`SetVisibility false`) Body, Torso, Legs e Feet do MetaHuman e deixa **Face e cabelo** visíveis.
    - O rosto continua animando pelo corpo invisível; confira.
    - No escuro, o corte do pescoço não aparece. Se aparecer, um `M_DarkVoid` pequeno atrás resolve.
  - `FaceLightOn(Intensity, Fade)` / `FaceLightOff(Fade)` (Fase 0.4).
  - `IsSeen(DotMin) → bool` e `HeadVisible() → bool`: dot da câmera com a cabeça + raio `TraceTypeQuery2` câmera→head (mesma regra do `ExposeCount`). Comece o raio 60 cm à frente da câmera.
  - `Vanish()`: esconde, liga `bDying` e chama `SetLifeSpan 0.1` (mesma correção do `BP_Apparition`: nunca destrua no meio do Tick).
- **Teste da Fase 1:** um `BP_MonsterStand` temporário no corredor dos clientes (−300, 215), no Simulate. Fotos de cada caso:
  - pose parada;
  - `PlayClip` do andar de ré a rate 3, com `StepFPS` 15 e com 0;
  - `SnapLook` para a câmera;
  - `HeadOnly`;
  - pose de apontar (1.6).

  Rode também o `MeasureClipSpeed` do `MH_MF_Unarmed_Walk_Bwd`.

**1.4 `BP_ScareManager`** (1 na cena, `Gameplay/`). Decide quando um susto pode rodar e garante **um susto por vez**: nem susto novo nem aparição do Director enquanto outro roda.
- `Scares[]`: os atores `BP_Scare_*` da cena (achados no BeginPlay).
- **Regras para armar:**
  - noite (`BP_GameClock.GameMinutes` ≥ 1170, como o Director);
  - `Day ≥ Scare.MinDay`;
  - susto ainda não usado hoje (`LastDayUsed`);
  - cooldown global de 60–120 s desde o último susto ou aparição;
  - jogador **fora** do computador: `PlayerController.bShowMouseCursor` falso + 1 s de carência (a mesma regra do `UpdateBusy`);
  - nenhum cliente no balcão em State 2/3, para não estragar um atendimento.
- **`bBusy` público.** O `BP_ApparitionDirector` passa a consultar `ScareManager.bBusy` antes de nascer (uma checagem no `SpotFree`/`InfiniteSpawn`/`TrySpawn`). O manager, por sua vez, só arma sem o monstro rastejante em cena (`Director.Apparition` inválido). **Uma aparição por vez no total.**
- **Escolha:** a cada 2 s, sorteia com peso um entre os sustos "armáveis" e chama `Arm()`. O próprio susto decide quando disparar (pelos gatilhos dele). Se não disparar em `ArmTimeout` (60–120 s), `Disarm()`.
- **Teclas de debug:** como as 1–4 do Director (`AutoReceiveInput = Player0`, eventos `Input|KeyboardEvents`).
  - **5** = A (apontar o livro), **6** = B (rosto no canto), **7** = C (porta + empurrão), **8** = D (escada), **9** = E (fim do corredor), **0** = F (atrás de você).
  - `DebugArm(Idx)` arma na hora, ignorando horário e regras.
  - `bScareTest` liga as teclas e desliga as regras de dia e horário.
- **Calendário sugerido** (ajustável pelo `MinDay` de cada ator): dia 1 → B; dia 2 → E e A; dia 3 → D e F; dia 4+ → C e todos sorteáveis. No máximo 2 sustos por noite (`MaxPerNight` = min(dia, 2)).

**1.5 `BP_Scare` (base) + `BP_Scare_*` (filhos).** Cada susto é um ator posto na cena, com componentes que o usuário ajusta **com a cena parada** (regra 0):
- **Componentes:**
  - `Root`;
  - `MonsterMark` (Arrow: posição e direção dos pés do monstro; a seta aponta para onde ele olha);
  - extras por tipo: `RetreatPts` (array de vetores **instance editable com `MakeEditWidget`**), `TriggerBox`, `BookMark`, `DarkZone`.
- **Variáveis comuns:**
  - `MinDay`, `Weight`, `LastDayUsed`, `bArmed`;
  - `State` (int: 0 inativo, 1 armado, 2 executando, 3 terminando);
  - `Monster` (`BP_MonsterStand`), `Manager`, `bDebugLog`.
- **Funções comuns:**
  - `CanArm() → bool`: o filho sobrescreve (distância do jogador, ponto fora da vista etc.).
  - `Arm()`, `Disarm()`.
  - `Finish()`: o monstro some, a zona e as luzes voltam, avisa o manager e grava `LastDayUsed`.
  - `SpawnMonster(Mark) → BP_MonsterStand`: só com o ponto **fora da vista** (dot < 0,3 ou sem linha de visão).
- **Tick** só com `State` > 0 (como o `BP_Book`: `SetActorTickEnabled` no `Arm`/`Finish`).

**1.6 Pose de apontar montada (`PointAlpha`), sem animação**
Pedido do usuário: **estático**, **cabeça baixa**, braço direito esticado para a frente e **só o indicador apontando**.

**Ideia central.** A receita não depende de saber os eixos locais dos ossos do MetaHuman (foi isso que travou a mão na quina). Cada rotação é calculada como "a rotação que leva a direção atual de um segmento (ex.: ombro→cotovelo) até a direção desejada", tudo em **espaço do componente**. Ela é aplicada com `Transform (Modify) Bone` em **Rotation Mode = Add to Existing** e **Rotation Space = Component Space**: a rotação gira o osso, e os filhos junto, em volta da própria articulação. Os eixos do corpo também não são supostos: são **lidos do ator** em runtime.

**Ossos do `SKM_MH_Monster_BodyMesh`** (lidos em 2026-11-06):
- Braço: `clavicle_r` → `upperarm_r` → `lowerarm_r` → `hand_r`.
  - Filhos corretivos e de torção (`upperarm_twist_01/02_r`, `lowerarm_twist_01/02_r`, `*_correctiveRoot_r`, `wrist_inner/outer_r`) acompanham sozinhos.
- Dedos: `hand_r` → `{index,middle,ring,pinky}_metacarpal_r` → `*_01_r` → `*_02_r` → `*_03_r`. **Não gire os metacarpos.**
- Polegar: `hand_r` → `thumb_01_r` → `thumb_02_r` → `thumb_03_r` (sem metacarpo).
- Coluna e cabeça: `spine_01..05` → `neck_01` → `neck_02` → `head`.
- Os ossos `*_bulge/_half/_side/_in/_pip/_dip/_mcp/_palm*` são corretivos: ignore.

**Base.** `MH_MM_Idle` no Sequence Evaluator com `PoseTime` **fixo**. Escolha um quadro com os braços soltos; sem `PlayClip`, não há respiração nem balanço. Os nós da pose vêm depois do Evaluator, todos com `Alpha = PointAlpha`: 0 desliga tudo e 1 aponta. Interpolar em 0,2–0,3 s dá o "levantar seco" do braço.

**Passo 1: `CalibratePose()`** (automático no `BeginPlay` + 0,3 s, com `PointAlpha` 0 e `LookAlpha` 0). Funciona para qualquer monstro.
- Para cada osso da lista, `P = InverseTransformLocation(BodyCompTransform, Body.GetSocketLocation(osso))` (posição em espaço do componente).
  - Lista: `upperarm_r` (S), `lowerarm_r` (E), `hand_r` (W), `index_01_r`, `index_03_r`, `middle_01_r`, `middle_03_r`, `pinky_01_r`, `thumb_01_r`, `neck_01`, `head`, `spine_05`.
  - Grave em variáveis `Ref_*`.
- Eixos do corpo em espaço do componente:
  - `FwdC = Body.InverseTransformDirection(ActorForward)`;
  - `RightC = Body.InverseTransformDirection(ActorRight)`;
  - `UpC = Body.InverseTransformDirection(ActorUp)`.
  - (Pelo `BP_CustomerMH`, deve sair `FwdC` ≈ +Y, `RightC` ≈ −X e `UpC` ≈ +Z; o log confirma.)
- **Nunca** recalibre com `PointAlpha` ou `LookAlpha` ligados: a leitura já viria modificada e a conta viraria laço.
- Logue tudo e anote no MONSTER_METAHUMAN.

**Funções de apoio** (puras, no BP):
- **`RotBetween(A, B) → Rotator`** = `RotatorFromAxisAndAngle(Normalize(Cross(A,B)), Degrees(Acos(Clamp(Dot(Â,B̂),−1,1))))`. Se `|Cross|` < 0,0001, devolve (0,0,0). É o "find between" que o Blueprint não tem pronto.
  - **Autoteste:** `RotateVector(Â, R)` tem que dar ≈ `B̂` (dot > 0,999).
  - Se der ≈ o espelhado, a convenção de sinal do UE está invertida: troque o ângulo para negativo **em todas** as chamadas e anote no MONSTER_METAHUMAN.
- **Girar um vetor:** `RotateVector(V, R)`.
- **Compor:** `CombineRotators(R1, R2)` = aplica R1 e depois R2.
- **`ChainRot(V, [R1..Rn])`:** aplica as rotações em ordem a um vetor de direção.
  - O pivô não importa para direções: as articulações só deslocam posições, e as direções dos segmentos já incluem tudo que veio antes.

**Passo 2: direção do braço `D`** (espaço do componente).
- **Sem alvo:** `D = Normalize(FwdC·0,95 + RightC·0,15 − UpC·0,28)` (para a frente, um pouco para a direita e ~16° abaixo da horizontal; ajuste por foto).
- **Com o livro como alvo (Fase 4):**
  1. Gire o **ator** para o livro: yaw = direção XY até o livro + `PointYawOffset` (~−12°, isto é, o corpo vira um pouco para a esquerda, para o braço direito cruzar menos).
  2. `ShoulderW = Body.GetSocketLocation(upperarm_r)`, lido com o `PointAlpha` 0.
  3. `D = Normalize(Body.InverseTransformDirection(LivroW − ShoulderW))`.
- **Limites** (senão o braço torce):
  - ângulo horizontal entre `D` e `FwdC` ≤ 35°;
  - inclinação entre −50° (para baixo) e +10°.
  - Se passar, gire mais o ator e recalcule.

**Passo 3: braço** (nós em `upperarm_r`, `lowerarm_r` e `hand_r`, nesta ordem).
- `R_UA = RotBetween(E − S, D)`: o braço inteiro mira em D.
- `F1 = RotateVector(W − E, R_UA)` e `R_LA = RotBetween(F1, D)`: estica o cotovelo, e o antebraço fica alinhado com D.
- `H1 = ChainRot(middle_01_r − W, [R_UA, R_LA])` e `R_H = RotBetween(H1, D)`: pulso reto, mão alinhada com D.
- **Rolagem da palma** (o polegar fica para cima, a palma para o lado de dentro, a "pose de revólver"):
  1. `T = ChainRot(thumb_01_r − W, [R_UA, R_LA, R_H])`;
  2. `Tp = Normalize(T − D·Dot(T,D))` e `Up = Normalize(UpC − D·Dot(UpC,D))`;
  3. `HandRoll = Degrees(Acos(Clamp(Dot(Tp,Up))))`, com sinal = sinal de `Dot(Cross(Tp,Up), D)`;
  4. `R_Roll = RotatorFromAxisAndAngle(D, HandRoll)`;
  5. o nó do `hand_r` recebe `RotHand = CombineRotators(R_H, R_Roll)`.
- **Ombro (opcional, se o ombro parecer "duro"):** `clavicle_r` com `RotBetween(Ref ombro − Ref clavícula, …)` não é preciso. Basta 8° em volta de `UpC` (com o sinal que leva o ombro para a frente) e 5° em volta de `FwdC` (que o levanta), testados como no passo 5.

**Passo 4: dedos. Caminho principal: a mão do Mixamo** (`MH_A_Mixamo_Pointing`, quadro 25).
- **No AnimGraph:** um segundo `Sequence Evaluator` com `MH_A_Mixamo_Pointing` em tempo fixo 0,83 s → `Layered blend per bone`.
  - Base: a pose parada. Blend: a pose do Pointing. Peso: `PointAlpha`.
  - Branch filters: `index_metacarpal_r`, `middle_metacarpal_r`, `ring_metacarpal_r`, `pinky_metacarpal_r` e `thumb_01_r`, todos com `Blend Depth` 0.
  - `bMeshSpaceRotationBlend` **desligado**, ou seja, mistura em espaço local: os dedos trazem só a curvatura relativa à mão.
  - **Não inclua o `hand_r`** no filtro: a orientação da mão é a calculada no passo 3.
- **Ordem:** o blend vem **antes** dos nós `Modify Bone` do braço. Assim a mão girada leva junto os dedos já na pose de apontar.
- **Conferir no Simulate:**
  - o indicador sai reto e os outros dedos ficam fechados;
  - o retarget (`RTG_AutoGenerated`) mapeia as cadeias de dedos. Se os dedos vierem retos ou tortos, a cadeia de dedos não foi mapeada: abra o `RTG_AutoGenerated`/IK Rigs, confira as chains `Index/Middle/Ring/Pinky/Thumb` e retargete de novo. Peça isso ao usuário, porque o MCP não edita retarget.
- **Indicador alinhado com `D`:** como o braço e a mão vêm da conta e os dedos do Mixamo, o indicador pode sair alguns graus fora de `D`. Corrija com `index_01_r` = `RotBetween(ChainRot(index_03_r − index_01_r, R_total + pose do Mixamo), D)`. Ou, mais simples, um ajuste fixo de `HandRoll`/`R_H` medido no Simulate.

**Passo 4 (plano B, se a mão do Mixamo não servir): dedos calculados** (o indicador fica reto; os outros fecham).
- `R_total = [R_UA, R_LA, R_H, R_Roll]`.
- **Eixo de dobra:** `K = Normalize(ChainRot(index_01_r − pinky_01_r, R_total))`, a linha dos nós dos dedos com a mão já na pose.
- **Normal da palma:** `N = Normalize(P − D·Dot(P,D))`, com `P = −RightC` (na pose de revólver da mão direita, a palma olha para a esquerda do personagem).
- **Sentido da dobra**, decidido por conta e não por tentativa: `Tip = ChainRot(middle_03_r − middle_01_r, R_total)`.
  - Calcule `a = Dot(RotateVector(Tip, RotatorFromAxisAndAngle(K, 40)), N)` e `b = Dot(RotateVector(Tip, RotatorFromAxisAndAngle(−K, 40)), N)`.
  - `CurlAxis = K` se a > b, senão `−K`.
- **Médio, anelar e mínimo:** `_01_r` **75°**, `_02_r` **95°** e `_03_r` **65°**, cada um com `RotatorFromAxisAndAngle(CurlAxis, ângulo)`. São 9 nós; a mesma variável por falange (`RotCurl01/02/03`) serve aos 3 dedos.
  - Como cada nó gira em volta da própria articulação e as rotações de componente se acumulam, o mesmo `CurlAxis` vale nas 3 falanges.
  - O mínimo pode ficar 10° a mais (`_01_r` 85°), para a mão fechar redonda.
- **Indicador:** `index_01_r` com `RotBetween(ChainRot(index_03_r − index_01_r, R_total), D)`. Isso endireita o dedo na linha de D, e `_02_r`/`_03_r` ficam com 0°.
- **Polegar:** `thumb_02_r` 25° e `thumb_03_r` 30° em volta de `CurlAxis`, e `thumb_01_r` 15° em volta de `D`, com o sinal que leva a ponta do polegar na direção de `N` (mesmo teste a/b).
  - É o que mais pode ficar estranho, mas no escuro e de longe importa pouco.
  - Alternativa: só `thumb_01_r` 20° em volta de `CurlAxis` (polegar reto encostado na mão).

**Passo 5: cabeça baixa e corpo.**
- **Eixo de "olhar para baixo":** `±RightC`.
  - Sinal, por conta: `Hd = head − neck_01` (Ref). Gire `Hd` 30° em volta de `+RightC` e de `−RightC`, e escolha o eixo em que `Dot(·, UpC)` **diminui** e `Dot(·, FwdC)` **aumenta** (a cabeça vai para a frente e para baixo).
  - Chame o resultado de `NodAxis`.
- **Ângulos** em volta de `NodAxis`: `spine_05` 6°, `neck_01` 15°, `neck_02` 15° e `head` 20°, total de ~56°.
  - Variável `HeadDown` (0–1) multiplica os ângulos.
- **Tombar a cabeça para o lado do braço:** `head` com 8–10° em volta de `±FwdC`. Escolha o sinal em que `Dot(Hd girado, RightC)` aumenta (a cabeça pende para a direita). Variável `HeadTilt`.
- **Coluna para o lado do braço:** `spine_05` com mais 4° em volta de `±FwdC`, com o mesmo sinal.
- Cabelo, se houver, tende a cobrir o rosto, como no vídeo.
- **Braço esquerdo:** fica como no idle (solto). Opcional: `upperarm_l` 4° para afastar a mão da coxa (sinal em que `hand_l` se afasta do eixo do corpo).
- O `SnapLook` (1.2) soma por cima quando um susto pede olhar para o jogador.

**Onde calcular.** Tudo em `BP_MonsterStand.BuildPointPose(TargetWorld)`, chamado uma vez ao apontar e não por quadro.
- Grava no ABP, pela instância de animação (`GetAnimInstance` → cast `ABP_MonsterStand`), as variáveis:
  - `RotUA`, `RotLA`, `RotHand`, `RotCurl01/02/03`, `RotIdx01`, `RotTh1/2/3`;
  - `RotSpine`, `RotNeck1`, `RotNeck2`, `RotHead`, `PointAlpha`.
- O AnimGraph só tem os nós `Modify Bone` ligados a essas variáveis, nesta ordem: Evaluator → spine_05 → neck_01 → neck_02 → head → upperarm_r → lowerarm_r → hand_r → index_01_r → middle/ring/pinky_01..03_r → thumb_01..03_r → nós de olhar (1.2).
- Divida o `BuildPointPose` em funções pequenas (`ArmRots`, `HandRoll`, `FingerRots`, `HeadRots`), por causa do DSL.
- Depois, `PointAlpha` 0 → 1 em 0,25 s.

**Se a verificação falhar** (o modo "Add, Component" do UE se comportar de outro jeito): use **Replace Existing + Component Space**.
- No `CalibratePose`, guarde também `RefRot_osso = Body.GetSocketRotation(osso)` convertida para o componente.
- Mande `CombineRotators(RefRot_osso, R_acumulada_até_esse_osso)`, onde `R_acumulada` é a composição de todas as rotações dos ossos-pai e a do próprio osso (é o que o "Add" faria).
- Isso é explícito e não depende do comportamento do nó.

**Plano B do braço (só se o passo 3 der problema):** nó `Two Bone IK` no `hand_r` em **Component Space**.
- Efetor em `S + D·200`: longe demais, então o braço estica reto.
- `JointTarget` (cotovelo) em `E − RightC·30`.
- A tentativa antiga de IK deixou a mão no peito, provavelmente porque o alvo estava em espaço de mundo.

**Verificação** (Simulate, com o monstro em (−300, 215) e uma caixa-alvo a 3 m à frente):
1. `PointAlpha` 0: foto e log do `CalibratePose`. Confira `FwdC`/`RightC`/`UpC` e o autoteste do `RotBetween`.
2. `PointAlpha` 1: log destes critérios.
   - ângulo entre (`hand_r − upperarm_r`) e `D` < 3°;
   - ângulo entre (`index_03_r − index_01_r`) e `D` < 8°;
   - `middle_03_r` a < 5 cm do ponto `W + 0,5·(middle_01_r − W)` (dedos fechados);
   - Z do `head` 8–15 cm abaixo do idle;
   - `thumb_03_r` acima do `index_01_r` em `UpC`.
3. Fotos de frente, de perfil, **da vista do jogador a 5–7 m** e uma bem de perto da mão. Mostre ao usuário antes de seguir para a Fase 4.
4. Teste o alvo em 4 lugares (à frente, 30° à direita, mais baixo, no chão) para conferir os limites de `D`.

### Fase 2 ◐ (2026-11-10): B, rosto no canto escuro — redesenhada após testes do usuário
**Estado:** `BP_Scare_B` pronto e testado pelo usuário (tecla **9** dispara todos os pontos de uma vez); 7 pontos na cena (`Gameplay/Scares/B`): atrás do PC (`ScareB_PC`), 5 frestas do térreo (`ScareB_Fresta_X95/X210/X395/X510/X697`, y 388) e 1 em pé (`ScareB_EmPe_Magazines`). Detalhes, valores e armadilhas em MONSTER_METAHUMAN.md ("Fase 2 dos sustos"). **O desenho mudou do texto abaixo:** o corpo inteiro aparece (o `HeadOnly` não esconde o tronco deste MetaHuman), sempre **de frente para o jogador** (reorienta a cada tick), e sai em **movimento aos saltos** (degraus de quadro, estilo The Mortuary Assistant): PC e em pé saem de lado; frestas saem **de ré** para a sombra (`bExitBack`). Sorteio por vez: parado ou saindo da quina (`EmergeChance`).
**Atualização 2026-11-10 (tarde):** `BP_DarkZone` + `M_DarkVoid`/`M_DarkVoidFade` feitos; 2 pontos no mezanino (`ScareB_Mezz_Parede`, `ScareB_Mezz_Estante`) e zonas escuras globais (térreo pisca, mezanino fixo). Teclas **7** (térreo), **8** (mezanino), **9** (todos); apertar de novo encerra o susto e remove o monstro.
**Pendente da Fase 2:** (1) refazer os pontos de teto/chão das gôndolas e o baixo junto ao balcão; (2) ligar o `BP_Scare_B` ao `ScareManager.Pick` (hoje só teclas 7/8/9 e `bTestOnStart`); (3) o ponto em pé (Magazines) e os cantos do mezanino ainda não foram vistos em movimento pelo usuário em todos os ângulos; (4) `M_DarkVoid` ainda não está em nenhuma malha (só se algum canto precisar de fundo preto); (5) opcional: `CanArm` pela escada; (6) reverter o estado de teste da cena (CLAUDE.md "Para retomar").

#### Texto do plano original da Fase 2
**Lugar:** um vão de 10–25 cm, escuro, à altura de uma cabeça (150–175 cm) ou mais baixo (~100 cm, agachado), visto **de passagem** na periferia de um caminho que o jogador faz sempre. **Não coloque sem aprovação com foto.** Candidatos para fotografar:
- a fresta entre a ponta de uma estante e uma coluna no térreo;
- entre a `BP_BookShelfs36` e a `ColumnBigger2`, no mezanino;
- ao lado da `Column3` (−460, 300), perto do pé da escada;
- atrás dos arquivos de aço da área do atendente (X −729…−681).

**Componentes:**
- `MonsterMark`: posição da cabeça; a raiz do `BP_MonsterStand` fica ~1,9 m abaixo (meça o Z do `head` no `CalibratePose`), ou use uma pose agachada;
- `HidePt`: 15–25 cm mais fundo no vão;
- `DarkZone`: caixa só no canto;
- um `M_DarkVoid` atrás do vão.

**Fluxo:**
1. **`Arm`:** `CanArm` = jogador a 3–9 m e o vão **fora da vista**.
   - Liga a `DarkZone` (luzes locais a 0,1, void visível).
   - Nasce o monstro com `HeadOnly(true)` e pose idle, cabeça inclinada (10–20° de roll, pelo `HeadTilt`), `FaceLight` de 0 a fraca em 0,4 s.
2. **Espera o jogador passar a vista:** dispara quando o dot da câmera com a cabeça fica entre **0,45 e 0,85** (periferia), com linha de visão.
3. **Conta `SeenT`.** Some quando:
   - `SeenT` > 0,5–0,9 s (sorteado);
   - **ou** o jogador olha direto (dot > 0,9 por 0,12 s);
   - **ou** ele chega a menos de 2,5 m.
4. **Sumir = "esconder":** a `FaceLight` apaga em 0,15 s, a cabeça desliza para o `HidePt` em 0,25 s (ease-in) virando 20° para dentro do vão, e então `Vanish`.
5. **Ao fim,** a zona volta ao normal **quando estiver fora da vista**, ou em 3 s com um fade lento de 2 s.
- Se o jogador nunca olhar em 90 s → `Disarm` sem nada.

**Parâmetros iniciais:** `PeriphMin` 0,45, `PeriphMax` 0,85, `StareDot` 0,9, `ShowMin/Max` 0,5/0,9, `NearDist` 250, `ZoneScale` 0,1, `FaceLightInt` (ajustar por foto: o rosto deve ser **pouco** visível).

**Teste:**
- `BP_ScenDriver` com o jogador parado a 5 m, girando o yaw devagar através do vão.
- Log com dot, `SeenT` e estado.
- Fotos no momento em que o rosto aparece (`CaptureEditorImage`).
- Depois, o usuário testa com a tecla **6**.

### Fase 3 ☐: E, fim do corredor (recua de ré e some na curva)
**Lugar:** um corredor comprido entre estantes (ou o corredor central do térreo) cujo **fim tem uma quina** para um lado (ponta de estante, coluna, recuo raso). Distância de quem vê: 8–15 m. Candidatos: os corredores entre as estantes do térreo vistos do lado da porta (X alto) para o oeste, ou um corredor do mezanino.

**Componentes:**
- `MonsterMark`: no fim, olhando o corredor;
- `RetreatPts`: 3–6 pontos (1–2 m de ré em linha reta, depois 90° para trás da quina), como o `PathPts` atual, mas em pé;
- `WatchFrom` (opcional): caixa onde o jogador precisa estar para armar, garantindo que ele chega pelo corredor.

**Fluxo:**
1. **`Arm`** com o ponto fora da vista e o jogador dentro de `WatchFrom` (ou a < 15 m na linha do corredor).
   - Nasce parado, com o idle "esquisito" e a cabeça um pouco baixa (`HeadDown` 0,4).
   - Segue o jogador com a cabeça **devagar** (20°/s, limite 30°).
   - A zona do fim do corredor fica a 0,3 (meia-luz, como no vídeo, em que ela é visível de longe).
2. **Gatilho** (qualquer um):
   - o jogador **avança na direção dele** (velocidade na direção > 60 cm/s por 0,5 s) com ele à vista;
   - **ou** o encara por 2,5–4 s;
   - **ou** chega a < 5 m.
3. **Recuo:** `WalkPath(RetreatPts, VClip·Rate, MH_MF_Unarmed_Walk_Bwd, Rate 1,3–1,6, StepFPS 0)`.
   - É mais calmo que o de A: o vídeo mostra um andar de ré quase normal, e o choque vem do lugar onde ela some.
   - No último trecho (a curva), ele gira o corpo junto com o caminho.
4. **Some:**
   - assim que `HeadVisible()` falha por 0,1 s (a quina tapou) → `Vanish`;
   - **se terminar o caminho ainda visível** (o jogador entrou no corredor de lado): `FaceLightOff` + `ZoneLights` 0 em 0,2 s + `Vanish` no escuro. Fallback: piscar de 2 quadros.
5. **Ao fim,** a zona volta ao normal com o jogador fora da vista.

**Cuidado:** cheque o caminho de ré com raios **osso a osso**, como em MONSTER_METAHUMAN ("Caminhos testados"). O monstro não pode atravessar estante à vista do jogador.

**Teste:**
- O driver anda o jogador pelo corredor na direção do monstro.
- Log de estado e visibilidade.
- Fotos em 3 instantes: parado, de ré e na curva.
- Tecla **9**.

### Fase 4 ☐: A, aponta para o livro bizarro
Depende da **pose montada de apontar** (1.6) e dos **livros bizarros**. Enquanto o sistema dos livros bizarros não existir, use o `SM_Book_06` ("The Last Borrower", fora do catálogo; veja [BOOK_COVERS.md](BOOK_COVERS.md)) como livro-alvo.

**Lugar:** uma área com fundo ou canto onde o recuo caiba. Opções:
- a sala de leitura do mezanino (mesa comprida, centro (640, 0));
- o canto de leitura ao lado da `BP_BookShelfs36`;
- um corredor de estantes.

O livro fica numa mesa, em pé numa prateleira (meio puxado para fora) ou no chão.

**Componentes:**
- `MonsterMark`: onde ele começa, **de costas para o jogador**, perto do livro, "mexendo em algo" (pose idle, `HeadDown` 0,6);
- `RetreatPts`: 1,5–2,5 m de ré **sem sair da vista**, terminando encostado num canto ou parede;
- `BookMark`: posição e rotação do livro.

**Fluxo:**
1. **`Arm`:** `CanArm` = o monstro e o `BookMark` **fora da vista**, e o jogador a 5–12 m.
   - Spawn de um `BP_Book` (malha do livro bizarro) no `BookMark`, em State 0 (parado, sem física). **Não** ligue o tick, ou ligue e deixe o `SleepIfIdle` dormir.
   - Marque o livro (`Tags` += `Strange`) para o futuro sistema de livros bizarros reconhecê-lo.
   - Nasce o monstro de costas.
2. **Gatilho:** o jogador o vê (dot > 0,75, com LOS) por 0,3–0,6 s, **ou** chega a < 5 m.
3. **Recuo de ré acelerado** (o pedido principal do usuário):
   - `WalkPath(RetreatPts, VClip·Rate, MH_MF_Unarmed_Walk_Bwd, Rate 2,8–3,4, StepFPS 12–15, bBackwards)`;
   - com `VClip` ≈ 150–170 cm/s, isso dá **≈ 450–550 cm/s**. No vídeo, ~1,5 m em 0,3 s ≈ 500 cm/s;
   - ele gira para ficar **de frente para o jogador** enquanto anda (no vídeo ela termina de lado, de costas para a parede);
   - o degrau (`StepFPS`) é o que dá o "mais rápido que a realidade". Grave com e sem degrau e deixe o usuário escolher (`StepFPS` instance editable).
4. **Chegou:**
   - volta à pose base parada (`SetPose(MH_MM_Idle, quadro fixo)`);
   - gira o ator para o livro e chama `BuildPointPose(BookMark)` (1.6);
   - `PointAlpha` 0 → 1 em 0,2–0,3 s: o braço sobe seco e para;
   - corpo parado, cabeça baixa (`HeadDown` 1), sem olhar para o jogador. **Nada se mexe depois disso.**
5. **Some** quando:
   - o jogador olha para o **livro** (dot com o livro > 0,85) e o monstro sai da vista (dot < 0,35) → `Vanish`;
   - **ou** o jogador chega a < 1,3 m → piscar de luz (`FlickerZone` 0,4 s) e `Vanish` no meio do piscar;
   - **ou** 25 s se passam.
6. **O livro fica.** Gancho para o futuro: `OnStrangeBookShown(Book)` no manager (vazio por enquanto).

**Teste:**
- O driver fica parado a 7 m, olhando o monstro.
- Log: velocidade real (cm/s), duração do recuo, yaw final e os critérios da verificação da 1.6, com `D` apontando para o livro.
- Fotos do recuo (no meio) e do apontar.
- Tecla **5**.

### Fase 5 ☐: D, parado na escada (cabeça vira de sopetão, apagão)
**Lugar:** a escada `StairHalf_02` (X −450…−164, Y 292…443, sobe de Z 10 a 434).
- O monstro fica **num degrau do meio ou no patamar**, no caminho, de frente para quem sobe (ou de lado, olhando a parede).
- O jogador costuma subir a partir do balcão. Confira a linha de visão do pé da escada (≈ −480, 360) e do mezanino (para quem desce).

**Componentes:**
- `MonsterMark`: pés no degrau (use `GroundSnap`);
- `PassBox`: caixa fina em volta do corpo; overlap com o jogador = ele está atravessando;
- `ArmFrom`: caixa no pé **ou** no topo da escada.

**Fluxo:**
1. **`Arm`** só com o ponto fora da vista (ex.: jogador atrás do balcão de costas, ou no mezanino, longe).
   - Nasce parado, com o idle esquisito e a cabeça **olhando para outro lado** (yaw −60°, pitch −20°, pelo olhar da 1.2).
   - Sem colisão nenhuma.
   - **Não reage a ser visto.** É o oposto das outras aparições: ele não foge.
2. **Gatilho:** o jogador a < `SnapDist` (110–140 cm, medido em 3D da cabeça do monstro à câmera) **ou** overlap com a `PassBox`.
3. **`SnapLook(câmera, 0,07 s)`:** só a cabeça vira, de uma vez; o corpo continua parado. Segura 0,25–0,45 s.
4. **`LightRig.Blackout(2,5–4 s)`:** preto absoluto e instantâneo, sem piscar (no vídeo a luz cai seco).
   - Durante o preto, `Vanish`.
   - Ao voltar, a luz acende de uma vez (ou pisca 2 vezes) e não há nada.
5. Se o jogador nunca chegar perto em `ArmTimeout` → some quando estiver fora da vista.

Se o jogador vier **de cima** (descendo), a mesma lógica vale.

**Teste:** o driver sobe a escada (veja `BP_ApproachDriver`, que anda o jogador). Tecla **8**.

### Fase 6 ☐: F, atrás de você no beco sem saída
**Lugar:** um fim de corredor fechado (estante + parede, ou o recuo de um corredor entre estantes encostadas na parede). O jogador precisa entrar **olhando para o fundo** e se virar para sair.

**Componentes:**
- `DeadEndBox`: o fundo (1,5–2 m);
- `FaceDir` (Arrow): direção para o fundo.

**Fluxo:**
1. **`Arm`** (ainda não nasce nada).
   - Dispara quando o jogador está dentro da `DeadEndBox` olhando para o fundo (dot com `FaceDir` > 0,7) por 0,8–1,5 s.
   - Calcula o ponto atrás dele: `P = câmeraXY − fwdXY·BehindDist (120–150)`.
   - Exige: `P` no NavMesh (`ProjectPointToNavigation`), nenhuma parede entre `P` e o jogador (raio) e `P` **fora da vista** (dot < −0,3).
   - Nasce o monstro com os pés em `P`, de frente para o jogador. Como ele tem 205 cm, olha para a câmera de cima (`SnapLook` contínuo, pitch para baixo). `FaceLight` fraca.
   - Opcional: a zona do corredor cai para 0,4, deixando só silhueta + rosto.
2. **Gatilho:** o jogador vira e o vê (dot > 0,7, com LOS).
   - Segura 0,4–0,7 s: o susto é ver o rosto de perto.
   - `LightRig.Blackout(1,5–2,5 s)` absoluto → `Vanish` no escuro → a luz volta, nada.
3. **Outros finais:**
   - se ele não virar em 8 s → `Vanish` em silêncio (fora da vista) e `Disarm`;
   - se o jogador andar de costas e encostar no monstro (< 50 cm) → o mesmo apagão.
4. **Variante do vídeo (mão no canto):** se o beco tiver quina lateral, nascer **atrás da quina** com só a mão visível. Fica como ideia: depende da pose "agarrar borda", que ainda não existe. Pode ser montada com a técnica da 1.6 (braço mirando a quina, dedos dobrados sobre ela).

**Teste:**
- O driver anda o jogador até o fundo, espera 1,5 s e gira 180° em 0,4 s.
- Log do ponto P, do dot e dos tempos; foto no instante em que ele vira.
- Tecla **0**.

### Fase 7 ☐: C, parado na passagem escura + empurrão (o mais complexo; por último)
Depende do **Push** (1.1), de uma **zona bem escura** (Fase 0) e da **queda do jogador** (7.2).

**Lugar:** uma passagem que possa ficar escura e ser vista de 6–12 m, com um "fundo" onde o `M_DarkVoid` deixe tudo preto. Proponha 2–3 opções com foto antes. Candidatas:
- um vão entre estantes que dê num canto sem luz;
- o espaço **embaixo ou atrás da escada**;
- a passagem para a área do atendente.

**7.1 Fluxo:**
1. **`Arm`:** a zona escurece **fora da vista** (luzes locais em 0, void ligado).
   - O monstro nasce de pé **meio para dentro do escuro**, deslocado para um lado do vão (como no vídeo, metade atrás do batente), de frente para o jogador.
   - Idle quase parado, `FaceLight` bem fraca: o rosto só lê como uma mancha pálida.
2. **Fica enquanto o jogador olha.** Some quando:
   - for visto por 3–6 s;
   - **ou** o jogador andar até ele (< 5 m).

   Para sumir, dá 1 passo de ré (`WalkPath` 40 cm, `Walk_Bwd` rate 1), a `FaceLight` apaga em 0,3 s e `Vanish` ("afunda" no escuro).
3. **Armadilha:** o susto continua armado (`State` 2) e a zona continua escura. Quando o jogador entra na `TrapBox` (na boca da passagem, ~1–1,5 m) olhando para dentro (dot com a direção da passagem > 0,5):
   - nasce o monstro 70–90 cm à frente, **dentro do escuro**, com o rosto aceso em 0,1 s;
   - `PlayClip(Push, Rate 1,4)`, de `StartTime` 0,73 s (quadro 22) a `EndTime` 1,50 s (quadro 45; ver 1.1). Quando `PoseTime` ≥ **1,17 s** (quadro 35, braços esticados) → `Player.KnockDown(dir)`;
   - `Vanish` logo depois do corte para o preto.
4. Se o jogador nunca entrar em 60 s → `Disarm`, e a zona volta ao normal fora da vista.

**7.2 Queda do jogador (`BP_LibraryCharacter.KnockDown(PushDir)`).** Tudo no BP do jogador; o template fica intocado.
- `DisableInput` e o que fazer com os livros da mão (`Drop` de cada um, ou mantê-los). **Padrão: os livros caem junto.** Confirme com o usuário.
- `LaunchCharacter(PushDir * 450 + Z 150)`.
- **Câmera:**
  - Crie o `BP_CamKnock`, filho de `CameraModifier` (evento `BlueprintModifyCamera`).
  - Ele aplica pitch +25° e roll 35° numa curva rápida (0,25 s) e depois deita (roll 80°, câmera −120 cm).
  - Adicione com `PlayerCameraManager.AddNewCameraModifier` e remova ao levantar.
  - Se o `CameraModifier` não funcionar pelo MCP, a alternativa é animar o `CrouchCamOffset` (o mesmo mecanismo do agachar, que desce a `FirstPersonMesh`) + o roll por `SetControlRotation` com `bUseControllerRotationRoll`. Teste os dois.
- **Preto:**
  - `PlayerCameraManager.StartCameraFade(0→1, 0,12 s)` no impacto;
  - segura 2–3 s (a luz da zona volta ao normal durante o preto);
  - fade in já deitado (1 s);
  - "levanta" em 1,5 s (o modifier volta a zero) e `EnableInput`.
- **Sem game over** (padrão; é só um susto com punição). O `GameClock` continua correndo.

**Teste:**
- O driver anda o jogador até a `TrapBox`.
- Log do quadro do empurrão e da posição final do jogador.
- Fotos: monstro aparecendo, impacto (antes do preto), deitado e de pé.
- Garanta que o jogador **não** atravessa o piso nem fica preso numa estante: lance um raio na direção do empurrão e, se bater em algo a < 150 cm, reduza a força.
- Tecla **7**.

### Fase 8 ☐: Integração, ajuste e documentação
- Manager com o calendário (1.4) e o Director respeitando o `bBusy` (uma aparição por vez).
- Um passe de ajuste com o usuário jogando uma noite inteira (`DebugStartMinutes` 1170, `SecondsPerGameMinute` 2).
- **Docs:**
  - MONSTER_METAHUMAN: seção nova "Sustos", com cada `BP_Scare_*`, os lugares escolhidos e os valores finais;
  - SCENE_MAP: atores novos em `Gameplay/Scares` e as zonas;
  - ROADMAP: Etapa 4;
  - `CLAUDE.md`: o "Onde paramos".
- **Flags para desligar antes de testadores:** `bScareTest` e o `bDebugLog` de cada susto, além das do Director e do GameClock já documentadas.

## 4. Resumo do que é novo
| Asset | Tipo | Fase |
|---|---|---|
| `BP_LightRig`, `BP_DarkZone`, `PP_Night` (ator na cena), `M_DarkVoid`, `M_DarkVoidFade`, `MI_LampOff` (se preciso) | luz/escuro | 0 |
| `ABP_MonsterStand`, `BP_MonsterStand`, `BP_ScareManager`, `BP_Scare` | infraestrutura | 1 |
| Pose de apontar montada (`CalibratePose`, `BuildPointPose`, `PointAlpha`) | pose calculada | 1.6 |
| `MH_A_Mixamo_Push` ("Standing 2H Magic Attack 03", quadros 22–45, contato no 35) + `MH_A_Mixamo_Pointing` (só a mão, quadro 25) + idle opcional | animação (o usuário baixa) | 1 |
| `BP_Scare_CornerFace` (B), `BP_Scare_AisleEnd` (E), `BP_Scare_PointBook` (A), `BP_Scare_Stairs` (D), `BP_Scare_Behind` (F), `BP_Scare_Doorway` (C) | sustos | 2–7 |
| `BP_CamKnock` + `KnockDown` no `BP_LibraryCharacter` | jogador | 7 |
| Mudanças pequenas: `BP_GameClock` (blend do `PP_Night` à noite), `PointLight` na luminária do balcão, `BP_ApparitionDirector` (respeitar `ScareManager.bBusy`; depois usar o `BP_LightRig`) | ajustes | 0, 1, 8 |

Atores de cena: a pasta `Gameplay/Scares` (um ator por susto colocado) e `Gameplay/` (`LightRig`, `ScareManager`, `PP_Night`).

## 5. Riscos e o que conferir cedo
- **Rosto sem corpo (`HeadOnly`):** confirme no Simulate que a `Face` continua animando com o Body escondido (`AlwaysTickPoseAndRefreshBones`). Se não continuar, plano B: o corpo inteiro numa pose agachada **atrás** da geometria e só a cabeça no vão.
- **Rotação da cabeça no ABP e o rosto do MetaHuman:** se o rosto não acompanhar o `Modify Bone`, aplique a rotação em `neck_01` ou use o nó `Look At`.
- **Convenção de sinal das rotações do UE:** os autotestes da 1.6 (`RotBetween`, curl, nod) decidem por conta. Não chute sinais.
- **Escuridão contra jogabilidade:** o balcão e o computador precisam continuar legíveis; meça por foto às 21:00.
- **Desempenho:** mexer em ~40 luzes por quadro no `FlickerZone` é barato, e o `MegaLights` está ligado. Se cair, meça com o Unreal em primeiro plano (`BP_PerfDriver`).
- **Emissivos:** sem apagar o emissivo das luminárias, nenhuma zona fica preta de verdade (2.1). Resolva isso cedo, na Fase 0.
- **Pés patinando no andar de ré:** sempre `Speed = VClip × Rate`, com o `VClip` medido no corpo do monstro.
