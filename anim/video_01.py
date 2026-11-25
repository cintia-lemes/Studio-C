"""
Vídeo 01 — "1% por dia"  (≈35 s, 16:9)

Roteiro de narração (grave por cima, os tempos batem com a animação):

 0.0  "Se você melhorar só um por cento por dia..."
 1.6  "...em um ano você fica trinta e sete vezes melhor."
 3.0  "Se piorar um por cento... sobra quase nada."
 5.2  "Isso é juros compostos."
 7.0  "Só que aplicado em você."
10.1  "Ler dez páginas. Treinar vinte minutos. Dormir cedo."
13.3  "Todo dia."
15.6  "Mas a maioria desiste no dia três..."
18.4  "...e acha que é falta de talento."
21.0  "Não é motivação."
23.0  "É repetir. Trezentas e sessenta e cinco vezes."
26.0  "Você não precisa de força de vontade. Precisa de um sistema."
28.4  "Aí fica cada vez mais fácil."
31.2  "Segue o Studio C."

Rodar:  python3 anim/video_01.py            -> out/video_01.mp4
        python3 anim/video_01.py --stills   -> out/stills/*.png (prévia rápida)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from engine import *  # noqa

S = Scene(W=1280, H=720, fps=30, duration=35)


def cam_keys():
    # (tempo, x, easing) — saltos de 1 ms são cortes secos; 0,4 s com in_out = whip pan
    return Track(0,
                 (2.6, 0, lin), (3.2, 190, in_out_cubic),          # revela a 2ª coluna
                 (5.0, 190, lin), (5.001, 1400, lin),              # corte
                 (9.6, 1400, lin), (10.0, 3000, in_out_cubic),     # WHIP
                 (14.8, 3000, lin), (15.6, 3330, in_out_cubic),    # desliza p/ calendário
                 (20.9, 3330, lin), (20.901, 4900, lin),           # corte
                 (22.6, 4900, lin), (23.2, 5150, in_out_cubic),    # revela x365
                 (25.6, 5150, lin), (26.0, 7000, in_out_cubic),    # WHIP
                 (30.9, 7000, lin), (30.901, 9000, lin))           # corte p/ final


S.cam_x = cam_keys()
S.cam_y = const(-10)
S.zoom = Track(1, (5.0, 1, lin), (5.001, 1, lin), (9.6, 1.12, lin),   # push-in lento
               (9.8, 1, out_cubic), (26.0, 1, lin), (30.9, 1.08, lin), (30.901, 1, lin))
S.ground_a = Track(1, (30.9, 1, lin), (30.901, 0, lin))
S.sfx += [(9.55, "whoosh"), (25.55, "whoosh"), (5.0, "thud"), (20.9, "thud")]


def br(v):  # número no formato brasileiro
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------- S1: 1,01^365 vs 0,99^365 ----------------
T1_OUT = 4.7
S.add(CheckIcon(x=const(0), y=const(-110), r=24, s=appear(.5), a=life(.5, T1_OUT)), .5)
S.add(Text(x=const(0), y=const(-20), size=58,
           text=lambda t: br(1.01 ** (365 * out_cubic(min(1, max(0, (t - .8) / 1.8))))),
           s=appear(.2), a=life(.2, T1_OUT)), .2)
S.add(Pill(x=const(0), y=const(45), text="1% MELHOR POR DIA", s=appear(1.0), a=life(1.0, T1_OUT)), 1.0)
S.sfx += [(.8 + i * .12, "tick") for i in range(15)]

S.add(WarnIcon(x=const(380), y=const(-110), r=26, s=appear(3.1), a=life(3.1, T1_OUT)), 3.1)
S.add(Text(x=const(380), y=const(-20), size=58,
           text=lambda t: br(.99 ** (365 * out_cubic(min(1, max(0, (t - 3.3) / 1.0))))),
           s=appear(2.95), a=life(2.95, T1_OUT)), 2.95)
S.add(Pill(x=const(380), y=const(45), text="1% PIOR POR DIA", s=appear(3.5), a=life(3.5, T1_OUT)), 3.5)
S.sfx += [(3.3 + i * .1, "tick") for i in range(9)]

# ---------------- S2: juros compostos ----------------
X2 = 1400
S.add(Person(x=const(X2 - 260), y=const(120), s=appear(5.25), a=life(5.25, 9.55)), 5.25)
curve = [(i * 26, -(1.018 ** (i * 9) - 1) * 6) for i in range(22)]  # exponencial
S.add(Path(x=const(X2 - 200), y=const(110), pts=curve,
           prog=Track(0, (6.0, 0, lin), (8.2, 1, in_out_cubic)),
           tip=CoinIcon(r=18, s=appear(6.0)), a=life(6.0, 9.55)), 6.0)
S.add(Pill(x=const(X2 + 20), y=const(-150), text="JUROS COMPOSTOS", s=appear(7.0), a=life(7.0, 9.55)), 7.0)

# ---------------- S3: a rotina ----------------
X3 = 3000
P3 = S.add(Person(x=const(X3 - 170), y=const(120), h=130,
                  s=Track(0, (10.05, 0, lin), (10.4, 1, out_back)),
                  # depois "desiste": fica cinza e some
                  a=Track(0, (10.05, 0, lin), (10.3, 1, out_cubic), (16.9, 1, lin), (17.5, .22, out_cubic),
                          (18.0, .22, lin), (18.6, 0, in_cubic)),
                  phase=1), 10.05)
S.add(ListBox(x=const(X3 + 150), y=const(-5), w=300, title="O QUE ELE FAZ",
              items=[("LER 10 PÁGINAS", 10.9, True), ("TREINAR 20 MIN", 11.7, True), ("DORMIR CEDO", 12.5, True)],
              s=appear(10.6, e=out_cubic, s0=.85), a=life(10.6, 14.7)), 10.6)
S.sfx += [(10.9, "pop"), (11.7, "pop"), (12.5, "pop")]
S.add(Pill(x=const(X3 - 170), y=const(-60), text="TODO DIA", s=appear(13.3), a=life(13.3, 14.7)), 13.3)

# ---------------- S4: desiste no dia 3 ----------------
S.add(CalendarIcon(x=const(3600), y=const(10), w=110, label="DIA 3", s=appear(15.8), a=life(15.8, 20.6)), 15.8)
S.add(Pill(x=const(X3 - 170), y=const(-60), text="DESISTE", s=appear(16.6), a=life(16.6, 18.6, dim_at=17.0)), 16.6)
S.add(XIcon(x=const(3600), y=const(10), r=36, s=appear(18.3, .3), a=life(18.3, 20.6)), 18.3, "thud")
S.add(Pill(x=const(3600), y=const(-105), text="NÃO É FALTA DE TALENTO", s=appear(19.0), a=life(19.0, 20.6)), 19.0)

# ---------------- S5: x365 ----------------
X5 = 4900
S.add(Person(x=const(X5 - 30), y=const(120), s=appear(21.0), a=life(21.0, 25.55, dim_at=23.2, dim_to=.35),
             phase=2), 21.0)
S.add(Pill(x=const(X5 - 30), y=const(-60), text="NÃO É MOTIVAÇÃO", s=appear(21.4),
           a=life(21.4, 25.55, dim_at=23.2, dim_to=.35)), 21.4)
S.add(Text(x=const(5400), y=const(0), size=96, weight="Black",
           text=lambda t: f"x{int(round(1 + 364 * out_expo(min(1, max(0, (t - 23.3) / 1.4)))))}",
           s=appear(23.2, .4), a=life(23.2, 25.55)), 23.2)
S.add(Pill(x=const(5400), y=const(-85), text="REPETIR", s=appear(23.6), a=life(23.6, 25.55)), 23.6)
S.sfx += [(23.3 + i * .08, "tick") for i in range(14)]

# ---------------- S6: sistema ----------------
X6 = 7000
S.add(Box(x=const(X6 - 170), y=const(20), w=180, h=180, label="SISTEMA", s=appear(26.1), a=life(26.1, 30.7)),
      26.1, "thud")
COIN_END = [(40, -10), (150, -90), (95, 60), (240, -20), (300, -130)]
for i, t0 in enumerate([27.0, 27.4, 27.8, 28.2, 28.6]):
    ex, ey = COIN_END[i]
    S.add(CoinIcon(x=Track(X6 - 80, (t0, X6 - 80, lin), (t0 + 1.6, X6 + ex, out_cubic)),
                   y=Track(20, (t0, 20, lin), (t0 + 1.6, ey, out_cubic)),
                   r=19, s=appear(t0), a=life(t0, 30.7), phase=i), t0)
S.add(Pill(x=const(X6 + 230), y=const(-160), text="CADA VEZ MAIS FÁCIL", s=appear(28.4), a=life(28.4, 30.7)), 28.4)

# ---------------- S7: final ----------------
X7 = 9000
S.add(Text(x=const(X7), y=const(-25), text="STUDIO C", size=84, weight="Black", s=appear(31.2, .45),
           a=life(31.2, 34.2, dur=.5)), 31.2, "thud")
S.add(Pill(x=const(X7), y=const(55), text="SIGA PARA MAIS", s=appear(31.9), a=life(31.9, 34.2, dur=.5)), 31.9)


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills", exist_ok=True)
        for t in [1.5, 4.2, 7.5, 9.8, 13.6, 18.8, 22.0, 24.8, 29.5, 32.5]:
            S.still(t, f"{root}/stills/t{t:05.1f}.png")
        print("stills ok")
    else:
        S.render(f"{root}/video_01.mp4")
