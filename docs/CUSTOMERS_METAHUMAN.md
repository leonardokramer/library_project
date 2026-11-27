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

## Traje principal aplicado (2026-11-26, substitutos até as peças da etapa 3)
| Persona | Traje | Substitui (falta na biblioteca) |
|---|---|---|
| Helena | Sweater, Slim Jeans, Flats | cardigan, saia/calça social |
| Marcos | Hoodie, Jeans, Hightops | |
| Beatriz | Shirt V-neck (`Shirt_01`), Slim Jeans, Loafers | |
| Tomás | Crew Neck T (Clumsy Boy), Clarkston Carpenter Pants, Boots | |
| Rafael | T manga 3/4 (`Tshirt3QSlv`), Jeans, Running Shoes | |
| Clara | Sleeveless Turtleneck, Slim Jeans, Chelsea Boots | cardigan |
| Otávio | Shirt com bolso, Slim Jeans escuro, Oxfords | camisa social, calça social |
| Isadora | Tucked T, Slim Jeans, Casual Sneakers | |
| Joaquim | T manga longa (`TshirtLngSlv`), Jeans, Loafers | colete de tricô, calça social |

A 5.9 saiu só como **Preview** (2026-11-26); o usuário decidiu esperar a 5.9.0 final antes de converter o projeto (motivo: alvo web para Blueprint-only). Checkpoint antes da conversão: commit `4415ee8`.

## Estado em 2026-11-26 (sessão sem supervisão, parada no limite de uso)
- **Vestidos e salvos (9/9):** Helena (suéter bege, jeans, sapatilha), Marcos (moletom marrom, jeans, cano alto), Beatriz (manga longa oliva por dentro, jeans, mocassim), Tomás (camiseta marinho, Clarkston cáqui, bota Tactical), Rafael (3/4 bordô, jeans, tênis claro), Clara (gola alta sem manga ferrugem, jeans, tênis), Otávio (suéter cinza-azulado, calça grafite, mocassim), Isadora (manga 3/4 mostarda por dentro, jeans, cano alto), Joaquim (manga longa taupe, calça, mocassim). Pendente: cor secundária azul nos sapatos de Marcos e Beatriz.
- **Montados (9/9, 2026-11-26):** Assembly UE Optimized, Medium, em `Customers/MH_<Nome>/BP_MH_<Nome>`. Helena e Marcos pela interface; os outros 7 por script Python (`Tools/mh_build.py`, uma persona por execução, ~5 min cada; `Tools/mh_build_all.ps1` abre o editor com `-ExecutePythonScript="Tools/mh_build.py <Nome> quit"` em sequência, sem mouse). **Ligados no jogo:** os 9 `SetChildActorClass` do `BP_CustomerMH.ChooseVisual` apontam para os novos (os `MH_*` antigos continuam no disco). Testado no PIE: a Helena nova entra, chega ao balcão e deixa o livro.
- **Ligar no jogo:** `BP_CustomerMH.ChooseVisual` é uma cadeia de if por `PersonaIdx` chamando `SetChildActorClass(MHVisual, BP_MH_<preset>_C)`; trocar as 9 classes (índices 0..9, sem o 4). `LinkMHPose` liga em leader pose todos os SkeletalMesh sem AnimClass. Os antigos ficam até testar.
- **Armadilhas aprendidas:** (1) o botão **Remove** tira TODAS as peças ainda selecionadas: remova o `WI_DefaultGarment` **antes** de vestir; (2) a pasta de roupas arrastada para "Outfit Clothing" não persiste entre sessões do editor (arraste de novo; `wardrobePaths` nas configurações não funcionou, slot errado); (3) o editor tem só 16 GB: reinicie a cada 1–2 MetaHumans (estourou memória uma vez); abra com `/Engine/Maps/Entry`; (4) Chelsea, Oxfords e Casual Sneakers não terminaram de baixar; (5) a camisa `Shirt_05` não tem ajuste de cor (verde/preta); (6) `presetsDirectories` agora aponta para os presets da engine (`Config/DefaultMetaHumanCharacter.ini`), então a galeria de presets do Creator funciona.

