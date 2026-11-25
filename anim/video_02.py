"""
Vídeo 02 — "Pare de correr atrás do dinheiro"  (≈61 s, 16:9, 1920×1080)
Página: Guidelight

Roteiro de narração (os tempos batem com a animação):

 0.3  "Você passa anos correndo atrás do dinheiro..."
 3.6  "...e ele sempre fica um passo à frente."
 7.0  "Porque você troca horas por dinheiro."
10.6  "Parou de trabalhar..."
12.0  "...parou de ganhar."
14.3  "Salário? Tem."
16.3  "Tempo livre? Não."
17.4  "Renda que não depende dele? Nenhuma."
20.6  "Os ricos fazem exatamente o contrário."
24.7  "Eles constroem ativos. Coisas que trabalham por eles."
28.0  "E o dinheiro passa a ir atrás deles."
33.2  "Conhecimento que vira produto."
34.8  "Audiência que vira cliente."
36.3  "Investimento que vira renda."
41.5  "No começo é lento..."
44.0  "...depois fica cada vez mais rápido."
48.2  "Pare de correr atrás do dinheiro."
51.0  "Construa algo que corra atrás de você."
55.2  "Segue a Guidelight pra mais conteúdo assim."

Rodar:  python3 anim/video_02.py --stills   (prévia)
        python3 anim/video_02.py            -> out/video_02.mp4
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from engine import *  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = (255, 196, 56)
RED = (255, 82, 82)
GREEN = (64, 222, 140)

S = Scene(W=1920, H=1080, fps=30, duration=61)
S.cam_y = const(-10)


def br_int(v):
    return f"{int(v):,}".replace(",", ".")


def clamp01(x):
    return max(0.0, min(1.0, x))


@dataclass
class Clock(El):
    r: float = 34
    speed: float = 6.0

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        col = self.c(a)
        c.d.ellipse([X - r, Y - r, X + r, Y + r], outline=col, width=max(1, int(3.2 * k)), fill=(0, 0, 0))
        for ang, L in ((c.t * self.speed, .72), (c.t * self.speed / 12, .45)):
            c.d.line([(X, Y), (X + math.sin(ang) * r * L, Y - math.cos(ang) * r * L)], fill=col,
                     width=max(1, int(3.2 * k)))


def coin_stream(x0, y0, x1, y1, starts, t_end, color=GOLD, fly=1.1):
    """Moedas que voam de (x0,y0) até (x1,y1) em arco — 'o dinheiro vem até você'."""
    for i, t0 in enumerate(starts):
        top = min(y0, y1) - 70 - (i % 3) * 18
        S.add(CoinIcon(x=Track(x0, (t0, x0, lin), (t0 + fly, x1, in_out_cubic)),
                       y=Track(y0, (t0, y0, lin), (t0 + fly * .5, top, out_cubic), (t0 + fly, y1, in_cubic)),
                       r=19, color=color, s=appear(t0, .25),
                       a=Track(0, (t0, 0, lin), (t0 + .15, 1, lin), (t0 + fly - .12, 1, lin),
                               (t0 + fly, 0, lin)) if t0 + fly < t_end else life(t0, t_end),
                       phase=i), t0)
        S.sfx.append((t0 + fly, "tick"))


# ======================================================================
# CÂMERA
# ======================================================================
RUN_V = 260  # px/s do corredor na cena 1


def runner_x(t):
    return RUN_V * min(t, 6.4)


cam_rest = Track(RUN_V * 6.4 + 80,
                 (6.4, RUN_V * 6.4 + 80, lin), (6.8, 3000, in_out_cubic),      # WHIP
                 (10.0, 3000, lin), (10.6, 3420, in_out_cubic),                 # revela lado direito
                 (14.0, 3420, lin), (14.001, 5000, lin),                        # corte
                 (20.4, 5000, lin), (20.401, 7000, lin),                        # corte (inversão)
                 (24.4, 7000, lin), (24.401, 9000, lin),                        # corte
                 (32.9, 9000, lin), (32.901, 11000, lin),                       # corte
                 (40.9, 11000, lin), (40.901, 13000, lin),                      # corte
                 (47.9, 13000, lin), (47.901, 15000, lin),                      # corte
                 (54.4, 15000, lin), (54.85, 17000, in_out_cubic))              # WHIP p/ final


def cam_x(t):
    return runner_x(t) + 80 if t < 6.4 else cam_rest(t)


S.cam_x = cam_x
S.zoom = Track(1, (40.9, 1, lin), (40.901, 1, lin), (47.9, 1.1, lin), (47.901, 1, lin))
S.ground_a = Track(1, (54.4, 1, lin), (54.8, 0, in_cubic))
S.invert = Track(0, (20.4, 0, lin), (20.55, 1, out_cubic), (24.3, 1, lin), (24.45, 0, in_cubic))
S.sfx += [(6.35, "whoosh"), (54.35, "whoosh"), (14.0, "thud"), (20.4, "thud"), (24.4, "thud"),
          (32.9, "thud"), (40.9, "thud"), (47.9, "thud")]

# ======================================================================
# S1 — correndo atrás do dinheiro (0–6.4)
# ======================================================================
S.add(Person(x=runner_x, y=const(120), h=130, legs=True, run=const(1), gait=13,
             s=appear(.1), a=life(.1, 6.4), float_amp=0), .1)
S.add(CoinIcon(x=lambda t: runner_x(t) + 340, y=lambda t: 98 - abs(math.sin(t * 5.5)) * 55,
               r=22, color=GOLD, s=appear(.4), a=life(.4, 6.4), float_amp=0), .4)
S.add(Pill(x=runner_x, y=const(-60), text="CORRENDO ATRÁS", s=appear(1.0), a=life(1.0, 3.4)), 1.0)
S.add(Pill(x=runner_x, y=const(-60), text="ANOS E ANOS", s=appear(3.6), a=life(3.6, 6.4)), 3.6)
S.add(Pill(x=lambda t: runner_x(t) + 340, y=const(-40), text="SEMPRE À FRENTE", color=GOLD,
           s=appear(4.3), a=life(4.3, 6.4)), 4.3)
S.sfx += [(i * .23 + .1, "tick") for i in range(27)]  # passos

# ======================================================================
# S2 — troca tempo por dinheiro (6.8–14)
# ======================================================================
S.add(Clock(x=const(2770), y=const(0), r=40, speed=8, s=appear(7.0), a=life(7.0, 13.8, dim_at=10.6)), 7.0)
S.add(Path(x=const(2830), y=const(0), pts=[(0, 0), (130, 0)], arrow=True,
           prog=Track(0, (7.5, 0, lin), (8.0, 1, out_cubic)), a=life(7.5, 13.8, dim_at=10.6)), 7.5)
S.add(CoinIcon(x=const(3020), y=const(0), r=30, color=GOLD, s=appear(8.0), a=life(8.0, 13.8, dim_at=10.6)), 8.0)
S.add(Pill(x=const(2895), y=const(-95), text="TROCA HORAS POR DINHEIRO", s=appear(8.5),
           a=life(8.5, 13.8, dim_at=10.6)), 8.5)

S.add(Person(x=const(3480), y=const(120), h=130, s=appear(10.6), a=life(10.6, 13.8)), 10.6)
S.add(Pill(x=const(3480), y=const(-55), text="PAROU DE TRABALHAR", s=appear(11.1), a=life(11.1, 13.8)), 11.1)
S.add(Text(x=const(3730), y=const(10), text="R$ 0", size=78, weight="Black", color=RED,
           s=appear(12.0, .35), a=life(12.0, 13.8)), 12.0, "thud")
S.add(WarnIcon(x=const(3730), y=const(-90), r=26, color=RED, s=appear(12.3), a=life(12.3, 13.8)), 12.3)

# ======================================================================
# S3 — o que ele tem (14–20.4)
# ======================================================================
S.add(Person(x=const(4800), y=const(120), h=135, s=appear(14.2),
             a=Track(0, (14.2, 0, lin), (14.45, 1, out_cubic), (18.4, 1, lin), (18.9, .3, out_cubic),
                     (20.1, .3, lin), (20.35, 0, in_cubic))), 14.2)
S.add(ListBox(x=const(5130), y=const(-5), w=320, title="O QUE ELE TEM",
              items=[("SALÁRIO", 15.0, True), ("TEMPO LIVRE", 16.3, False), ("RENDA PASSIVA", 17.4, False)],
              ok_color=GREEN, bad_color=RED, s=appear(14.6, e=out_cubic, s0=.85), a=life(14.6, 20.1)), 14.6)
S.sfx += [(15.0, "pop"), (16.3, "pop"), (17.4, "pop")]
S.add(Pill(x=const(4800), y=const(-55), text="CANSADO", color=RED, s=appear(18.4), a=life(18.4, 20.1)), 18.4)

# ======================================================================
# S4 — INVERSÃO (fundo branco) (20.4–24.4)
# ======================================================================
S.add(Text(x=const(7000), y=const(-30), text="INVERTA O JOGO", size=96, weight="Black",
           s=appear(20.6, .4), a=life(20.6, 24.2, dur=.15)), 20.6)
S.add(Pill(x=const(7000), y=const(60), text="OS RICOS FAZEM O CONTRÁRIO", size=17,
           s=appear(21.6), a=life(21.6, 24.2, dur=.15)), 21.6)
S.add(Person(x=const(6440), y=const(120), h=110, legs=True, run=const(.45), gait=6,
             s=appear(22.4), a=life(22.4, 24.2, dur=.15), float_amp=0), 22.4)
S.add(Person(x=const(7560), y=const(120), h=110, legs=True, run=const(.45), gait=6, phase=1,
             s=appear(22.7), a=life(22.7, 24.2, dur=.15), float_amp=0), 22.7)

# ======================================================================
# S5 — o dinheiro vem até você (24.4–32.9)
# ======================================================================
S.add(Person(x=const(8780), y=const(120), h=135, s=appear(24.6), a=life(24.6, 32.7)), 24.6)
S.add(Box(x=const(9260), y=const(40), w=170, h=150, label="ATIVOS", size=24, color=GOLD,
          s=appear(25.5), a=life(25.5, 32.7)), 25.5, "thud")
coin_stream(9200, 10, 8800, -20, [26.4 + i * .55 for i in range(10)], 32.7)
S.add(Text(x=const(8780), y=const(-150), size=40, weight="Black", color=GREEN,
           text=lambda t: f"R$ {br_int(12400 * out_cubic(clamp01((t - 26.5) / 5.2)))}",
           s=appear(26.4), a=life(26.4, 32.7)), 26.4)
S.add(Pill(x=const(9180), y=const(-175), text="O DINHEIRO VEM ATÉ VOCÊ", color=GOLD,
           s=appear(28.0), a=life(28.0, 32.7)), 28.0)

# ======================================================================
# S6 — três ativos (32.9–40.9)
# ======================================================================
S.add(Pill(x=const(11000), y=const(-190), text="3 ATIVOS", size=17, s=appear(33.0), a=life(33.0, 40.7)), 33.0)
for i, (name, res, t0) in enumerate([("CONHECIMENTO", "VIRA PRODUTO", 33.3),
                                      ("AUDIÊNCIA", "VIRA CLIENTE", 35.5),
                                      ("INVESTIMENTO", "VIRA RENDA", 37.75)]):
    x = 10640 + i * 360
    S.add(Box(x=const(x), y=const(-70), w=230, h=110, label=name, size=21, s=appear(t0),
              a=life(t0, 40.7)), t0, "thud")
    S.add(Path(x=const(x), y=const(-5), pts=[(0, 0), (0, 45)], arrow=True,
               prog=Track(0, (t0 + .4, 0, lin), (t0 + .7, 1, out_cubic)), a=life(t0 + .4, 40.7)), t0 + .4)
    S.add(Pill(x=const(x - 25), y=const(72), text=res, color=GOLD, s=appear(t0 + .7), a=life(t0 + .7, 40.7)), t0 + .7)
    S.add(CoinIcon(x=const(x + 95), y=const(72), r=15, color=GOLD, s=appear(t0 + .9), a=life(t0 + .9, 40.7)), t0 + .9)

# ======================================================================
# S7 — gráfico salário × ativos (40.9–47.9)
# ======================================================================
GX, GY = 12640, 110
S.add(Path(x=const(GX), y=const(GY), pts=[(0, -280), (0, 0), (760, 0)], width=2.4, color=(150, 150, 150),
           prog=Track(0, (41.0, 0, lin), (41.5, 1, out_cubic)), a=life(41.0, 47.7)), 41.0)
S.add(Pill(x=const(GX + 700), y=const(GY + 30), text="TEMPO", size=13, s=appear(41.3), a=life(41.3, 47.7)), 41.3)
sal = [(i * 35, -i * 4.2) for i in range(21)]
S.add(Path(x=const(GX), y=const(GY), pts=sal, color=(170, 170, 170),
           prog=Track(0, (41.6, 0, lin), (44.0, 1, lin)), a=life(41.6, 47.7)), 41.6)
S.add(Pill(x=const(GX + 790), y=const(GY - 90), text="SALÁRIO", size=13, color=(170, 170, 170),
           s=appear(44.0), a=life(44.0, 47.7)), 44.0)
ativ = [(i * 35, -(1.021 ** (i * 9) - 1) * 6.0) for i in range(21)]
S.add(Path(x=const(GX), y=const(GY), pts=ativ, color=GREEN, width=4.2,
           prog=Track(0, (42.4, 0, lin), (46.0, 1, in_cubic)),
           tip=CoinIcon(r=17, color=GOLD, s=appear(42.4)), a=life(42.4, 47.7)), 42.4)
S.add(Pill(x=const(GX + 560), y=const(GY - 330), text="ATIVOS", color=GREEN, s=appear(46.0), a=life(46.0, 47.7)), 46.0)
S.add(Pill(x=const(GX + 200), y=const(GY - 200), text="LENTO NO COMEÇO", size=13, s=appear(41.8),
           a=life(41.8, 47.7, dim_at=44.0)), 41.8)

# ======================================================================
# S8 — pare de correr / construa (47.9–54.4)
# ======================================================================
S.add(Person(x=Track(14560, (48.0, 14560, lin), (49.3, 14820, out_cubic)), y=const(120), h=135, legs=True,
             run=Track(1, (48.6, 1, lin), (49.3, 0, out_cubic)), gait=13, float_amp=0,
             s=appear(47.95, .2), a=life(47.95, 54.3)), 48.0)
S.add(Pill(x=const(14820), y=const(-55), text="PARE DE CORRER", color=RED, s=appear(49.3),
           a=life(49.3, 54.3, dim_at=50.9, dim_to=.35)), 49.3)
S.add(Box(x=const(15280), y=const(40), w=180, h=150, label="CONSTRUA", size=24, color=GOLD,
          s=appear(51.0), a=life(51.0, 54.3)), 51.0, "thud")
coin_stream(15220, 10, 14840, -20, [51.8 + i * .5 for i in range(5)], 54.3)
S.add(Pill(x=const(15050), y=const(-175), text="ELE VAI ATRÁS DE VOCÊ", color=GOLD, s=appear(52.3),
           a=life(52.3, 54.3)), 52.3)

# ======================================================================
# S9 — final: Guidelight (54.8–61)
# ======================================================================
X9 = 17000
S.add(Pill(x=const(X9), y=const(-225), text="SIGA A PÁGINA", size=17, s=appear(56.0), a=life(56.0, 60.4)), 56.0)
S.add(Avatar(x=const(X9), y=const(-90), r=95, path=os.path.join(HERE, "assets", "guidelight.jpg"), ring=GOLD,
             s=appear(55.0, .45), a=life(55.0, 60.4)), 55.0, "thud")
S.add(Text(x=const(X9), y=const(60), text="GUIDELIGHT", size=62, weight="Black",
           s=appear(55.5, .4), a=life(55.5, 60.4)), 55.5)
CLICK = 58.2
S.add(Button(x=const(X9), y=const(150), w=230, h=58,
             text=lambda t: "SEGUINDO" if t >= CLICK else "SEGUIR",
             fill=lerp_color((255, 255, 255), GOLD, CLICK, CLICK + .15),
             s=Track(0, (56.6, 0, lin), (56.95, 1, out_back), (CLICK - .05, 1, lin), (CLICK + .05, .9, lin),
                     (CLICK + .35, 1, out_back)),
             a=life(56.6, 60.4)), 56.6)
S.add(Cursor(x=Track(X9 + 330, (57.2, X9 + 330, lin), (58.0, X9 + 20, in_out_cubic)),
             y=Track(320, (57.2, 320, lin), (58.0, 150, in_out_cubic)),
             s=Track(1, (CLICK - .05, 1, lin), (CLICK + .05, .85, lin), (CLICK + .25, 1, out_cubic)),
             a=life(57.2, 59.6)), CLICK)
S.sfx.append((CLICK + .02, "tick"))
S.add(Rays(x=const(X9), y=const(-90), r=122, n=5, prog=Track(0, (CLICK, 0, lin), (CLICK + .3, 1, out_back)),
           color=GOLD, a=life(CLICK, 60.4), float_amp=0))


# Narração (ElevenLabs, voz "Jarnathan", id c6SfcYrb2t09NHXiT80T, modelo eleven_v4):
# (arquivo, segundo em que começa no vídeo)
VOZ = [("s1.mp3", 0.3), ("s2.mp3", 8.0), ("s3.mp3", 13.95), ("s4.mp3", 20.75), ("s5.mp3", 24.6),
       ("s6.mp3", 33.2), ("s7.mp3", 41.4), ("s8.mp3", 48.3), ("s9.mp3", 55.5)]


if __name__ == "__main__":
    root = os.path.join(HERE, "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills02", exist_ok=True)
        for t in [2.0, 5.5, 9.5, 13.0, 18.9, 22.9, 30.0, 38.5, 46.8, 53.5, 58.9]:
            S.still(t, f"{root}/stills02/t{t:05.1f}.png")
        print("stills ok")
    else:
        S.render(f"{root}/video_02.mp4")
        mix_voice(f"{root}/video_02.mp4", [(os.path.join(HERE, "assets", "voz02", f), t) for f, t in VOZ],
                  f"{root}/guidelight_pare_de_correr_16x9.mp4")
