"""
Vídeo 05: "2027: imposto, SUS e posse: adivinha quem paga a conta?"  (9:16, 1080×1920, ≈89 s)
Página: Guidelight. Roteiro e fontes: docs/roteiros/video_05_2027_imposto_sus_posse.md
Narração: ElevenLabs, voz "Elvis – Social Media & Shorts" (zNEsdgTUa3ndwKry8Xcq), eleven_v4, em anim/assets/voz05/

Rodar:  python3 anim/video_05.py --stills | --mix | (sem nada: render + mix)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from engine import *  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = (255, 196, 56)
RED = (255, 82, 82)
GREEN = (64, 222, 140)
ORANGE = (255, 140, 60)
GREY = (150, 150, 150)

S = Scene(W=1080, H=1920, fps=30, duration=89.5, base_w=720)
PILL = 19

VOZ = [("s01.mp3", 0.1), ("s02.mp3", 9.4), ("s03.mp3", 16.0), ("s04.mp3", 23.4), ("s05.mp3", 32.6),
       ("s06.mp3", 39.9), ("s07.mp3", 50.0), ("s08.mp3", 55.4), ("s09.mp3", 63.3), ("s10.mp3", 71.4),
       ("s11.mp3", 78.3), ("s12.mp3", 83.9)]


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
class PriceTag(El):
    w: float = 200
    h: float = 100
    text: str = "%"
    sway: float = 0.0

    def paint(self, c, X, Y, k, a):
        w, h = self.w * k, self.h * k
        X = X + math.sin(c.t * 2.4 + self.phase) * self.sway * k
        col = self.c(a)
        sw = max(1, int(3.4 * k))
        pts = [(X - w / 2, Y), (X - w / 2 + h * .45, Y - h / 2), (X + w / 2, Y - h / 2),
               (X + w / 2, Y + h / 2), (X - w / 2 + h * .45, Y + h / 2)]
        c.d.polygon(pts, outline=col, width=sw, fill=(0, 0, 0))
        r = h * .09
        hx = X - w / 2 + h * .42
        c.d.ellipse([hx - r, Y - r, hx + r, Y + r], outline=col, width=max(1, int(2.4 * k)))
        c.d.text((X + h * .2, Y), self.text, font=font("Black", h * .44), fill=col, anchor="mm")


@dataclass
class HealthCross(El):
    s_: float = 120

    def paint(self, c, X, Y, k, a):
        s = self.s_ * k
        t = s * .34
        col = self.c(a)
        sw = max(1, int(3.6 * k))
        pts = [(X - t / 2, Y - s / 2), (X + t / 2, Y - s / 2), (X + t / 2, Y - t / 2), (X + s / 2, Y - t / 2),
               (X + s / 2, Y + t / 2), (X + t / 2, Y + t / 2), (X + t / 2, Y + s / 2), (X - t / 2, Y + s / 2),
               (X - t / 2, Y + t / 2), (X - s / 2, Y + t / 2), (X - s / 2, Y - t / 2), (X - t / 2, Y - t / 2)]
        c.d.polygon(pts, outline=col, width=sw, fill=tuple(int(v * a * .18) for v in self.color))


@dataclass
class Basket(El):
    w: float = 200

    def paint(self, c, X, Y, k, a):
        w = self.w * k
        h = w * .55
        col = self.c(a)
        sw = max(1, int(3.6 * k))
        top = Y - h * .2
        c.d.arc([X - w * .32, top - h * .75, X + w * .32, top + h * .5], 180, 360, fill=col, width=sw)
        c.d.polygon([(X - w / 2, top), (X + w / 2, top), (X + w * .38, top + h), (X - w * .38, top + h)],
                    outline=col, width=sw, fill=(0, 0, 0))
        for i in range(1, 4):
            xx = X - w * .38 + i * w * .19
            c.d.line([(xx + (xx - X) * .2, top + 4 * k), (xx, top + h - 4 * k)], fill=self.c(a * .55), width=max(1, int(2.4 * k)))


@dataclass
class Podium(El):
    w: float = 360

    def paint(self, c, X, Y, k, a):
        w = self.w * k
        col = self.c(a)
        sw = max(1, int(3.4 * k))
        c.d.rectangle([X - w / 2, Y, X + w / 2, Y + 40 * k], outline=col, width=sw, fill=(0, 0, 0))
        c.d.rectangle([X - w * .32, Y + 40 * k, X + w * .32, Y + 80 * k], outline=col, width=sw, fill=(0, 0, 0))


def P(x, y, text, t, t_out=None, color=(255, 255, 255), size=PILL, dim_at=None, dim_to=.3):
    return S.add(Pill(x=const(x), y=const(y), text=text, size=size, color=color, s=appear(t),
                      a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


def T(x, y, text, t, t_out=None, size=60, color=(255, 255, 255), weight="Black", dim_at=None, dim_to=.3, dur=.35):
    return S.add(Text(x=const(x), y=const(y), text=text, size=size, weight=weight, color=color,
                      s=appear(t, dur), a=life(t, t_out, dim_at=dim_at, dim_to=dim_to)), t)


# ---------------------------------------------------------------- câmera
XA, XB, XC, XD, XE, XF, XG, XH, XI, XJ, XK, XL = [i * 1500 for i in range(12)]
S.cam_x = Track(XA, (cut(9.25), XA, lin), (cut(9.25) + .001, XB, lin),
                (15.75, XB, lin), (16.1, XC, in_out_cubic),
                (cut(23.25), XC, lin), (cut(23.25) + .001, XD, lin),
                (32.35, XD, lin), (32.7, XE, in_out_cubic),
                (cut(39.75), XE, lin), (cut(39.75) + .001, XF, lin),
                (49.75, XF, lin), (50.1, XG, in_out_cubic),
                (cut(55.25), XG, lin), (cut(55.25) + .001, XH, lin),
                (63.05, XH, lin), (63.4, XI, in_out_cubic),
                (cut(71.25), XI, lin), (cut(71.25) + .001, XJ, lin),
                (cut(78.15), XJ, lin), (cut(78.15) + .001, XK, lin),
                (83.55, XK, lin), (83.9, XL, in_out_cubic))
S.cam_y = const(0)
S.ground_a = const(0)
S.invert = Track(0, (80.3, 0, lin), (80.4, 1, out_cubic), (83.45, 1, lin), (83.55, 0, in_cubic))
S.sfx += [(t, "whoosh") for t in (15.7, 32.3, 49.7, 63.0, 83.5)] + \
         [(t, "thud") for t in (9.25, 23.25, 39.75, 55.25, 71.25, 78.15, 80.3)]

# ---------------------------------------------------------------- A: gancho (0.1–9.1)
# "Em 2027, mexem no seu imposto, no dinheiro do SUS... e ainda tem a festa da posse. Adivinha quem paga a conta?"
AO = 9.2
T(XA, -420, "2027", .05, AO, size=210, color=GOLD, dur=.4)
S.sfx.append((.05, "thud"))
for i, (dx, t0) in enumerate([(-220, 3.25), (0, 4.9), (220, 7.0)]):
    if i == 0:
        el = PriceTag(x=const(XA + dx), y=const(-110), w=150, h=76, text="%", color=GOLD, sway=4)
    elif i == 1:
        el = HealthCross(x=const(XA + dx), y=const(-110), s_=110, color=RED)
    else:
        el = Box(x=const(XA + dx), y=const(-110), w=150, h=100, label="POSSE", size=24, color=GOLD)
    el.s, el.a = appear(t0), life(t0, AO, dim_at=7.9, dim_to=.35)
    S.add(el, t0, "pop")
    P(XA + dx, -10, ["IMPOSTO", "SUS", "FESTA"][i], t0 + .15, AO, size=17, dim_at=7.9, dim_to=.35)
S.add(Rays(x=const(XA + 220), y=const(-110), r=95, prog=Track(0, (7.1, 0, lin), (7.4, 1, out_back)), color=GOLD,
           a=life(7.1, AO, dim_at=7.9, dim_to=.3), float_amp=0))
S.add(Person(x=const(XA), y=const(400), h=160, s=appear(7.85), a=life(7.85, AO)), 7.85)
S.add(PriceTag(x=const(XA), y=Track(-800, (8.1, -800, lin), (8.5, 150, out_back)), w=230, h=100, text="CONTA",
               color=RED, a=life(8.1, AO), float_amp=0), 8.5, "thud")
P(XA, 520, "ADIVINHA QUEM PAGA?", 8.3, AO, color=RED, size=22)

# ---------------------------------------------------------------- B: reforma (9.4–15.7)
# "Começa pela reforma tributária. Em janeiro, a CBS substitui o PIS e a Cofins."
BO = 15.75
T(XB, -440, "REFORMA", 9.45, BO, size=84)
T(XB, -350, "TRIBUTÁRIA", 9.75, BO, size=84)
P(XB, -220, "JANEIRO DE 2027", 11.8, BO, color=GOLD, size=22)
for i, (dx, lab) in enumerate([(-140, "PIS"), (140, "COFINS")]):
    S.add(Box(x=const(XB + dx), y=const(-60), w=220, h=110, label=lab, size=34, color=GREY, s=appear(12.5 + i * .25),
              a=life(12.5 + i * .25, BO, dim_at=13.6, dim_to=.25)), 12.5 + i * .25)
    S.add(XIcon(x=const(XB + dx + 100), y=const(-110), r=22, color=RED, s=appear(13.6 + i * .15),
                a=life(13.6 + i * .15, BO)), 13.6 + i * .15)
S.add(Path(x=const(XB), y=const(20), pts=[(0, 0), (0, 90)], arrow=True, width=3.4, color=GOLD,
           prog=Track(0, (13.8, 0, lin), (14.1, 1, out_cubic)), a=life(13.8, BO)))
S.add(Box(x=const(XB), y=const(220), w=300, h=140, label="CBS", size=70, color=GOLD, s=appear(14.0, .4),
          a=life(14.0, BO)), 14.0, "thud")

# ---------------------------------------------------------------- C: alíquota (16.0–23.1)
# "O Tribunal de Contas calculou a alíquota em 11,3%. E quem bate o martelo é o Senado."
CO = 23.25
P(XC, -440, "TRIBUNAL DE CONTAS (TCU)", 16.1, CO, size=21)
S.add(Text(x=const(XC), y=const(-250), size=170, weight="Black", color=GOLD,
           text=counter(lambda v: f"{v:.1f}%".replace(".", ","), 0, 11.3, 17.5, 1.8),
           s=appear(17.3, .35), a=life(17.3, CO, dim_at=20.8, dim_to=.45)), 17.3)
S.sfx += [(17.5 + i * .12, "tick") for i in range(14)]
P(XC, -110, "ALÍQUOTA DE REFERÊNCIA DA CBS", 18.6, CO, size=19)
S.add(Box(x=const(XC), y=const(150), w=330, h=130, label="SENADO", size=52, s=appear(20.85, .35),
          a=life(20.85, CO)), 20.85, "thud")
S.add(Rays(x=const(XC), y=const(150), r=210, n=7, prog=Track(0, (21.1, 0, lin), (21.4, 1, out_back)), color=GOLD,
           a=life(21.1, CO), float_amp=0))
P(XC, 300, "BATE O MARTELO ATÉ 15/12", 21.6, CO, color=GOLD, size=20)

# ---------------------------------------------------------------- D: cesta básica (23.4–32.3)
# "A cesta básica fica com imposto zero. Mas atenção: imposto menor não quer dizer preço menor. Depende de alguém repassar."
DO = 32.35
S.add(Basket(x=const(XD), y=const(-370), w=230, s=appear(23.5, .4), a=life(23.5, DO)), 23.5)
P(XD, -205, "CESTA BÁSICA", 23.8, DO, size=21)
T(XD, -120, "IMPOSTO ZERO", 24.6, DO, size=66, color=GREEN)
S.add(WarnIcon(x=const(XD), y=const(10), r=30, color=ORANGE, s=appear(26.25), a=life(26.25, DO)), 26.25, "thud")
P(XD, 80, "MAS ATENÇÃO", 26.35, DO, color=ORANGE, size=20)
T(XD - 40, 180, "IMPOSTO MENOR", 27.35, DO, size=46, color=GREEN)
S.add(CheckIcon(x=const(XD + 210), y=const(180), r=22, color=GREEN, s=appear(27.7), a=life(27.7, DO)), 27.7)
T(XD - 40, 260, "PREÇO MENOR", 28.8, DO, size=46, color=RED)
T(XD + 200, 260, "?", 29.4, DO, size=60, color=RED)
P(XD, 360, "DEPENDE DE ALGUÉM REPASSAR", 30.6, DO, color=GOLD, size=20)

# ---------------------------------------------------------------- E: SUS (32.6–39.6)
# "Agora, a saúde. Um projeto do governo, já aprovado no Senado, muda a conta do piso do SUS."
EO = 39.75
T(XE, -440, "SAÚDE", 32.65, EO, size=96, color=RED)
S.add(HealthCross(x=const(XE), y=const(-250), s_=150, color=RED, s=appear(32.9, .4), a=life(32.9, EO)), 32.9, "thud")
P(XE, -110, "PROJETO DO GOVERNO", 34.45, EO, size=22)
P(XE - 30, -40, "APROVADO NO SENADO", 35.6, EO, size=20, color=GOLD)
S.add(CheckIcon(x=const(XE + 165), y=const(-40), r=20, color=GOLD, s=appear(36.0), a=life(36.0, EO)), 36.0)
P(XE, 30, "FALTA A CÂMARA", 36.4, EO, size=16)
T(XE, 180, "PISO DO SUS", 37.6, EO, size=64)
S.add(Path(x=const(XE - 230), y=const(240), pts=[(0, 0), (460, 0)], width=4, color=RED,
           prog=Track(0, (37.8, 0, lin), (38.3, 1, out_cubic)), a=life(37.8, EO)))
P(XE, 320, "NOVA REGRA DE CÁLCULO", 38.4, EO, color=RED, size=20)

# ---------------------------------------------------------------- F: 10 bi (39.9–49.7)
# "Entidades da saúde calculam que o SUS pode perder até 10 bilhões de reais por ano.
#  O governo nega, e diz que o orçamento da saúde vai crescer."
FO = 49.75
P(XF, -460, "ENTIDADES DA SAÚDE", 40.0, FO, size=22)
P(XF, -390, "CALCULAM", 40.9, FO, size=17)
S.add(Text(x=const(XF), y=const(-250), size=84, weight="Black", color=RED,
           text=counter(lambda v: f"ATÉ -R$ {int(round(v))} BI", 0, 10, 42.0, 2.4),
           s=appear(41.8, .35), a=life(41.8, FO, dim_at=46.0, dim_to=.5)), 41.8, "thud")
S.sfx += [(42.0 + i * .2, "tick") for i in range(11)]
P(XF, -140, "POR ANO · ESTIMATIVA", 44.2, FO, color=RED, size=20)
S.add(Path(x=const(XF - 300), y=const(-50), pts=[(0, 0), (600, 0)], width=2, color=GREY,
           prog=Track(0, (45.6, 0, lin), (46.0, 1, out_cubic)), a=life(45.6, FO)))
T(XF, 60, "O GOVERNO NEGA", 46.05, FO, size=58)
T(XF, 160, "\"O ORÇAMENTO VAI CRESCER\"", 47.6, FO, size=34, color=GREEN)
S.add(Path(x=const(XF), y=const(330), pts=[(0, 0), (0, -100)], arrow=True, width=4, color=GREEN,
           prog=Track(0, (48.0, 0, lin), (48.4, 1, out_cubic)), a=life(48.0, FO)), 48.0)

# ---------------------------------------------------------------- G: posse (50.0–55.1)
# "E no meio disso tudo... a posse presidencial, dia 5 de janeiro."
GO = 55.25
T(XG, -440, "E NO MEIO DISSO TUDO…", 50.1, GO, size=44)
S.add(Person(x=const(XG), y=const(-10), h=170, color=GOLD, s=appear(51.85, .35), a=life(51.85, GO)), 51.85)
S.add(Podium(x=const(XG), y=const(-10), w=380, s=appear(51.9), a=life(51.9, GO)))
S.add(Rays(x=const(XG), y=const(-110), r=150, n=7, prog=Track(0, (52.0, 0, lin), (52.3, 1, out_back)),
           color=GOLD, a=life(52.0, GO), float_amp=0))
T(XG, 190, "POSSE", 52.0, GO, size=110, color=GOLD)
S.sfx.append((52.0, "thud"))
P(XG, 300, "5 DE JANEIRO", 53.6, GO, size=24)

# ---------------------------------------------------------------- H: 2023 (55.4–63.0)
# "Em 2023, só a cerimônia custou 628 mil reais aos cofres públicos. Fora o show."
HO = 63.1
P(XH, -460, "POSSE DE 2023", 55.45, HO, size=22)
P(XH, -390, "SÓ A CERIMÔNIA", 57.6, HO, size=19)
S.add(Text(x=const(XH), y=const(-240), size=96, weight="Black", color=GOLD,
           text=counter(lambda v: f"R$ {int(round(v))} MIL", 0, 628, 58.6, 2.3),
           s=appear(58.4, .35), a=life(58.4, HO)), 58.4)
S.sfx += [(58.6 + i * .15, "tick") for i in range(14)]
P(XH, -130, "AOS COFRES PÚBLICOS", 60.4, HO, size=19)
T(XH, 60, "+ SHOW", 62.0, HO, size=110, color=RED, dur=.3)
P(XH, 170, "NÃO ENTRA NA CONTA", 62.3, HO, color=RED, size=18)
S.sfx.append((62.0, "thud"))

# ---------------------------------------------------------------- I: 2027 (63.3–71.1)
# "Pra essa, o custo oficial ainda não foi divulgado. Mas as diárias em Brasília já subiram até 600%."
IO = 71.25
P(XI, -460, "POSSE DE 2027", 63.35, IO, size=22, color=GOLD)
S.add(Text(x=const(XI), y=const(-300), text="R$ ???", size=140, weight="Black",
           s=Track(0, (63.6, 0, lin), (63.95, 1, out_back)), a=life(63.6, IO, dim_at=66.8, dim_to=.4)), 63.6, "thud")
P(XI, -180, "CUSTO OFICIAL NÃO DIVULGADO", 64.9, IO, color=RED, size=20)
P(XI, -20, "DIÁRIAS EM BRASÍLIA", 66.9, IO, size=22)
S.add(Text(x=const(XI), y=const(120), size=150, weight="Black", color=RED,
           text=counter(lambda v: f"+{int(round(v))}%", 0, 600, 68.6, 2.0),
           s=appear(68.4, .35), a=life(68.4, IO)), 68.4)
S.sfx += [(68.6 + i * .13, "tick") for i in range(15)]
P(XI, 260, "FONTE: MPDFT", 69.5, IO, size=15)

# ---------------------------------------------------------------- J: resumo (71.4–78.0)
# "Resumindo: imposto novo, saúde com menos garantia... e festa sem preço na etiqueta."
JO = 78.15
P(XJ, -460, "RESUMINDO", 71.45, JO, size=24)
rows = [(-260, 72.45, "IMPOSTO NOVO", GOLD), (-90, 73.6, "SAÚDE COM MENOS GARANTIA", RED),
        (80, 75.75, "FESTA SEM PREÇO NA ETIQUETA", GOLD)]
for y, t0, txt, col in rows:
    if col == RED and "SAÚDE" in txt:
        ic = HealthCross(x=const(XJ - 270), y=const(y), s_=70, color=RED)
    else:
        ic = PriceTag(x=const(XJ - 270), y=const(y), w=100, h=56, text="%" if "IMPOSTO" in txt else "?", color=col)
    ic.s, ic.a = appear(t0), life(t0, JO)
    S.add(ic, t0, "pop")
    S.add(Text(x=const(XJ + 40), y=const(y), text=txt, size=28, weight="Black", color=col, s=appear(t0 + .1),
               a=life(t0 + .1, JO)))

# ---------------------------------------------------------------- K: fiscaliza (78.3–83.6), com inversão
# "E quem fiscaliza tudo isso? Você. Mas só se estiver prestando atenção."
KO = 83.55
T(XK, -330, "QUEM FISCALIZA?", 78.35, KO, size=66)
T(XK, -110, "VOCÊ.", 80.37, KO, size=170, dur=.3)
S.add(Person(x=const(XK), y=const(330), h=170, s=appear(80.4), a=life(80.4, KO)), 80.4)
P(XK, 60, "SE ESTIVER PRESTANDO ATENÇÃO", 81.3, KO, size=20)

# ---------------------------------------------------------------- L: final (83.7–89.5)
LO = 89.2
P(XL, -390, "SIGA A PÁGINA", 84.6, LO, size=22)
S.add(Avatar(x=const(XL), y=const(-150), r=150, path=os.path.join(HERE, "assets", "guidelight.jpg"), ring=GOLD,
             s=appear(83.95, .45), a=life(83.95, LO)), 83.95, "thud")
T(XL, 80, "GUIDELIGHT", 84.3, LO, size=78)
CLICK = 86.9
S.add(Button(x=const(XL), y=const(210), w=300, h=78, text=lambda t: "SEGUINDO" if t >= CLICK else "SEGUIR",
             fill=lerp_color((255, 255, 255), GOLD, CLICK, CLICK + .15),
             s=Track(0, (85.0, 0, lin), (85.35, 1, out_back), (CLICK - .05, 1, lin), (CLICK + .05, .9, lin),
                     (CLICK + .35, 1, out_back)), a=life(85.0, LO)), 85.0)
S.add(Cursor(x=Track(XL + 300, (86.0, XL + 300, lin), (86.75, XL + 30, in_out_cubic)),
             y=Track(560, (86.0, 560, lin), (86.75, 215, in_out_cubic)), size=44,
             s=Track(1, (CLICK - .05, 1, lin), (CLICK + .05, .85, lin), (CLICK + .25, 1, out_cubic)),
             a=life(86.0, 88.8)), CLICK)
S.sfx.append((CLICK + .02, "tick"))
S.add(Rays(x=const(XL), y=const(-150), r=190, n=7, prog=Track(0, (CLICK, 0, lin), (CLICK + .3, 1, out_back)),
           color=GOLD, a=life(CLICK, LO), float_amp=0))


def mix(root):
    mix_voice(f"{root}/video_05.mp4", [(os.path.join(HERE, "assets", "voz05", f), t) for f, t in VOZ],
              f"{root}/guidelight_2027_imposto_sus_posse_9x16.mp4", voice_vol=1.2)


if __name__ == "__main__":
    root = os.path.join(HERE, "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills05", exist_ok=True)
        for f in os.listdir(f"{root}/stills05"):
            os.remove(f"{root}/stills05/{f}")
        for t in [8.9, 15.2, 22.8, 31.8, 39.2, 49.2, 54.8, 62.7, 70.8, 77.7, 82.8, 88.0]:
            S.still(t, f"{root}/stills05/t{t:05.1f}.png")
        print("stills ok")
    elif "--mix" in sys.argv:
        mix(root)
    else:
        S.render(f"{root}/video_05.mp4")
        mix(root)
