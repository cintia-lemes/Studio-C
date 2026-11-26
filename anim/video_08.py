"""
Vídeo 08: "Parece loucura": identidade, merecimento e postura  (9:16, 1080×1920, ≈63 s)
Página: Guidelight. Roteiro e ganchos: docs/roteiros/video_08_parece_loucura.md
Narração: ElevenLabs, voz "Elvis – Social Media & Shorts" (zNEsdgTUa3ndwKry8Xcq), eleven_v4, em anim/assets/voz08/

Rodar:  python3 anim/video_08.py --stills | --mix | (sem nada: render + mix)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from engine import *  # noqa
import video_05 as v5  # PriceTag

PriceTag = v5.PriceTag
HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = (255, 196, 56)
RED = (255, 82, 82)
GREEN = (64, 222, 140)
GREY = (150, 150, 150)

S = Scene(W=1080, H=1920, fps=30, duration=63.0, base_w=720)
PILL = 19

VOZ = [("s01.mp3", 0.05), ("s02.mp3", 7.95), ("s03.mp3", 13.9), ("s04.mp3", 17.3), ("s05.mp3", 20.5),
       ("s06.mp3", 26.0), ("s07.mp3", 33.3), ("s08.mp3", 38.9), ("s09.mp3", 44.6), ("s10.mp3", 50.7),
       ("s11.mp3", 58.3)]


def cut(t):
    return t + 0.015


@dataclass
class Clock(El):
    r: float = 40
    speed: float = 8

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        col = self.c(a)
        c.d.ellipse([X - r, Y - r, X + r, Y + r], outline=col, width=max(1, int(3.4 * k)), fill=(0, 0, 0))
        for ang, L in ((c.t * self.speed, .72), (c.t * self.speed / 12, .45)):
            c.d.line([(X, Y), (X + math.sin(ang) * r * L, Y - math.cos(ang) * r * L)], fill=col,
                     width=max(1, int(3.4 * k)))


@dataclass
class Dashed(El):
    w: float = 640
    float_amp: float = 0

    def paint(self, c, X, Y, k, a):
        x = X - self.w * k / 2
        while x < X + self.w * k / 2:
            c.d.line([(x, Y), (x + 7 * k, Y)], fill=self.c(a * .35), width=max(1, int(2 * k)))
            x += 13 * k


@dataclass
class Wand(El):
    s_: float = 170

    def paint(self, c, X, Y, k, a):
        s = self.s_ * k
        col = self.c(a)
        sw = max(1, int(4 * k))
        c.d.line([(X - s * .45, Y + s * .45), (X + s * .15, Y - s * .15)], fill=col, width=sw)
        cx, cy, r = X + s * .25, Y - s * .25, s * .2
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5 + c.t * 1.5
            rr = r if i % 2 == 0 else r * .45
            pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
        c.d.polygon(pts, outline=col, width=sw)


def coin_stream(x0, y0, x1, y1, starts, t_end, fly=1.0):
    for i, t0 in enumerate(starts):
        top = min(y0, y1) - 80 - (i % 3) * 20
        S.add(CoinIcon(x=Track(x0, (t0, x0, lin), (t0 + fly, x1, in_out_cubic)),
                       y=Track(y0, (t0, y0, lin), (t0 + fly * .5, top, out_cubic), (t0 + fly, y1, in_cubic)),
                       r=20, color=GOLD, s=appear(t0, .25),
                       a=Track(0, (t0, 0, lin), (t0 + .12, 1, lin), (t0 + fly - .1, 1, lin), (t0 + fly, 0, lin))
                       if t0 + fly < t_end else life(t0, t_end), phase=i), t0)
        S.sfx.append((t0 + fly, "tick"))


def P(x, y, text, t, t_out=None, color=(255, 255, 255), size=PILL, dim_at=None, dim_to=.3):
    return S.add(Pill(x=const(x), y=const(y), text=text, size=size, color=color, s=appear(t),
                      a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


def T(x, y, text, t, t_out=None, size=60, color=(255, 255, 255), weight="Black", dim_at=None, dim_to=.3, dur=.35):
    return S.add(Text(x=const(x), y=const(y), text=text, size=size, weight=weight, color=color,
                      s=appear(t, dur), a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


# ---------------------------------------------------------------- câmera
XA, XB, XC, XD, XE, XF, XG, XH, XI, XJ, XK = [i * 1500 for i in range(11)]
S.cam_x = Track(XA, (cut(7.8), XA, lin), (cut(7.8) + .001, XB, lin),
                (cut(13.75), XB, lin), (cut(13.75) + .001, XC, lin),
                (17.0, XC, lin), (17.35, XD, in_out_cubic),
                (cut(20.35), XD, lin), (cut(20.35) + .001, XE, lin),
                (25.7, XE, lin), (26.05, XF, in_out_cubic),
                (cut(33.15), XF, lin), (cut(33.15) + .001, XG, lin),
                (cut(38.75), XG, lin), (cut(38.75) + .001, XH, lin),
                (44.3, XH, lin), (44.65, XI, in_out_cubic),
                (cut(50.55), XI, lin), (cut(50.55) + .001, XJ, lin),
                (58.0, XJ, lin), (58.35, XK, in_out_cubic))
S.cam_y = const(0)
S.ground_a = const(0)
S.invert = Track(0, (cut(33.15), 0, lin), (cut(33.15) + .1, 1, out_cubic), (38.65, 1, lin), (38.75, 0, in_cubic))
S.sfx += [(t, "whoosh") for t in (16.95, 25.65, 44.25, 57.95)] + \
         [(t, "thud") for t in (7.8, 13.75, 20.35, 33.15, 38.75, 50.55)]

# ---------------------------------------------------------------- A: gancho (0.05–7.65)
AO = 7.8
T(XA, -460, "PARECE LOUCURA.", .05, AO, size=64, dur=.25)
S.sfx.append((.05, "thud"))
S.add(Dashed(x=const(XA), y=const(330), a=life(1.5, AO)))
S.add(Person(x=const(XA), y=const(330), h=160, s=appear(1.6), a=life(1.6, AO)), 1.6)
P(XA, -330, "QUANDO VOCÊ ACREDITA", 1.7, AO, size=22)
T(XA, -230, "AS MELHORES COISAS", 3.4, AO, size=50, color=GOLD)
T(XA, -90, "ENCONTRAM CAMINHO", 5.7, AO, size=48)
coin_stream(XA + 330, 120, XA + 10, 200, [5.8, 6.15, 6.5, 6.85], AO, fly=.9)
coin_stream(XA - 330, 120, XA - 10, 200, [6.0, 6.35, 6.7], AO, fly=.9)

# ---------------------------------------------------------------- B: não é mágica (7.95–13.6)
BO = 13.75
T(XB, -460, "E NÃO,", 7.95, BO, size=60)
T(XB, -370, "NÃO É MÁGICA.", 8.7, BO, size=76)
S.add(Wand(x=const(XB), y=const(-160), s_=190, color=GOLD, s=appear(8.8, .35), a=life(8.8, BO, dim_at=9.9, dim_to=.35)), 8.8)
S.add(XIcon(x=const(XB + 90), y=const(-230), r=34, color=RED, s=appear(9.4), a=life(9.4, BO)), 9.4, "thud")
S.add(Person(x=const(XB - 120), y=const(330), h=150, s=appear(10.1), a=life(10.1, BO)), 10.1)
S.add(Clock(x=const(XB + 140), y=const(230), r=60, speed=12, s=appear(10.3), a=life(10.3, BO)), 10.3)
P(XB, 60, "ESPERAR O UNIVERSO DEPOSITAR", 10.2, BO, size=19, color=RED)

# ---------------------------------------------------------------- C: mais simples / desconfortável (13.9–17.0)
CO = 17.0
T(XC, -160, "É MAIS SIMPLES.", 13.9, CO, size=66)
S.add(Text(x=lambda t: XC + (math.sin(t * 45) * 4 if t > 15.3 else 0), y=const(-40), text="E MAIS DESCONFORTÁVEL.",
           size=46, weight="Black", color=RED, s=appear(15.3, .3), a=life(15.3, CO)), 15.3, "thud")

# ---------------------------------------------------------------- D: merece pouco / cobra pouco (17.3–20.2)
DO = 20.35
P(XD, -470, "AUTOSSABOTAGEM", 17.35, DO, size=21, color=RED)
T(XD, -360, "MERECE POUCO", 17.5, DO, size=70)
S.add(Dashed(x=const(XD), y=const(330), a=life(17.35, DO)))
S.add(Person(x=const(XD - 120), y=const(330), h=120, color=GREY, s=appear(17.5), a=life(17.5, DO)), 17.5)
S.add(PriceTag(x=const(XD + 130), y=const(200), w=200, h=86, text="R$ 50", color=GREY,
               s=appear(19.3, .3), a=life(19.3, DO)), 19.3, "pop")
T(XD, -240, "COBRA POUCO", 19.3, DO, size=56, color=RED)

# ---------------------------------------------------------------- E: aceita o mínimo (20.5–25.7)
EO = 25.7
S.add(Dashed(x=const(XE), y=const(360), a=life(20.4, EO)))
S.add(Person(x=const(XE), y=const(360), h=150, color=GREY,
             s=Track(1, (20.4, 1, lin), (25.5, .78, in_out_cubic)), a=life(20.4, EO)), 20.4)
for i, (lab, t0) in enumerate([("ACEITA O 1º NÃO", 20.5), ("EMPREGO QUE PAGA MAL", 22.15), ("\"PODIA SER PIOR\"", 24.65)]):
    P(XE, -380 + i * 110, lab, t0, EO, color=RED, size=25)

# ---------------------------------------------------------------- F: oportunidade / sabota (26.0–33.0)
FO = 33.15
S.add(Dashed(x=const(XF), y=const(330), a=life(26.0, FO)))
S.add(Box(x=const(XF + 160), y=const(220), w=230, h=200, label="OPORTUNIDADE", size=22, color=GOLD,
          s=appear(26.1, .4), a=life(26.1, FO, dim_at=28.7, dim_to=.3)), 26.1, "thud")
S.add(Rays(x=const(XF + 160), y=const(220), r=150, n=7, prog=Track(0, (26.3, 0, lin), (26.6, 1, out_back)), color=GOLD,
           a=life(26.3, FO, dim_at=28.7, dim_to=.2), float_amp=0))
S.add(Person(x=Track(XF - 90, (28.7, XF - 90, lin), (29.6, XF - 250, out_cubic)), y=const(330), h=150, legs=True,
             run=Track(0, (28.65, 0, lin), (28.75, .6, lin), (29.5, .6, lin), (29.65, 0, lin)), gait=10, float_amp=0,
             s=appear(26.0), a=life(26.0, FO)), 26.0)
T(XF, -380, "SABOTA.", 28.7, FO, size=110, color=RED, dur=.25)
S.sfx.append((28.7, "thud"))
P(XF - 160, 60, "NÃO É PRA MIM", 29.9, FO, size=22)

# ---------------------------------------------------------------- G: identidade → aceitação (33.3–38.6), inversão
GO = 38.65
T(XG, -440, "AGORA…", 33.35, GO, size=56)
T(XG, -250, "QUEM VOCÊ É", 34.1, GO, size=84)
S.add(Path(x=const(XG), y=const(-170), pts=[(0, 0), (0, 130)], arrow=True, width=4.5,
           prog=Track(0, (36.3, 0, lin), (36.8, 1, out_cubic)), a=life(36.3, GO)), 36.3)
T(XG, 50, "O QUE VOCÊ ACEITA", 36.9, GO, size=58)
S.sfx.append((36.9, "thud"))

# ---------------------------------------------------------------- H: postura nova (38.9–44.3)
HO = 44.3
S.add(Dashed(x=const(XH), y=const(380), a=life(38.85, HO)))
S.add(Person(x=const(XH), y=const(380), h=200, color=GOLD, s=appear(38.9, .4), a=life(38.9, HO)), 38.9)
for i, (lab, t0) in enumerate([("PEDE O AUMENTO", 39.2), ("COLOCA O PREÇO CERTO", 40.8), ("SAI DE ONDE TE DIMINUI", 42.7)]):
    y = -420 + i * 110
    S.add(Text(x=const(XH - 20), y=const(y), text=lab, size=36, weight="Black", s=appear(t0), a=life(t0, HO)), t0, "pop")
    S.add(CheckIcon(x=const(XH + 285), y=const(y), r=22, color=GREEN, s=appear(t0 + .25), a=life(t0 + .25, HO)))

# ---------------------------------------------------------------- I: não cai do céu (44.6–50.4)
IO = 50.55
T(XI, -450, "NÃO CAEM DO CÉU", 44.65, IO, size=60)
S.add(CoinIcon(x=const(XI), y=Track(-700, (44.8, -700, lin), (45.6, -250, in_cubic)), r=30, color=GOLD,
               a=life(44.8, 46.9), float_amp=0))
S.add(XIcon(x=const(XI + 40), y=const(-290), r=24, color=RED, s=appear(45.7), a=life(45.7, 46.9)), 45.7, "tick")
S.add(Dashed(x=const(XI), y=const(330), a=life(44.6, IO)))
S.add(Person(x=Track(XI - 250, (47.2, XI - 250, lin), (48.4, XI - 60, in_out_cubic)), y=const(330), h=160, color=GOLD,
             legs=True, run=Track(0, (47.1, 0, lin), (47.25, .6, lin), (48.25, .6, lin), (48.45, 0, lin)), gait=8,
             float_amp=0, s=appear(44.7), a=life(44.7, IO)), 44.7)
S.add(Box(x=const(XI + 170), y=const(230), w=200, h=170, label="MELHORES", size=24,
          color=GOLD, s=appear(47.25), a=life(47.25, IO)), 47.25)
P(XI, -100, "PARA DE FUGIR DELAS", 47.4, IO, color=GOLD, size=24)
coin_stream(XI + 170, 180, XI - 50, 200, [48.5, 48.85, 49.2, 49.55], IO, fly=.8)

# ---------------------------------------------------------------- J: reflexão (50.7–57.9)
JO = 58.0
T(XJ, -420, "VOCÊ MERECE?", 50.75, JO, size=76, dim_at=53.4, dim_to=.3)
S.add(Path(x=const(XJ - 250), y=const(-420), pts=[(0, 0), (500, 0)], width=6, color=RED,
           prog=Track(0, (52.4, 0, lin), (52.8, 1, out_cubic)), a=life(52.4, JO), float_amp=0))
P(XJ, -300, "A PERGUNTA É OUTRA", 53.5, JO, size=22, color=GOLD)
T(XJ, -150, "O QUE VOCÊ TÁ", 54.25, JO, size=58, color=GOLD)
T(XJ, -70, "ACEITANDO", 54.6, JO, size=76, color=GOLD)
T(XJ, 50, "QUE NÃO COMBINA", 55.8, JO, size=50)
T(XJ, 130, "COM QUEM VOCÊ", 56.4, JO, size=50)
T(XJ, 210, "QUER SER?", 56.9, JO, size=66)

# ---------------------------------------------------------------- K: final (58.1–63)
KO = 62.7
P(XK, -390, "SIGA A PÁGINA", 58.9, KO, size=22)
S.add(Avatar(x=const(XK), y=const(-150), r=150, path=os.path.join(HERE, "assets", "guidelight.jpg"), ring=GOLD,
             s=appear(58.2, .45), a=life(58.2, KO)), 58.2, "thud")
T(XK, 80, "GUIDELIGHT", 58.5, KO, size=78)
CLICK = 60.7
S.add(Button(x=const(XK), y=const(210), w=300, h=78, text=lambda t: "SEGUINDO" if t >= CLICK else "SEGUIR",
             fill=lerp_color((255, 255, 255), GOLD, CLICK, CLICK + .15),
             s=Track(0, (58.9, 0, lin), (59.25, 1, out_back), (CLICK - .05, 1, lin), (CLICK + .05, .9, lin),
                     (CLICK + .35, 1, out_back)), a=life(58.9, KO)), 58.9)
S.add(Cursor(x=Track(XK + 300, (59.8, XK + 300, lin), (60.55, XK + 30, in_out_cubic)),
             y=Track(560, (59.8, 560, lin), (60.55, 215, in_out_cubic)), size=44,
             s=Track(1, (CLICK - .05, 1, lin), (CLICK + .05, .85, lin), (CLICK + .25, 1, out_cubic)),
             a=life(59.8, 62.4)), CLICK)
S.sfx.append((CLICK + .02, "tick"))
S.add(Rays(x=const(XK), y=const(-150), r=190, n=7, prog=Track(0, (CLICK, 0, lin), (CLICK + .3, 1, out_back)),
           color=GOLD, a=life(CLICK, KO), float_amp=0))


def mix(root):
    mix_voice(f"{root}/video_08.mp4", [(os.path.join(HERE, "assets", "voz08", f), t) for f, t in VOZ],
              f"{root}/guidelight_parece_loucura_9x16.mp4", voice_vol=1.2)


if __name__ == "__main__":
    root = os.path.join(HERE, "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills08", exist_ok=True)
        for f in os.listdir(f"{root}/stills08"):
            os.remove(f"{root}/stills08/{f}")
        for t in [7.2, 12.9, 16.6, 20.0, 25.4, 31.5, 38.3, 44.0, 49.6, 57.6, 61.5]:
            S.still(t, f"{root}/stills08/t{t:05.1f}.png")
        print("stills ok")
    elif "--mix" in sys.argv:
        mix(root)
    else:
        S.render(f"{root}/video_08.mp4")
        mix(root)
