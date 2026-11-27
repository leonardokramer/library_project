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
