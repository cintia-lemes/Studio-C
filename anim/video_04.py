"""
Vídeo 04: Lei 3, "Oculte suas intenções" (As 48 Leis do Poder)  (9:16, 1080×1920, ≈48 s)
Página: Guidelight. Roteiro: docs/roteiros/video_04_lei3_oculte_intencoes.md
Narração: ElevenLabs, voz "Letícia" (CcElPA8NBrawbunFs7rh), eleven_v4, em anim/assets/voz04/

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

S = Scene(W=1080, H=1920, fps=30, duration=48.0, base_w=720)
PILL = 19
GY = 250  # chão das cenas com bonecos

VOZ = [("s01.mp3", 0.1), ("s02.mp3", 4.4), ("s03.mp3", 11.2), ("s04.mp3", 14.9), ("s05.mp3", 19.4),
       ("s06.mp3", 24.4), ("s07.mp3", 29.2), ("s08.mp3", 34.0), ("s09.mp3", 38.8), ("s10.mp3", 43.8)]


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


def P(x, y, text, t, t_out=None, color=(255, 255, 255), size=PILL, dim_at=None, dim_to=.3):
    return S.add(Pill(x=const(x), y=const(y), text=text, size=size, color=color, s=appear(t),
                      a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


def T(x, y, text, t, t_out=None, size=60, color=(255, 255, 255), weight="Black", dim_at=None, dim_to=.3, dur=.35):
    return S.add(Text(x=const(x), y=const(y), text=text, size=size, weight=weight, color=color,
                      s=appear(t, dur), a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


# ---------------------------------------------------------------- câmera
XA, XB, XC, XD, XE, XF, XG, XH = 0, 1500, 3000, 4500, 6000, 7500, 9000, 11000
S.cam_x = Track(XA, (cut(4.3), XA, lin), (cut(4.3) + .001, XB, lin),
                (cut(11.05), XB, lin), (cut(11.05) + .001, XC, lin),
                (14.6, XC, lin), (14.95, XD, in_out_cubic),
                (cut(19.25), XD, lin), (cut(19.25) + .001, XE, lin),
                (24.05, XE, lin), (24.4, XF, in_out_cubic),
                (cut(38.6), XF, lin), (cut(38.6) + .001, XG, lin),
                (43.3, XG, lin), (43.65, XH, in_out_cubic))
S.cam_y = const(0)
S.zoom = Track(1, (cut(38.6), 1, lin), (cut(38.6) + .001, 1, lin), (43.3, 1.05, lin), (43.31, 1, lin))
S.ground_a = const(0)
S.invert = Track(0, (cut(4.3), 0, lin), (cut(4.3) + .1, 1, out_cubic), (10.95, 1, lin), (11.05, 0, in_cubic))
S.sfx += [(14.55, "whoosh"), (24.0, "whoosh"), (43.25, "whoosh"), (4.3, "thud"), (11.05, "thud"),
          (19.25, "thud"), (38.6, "thud")]

# ---------------------------------------------------------------- A: gancho (0–4.3)
# "Você contou sua ideia... e outro levou o crédito."
T(XA, -440, "SUA IDEIA", .05, 4.25, size=80)
S.add(Dashed(x=const(XA), y=const(GY), a=life(0, 4.25)))
S.add(Person(x=const(XA - 170), y=const(GY), h=150, s=appear(.05, .25),
             a=Track(0, (.05, 0, lin), (.2, 1, lin), (2.9, 1, lin), (3.3, .25, out_cubic), (4.1, .25, lin),
                     (4.25, 0, lin))), .05)
S.add(Person(x=const(XA + 170), y=const(GY), h=150, s=appear(.25, .25), a=life(.25, 4.25), phase=1), .25)
bx = Track(XA - 170, (2.3, XA - 170, lin), (2.95, XA + 170, in_out_cubic))
by = Track(-10, (2.3, -10, lin), (2.6, -140, out_cubic), (2.95, -10, in_cubic))
S.add(Bulb(x=bx, y=by, r=36, color=GOLD, s=appear(.35, .35), a=life(.35, 4.25)), .35)
S.add(Rays(x=bx, y=by, r=56, prog=Track(0, (.5, 0, lin), (.8, 1, out_back)), color=GOLD, a=life(.5, 4.25),
           float_amp=0))
S.sfx.append((2.3, "whoosh"))
P(XA + 170, -140 - 50, "CRÉDITO", 3.05, 4.25, color=GOLD)
S.add(XIcon(x=const(XA - 170), y=const(-60), r=26, color=RED, s=appear(3.3), a=life(3.3, 4.25)), 3.3, "thud")

# ---------------------------------------------------------------- B: a lei (inversão) (4.4–11.0)
# "A Lei 3 do livro As 48 Leis do Poder é clara: oculte suas intenções."
T(XB, -120, "LEI 3", 4.55, 10.95, size=210, dur=.45)
S.add(BookIcon(x=const(XB), y=const(-420), w=130, s=appear(5.4), a=life(5.4, 10.95)), 5.4)
P(XB, -320, "AS 48 LEIS DO PODER", 5.6, 10.95, size=21)
T(XB, 150, "OCULTE SUAS", 8.85, 10.95, size=66)
T(XB, 240, "INTENÇÕES", 9.15, 10.95, size=82)
S.sfx += [(8.85, "thud")]

# ---------------------------------------------------------------- C: lógica 1 (11.2–14.6)
# "Quem sabe o seu próximo passo consegue te bloquear."
S.add(Dashed(x=const(XC), y=const(GY), a=life(11.1, 14.6)))
S.add(Person(x=const(XC - 240), y=const(GY), h=150, s=appear(11.15), a=life(11.15, 14.6)), 11.15)
S.add(Flag(x=const(XC + 250), y=const(GY), h=170, color=GOLD, s=appear(11.3), a=life(11.3, 14.6)), 11.3)
S.add(Path(x=const(XC - 180), y=const(120), pts=[(0, 0), (370, 0)], arrow=True, width=3.4, color=GOLD,
           prog=Track(0, (11.5, 0, lin), (12.2, 1, in_out_cubic)), a=life(11.5, 14.6, dim_at=12.9, dim_to=.25)), 11.5)
P(XC, -330, "PRÓXIMO PASSO", 11.6, 14.6, color=GOLD, size=22)
S.add(Person(x=const(XC + 20), y=Track(-800, (12.6, -800, lin), (12.95, GY, out_back)), h=160, color=RED,
             a=life(12.6, 14.6), float_amp=0), 12.95, "thud")
S.add(XIcon(x=const(XC + 20), y=const(-110), r=28, color=RED, s=appear(13.2), a=life(13.2, 14.6)), 13.2)
P(XC + 20, -200, "BLOQUEIO", 13.3, 14.6, color=RED)

# ---------------------------------------------------------------- D: lógica 2 (14.9–19.1)
# "Quando você anuncia o que quer, os outros têm tempo de se preparar."
S.add(Dashed(x=const(XD), y=const(GY), a=life(14.9, 19.2)))
S.add(Person(x=const(XD), y=const(GY), h=150, s=appear(15.0), a=life(15.0, 19.2)), 15.0)
P(XD, 50, "EU VOU…", 15.3, 19.2, size=24)
for i, (dx, t0) in enumerate([(-240, 16.85), (240, 17.05), (-120, 17.25), (120, 17.4)]):
    S.add(Person(x=const(XD + dx), y=const(GY), h=115, color=GREY, s=appear(t0), a=life(t0, 19.2), phase=i), t0)
S.add(Clock(x=const(XD), y=const(-260), r=50, speed=14, color=RED, s=appear(17.6), a=life(17.6, 19.2)), 17.6)
P(XD, -150, "TEMPO PRA SE PREPARAR", 17.9, 19.2, color=RED)

# ---------------------------------------------------------------- E: lógica 3 (19.4–24.0)
# "Por isso, quem é estratégico fala pouco e mostra resultado."
S.add(Dashed(x=const(XE), y=const(GY), a=life(19.3, 24.0)))
S.add(Person(x=const(XE - 210), y=const(GY), h=150, s=appear(19.35), a=life(19.35, 24.0)), 19.35)
P(XE - 210, 50, "ESTRATÉGICO", 20.3, 24.0, color=GOLD)
T(XE, -400, "FALA POUCO", 21.7, 24.0, size=62, dim_at=22.6, dim_to=.35)
T(XE, -300, "MOSTRA RESULTADO", 22.6, 24.0, size=52, color=GREEN)
S.add(Bars(x=const(XE + 130), y=const(GY), t0=22.7, color=GREEN, a=life(22.7, 24.0)))
S.sfx += [(22.7 + i * .18, "pop") for i in range(4)]

# ---------------------------------------------------------------- F: exemplo (24.4–38.2)
# "Exemplo: na entrevista, perguntam sua pretensão salarial."
# "Não fale um número primeiro. Pergunte qual é a faixa da vaga."
# "Quem revela o próprio limite... negocia contra si mesmo."
FO = 38.55
P(XF, -460, "EXEMPLO", 24.45, FO, size=22)
T(XF, -390, "ENTREVISTA", 25.5, FO, size=58)
S.add(Dashed(x=const(XF), y=const(GY), a=life(24.4, FO)))
cand_a = Track(0, (24.5, 0, lin), (24.7, 1, out_cubic), (36.4, 1, lin), (36.9, .3, out_cubic), (FO, .3, lin),
               (FO + .15, 0, lin))
S.add(Person(x=const(XF - 220), y=const(GY), h=150, s=appear(24.5), a=cand_a), 24.5)
S.add(Person(x=const(XF + 220), y=const(GY), h=150, color=(200, 200, 200), s=appear(24.7), a=life(24.7, FO),
             phase=1), 24.7)
S.add(Path(x=const(XF - 110), y=const(GY - 70), pts=[(0, 0), (220, 0)], width=3.4, color=GREY,
           prog=Track(0, (24.8, 0, lin), (25.1, 1, out_cubic)), a=life(24.8, FO)))
S.add(Text(x=const(XF - 220), y=const(GY + 45), text="VOCÊ", size=20, weight="Black", s=appear(25.0),
           a=life(25.0, FO)))
S.add(Text(x=const(XF + 220), y=const(GY + 45), text="RECRUTADOR", size=20, weight="Black", color=(200, 200, 200),
           s=appear(25.1), a=life(25.1, FO)))
P(XF + 120, 30, "PRETENSÃO SALARIAL?", 26.3, 31.1, dim_at=29.3)
# não fale um número primeiro
T(XF - 150, -150, "R$ ???", 29.4, 31.2, size=48, color=GOLD)
S.add(XIcon(x=const(XF - 150), y=const(-235), r=30, color=RED, s=appear(30.1, .3), a=life(30.1, 31.2)), 30.1, "thud")
# pergunte a faixa
P(XF - 150, 30, "QUAL A FAIXA?", 31.3, FO, color=GREEN, size=21, dim_at=34.0)
S.add(CheckIcon(x=const(XF + 15), y=const(30), r=20, color=GREEN, s=appear(31.9), a=life(31.9, FO, dim_at=34.0)), 31.9)
T(XF + 140, -170, "R$ 6–8 MIL", 32.4, FO, size=46, color=GOLD)
P(XF + 140, -110, "FAIXA DA VAGA", 32.6, FO, color=GOLD, size=16)
# revelar o limite
T(XF - 185, -170, "R$ 5 MIL", 34.6, FO, size=44, color=RED)
S.add(WarnIcon(x=const(XF - 185), y=const(-250), r=24, color=RED, s=appear(34.8), a=life(34.8, FO)), 34.8)
S.add(Path(x=const(XF + 30), y=const(-170), pts=[(0, 0), (-120, 0)], arrow=True, width=3, color=RED,
           prog=Track(0, (35.2, 0, lin), (35.6, 1, out_cubic)), a=life(35.2, FO)), 35.2)
P(XF, 380, "NEGOCIA CONTRA SI MESMO", 36.4, FO, color=RED, size=22)

# ---------------------------------------------------------------- G: impacto (38.8–43.3)
# "Não esconde quem você é. Esconde o seu próximo passo."
T(XG, -170, "NÃO ESCONDE", 38.85, 43.3, size=64, dim_at=40.95, dim_to=.3)
T(XG, -85, "QUEM VOCÊ É.", 39.25, 43.3, size=64, dim_at=40.95, dim_to=.3)
T(XG, 95, "ESCONDE O SEU", 41.0, 43.3, size=62, color=GOLD, dur=.4)
T(XG, 180, "PRÓXIMO PASSO.", 41.35, 43.3, size=68, color=GOLD, dur=.4)
S.sfx += [(41.0, "thud")]

# ---------------------------------------------------------------- H: final (43.6–48)
P(XH, -390, "SIGA A PÁGINA", 44.4, 47.6, size=22)
S.add(Avatar(x=const(XH), y=const(-150), r=150, path=os.path.join(HERE, "assets", "guidelight.jpg"), ring=GOLD,
             s=appear(43.6, .45), a=life(43.6, 47.6)), 43.6, "thud")
T(XH, 80, "GUIDELIGHT", 44.0, 47.6, size=78)
CLICK = 46.2
S.add(Button(x=const(XH), y=const(210), w=300, h=78, text=lambda t: "SEGUINDO" if t >= CLICK else "SEGUIR",
             fill=lerp_color((255, 255, 255), GOLD, CLICK, CLICK + .15),
             s=Track(0, (44.8, 0, lin), (45.15, 1, out_back), (CLICK - .05, 1, lin), (CLICK + .05, .9, lin),
                     (CLICK + .35, 1, out_back)), a=life(44.8, 47.6)), 44.8)
S.add(Cursor(x=Track(XH + 300, (45.3, XH + 300, lin), (46.05, XH + 30, in_out_cubic)),
             y=Track(560, (45.3, 560, lin), (46.05, 215, in_out_cubic)), size=44,
             s=Track(1, (CLICK - .05, 1, lin), (CLICK + .05, .85, lin), (CLICK + .25, 1, out_cubic)),
             a=life(45.3, 47.3)), CLICK)
S.sfx.append((CLICK + .02, "tick"))
S.add(Rays(x=const(XH), y=const(-150), r=190, n=7, prog=Track(0, (CLICK, 0, lin), (CLICK + .3, 1, out_back)),
           color=GOLD, a=life(CLICK, 47.6), float_amp=0))


def mix(root):
    mix_voice(f"{root}/video_04.mp4", [(os.path.join(HERE, "assets", "voz04", f), t) for f, t in VOZ],
              f"{root}/guidelight_lei3_oculte_intencoes_9x16.mp4")


if __name__ == "__main__":
    root = os.path.join(HERE, "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills04", exist_ok=True)
        for t in [1.5, 3.8, 9.8, 13.9, 18.6, 23.6, 27.5, 30.6, 33.3, 37.5, 42.6, 46.6]:
            S.still(t, f"{root}/stills04/t{t:05.1f}.png")
        print("stills ok")
    elif "--mix" in sys.argv:
        mix(root)
    else:
        S.render(f"{root}/video_04.mp4")
        mix(root)
