# Biblioteca Fab do usuário (seleção)

Extraída em 2026-10-29 da página `fab.com/library` (372 de 376 itens capturados; 141 da Dekogon Studios, 32 da Hivemind, 18 Quixel Megascans, 11 Epic, 11 RagTarock, 8 Barrel & Bark…).
**Quase nenhum está baixado**: só o Lyra está "No disco". Para usar um item, baixe pelo Fab ("Add to Project") e confira o conteúdo antes de levar ao `library_project`.
Pelo CLAUDE.md, pacotes de terceiros não são editados: duplique para `/Game/Library/`.
Os números são a posição na lista extraída; o título é o nome na Fab (busque por ele). Itens marcados ⭐ são os primeiros a conferir.

## Computador / eletrônicos
- ✅ **Em uso: 1996 Police Headquarters** (Dekogon, projeto completo, UE 4.25–4.27 e 5.0–5.7, classificação Mature). Os meshes `SM_Computer*` e `SM_Telephone` foram migrados para `/Game/PoliceDepartment/` e o conjunto `SM_Computer_01a` está no balcão. O monitor tem slot `Screen` próprio (`MI_Screen_01a`) e é por ele que a tela fica ligada.
- **Jobsite VOL.12 - Office** (Dekogon) — já no projeto em `/Game/JOBSITE/VOL12_Office/` (nomes `SM_Tanker_*`); mesas, fichários e material de escritório. Ainda não inventariado.
- **Jobsite VOL.3 - Postal Service** / **VOL.6 - Movies & Rental** (Dekogon) — balcão de atendimento e aluguel, tema parecido com empréstimo.
- ❌ **Retro 80's VOL.2 - Electronics** é só equipamento de som (vitrola, caixas, vinil), sem computador; serve de prop atmosférico.
- ❌ **1970 Office Environment** é um escritório militar de 1971 (Saigon): tom errado.

## Livraria / biblioteca
- ⭐ **Modern Library / Bookstore Environment** (Edanur Artworks) — estantes, livros, mobiliário.
- ⭐ **Book Generator** (Meshingun Studio) — gera livros proceduralmente.
- **Modular Stationer Environment** (Barrel & Bark) — já é a base da cena (`/Game/Stationer/`).
- **Museum and Gallery - Archinteriors Vol 10** (Evermotion), **Modern Art Museum** / **ShowRoom Museum** (PainterNur) — quadros, molduras, iluminação de galeria.
- **Gothic Furniture Props Vol1** (Meshingun) — mobília para a fase mais sombria.

## Café / mezanino
- ⭐ **Restaurant VOL.3 - Dining Decor** (Dekogon), **Double Triangle Diner** (Dekogon), **University Cafeteria** (Kaan Artworks).
- **Stores VOL.1 - Shop and Grocery Displays**, **Grocery VOL.3 - General Goods** (Dekogon).

## Decoração, portas, materiais de interior
- **Suburbs VOL.24 - Apartment**, **VOL.25 - Knick Knacks**, **VOL.1 - Wall Decor** (Dekogon).
- **Realistic Materials VOL.4 - Suburban Interiors** (70+ materiais), **VOL.9 - Town Surfaces** (Dekogon).
- **Buildings VOL.12 - Town Doors**, **Assortment of Doors** (Kingboars) — para a porta que abre.
- **Steam Punk Lamp 19th century decor** (Ayon), **Lighting VOL.3 - Industrial** (Dekogon).
- **Modern Home / House Interior with 22 Paintings** (PainterNur).

## Terror (fases futuras: P.T. / Silent Hill)
- ⭐ **Horror and Decay VOL.1 Organics / VOL.2 Urban Debris / VOL.3 Quarantine-Hospital / VOL.5 Urban Surfaces** (Dekogon).
- ⭐ **Decals VOL.3 Blood / VOL.4 Decay / VOL.5 Grunge**, **TRASH VOL.2 - Floor Debris** (Dekogon) — sujeira e sangue por cima da cena existente.
- ⭐ **Bodycam Backroom VHS Effect** (Kaizen) — pós-processo VHS, bom para o estilo P.T.
- **Immersive Dark Ambient Music Pack** (WOW Sound) — áudio.
- **Holidays VOL.1/2 - Halloween Decor**, **Bodybags - Corpses** (Dekogon).
- **Apocalyptic Hospital**, **Modular Hospital** (Hivemind), **Hospital Props VOL.1/VOL.3** (Dekogon), **Quarantine Medical Tent**.
- **Anemoia Manor**, **Albert Manor** (Dekogon), **Abandoned Cathedral** (RagTarock), **Derelict Corridor Megascans Sample**.

