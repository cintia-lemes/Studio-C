# Análise do vídeo de referência — animação 2D minimalista

Vídeo de 69 s, 16:9 (1024×576), 30 fps, analisado em folhas de quadros a 1 fps e trechos a 5 fps.

## 1. Linguagem visual

| Elemento | Como é feito |
|---|---|
| Fundo | Preto quase puro com **vinheta radial**: o centro é um pouco mais claro (~#1e1e1e) e as bordas mais escuras (~#080808). Há um leve grão. |
| Chão | **Linha tracejada cinza** horizontal que atravessa a tela. É o que "ancora" o pictograma e dá a sensação de câmera andando de lado. |
| Personagem | **Pictograma branco sólido**: cabeça redonda e corpo de cantos arredondados. Sem rosto, sem braços. Qualquer pessoa se vê nele. |
| Ícones | **Só contorno branco** (~3 px): documento, celular, relógio, moeda $, alvo, check ✓, X, aviso ⚠, caixa. Por dentro são pretos, então tampam o que está atrás. |
| Texto principal | Caixa alta, sans-serif **extra bold** (no estilo Inter/Montserrat), branco, grande. Ex.: `R$ 10.000`, `x10`. |
| Pílulas | Rótulos **pequenos em caixa alta**, com letras espaçadas e borda arredondada: `MAIS DIFÍCIL`, `DESISTE`, `NÃO É BRIGA NOVA`. É o "legendão" do conceito, não a fala inteira. |
| Glow | Tudo tem um **brilho suave** (bloom), o que dá o ar de neon apagado. |
| Paleta | Monocromática. A cor só aparece no cartão final. O cinza indica fracasso, passado ou algo secundário. |

## 2. Gramática de movimento (o que faz o vídeo "prender")

1. **Pop com overshoot**: os elementos nascem de escala 0 e passam um pouco de 100% antes de assentar (~0,3 s, easing *back*). Cada pop tem um som curto.
2. **Contador rolando**: números sobem ou descem rapidamente até o valor final (`R$ 8.770 → 10.000`, `R$ 64.126 → 98.302 → 100.000`), sempre com "ticks" no áudio.
3. **Câmera lateral**: em vez de cortar, a câmera desliza para o lado e o próximo elemento entra pela direita. Dá para ver `R$ 7…` cortado na borda antes de ele aparecer inteiro.
4. **Comparação esquerda × direita**: duas colunas iguais com ícones opostos (⚠ × ✓, `MAIS DIFÍCIL` × `MAIS FÁCIL`, `1 ANO` × `10 ANOS?`, `IMPOSSÍVEL` × `PIADA`). É o recurso que mais se repete.
5. **Fracasso = cinza**: quando o personagem "desiste", ele fica cinza, afunda um pouco e some, enquanto a pílula continua lá. Depois um **X** carimba o objeto (`CONTA ⊗`).
6. **Lista que cresce**: o painel `O QUE ELE TEM` ganha um item por fala, com ✓ ou ✗ aparecendo com pop.
7. **Whip pan**: em mudanças de bloco (7 s, 39 s) a câmera dispara para o lado com **borrão horizontal e riscos de luz**, acompanhada de um *whoosh*.
8. **Escurecer o que já foi dito**: ao introduzir algo novo, o anterior cai para ~30% de brilho (34 s).
9. **Movimento ocioso**: nada fica 100% parado. Há uma leve flutuação e um *push-in* lento da câmera.
10. **Ritmo**: um beat visual novo a cada **1 a 1,5 s**, sincronizado com a narração. A tela fica vazia por ~0,3 s entre blocos para "respirar".

## 3. Estrutura narrativa (≈ 60 s + CTA)

1. **Gancho com número** (0–5 s): comparação chocante, mais difícil × mais fácil.
2. **Personagem e problema** (5–17 s): pessoa, linha reta (a expectativa) e a realidade, com `DESISTE`.
3. **Diagnóstico** (18–35 s): lista do que falta (✗ ✗ ✗) e por que "nada acontece".
4. **Virada** (36–48 s): outro personagem, `CHEGOU AOS 10 MIL`, `O QUE FUNCIONA`, lista com ✓ ✓ ✓.
5. **Princípio** (49–58 s): `NÃO É BRIGA NOVA`, `REPETIR x10`.
6. **Conclusão** (59–64 s): `MÁQUINA` gerando moedas, `CADA VEZ MAIS FÁCIL`.
7. **CTA** (65–69 s): cartão com o @ do perfil.

## 4. Fórmula para os nossos vídeos

- Uma ideia só, contada com **um personagem** e uma **comparação**.
- Narração em frases curtas. **Cada frase vira um ícone, um número ou uma pílula.**
- A pílula traz 2 a 4 palavras-chave, nunca a frase inteira.
- Vale abrir com um número que muda na tela.
- Feche com um "sistema/máquina" e um CTA.

O motor em `anim/engine.py` implementa tudo isso; `anim/video_01.py` é o primeiro vídeo ("1% por dia").
