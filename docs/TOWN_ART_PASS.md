# Passe de arte da rua (pedido do usuário em 2026-11-27, depois do 3º teste)

Feedback: "ainda tá com a lacuna no horizonte, a linha no céu, a roda do carro atravessa o chão, o poste solta luz do megafone e não de uma lâmpada, a cena tem muitos espaços vazios. Quero beleza, luzes, LEDs piscando, medo, mas a sensação de que o jogo é muito maior. Preencha com vontade, detalhes, coisas a mais. Olhe como Silent Hill tem bastante coisa na cena." Referências: SH2 remake (rua com semáforos), SH f (vielas japonesas apertadas, muitos postes, fios, luminárias com lâmpada, janelas acesas, poças, plantas, entulho), Townfall (muros, árvore seca, janela acesa ao longe).

## Ordem de trabalho
1. **Defeitos:**
   - carro com a roda no chão: o `CAR_` wagon está em cima do meio-fio; tirar dele e conferir o Z;
   - luminária "megafone" (`SM_Light_Set_NN_61e`): trocar por luminária de braço com lâmpada visível e emissiva no ponto da luz;
   - linha no céu e cunha no horizonte: o envelope de névoa tem bordas (elipsoide do `LocalFog` x caixa); resolver de vez (segundo volume de névoa acima do telhado e a caixa toda dentro da névoa, ou material de céu em gradiente).
2. **Encher a rua (clutter):** sacos de lixo, caçambas, lixeiras, caixas, jornais, folhas e entulho no chão e nas sarjetas, poças, arbustos e mato nas frestas, bicicleta, carrinho de compras, caixas de correio, hidrantes, bancos, placas de rua, cones e cavaletes (rua bloqueada = limite), transformadores e mais fios cruzando a rua, postes extras (como nas referências japonesas, vários em fila).
3. **Luz e vida:** janelas acesas (quentes, fracas) em algumas casas, letreiros de neon piscando (KING WASH falhando; um letreiro novo de DINER na loja do sul), LEDs âmbar dos semáforos (já piscam), luminárias de varanda acesas, uma vitrine acesa.
4. **Profundidade:** silhuetas em camadas ao fundo (casas e pinheiros já; igreja quando o download acabar), postes e fios sumindo na névoa nas duas pontas da rua.
5. Medir o desempenho, fotos, docs (SCENE_MAP "Bairro"), perguntar sobre o commit.

Pacotes disponíveis: Meridian 55 Elm (inteiro), 14 Widow (inteiro), King Wash (enxugado: só o que a cena usa), FENCES, SIGNAGE (sem placa de STOP), LIGHTING VOL5, BUILDINGS VOL13 (calçadas; tem `SM_Drainage` e grama), REALISTIC_MATERIALS VOL6 (decalques de rua `MI_Road_Decal_*`, `MI_Street_Decal_01a`). A igreja Sacred Pines estava baixando (51%).

## Feito (2026-11-27)
- Luminária de braço com lâmpada acesa (SM_Town_CobraLight, Blender, lente MI_Town_LampLens), 9 postes em fila dos dois lados, 33 fios; carros fora do meio-fio.
- Tools/town_clutter.py (CL_, 204 objetos): folhas e lixo nas sarjetas, sacos/caixas/lixeiras nas calçadas, mato nas bases, entulho nos becos, brinquedos e bicicletas nos quintais, 4 janelas acesas (abajur + luz quente).
- Caixa de névoa fechada + EmissiveDay 0,3 / EmissiveNight 0,12 gravados na instância: sem linha no céu nem cunha (conferido às 18:43–19:38).
- Falta: letreiro DINER piscando, neon do KING WASH falhando, igreja (download a 100%), barreira de rua fechada ao sul, medir o desempenho.

## 4º teste do usuário (2026-11-27, noite): ainda não pegou o feeling
Feedback: "a planta tá atravessando a porta, não consigo sair. A linha no céu ainda existe. Olhando de longe parece que tem um troço ao redor. Não é só cheia de detalhe, é cheia de casa, construção, coisa; olha esse espação sem nada. Quero uma coisa **opressora** como as imagens de Silent Hill, para que a pessoa pareça **pequena perto da cidade**."

