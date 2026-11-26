# Clientes MetaHuman (personas fixas)

Plano aprovado pelo usuário em 2026-11-25. Objetivo: trocar os 9 presets `MH_*` (Ada, Aera, Aoi, Asha, Bo, Bruce, Cameron, Celeste, Kelvin) por MetaHumans próprios, feitos a partir de misturas de presets, críveis numa livraria em 1996. O `MH_Monster` não muda. Rostos fixos importam para o terror: o jogador precisa reconhecer os regulares para estranhar quando algo muda.

## Divisão do trabalho
- **Claude:** busca, instalação, misturas iniciais, fotos, ligar na `DT_People`/`BP_CustomerMH`, conferir animações (retarget, pés no chão, livro na mão, mão na maçaneta, caminhada) e PIE.
- **Usuário:** escolha visual e ajuste fino de rosto no Creator.
- O MetaHuman antigo de uma persona só sai depois de o novo estar testado.

## Personas (idade e perfil são decisões de jogo; a `DT_People` só guarda nome e documento)
| Linha | Persona | Idade | Corpo | Base (preset atual + mistura) | Traje principal | Extras (2ª etapa) |
|---|---|---|---|---|---|---|
| P01 | Helena Duarte, professora aposentada | 68 | baixa, magra | Ada + preset idoso | cardigan* sobre T manga longa, saia* ou calça social*, Flats | Sweater; capa de chuva* |
| P02 | Marcos Vieira, colegial | 17 | alto, desengonçado | Kelvin + preset jovem | Hoodie, Jeans, Hightops | Crew Neck lisa + Cargo; Shorts + Running Shoes |
| P03 | Beatriz Nakamura, desenhista de arquitetura | 34 | média, esguia | Aera + ? | Shirt V-neck manga dobrada, Slim Jeans, Loafers | Tucked T + Carpenter Pants; Sleeveless Turtleneck |
| P04 | Tomás Albuquerque, marceneiro | 45 | largo, barriga | Cameron + ? | Shirt com bolso, Carpenter Pants, Boots | jaqueta do Survivor; Crew Neck + Jeans |
| P06 | Rafael Monteiro, estudante de Letras | 22 | médio, magro | Bo + ? | T manga 3/4, Jeans, Casual Sneakers | Sweater; Shirt com bolso |
| P07 | Clara Bittencourt, enfermeira do plantão noturno | 29 | corpo cheio, baixa | Celeste + ? | Sleeveless Turtleneck + cardigan*, Slim Jeans, Chelsea Boots | Casual Wear Female; Tucked T + Yoga Pants |
| P08 | Otávio Reis, contador | 55 | barriga, grisalho | Bruce + ? | camisa social* (ou Shirt com bolso), calça social*, Oxfords | Sweater sobre a camisa; blazer* |
| P09 | Isadora Lins, universitária | 19 | baixa, magra | Asha + ? | Tucked T, Slim Jeans, Hightops | Casual Shorts + Sneakers; Hoodie |
| P10 | Joaquim Prado, viúvo, vem ler jornal | 74 | alto, curvado | Aoi + preset idoso | T manga longa, colete de tricô*, calça social*, Loafers | Sweater; sobretudo* |

\* peça que não existe na biblioteca da Fab (etapa 3: Sketchfab só CC0/CC BY, MetaTailor; cada download confirmado pelo usuário). Saem: emblema do Bruce, jaqueta Techwear amarela do Kelvin; Techwear e Streetwear não entram em ninguém.

## Misturas de preset propostas (2026-11-25, a confirmar pelo usuário)
Folha de contato dos 29 presets: `scratchpad/preset_sheet.jpg` da sessão (refazer: duplicar o preset para `_Scratch`, abrir, trocar a câmera da viewport para **Face** e capturar; a escolha de câmera persiste entre janelas).
Idosos na lista: Sook-ja (mulher, leste asiático), Grace (mulher, cabelo branco), Walter e Jorge (homens grisalhos); meia-idade: Aoi, Bruce, Dominic, Lani, Lorenzo, Orlando. Jovens: Jelena, Mikel, Zuri, Etta, Tuya, Aera.
| Persona | Mistura proposta |
|---|---|
| P01 Helena (68) | Grace + Ada |
| P02 Marcos (17) | Mikel + Kelvin |
| P03 Beatriz (34) | Aera + Tuya |
| P04 Tomás (45) | Dominic + Orlando |
| P06 Rafael (22) | Omari + Isaiah |
| P07 Clara (29) | Celeste + Vivian |
| P08 Otávio (55) | Lorenzo + Bruce (sem o bigode/barba de época) |
| P09 Isadora (19) | Zuri + Etta |
| P10 Joaquim (74) | Walter + Jorge |

