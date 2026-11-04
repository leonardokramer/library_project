# Capas dos livros (Stationer) — o que existe e como bater com o sistema

## Como as capas funcionam
- **Todas as malhas** `SM_Book_XX` (`/Game/Stationer/Meshes/Books`) usam o mesmo material `MI_BookCoversCC0` (slot `BookCoverCC0`), que lê o **atlas** `T_BookCoversCC0_B` (4096×4096, `/Game/Stationer/Textures/BooksAndPosters`). Cada malha tem o UV apontando para uma região do atlas. O atlas não é uma grade regular.
- **As capas têm título e autor impressos.** O que está na `DT_Books` precisa bater com o impresso, senão o jogador vê um texto na capa e outro no sistema.
- O atlas tem uns 70 designs distintos (estimativa visual), entre eles revistas e livros em vietnamita. Cada design tem frente e verso. O rodapé do atlas traz os 8 rótulos de gênero: Dictionaries, Science, Biography, Fantasy, Sci-Fi, Novels, Economy, History.
- **Existem 24 malhas:** 01–15, 17, 20–22, 26, 29–32 (não existem 16, 18, 19, 23–25, 27, 28 nem 33 em diante).
- Duas capas **lisas** (sem texto impresso): `SM_Book_05` (couro escuro) e `SM_Book_06` (couro com cantos dourados). Servem para livros com título à escolha, como os livros estranhos do terror.

## Mapeamento conferido (2026-10-31, fotografando as malhas)
| Malha | Título impresso | Autor impresso | Estado na `DT_Books` |
|---|---|---|---|
| 01 | A Universal Guide to Creating Book Covers | Bernhard B. Painter | ok |
| 02, 07 | Diary of Ms. Rose | Sydney Andrews | autor corrigido (mesma capa nas duas malhas) |
| 03 | L'homme qui vivait au loin | Alphonsine Beaujolie | autor corrigido |
| 04 | Summer's End | Arthur Heinlein | ok |
| 05 | (lisa) | — | título livre: "Classic Poems of the 18th Century, Volume I" |
| 06 | **The Last Borrower** (dourado, escrito por nós) | Anonymous | **livro estranho**: cópia da malha em `/Game/Library/Meshes/Books/SM_Book_06` com `M_BookStrange`; linha na `DT_Books` (gênero Novels). Ainda **não está em nenhuma estante** |
| 08 | Open Office Design | Johnny Matthews | ok |
| 09 | Lost Souls | Gregg Tielms | ok |
| 10 | Colorblind | Kevin Reich | ok |
| 11 | Cities | ilegível na textura; usamos "Jeremy & Gloria Reinstein" (a melhor leitura; o usuário aprovou) | ok por decisão |
| 12 | Chrysanthemums (Photography) | Xiaohong Zhao (na lombada) | autor corrigido |
| 13 | Theoretical Calculus | Dr. Albert Faraday | ok |
| 14 | Data Structures and Programming | John W. Matthews | autor corrigido |
| 15 | First Contact | Patric J. Picard (lido no atlas, não na malha) | ok |
| 17 | Analytic Geometry | Dr. C. Marie Matthews | autor corrigido |
| 20 | The Illusion of Democracy | Mark Cox | autor corrigido |
| 21 | Treasure of Al-Saban | Joseph Phillips | título e autor corrigidos (`DT_SeedLoans` Seed02 também) |
| 22 | Space Walk | Alex Leonov | ok |
| 26 | The Lake Murders | Nathan Hughes | autor corrigido |
| 29 | Cats and Their Humans | Freya Malcolm | ok |
| 30 | cachorro amarelo, título em escrita não latina | ilegível | **fora do catálogo de propósito** (outro idioma) |
| 31 | Fluffy Doggo | Johnny Matthews | linha nova (gênero Fantasy) |
| 32 | "Kẹo Quốc…" (vietnamita) | Hồ Nhựt Châu | **fora do catálogo de propósito** (outro idioma) |

## Armadilhas
- Mudar o **título** na `DT_Books` exige mudar também `DT_SeedLoans` (o histórico guarda só o título).
- Para fotografar as malhas: spawnar no céu (Z 30000), câmera a 30 cm olhando +X (a frente da capa aponta para -X). Luz do sol fica de costas e escurece as capas; uma `PointLight` de intensidade ~5 resolve. `CaptureViewport` **em paralelo desalinha a câmera**: chame uma por vez. O resultado base64 vem em arquivo; decodifique com Python.
- O texto pequeno (autor da Cities, por exemplo) só tem a resolução do atlas: não dá para ler dando zoom.
- `M_TmpAtlasView` (`/Game/Library/Debug`) é um material de depuração que mostra o atlas emissivo; pode ser apagado pelo Content Browser.