**Defeitos:**
1. **Planta na porta:** a árvore de vaso da Stationer ao lado da porta (dentro da `L_Library`) atravessa a folha aberta e bloqueia a saída. Mova a **instância** (nunca o asset da Stationer) para longe do arco da folha (a folha abre para dentro a 95°; porta em Y 164..251, X ~1040).
2. **Linha no céu / "troço ao redor":** é a **caixa de névoa** (`BP_OutsideFog`: cubo `FogFar` 132×184×29 m + paredes `Block*`). De longe se vê a caixa como um prédio marrom com aberturas, e de dentro a quina do topo e a borda do `LocalFog` viram linhas. **A caixa não resolve: troque o método.** Sugestão: uma **cúpula esférica invertida** (sem arestas) com material unlit na cor da névoa e com o mesmo emissivo dia/noite, raio ~70 m em volta da rua, mais um `LocalFog` esférico (ou a névoa de altura global, com `StartDistance` para não afetar o interior). Confira de 5 lugares (porta, meio da rua, cruzamento, olhando para cima e por cima da livraria) de dia e às 19:30.
3. **Horizonte com borda:** o chão (`ST_Ground`) e o asfalto acabam numa linha reta visível (foto com a rua terminando seca na névoa). Feche as pontas da rua com **construções**, não com névoa.

**Direção nova (o mais importante): centrinho de cidadezinha americana denso, não bairro aberto e nem cidade grande.**
Correção do usuário: "precisa fazer sentido como vilarejo, cidadezinha. Eu real preciso que você busque referências para entender." **Antes de montar qualquer coisa, pesquise referências** (WebSearch e imagens): o centro de Silent Hill (SH1, SH2 e remake, SH3, SH Downpour, SH f), Townfall e fotos reais de *small town main street USA* / *downtown historic district* (Main Street de cidade de 2–10 mil habitantes, anos 70–90, Nova Inglaterra e Meio-Oeste; Toluca Lake/Brahms; Centralia PA, que inspirou SH). Escreva um resumo do que se repete (altura, recuo, materiais, o que fica entre os prédios, como a rua termina) neste doc e mostre ao usuário **antes** de colocar.
O que já se sabe dessas referências (confirmar na pesquisa):
- A rua da livraria é a **Main Street do centrinho**: fileira contínua de prédios comerciais de tijolo de 2–3 andares, parede com parede, vitrine embaixo e janelas de apartamento em cima (barbearia, farmácia, lanchonete, loja de penhores, cinema velho, banco, correio). Sem gramados nem terrenos vazios no centro.
- Os **becos** e as ruas laterais levam às casas de madeira, em lotes estreitos e próximos (é aí que entram as casas da Meridian e o trailer, mais apertados que hoje), com cerca de arame, garagem e quintal pequeno.
- Marcos maiores que o resto para dar escala ao fundo: igreja com torre, caixa-d'água, prédio da prefeitura ou hotel antigo de 4–5 andares, letreiro de motel/cinema; aparecem por cima dos telhados, em camadas, sumindo na névoa.
- Acabar com os gramados e terrenos vazios (`Lawn`, quintais abertos, lote do trailer): os dois lados da rua viram **fileiras contínuas** (cascas servem: fachada + telhado; BUILDINGS VOL13, King Wash, casas da Meridian em fileira).
- De qualquer ponto da rua, a visão deve bater em construção a no máximo 30–60 m (rua fechada nas pontas por prédios, uma curva ou uma barricada com prédio atrás); a névoa só come o que está atrás.
- Densidade vertical: placas e letreiros saindo das fachadas, marquises, escadas de incêndio, toldos, varais de fios cruzando a rua, postes altos em fila.
- Luz: janelas acesas espalhadas pelos andares altos, neon falhando (DINER, KING WASH), LEDs âmbar piscando.
- Referências do usuário: SH2 remake (rua com semáforos), SH f (vielas apertadas), Townfall.
- Plano + fotos antes de colocar (regra do usuário); medir desempenho (último: 17,4 ms na vista do balcão, antes da casa D, pinheiros, postes e entulho).
