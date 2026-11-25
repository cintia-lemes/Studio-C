"""
Vídeo 04: Lei 3, "Oculte suas intenções" (As 48 Leis do Poder)  (9:16, 1080×1920, ≈48 s)
Página: Guidelight. Roteiro: docs/roteiros/video_04_lei3_oculte_intencoes.md
Narração: ElevenLabs, voz "Nassif – Documentary, History & Thriller" (acdKA5HckGxoxxvy40dA), eleven_v4,
em anim/assets/voz04/ (1ª versão, mais curta, com a voz Letícia: anim/assets/voz04_leticia_v1/ e histórico do git)

Rodar:  python3 anim/video_04.py --stills | --mix | (sem nada: render + mix)
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

S = Scene(W=1080, H=1920, fps=30, duration=71.5, base_w=720)
PILL = 19
GY = 250  # chão das cenas com bonecos

VOZ = [("s01.mp3", 0.1), ("s02.mp3", 5.9), ("s03.mp3", 13.0), ("s04.mp3", 17.6), ("s05.mp3", 25.7),
       ("s06.mp3", 33.9), ("s07.mp3", 39.0), ("s08.mp3", 43.8), ("s09.mp3", 48.4), ("s10.mp3", 53.0),
       ("s11.mp3", 59.8), ("s12.mp3", 64.0), ("s13.mp3", 66.8)]


def clamp01(x):
    return max(0.0, min(1.0, x))


def cut(t):
    return t + 0.015


# ---------------------------------------------------------------- elementos
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
class Clock(El):
    r: float = 40
    speed: float = 8

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        col = self.c(a)
        c.d.ellipse([X - r, Y - r, X + r, Y + r], outline=col, width=max(1, int(3.2 * k)), fill=(0, 0, 0))
        for ang, L in ((c.t * self.speed, .72), (c.t * self.speed / 12, .45)):
            c.d.line([(X, Y), (X + math.sin(ang) * r * L, Y - math.cos(ang) * r * L)], fill=col,
                     width=max(1, int(3.2 * k)))


@dataclass
class Bars(El):
    heights: tuple = (60, 110, 170, 250)
    t0: float = 0
    bw: float = 60
    gap: float = 22

    def paint(self, c, X, Y, k, a):
        n = len(self.heights)
        tot = n * self.bw + (n - 1) * self.gap
        x = X - tot * k / 2
        for i, hh in enumerate(self.heights):
            p = clamp01((c.t - self.t0 - i * .18) / .4)
            if p > 0:
                h = hh * k * out_back(p, 1.2)
                c.d.rounded_rectangle([x, Y - h, x + self.bw * k, Y], radius=6 * k, outline=self.c(a),
                                      width=max(1, int(3 * k)), fill=tuple(int(v * a * .22) for v in self.color))
            x += (self.bw + self.gap) * k


@dataclass
class Bulb(El):
    r: float = 34

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        col = self.c(a)
        sw = max(1, int(3.4 * k))
        c.d.ellipse([X - r, Y - r, X + r, Y + r], outline=col, width=sw, fill=tuple(int(v * a * .25) for v in self.color))
        c.d.rectangle([X - r * .42, Y + r * .85, X + r * .42, Y + r * 1.35], outline=col, width=sw, fill=(0, 0, 0))
        c.d.line([(X - r * .42, Y + r * 1.1), (X + r * .42, Y + r * 1.1)], fill=col, width=max(1, int(2 * k)))


@dataclass
class Flag(El):
    h: float = 150

    def paint(self, c, X, Y, k, a):
        h = self.h * k
        col = self.c(a)
        sw = max(1, int(3.4 * k))
        c.d.line([(X, Y), (X, Y - h)], fill=col, width=sw)
        wave = math.sin(c.t * 5) * 6 * k
        c.d.polygon([(X, Y - h), (X + h * .55, Y - h * .82 + wave), (X, Y - h * .62)], fill=col)


@dataclass
class Gauge(El):
    """Barra horizontal de 0 a 100% com rótulo e porcentagem."""
    w: float = 460
    h: float = 34
    label: str = ""
    value: Callable = const(1)
    col_fn: Callable = None
    float_amp: float = 0

    def paint(self, c, X, Y, k, a):
        v = clamp01(self.value(c.t))
        w, h = self.w * k, self.h * k
        colr = self.col_fn(v) if self.col_fn else self.color
        col = tuple(int(q * a) for q in colr)
        x0 = X - w / 2
        c.d.rounded_rectangle([x0, Y - h / 2, x0 + w, Y + h / 2], radius=h / 2, outline=self.c(a * .7),
                              width=max(1, int(2.6 * k)), fill=(0, 0, 0))
        if v > 0.01:
            c.d.rounded_rectangle([x0 + 5 * k, Y - h / 2 + 5 * k, x0 + 5 * k + (w - 10 * k) * v, Y + h / 2 - 5 * k],
                                  radius=(h - 10 * k) / 2, fill=col)
        c.d.text((x0, Y - h / 2 - 22 * k), self.label, font=font("Black", 19 * k), fill=self.c(a), anchor="lm")
        c.d.text((x0 + w, Y - h / 2 - 22 * k), f"{int(round(v * 100))}%", font=font("Black", 26 * k), fill=col,
                 anchor="rm")


def green_to_red(v):
    return tuple(int(r + (g - r) * v) for r, g in zip(RED, GREEN))


def P(x, y, text, t, t_out=None, color=(255, 255, 255), size=PILL, dim_at=None, dim_to=.3):
    return S.add(Pill(x=const(x), y=const(y), text=text, size=size, color=color, s=appear(t),
                      a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


def T(x, y, text, t, t_out=None, size=60, color=(255, 255, 255), weight="Black", dim_at=None, dim_to=.3, dur=.35):
    return S.add(Text(x=const(x), y=const(y), text=text, size=size, weight=weight, color=color,
                      s=appear(t, dur), a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


# ---------------------------------------------------------------- câmera
XA, XB, XC, XD, XE, XF, XG, XH, XI, XJ = 0, 1500, 3000, 4500, 6000, 7500, 9000, 10500, 12000, 13500
S.cam_x = Track(XA, (cut(5.75), XA, lin), (cut(5.75) + .001, XB, lin),
                (cut(12.85), XB, lin), (cut(12.85) + .001, XC, lin),
                (17.3, XC, lin), (17.65, XD, in_out_cubic),
                (cut(25.55), XD, lin), (cut(25.55) + .001, XE, lin),
                (33.6, XE, lin), (33.95, XF, in_out_cubic),
                (cut(38.85), XF, lin), (cut(38.85) + .001, XG, lin),
                (52.7, XG, lin), (53.05, XH, in_out_cubic),
                (cut(59.55), XH, lin), (cut(59.55) + .001, XI, lin),
                (66.3, XI, lin), (66.65, XJ, in_out_cubic))
S.cam_y = const(0)
S.zoom = Track(1, (cut(59.55), 1, lin), (cut(59.55) + .001, 1, lin), (66.3, 1.06, lin), (66.31, 1, lin))
S.ground_a = const(0)
S.invert = Track(0, (cut(5.75), 0, lin), (cut(5.75) + .1, 1, out_cubic), (12.75, 1, lin), (12.85, 0, in_cubic))
S.sfx += [(17.25, "whoosh"), (33.55, "whoosh"), (52.65, "whoosh"), (66.25, "whoosh")] + \
         [(t, "thud") for t in (5.75, 12.85, 25.55, 38.85, 59.55)]

# ---------------------------------------------------------------- A: gancho (0.1–5.6)
# "Por que contar seus planos antes de acontecerem... reduz suas chances de realizá-los?"
T(XA, -470, "SEUS PLANOS", .05, 5.7, size=76)
S.add(Dashed(x=const(XA), y=const(GY), a=life(0, 5.7)))
S.add(Person(x=const(XA - 190), y=const(GY), h=150, s=appear(.1, .25), a=life(.1, 5.7)), .1)
P(XA - 150, 50, "MEU PLANO É…", .6, 5.7, size=22)
for i, (dx, t0) in enumerate([(90, 1.0), (190, 1.2), (290, 1.4)]):
    S.add(Person(x=const(XA + dx), y=const(GY), h=110, color=GREY, s=appear(t0), a=life(t0, 5.7), phase=i), t0)
chance = Track(0, (.9, 0, lin), (1.7, 1, out_cubic), (3.3, 1, lin), (4.8, .18, in_out_cubic))
S.add(Gauge(x=const(XA), y=const(-250), w=520, label="SUAS CHANCES", value=chance, col_fn=green_to_red,
            s=appear(.8, .3, s0=.8), a=life(.8, 5.7)), .8)
S.sfx += [(3.4 + i * .12, "tick") for i in range(10)]
S.add(WarnIcon(x=const(XA), y=const(-360), r=28, color=RED, s=appear(4.7), a=life(4.7, 5.7)), 4.7, "thud")

# ---------------------------------------------------------------- B: a lei (inversão) (5.9–12.75)
# "A resposta está na Lei 3 do livro As 48 Leis do Poder: oculte suas intenções."
P(XB, -500, "A RESPOSTA", 6.0, 12.75, size=21)
T(XB, -150, "LEI 3", 7.2, 12.75, size=210, dur=.45)
S.add(BookIcon(x=const(XB), y=const(-400), w=120, s=appear(8.3), a=life(8.3, 12.75)), 8.3)
P(XB, 20, "AS 48 LEIS DO PODER", 8.6, 12.75, size=21)
T(XB, 170, "OCULTE SUAS", 10.6, 12.75, size=66)
T(XB, 260, "INTENÇÕES", 10.9, 12.75, size=82)
S.sfx += [(7.2, "thud"), (10.6, "thud")]

# ---------------------------------------------------------------- C: 1 (13.0–17.3)
# "Primeiro: quem sabe o seu próximo passo consegue te bloquear."
T(XC, -470, "1", 13.0, 17.3, size=120, color=GOLD)
S.add(Dashed(x=const(XC), y=const(GY), a=life(13.0, 17.3)))
S.add(Person(x=const(XC - 240), y=const(GY), h=150, s=appear(13.1), a=life(13.1, 17.3)), 13.1)
S.add(Flag(x=const(XC + 250), y=const(GY), h=170, color=GOLD, s=appear(13.3), a=life(13.3, 17.3)), 13.3)
S.add(Path(x=const(XC - 180), y=const(120), pts=[(0, 0), (370, 0)], arrow=True, width=3.4, color=GOLD,
           prog=Track(0, (14.1, 0, lin), (14.9, 1, in_out_cubic)), a=life(14.1, 17.3, dim_at=16.2, dim_to=.25)), 14.1)
P(XC, -300, "PRÓXIMO PASSO", 14.3, 17.3, color=GOLD, size=22)
S.add(Person(x=const(XC + 20), y=Track(-800, (15.9, -800, lin), (16.25, GY, out_back)), h=160, color=RED,
             a=life(15.9, 17.3), float_amp=0), 16.25, "thud")
S.add(XIcon(x=const(XC + 20), y=const(-110), r=28, color=RED, s=appear(16.5), a=life(16.5, 17.3)), 16.5)
P(XC + 20, -200, "BLOQUEIO", 16.6, 17.3, color=RED)

# ---------------------------------------------------------------- D: 2 (17.6–25.4)
# "Segundo: quando você anuncia o que quer, os outros têm tempo de se preparar. E nem todo mundo torce por você."
T(XD, -470, "2", 17.6, 25.5, size=120, color=GOLD)
S.add(Dashed(x=const(XD), y=const(GY), a=life(17.5, 25.5)))
S.add(Person(x=const(XD), y=const(GY), h=150, s=appear(17.7), a=life(17.7, 25.5)), 17.7)
P(XD, 50, "EU VOU…", 18.6, 25.5, size=24)
others = [(-250, 20.5), (250, 20.7), (-130, 20.9), (130, 21.05)]
for i, (dx, t0) in enumerate(others):
    S.add(Person(x=const(XD + dx), y=const(GY), h=115, color=GREY, s=appear(t0),
                 a=life(t0, 25.5, dim_at=23.1 if i in (0, 3) else None, dim_to=0), phase=i), t0)
for i in (0, 3):
    dx = others[i][0]
    S.add(Person(x=const(XD + dx), y=const(GY), h=115, color=RED, a=life(23.1, 25.5), phase=i))
S.add(Clock(x=const(XD), y=const(-250), r=50, speed=14, color=GOLD, s=appear(21.0),
            a=life(21.0, 25.5, dim_at=23.1, dim_to=.25)), 21.0)
P(XD, -150, "TEMPO PRA SE PREPARAR", 21.3, 25.5, color=GOLD, dim_at=23.1, dim_to=.25)
P(XD, 400, "NEM TODO MUNDO TORCE POR VOCÊ", 23.2, 25.5, color=RED, size=21)
S.sfx += [(23.15, "thud")]

# ---------------------------------------------------------------- E: 3 (25.7–33.6)
# "Terceiro: tem estudo mostrando que, quando você anuncia uma meta, já sente que avançou... e se esforça menos."
T(XE, -470, "3", 25.7, 33.6, size=120, color=GOLD)
P(XE, -360, "ESTUDO", 26.9, 33.6, size=22)
S.add(Dashed(x=const(XE), y=const(GY + 60), a=life(25.7, 33.6)))
S.add(Person(x=const(XE), y=const(GY + 60), h=150, s=appear(25.8), a=life(25.8, 33.6)), 25.8)
P(XE, 110, "MINHA META É…", 28.4, 33.6, size=22)
S.add(Gauge(x=const(XE), y=const(-220), w=520, label="SENSAÇÃO DE AVANÇO",
            value=Track(.1, (30.4, .1, lin), (31.4, .8, out_cubic)), color=GOLD,
            s=appear(29.8, .3, s0=.8), a=life(29.8, 33.6)), 29.8)
S.add(Gauge(x=const(XE), y=const(-90), w=520, label="ESFORÇO",
            value=Track(.8, (32.2, .8, lin), (33.2, .3, in_out_cubic)), col_fn=green_to_red,
            s=appear(30.0, .3, s0=.8), a=life(30.0, 33.6)), 30.0)
S.sfx += [(32.2 + i * .1, "tick") for i in range(9)]

# ---------------------------------------------------------------- F: estratégico (33.9–38.7)
# "Por isso, quem é estratégico fala pouco... e mostra resultado."
S.add(Dashed(x=const(XF), y=const(GY), a=life(33.8, 38.85)))
S.add(Person(x=const(XF - 210), y=const(GY), h=150, s=appear(33.9), a=life(33.9, 38.85)), 33.9)
P(XF - 210, 50, "ESTRATÉGICO", 34.8, 38.85, color=GOLD)
T(XF, -400, "FALA POUCO", 36.35, 38.85, size=62, dim_at=37.25, dim_to=.35)
T(XF, -300, "MOSTRA RESULTADO", 37.25, 38.85, size=52, color=GREEN)
S.add(Bars(x=const(XF + 130), y=const(GY), t0=37.3, color=GREEN, a=life(37.3, 38.85)))
S.sfx += [(37.3 + i * .18, "pop") for i in range(4)]

# ---------------------------------------------------------------- G: entrevista (39.0–52.7)
GO = 52.85
P(XG, -480, "NA PRÁTICA", 39.05, GO, size=22)
T(XG, -405, "ENTREVISTA", 40.3, GO, size=58)
S.add(Dashed(x=const(XG), y=const(GY), a=life(39.0, GO)))
cand_a = Track(0, (39.1, 0, lin), (39.3, 1, out_cubic), (50.7, 1, lin), (51.2, .3, out_cubic), (GO, .3, lin),
               (GO + .15, 0, lin))
S.add(Person(x=const(XG - 220), y=const(GY), h=150, s=appear(39.1), a=cand_a), 39.1)
S.add(Person(x=const(XG + 220), y=const(GY), h=150, color=(200, 200, 200), s=appear(39.3), a=life(39.3, GO),
             phase=1), 39.3)
S.add(Path(x=const(XG - 110), y=const(GY - 70), pts=[(0, 0), (220, 0)], width=3.4, color=GREY,
           prog=Track(0, (39.4, 0, lin), (39.7, 1, out_cubic)), a=life(39.4, GO)))
S.add(Text(x=const(XG - 220), y=const(GY + 45), text="VOCÊ", size=20, weight="Black", s=appear(39.5),
           a=life(39.5, GO)))
S.add(Text(x=const(XG + 220), y=const(GY + 45), text="RECRUTADOR", size=20, weight="Black", color=(200, 200, 200),
           s=appear(39.6), a=life(39.6, GO)))
P(XG + 120, 30, "PRETENSÃO SALARIAL?", 41.9, 45.8, dim_at=43.9)
T(XG - 150, -150, "R$ ???", 43.9, 45.8, size=48, color=GOLD)
S.add(XIcon(x=const(XG - 150), y=const(-235), r=30, color=RED, s=appear(44.7, .3), a=life(44.7, 45.8)), 44.7, "thud")
P(XG - 150, 30, "QUAL A FAIXA?", 45.95, GO, color=GREEN, size=21, dim_at=48.4)
S.add(CheckIcon(x=const(XG + 15), y=const(30), r=20, color=GREEN, s=appear(46.5), a=life(46.5, GO, dim_at=48.4)), 46.5)
T(XG + 140, -170, "R$ 6–8 MIL", 46.9, GO, size=46, color=GOLD)
P(XG + 140, -110, "FAIXA DA VAGA", 47.1, GO, color=GOLD, size=16)
T(XG - 185, -170, "R$ 5 MIL", 48.5, GO, size=44, color=RED)
S.add(WarnIcon(x=const(XG - 185), y=const(-250), r=24, color=RED, s=appear(48.7), a=life(48.7, GO)), 48.7)
S.add(Path(x=const(XG + 30), y=const(-170), pts=[(0, 0), (-120, 0)], arrow=True, width=3, color=RED,
           prog=Track(0, (49.2, 0, lin), (49.6, 1, out_cubic)), a=life(49.2, GO)), 49.2)
P(XG, 380, "NEGOCIA CONTRA SI MESMO", 50.75, GO, color=RED, size=22)

# ---------------------------------------------------------------- H: promoção (53.0–59.3)
# "No trabalho, vale o mesmo. Vai pedir uma promoção? Primeiro entrega. Depois conversa."
HO = 59.55
T(XH, -470, "NO TRABALHO", 53.05, HO, size=66)
S.add(Dashed(x=const(XH), y=const(GY), a=life(53.0, HO)))
S.add(Person(x=const(XH - 200), y=const(GY), h=150, s=appear(53.1), a=life(53.1, HO)), 53.1)
P(XH - 200, 50, "PROMOÇÃO?", 54.9, HO, color=GOLD, size=22)
S.add(Box(x=const(XH + 120), y=const(-260), w=290, h=96, label="1. ENTREGA", size=28, color=GREEN,
          s=appear(56.5), a=life(56.5, HO)), 56.5, "thud")
S.add(CheckIcon(x=const(XH + 265), y=const(-308), r=22, color=GREEN, s=appear(56.9), a=life(56.9, HO)), 56.9)
S.add(Path(x=const(XH + 120), y=const(-205), pts=[(0, 0), (0, 80)], arrow=True, width=3.2,
           prog=Track(0, (57.5, 0, lin), (57.85, 1, out_cubic)), a=life(57.5, HO)), 57.5)
S.add(Box(x=const(XH + 120), y=const(-60), w=290, h=96, label="2. CONVERSA", size=28,
          s=appear(57.9), a=life(57.9, HO)), 57.9, "thud")

# ---------------------------------------------------------------- I: impacto (59.8–66.3)
# "Não esconde quem você é. Esconde o seu próximo passo." / "E deixa o resultado fazer barulho."
T(XI, -270, "NÃO ESCONDE", 59.85, 63.9, size=62, dim_at=61.8, dim_to=.3)
T(XI, -190, "QUEM VOCÊ É.", 60.3, 63.9, size=62, dim_at=61.8, dim_to=.3)
T(XI, -40, "ESCONDE O SEU", 61.8, 63.9, size=62, color=GOLD, dur=.4)
T(XI, 50, "PRÓXIMO PASSO.", 62.2, 63.9, size=68, color=GOLD, dur=.4)
S.sfx += [(61.8, "thud")]
T(XI, -80, "DEIXA O RESULTADO", 64.05, 66.3, size=58)
T(XI, 30, "FAZER BARULHO.", 65.0, 66.3, size=76, color=GOLD, dur=.3)
S.add(Rays(x=const(XI), y=const(-30), r=270, n=9, prog=Track(0, (65.0, 0, lin), (65.3, 1, out_back)),
           color=GOLD, a=life(65.0, 66.3), float_amp=0))
S.sfx += [(65.0, "thud")]

# ---------------------------------------------------------------- J: final (66.6–71.5)
P(XJ, -390, "SIGA A PÁGINA", 67.5, 71.2, size=22)
S.add(Avatar(x=const(XJ), y=const(-150), r=150, path=os.path.join(HERE, "assets", "guidelight.jpg"), ring=GOLD,
             s=appear(66.7, .45), a=life(66.7, 71.2)), 66.7, "thud")
T(XJ, 80, "GUIDELIGHT", 67.1, 71.2, size=78)
CLICK = 69.4
S.add(Button(x=const(XJ), y=const(210), w=300, h=78, text=lambda t: "SEGUINDO" if t >= CLICK else "SEGUIR",
             fill=lerp_color((255, 255, 255), GOLD, CLICK, CLICK + .15),
             s=Track(0, (67.9, 0, lin), (68.25, 1, out_back), (CLICK - .05, 1, lin), (CLICK + .05, .9, lin),
                     (CLICK + .35, 1, out_back)), a=life(67.9, 71.2)), 67.9)
S.add(Cursor(x=Track(XJ + 300, (68.5, XJ + 300, lin), (69.25, XJ + 30, in_out_cubic)),
             y=Track(560, (68.5, 560, lin), (69.25, 215, in_out_cubic)), size=44,
             s=Track(1, (CLICK - .05, 1, lin), (CLICK + .05, .85, lin), (CLICK + .25, 1, out_cubic)),
             a=life(68.5, 70.9)), CLICK)
S.sfx.append((CLICK + .02, "tick"))
S.add(Rays(x=const(XJ), y=const(-150), r=190, n=7, prog=Track(0, (CLICK, 0, lin), (CLICK + .3, 1, out_back)),
           color=GOLD, a=life(CLICK, 71.2), float_amp=0))


def mix(root):
    mix_voice(f"{root}/video_04.mp4", [(os.path.join(HERE, "assets", "voz04", f), t) for f, t in VOZ],
              f"{root}/guidelight_lei3_oculte_intencoes_9x16.mp4", voice_vol=1.8)


if __name__ == "__main__":
    root = os.path.join(HERE, "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills04", exist_ok=True)
        for f in os.listdir(f"{root}/stills04"):
            os.remove(f"{root}/stills04/{f}")
        for t in [4.9, 11.8, 16.9, 24.5, 33.0, 38.3, 47.5, 52.0, 58.8, 63.5, 65.9, 70.0]:
            S.still(t, f"{root}/stills04/t{t:05.1f}.png")
        print("stills ok")
    elif "--mix" in sys.argv:
        mix(root)
    else:
        S.render(f"{root}/video_04.mp4")
        mix(root)