## Livros estranhos (o `SM_Book_06`)
- Regra do usuário: a maioria dos livros é fictícia, alguns de domínio público, e uns poucos "estranhos" aparecem ao longo do jogo (terror). As capas **lisas** (05 e 06) são as únicas em que o texto pode ser escolhido. A 05 ficou com o título comum; a 06 é o estranho.
- **Como o texto dourado funciona:** `M_BookStrange` (`/Game/Library/Materials`) mostra o atlas e, só na face da frente (normal local -X), mistura a textura `T_Book06_Gold` (PNG com alpha, 832×1282) usando a **posição local do mesh** como UV (u = y/17,2035; v = 1 − z/26,4622). Não depende do UV do atlas, então serve para qualquer capa nova. O dourado também é metálico e mais liso. Para trocar o texto: gerar outro PNG (PowerShell + `System.Drawing`; Georgia Bold 74 px; centrado) e importar com **outro nome** (o `import_file` não sobrescreve).
- O `BP_Book` identifica o livro pelo **nome da malha**. A cópia em `/Game/Library/Meshes/Books/SM_Book_06` mantém o nome `SM_Book_06`, então a linha da `DT_Books` vale. Para fazer o livro aparecer, coloque um `BP_Book` com essa malha; as estantes atuais não usam a 06.
- O texto "ANONYMOUS" ficou pequeno; se incomodar, gerar outro PNG com fonte maior.

## Livros novos com capas do atlas (feito em 2026-10-31)
**28 livros novos**, sem gerar nenhuma imagem: cada um é uma malha `/Game/Library/Meshes/Books/SM_BookX_<Nome>` (cópia de uma malha do pacote) com um material `/Game/Library/Materials/Covers/MI_Cover_<Nome>` que mostra outra capa do atlas. A linha da `DT_Books` tem o mesmo nome da malha (`SM_BookX_<Nome>`) e título/autor **iguais aos impressos na capa**. Com os 22 anteriores são **50 linhas** na tabela. Nenhum está numa estante ainda.

**Como funciona (`M_BookAtlas`):**
- Parâmetros: `UScale`, `UOffset`, `VOffset` (deslocam e esticam o UV da malha) e `UMin/UMax/VMin/VMax` (janela da capa da malha-base). **Só o UV dentro da janela é deslocado**; fora dela (a textura de páginas, no canto inferior direito do atlas) fica intacta. Sem a janela, a borda das páginas pega lixo.
- Orientação do atlas: o mosaico montado e girado 90° tem **U na horizontal e V na vertical (para baixo)**, texto em pé. Cada capa é uma jaqueta horizontal: verso (esquerda), lombada, frente (direita). As **linhas** são regulares (altura 339,2 px num atlas de 4004 px; linha k começa em y = k·339,2 + 1; a linha 10 é a faixa de rótulos de gênero). Em U, cada jaqueta tem largura própria (466–571 px).
- Cada capa nova é definida por `(linha, borda direita R, largura W)` em px do mosaico. A malha-base é a malha do pacote cuja jaqueta tem largura mais parecida (jaquetas medidas das malhas: 01 R3750 W488 linha 3; 02 R3445/507/9; 03 R2932/477/9; 04 R2448/473/9; 08 R1965/510/9; 09 R527/509/8; 12 R2520/498/8; 13 R3015/493/8; 15 R2980/480/7; 17 R2002/487/7; 20 R527/522/7; 22 R1002/474/6; 26 R3475/505/6; 29 R2570/495/5). Com `k = W_alvo/W_base`: `UScale = k`, `UOffset = (R_alvo − k·R_base)/4004,3`, `VOffset = (linha_alvo − linha_base)·339,2/4004,3`; janela `UMin=(R_base−W_base−4)/4004,3`, `UMax=(R_base+4)/4004,3`, `VMin=(linha_base·339,2−4)/4004,3`, `VMax=((linha_base+1)·339,2+4)/4004,3`.
- Usar uma malha-base de largura parecida dá tamanhos de livro variados e evita esticar o texto. Se a frente do alvo é mais larga que a média (caso de *Highways* e *Runaway*), superestime W (usei 600 e 560) para não cortar o título.
- A lombada e a frente foram conferidas renderizando cada livro (frente e lombada). **Atenção:** a fórmula acima (`k = W_alvo/W_base`, ancorada só na borda direita) deixava a lombada fora do lugar em vários livros (texto do verso na lombada, lombada na frente). Foi **substituída em 2026-11-01** pelo método de âncora na lombada (próxima seção).

