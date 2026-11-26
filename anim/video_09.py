"""
Vídeo 09: "Se você perdesse sua renda amanhã, quanto tempo sua rotina aguentaria de pé?"  (9:16, ≈59 s)
Página: Guidelight. Roteiro: docs/roteiros/video_09_quanto_tempo_aguenta.md
Narração: ElevenLabs, voz "Elvis – Social Media & Shorts" (zNEsdgTUa3ndwKry8Xcq), eleven_v4, em anim/assets/voz09/

Rodar:  python3 anim/video_09.py --stills | --mix | (sem nada: render + mix)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from engine import *  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = (255, 196, 56)
RED = (255, 82, 82)
GREEN = (64, 222, 140)
GREY = (150, 150, 150)

S = Scene(W=1080, H=1920, fps=30, duration=59.3, base_w=720)
PILL = 19

VOZ = [("s01.mp3", 0.05), ("s02.mp3", 5.95), ("s03.mp3", 9.3), ("s04.mp3", 15.3), ("s05.mp3", 18.9),
       ("s06.mp3", 24.3), ("s07.mp3", 29.9), ("s08.mp3", 36.4), ("s09.mp3", 39.6), ("s10.mp3", 47.2),
       ("s11.mp3", 54.6)]


def clamp01(x):
    return max(0.0, min(1.0, x))


def cut(t):
    return t + 0.015


def counter(fmt, v0, v1, t0, dur, ease=out_cubic):
    return lambda t: fmt(v0 + (v1 - v0) * ease(clamp01((t - t0) / dur)))


def br_int(v):
    return f"{int(round(v)):,}".replace(",", ".")


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
class Months(El):
    """Blocos de meses que acendem (um por mês)."""
    n: int = 6
    cols: int = 6
    filled: Callable = const(0)   # quantos estão cheios (float)
    cell: float = 82
    label: bool = True
    float_amp: float = 0

    def paint(self, c, X, Y, k, a):
        cell, gap = self.cell * k, 12 * k
        rows = (self.n + self.cols - 1) // self.cols
        W = self.cols * cell + (self.cols - 1) * gap
        f = self.filled(c.t)
        for i in range(self.n):
            r, cc = divmod(i, self.cols)
            x0 = X - W / 2 + cc * (cell + gap)
            y0 = Y + r * (cell + gap) - (rows * (cell + gap) - gap) / 2
            p = clamp01(f - i)
            col = self.c(a)
            c.d.rounded_rectangle([x0, y0, x0 + cell, y0 + cell], radius=10 * k, outline=self.c(a * .55),
                                  width=max(1, int(2.6 * k)), fill=(0, 0, 0))
            if p > 0:
                inset = (1 - out_back(p)) * cell * .4
                c.d.rounded_rectangle([x0 + 6 * k + inset, y0 + 6 * k + inset, x0 + cell - 6 * k - inset,
                                       y0 + cell - 6 * k - inset], radius=7 * k, fill=col)
            if self.label:
                c.d.text((x0 + cell / 2, y0 + cell / 2), str(i + 1), font=font("Black", cell * .36),
                         fill=(0, 0, 0) if p > .5 else self.c(a * .6), anchor="mm")


def P(x, y, text, t, t_out=None, color=(255, 255, 255), size=PILL, dim_at=None, dim_to=.3):
    return S.add(Pill(x=const(x), y=const(y), text=text, size=size, color=color, s=appear(t),
                      a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


def T(x, y, text, t, t_out=None, size=60, color=(255, 255, 255), weight="Black", dim_at=None, dim_to=.3, dur=.35):
    return S.add(Text(x=const(x), y=const(y), text=text, size=size, weight=weight, color=color,
                      s=appear(t, dur), a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


def ticks(t0, n, step):
    S.sfx.extend((t0 + i * step, "tick") for i in range(n))


# ---------------------------------------------------------------- câmera
XA, XB, XC, XF, XG, XH, XI, XJ, XK = [i * 1500 for i in range(9)]
S.cam_x = Track(XA, (cut(5.8), XA, lin), (cut(5.8) + .001, XB, lin),
                (9.0, XB, lin), (9.35, XC, in_out_cubic),
                (cut(24.15), XC, lin), (cut(24.15) + .001, XF, lin),
                (29.6, XF, lin), (29.95, XG, in_out_cubic),
                (cut(36.25), XG, lin), (cut(36.25) + .001, XH, lin),
                (39.3, XH, lin), (39.65, XI, in_out_cubic),
                (cut(47.05), XI, lin), (cut(47.05) + .001, XJ, lin),
                (54.2, XJ, lin), (54.55, XK, in_out_cubic))
S.cam_y = const(0)
S.ground_a = const(0)
S.invert = Track(0, (cut(5.8), 0, lin), (cut(5.8) + .1, 1, out_cubic), (8.95, 1, lin), (9.05, 0, in_cubic))
S.sfx += [(t, "whoosh") for t in (8.95, 29.55, 39.25, 54.15)] + \
         [(t, "thud") for t in (5.8, 24.15, 36.25, 47.05)]

# ---------------------------------------------------------------- A: gancho (0.05–5.65)
AO = 5.8
T(XA, -470, "SE VOCÊ PERDESSE", .05, AO, size=52, dur=.25)
T(XA, -395, "SUA RENDA AMANHÃ…", .9, AO, size=50, color=RED)
S.sfx.append((.05, "thud"))
COL_Y = 260
S.add(Box(x=lambda t: XA + (math.sin(t * 50) * 5 if 1.2 < t < 2.4 else 0),
          y=Track(COL_Y, (2.5, COL_Y, lin), (3.1, COL_Y + 900, in_cubic)), w=210, h=330,
          label="RENDA", size=36, s=appear(.1, .35), a=life(.1, 3.0)), .1)
S.sfx.append((3.0, "thud"))
P(XA, 150, "PRINCIPAL", .4, 2.5, size=16)
person_y = Track(COL_Y - 165, (3.2, COL_Y - 165, lin), (5.6, COL_Y + 60, in_cubic))
S.add(Person(x=const(XA), y=person_y, h=150, s=appear(.2), a=life(.2, AO), float_amp=0), .2)
S.add(Path(x=const(XA - 130), y=const(COL_Y - 165), pts=[(0, 0), (260, 0)], width=3, color=RED,
           prog=Track(0, (3.0, 0, lin), (3.3, 1, out_cubic)), a=life(3.0, AO), float_amp=0))
T(XA, -250, "QUANTO TEMPO", 3.5, AO, size=66, color=GOLD)
P(XA, -165, "SUA ROTINA AGUENTA DE PÉ?", 4.2, AO, size=21, color=GOLD)
S.add(Clock(x=const(XA + 230), y=const(-40), r=50, speed=18, color=GOLD, s=appear(3.6), a=life(3.6, AO)), 3.6)

# ---------------------------------------------------------------- B: uma semana? (5.95–9.0), inversão
BO = 9.0
T(XB, -250, "UMA SEMANA?", 5.95, BO, size=84, dim_at=7.15, dim_to=.3)
T(XB, -60, "UM MÊS?", 7.2, BO, size=100, dim_at=8.2, dim_to=.3)
T(XB, 150, "OU NEM ISSO?", 8.25, BO, size=92, dur=.25)
S.sfx += [(5.95, "pop"), (7.2, "pop"), (8.25, "thud")]

# ---------------------------------------------------------------- C: a conta (9.3–24.0)
CO = 24.15
T(XC, -470, "FAZ A CONTA", 9.35, CO, size=72)
P(XC, -395, "É SIMPLES", 10.65, CO, size=22, color=GOLD)
S.add(Box(x=const(XC), y=const(-290), w=420, h=120, label="", color=GOLD, s=appear(12.0), a=life(12.0, CO)), 12.0, "pop")
S.add(Text(x=const(XC), y=const(-290), size=62, weight="Black", color=GOLD,
           text=counter(lambda v: f"R$ {br_int(v)}", 0, 6000, 12.3, 1.2), s=appear(12.1), a=life(12.1, CO)))
ticks(12.3, 10, .12)
P(XC, -205, "GUARDADO E FÁCIL DE SACAR", 12.6, CO, size=19, color=GOLD)
T(XC, -115, "÷", 15.35, CO, size=90)
S.add(Box(x=const(XC), y=const(-10), w=420, h=120, label="", color=RED, s=appear(15.5), a=life(15.5, CO)), 15.5, "pop")
S.add(Text(x=const(XC), y=const(-10), size=62, weight="Black", color=RED,
           text=counter(lambda v: f"R$ {br_int(v)}", 0, 3000, 15.8, 1.0), s=appear(15.6), a=life(15.6, CO)))
ticks(15.8, 8, .12)
P(XC, 75, "QUANTO VOCÊ GASTA POR MÊS", 16.3, CO, size=19, color=RED)
S.add(Rays(x=const(XC), y=const(-290), r=230, n=7, prog=Track(0, (18.95, 0, lin), (19.25, 1, out_back)), color=GOLD,
           a=life(18.95, 21.0), float_amp=0))
S.add(Rays(x=const(XC), y=const(-10), r=230, n=7, prog=Track(0, (21.0, 0, lin), (21.3, 1, out_back)), color=RED,
           a=life(21.0, 22.5), float_amp=0))
T(XC, 160, "=", 22.4, CO, size=90)
T(XC, 300, "2 MESES", 22.55, CO, size=120, color=GOLD, dur=.3)
S.sfx.append((22.55, "thud"))

# ---------------------------------------------------------------- F: fôlego (24.3–29.6)
FO = 29.6
T(XF, -430, "ESSE NÚMERO É", 24.35, FO, size=50)
T(XF, -340, "SEU FÔLEGO", 24.8, FO, size=86, color=GOLD)
S.add(Months(x=const(XF), y=const(-130), n=6, cols=6, cell=88, color=GOLD,
             filled=Track(0, (25.2, 0, lin), (25.9, 2, out_cubic)), s=appear(25.0, .3, s0=.8), a=life(25.0, FO)), 25.0)
P(XF, -40, "2 DE 6 MESES", 26.0, FO, size=20, color=GOLD)
P(XF, 120, "A MAIORIA NUNCA CALCULOU", 26.8, FO, size=22, color=RED)
S.add(Person(x=const(XF), y=const(400), h=140, s=appear(26.8), a=life(26.8, FO)), 26.8)
S.add(Text(x=const(XF + 90), y=const(240), text="?", size=70, weight="Black", s=appear(27.4), a=life(27.4, FO)))

# ---------------------------------------------------------------- G: referência (29.9–36.1)
GO = 36.25
P(XG, -470, "A REFERÊNCIA MAIS COMUM", 29.95, GO, size=22)
T(XG, -370, "RENDA ESTÁVEL", 31.6, GO, size=46, color=GREEN)
S.add(Months(x=const(XG), y=const(-260), n=6, cols=6, cell=80, color=GREEN,
             filled=Track(0, (31.8, 0, lin), (33.6, 6, lin)), s=appear(31.6, .3, s0=.8), a=life(31.6, GO)), 31.6)
ticks(31.8, 6, .3)
T(XG, -165, "6 MESES", 33.6, GO, size=40, color=GREEN)
T(XG, -40, "RENDA QUE OSCILA", 34.6, GO, size=46, color=GOLD)
S.add(Months(x=const(XG), y=const(110), n=12, cols=6, cell=80, color=GOLD,
             filled=Track(0, (34.7, 0, lin), (35.9, 12, lin)), s=appear(34.6, .3, s0=.8), a=life(34.6, GO)), 34.6)
ticks(34.7, 12, .1)
T(XG, 300, "1 ANO", 35.8, GO, size=46, color=GOLD)

# ---------------------------------------------------------------- H: começa pelo 1º mês (36.4–39.3)
HO = 39.3
T(XH, -330, "PARECE MUITO?", 36.45, HO, size=74, dim_at=37.7, dim_to=.35)
S.add(Months(x=const(XH), y=const(10), n=1, cols=1, cell=190, color=GOLD, label=False,
             filled=Track(0, (37.8, 0, lin), (38.2, 1, out_cubic)), s=appear(37.7, .35), a=life(37.7, HO)), 37.7, "thud")
S.add(Text(x=const(XH), y=const(10), text="1º", size=86, weight="Black", s=appear(37.75), a=life(37.75, HO),
           color=(10, 10, 10)))
S.add(Rays(x=const(XH), y=const(10), r=170, n=9, prog=Track(0, (38.0, 0, lin), (38.3, 1, out_back)), color=GOLD,
           a=life(38.0, HO), float_amp=0))
P(XH, 190, "COMEÇA PELO PRIMEIRO MÊS", 37.9, HO, size=22, color=GOLD)

# ---------------------------------------------------------------- I: como (39.6–46.9)
IO = 47.05
T(XI, -470, "COMO", 39.65, IO, size=76)
for i, (lab, t0) in enumerate([("CORTA UM GASTO QUE", 39.65), ("SEPARA TODO MÊS", 41.95), ("LUGAR SEGURO,", 43.65)]):
    y = -330 + i * 150
    S.add(Text(x=const(XI - 20), y=const(y), text=lab, size=36, weight="Black", s=appear(t0), a=life(t0, IO)), t0, "pop")
    sub = ["NÃO FAZ FALTA", None, "COM SAQUE RÁPIDO"][i]
    if sub:
        S.add(Text(x=const(XI - 20), y=const(y + 48), text=sub, size=36, weight="Black", s=appear(t0 + .1),
                   a=life(t0 + .1, IO)))
    S.add(CheckIcon(x=const(XI + 290), y=const(y + (24 if sub else 0)), r=22, color=GREEN, s=appear(t0 + .6),
                    a=life(t0 + .6, IO)), t0 + .6, "tick")
S.add(Months(x=const(XI), y=const(260), n=6, cols=6, cell=80, color=GOLD,
             filled=Track(0, (42.0, 0, lin), (46.6, 2.4, lin)), s=appear(41.9, .3, s0=.8), a=life(41.9, IO)), 41.9)
P(XI, 360, "RESERVA CRESCENDO", 42.4, IO, size=19, color=GOLD)

# ---------------------------------------------------------------- J: liberdade (47.2–54.2)
JO = 54.2
T(XJ, -470, "RESERVA NÃO É", 47.25, JO, size=50)
T(XJ, -395, "DINHEIRO PARADO", 47.7, JO, size=56)
PY = 300
S.add(Box(x=const(XJ - 110), y=Track(PY, (48.6, PY, lin), (49.2, PY + 900, in_cubic)), w=180, h=280, label="RENDA",
          size=28, s=appear(47.3, .35), a=life(47.3, 49.1)), 47.3)
S.sfx.append((49.1, "thud"))
S.add(Box(x=const(XJ + 110), y=const(PY), w=180, h=280, label="RESERVA", size=26, color=GOLD, s=appear(47.5, .35),
          a=life(47.5, JO)), 47.5)
S.add(Path(x=const(XJ - 220), y=const(PY - 140), pts=[(0, 0), (440, 0)], width=4, a=life(47.6, JO), float_amp=0))
S.add(Person(x=const(XJ + 40), y=const(PY - 140), h=150, color=GOLD, s=appear(47.7), a=life(47.7, JO), float_amp=0), 47.7)
T(XJ, -250, "É LIBERDADE", 50.1, JO, size=86, color=GOLD, dur=.3)
S.sfx.append((50.1, "thud"))
P(XJ, -160, "DE NÃO ACEITAR QUALQUER COISA", 51.3, JO, size=20, color=GOLD)
P(XJ, -95, "QUANDO A VIDA APERTA", 52.6, JO, size=20)

# ---------------------------------------------------------------- K: final (54.4–59.3)
KO = 59.0
P(XK, -390, "SIGA A PÁGINA", 55.2, KO, size=22)
S.add(Avatar(x=const(XK), y=const(-150), r=150, path=os.path.join(HERE, "assets", "guidelight.jpg"), ring=GOLD,
             s=appear(54.5, .45), a=life(54.5, KO)), 54.5, "thud")
T(XK, 80, "GUIDELIGHT", 54.8, KO, size=78)
CLICK = 57.1
S.add(Button(x=const(XK), y=const(210), w=300, h=78, text=lambda t: "SEGUINDO" if t >= CLICK else "SEGUIR",
             fill=lerp_color((255, 255, 255), GOLD, CLICK, CLICK + .15),
             s=Track(0, (55.3, 0, lin), (55.65, 1, out_back), (CLICK - .05, 1, lin), (CLICK + .05, .9, lin),
                     (CLICK + .35, 1, out_back)), a=life(55.3, KO)), 55.3)
S.add(Cursor(x=Track(XK + 300, (56.2, XK + 300, lin), (56.95, XK + 30, in_out_cubic)),
             y=Track(560, (56.2, 560, lin), (56.95, 215, in_out_cubic)), size=44,
             s=Track(1, (CLICK - .05, 1, lin), (CLICK + .05, .85, lin), (CLICK + .25, 1, out_cubic)),
             a=life(56.2, 58.7)), CLICK)
S.sfx.append((CLICK + .02, "tick"))
S.add(Rays(x=const(XK), y=const(-150), r=190, n=7, prog=Track(0, (CLICK, 0, lin), (CLICK + .3, 1, out_back)),
           color=GOLD, a=life(CLICK, KO), float_amp=0))


def mix(root):
    mix_voice(f"{root}/video_09.mp4", [(os.path.join(HERE, "assets", "voz09", f), t) for f, t in VOZ],
              f"{root}/guidelight_quanto_tempo_aguenta_9x16.mp4", voice_vol=1.2)


if __name__ == "__main__":
    root = os.path.join(HERE, "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills09", exist_ok=True)
        for f in os.listdir(f"{root}/stills09"):
            os.remove(f"{root}/stills09/{f}")
        for t in [1.8, 5.3, 8.7, 23.6, 29.2, 35.9, 38.9, 46.6, 49.5, 53.8, 58.0]:
            S.still(t, f"{root}/stills09/t{t:05.1f}.png")
        print("stills ok")
    elif "--mix" in sys.argv:
        mix(root)
    else:
        S.render(f"{root}/video_09.mp4")
        mix(root)