## Rua / exterior (quando o jogador sair da livraria)
- **Meridian 1988** (Dekogon): Cedar Point School, King Wash Stripmall, 14 Widow Street, 55 Elm Street, Sacred Pines Church, Moose's Dock House — a vizinhança inteira, estilo cidade pequena americana (Silent Hill).
- **Volstok District**, **Signage VOL.3/VOL.4/VOL.5**, **Decals VOL.1/VOL.2**, **Realistic Materials VOL.6 Roads & Sidewalks**, **Buildings VOL.13 Sidewalks**, **Fences VOL.4**, **Foliage VOL.23/26/34** (Dekogon).
- **School VOL.1 Interior / VOL.2 Classroom / VOL.3 Science Lab**, **High school Science Lab (90's)** (Dekogon) — interiores de escola.
- **Graveyard / Cemetery VOL.1–5** (Dekogon), **Railway Street** (Tennur).
- **Graffiti Street Art Decals** (Casein), **Procedural / Megascans** para vegetação.

## Plugins / sistemas úteis
- **Inventory System** (Gamma Studio), **Advanced Phone System V3** (SametStore) — pode inspirar o telefone da recepção.
- **Tempered Glass – Destructible Glass System**, **Destruction System** (UB).
- **MetaHuman Animator** (Epic) — para quando os MetaHumans entrarem.

## Plano de enriquecimento do interior (2026-10-30, a aprovar: nada foi colocado na cena)
Princípio: pouca coisa, só o que combina com uma livraria/biblioteca aconchegante dos anos 80/90 que vai azedando. **Primeira passada: no máximo ~30 atores novos.** Os pacotes abaixo já estão no projeto (Jobsite VOL.12 e VOL.3 em `/Game/JOBSITE/`, Apartment em `/Game/SUBURBS/VOL24_Apartment/`, Wall Decor em `/Game/House_Decor/VOL1_Wall_Decor/`); usar sempre as malhas `Meshes/NN` (Nanite; o Lumen está ligado) e nunca editar os pacotes.
As folhas de miniaturas usadas na leitura estão em `scratchpad` (veja o relatório) e foram geradas por `CaptureAssetImage` → `Saved/Thumbs/` (ignorado pelo git).

### O que cada pacote realmente tem (lido nas miniaturas)
- **Jobsite VOL.12 – Office:** `Stationery` (57: fichários verdes 01A–C, pranchetas, pastas pardas, porta-canetas com lápis 01P/01Q, post-its, canetas, fotos P&B 01AG–AK, cartões escritos à mão 01AL–AO, pilhas de papel 01AV–AZ), `Books_Mail` (01A–G são **livros/brochuras**, 01H–K envelopes), 2 cadeiras giratórias cinza, 5 porta-retratos, `Tanker_Desk` (escrivaninha de aço dos anos 50: 01A, 01J, 01K; gavetas; **01I é uma chave**), `Water_Cooler` (bebedouro, galão, copos), `Utility_Storage` (arquivos de aço de 4 gavetas 01G/01I fechados, 01H/01N abertos, de 3 gavetas 01K/01L, lata de lixo 01Q, caixa térmica vermelha 01R/01U). Atenção: os post-its 01AP–AU têm texto de delegacia ("DO NOT EAT PIE EVIDENCE"); evitar, exceto 01AR ("BUY MORE INSTANT COFFEE"). O porta-canetas 01O/01R traz um brasão oficial: preferir o 01P/01Q.
- **Jobsite VOL.3 – Postal Service:** `Large_Storage_Shelf_01a` (armário de **8 escaninhos** cinza), `Office_Sorting_01a/b` (bancada com escaninhos), `Post_Desk_01a` (estação grande), banquinhos altos `Post_Desk_01b/c`, **carimbos de borracha** `Post_Desk_Set_02a/b/c`, almofadas de tinta `02m` (azul) e `02n` (rosa), `Newspapers_01a–f` (pilhas), **carrinhos de arame** `Storage_Rolling_Bin_01a/b/c`, `Rolling_Shelf_01a` (estante com rodas e caixas) e `01b` (grade de arame), carrinhos de mão `Trolly_Set_01a/c`.
- **Suburbs VOL.24 – Apartment:** **sofá de dois lugares florido** `Furniture_01f` (tons amarelo-verde dos anos 70), mesinha de centro `Coffee_Table_01a`, criados-mudos `Furniture_01m/n`, otomana com almofada verde `Furniture_01o`, banco `Furniture_01p`, banco com prateleira `Furniture_01k` (de telefone), cadeira `Wooden_Chairs_01b` e banqueta `01a`, **luminárias de mesa laranja** `Light_Props_01j/k/l`, arandelas `01c–g`, pendentes `01h/i`, ventilador de teto `01a/b`, prateleiras de parede `Wall_Shelfs_01a/b/c` (a 01a tem ganchos). Não há poltrona individual. Os tapetes `Carpets_Towels` são toalhas, não servem.
- **Suburbs VOL.1 – Wall Decor:** quadros com moldura de madeira. Os que valem: botânicos e pássaros `Wall_Frame_14e/f/g/h/i/j` e `15f/g/h/i/j` (as imagens borradas nas miniaturas são só streaming de textura). `Wall_Decor_Set_05a–c` são cinzas/placeholders. Os `Wall_Frames` (40) não foram vistos, são conjuntos.

### Onde e o quê (proposta)
**A. Atrás do balcão (espaço do atendente: X -730…-538, Y 44…292; parede dos fundos X≈-740, `Wall24/25`).** O tampo do balcão fica livre para os livros e o computador (`Zone_Counter` Y 48–210, computador Y 217–286), então os adereços vão para a parede de trás, sem tirar espaço do jogador (manter ≥ 100 cm de passagem a partir do `PlayerStart` (-640, 170)):
1. 1 arquivo de aço de 4 gavetas fechado (`Utility_Storage_01g`) encostado na parede, perto de Y 70.
2. 1 armário de escaninhos (`Large_Storage_Shelf_01a`) ao lado, com 3–5 livros de `Books_Mail_01a–g` nos escaninhos (decorativo, é "reserva").
3. 2 prateleiras de parede (`Wall_Shelfs_01b`, `01c`) acima, a ~Z 150–185, com: porta-canetas `Stationery_01p`, 2 fichários `Stationery_01a/b`, carimbo `Post_Desk_Set_02a`, almofada de tinta `02m` e uma luminária laranja `Light_Props_01j`.
4. 1 carrinho de arame `Storage_Rolling_Bin_01a` perto de Y 280, como "carrinho de devolução" (vazio, ou depois com livros de verdade).
5. Opcional: bebedouro `Water_Cooler_01a` + 1 copo.
Total ≈ 12 atores.

**B. Mezanino (sala de leitura; piso Z 330).** Canto de leitura na parede norte, a leste da `BP_BookShelfs36`, **sem encostar em estante** (livros em Y 390–409; ficar a ≥ 120 cm):
1. Sofá florido `Furniture_01f` perto de (880, 385) virado para -Y, mesinha `Coffee_Table_01a` à frente, 1 criado-mudo `Furniture_01m` ao lado com luminária laranja `Light_Props_01k`.
2. 2 luminárias laranja (`Light_Props_01j`) sobre as mesas redondas (950, 0) e (950, 250).
3. 1 pilha de jornal (`Newspapers_01c`) na mesa comprida (centro (640, 0)).
Total ≈ 6 atores.

**C. Paredes (quadros).** 6–8 quadros botânicos/pássaros (`Wall_Frame_14e/f/g/i/j`, `15g/h/i`), agrupados em 2 painéis pequenos: um acima do sofá (3) e outro perto da escada (3–4); no térreo, 2 junto à porta. **Medir** as faces das paredes antes (o pivô dos quadros ainda não foi conferido). Total ≈ 8 atores.

**D. Deixar para a fase de terror (não colocar agora):** `Stationery_01AG–AK` (fotos P&B), `01AL–AO` (cartões escritos à mão), chave `Tanker_Desk_01i`, cabos vermelhos `01BD/BE`, escrivaninhas `Tanker_Desk_01a/j/k`, `Utility_Storage` com gavetas abertas/quebradas (`01h`, `01j`, `01n`), ventilador de teto `Light_Props_01a`, Church VOL.1, Gothic Furniture, decals de decay, TRASH VOL.2.

**E. Não usar:** Apartment (cozinha, geladeira, fogão, portas, tomadas), post-its com texto de delegacia, `Trolly_Set_01e–i` (rodas soltas), Wall_Decor_Set 05a–c, Knick Knacks/Store Displays/School (não importados).

### Como executar (depois que você aprovar)
1. **Medir antes de colocar:** `find_actors` com bounds nas áreas A, B e C, `get_actor_bounds` das malhas escolhidas e foto "antes" de cada área.
2. **Colocar em lotes por área**, um script por área, **sempre com `location`, `rotation` e `scale` completos** (o `set_actor_transform` zera o que faltar), nas pastas do Outliner `Props/Counter`, `Props/Mezzanine` e `Props/Walls`. Conferir os bounds depois (nada flutuando, nada atravessando parede, `Zone_*` e estantes livres).
3. **Foto "depois"** de cada lote; você aprova ou pede ajuste antes de seguir para o próximo.
4. **Navegação:** o NavMesh não deve ganhar ilhas em cima de móveis (os `NavBlock_*` cobrem Z 40–300 no térreo e 360–850 no mezanino); móvel alto no mezanino acima de Z 360 pede buraco ou ajuste.
5. `save_assets`, atualizar `docs/SCENE_MAP.md` e este arquivo. Commit só quando você pedir (os pacotes continuam fora do git).

## Observações
- A lista completa (372) pode ser regerada com a extensão do Chrome em `fab.com/library` (rolar até o fim e ler os links `/listings/`).
- Itens da Hivemind e RagTarock são, em sua maioria, fantasia/medieval/sci-fi e fogem do tema.
