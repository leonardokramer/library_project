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

## Para o jogo (a fazer)
Ainda **não** integrado: o `BP_CustomerMH` usa os 9 `MH_*` por linha da `DT_People`. O monstro entra como aparição
à parte (ator próprio, não é cliente). Para anomalias que aparecem só em certos momentos, considerar morph target ou
Control Rig em runtime em vez de trocar de personagem.
