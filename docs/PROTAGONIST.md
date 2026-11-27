# Protagonista (MetaHuman)

## Conceito (2026-11-26, conversa com o usuário)
- Mulher, **nipo-brasileira**, ~32 anos, pessoa comum de 1996. Vibe **Silent Hill**: alguém "fudida investigando", cansada, nada sexualizado, nada glamoroso.
- História (em aberto): no começo parece que ela cometeu crimes e está pagando por isso; depois revela que estava investigando outra pessoa. Talvez haja histórias de outros (até dos NPCs) para ela descobrir.
- Não negra (decisão do usuário, para não reforçar estereótipo).

## Estado (2026-11-26)
- `MHC_Protagonista` em `/Game/Library/Characters/Metahumans/Protagonist/` (fora do git, como os Customers).
- **Rosto:** preset **Tuya** + 35 % **Lani** por script (`Tools/mh_proto_blend.py Lani 0.35 Tuya`). Pele e olhos do Tuya.
- **Cabelo:** Long Messy (preso para trás, desarrumado).
- **Roupa:** `WI_OA_SurvivorOutfit` (polycornStudio, grátis, já instalado em `/Game/Fab/MetaHuman`): jaqueta grafite, camiseta clara, calça escura e bota. Nenhuma NPC usa. Sem parâmetro de cor.
- **Montagem:** `Tools\mh_build_all.ps1 -Names Protagonista` (o `mh_build.py` usa a pasta Protagonist quando o nome é `Protagonista`). Saída: `Protagonist/MH_Protagonista/BP_MH_Protagonista`.
- **Montada e fotografada (2026-11-26).** Fora do git (`.gitignore`, como os Customers). Fotos: `Tools/mh_proto_photo.py [dist] [z]` põe um `TEMP_Proto` na frente do balcão (não salve o mapa; feche sem salvar).
- **Falta:** ligar no `BP_LibraryCharacter` (primeira pessoa: corpo, mãos, cenas de queda/arrasto), decidir se troca a jaqueta.

## Mistura de rosto por Python (funciona)
`MetaHumanCharacterEditorSubsystem.get_face_model_coefficients(preset)` devolve 1397 floats; `set_face_model_coefficients(char, mix)` aplica **ao vivo** com o personagem aberto no editor e `save_loaded_asset` salva. Os presets precisam de `try_add_object_to_edit` antes de ler. Não chame `try_add_object_to_edit` no personagem e depois abra o editor dele: dá "failed to create editing state" (chame `remove_object_to_edit` antes).
- O **Aoi é homem de barba**; mulheres do leste asiático: Tuya, Aera (usada na Beatriz), Sook-ja (idosa).

## MetaTailor e Sketchfab (testado, deixado de lado)
- Peças soltas do Sketchfab aparecem buscando só o nome da peça ("jacket", "turtleneck"); buscas como "female cardigan outfit" trazem escaneamentos de pessoas inteiras.
- Baixadas (CC-BY) em `Downloads`: `women-turtleneck.zip` (Juan Ledezma) e `heavy_worn_jacket.glb` (ALCArt).
- MetaTailor 2.7 (`Downloads\METATAILOR Launcher`): não tem manequim MetaHuman; precisa exportar o corpo do MH como avatar. A jaqueta encaixou no manequim com Pose Match, mas **as mangas embolaram** na caminhada. O plano grátis marca **"noncommercial use only"**: para o jogo à venda, só no plano pago.
- O Creator tem a seção **Skeletal Clothing**, onde uma peça exportada do MetaTailor entraria.

## Fab: peças pagas que combinam (2026-11-26, não compradas)
- Denim Jacket parametric (Husky studio), R$ 61,09 pessoal em promoção até 02/12: https://www.fab.com/listings/08687691-e8d1-4436-85ad-ce1d639c09ed
- Casual Outfit Jacket M65 (Quantum Assets), R$ 116,40: https://www.fab.com/listings/0680baf5-b2b5-439d-b758-bcc7b38ed3b5
- Grátis ainda não instalados: Altena Blouse (QuingKhaos), Henley T-Shirt (ADS).