## Bases criadas (2026-11-25)
`/Game/Library/Characters/Metahumans/Customers/MHC_<Nome>` (fora do git, ~9 MB cada sem rig): duplicata do **primeiro** preset da mistura, salva e sem rig. Helena=Grace, Marcos=Mikel, Beatriz=Aera, Tomas=Dominic, Rafael=Omari, Clara=Celeste, Otavio=Lorenzo, Isadora=Zuri, Joaquim=Walter.
- **Mistura e rosto: usuário, no Creator** (Head & Body → Blend com o segundo preset; corpo em Body Params). Pelo MCP não dá: o clique simulado não abre o Blend, a aba Presets do editor vem vazia e o Blend pede arrastar na viewport.
- Depois: roupa (Hair & Clothing, um `WI_` por vez, foto de frente/lado/andando para ver se atravessa), rig, Assembly para `/Game/Library/Characters/Metahumans/Customers/`, ligar no `BP_CustomerMH.ChooseVisual`. Os `MH_*` antigos ficam até o novo ser testado.

## Roupas da biblioteca da Fab (37 itens, levantados em 2026-11-25)
Galeria com fotos: https://claude.ai/artifact/FtTvfE2QiYAcSeG1WP3wsi (privada). Instaladas em `/Game/Fab/MetaHuman` (fora do git, ver SETUP): T Shirt Variants, Crew Neck (Clumsy Boy), Shirt V-neck, Sleeveless Shirt/Turtleneck, Jeans, Slim Jeans, Cargo, Boots, Running Shoes, Tactical Boots, Techwear, Survivor, Half T-Shirt, Casual Wear Female, Streetwear 12. Na biblioteca, não instaladas: Tucked T, Sweater, Hoodie, Crop Top, Custom T, Shirt com bolso, Singlet, Clarkston Carpenter Pants, Basic Sweatpants (talvez = `BasicOutfit`), Yoga Pants, Shorts, Casual Shorts, Loafers, Oxfords, Chelsea, Flats, Hightops, Casual Sneakers, FlipFlops, Performance Runner, Streetwear 01.

## Cuidados
- **Peças atravessando (aviso do usuário):** em testes anteriores algumas peças atravessaram a calça (camisa por dentro/por fora, barra sobre o sapato). Para cada traje: foto de frente, de lado e andando; olhar cintura, barra da calça sobre o sapato e punhos. Se atravessar, testar outra combinação antes de ajustar malha; peças paramétricas se ajustam ao corpo, as outras não.
- **Presets do Creator 5.8:** 29 (Ada, Aera, Aoi, Asha, Bo, Bruce, Cameron, Celeste, Dominic, Etta, Grace, Isaiah, Jelena, Jorge, Kelvin, Lani, Lorenzo, Mateo, Mikel, Omari, Orlando, Sook-ja, Sunita, Trey, Tuya, Victor, Vivian, Walter, Zuri), em `Engine/Plugins/MetaHuman/MetaHumanCharacter/Content/Optional/Presets`. A web não descreve a aparência deles e o `CaptureAssetImage` não renderiza `MetaHumanCharacter`: veja a galeria no editor (aba Presets de um personagem **sem rig**; com rig ela fica travada).
- **Espaço em disco:** mexer em MetaHuman enche `Saved/Autosaves` (6,4 GB em 2026-11-25, texturas `T_Body_BC_VT` de 256 MB cada). Apague a pasta com o Unreal **fechado**. Depois de escolher os trajes, dá para remover as roupas da Fab não usadas (~1,5 GB, rebaixáveis); depois de testar os novos, os `MH_*` antigos (~2,4 GB).
- **Miniaturas da Fab:** o `thumbnailUrl` da ferramenta da Fab é um borrão de 144 px; a versão de 640 px vem de `fab.com/i/listings/<id>` (campo `thumbnails[0].images`), lida pelo navegador. Páginas publicadas não carregam imagem de outro site: embuta como data URI.