## Correções depois da vitrine (2026-11-26)
- **Tomás:** a calça Clarkston atravessava a barra da camiseta; trocada pela camiseta para dentro (`WI_OA_CrewnecktTk`, azul-marinho 2E3A4F).
- **Clara:** o jeans atravessava a gola alta sem manga (o jeans slim também atravessa); trocada pela camiseta de manga dobrada para dentro (`WI_OA_TshirtTkPushCufSlv`, verde-petróleo 2F5D5A).
- Regra prática: peça de cima **solta** sobre calça de cintura alta atravessa; prefira as versões `Tk` (para dentro). Remontar sem refazer o rig: `Tools\mh_build_all.ps1 -Names Tomas,Clara -NoRig`.
- No Python, `unreal.Rotator(a, b, c)` é (roll, pitch, yaw): use `unreal.Rotator(roll=0, pitch=0, yaw=180)`; o MetaHuman olha para +Y.

## Economia de tokens (aprendido em 2026-11-26)
- **Python no editor em vez de cliques:** `py "<arquivo>.py" args` no console do editor (computer use só para digitar), ou `-ExecutePythonScript` na linha de comando. Resultado por arquivo de log em `Saved/`, esperado por um comando em segundo plano. A API `unreal.MetaHumanCharacterEditorSubsystem` tem `try_add_object_to_edit`, `request_auto_rigging` (blocking), `request_texture_sources`, `can_build_meta_human` e `build_meta_human`.
- Python **não** cria atores no mundo do PIE/Simulate (`GameplayStatics` sem spawn deferred). No mundo do editor o `BP_CustomerMH` aparece deitado (pose só no jogo) e `PersonaIdx` não é editável por instância: teste com o PIE de verdade.
- Fotos: decodifique o PNG do `CaptureEditorImage` direto para arquivo e veja uma cópia reduzida.

## Roupas da biblioteca da Fab (37 itens, levantados em 2026-11-25)
Galeria com fotos: https://claude.ai/artifact/FtTvfE2QiYAcSeG1WP3wsi (privada). Instaladas em `/Game/Fab/MetaHuman` (fora do git, ver SETUP): T Shirt Variants, Crew Neck (Clumsy Boy), Shirt V-neck, Sleeveless Shirt/Turtleneck, Jeans, Slim Jeans, Cargo, Boots, Running Shoes, Tactical Boots, Techwear, Survivor, Half T-Shirt, Casual Wear Female, Streetwear 12. Na biblioteca, não instaladas: Tucked T, Sweater, Hoodie, Crop Top, Custom T, Shirt com bolso, Singlet, Clarkston Carpenter Pants, Basic Sweatpants (talvez = `BasicOutfit`), Yoga Pants, Shorts, Casual Shorts, Loafers, Oxfords, Chelsea, Flats, Hightops, Casual Sneakers, FlipFlops, Performance Runner, Streetwear 01.

