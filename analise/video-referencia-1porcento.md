# Análise do vídeo de referência — "E se você melhorasse só 1% por dia?"

Vídeo original: 85,5 s · 576×576 (quadrado) · 30 fps · narração contínua do início ao fim (sem pausas até 82,5 s) · marca d'água `@gryn.red`.

> Observação importante: **não é animação 3D.** É *motion graphics 2D* minimalista em estilo "neon / linha branca brilhante" sobre fundo preto. Isso é ótimo: é bem mais simples e barato de produzir que 3D.

---

## 1. Identidade visual (o "look")

| Elemento | Como é feito |
|---|---|
| Fundo | Preto puro (#000) com uma **vinheta radial cinza bem suave** no centro, dando sensação de "palco iluminado". Em algumas cenas aparece um grid de pontinhos quase invisível. |
| Cor | **Monocromático**: só branco e tons de cinza. Nenhuma cor até o card final. |
| Glow | Todo traço/ícone branco tem **brilho (bloom)**: o objeto + uma cópia desfocada por trás (blur 10–20 px, opacidade 60–80%). É isso que dá o ar "premium". |
| Ícones | *Line art* com traço grosso e cantos arredondados: boneco (círculo + "pílula"), livro, pote de moedas, haltere, sofá, lâmpada, chip "IA", celular, planta com raízes, triângulo. |
| Personagem | Boneco sem rosto: **círculo (cabeça) + retângulo arredondado (corpo)**, preenchido branco com glow. Versões "secundárias" ficam em cinza/desfocadas. |
| Linha do chão | Uma linha horizontal fina atravessando a tela inteira — ancora todas as cenas. |
| Tipografia | **Título no topo**, caixa-alta, fonte sans-serif *black/extra-bold* pequena com letter-spacing largo (estilo Montserrat Black / Inter Black). Subtítulo menor, cinza, logo abaixo. Números grandes (1%, 1,01, 365) em bold com glow. |
| Balões | "Pílulas" brancas com texto preto (`+1%`, `≈ 38×`, `< 3%`) ou contorno branco com texto branco (`AMANHÃ EU COMEÇO`, `NÃO FUNCIONA`). |
| Gráficos | Eixos com seta, label pequenino "DIAS", curva branca grossa com glow + ponto (bolinha) na ponta, linha tracejada para comparação. |

## 2. Como as animações funcionam (mecânica)

Analisando a 6 fps, todas as transições se resumem a **6 movimentos básicos**, sempre com *easing* suave (ease-out / ease-in-out), nunca linear:

1. **Texto "máquina de escrever" (typewriter)** — o título do topo aparece letra a letra no ritmo da fala (ex.: `E SE VOC…` → `E SE VOCÊ MELHORASSE`). Na troca, o texto antigo some do mesmo jeito ou com fade. **É a legenda do vídeo** — sincronizada com a narração.
2. **Fade + scale-in ("pop")** — ícones e números entram de opacidade 0 → 1 com escala ~0,8 → 1,0 (às vezes um leve *overshoot* 1,05). Ex.: o `1%` surge acima do boneco.
3. **Desenho de linha (stroke draw / trim path)** — curvas de gráfico, eixos, raízes da planta, setas e o triângulo são "desenhados" do início ao fim do traço. A bolinha da ponta acompanha a linha.
4. **Câmera/cena deslizando (pan)** — a cena inteira desliza horizontalmente para dar lugar ao próximo objeto (livro → pote de moedas → haltere entram pela direita empurrando o anterior). No final, câmera **desce/sobe** (acima do chão vs. raízes abaixo do chão).
5. **Zoom / reenquadramento** — o boneco "cresce" ou a câmera aproxima/afasta (o boneco fica maior quando o 1% aparece, depois diminui quando "parece nada").
6. **Ênfase** — balão aparece com pop, ícone de "X" (⊗) entra com pop para negar algo, elementos secundários ficam cinza/desfocados (*depth of field* fake) para destacar o principal.

Regras de ritmo observadas:
- **Uma ideia por frase, uma mudança visual por frase** (~1,5–3 s cada). Nunca há tela parada por mais de ~2 s.
- **Continuidade de objetos**: o mesmo boneco/gráfico é reaproveitado e transformado em vez de cortar (o boneco vira o boneco no sofá; o gráfico de 365% vira a curva de 38×). Quase não há cortes secos — tudo é *morph* ou *pan*.
- Animações de entrada ~0,3–0,6 s; desenho de curvas ~1–1,5 s.

## 3. Estrutura narrativa (roteiro reconstruído pelos frames)

| Tempo aprox. | Bloco | Texto na tela | Visual |
|---|---|---|---|
| 0–6 s | **Gancho (pergunta)** | E SE VOCÊ MELHORASSE / SÓ 1% POR DIA? / PARECE NADA | Boneco sozinho, "1%" surge e encolhe |
| 6–14 s | Exemplos concretos | NINGUÉM NOTA / LER 10 PÁGINAS / GUARDAR UMA MOEDA / UMA FLEXÃO A MAIS | Outros bonecos com balões; ícones deslizando |
| 14–24 s | **Virada (a matemática)** | MAS FAZ A CONTA / 1,01 × ELE MESMO / 365 VEZES / VOCÊ NÃO ESTÁ 365% MELHOR / VOCÊ ESTÁ QUASE 38 VEZES MELHOR | Números, gráfico linear tracejado com ⊗ vs. curva exponencial "≈ 38×" |
| 24–36 s | **Lado sombrio (contraste)** | PIORA SÓ 1% POR DIA / "AMANHÃ EU COMEÇO" / UM DIA A MAIS NO SOFÁ / NO FIM DO ANO SOBRA MENOS DE 3% DE QUEM VOCÊ ERA | Boneco no sofá, balões, curva decrescente "< 3%" |
| 36–48 s | **Por que as pessoas desistem** | E O MAIS CRUEL / NA PRIMEIRA SEMANA OS DOIS CAMINHOS PARECEM IGUAIS / POR ISSO A MAIORIA DESISTE / OLHA PRO SÉTIMO DIA (1,07 vs 0,93) / E CONCLUI QUE NÃO FUNCIONA | Gráfico em "<" (bifurcação), zoom na 1ª semana, bandeira, "NÃO FUNCIONA ⊗" |
| 48–60 s | **Metáfora** | 1% NÃO APARECE NO COMEÇO / ELE APARECE DE REPENTE DEPOIS DE MUITO TEMPO INVISÍVEL / QUEM VÊ DE FORA CHAMA DE SORTE / QUEM VIVEU SABE QUE FOI UM DIA DE CADA VEZ | Raízes crescendo sob o chão (Dia 5 → Dia 27), planta brota, bonecos dizendo "QUE SORTE!", tracinhos contando dias |
| 60–70 s | **Lição** | VOCÊ NÃO PRECISA MUDAR TUDO / SÓ PRECISA SER 1% MELHOR DO QUE ONTEM | Triângulo "MUDAR TUDO" com ⊗; boneco ONTEM (cinza) vs HOJE (+1%) |
| 70–76 s | **Ponte para CTA** | E SE O SEU 1% DE HOJE FOR APRENDER ALGO NOVO? | Lâmpada acende, balão "+1%" |
| 76–83 s | **CTA** | EU FIZ UM TUTORIAL MOSTRANDO COMO GERAR VÍDEOS ASSIM / ESTÁ NO MEU VÍDEO FIXADO | Chip "IA" → celular com o boneco → grade do perfil com vídeo fixado |
| 83–85 s | Outro | — | Card padrão do TikTok |

### Por que viraliza (fórmula)
1. **Gancho em forma de pergunta** nos 2 primeiros segundos, com conceito simples (1%).
2. **Número surpreendente** (38×) que contradiz a intuição (365%) → gera "uau" e compartilhamento.
3. **Contraste** (o caminho bom vs. o ruim) → tensão emocional.
4. **Explica a dor** do público ("na primeira semana parece que não funciona").
5. **Metáfora visual memorável** (raízes invisíveis → planta).
6. **Lição curta e repetível** + **CTA** que aproveita o interesse (o tutorial).
7. Visual limpo e "hipnótico", legenda embutida (funciona sem som), loop fácil.

## 4. Receita técnica para reproduzirmos

**Formato:** 1080×1920 (9:16, ideal para Reels/TikTok) ou 1080×1080 como o original · 30 fps · 60–90 s.

**Pipeline sugerido:**
1. **Roteiro** — 25–35 frases curtas, uma ideia por frase, seguindo a estrutura da seção 3.
2. **Narração** — voz masculina/feminina calma e grave, ritmo pausado (podemos gerar com ElevenLabs, que já está conectado aqui).
3. **Marcação de tempo** — transcrever a narração com timestamps por palavra (para sincronizar o typewriter e as entradas).
4. **Animação** — duas opções:
   - **Código (recomendado aqui):** cenas em HTML/SVG/Canvas (ou Remotion), com glow via filtro de blur, renderizadas frame a frame e montadas em MP4 com ffmpeg. 100% reprodutível e fácil de gerar vários vídeos por série.
   - **Ferramenta visual:** After Effects (Trim Paths + Glow), Jitter, Rive ou CapCut com ícones em SVG.
5. **Trilha** — música ambiente/piano baixinho por baixo da voz (-20 dB).
6. **Exportar** — H.264, legenda já está embutida no topo.

**Parâmetros de estilo (para nosso "kit"):**
- Fundo `#000`, vinheta radial `#1a1a1a → #000` no centro.
- Traço `#FFFFFF`, 4–6 px, `stroke-linecap: round`.
- Glow: duplicar elemento, `blur(12px)`, opacidade 0,7 (+ uma segunda camada `blur(30px)` 0,3 para objetos principais).
- Secundário: `#8a8a8a` + `blur(1–2px)`.
- Título: Montserrat/Inter Black, caixa-alta, ~34 px em 1080 de largura, letter-spacing 0,12 em.
- Easing: `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out forte) para entradas; 0,4 s padrão.

## 5. Próximo passo

Para criarmos o **nosso** vídeo nessa mesma pegada (sem copiar o roteiro dele), precisamos definir:
- **Tema** (ex.: hábitos, dinheiro, produtividade, relacionamentos, curiosidades, seu nicho de negócio);
- **Formato** (9:16 vertical ou quadrado);
- **Voz** (gerada por IA ou gravada por você);
- **CTA final** (seguir, link, produto…).

Com isso, escrevo o roteiro cena a cena e monto um gerador de animações em código neste repositório que renderiza o MP4 final.