**Como o atlas foi lido:** plano 10×10 m no céu com `M_TmpAtlasView` (emissivo), câmera a 232 cm olhando para baixo (≈ 1 px por texel; hfov 90°, 4,004 px/cm), 15 capturas (5 linhas × 3 colunas) uma por vez; mosaico montado com `System.Drawing` (PowerShell) e girado 90°. Para achar a borda direita de cada jaqueta: leitura visual aproximada + ajuste para a borda vertical mais forte (código C# via `Add-Type`). Onde o fundo é claro a borda é fraca, então vale a leitura visual.

### Catálogo dos livros novos (título e autor impressos)
| Malha `SM_BookX_…` | Título | Autor | Gênero |
|---|---|---|---|
| CurveInThePlane | Curve in the Plane | Tommas Raibows | Novels |
| Weather | Weather: Untamable Force | Jeff E. Storm | Science |
| TheAttic | The Attic | Paul Torres | Novels |
| JesterVampire | The Jester Vampire | Caroline Therrien | Fantasy |
| FourthTarget | The Fourth Target | Jean-Gregoire Malvoisin | Sci-Fi |
| Symmetry | Symmetry | Matthew Roberts | Science |
| SkylandTales | Skyland Tales | Fynn G. | Fantasy |
| SkylandStory | Skyland Story | Fynn G. | Fantasy |
| SadRiseMountain | Sad Rise Mountain | Jason Adams | Novels |
| PilotDreams | Pilot Dreams | Timothy Peterson | Novels |
| PeepingTim | Peeping Tim | Timothy Peterson | Novels |
| MorningDew | Morning Dew | Jonathan Campbell | Novels |
| HoustonMurders | The Houston Murders | Daniel Hill | Novels |
| Highways | Highways | John White | Novels |
| FinalGamble | The Final Gamble | Nicholas Lopez | Novels |
| FinalLight | Final Light | John D. Raster | Fantasy |
| Escapee | Escapee | Michael Martinez | Novels |
| DontBother | Don't Bother | Karl Lasch and Nick Hoff | Economy |
| LeadingFromTheBack | Leading from the Back of the Line | Jessica Stuzzart | Economy |
| Polaroid | Polaroid | Jack S. Toneg | Novels |
| Runaway | Runaway | Midas Cole | Biography |
| DSharpForBeginners | D## For Beginners | Lennon Sharpe | Science |
| SaturnRecoiling | Saturn Recoiling | Joyce Smilecht (leitura aproximada: letra muito miúda) | Sci-Fi |
| Mars | Mars | Mark Watney | Sci-Fi |
| LakeMurdersII | The Lake Murders II | Nathan Hughes | Novels |
| HuntingTechniques | Hunting Techniques | John H. Shotgun | Science |
| HareApparent | Hare Apparent | Wilma Palmer | Novels |
| Fuerteventura | Fuerteventura Travel Guide | Mike W. Traveler | History |

### Revistas maiores que o vão da prateleira (corrigido em 2026-11-04)
- A malha das revistas tem 32,3 cm de altura (origem na base), mas o vão entre as tábuas da estante 26 é de **30 cm** (35 cm só na primeira fileira): as revistas atravessavam a tábua de cima (medido com `trace_world` para cima a partir de cada prateleira).
- **Primeira tentativa (não serve):** escala 0,9 no componente `Mesh`. Mas o `Mesh` é a **raiz** do `BP_Book`, então a escala dele é a escala do ator, e o tick (`SetActorTransform` no estado 1 e 2) e o `Drop` voltam tudo para 1: a revista crescia ao ser pega e voltava grande.
- **Correção definitiva:** variável `BP_Book.ExtraShrink` (float, instance editable; **0 = tamanho normal**, por isso os 1.632 livros comuns não mudam; as 102 revistas têm **0,1**). A escala efetiva é `escala × (1 − ExtraShrink)`: `BP_Book.ScaledTarget(T)` (aplicada ao alvo do estado 2 no tick, antes do `TInterpTo` e do `SetActorTransform` final), `ScaleHoldTransform` (estado 1: `HoldScale × (1 − ExtraShrink)`) e `Drop`. Altura da revista: 32,3 → 29,1 cm, e a base continua na prateleira. Testado no PIE (pegar e guardar): fica em 0,9.
- ⚠️ `Tools/shelf_populate.py` recria as revistas com `ExtraShrink` 0: se repovoar a estante 26, ponha `ExtraShrink = 0.1` e escala 0,9 em cada revista. Outro livro grande demais para o vão: use o mesmo `ExtraShrink`. `GetBookExtents` ainda usa as dimensões da malha sem o encolhimento, então a posição na mão fica ~10% mais afastada (não incomoda).

### Revistas e o livro em francês (acrescentados depois, a pedido do usuário)
Decisão do usuário: inglês, francês, espanhol e português entram; **vietnamita (e tailandês) ficam de fora** por parecerem estranhos. Novo gênero **Magazines**. Total agora: **61 linhas** na `DT_Books` (39 livros novos no total).

Base das revistas: malha `SM_Book_30` (fina, 24,3×32,3×2,65 cm; jaqueta R 2075, W 533, linha 5), proporção parecida com a de uma revista. Frente-só: usei `W_alvo = largura_da_frente / 0,45` e `k = W_alvo/533`. A parte "verso" da janela mostra a arte vizinha (só se vê ao virar). A `La culture de la framboise` usou a malha 20 (R 540, W 535, linha 0).

| Malha `SM_BookX_…` | Título | Autor | Gênero |
|---|---|---|---|
| Mag_Matsulki | Matsulki: Tetris Time | Vários autores | Magazines |
| Mag_BringWaterproofs | Bring Waterproofs | Vários autores | Magazines |
| Mag_IntlGeography | International Geography: Coffee | Vários autores | Magazines |
| Mag_Glass | Glass | Vários autores | Magazines |
| Mag_Business | Business | Vários autores | Magazines |
| Mag_Liquid | Liquid: Mantaflow | Vários autores | Magazines |
| Mag_Species | Species | Vários autores | Magazines |
| Mag_EngineDoctor | Engine Doctor | Vários autores | Magazines |
| Mag_Africa | Africa | Vários autores | Magazines |
| Mag_MedicineToday | Medicine Today | Vários autores | Magazines |
| Framboise | La culture de la framboise | Adrienne Renaud | Science |

**Ficaram de fora de propósito:** capas em vietnamita/tailandês (Thế Giới Bánh, Tiếu Xanh, Hoạt hình nâng cao, Kẹo Quốc, Đôn Hổ, o cachorro amarelo). Também sobrou uma capa lisa de couro verde-oliva (linha 5, R≈3550) sem texto, boa para um livro estranho futuro. O autor aproximado de *Saturn Recoiling* ("Joyce Smilecht") fica como está, por decisão do usuário.

## Gêneros revisados e estantes refeitas (2026-10-31)
- Gêneros que não faziam sentido foram corrigidos na `DT_Books`: Classic Poems e Lost Souls → Novels; Colorblind → History (o verso fala de racismo); Chrysanthemums → Science (é fotografia). Novo gênero **Guides** para manuais e guias (Book Covers Guide, Open Office Design, Data Structures, D## For Beginners, Hunting Techniques, Fuerteventura Travel Guide). **Dictionaries** deixou de existir.
- **Sinopses corrigidas pelo verso da capa:** Diary of Ms. Rose, Colorblind, Chrysanthemums, Lost Souls, Treasure of Al-Saban, Space Walk, First Contact e Summer's End contradiziam o que está impresso. **Regra: ao escrever uma sinopse, leia o verso da capa no atlas (as faixas do mosaico).**
- As 24 estantes de livro foram refeitas com `Tools/shelf_populate.py` (59 títulos; 1.734 livros). Escala de enchimento automática: 0,5 no térreo e 0,6 no mezanino. Veja a tabela em [SCENE_MAP.md](SCENE_MAP.md) (as estantes 26 = Magazines e 19 = Guides são do `BP_BookShelf_Library`, com placas novas).
- O script aceita malhas `SM_BookX_*`; as dimensões (meia espessura, profundidade) da cópia são as da malha-base (veja `GEN` no script).

## Próximos passos
1. Revistas: a parte "verso" da janela mostra arte vizinha e as lombadas ficam brancas (revista não tem lombada impressa). Se incomodar, trocar a malha-base por uma própria.
2. Os livros novos usam o material simples `M_BookAtlas` (sem sujeira/riscos e sem normal map): de perto ficam um pouco mais lisos que os do pacote.

## Correção das lombadas (2026-11-01)
Problema: o usuário viu lombadas tortas (Skyland Story, Runaway, Jester Vampire, Framboise, Highways...) e revistas com a lombada toda branca.
- **Causa:** a escala única só acertava a borda direita da capa; a largura `W` medida de algumas jaquetas estava errada (Skyland Story: o centro real da lombada fica em x=868, não em 833) e a lombada de cada jaqueta tem largura própria.
- **Método novo (livros, 29 `MI_Cover_*` fora as revistas):** ancorar em **duas medidas confiáveis**: o **centro da lombada** `c` (centro do texto vertical da lombada, lido no mosaico `atlas_upright.png` com régua) e a **borda direita da frente** `R`. Com `c_b`/`R_b` da malha-base (mesma medida): `UScale = (R_t − c_t)/(R_b − c_b)` e `UOffset = (c_t − UScale·c_b)/4004,3`. A janela (`UMin..VMax`) e o `VOffset` ficam como estavam.
- **Centros `c_b` das malhas-base** (px do mosaico): 01=3501, 30=1809, 29=2325, 22=764, 26=3223, 20=272, 17=1760, 15=2739, 09=273,5, 12=2272, 13=2767, 08=1719, 04=2212, 03=2690, 02=3192. Espessura física da lombada na malha: `X_malha · px/cm`, com `px/cm = (R_b − c_b)/(X/2 + Y)` (confere com as bandas medidas: 09=54 px, 30=26 px).
- **Centros `c_t` dos livros** (px): Framboise 280, Weather 290, TheAttic 1899, JesterVampire 2396, FourthTarget 2918, Symmetry 3452, SkylandTales 301, **SkylandStory 868**, SadRiseMountain 1422, PilotDreams 1947, PeepingTim 2469, MorningDew 2995, HoustonMurders 273, Highways 1288, FinalGamble 1855, FinalLight 2349, Escapee 2851, DontBother 3377, LeadingFromTheBack 260, Polaroid 757, Runaway 1250, DSharpForBeginners 2809, SaturnRecoiling 1249, Mars 1729, LakeMurdersII 2713, HuntingTechniques 780, HareApparent 1265, Fuerteventura 2260, CurveInThePlane 3295.
- **Limite conhecido:** a lombada de *Runaway* na arte é fina (faixa vermelha de ~28 px) e a da malha é mais larga, então sobra um pedaço branco ao lado do texto. Corrigir exigiria um mapa de U em 3 trechos (verso|lombada|frente) no material; não foi preciso para o resto.
- **Revistas:** o `M_BookAtlasMag` (cópia do `M_BookAtlas`) mistura, **só na face da lombada** (normal local −Y, máscara `saturate(−10·ny − 3)`), uma textura `SpineTex` por revista (`/Game/Library/Materials/Spines/T_Spine_<Nome>`, 128×1560, gerada com PIL: cor de fundo da capa + título vertical). UV pela posição local: `u = 0,5 − x/2,65`, `v = 1 − z/32,34` (malha-base 30: x ±1,325; z 0–32,34; lombada em y=0). Para as 10 `MI_Cover_Mag_*`, `UScale/UOffset` foram refeitos pela **borda esquerda da frente `s1`** e `R`: `k = (R − s1)/(2075 − 1822,75)`, `UOffset = (s1 − k·1822,75)/4004,3` (frente/R em px: Matsulki 2311/2567, Bring 2570/2800, IntlGeography 2834/3055, Glass 283/543, Business 815/1080, Liquid 1363/1620, Species 1904/2162, Engine 2444/2701, Africa 2987/3246, Medicine 3533/3791).
- **Para fotografar/conferir:** spawne as malhas no céu (Z 30000) lado a lado (X de 5 em 5 cm para lombadas, Y de 27 em 27 para frentes) com uma `PointLight` intensidade 5. A luz do teste deixa as cores escuras mais cinza (os livros pretos do pacote também): não é erro do material.
- **Revistas "tortinhas":** no PIE, nenhuma das 102 revistas tem pitch/roll/yaw diferente do esperado (0 inclinadas), então a inclinação que o usuário viu não vem da física nem do `shelf_populate.py`. Se ainda parecer torta no jogo, é a lombada branca (agora corrigida) sem sombra de relevo; reavaliar com a foto do usuário.