## Cuidados
- **Peças atravessando (aviso do usuário):** em testes anteriores algumas peças atravessaram a calça (camisa por dentro/por fora, barra sobre o sapato). Para cada traje: foto de frente, de lado e andando; olhar cintura, barra da calça sobre o sapato e punhos. Se atravessar, testar outra combinação antes de ajustar malha; peças paramétricas se ajustam ao corpo, as outras não.
- **Presets do Creator 5.8:** 29 (Ada, Aera, Aoi, Asha, Bo, Bruce, Cameron, Celeste, Dominic, Etta, Grace, Isaiah, Jelena, Jorge, Kelvin, Lani, Lorenzo, Mateo, Mikel, Omari, Orlando, Sook-ja, Sunita, Trey, Tuya, Victor, Vivian, Walter, Zuri), em `Engine/Plugins/MetaHuman/MetaHumanCharacter/Content/Optional/Presets`. A web não descreve a aparência deles e o `CaptureAssetImage` não renderiza `MetaHumanCharacter`: veja a galeria no editor (aba Presets de um personagem **sem rig**; com rig ela fica travada).
- **Espaço em disco:** mexer em MetaHuman enche `Saved/Autosaves` (6,4 GB em 2026-11-25, texturas `T_Body_BC_VT` de 256 MB cada). Apague a pasta com o Unreal **fechado**. Depois de escolher os trajes, dá para remover as roupas da Fab não usadas (~1,5 GB, rebaixáveis); depois de testar os novos, os `MH_*` antigos (~2,4 GB).
- **Miniaturas da Fab:** o `thumbnailUrl` da ferramenta da Fab é um borrão de 144 px; a versão de 640 px vem de `fab.com/i/listings/<id>` (campo `thumbnails[0].images`), lida pelo navegador. Páginas publicadas não carregam imagem de outro site: embuta como data URI.

## Beatriz: ombros e cabeça (2026-11-26)
- O usuário achou a Beatriz "ombruda", com a cabeça desproporcional. O pescoço dela estava com 28,3 cm, abaixo do mínimo do Creator (31). Ajustei por script: `Neck` 32, `Neck Base` 35 e `Across Shoulder` 25 (era 27,1). Depois remontei com `Tools\mh_build_all.ps1 -Names Beatriz`.
- **Medidas de corpo por Python:** `Tools/mh_body.py <Nome>` lista as medidas e `Tools/mh_body.py <Nome> "Neck=32" ...` aplica e salva. A armadilha: `get_body_constraints` devolve structs por cópia, então é preciso editar a lista e devolvê-la com `set_body_constraints`. A flag se chama `is_active`.

## Proporções no jogo e livro na mão (2026-11-26, conferido no Simulate; falta o teste do usuário)
- **Problema (visto pelo usuário com a Isadora):** no jogo, quem anima o cliente é o `CharacterMesh0` invisível
  (`SKM_NpcMaleCharacter_BodyMesh`, um homem médio), e o corpo do MetaHuman copia a pose por *leader pose*, que copia
  **também o comprimento dos ossos**. Todo cliente ficava com as proporções daquele homem; a Isadora (baixa e magra)
  ficava esticada. Na fila/vitrine (BP_MH_* com o próprio esqueleto) ela era normal.
- **Correção:** `BP_CustomerMH.LinkMHPose` primeiro troca a malha do `CharacterMesh0` pela malha do `Body` do próprio
  MetaHuman (`SetSkeletalMeshAsset`; todos usam o `metahuman_base_skel`, então o `MH_ABP_Customer` continua servindo) e
  depois liga o *leader pose*. Conferido: Isadora cliente com a mesma altura e proporções da Isadora da fila.
- **Livros:** a posição antiga (`FixBooks`: ponto fixo (−28, 16,5, 128,5) no espaço do corpo) era do corpo do homem; num
  corpo menor o livro flutuava na altura do rosto. Agora `FixBooks` → `FixOneBook(Bk, I, H)`: enquanto o livro está preso
  ao cliente e ainda **não** está no socket `hand_r`, ele é posto a cada Tick na transformação da mão
  (`GetSocketTransform(hand_r)`) composta com o deslocamento medido no corpo antigo, já preso à mão: posição
  (12,49; 10,29; 7,21), rotação (roll −155,41, pitch 17,29, yaw −96,33), +3 cm por livro na pilha (eixo Z do livro). Livros
  que saíram do cliente (balcão) não são tocados. Conferido de frente na Isadora (livro na mão, na cintura). Falta ver
  vários livros, a devolução no balcão e os outros 8 corpos andando.
- **Teste:** `BP_CustomerMH` posto na cena com o `ChildActorClass` do `MHVisual` trocado na instância (o `PersonaIdx` não é
  editável) + `DebugWalk`/`DebugBooks`.
