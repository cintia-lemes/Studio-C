"""
Vídeo 07: versão 2 do macete do algoritmo, "Você não é robô. É impaciente."  (9:16, 1080×1920, ≈61 s)
Três blocos: o impulso do atalho; interação mecânica × valor real; engajamento como moeda social.
Página: Guidelight. Roteiro: docs/roteiros/video_07_macete_v2.md
Narração: ElevenLabs, voz "Elvis – Social Media & Shorts" (zNEsdgTUa3ndwKry8Xcq), eleven_v4, em anim/assets/voz07/

Rodar:  python3 anim/video_07.py --stills | --mix | (sem nada: render + mix)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from engine import *  # noqa
import video_06 as v6  # reaproveita Action, Phone, Captcha, Gauge (só as classes)

Action, Phone, Captcha, Gauge = v6.Action, v6.Phone, v6.Captcha, v6.Gauge

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = (255, 196, 56)
RED = (255, 82, 82)
GREEN = (64, 222, 140)
ORANGE = (255, 140, 60)
GREY = (150, 150, 150)

S = Scene(W=1080, H=1920, fps=30, duration=61.0, base_w=720)
PILL = 19

VOZ = [("s01.mp3", 0.05), ("s02.mp3", 3.1), ("s03.mp3", 11.3), ("s04.mp3", 16.9), ("s05.mp3", 21.6),
       ("s06.mp3", 28.1), ("s07.mp3", 33.4), ("s08.mp3", 39.0), ("s09.mp3", 44.7), ("s10.mp3", 51.1),
       ("s11.mp3", 56.5)]


def clamp01(x):
    return max(0.0, min(1.0, x))


def cut(t):
    return t + 0.015


@dataclass
class Padlock(El):
    s_: float = 110
    open_t: float = 999

    def paint(self, c, X, Y, k, a):
        s = self.s_ * k
        col = self.c(a)
        sw = max(1, int(4 * k))
        lift = s * .18 * clamp01((c.t - self.open_t) / .3)
        c.d.arc([X - s * .3, Y - s * .75 - lift, X + s * .3, Y - s * .05 - lift], 180, 360, fill=col, width=sw)
        c.d.line([(X - s * .3, Y - s * .4 - lift), (X - s * .3, Y - s * .15)], fill=col, width=sw)
        c.d.line([(X + s * .3, Y - s * .4 - lift), (X + s * .3, Y - s * .15)], fill=col, width=sw)
        c.d.rounded_rectangle([X - s * .45, Y - s * .15, X + s * .45, Y + s * .5], radius=10 * k, outline=col, width=sw,
                              fill=(0, 0, 0))
        c.d.text((X, Y + s * .17), "?", font=font("Black", s * .45), fill=col, anchor="mm")


@dataclass
class PauseIcon(El):
    r: float = 34

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        col = self.c(a)
        sw = max(1, int(3.2 * k))
        c.d.ellipse([X - r, Y - r, X + r, Y + r], outline=col, width=sw, fill=(0, 0, 0))
        for dx in (-.28, .28):
            c.d.rounded_rectangle([X + dx * r - r * .1, Y - r * .4, X + dx * r + r * .1, Y + r * .4], radius=2 * k, fill=col)


def P(x, y, text, t, t_out=None, color=(255, 255, 255), size=PILL, dim_at=None, dim_to=.3):
    return S.add(Pill(x=const(x), y=const(y), text=text, size=size, color=color, s=appear(t),
                      a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


def T(x, y, text, t, t_out=None, size=60, color=(255, 255, 255), weight="Black", dim_at=None, dim_to=.3, dur=.35):
    return S.add(Text(x=const(x), y=const(y), text=text, size=size, weight=weight, color=color,
                      s=appear(t, dur), a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


# ---------------------------------------------------------------- câmera
XA, XB, XC, XD, XE, XF, XG, XH, XI, XJ, XK = [i * 1500 for i in range(11)]
S.cam_x = Track(XA, (cut(2.95), XA, lin), (cut(2.95) + .001, XB, lin),
                (cut(11.15), XB, lin), (cut(11.15) + .001, XC, lin),
                (16.6, XC, lin), (16.95, XD, in_out_cubic),
                (cut(21.45), XD, lin), (cut(21.45) + .001, XE, lin),
                (27.8, XE, lin), (28.15, XF, in_out_cubic),
                (cut(33.25), XF, lin), (cut(33.25) + .001, XG, lin),
                (38.7, XG, lin), (39.05, XH, in_out_cubic),
                (cut(44.55), XH, lin), (cut(44.55) + .001, XI, lin),
                (cut(50.95), XI, lin), (cut(50.95) + .001, XJ, lin),
                (56.2, XJ, lin), (56.55, XK, in_out_cubic))
S.cam_y = const(0)
S.ground_a = const(0)
S.invert = Track(0, (cut(50.95), 0, lin), (cut(50.95) + .1, 1, out_cubic), (56.1, 1, lin), (56.2, 0, in_cubic))
S.sfx += [(t, "whoosh") for t in (16.55, 27.75, 38.65, 56.15)] + \
         [(t, "thud") for t in (2.95, 11.15, 21.45, 33.25, 44.55, 50.95)]

# ---------------------------------------------------------------- A: gancho (0.05–2.85)
AO = 2.95
S.add(Captcha(x=const(XA), y=const(-300), check_t=.35, s=appear(.05, .25), a=life(.05, AO, dim_at=1.84, dim_to=.3)), .05)
S.sfx.append((.35, "tick"))
T(XA, -80, "VOCÊ NÃO É ROBÔ.", .1, AO, size=60, dim_at=1.84, dim_to=.35)
T(XA, 60, "É IMPACIENTE.", 1.84, AO, size=84, color=RED, dur=.25)


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


S.add(Clock(x=const(XA), y=const(280), r=70, speed=40, color=RED, s=appear(1.9, .3), a=life(1.9, AO)), 1.9, "thud")

# ---------------------------------------------------------------- B: clique frenético (3.1–11.0)
BO = 11.15
S.add(Phone(x=const(XB), y=const(-40), s=appear(3.0, .3, s0=.8), a=life(3.0, BO, dim_at=8.4, dim_to=.35)))
KINDS = ["heart", "bubble", "bookmark", "plus", "share"]
WORDS = ["CURTE", "COMENTA", "SALVA", "SEGUE", "REPUBLICA"]
T_ON = [3.15, 3.8, 4.45, 5.1, 5.8]
IY = [-230 + i * 95 for i in range(5)]
for i, kind in enumerate(KINDS):
    S.add(Action(x=const(XB + 115), y=const(IY[i]), kind=kind, r=28, s=appear(3.05 + i * .04),
                 a=life(3.05, BO, dim_at=8.4, dim_to=.35)))
    t0 = T_ON[i]
    S.add(Text(x=const(XB - 50), y=const(-40), text=WORDS[i], size=46, weight="Black", color=GOLD,
               s=Track(0, (t0, 1.4, lin), (t0 + .2, 1, out_cubic)),
               a=Track(0, (t0, 0, lin), (t0 + .06, 1, lin), (t0 + .5, 1, lin), (t0 + .6, 0, lin))))
# piscadas: primeiro a sequência, depois o "automático" frenético
blinks = [(T_ON[i], i) for i in range(5)]
t = 6.6
j = 0
while t < 8.4:
    blinks.append((t, j % 5))
    t += .13
    j += 1
for t0, i in blinks:
    S.add(Action(x=const(XB + 115), y=const(IY[i]), kind=KINDS[i], r=28, on_t=t0,
                 a=Track(0, (t0, 0, lin), (t0 + .02, 1, lin), (t0 + .2, 1, lin), (t0 + .3, 0, lin))))
    S.sfx.append((t0, "tick"))
S.add(Cursor(x=lambda t: XB + 130 + 6 * math.sin(t * 40), y=lambda t: -230 + ((int(t / .13) % 5) * 95) + 10,
             size=40, a=life(6.6, 8.4)), None)
P(XB, 330, "TUDO NO AUTOMÁTICO", 7.1, BO, color=RED, size=22)
S.add(Padlock(x=const(XB), y=const(-430), s_=110, color=GOLD, s=appear(8.4, .35), a=life(8.4, BO)), 8.4, "thud")
P(XB, 420, "DESTRAVA O ALGORITMO?", 9.0, BO, color=GOLD, size=22)

# ---------------------------------------------------------------- C: mesmo impulso / sem base (11.3–16.6)
CO = 16.6
T(XC, -470, "MESMO IMPULSO", 11.35, CO, size=66)
P(XC, -390, "O MACETE", 12.4, CO, size=22)
T(XC, -300, "DINHEIRO RÁPIDO", 13.6, CO, size=56, color=GOLD)
fall = 15.6
for i in range(3):
    by = 120 - i * 105
    S.add(Box(x=lambda t, i=i: XC + math.sin(t * 7 + i) * (6 + 10 * i), y=Track(by, (fall, by, lin), (fall + .6, by + 700, in_cubic)),
              w=230, h=95, label="R$", size=40, color=GOLD, s=appear(13.8 + i * .2), a=life(13.8 + i * .2, CO)),
          13.8 + i * .2, "pop")
S.add(Path(x=const(XC - 250), y=const(330), pts=[(0, 0), (160, 0)], width=3, color=GREY, a=life(13.8, CO)))
S.add(Path(x=const(XC + 90), y=const(330), pts=[(0, 0), (160, 0)], width=3, color=GREY, a=life(13.8, CO)))
P(XC, 420, "SEM CONSTRUIR BASE", 15.2, CO, color=RED, size=22)
S.sfx.append((fall + .55, "thud"))

# ---------------------------------------------------------------- D: não é botão (16.9–21.3)
DO = 21.45
T(XD, -460, "O TIKTOK NÃO", 16.95, DO, size=62)
T(XD, -385, "DISTRIBUI POR BOTÃO", 17.3, DO, size=46)
for i, kind in enumerate(KINDS):
    x = XD - 240 + i * 120
    S.add(Action(x=const(x), y=const(-150), kind=kind, r=32, color=GREY, s=appear(18.0 + i * .1), a=life(18.0, DO)))
    S.add(XIcon(x=const(x + 30), y=const(-185), r=16, color=RED, s=appear(19.3 + i * .15), a=life(19.3 + i * .15, DO)),
          19.3 + i * .15, "tick")
P(XD, 20, "APERTAR NÃO É ASSISTIR", 20.1, DO, size=21, color=RED)

# ---------------------------------------------------------------- E: o que ele olha (21.6–27.8)
EO = 27.8
T(XE, -470, "ELE OLHA:", 21.6, EO, size=74)
for i, (lab, val, t0) in enumerate([("ASSISTIU ATÉ O FIM", .85, 21.9), ("VOLTOU PRA VER DE NOVO", .62, 24.3),
                                     ("COMPARTILHOU DE VERDADE", .48, 26.1)]):
    S.add(Gauge(x=const(XE), y=const(-280 + i * 150), w=540, label=lab, color=GREEN,
                value=Track(0, (t0 + .2, 0, lin), (t0 + 1.1, val, out_cubic)), s=appear(t0, .3, s0=.8),
                a=life(t0, EO)), t0)
P(XE, 250, "SINAIS REAIS", 27.0, EO, color=GREEN, size=24)

# ---------------------------------------------------------------- F: piloto automático (28.1–33.1)
FO = 33.25
T(XF, -470, "PILOTO", 28.2, FO, size=80)
T(XF, -380, "AUTOMÁTICO", 28.45, FO, size=80)
S.add(Phone(x=const(XF - 170), y=const(-110), w=150, h=270, s=appear(28.6), a=life(28.6, FO)), 28.6)
S.add(Action(x=const(XF - 170), y=const(-110), kind="heart", r=30, on_t=29.0, s=appear(28.7), a=life(28.7, FO)))
T(XF, -110, "=", 30.0, FO, size=90)
S.add(Box(x=const(XF + 170), y=const(-110), w=190, h=150, label="TRABALHO", size=26, s=appear(30.4), a=life(30.4, FO)), 30.4, "pop")
P(XF, 90, "SEM ESTRATÉGIA", 32.0, FO, color=RED, size=24)

# ---------------------------------------------------------------- G: movimento sem resultado (33.4–38.7)
GO = 38.7


@dataclass
class Dashed(El):
    w: float = 640
    float_amp: float = 0

    def paint(self, c, X, Y, k, a):
        x = X - self.w * k / 2
        while x < X + self.w * k / 2:
            c.d.line([(x, Y), (x + 7 * k, Y)], fill=self.c(a * .35), width=max(1, int(2 * k)))
            x += 13 * k


S.add(Dashed(x=const(XG), y=const(330), w=640, a=life(33.3, GO)))
S.add(Person(x=const(XG), y=const(330), h=160, legs=True, run=const(1), gait=14, float_amp=0, s=appear(33.4),
             a=life(33.4, GO)), 33.4)
for i, (lab, t0, col) in enumerate([("MOVIMENTO", 33.6, (255, 255, 255)), ("CANSAÇO", 34.6, ORANGE),
                                     ("ANSIEDADE", 35.6, RED)]):
    P(XG, -420 + i * 85, lab, t0, GO, color=col, size=26)
T(XG - 30, -60, "RESULTADO", 37.1, GO, size=66)
S.add(XIcon(x=const(XG + 260), y=const(-60), r=32, color=RED, s=appear(37.6), a=life(37.6, GO)), 37.6, "thud")

# ---------------------------------------------------------------- H: moeda social (39.0–44.4)
HO = 44.55
P(XH - 160, -300, "TIKTOK", 39.1, HO, size=26)
P(XH + 160, -300, "DINHEIRO", 40.85, HO, size=26, color=GOLD)
T(XH, -460, "A MOEDA É A MESMA", 42.4, HO, size=52)
for i, (dx, lab, t0) in enumerate([(-160, "ATENÇÃO", 42.6), (160, "CONFIANÇA", 43.55)]):
    S.add(CoinIcon(x=const(XH + dx), y=const(-60), r=95, color=GOLD, s=appear(t0, .35), a=life(t0, HO)), t0, "thud")
    S.add(Text(x=const(XH + dx), y=const(90), text=lab, size=36, weight="Black", color=GOLD, s=appear(t0 + .1),
               a=life(t0 + .1, HO)))
    S.add(Path(x=const(XH + dx), y=const(-260), pts=[(0, 0), (0, 80)], arrow=True, width=3,
               prog=Track(0, (t0 - .2, 0, lin), (t0, 1, out_cubic)), a=life(t0 - .2, HO)))

# ---------------------------------------------------------------- I: entender = valor (44.7–50.8)
IO = 50.95
T(XI, -470, "POR QUE ALGUÉM…", 44.75, IO, size=58)
for i, (lab, t0) in enumerate([("PARA", 46.5), ("SALVA", 47.2), ("COMPARTILHA", 47.9)]):
    x = XI - 220 + i * 220
    if i == 0:
        ic = PauseIcon(x=const(x), y=const(-250), r=44)
    else:
        ic = Action(x=const(x), y=const(-250), kind=["bookmark", "share"][i - 1], r=40)
    ic.s, ic.a = appear(t0), life(t0, IO, dim_at=48.9, dim_to=.4)
    S.add(ic, t0, "pop")
    S.add(Text(x=const(x), y=const(-160), text=lab, size=26, weight="Black", s=appear(t0 + .05),
               a=life(t0 + .05, IO, dim_at=48.9, dim_to=.4)))
T(XI, -10, "ENTENDE", 48.9, IO, size=60)
T(XI, 200, "VALOR", 49.6, IO, size=140, color=GREEN, dur=.3)
S.add(Rays(x=const(XI), y=const(200), r=165, n=9, prog=Track(0, (49.7, 0, lin), (50.0, 1, out_back)), color=GREEN,
           a=life(49.7, IO), float_amp=0))
S.sfx.append((49.6, "thud"))

# ---------------------------------------------------------------- J: fechamento (51.1–56.1), inversão
JO = 56.15
T(XJ, -380, "QUEM GERA VALOR", 51.2, JO, size=58)
T(XJ, -280, "NÃO IMPLORA", 52.4, JO, size=80)
T(XJ, -110, "POR CLIQUE.", 54.0, JO, size=84, dur=.3)
T(XJ, 20, "NEM POR DINHEIRO.", 55.2, JO, size=62, dur=.3)
S.sfx += [(54.0, "thud"), (55.2, "thud")]

# ---------------------------------------------------------------- K: final (56.3–61)
KO = 60.7
P(XK, -390, "SIGA A PÁGINA", 57.0, KO, size=22)
S.add(Avatar(x=const(XK), y=const(-150), r=150, path=os.path.join(HERE, "assets", "guidelight.jpg"), ring=GOLD,
             s=appear(56.4, .45), a=life(56.4, KO)), 56.4, "thud")
T(XK, 80, "GUIDELIGHT", 56.7, KO, size=78)
CLICK = 58.8
S.add(Button(x=const(XK), y=const(210), w=300, h=78, text=lambda t: "SEGUINDO" if t >= CLICK else "SEGUIR",
             fill=lerp_color((255, 255, 255), GOLD, CLICK, CLICK + .15),
             s=Track(0, (57.1, 0, lin), (57.45, 1, out_back), (CLICK - .05, 1, lin), (CLICK + .05, .9, lin),
                     (CLICK + .35, 1, out_back)), a=life(57.1, KO)), 57.1)
S.add(Cursor(x=Track(XK + 300, (57.9, XK + 300, lin), (58.65, XK + 30, in_out_cubic)),
             y=Track(560, (57.9, 560, lin), (58.65, 215, in_out_cubic)), size=44,
             s=Track(1, (CLICK - .05, 1, lin), (CLICK + .05, .85, lin), (CLICK + .25, 1, out_cubic)),
             a=life(57.9, 60.4)), CLICK)
S.sfx.append((CLICK + .02, "tick"))
S.add(Rays(x=const(XK), y=const(-150), r=190, n=7, prog=Track(0, (CLICK, 0, lin), (CLICK + .3, 1, out_back)),
           color=GOLD, a=life(CLICK, KO), float_amp=0))


def mix(root):
    mix_voice(f"{root}/video_07.mp4", [(os.path.join(HERE, "assets", "voz07", f), t) for f, t in VOZ],
              f"{root}/guidelight_macete_algoritmo_v2_9x16.mp4", voice_vol=1.2)


if __name__ == "__main__":
    root = os.path.join(HERE, "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills07", exist_ok=True)
        for f in os.listdir(f"{root}/stills07"):
            os.remove(f"{root}/stills07/{f}")
        for t in [2.6, 7.6, 10.5, 15.8, 21.0, 27.5, 32.8, 38.2, 44.2, 50.5, 55.8, 59.5]:
            S.still(t, f"{root}/stills07/t{t:05.1f}.png")
        print("stills ok")
    elif "--mix" in sys.argv:
        mix(root)
    else:
        S.render(f"{root}/video_07.mp4")
        mix(root)
