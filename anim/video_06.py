"""
Vídeo 06: "Não salva esse vídeo": o macete do algoritmo e o dinheiro fácil  (9:16, 1080×1920, ≈54 s)
Página: Guidelight. Roteiro e os 12 ganchos: docs/roteiros/video_06_macete_algoritmo.md
Narração: ElevenLabs, voz "Elvis – Social Media & Shorts" (zNEsdgTUa3ndwKry8Xcq), eleven_v4, em anim/assets/voz06/

Rodar:  python3 anim/video_06.py --stills | --mix | (sem nada: render + mix)
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from engine import *  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = (255, 196, 56)
RED = (255, 82, 82)
GREEN = (64, 222, 140)
GREY = (150, 150, 150)

S = Scene(W=1080, H=1920, fps=30, duration=54.0, base_w=720)
PILL = 19

VOZ = [("s01.mp3", 0.05), ("s02.mp3", 1.9), ("s03.mp3", 9.6), ("s04.mp3", 13.9), ("s05.mp3", 20.9),
       ("s06.mp3", 29.4), ("s07.mp3", 34.9), ("s08.mp3", 41.2), ("s09.mp3", 45.9), ("s10.mp3", 49.3)]


def clamp01(x):
    return max(0.0, min(1.0, x))


def cut(t):
    return t + 0.015


def counter(fmt, v0, v1, t0, dur, ease=out_cubic):
    return lambda t: fmt(v0 + (v1 - v0) * ease(clamp01((t - t0) / dur)))


def br_int(v):
    return f"{int(round(v)):,}".replace(",", ".")


# ---------------------------------------------------------------- elementos
@dataclass
class Action(El):
    """Ícones de ação de rede social: heart, bubble, bookmark, plus, share. Acende (preenche) a partir de on_t."""
    kind: str = "heart"
    r: float = 30
    on_t: float = 999
    on_color: tuple = GOLD
    float_amp: float = 0

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        on = c.t >= self.on_t
        p = clamp01((c.t - self.on_t) / .25)
        col = tuple(int(v * a) for v in (self.on_color if on else self.color))
        fill = tuple(int(v * a * .9 * p) for v in self.on_color) if on else (0, 0, 0)
        sw = max(1, int(3.2 * k))
        if on:
            r *= 1 + .25 * math.sin(p * math.pi)
        if self.kind == "heart":
            pts = []
            for i in range(40):
                t = i / 40 * 2 * math.pi
                x = 16 * math.sin(t) ** 3
                y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
                pts.append((X + x * r / 17, Y + y * r / 17))
            c.d.polygon(pts, outline=col, width=sw, fill=fill)
        elif self.kind == "bubble":
            c.d.ellipse([X - r, Y - r * .8, X + r, Y + r * .7], outline=col, width=sw, fill=fill)
            c.d.polygon([(X - r * .5, Y + r * .5), (X - r * .7, Y + r * 1.05), (X - r * .05, Y + r * .65)],
                        outline=col, width=sw, fill=fill)
            for dx in (-.45, 0, .45):
                d = r * .1
                c.d.ellipse([X + dx * r - d, Y - d - r * .05, X + dx * r + d, Y + d - r * .05],
                            fill=(0, 0, 0) if on else col)
        elif self.kind == "bookmark":
            w = r * 1.3
            c.d.polygon([(X - w / 2, Y - r), (X + w / 2, Y - r), (X + w / 2, Y + r), (X, Y + r * .45), (X - w / 2, Y + r)],
                        outline=col, width=sw, fill=fill)
        elif self.kind == "plus":
            c.d.ellipse([X - r, Y - r, X + r, Y + r], outline=col, width=sw, fill=fill)
            lc = (0, 0, 0) if on else col
            c.d.line([(X - r * .5, Y), (X + r * .5, Y)], fill=lc, width=sw)
            c.d.line([(X, Y - r * .5), (X, Y + r * .5)], fill=lc, width=sw)
        elif self.kind == "share":
            pts = [(X - r, Y + r * .55), (X - r * .2, Y - r * .25), (X - r * .2, Y - r * .7), (X + r, Y + r * .05),
                   (X - r * .2, Y + r * .75), (X - r * .2, Y + r * .3)]
            c.d.polygon(pts, outline=col, width=sw, fill=fill)


@dataclass
class Phone(El):
    w: float = 330
    h: float = 620

    def paint(self, c, X, Y, k, a):
        w, h = self.w * k, self.h * k
        col = self.c(a)
        sw = max(1, int(3.6 * k))
        c.d.rounded_rectangle([X - w / 2, Y - h / 2, X + w / 2, Y + h / 2], radius=40 * k, outline=col, width=sw,
                              fill=(0, 0, 0))
        c.d.line([(X - w * .13, Y - h / 2 + 20 * k), (X + w * .13, Y - h / 2 + 20 * k)], fill=col, width=sw)


@dataclass
class Captcha(El):
    w: float = 470
    label: str = "NÃO SOU UM ROBÔ"
    check_t: float = 999

    def paint(self, c, X, Y, k, a):
        w, h = self.w * k, 110 * k
        col = self.c(a)
        sw = max(1, int(3.2 * k))
        c.d.rounded_rectangle([X - w / 2, Y - h / 2, X + w / 2, Y + h / 2], radius=12 * k, outline=col, width=sw,
                              fill=(0, 0, 0))
        b = 50 * k
        bx = X - w / 2 + 30 * k
        c.d.rounded_rectangle([bx, Y - b / 2, bx + b, Y + b / 2], radius=6 * k, outline=col, width=sw)
        p = clamp01((c.t - self.check_t) / .25)
        if p > 0:
            g = tuple(int(v * a) for v in GREEN)
            pts = [(bx + b * .18, Y), (bx + b * .42, Y + b * .25), (bx + b * .85, Y - b * .3)]
            c.d.line(pts[:2] if p < .5 else pts, fill=g, width=max(2, int(5 * k)), joint="curve")
        c.d.text((bx + b + 24 * k, Y), self.label, font=font("Black", 30 * k), fill=col, anchor="lm")


@dataclass
class BigButton(El):
    w: float = 260

    def paint(self, c, X, Y, k, a):
        w = self.w * k
        col = self.c(a)
        red = tuple(int(v * a) for v in RED)
        sw = max(1, int(3.4 * k))
        c.d.rounded_rectangle([X - w / 2, Y - w * .05, X + w / 2, Y + w * .18], radius=10 * k, outline=col, width=sw,
                              fill=(0, 0, 0))
        press = 6 * k * (1 + math.sin(c.t * 6)) / 2
        c.d.chord([X - w * .36, Y - w * .32 + press, X + w * .36, Y + w * .12 + press], 180, 360, fill=red, outline=red)


@dataclass
class Slot(El):
    w: float = 380
    stop_t: float = 0

    def paint(self, c, X, Y, k, a):
        w, h = self.w * k, self.w * .62 * k
        col = self.c(a)
        sw = max(1, int(3.4 * k))
        c.d.rounded_rectangle([X - w / 2, Y - h / 2, X + w / 2, Y + h / 2], radius=18 * k, outline=col, width=sw,
                              fill=(0, 0, 0))
        cw = w * .26
        for i in range(3):
            cx = X - w * .3 + i * w * .3
            c.d.rounded_rectangle([cx - cw / 2, Y - h * .3, cx + cw / 2, Y + h * .3], radius=8 * k, outline=col,
                                  width=max(1, int(2.4 * k)))
            stopped = c.t >= self.stop_t + i * .25
            if stopped:
                d, colr = "7", GOLD
            else:
                random.seed(int(c.t * 20) * 7 + i)
                d, colr = str(random.randint(0, 9)), (200, 200, 200)
            c.d.text((cx, Y), d, font=font("Black", h * .42), fill=tuple(int(v * a) for v in colr), anchor="mm")
        lx = X + w / 2 + 26 * k
        c.d.line([(X + w / 2, Y), (lx, Y), (lx, Y - h * .55)], fill=col, width=sw)
        r = 14 * k
        c.d.ellipse([lx - r, Y - h * .55 - r, lx + r, Y - h * .55 + r], fill=tuple(int(v * a) for v in RED))


@dataclass
class Gauge(El):
    w: float = 460
    h: float = 34
    label: str = ""
    value: Callable = const(1)
    float_amp: float = 0

    def paint(self, c, X, Y, k, a):
        v = clamp01(self.value(c.t))
        w, h = self.w * k, self.h * k
        col = self.c(a)
        x0 = X - w / 2
        c.d.rounded_rectangle([x0, Y - h / 2, x0 + w, Y + h / 2], radius=h / 2, outline=tuple(int(q * a * .7) for q in (255, 255, 255)),
                              width=max(1, int(2.6 * k)), fill=(0, 0, 0))
        if v > 0.01:
            c.d.rounded_rectangle([x0 + 5 * k, Y - h / 2 + 5 * k, x0 + 5 * k + (w - 10 * k) * v, Y + h / 2 - 5 * k],
                                  radius=(h - 10 * k) / 2, fill=col)
        c.d.text((x0, Y - h / 2 - 22 * k), self.label, font=font("Black", 20 * k), fill=(int(255 * a),) * 3, anchor="lm")
        c.d.text((x0 + w, Y - h / 2 - 22 * k), f"{int(round(v * 100))}%", font=font("Black", 26 * k), fill=col, anchor="rm")


def P(x, y, text, t, t_out=None, color=(255, 255, 255), size=PILL, dim_at=None, dim_to=.3):
    return S.add(Pill(x=const(x), y=const(y), text=text, size=size, color=color, s=appear(t),
                      a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


def T(x, y, text, t, t_out=None, size=60, color=(255, 255, 255), weight="Black", dim_at=None, dim_to=.3, dur=.35):
    return S.add(Text(x=const(x), y=const(y), text=text, size=size, weight=weight, color=color,
                      s=appear(t, dur), a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


# ---------------------------------------------------------------- câmera
XA, XC, XD, XE, XF, XG, XH, XI, XJ = [i * 1500 for i in range(9)]
S.cam_x = Track(XA, (cut(9.45), XA, lin), (cut(9.45) + .001, XC, lin),
                (13.6, XC, lin), (13.95, XD, in_out_cubic),
                (cut(20.75), XD, lin), (cut(20.75) + .001, XE, lin),
                (29.1, XE, lin), (29.45, XF, in_out_cubic),
                (cut(34.75), XF, lin), (cut(34.75) + .001, XG, lin),
                (cut(41.05), XG, lin), (cut(41.05) + .001, XH, lin),
                (45.6, XH, lin), (45.95, XI, in_out_cubic),
                (49.0, XI, lin), (49.35, XJ, in_out_cubic))
S.cam_y = const(0)
S.ground_a = const(0)
S.invert = Track(0, (cut(41.05), 0, lin), (cut(41.05) + .1, 1, out_cubic), (45.5, 1, lin), (45.6, 0, in_cubic))
S.sfx += [(t, "whoosh") for t in (13.55, 29.05, 45.55, 48.95)] + [(t, "thud") for t in (9.45, 20.75, 34.75, 41.05)]

# ---------------------------------------------------------------- A+B: gancho + "aqueles vídeos" (0–9.4)
AO = 9.4
T(XA, -480, "NÃO SALVA", .05, 1.85, size=88, color=RED, dur=.25)
T(XA, -390, "ESSE VÍDEO.", .2, 1.85, size=70, dur=.25)
S.sfx.append((.05, "thud"))
S.add(Phone(x=const(XA), y=const(20), s=appear(.05, .3, s0=.7), a=life(.05, AO, dim_at=7.3, dim_to=.35)))
ICONS = [("heart", 3.35, "CURTE"), ("bubble", 4.0, "COMENTA"), ("bookmark", 4.6, "SALVA"), ("plus", 5.3, "SEGUE"),
         ("share", 6.05, "REPUBLICA")]
for i, (kind, t_on, lab) in enumerate(ICONS):
    S.add(Action(x=const(XA + 115), y=const(-170 + i * 95), kind=kind, r=28, on_t=t_on, s=appear(.15 + i * .05),
                 a=life(.15, AO, dim_at=7.3, dim_to=.35)))
    S.sfx.append((t_on, "pop"))
    S.add(Text(x=const(XA - 50), y=const(20), text=lab, size=48, weight="Black", color=GOLD,
               s=Track(0, (t_on, 1.4, lin), (t_on + .2, 1, out_cubic)),
               a=Track(0, (t_on, 0, lin), (t_on + .06, 1, lin), (t_on + .5, 1, lin), (t_on + .6, 0, lin))))
# o X no salvar, durante o gancho
S.add(XIcon(x=const(XA + 115), y=const(20), r=40, color=RED, s=appear(.6, .3), a=life(.6, 1.85)), .6, "thud")
P(XA, -440, "SABE AQUELES VÍDEOS?", 1.95, AO, size=22)
P(XA, 400, "PRO ALGORITMO…", 7.3, AO, size=20)
S.add(Captcha(x=const(XA), y=const(510), check_t=8.6, s=appear(7.7, .35), a=life(7.7, AO)), 7.7)
S.sfx.append((8.6, "tick"))

# ---------------------------------------------------------------- C: milhões de views (9.6–13.6)
CO = 13.6
S.add(Text(x=const(XC), y=const(-330), size=96, weight="Black",
           text=counter(lambda v: br_int(v), 0, 2400000, 9.7, 1.6), s=appear(9.6, .3), a=life(9.6, CO)), 9.6)
S.sfx += [(9.7 + i * .1, "tick") for i in range(16)]
P(XC, -230, "VISUALIZAÇÕES", 10.0, CO, size=22)
S.add(Gauge(x=const(XC), y=const(60), w=520, label="CONTEÚDO", color=RED,
            value=Track(0, (11.8, 0, lin), (12.4, .06, out_cubic)), s=appear(11.75, .3, s0=.8), a=life(11.75, CO)), 11.75)
P(XC, 160, "QUASE NENHUM", 12.4, CO, color=RED, size=21)

# ---------------------------------------------------------------- D: botão secreto (13.9–20.6)
DO = 20.75
T(XD, -460, "O IMPULSO", 13.95, DO, size=76)
P(XD, -380, "POR TRÁS DISSO", 14.8, DO, size=20)
S.add(BigButton(x=const(XD + 120), y=const(120), w=280, s=appear(16.4, .4), a=life(16.4, DO)), 16.4, "thud")
P(XD + 120, -40, "BOTÃO SECRETO", 16.7, DO, color=GOLD, size=22)
S.add(Person(x=Track(XD - 240, (17.6, XD - 240, lin), (19.0, XD - 70, in_out_cubic)), y=const(330), h=150,
             legs=True, run=Track(0, (17.5, 0, lin), (17.7, .55, lin), (18.8, .55, lin), (19.0, 0, lin)), gait=8,
             float_amp=0, s=appear(14.0), a=life(14.0, DO)), 14.0)
P(XD, 450, "RESULTADO SEM ESFORÇO", 18.9, DO, color=RED, size=21)

# ---------------------------------------------------------------- E: dinheiro fácil (20.9–29.1)
EO = 29.1
T(XE, -470, "MESMO IMPULSO", 20.95, EO, size=66)
T(XE, -390, "DINHEIRO FÁCIL", 22.6, EO, size=50, color=GOLD)
S.add(Slot(x=const(XE), y=const(-170), w=380, stop_t=23.4, s=appear(21.1, .4), a=life(21.1, EO)), 21.1)
S.sfx += [(23.4 + i * .25, "pop") for i in range(3)]
P(XE, 60, "A APOSTA", 24.3, EO, size=22)
P(XE, 140, "O CURSO MILAGROSO", 25.4, EO, size=22)
P(XE, 220, "RENDE 30% AO MÊS", 26.8, EO, size=22, color=RED)
S.add(WarnIcon(x=const(XE), y=const(320), r=30, color=RED, s=appear(27.4), a=life(27.4, EO)), 27.4, "thud")

# ---------------------------------------------------------------- F: valor (29.4–34.6)
FO = 34.75
T(XF, -420, "O QUE SEGURA", 29.5, FO, size=56)
T(XF, -350, "ALGUÉM NO SEU VÍDEO?", 29.9, FO, size=44)
T(XF, -90, "VALOR", 32.2, FO, size=150, color=GREEN, dur=.3)
S.add(Rays(x=const(XF), y=const(-90), r=165, n=7, prog=Track(0, (32.3, 0, lin), (32.6, 1, out_back)), color=GREEN,
           a=life(32.3, FO), float_amp=0))
S.sfx.append((32.2, "thud"))
T(XF, 140, "\"SALVA AÍ\"", 33.25, FO, size=70, color=GREY)
S.add(Path(x=const(XF - 190), y=const(140), pts=[(0, 0), (380, 0)], width=6, color=RED,
           prog=Track(0, (33.7, 0, lin), (34.0, 1, out_cubic)), a=life(33.7, FO), float_amp=0))

# ---------------------------------------------------------------- G: gráfico (34.9–40.9)
GO = 41.05
T(XG, -470, "COM DINHEIRO", 34.95, GO, size=62)
T(XG, -395, "É IGUAL", 35.3, GO, size=62)
GX, GY = XG - 300, 260
S.add(Path(x=const(GX), y=const(GY), pts=[(0, -440), (0, 0), (600, 0)], width=2.4, color=GREY,
           prog=Track(0, (35.4, 0, lin), (35.9, 1, out_cubic)), a=life(35.4, GO)))
mac = [(0, 0), (60, -10), (110, -40), (150, -300), (175, -330), (200, -80), (240, -20), (600, -10)]
S.add(Path(x=const(GX), y=const(GY), pts=mac, width=4, color=RED,
           prog=Track(0, (36.7, 0, lin), (38.5, 1, lin)), a=life(36.7, GO, dim_at=39.1, dim_to=.35)), 36.7)
P(GX + 175, GY - 370, "MACETE", 37.3, GO, color=RED, size=18, dim_at=39.1, dim_to=.35)
steps = []
for i in range(10):
    x0, y0 = i * 60, -i * 40
    steps += [(x0, y0), (x0 + 60, y0)]
    steps += [(x0 + 60, y0 - 40)]
S.add(Path(x=const(GX), y=const(GY), pts=steps[:-1], width=4.5, color=GREEN,
           prog=Track(0, (39.15, 0, lin), (40.8, 1, lin)), a=life(39.15, GO)), 39.15)
P(GX + 420, GY - 430, "VALOR + CONSTÂNCIA", 39.6, GO, color=GREEN, size=18)

# ---------------------------------------------------------------- H: o verdadeiro robô (41.2–45.6), inversão
HO = 45.55
T(XH, -460, "O VERDADEIRO", 41.25, HO, size=66)
T(XH, -360, "ROBÔ", 41.5, HO, size=96)
S.add(Captcha(x=const(XH), y=const(-120), w=500, label="VOCÊ É UM ROBÔ?", s=appear(42.0, .35), a=life(42.0, HO)), 42.0)
P(XH, 60, "REPETE MACETE", 43.2, HO, size=24)
P(XH, 140, "SEM CONSTRUIR NADA", 44.2, HO, size=24)

# ---------------------------------------------------------------- I: aplica (45.9–48.9)
IO = 49.0
S.add(Action(x=const(XI), y=const(-250), kind="bookmark", r=70, s=appear(45.95, .3), a=life(45.95, IO)), 45.95)
S.add(XIcon(x=const(XI + 70), y=const(-310), r=34, color=RED, s=appear(46.6), a=life(46.6, IO)), 46.6, "thud")
T(XI, -100, "NÃO SALVA.", 46.1, IO, size=70, dim_at=48.2, dim_to=.35)
T(XI, 130, "APLICA.", 48.15, IO, size=150, color=GOLD, dur=.3)
S.add(Rays(x=const(XI), y=const(130), r=185, n=9, prog=Track(0, (48.2, 0, lin), (48.5, 1, out_back)), color=GOLD,
           a=life(48.2, IO), float_amp=0))
S.sfx.append((48.15, "thud"))

# ---------------------------------------------------------------- J: final (49.1–54)
JO = 53.7
P(XJ, -390, "SIGA A PÁGINA", 49.9, JO, size=22)
S.add(Avatar(x=const(XJ), y=const(-150), r=150, path=os.path.join(HERE, "assets", "guidelight.jpg"), ring=GOLD,
             s=appear(49.2, .45), a=life(49.2, JO)), 49.2, "thud")
T(XJ, 80, "GUIDELIGHT", 49.5, JO, size=78)
CLICK = 51.6
S.add(Button(x=const(XJ), y=const(210), w=300, h=78, text=lambda t: "SEGUINDO" if t >= CLICK else "SEGUIR",
             fill=lerp_color((255, 255, 255), GOLD, CLICK, CLICK + .15),
             s=Track(0, (49.9, 0, lin), (50.25, 1, out_back), (CLICK - .05, 1, lin), (CLICK + .05, .9, lin),
                     (CLICK + .35, 1, out_back)), a=life(49.9, JO)), 49.9)
S.add(Cursor(x=Track(XJ + 300, (50.7, XJ + 300, lin), (51.45, XJ + 30, in_out_cubic)),
             y=Track(560, (50.7, 560, lin), (51.45, 215, in_out_cubic)), size=44,
             s=Track(1, (CLICK - .05, 1, lin), (CLICK + .05, .85, lin), (CLICK + .25, 1, out_cubic)),
             a=life(50.7, 53.3)), CLICK)
S.sfx.append((CLICK + .02, "tick"))
S.add(Rays(x=const(XJ), y=const(-150), r=190, n=7, prog=Track(0, (CLICK, 0, lin), (CLICK + .3, 1, out_back)),
           color=GOLD, a=life(CLICK, JO), float_amp=0))


def mix(root):
    mix_voice(f"{root}/video_06.mp4", [(os.path.join(HERE, "assets", "voz06", f), t) for f, t in VOZ],
              f"{root}/guidelight_macete_algoritmo_9x16.mp4", voice_vol=1.2)


if __name__ == "__main__":
    root = os.path.join(HERE, "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills06", exist_ok=True)
        for f in os.listdir(f"{root}/stills06"):
            os.remove(f"{root}/stills06/{f}")
        for t in [1.2, 4.7, 9.0, 13.2, 20.0, 28.5, 34.2, 40.7, 44.8, 48.7, 52.5]:
            S.still(t, f"{root}/stills06/t{t:05.1f}.png")
        print("stills ok")
    elif "--mix" in sys.argv:
        mix(root)
    else:
        S.render(f"{root}/video_06.mp4")
        mix(root)
