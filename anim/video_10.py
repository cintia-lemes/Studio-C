"""
Vídeo 10: "A mesma desculpa"  (9:16, ≈61 s)
"A mesma desculpa que você usa pra faltar ao treino num dia cansativo é a que te faz parcelar o que você não precisa."
Página: Guidelight. Roteiro: docs/roteiros/video_10_mesma_desculpa.md
Narração: ElevenLabs, voz "Elvis – Social Media & Shorts" (zNEsdgTUa3ndwKry8Xcq), eleven_v4, em anim/assets/voz10/

Rodar:  python3 anim/video_10.py --stills | --mix | (sem nada: render + mix)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from engine import *  # noqa
import video_05 as v5  # PriceTag
import video_06 as v6  # Phone

PriceTag, Phone = v5.PriceTag, v6.Phone
HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = (255, 196, 56)
RED = (255, 82, 82)
GREEN = (64, 222, 140)
GREY = (150, 150, 150)

S = Scene(W=1080, H=1920, fps=30, duration=61.3, base_w=720)
PILL = 19

VOZ = [("s01.mp3", 0.05), ("s02.mp3", 6.4), ("s03.mp3", 12.7), ("s04.mp3", 17.2), ("s05.mp3", 21.9),
       ("s06.mp3", 30.6), ("s07.mp3", 37.9), ("s08.mp3", 46.0), ("s09.mp3", 52.5), ("s10.mp3", 56.6)]


def clamp01(x):
    return max(0.0, min(1.0, x))


def cut(t):
    return t + 0.015


@dataclass
class Dumbbell(El):
    w: float = 200

    def paint(self, c, X, Y, k, a):
        w = self.w * k
        col = self.c(a)
        sw = max(1, int(3.6 * k))
        c.d.line([(X - w * .32, Y), (X + w * .32, Y)], fill=col, width=int(w * .07))
        for s in (-1, 1):
            for j, (dx, hh) in enumerate([(.36, .42), (.46, .3)]):
                x = X + s * w * dx
                c.d.rounded_rectangle([x - w * .045, Y - w * hh / 2, x + w * .045, Y + w * hh / 2], radius=4 * k,
                                      outline=col, width=sw, fill=(0, 0, 0))


@dataclass
class Bag(El):
    w: float = 170

    def paint(self, c, X, Y, k, a):
        w = self.w * k
        h = w * 1.05
        col = self.c(a)
        sw = max(1, int(3.6 * k))
        top = Y - h * .35
        c.d.arc([X - w * .22, top - h * .35, X + w * .22, top + h * .2], 180, 360, fill=col, width=sw)
        c.d.polygon([(X - w * .5, top), (X + w * .5, top), (X + w * .56, Y + h * .62), (X - w * .56, Y + h * .62)],
                    outline=col, width=sw, fill=(0, 0, 0))


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


def P(x, y, text, t, t_out=None, color=(255, 255, 255), size=PILL, dim_at=None, dim_to=.3):
    return S.add(Pill(x=const(x), y=const(y), text=text, size=size, color=color, s=appear(t),
                      a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


def T(x, y, text, t, t_out=None, size=60, color=(255, 255, 255), weight="Black", dim_at=None, dim_to=.3, dur=.35):
    return S.add(Text(x=const(x), y=const(y), text=text, size=size, weight=weight, color=color,
                      s=appear(t, dur), a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


def X_(x, y, t, t_out, r=30):
    S.add(XIcon(x=const(x), y=const(y), r=r, color=RED, s=appear(t, .3), a=life(t, t_out)), t, "thud")


def OK(x, y, t, t_out, r=26):
    S.add(CheckIcon(x=const(x), y=const(y), r=r, color=GREEN, s=appear(t, .3), a=life(t, t_out)), t, "tick")


# ---------------------------------------------------------------- câmera
XA, XB, XC, XD, XE, XF, XG, XH, XI, XJ = [i * 1500 for i in range(10)]
S.cam_x = Track(XA, (cut(6.25), XA, lin), (cut(6.25) + .001, XB, lin),
                (12.4, XB, lin), (12.75, XC, in_out_cubic),
                (cut(17.05), XC, lin), (cut(17.05) + .001, XD, lin),
                (cut(21.75), XD, lin), (cut(21.75) + .001, XE, lin),
                (30.3, XE, lin), (30.65, XF, in_out_cubic),
                (cut(37.75), XF, lin), (cut(37.75) + .001, XG, lin),
                (45.7, XG, lin), (46.05, XH, in_out_cubic),
                (cut(52.35), XH, lin), (cut(52.35) + .001, XI, lin),
                (56.2, XI, lin), (56.55, XJ, in_out_cubic))
S.cam_y = const(0)
S.ground_a = const(0)
S.invert = Track(0, (cut(17.05), 0, lin), (cut(17.05) + .1, 1, out_cubic), (21.65, 1, lin), (21.75, 0, in_cubic))
S.sfx += [(t, "whoosh") for t in (12.35, 30.25, 45.65, 56.15)] + \
         [(t, "thud") for t in (6.25, 17.05, 21.75, 37.75, 52.35)]

# ---------------------------------------------------------------- A: gancho (0.05–6.1)
AO = 6.25
T(XA, -470, "A MESMA DESCULPA", .05, AO, size=62, dur=.25)
S.sfx.append((.05, "thud"))
S.add(Path(x=const(XA), y=const(-330), pts=[(0, 0), (0, 440)], width=2.4, color=GREY,
           prog=Track(0, (.2, 0, lin), (.6, 1, out_cubic)), a=life(.2, AO), float_amp=0))
P(XA - 180, -320, "TREINO", .3, AO, size=22)
S.add(Dumbbell(x=const(XA - 180), y=const(-60), w=230, s=appear(.4), a=life(.4, AO, dim_at=1.8, dim_to=.35)), .4)
X_(XA - 180, -60, 1.9, AO, 38)
P(XA - 180, 90, "FALTA", 2.1, AO, size=22, color=RED)
P(XA + 180, -320, "COMPRA", 3.3, AO, size=22)
S.add(Bag(x=const(XA + 180), y=const(-70), w=170, color=GOLD, s=appear(3.35), a=life(3.35, AO)), 3.35, "pop")
P(XA + 180, 90, "PARCELA 12x", 4.6, AO, size=22, color=RED)
T(XA, 280, "MESMA RAIZ", 5.3, AO, size=56, color=GOLD)

# ---------------------------------------------------------------- B: dia pesado (6.4–12.4)
BO = 12.4
T(XB, -440, "DIA PESADO.", 6.45, BO, size=80, color=RED)
S.add(Person(x=const(XB - 130), y=const(330), h=150, color=GREY, float_amp=0,
             s=Track(1, (6.5, 1, lin), (8.0, .9, in_out_cubic)), a=life(6.5, BO)), 6.5)
S.add(Dumbbell(x=const(XB + 160), y=const(260), w=180, s=appear(8.1), a=life(8.1, BO, dim_at=11.0, dim_to=.25)), 8.1)
P(XB, 30, "\"HOJE EU MEREÇO", 10.25, BO, size=26, color=GOLD)
P(XB, 100, "DESCANSAR\"", 10.6, BO, size=26, color=GOLD)
X_(XB + 160, 260, 11.2, BO, 30)

# ---------------------------------------------------------------- C: o mimo (12.7–16.9)
CO = 17.05
S.add(Phone(x=const(XC + 90), y=const(-90), w=300, h=560, s=appear(12.75, .35, s0=.8), a=life(12.75, CO)), 12.75)
S.add(Bag(x=const(XC + 90), y=const(-190), w=130, color=GOLD, s=appear(13.2), a=life(13.2, CO)), 13.2, "pop")
S.add(Text(x=const(XC + 90), y=const(-30), text="R$ 59,90", size=40, weight="Black", s=appear(13.5), a=life(13.5, CO)))
CLK = 16.4
S.add(Button(x=const(XC + 90), y=const(90), w=230, h=64, text=lambda t: "COMPRADO" if t >= CLK else "12x SEM JUROS",
             fill=lerp_color(GOLD, (255, 255, 255), CLK, CLK + .1), s=appear(14.2), a=life(14.2, CO)), 14.2)
S.add(Cursor(x=Track(XC + 260, (15.6, XC + 260, lin), (16.3, XC + 110, in_out_cubic)),
             y=Track(320, (15.6, 320, lin), (16.3, 95, in_out_cubic)), size=40, a=life(15.6, CO)), CLK, "tick")
S.add(Person(x=const(XC - 210), y=const(330), h=150, color=GREY, float_amp=0, s=appear(12.8), a=life(12.8, CO)), 12.8)
P(XC, 300 + 70, "\"HOJE EU MEREÇO ESSE MIMO\"", 15.0, CO, size=22, color=GOLD)

# ---------------------------------------------------------------- D: mesma frase (17.2–21.6), inversão
DO = 21.65
T(XD, -240, "MESMA FRASE.", 17.2, DO, size=74)
T(XD, -110, "MESMO CANSAÇO.", 18.5, DO, size=66)
T(XD, 60, "E A CONTA", 20.1, DO, size=74)
T(XD, 160, "CHEGA DEPOIS.", 20.45, DO, size=74)
S.sfx += [(17.2, "pop"), (18.5, "pop"), (20.1, "thud")]

# ---------------------------------------------------------------- E: as contas (21.9–30.3)
EO = 30.3
T(XE, -470, "NO TREINO", 21.9, EO, size=56)
S.add(Person(x=const(XE - 80), y=const(-150), h=150, color=GREY, s=appear(22.8), a=life(22.8, EO)), 22.8)
S.add(Person(x=const(XE + 80), y=const(-150), h=150, color=GREY, s=appear(23.2), a=life(23.2, EO)), 23.2)
P(XE, -95, "O CORPO NÃO MUDA", 23.85, EO, size=22, color=RED)
P(XE - 80, -330, "ANTES", 22.8, EO, size=15)
P(XE + 80, -330, "DEPOIS", 23.2, EO, size=15)
T(XE, 40, "NO DINHEIRO", 25.4, EO, size=56)
for i in range(12):
    r, cc = divmod(i, 4)
    t0 = 26.3 + i * .18
    S.add(PriceTag(x=const(XE - 225 + cc * 150), y=const(150 + r * 85), w=130, h=60, text=f"{i + 1}/12", color=RED,
                   s=appear(t0, .25), a=life(t0, EO)), t0, "tick")
P(XE, 440, "DE ALGO QUE VOCÊ NEM LEMBRA", 28.8, EO, size=20, color=RED)

# ---------------------------------------------------------------- F: o problema (30.6–37.6)
FO = 37.75
T(XF - 40, -400, "DESCANSAR", 30.65, FO, size=60, dim_at=34.5, dim_to=.35)
OK(XF + 210, -400, 31.6, FO)
T(XF - 40, -290, "SE DAR UM PRESENTE", 32.8, FO, size=42, dim_at=34.5, dim_to=.35)
OK(XF + 270, -290, 33.5, FO)
P(XF, -150, "O PROBLEMA É", 34.5, FO, size=24)
T(XF, -30, "O CANSAÇO", 35.3, FO, size=96, color=RED, dur=.3)
T(XF, 90, "DECIDIR POR VOCÊ", 36.2, FO, size=54)
S.sfx.append((35.3, "thud"))

# ---------------------------------------------------------------- G: a regra (37.9–45.7)
GO = 45.7
P(XG, -480, "UMA REGRA SIMPLES", 37.95, GO, size=24, color=GOLD)
T(XG, -390, "DIA CANSADO =", 39.45, GO, size=58)
T(XG, -310, "VERSÃO MENOR", 40.6, GO, size=72, color=GOLD)
S.add(Dumbbell(x=const(XG - 160), y=const(-80), w=200, color=GOLD, s=appear(42.3), a=life(42.3, GO)), 42.3, "pop")
T(XG - 160, 40, "15 MIN", 42.5, GO, size=52, color=GREEN)
OK(XG - 160, 120, 43.0, GO, 28)
S.add(Bag(x=const(XG + 160), y=const(-90), w=150, color=GREY, s=appear(44.0), a=life(44.0, GO)), 44.0, "pop")
T(XG + 160, 40, "PARCELADO", 44.2, GO, size=40, color=RED)
X_(XG + 160, 120, 44.8, GO, 28)

# ---------------------------------------------------------------- H: 24 horas (46.0–52.2)
HO = 52.35
S.add(Clock(x=const(XH), y=const(-300), r=110, speed=24, color=GOLD, s=appear(46.05, .35), a=life(46.05, HO)), 46.05)
S.add(Text(x=const(XH), y=const(-100), size=110, weight="Black", color=GOLD,
           text=lambda t: f"{int(round(24 * out_cubic(clamp01((t - 46.3) / 2.6))))}H", s=appear(46.2), a=life(46.2, HO)))
S.sfx += [(46.3 + i * .2, "tick") for i in range(13)]
P(XH, 20, "AINDA QUER?", 48.0, HO, size=26)
T(XH, 150, "AÍ VOCÊ DECIDE.", 49.8, HO, size=60)
T(XH, 260, "DESCANSADO.", 51.35, HO, size=76, color=GREEN, dur=.3)
S.sfx.append((51.35, "thud"))

# ---------------------------------------------------------------- I: fecho (52.5–56.2)
IO = 56.2
T(XI, -420, "QUEM CONTROLA", 52.5, IO, size=66)
T(XI, -330, "A DESCULPA…", 53.0, IO, size=66)
S.add(Dumbbell(x=const(XI - 160), y=const(-80), w=200, color=GOLD, s=appear(54.2), a=life(54.2, IO)), 54.2, "pop")
T(XI - 160, 60, "O CORPO", 54.25, IO, size=46, color=GOLD)
S.add(Bag(x=const(XI + 160), y=const(-90), w=150, color=GOLD, s=appear(55.45), a=life(55.45, IO)), 55.45, "pop")
T(XI + 160, 60, "O BOLSO", 55.45, IO, size=46, color=GOLD)
P(XI, 200, "CONTROLA", 54.0, IO, size=26)

# ---------------------------------------------------------------- J: final (56.4–61.3)
JO = 61.0
P(XJ, -390, "SIGA A PÁGINA", 57.2, JO, size=22)
S.add(Avatar(x=const(XJ), y=const(-150), r=150, path=os.path.join(HERE, "assets", "guidelight.jpg"), ring=GOLD,
             s=appear(56.5, .45), a=life(56.5, JO)), 56.5, "thud")
T(XJ, 80, "GUIDELIGHT", 56.8, JO, size=78)
CLICK = 59.1
S.add(Button(x=const(XJ), y=const(210), w=300, h=78, text=lambda t: "SEGUINDO" if t >= CLICK else "SEGUIR",
             fill=lerp_color((255, 255, 255), GOLD, CLICK, CLICK + .15),
             s=Track(0, (57.3, 0, lin), (57.65, 1, out_back), (CLICK - .05, 1, lin), (CLICK + .05, .9, lin),
                     (CLICK + .35, 1, out_back)), a=life(57.3, JO)), 57.3)
S.add(Cursor(x=Track(XJ + 300, (58.2, XJ + 300, lin), (58.95, XJ + 30, in_out_cubic)),
             y=Track(560, (58.2, 560, lin), (58.95, 215, in_out_cubic)), size=44,
             s=Track(1, (CLICK - .05, 1, lin), (CLICK + .05, .85, lin), (CLICK + .25, 1, out_cubic)),
             a=life(58.2, 60.7)), CLICK)
S.sfx.append((CLICK + .02, "tick"))
S.add(Rays(x=const(XJ), y=const(-150), r=190, n=7, prog=Track(0, (CLICK, 0, lin), (CLICK + .3, 1, out_back)),
           color=GOLD, a=life(CLICK, JO), float_amp=0))


def mix(root):
    mix_voice(f"{root}/video_10.mp4", [(os.path.join(HERE, "assets", "voz10", f), t) for f, t in VOZ],
              f"{root}/guidelight_mesma_desculpa_9x16.mp4", voice_vol=1.2)


if __name__ == "__main__":
    root = os.path.join(HERE, "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills10", exist_ok=True)
        for f in os.listdir(f"{root}/stills10"):
            os.remove(f"{root}/stills10/{f}")
        for t in [5.8, 12.0, 16.7, 21.3, 29.9, 37.3, 45.3, 52.0, 55.9, 60.0]:
            S.still(t, f"{root}/stills10/t{t:05.1f}.png")
        print("stills ok")
    elif "--mix" in sys.argv:
        mix(root)
    else:
        S.render(f"{root}/video_10.mp4")
        mix(root)
