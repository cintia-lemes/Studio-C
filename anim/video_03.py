"""
Vídeo 03: "Por que a Black Friday cai junto com o 13º"  (9:16, 1080×1920, ≈66 s)
Página: Guidelight. Roteiro: docs/roteiros/video_03_black_friday_13.md
Narração: ElevenLabs, voz "Letícia – Gentle, Pleasant & Warm" (CcElPA8NBrawbunFs7rh), eleven_v4, em anim/assets/voz03/
(versão anterior com a voz Jarnathan em anim/assets/voz03_jarnathan/)

Rodar:  python3 anim/video_03.py --stills   (prévia)
        python3 anim/video_03.py            -> out/guidelight_black_friday_13_9x16.mp4
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

# Mundo vertical: 720 × 1280 unidades visíveis (base_w=720), renderizado em 1080×1920.
S = Scene(W=1080, H=1920, fps=30, duration=66.5, base_w=720)
PILL = 19  # pílulas um pouco maiores para celular

# Início de cada fala (s) — escolhidos a partir da duração real dos áudios
VOZ = [("s01.mp3", 0.2), ("s02.mp3", 3.8), ("s03.mp3", 7.7), ("s04.mp3", 11.9), ("s05.mp3", 17.1),
       ("s06.mp3", 23.4), ("s07.mp3", 29.0), ("s08.mp3", 35.0), ("s09.mp3", 41.0), ("s10.mp3", 47.1),
       ("s11.mp3", 53.5), ("s12.mp3", 61.65)]


def clamp01(x):
    return max(0.0, min(1.0, x))


def cut(t):
    """Cortes secos fora da grade de quadros (evita borrão falso)."""
    return t + 0.015


# ======================================================================
# Elementos específicos deste vídeo
# ======================================================================

@dataclass
class CalendarGrid(El):
    w: float = 400
    title: str = "NOVEMBRO"
    first_col: int = 0      # 1/11/2026 cai num domingo
    days: int = 30
    hl_day: int = 27        # Black Friday 2026
    hl_t: float = 1.0

    def paint(self, c, X, Y, k, a):
        w = self.w * k
        cols, cell = 7, w / 7
        rows = 5
        head = cell * 1.1
        h = head + cell * .6 + cell * rows
        x0, y0 = X - w / 2, Y - h / 2
        col = self.c(a)
        sw = max(1, int(3 * k))
        c.d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=12 * k, outline=col, width=sw, fill=(0, 0, 0))
        c.d.line([(x0, y0 + head), (x0 + w, y0 + head)], fill=col, width=sw)
        c.d.text((X, y0 + head / 2), self.title, font=font("Black", head * .42), fill=col, anchor="mm")
        for i, d in enumerate("DSTQQSS"):
            c.d.text((x0 + cell * (i + .5), y0 + head + cell * .3), d, font=font("Bold", cell * .22),
                     fill=self.c(a * .5), anchor="mm")
        for day in range(1, self.days + 1):
            idx = self.first_col + day - 1
            r, cc = divmod(idx, 7)
            cx = x0 + cell * (cc + .5)
            cy = y0 + head + cell * .6 + cell * (r + .5)
            if day == self.hl_day and c.t >= self.hl_t:
                p = clamp01((c.t - self.hl_t) / .3)
                pulse = 1 + .08 * math.sin((c.t - self.hl_t) * 8)
                rr = cell * .42 * out_back(p) * pulse
                c.d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=tuple(int(v * a) for v in GOLD))
                c.d.text((cx, cy), str(day), font=font("Black", cell * .34), fill=(0, 0, 0), anchor="mm")
            else:
                c.d.text((cx, cy), str(day), font=font("Bold", cell * .28), fill=self.c(a * .75), anchor="mm")


@dataclass
class Phone(El):
    w: float = 250
    h: float = 470
    notif_t: float = 1.0

    def paint(self, c, X, Y, k, a):
        w, h = self.w * k, self.h * k
        col = self.c(a)
        sw = max(1, int(3.4 * k))
        c.d.rounded_rectangle([X - w / 2, Y - h / 2, X + w / 2, Y + h / 2], radius=34 * k, outline=col,
                              width=sw, fill=(0, 0, 0))
        c.d.line([(X - w * .14, Y - h / 2 + 18 * k), (X + w * .14, Y - h / 2 + 18 * k)], fill=col, width=sw)
        p = clamp01((c.t - self.notif_t) / .45)
        if p > 0:
            e = out_back(p)
            nw, nh = w - 34 * k, 104 * k
            ny = Y - h / 2 + 40 * k + (1 - e) * -60 * k
            na = a * out_cubic(p)
            gold = tuple(int(v * na) for v in GOLD)
            c.d.rounded_rectangle([X - nw / 2, ny, X + nw / 2, ny + nh], radius=18 * k, outline=gold,
                                  width=sw, fill=(0, 0, 0))
            CoinIcon(r=20, color=GOLD).paint(c, X - nw / 2 + 36 * k, ny + nh / 2, k, na)
            c.d.text((X - nw / 2 + 66 * k, ny + nh * .36), "13º SALÁRIO", font=font("Black", 20 * k),
                     fill=gold, anchor="lm")
            c.d.text((X - nw / 2 + 66 * k, ny + nh * .68), "CAIU NA CONTA", font=font("Bold", 13 * k),
                     fill=self.c(na * .8), anchor="lm")


@dataclass
class Bars(El):
    heights: tuple = (110, 170, 140, 250)
    t0: float = 0
    hl_t: float = 99
    bw: float = 74
    gap: float = 30

    def paint(self, c, X, Y, k, a):
        n = len(self.heights)
        tot = n * self.bw + (n - 1) * self.gap
        x = X - tot * k / 2
        for i, hh in enumerate(self.heights):
            p = clamp01((c.t - self.t0 - i * .22) / .45)
            if p > 0:
                hgt = hh * k * out_back(p, 1.2)
                hl = i == n - 1 and c.t >= self.hl_t
                colr = tuple(int(v * a) for v in (GOLD if hl else self.color))
                c.d.rounded_rectangle([x, Y - hgt, x + self.bw * k, Y], radius=6 * k, outline=colr,
                                      width=max(1, int(3 * k)), fill=(0, 0, 0) if not hl else
                                      tuple(int(v * a * .25) for v in GOLD))
            x += (self.bw + self.gap) * k
        c.d.line([(X - tot * k / 2 - 14 * k, Y), (X + tot * k / 2 + 14 * k, Y)], fill=self.c(a * .6),
                 width=max(1, int(2.4 * k)))


@dataclass
class Gift(El):
    w: float = 180

    def paint(self, c, X, Y, k, a):
        w = self.w * k
        col = self.c(a)
        sw = max(1, int(3.4 * k))
        top = Y - w * .25
        c.d.rectangle([X - w * .45, top, X + w * .45, Y + w * .5], outline=col, width=sw, fill=(0, 0, 0))
        c.d.rectangle([X - w * .52, top - w * .2, X + w * .52, top], outline=col, width=sw, fill=(0, 0, 0))
        c.d.line([(X, top - w * .2), (X, Y + w * .5)], fill=col, width=sw)
        for s_ in (-1, 1):
            c.d.ellipse([X + s_ * w * .02 - (w * .22 if s_ < 0 else 0), top - w * .45,
                         X + s_ * w * .02 + (w * .22 if s_ > 0 else 0), top - w * .2], outline=col, width=sw)


@dataclass
class PriceTag(El):
    w: float = 200
    h: float = 100
    text: str = "-50%"
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
class Dashed(El):
    w: float = 640
    float_amp: float = 0

    def paint(self, c, X, Y, k, a):
        dash, gap = 7 * k, 6 * k
        x = X - self.w * k / 2
        while x < X + self.w * k / 2:
            c.d.line([(x, Y), (x + dash, Y)], fill=self.c(a * .35), width=max(1, int(2 * k)))
            x += dash + gap


@dataclass
class Dot(El):
    r: float = 14
    float_amp: float = 0

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        c.d.ellipse([X - r, Y - r, X + r, Y + r], fill=self.c(a))


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


def P(x, y, text, t, t_out=None, color=(255, 255, 255), size=PILL, dim_at=None):
    return S.add(Pill(x=const(x), y=const(y), text=text, size=size, color=color, s=appear(t),
                      a=life(t, t_out, dim_at=dim_at)), t)


# ======================================================================
# CÂMERA
# ======================================================================
TLX = 4000                                     # coluna da linha do tempo
NODES = [0, 1300, 2600, 3900, 5200]            # JAN, ABR–JUN, JUL–SET, OUT, NOV
PAN = [16.9, 22.95, 28.8, 34.7]                # descidas entre meses

S.cam_x = Track(0, (3.45, 0, lin), (3.85, 1000, in_out_cubic),            # whip A→B
                (cut(7.6), 1000, lin), (cut(7.6) + .001, 2000, lin),        # corte → inversão
                (cut(11.75), 2000, lin), (cut(11.75) + .001, TLX, lin),     # corte → linha do tempo
                (40.6, TLX, lin), (41.0, 7000, in_out_cubic),               # whip → pico
                (cut(46.9), 7000, lin), (cut(46.9) + .001, 9000, lin),      # corte → dezembro
                (cut(53.3), 9000, lin), (cut(53.3) + .001, 11000, lin),     # corte → compare
                (61.0, 11000, lin), (61.4, 13000, in_out_cubic))            # whip → final
cy_keys = [(cut(11.75), 0, lin)]
for i, tp in enumerate(PAN):
    cy_keys += [(tp, NODES[i], lin), (tp + .7, NODES[i + 1], in_out_cubic)]
cy_keys += [(40.8, NODES[-1], lin), (40.801, 0, lin)]                      # no meio do whip
S.cam_y = Track(0, *cy_keys)
S.ground_a = const(0)
S.invert = Track(0, (cut(7.6), 0, lin), (cut(7.6) + .12, 1, out_cubic), (11.6, 1, lin), (11.75, 0, in_cubic))
S.sfx += [(3.4, "whoosh"), (40.55, "whoosh"), (60.95, "whoosh"), (7.6, "thud"), (11.75, "thud"),
          (46.9, "thud"), (53.3, "thud")] + [(tp, "whoosh") for tp in PAN]

# ======================================================================
# A: "A Black Friday não cai no fim de novembro por acaso." (0.2–3.5)
# ======================================================================
S.add(Text(x=const(0), y=const(-430), text="BLACK FRIDAY", size=72, weight="Black", s=appear(.1, .4),
           a=life(.1, 3.45)), .1, "thud")
S.add(CalendarGrid(x=const(0), y=const(-60), w=440, hl_t=1.2, s=appear(.5, .4, s0=.6), a=life(.5, 3.45)), .5)
S.sfx.append((1.2, "pop"))
P(-40, 280, "POR ACASO?", 2.0, 3.45)
S.add(XIcon(x=const(105), y=const(280), r=24, color=RED, s=appear(2.7), a=life(2.7, 3.45)), 2.7)

# ======================================================================
# B: "Ela chega bem quando o 13º cai na sua conta." (3.8–7.4)
# ======================================================================
S.add(Phone(x=const(1000), y=const(-70), notif_t=5.0, s=appear(3.9, .4), a=life(3.9, 7.55)), 3.9)
S.sfx.append((5.0, "pop"))
for i, t0 in enumerate([5.5, 5.75, 6.0, 6.25]):
    xx = 1000 + (-70, 40, -20, 70)[i]
    S.add(CoinIcon(x=const(xx), y=Track(-700, (t0, -700, lin), (t0 + .55, 40, in_cubic)), r=22, color=GOLD,
                   s=appear(t0, .2), a=Track(0, (t0, 0, lin), (t0 + .1, 1, lin), (t0 + .5, 1, lin),
                                             (t0 + .6, 0, lin))))
    S.sfx.append((t0 + .55, "tick"))
P(1000, 300, "1ª PARCELA: ATÉ 30/11", 6.1, 7.55, color=GOLD)

# ======================================================================
# C: INVERSÃO: "E as lojas se preparam pra isso o ano inteiro." (7.7–11.6)
# ======================================================================
S.add(Text(x=const(2000), y=const(-150), text="O ANO", size=132, weight="Black", s=appear(7.75, .4),
           a=life(7.75, 11.6, dur=.12)), 7.75)
S.add(Text(x=const(2000), y=const(-10), text="INTEIRO", size=132, weight="Black", s=appear(8.0, .4),
           a=life(8.0, 11.6, dur=.12)), 8.0)
P(2000, 120, "AS LOJAS SE PREPARAM", 8.6, 11.6)
for i, m in enumerate("JFMAMJJASOND"):
    t0 = 9.0 + i * .17
    S.add(Text(x=const(2000 - 275 + i * 50), y=const(280), text=m, size=30, weight="Black",
               s=appear(t0, .25), a=life(t0, 11.6, dur=.12)), t0, "tick")

# ======================================================================
# LINHA DO TEMPO (11.9–40.6)
# ======================================================================
LX = TLX - 310
S.add(Path(x=const(LX), y=const(-430), pts=[(0, 0), (0, NODES[-1])], width=3,
           prog=lambda t: clamp01(S.cam_y(t) / NODES[-1]) if 11.7 < t < 40.8 else 0,
           a=life(11.8, 40.6), color=(120, 120, 120)))
TITLES = ["JANEIRO", "ABRIL – JUNHO", "JULHO – SETEMBRO", "OUTUBRO", "NOVEMBRO"]
T_IN = [11.85] + [tp + .55 for tp in PAN]
T_OUT = PAN + [40.55]
for ny, name, ti, to in zip(NODES, TITLES, T_IN, T_OUT):
    S.add(Dot(x=const(LX), y=const(ny - 430), r=13, color=GOLD, s=appear(ti), a=life(ti, 40.6)), ti)
    S.add(Text(x=const(TLX + 20), y=const(ny - 430), text=name, size=50, weight="Black", s=appear(ti, .35),
               a=life(ti, 40.6, dim_at=to, dim_to=.25)), ti)

# JAN: "Em janeiro, elas olham o que mais vendeu no ano passado. E definem a meta." (11.9–16.8)
Y0 = NODES[0]
S.add(Bars(x=const(TLX + 20), y=const(Y0 + 170), t0=12.5, hl_t=14.0, s=const(1), a=life(12.5, 16.9)))
S.sfx += [(12.5 + i * .22, "pop") for i in range(4)]
P(TLX + 20, Y0 + 230, "ANO PASSADO", 12.9, 16.9)
P(TLX + 120, Y0 - 170, "MAIS VENDEU", 14.0, 16.9, color=GOLD)
S.add(Path(x=const(TLX - 190), y=const(Y0 - 270), pts=[(0, 0), (420, 0)], width=3, color=GREEN,
           prog=Track(0, (15.5, 0, lin), (15.9, 1, out_cubic)), a=life(15.5, 16.9)), 15.5)
P(TLX + 20, Y0 - 320, "META", 15.7, 16.9, color=GREEN)

# ABR–JUN: "No meio do ano, já estão comprando estoque. Muita coisa vem de fora e leva meses pra chegar."
Y1 = NODES[1]
for i, (bx, by, t0) in enumerate([(TLX - 70, Y1 + 280, 17.7), (TLX + 110, Y1 + 280, 18.0),
                                   (TLX + 20, Y1 + 180, 18.3)]):
    S.add(Box(x=const(bx), y=Track(by - 420, (t0, by - 420, lin), (t0 + .4, by, out_back)), w=170, h=96,
              label="ESTOQUE", size=19, a=life(t0, 22.95)), t0 + .38, "thud")
S.add(Path(x=const(TLX - 260), y=const(Y1 - 90), pts=[(0, 0), (520, 0)], arrow=True, width=3,
           prog=Track(0, (19.9, 0, lin), (20.6, 1, in_out_cubic)), a=life(19.9, 22.95)), 19.9)
P(TLX - 180, Y1 - 150, "VEM DE FORA", 20.0, 22.95)
S.add(Clock(x=const(TLX + 150), y=const(Y1 - 200), r=40, speed=16, s=appear(21.2), a=life(21.2, 22.95)), 21.2)
P(TLX + 150, Y1 - 290, "MESES", 21.5, 22.95, color=GOLD)

# JUL–SET: "Depois, escolhem a isca: o produto com desconto que vai chamar você pra loja."
Y2 = NODES[2]
S.add(Path(x=const(TLX + 20), y=const(Y2 - 380), pts=[(0, 0), (0, 200)], width=2.4, color=(170, 170, 170),
           prog=Track(0, (24.4, 0, lin), (24.8, 1, out_cubic)), a=life(24.4, 28.8)), 24.4)
S.add(PriceTag(x=const(TLX + 20), y=const(Y2 - 130), w=230, h=110, text="-50%", color=RED, sway=10,
               s=appear(25.2, .35), a=life(25.2, 28.8)), 25.2, "thud")
P(TLX + 20, Y2 - 10, "ISCA", 25.6, 28.8, color=RED)
S.add(Rays(x=const(TLX + 20), y=const(Y2 - 130), r=130, prog=Track(0, (26.3, 0, lin), (26.6, 1, out_back)),
           color=RED, a=life(26.3, 28.8), float_amp=0))
S.add(Dashed(x=const(TLX + 20), y=const(Y2 + 330), w=640, a=life(24.0, 28.8)))
S.add(Person(x=Track(TLX - 230, (26.4, TLX - 230, lin), (28.0, TLX + 10, in_out_cubic)), y=const(Y2 + 330),
             h=150, legs=True, run=Track(0, (26.3, 0, lin), (26.5, .6, lin), (27.8, .6, lin), (28.1, 0, lin)),
             gait=8, float_amp=0, s=appear(24.0), a=life(24.0, 28.8)), 24.0)
P(TLX - 120, Y2 + 120, "VEM PRA LOJA", 27.0, 28.8)

# OUT: "Em outubro, contratam gente extra e reforçam o site. Tudo pra aguentar o pico."
Y3 = NODES[3]
S.add(Dashed(x=const(TLX + 20), y=const(Y3 + 340), w=640, a=life(29.4, 34.7)))
for i, (dx, t0) in enumerate([(0, 29.7), (-150, 30.4), (150, 30.6), (-290, 30.9), (290, 31.0)]):
    S.add(Person(x=const(TLX + 20 + dx), y=const(Y3 + 340), h=130 if i < 3 else 105,
                 s=appear(t0), a=life(t0, 34.7), phase=i), t0)
S.add(Text(x=const(TLX + 20), y=const(Y3 + 130), text="x3", size=60, weight="Black", color=GOLD,
           s=appear(31.1, .35), a=life(31.1, 34.7)), 31.1)
S.add(Box(x=const(TLX + 20), y=const(Y3 - 170), w=270, h=160, label="SITE", size=34, s=appear(31.8),
          a=life(31.8, 34.7)), 31.8, "thud")
S.add(CheckIcon(x=const(TLX + 155), y=const(Y3 - 250), r=24, color=GREEN, s=appear(32.4), a=life(32.4, 34.7)), 32.4)
S.add(Rays(x=const(TLX + 20), y=const(Y3 - 170), r=150, prog=Track(0, (33.0, 0, lin), (33.3, 1, out_back)),
           color=GOLD, a=life(33.0, 34.7), float_amp=0))
P(TLX + 20, Y3 - 10, "AGUENTAR O PICO", 33.1, 34.7)

# NOV: "Em novembro, começa o esquenta. Ofertas antes da hora, só pra você entrar no clima."
Y4 = NODES[4]
P(TLX + 20, Y4 - 320, "ESQUENTA", 35.6, 40.55, color=ORANGE, size=24)
for i, (dx, dy, txt, t0) in enumerate([(-150, -150, "-10%", 37.1), (130, -90, "-20%", 37.45),
                                        (-80, 20, "-30%", 37.8)]):
    S.add(PriceTag(x=const(TLX + 20 + dx), y=const(Y4 + dy), w=170, h=84, text=txt, color=ORANGE,
                   sway=6, phase=i, s=appear(t0), a=life(t0, 40.55, dim_at=38.5, dim_to=.35)), t0)
for i, (txt, t0) in enumerate([("3", 38.6), ("2", 39.25), ("1", 39.9)]):
    S.add(Text(x=const(TLX + 20), y=const(Y4 + 260), text=txt, size=230, weight="Black", color=GOLD,
               s=Track(0, (t0, 1.6, lin), (t0 + .25, 1, out_cubic)),
               a=Track(0, (t0, 0, lin), (t0 + .08, 1, lin), (t0 + .5, 1, lin), (t0 + .62, 0, lin))), t0, "thud")

# ======================================================================
# PICO: "Aí chega o dia. Dinheiro novo no bolso, vontade de comprar e oferta na tela." (41.0–46.7)
# ======================================================================
X9 = 7000
S.add(Text(x=const(X9), y=const(-470), text="O DIA", size=80, weight="Black", s=appear(41.05, .4),
           a=life(41.05, 46.85)), 41.05)
for i, (dx, label, colr, t0) in enumerate([(-235, "13º", GOLD, 42.3), (0, "VONTADE", (255, 255, 255), 43.7),
                                            (235, "OFERTA", RED, 45.0)]):
    S.add(Box(x=const(X9 + dx), y=const(-300), w=205, h=110, label=label, size=26 if i == 0 else 21,
              color=colr, s=appear(t0), a=life(t0, 46.85)), t0, "thud")
    S.add(Path(x=const(X9 + dx), y=const(-240), pts=[(0, 0), (-dx * .55, 120)], arrow=True, width=3,
               color=colr, prog=Track(0, (t0 + .3, 0, lin), (t0 + .6, 1, out_cubic)), a=life(t0 + .3, 46.85)), t0 + .3)
curve = [(i * 30, -(1.03 ** (i * 6) - 1) * 9) for i in range(20)]
S.add(Path(x=const(X9 - 285), y=const(380), pts=curve, width=4.5, color=GREEN,
           prog=Track(0, (42.4, 0, lin), (46.3, 1, in_cubic)), tip=CoinIcon(r=20, color=GOLD, s=appear(42.4)),
           a=life(42.4, 46.85)), 42.4)
S.add(Path(x=const(X9 - 300), y=const(390), pts=[(0, 0), (610, 0)], width=2.4, color=(130, 130, 130),
           prog=Track(0, (42.2, 0, lin), (42.6, 1, out_cubic)), a=life(42.2, 46.85)))
S.add(Text(x=const(X9), y=const(-30), text="PICO", size=90, weight="Black", color=GREEN,
           s=appear(46.0, .35), a=life(46.0, 46.85)), 46.0, "thud")

# ======================================================================
# DEZEMBRO: "E a segunda parcela do 13º chega até 20 de dezembro. Bem na hora do Natal." (47.1–53.1)
# ======================================================================
X10 = 9000
S.add(Text(x=const(X10), y=const(-450), text="DEZEMBRO", size=72, weight="Black", s=appear(47.0, .4),
           a=life(47.0, 53.25)), 47.0)
S.add(Gift(x=const(X10), y=const(-40), w=230, s=appear(47.4, .4), a=life(47.4, 53.25)), 47.4, "thud")
S.add(CoinIcon(x=const(X10 + 175), y=Track(-700, (48.4, -700, lin), (49.0, -170, out_back)), r=40, color=GOLD,
               s=const(1), a=life(48.4, 53.25)), 49.0, "tick")
S.add(Text(x=const(X10 + 175), y=const(-245), text="2ª", size=34, weight="Black", color=GOLD, s=appear(49.2),
           a=life(49.2, 53.25)), 49.2)
P(X10, 260, "2ª PARCELA: ATÉ 20/12", 49.3, 53.25, color=GOLD)
S.add(Rays(x=const(X10), y=const(-90), r=200, n=7, prog=Track(0, (51.5, 0, lin), (51.8, 1, out_back)),
           color=GOLD, a=life(51.5, 53.25), float_amp=0))
P(X10, 360, "NATAL", 51.6, 53.25)

# ======================================================================
# COMPARE: "Então, antes de comprar, veja quanto custava semanas atrás.
#           Às vezes o desconto é só o preço voltando ao normal." (53.5–61.1)
# ======================================================================
X11 = 11000
S.add(Text(x=const(X11), y=const(-470), text="COMPARE", size=86, weight="Black", s=appear(53.5, .4),
           a=life(53.5, 60.95)), 53.5, "thud")
S.add(WarnIcon(x=const(X11), y=const(-350), r=30, color=ORANGE, s=appear(53.9), a=life(53.9, 60.95)), 53.9)
PX = [X11 - 230, X11, X11 + 230]
PY = [150, -60, 150]
S.add(Path(x=const(PX[0]), y=const(PY[0]), pts=[(0, 0), (230, PY[1] - PY[0]), (460, 0)], width=4,
           color=(220, 220, 220), prog=Track(0, (55.0, 0, lin), (57.4, 1, lin)), a=life(55.0, 60.95)), 55.0)
for i, (mon, price, colr, t0) in enumerate([("SETEMBRO", "R$ 100", (255, 255, 255), 54.6),
                                             ("OUTUBRO", "R$ 150", RED, 56.1),
                                             ("BLACK FRIDAY", "R$ 100", GOLD, 57.4)]):
    S.add(Dot(x=const(PX[i]), y=const(PY[i]), r=11, color=colr, s=appear(t0), a=life(t0, 60.95)), t0)
    S.add(Text(x=const(PX[i]), y=const(PY[i] - 60), text=price, size=40, weight="Black", color=colr,
               s=appear(t0, .35), a=life(t0, 60.95)), t0, "pop")
    S.add(Text(x=const(PX[i]), y=const(330), text=mon, size=19, weight="Black", color=colr,
               s=appear(t0), a=life(t0, 60.95)))
S.add(PriceTag(x=const(PX[2] - 10), y=const(-60), w=150, h=72, text="-33%", color=GOLD, sway=4,
               s=appear(57.9), a=life(57.9, 60.95)), 57.9)
S.add(Dashed(x=const(X11), y=const(150), w=460, color=RED, a=life(58.7, 60.95)))
P(X11, 230, "MESMO PREÇO", 58.8, 60.95, color=RED, size=22)

# ======================================================================
# FINAL: "Segue a Guidelight pra entender o jogo do dinheiro." (61.5–64.8)
# ======================================================================
X12 = 13000
P(X12, -390, "SIGA A PÁGINA", 62.3, 66.0, size=22)
S.add(Avatar(x=const(X12), y=const(-150), r=150, path=os.path.join(HERE, "assets", "guidelight.jpg"), ring=GOLD,
             s=appear(61.4, .45), a=life(61.4, 66.0)), 61.4, "thud")
S.add(Text(x=const(X12), y=const(80), text="GUIDELIGHT", size=78, weight="Black", s=appear(61.8, .4),
           a=life(61.8, 66.0)), 61.8)
CLICK = 64.0
S.add(Button(x=const(X12), y=const(210), w=300, h=78, text=lambda t: "SEGUINDO" if t >= CLICK else "SEGUIR",
             fill=lerp_color((255, 255, 255), GOLD, CLICK, CLICK + .15),
             s=Track(0, (62.6, 0, lin), (62.95, 1, out_back), (CLICK - .05, 1, lin), (CLICK + .05, .9, lin),
                     (CLICK + .35, 1, out_back)), a=life(62.6, 66.0)), 62.6)
S.add(Cursor(x=Track(X12 + 300, (63.1, X12 + 300, lin), (63.85, X12 + 30, in_out_cubic)),
             y=Track(560, (63.1, 560, lin), (63.85, 215, in_out_cubic)), size=44,
             s=Track(1, (CLICK - .05, 1, lin), (CLICK + .05, .85, lin), (CLICK + .25, 1, out_cubic)),
             a=life(63.1, 65.4)), CLICK)
S.sfx.append((CLICK + .02, "tick"))
S.add(Rays(x=const(X12), y=const(-150), r=190, n=7, prog=Track(0, (CLICK, 0, lin), (CLICK + .3, 1, out_back)),
           color=GOLD, a=life(CLICK, 66.0), float_amp=0))


def mix(root):
    mix_voice(f"{root}/video_03.mp4", [(os.path.join(HERE, "assets", "voz03", f), t) for f, t in VOZ],
              f"{root}/guidelight_black_friday_13_9x16.mp4")


if __name__ == "__main__":
    root = os.path.join(HERE, "..", "out")
    if "--stills" in sys.argv:
        os.makedirs(f"{root}/stills03", exist_ok=True)
        for t in [2.9, 6.6, 10.5, 15.9, 21.9, 27.6, 33.8, 40.0, 46.4, 52.0, 59.5, 64.5]:
            S.still(t, f"{root}/stills03/t{t:05.1f}.png")
        print("stills ok")
    elif "--mix" in sys.argv:          # só refaz a mixagem da voz (sem renderizar de novo)
        mix(root)
    else:
        S.render(f"{root}/video_03.mp4")
        mix(root)