## Armadilhas desta sessão
- **Não abra o Unreal pelo `open_application` do computer use:** ele abre uma instância vazia nova. Traga a janela com `(New-Object -ComObject WScript.Shell).AppActivate(<pid>)`.
- **Creator + `L_Library` carregado estoura a memória de vídeo** e o editor cai (a RTX 2070 Super tem 8 GB). Abra o editor no `/Engine/Maps/Entry` antes de mexer em MetaHuman.
- A pasta de roupas da Fab tem que ser arrastada de novo para "Outfit Clothing" a cada sessão (`left_click_drag` do computer use funciona; mouse down/move/up separado não).

## No jogo (2026-11-26, testado no PIE; falta o teste do usuário)
- **Como funciona:** o Manny continua animando tudo (`CharacterMesh0` com `ABP_Body_Library`, `FirstPersonMesh` com `ABP_FP_Library`), mas fica **invisível**. A `SetupMH` (no fim do BeginPlay) cria **duas** `BP_MH_Protagonista`:
  - `MHWorld`: o `Body` é preso ao `CharacterMesh0` e copia a pose por retarget (`ABP_MH_FromManny` = nó *Retarget Pose From Mesh*, `RTG_Manny_to_MH`, origem = componente pai). Todas as peças ficam `WorldSpaceRepresentation` (sombra, sem aparecer para o dono).
  - `MHArms`: o `Body` é preso à `FirstPersonMesh`. As peças ficam `FirstPerson` + `OnlyOwnerSee` + sem sombra; o rosto e os grooms ficam invisíveis, com `neck_01`, `thigh_l` e `thigh_r` escondidos no corpo e na roupa (em primeira pessoa aparecem mãos, mangas e peito; as pernas não).
  - A roupa (`SkeletalMesh`) segue o `Body` por leader pose. Função: `MHAttach(Act, ParentMesh, bFP)`.
- **Cenas em que o jogador vê o próprio corpo** (arrasto/abdução): a `MHSync` (no fim do Tick, depois do `KnockStep`) olha o `bOwnerNoSee` do `CharacterMesh0`. Quando o `DragBegin` o desliga, a `MHSetView(true)` mostra o `MHWorld` ao dono (`FirstPersonPrimitiveType` None) e esconde o `MHArms`; no `DragEnd` volta. A `MHSync` também mantém o Manny invisível todo quadro (o `DragEnd` reacende a `FirstPersonMesh`).
- **Livros:** a `SyncHold` agora mede o `hand_r` do `Body` do `MHArms` (antes, o da `FirstPersonMesh` do Manny). Com o Manny, os livros flutuavam acima da mão dela, que tem o braço mais curto.
- **Testado no PIE:** olhar para baixo (mãos, mangas e peito, sem atravessar), corpo de fora (ejetado com F8), pose do arrasto e a volta, 3 livros a -35° e a -65° (mão sob a pilha), agachar com livros.
- **Falta:** teste do usuário andando e nos sustos; decidir se mostra as pernas em primeira pessoa; conferir a abdução completa (o `DragPlace` move o `CharacterMesh0`, e o `MHWorld` está preso a ele).
- **Atenção (git):** o `BP_LibraryCharacter` agora depende do `BP_MH_Protagonista`, que fica fora do git. Num clone sem a pasta `Protagonist/`, o jogador não aparece (restaure a pasta como a dos Customers; ver SETUP).
- **Ferramentas de teste no PIE** (rodar no console com `py`): `Tools/pie_call_player.py knock|dragbegin|dragend|books <pitch>|pitch <p> [yaw]|crouch|uncrouch`, `Tools/pie_inspect_player.py` (estado das malhas no `Saved/mh_proto.log`) e `Tools/pie_look_player.py <dist> <yawOffset> <z>` (câmera do editor no jogador depois do F8). Teclas reais do computer use chegam ao PIE (W/S/C, mouse para olhar).
- **Boca vista por dentro (corrigido, 2026-11-26):** depois do puxão, ao andar e olhar para baixo, aparecia a língua dela. A câmera fica dentro da cabeça do `MHWorld`, e o `FirstPersonPrimitiveType` sozinho não voltava a esconder o corpo do dono depois do arrasto. Agora a `MHSetView` também liga o `OwnerNoSee` (desligado só no arrasto), e o rosto e os grooms do `MHWorld` ficam sempre com `OwnerNoSee`. A sombra continua: o `OwnerNoSee` não tira a sombra. Conferido pelo usuário.
