"""
Studio C — motor de animação 2D minimalista (estilo "pictograma branco no fundo preto").

Ideia central (tirada da análise do vídeo de referência):
  * Fundo quase preto com vinheta radial (centro levemente mais claro).
  * Linha de chão tracejada atravessando a tela.
  * Tudo é branco: pictograma de pessoa sólido, ícones só com contorno,
    texto em caixa alta bold, "pílulas" (rótulos arredondados) pequenas.
  * Brilho suave (glow) em tudo.
  * Cada fala da narração = 1 "beat" visual novo a cada ~1 a 1,5 s.
  * Movimentos: pop com overshoot, contador de números, câmera que desliza
    para o lado para revelar o próximo elemento, "whip pan" com borrão
    de movimento, elementos que ficam cinza/apagam para mostrar fracasso.

Uso: veja anim/video_01.py. Rodar:  python3 anim/video_01.py
"""
from __future__ import annotations

import math
import os
import subprocess
import wave
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# --------------------------------------------------------------------------
# Easing
# --------------------------------------------------------------------------

def lin(x): return x
def out_cubic(x): return 1 - (1 - x) ** 3
def in_cubic(x): return x ** 3
def in_out_cubic(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def out_back(x, k=1.9):
    c3 = k + 1
    return 1 + c3 * (x - 1) ** 3 + k * (x - 1) ** 2
def out_expo(x): return 1 if x >= 1 else 1 - 2 ** (-10 * x)


class Track:
    """Keyframes: [(tempo, valor, easing_para_chegar_neste_valor), ...]"""

    def __init__(self, v0, *keys):
        self.keys = [(-1e9, v0, lin)] + sorted(keys, key=lambda k: k[0])

    def __call__(self, t):
        ks = self.keys
        if t >= ks[-1][0]:
            return ks[-1][1]
        for (t0, v0, _), (t1, v1, e) in zip(ks, ks[1:]):
            if t0 <= t < t1:
                if t1 - t0 > 1e6:  # segmento inicial infinito
                    return v0
                return v0 + (v1 - v0) * e((t - t0) / (t1 - t0))
        return ks[-1][1]


def const(v):
    return lambda t: v


# --------------------------------------------------------------------------
# Fontes
# --------------------------------------------------------------------------

FONT_DIRS = ["/usr/share/fonts/opentype/inter", os.path.join(os.path.dirname(__file__), "fonts")]
_font_cache: dict = {}


def font(weight: str, size: float):
    size = max(4, int(round(size)))
    key = (weight, size)
    if key not in _font_cache:
        f = None
        for d in FONT_DIRS:
            p = os.path.join(d, f"Inter-{weight}.otf")
            if os.path.exists(p):
                f = ImageFont.truetype(p, size)
                break
        _font_cache[key] = f or ImageFont.load_default(size)
    return _font_cache[key]


# --------------------------------------------------------------------------
# Cena / câmera
# --------------------------------------------------------------------------

@dataclass
class Ctx:
    d: ImageDraw.ImageDraw
    t: float
    W: int
    H: int
    cam: tuple  # (cx, cy, zoom)

    def sx(self, x, y):
        cx, cy, z = self.cam
        return (x - cx) * z + self.W / 2, (y - cy) * z + self.H / 2

    @property
    def z(self):
        return self.cam[2]


@dataclass
class El:
    """Elemento base. x,y em coordenadas de mundo (1 unidade = 1 px a zoom 1)."""
    x: Callable = const(0)
    y: Callable = const(0)
    s: Callable = const(1)      # escala
    a: Callable = const(1)      # opacidade/brilho 0..1
    float_amp: float = 2.0      # flutuação ociosa
    phase: float = 0.0
    color: tuple = (255, 255, 255)  # cor de destaque (padrão: branco)

    def c(self, a):
        return tuple(int(v * a) for v in self.color)

    def state(self, t):
        a = self.a(t)
        y = self.y(t) + math.sin(t * 1.6 + self.phase) * self.float_amp
        return self.x(t), y, self.s(t), max(0.0, min(1.0, a))

    def draw(self, c: Ctx):
        x, y, s, a = self.state(c.t)
        if a <= 0.004 or s <= 0.01:
            return
        X, Y = c.sx(x, y)
        self.paint(c, X, Y, s * c.z, a)

    def paint(self, c, X, Y, k, a):
        raise NotImplementedError


def gray(a):
    v = int(255 * a)
    return (v, v, v)


def appear(t0, dur=.35, s0=0.0, e=out_back):
    """Escala com overshoot (o 'pop' do vídeo)."""
    return Track(s0, (t0, s0, lin), (t0 + dur, 1.0, e))


def fade(t_in, t_out=None, dur=.25, lo=0.0, hi=1.0):
    keys = [(t_in, lo, lin), (t_in + dur, hi, out_cubic)]
    if t_out is not None:
        keys += [(t_out, hi, lin), (t_out + dur, lo, in_cubic)]
    return Track(lo, *keys)


def life(t_in, t_out=None, dim_at=None, dim_to=.3, dur=.25):
    """Opacidade: entra, opcionalmente fica 'apagado' (cinza) e sai."""
    keys = [(t_in, 0, lin), (t_in + dur, 1, out_cubic)]
    if dim_at is not None:
        keys += [(dim_at, 1, lin), (dim_at + .4, dim_to, out_cubic)]
    if t_out is not None:
        last = keys[-1][1]
        keys += [(t_out, last, lin), (t_out + dur, 0, in_cubic)]
    return Track(0, *keys)


# --------------------------------------------------------------------------
# Elementos
# --------------------------------------------------------------------------

@dataclass
class Person(El):
    h: float = 120  # altura total. Pés em y.
    legs: bool = False           # versão com pernas/braços (para andar/correr)
    run: Callable = const(0)     # 0 = parado, 1 = correndo
    gait: float = 9.0            # velocidade da passada

    def paint(self, c, X, Y, k, a):
        if self.legs:
            return self._paint_legs(c, X, Y, k, a)
        h = self.h * k
        col = self.c(a)
        r = h * 0.17
        bw = h * 0.42
        body_top = Y - h * 0.62
        c.d.ellipse([X - r, Y - h, X + r, Y - h + 2 * r], fill=col)
        c.d.rounded_rectangle([X - bw / 2, body_top, X + bw / 2, Y], radius=bw / 2.2, fill=col,
                              corners=(True, True, False, False))


    def _paint_legs(self, c, X, Y, k, a):
        h = self.h * k
        col = self.c(a)
        run = max(0.0, min(1.0, self.run(c.t)))
        ph = c.t * self.gait
        bob = abs(math.sin(ph)) * h * .04 * run
        lean = h * .07 * run
        Y0 = Y - bob
        hip = (X, Y0 - h * .40)
        lw = max(2, int(h * .14))

        def limb(p0, ang, L):
            p1 = (p0[0] + math.sin(ang) * L, p0[1] + math.cos(ang) * L)
            c.d.line([p0, p1], fill=col, width=lw)
            for q in (p0, p1):
                c.d.ellipse([q[0] - lw / 2, q[1] - lw / 2, q[0] + lw / 2, q[1] + lw / 2], fill=col)

        sw = math.sin(ph) * .75 * run
        limb(hip, sw, h * .38)
        limb(hip, -sw, h * .38)
        # tronco
        tw = h * .30
        top = (X + lean, Y0 - h * .74)
        c.d.line([hip, top], fill=col, width=int(tw))
        for q in (hip, top):
            c.d.ellipse([q[0] - tw / 2, q[1] - tw / 2, q[0] + tw / 2, q[1] + tw / 2], fill=col)
        # braços
        sh = (X + lean * .9, Y0 - h * .66)
        limb(sh, -sw * .9 + .15 * run, h * .27)
        limb(sh, sw * .9 + .15 * run, h * .27)
        r = h * .13
        hx, hy = X + lean * 1.25, Y0 - h * .90
        c.d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=col)


@dataclass
class Text(El):
    text: str | Callable = ""
    size: float = 56
    weight: str = "ExtraBold"
    float_amp: float = 1.5

    def paint(self, c, X, Y, k, a):
        txt = self.text(c.t) if callable(self.text) else self.text
        c.d.text((X, Y), txt, font=font(self.weight, self.size * k), fill=self.c(a), anchor="mm")


@dataclass
class Pill(El):
    """Rótulo pequeno em caixa alta com borda arredondada."""
    text: str = ""
    size: float = 15
    float_amp: float = 1.5

    def paint(self, c, X, Y, k, a):
        f = font("Bold", self.size * k)
        sp = self.size * k * 0.12  # letter-spacing
        widths = [f.getlength(ch) for ch in self.text]
        tw = sum(widths) + sp * (len(self.text) - 1)
        ph, pw = self.size * k * 1.9, tw + self.size * k * 2.0
        col = self.c(a)
        c.d.rounded_rectangle([X - pw / 2, Y - ph / 2, X + pw / 2, Y + ph / 2], radius=ph / 2,
                              fill=(0, 0, 0), outline=col, width=max(1, int(2.2 * k)))
        cx = X - tw / 2
        for ch, w in zip(self.text, widths):
            c.d.text((cx, Y), ch, font=f, fill=col, anchor="lm")
            cx += w + sp


def _sw(k, base=3.2):
    return max(1, int(round(base * k)))


@dataclass
class CheckIcon(El):
    r: float = 26

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        col = self.c(a)
        c.d.ellipse([X - r, Y - r, X + r, Y + r], outline=col, width=_sw(k))
        c.d.line([(X - r * .42, Y + r * .02), (X - r * .1, Y + r * .34), (X + r * .45, Y - r * .3)],
                 fill=col, width=_sw(k), joint="curve")


@dataclass
class XIcon(El):
    r: float = 26
    filled: bool = True

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        col = self.c(a)
        c.d.ellipse([X - r, Y - r, X + r, Y + r], outline=col, width=_sw(k),
                    fill=(0, 0, 0) if self.filled else None)
        q = r * .4
        c.d.line([(X - q, Y - q), (X + q, Y + q)], fill=col, width=_sw(k))
        c.d.line([(X - q, Y + q), (X + q, Y - q)], fill=col, width=_sw(k))


@dataclass
class WarnIcon(El):
    r: float = 30

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        col = self.c(a)
        pts = [(X, Y - r), (X + r * 1.1, Y + r * .8), (X - r * 1.1, Y + r * .8)]
        c.d.polygon(pts, outline=col, width=_sw(k))
        c.d.line([(X, Y - r * .3), (X, Y + r * .25)], fill=col, width=_sw(k))
        d = r * .08
        c.d.ellipse([X - d, Y + r * .45 - d, X + d, Y + r * .45 + d], fill=col)


@dataclass
class CoinIcon(El):
    r: float = 22

    def paint(self, c, X, Y, k, a):
        r = self.r * k
        col = self.c(a)
        c.d.ellipse([X - r, Y - r, X + r, Y + r], outline=col, width=_sw(k), fill=(0, 0, 0))
        c.d.ellipse([X - r * .78, Y - r * .78, X + r * .78, Y + r * .78], outline=self.c(a * .6), width=_sw(k, 1.6))
        c.d.text((X, Y), "$", font=font("Bold", r * 1.05), fill=col, anchor="mm")


@dataclass
class CalendarIcon(El):
    w: float = 90
    label: str = "DIA 1"

    def paint(self, c, X, Y, k, a):
        w = self.w * k
        h = w * 1.0
        col = self.c(a)
        x0, y0 = X - w / 2, Y - h / 2
        c.d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=w * .1, outline=col, width=_sw(k), fill=(0, 0, 0))
        c.d.line([(x0, y0 + h * .28), (x0 + w, y0 + h * .28)], fill=col, width=_sw(k))
        for fx in (.3, .7):
            c.d.line([(x0 + w * fx, y0 - h * .08), (x0 + w * fx, y0 + h * .1)], fill=col, width=_sw(k, 4))
        c.d.text((X, y0 + h * .64), self.label, font=font("ExtraBold", w * .2), fill=col, anchor="mm")


@dataclass
class BookIcon(El):
    w: float = 110

    def paint(self, c, X, Y, k, a):
        w = self.w * k
        h = w * .62
        col = self.c(a)
        sw = _sw(k)
        # duas páginas abertas
        c.d.polygon([(X, Y - h * .38), (X - w / 2, Y - h / 2), (X - w / 2, Y + h / 2), (X, Y + h * .38)],
                    outline=col, width=sw, fill=(0, 0, 0))
        c.d.polygon([(X, Y - h * .38), (X + w / 2, Y - h / 2), (X + w / 2, Y + h / 2), (X, Y + h * .38)],
                    outline=col, width=sw, fill=(0, 0, 0))
        for i in range(3):
            yy = Y - h * .18 + i * h * .18
            c.d.line([(X - w * .38, yy - h * .03), (X - w * .1, yy)], fill=self.c(a * .6), width=_sw(k, 2.4))
            c.d.line([(X + w * .1, yy), (X + w * .38, yy - h * .03)], fill=self.c(a * .6), width=_sw(k, 2.4))


@dataclass
class Box(El):
    """Caixa contornada com texto no meio (ex.: 'SISTEMA')."""
    w: float = 170
    h: float = 170
    label: str = ""
    size: float = 22

    def paint(self, c, X, Y, k, a):
        w, h = self.w * k, self.h * k
        col = self.c(a)
        c.d.rounded_rectangle([X - w / 2, Y - h / 2, X + w / 2, Y + h / 2], radius=8 * k, outline=col,
                              width=_sw(k), fill=(0, 0, 0))
        if self.label:
            c.d.text((X, Y), self.label, font=font("ExtraBold", self.size * k), fill=col, anchor="mm")


@dataclass
class ListBox(El):
    """Painel 'O QUE ELE TEM' com itens que aparecem um a um."""
    title: str = ""
    items: list = field(default_factory=list)  # [(texto, t_aparece, ok:bool)]
    w: float = 300
    ok_color: tuple = (255, 255, 255)
    bad_color: tuple = (255, 255, 255)

    def paint(self, c, X, Y, k, a):
        w = self.w * k
        row = 46 * k
        head = 34 * k
        n = max(1, sum(1 for _, ti, _ in self.items if c.t >= ti))
        # altura cresce suavemente conforme os itens entram
        grow = 0.0
        for _, ti, _ in self.items:
            grow += out_cubic(min(1, max(0, (c.t - ti) / .25)))
        h = head + row * max(1, grow) + 14 * k
        x0, y0 = X - w / 2, Y - (head + row * 1.5) / 2
        col = self.c(a)
        c.d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=8 * k, outline=col, width=_sw(k), fill=(0, 0, 0))
        c.d.line([(x0, y0 + head), (x0 + w, y0 + head)], fill=self.c(a * .55), width=_sw(k, 2))
        c.d.text((X, y0 + head / 2), self.title, font=font("Bold", 12 * k), fill=self.c(a * .7), anchor="mm")
        for i, (txt, ti, ok) in enumerate(self.items):
            p = (c.t - ti) / .3
            if p <= 0:
                continue
            p = min(1, p)
            ia = a * out_cubic(p)
            yy = y0 + head + row * (i + .5) + 6 * k
            dx = (1 - out_cubic(p)) * -20 * k
            c.d.text((x0 + 20 * k + dx, yy), txt, font=font("ExtraBold", 19 * k), fill=self.c(ia), anchor="lm")
            icon_s = out_back(p)
            Icon = CheckIcon if ok else XIcon
            ic = Icon(r=12, color=self.ok_color if ok else self.bad_color)
            ic.paint(c, x0 + w - 30 * k, yy, k * icon_s, ia)


@dataclass
class Path(El):
    """Linha desenhada progressivamente (gráfico, seta...). pts em coords relativas."""
    pts: list = field(default_factory=list)
    prog: Callable = const(1)
    width: float = 3.5
    tip: El | None = None  # elemento que viaja na ponta
    float_amp: float = 0
    arrow: bool = False

    def paint(self, c, X, Y, k, a):
        p = max(0, min(1, self.prog(c.t)))
        if p <= 0 or len(self.pts) < 2:
            return
        pts = [(X + px * k, Y + py * k) for px, py in self.pts]
        seg = [math.dist(p0, p1) for p0, p1 in zip(pts, pts[1:])]
        total = sum(seg) * p
        out = [pts[0]]
        for (p0, p1), L in zip(zip(pts, pts[1:]), seg):
            if total <= 0:
                break
            if L <= total:
                out.append(p1)
            else:
                f = total / L
                out.append((p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f))
            total -= L
        c.d.line(out, fill=self.c(a), width=_sw(k, self.width), joint="curve")
        if self.arrow and len(out) >= 2:
            (x0, y0), (x1, y1) = out[-2], out[-1]
            ang = math.atan2(y1 - y0, x1 - x0)
            L = 16 * k
            for da in (2.6, -2.6):
                c.d.line([(x1, y1), (x1 + math.cos(ang + da) * L, y1 + math.sin(ang + da) * L)],
                         fill=self.c(a), width=_sw(k, self.width))
        if self.tip is not None:
            self.tip.paint(c, out[-1][0], out[-1][1], k * self.tip.s(c.t), a)


@dataclass
class Rays(El):
    """Risquinhos de 'atenção/brilho' em volta de algo (como no celular do vídeo)."""
    r: float = 80
    n: int = 5
    prog: Callable = const(1)

    def paint(self, c, X, Y, k, a):
        p = max(0, min(1, self.prog(c.t)))
        wob = 1 + .06 * math.sin(c.t * 9)
        for i in range(self.n):
            ang = math.radians(-160 + i * (140 / (self.n - 1)))
            r0 = self.r * k * wob
            r1 = r0 + 26 * k * p
            c.d.line([(X + math.cos(ang) * r0, Y + math.sin(ang) * r0),
                      (X + math.cos(ang) * r1, Y + math.sin(ang) * r1)], fill=self.c(a), width=_sw(k))


@dataclass
class Avatar(El):
    """Foto redonda com anel (foto de perfil)."""
    path: str = ""
    r: float = 90
    ring: tuple = (255, 255, 255)
    _img: object = None

    def paint(self, c, X, Y, k, a):
        if self._img is None:
            self._img = Image.open(self.path).convert("RGB")
            w, h = self._img.size
            m = min(w, h)
            self._img = self._img.crop(((w - m) // 2, (h - m) // 2, (w + m) // 2, (h + m) // 2))
        r = int(self.r * k)
        if r < 2:
            return
        im = self._img.resize((2 * r, 2 * r), Image.LANCZOS)
        mask = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=int(255 * a))
        c.d._image.paste(im, (int(X - r), int(Y - r)), mask)
        rw = _sw(k, 5)
        col = tuple(int(v * a) for v in self.ring)
        c.d.ellipse([X - r - rw, Y - r - rw, X + r + rw, Y + r + rw], outline=col, width=rw)


@dataclass
class Button(El):
    """Botão colorido sólido (ex.: SEGUIR) com texto que pode mudar."""
    text: str | Callable = ""
    w: float = 220
    h: float = 60
    fill: Callable = const((255, 255, 255))
    text_color: tuple = (0, 0, 0)
    float_amp: float = 1.0

    def paint(self, c, X, Y, k, a):
        w, h = self.w * k, self.h * k
        f = self.fill(c.t)
        c.d.rounded_rectangle([X - w / 2, Y - h / 2, X + w / 2, Y + h / 2], radius=h / 2,
                              fill=tuple(int(v * a) for v in f))
        txt = self.text(c.t) if callable(self.text) else self.text
        c.d.text((X, Y), txt, font=font("ExtraBold", h * .38),
                 fill=tuple(int(v * a) for v in self.text_color), anchor="mm")


@dataclass
class Cursor(El):
    """Mãozinha/seta de clique."""
    size: float = 34
    float_amp: float = 0

    def paint(self, c, X, Y, k, a):
        L = self.size * k
        pts = [(X, Y), (X, Y + L), (X + L * .28, Y + L * .74), (X + L * .46, Y + L * 1.1),
               (X + L * .6, Y + L * 1.03), (X + L * .43, Y + L * .68), (X + L * .78, Y + L * .68)]
        c.d.polygon(pts, fill=self.c(a), outline=(0, 0, 0), width=_sw(k, 2))


def lerp_color(c0, c1, t0, t1):
    def f(t):
        p = max(0, min(1, (t - t0) / max(1e-6, t1 - t0)))
        return tuple(int(x + (y - x) * p) for x, y in zip(c0, c1))
    return f


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------

@dataclass
class Scene:
    W: int = 1280
    H: int = 720
    fps: int = 30
    duration: float = 10
    els: list = field(default_factory=list)
    cam_x: Callable = const(0)
    cam_y: Callable = const(0)
    zoom: Callable = const(1)
    ground_y: float = 120          # y do chão (mundo)
    ground_a: Callable = const(1)
    sfx: list = field(default_factory=list)  # [(t, 'pop'|'whoosh'|'tick'|'thud')]
    glow: float = 0.55
    invert: Callable = const(0)   # 0..1 — inverte preto/branco (fundo branco)
    base_w: int = 1280            # largura de referência das coordenadas de mundo

    def add(self, el, sfx_at=None, kind="pop"):
        self.els.append(el)
        if sfx_at is not None:
            self.sfx.append((sfx_at, kind))
        return el

    # ---- fundo com vinheta (pré-calculado) ----
    def _bg(self):
        yy, xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
        d = np.sqrt(((xx - self.W / 2) / (self.W * .55)) ** 2 + ((yy - self.H / 2) / (self.H * .6)) ** 2)
        v = 30 - 22 * np.clip(d, 0, 1) ** 1.4
        return np.repeat(v[..., None], 3, axis=2)

    def _ground(self, d, t, cam):
        a = self.ground_a(t)
        if a <= 0:
            return
        cx, cy, z = cam
        Y = (self.ground_y - cy) * z + self.H / 2
        dash, gap = 7 * z, 6 * z
        off = (-cx * z) % (dash + gap)
        x = -dash + off
        col = gray(.35 * a)
        while x < self.W:
            d.line([(x, Y), (x + dash, Y)], fill=col, width=max(1, int(2 * z)))
            x += dash + gap

    def frame(self, t, bg):
        k = self.W / self.base_w
        cam = (self.cam_x(t), self.cam_y(t), self.zoom(t) * k)
        layer = Image.new("RGB", (self.W, self.H), (0, 0, 0))
        d = ImageDraw.Draw(layer)
        self._ground(d, t, cam)
        c = Ctx(d, t, self.W, self.H, cam)
        for el in self.els:
            el.draw(c)
        L = np.asarray(layer, dtype=np.float32)
        G = np.asarray(layer.filter(ImageFilter.GaussianBlur(9 * k)), dtype=np.float32)
        out = bg + L + G * self.glow
        # whip pan: borrão na direção do movimento da câmera (derivada central, ignora cortes secos)
        eps = 0.004
        vx = abs(self.cam_x(t + eps) - self.cam_x(t - eps)) / (2 * eps) / self.fps * self.zoom(t)
        vy = abs(self.cam_y(t + eps) - self.cam_y(t - eps)) / (2 * eps) / self.fps * self.zoom(t)
        # saltos enormes de um quadro para o outro são cortes secos, não movimento: sem borrão
        if 30 < vx < 600:
            n = max(2, int(min(140, vx * 1.6) * k))
            cs = np.cumsum(np.pad(out, ((0, 0), (n, 0), (0, 0)), mode="edge"), axis=1)
            out = (cs[:, n:] - cs[:, :-n]) / n
            rng = np.random.default_rng(int(t * 1000))
            for _ in range(10):
                y = rng.integers(0, self.H)
                out[y:y + rng.integers(2, 9)] += rng.uniform(20, 70)
        if 30 < vy < 600:
            n = max(2, int(min(140, vy * 1.2) * k))
            cs = np.cumsum(np.pad(out, ((n, 0), (0, 0), (0, 0)), mode="edge"), axis=0)
            out = (cs[n:] - cs[:-n]) / n
        inv = self.invert(t)
        if inv > 0:
            out = np.clip(out, 0, 255)
            out = out * (1 - inv) + (255 - out) * inv
        # grão de filme bem leve
        out += np.random.default_rng(int(t * 997)).normal(0, 2.2, out.shape[:2])[..., None]
        return np.clip(out, 0, 255).astype(np.uint8)

    def render(self, path, audio=True, preview_png=None):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        bg = self._bg()
        n = int(self.duration * self.fps)
        wav = path.rsplit(".", 1)[0] + "_sfx.wav"
        if audio:
            self._sfx_wav(wav)
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{self.W}x{self.H}", "-r", str(self.fps), "-i", "-"]
        if audio:
            cmd += ["-i", wav, "-c:a", "aac", "-b:a", "160k", "-shortest"]
        cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", path]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(n):
            t = i / self.fps
            f = self.frame(t, bg)
            proc.stdin.write(f.tobytes())
            if i % (self.fps * 5) == 0:
                print(f"  {t:5.1f}s / {self.duration:.0f}s", flush=True)
        proc.stdin.close()
        proc.wait()
        if audio and os.path.exists(wav):
            os.remove(wav)
        print("ok ->", path)

    def still(self, t, path):
        Image.fromarray(self.frame(t, self._bg())).save(path)

    # ---- efeitos sonoros sintetizados (pop / whoosh / tick / thud) ----
    def _sfx_wav(self, path, sr=44100):
        n = int(self.duration * sr)
        buf = np.zeros(n, np.float32)
        rng = np.random.default_rng(7)
        for t, kind in self.sfx:
            i0 = int(t * sr)
            if kind == "pop":
                L = int(.09 * sr); tt = np.arange(L) / sr
                f = 520 * np.exp(-tt * 18) + 380
                s = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 40) * .35
            elif kind == "tick":
                L = int(.03 * sr); tt = np.arange(L) / sr
                s = np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 160) * .18
            elif kind == "thud":
                L = int(.35 * sr); tt = np.arange(L) / sr
                s = np.sin(2 * np.pi * (90 * np.exp(-tt * 6) + 45) * tt) * np.exp(-tt * 9) * .6
            elif kind == "whoosh":
                L = int(.45 * sr); tt = np.arange(L) / sr
                noise = rng.normal(0, 1, L)
                k = 60
                noise = np.convolve(noise, np.ones(k) / k, mode="same") * 6
                env = np.sin(np.pi * tt / tt[-1]) ** 2
                s = noise * env * .5
            else:
                continue
            i1 = min(n, i0 + len(s))
            if i0 < n:
                buf[i0:i1] += s[: i1 - i0]
        # cama sonora: drone grave bem baixinho
        tt = np.arange(n) / sr
        buf += (np.sin(2 * np.pi * 55 * tt) * .03 + np.sin(2 * np.pi * 82.4 * tt) * .02) * \
            np.clip(tt / 1.5, 0, 1) * np.clip((self.duration - tt) / 1.5, 0, 1)
        buf = np.clip(buf, -1, 1)
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((buf * 32767).astype(np.int16).tobytes())


def mix_voice(video, clips, out, sfx_vol=0.45, voice_vol=1.0):
    """Junta a narração (lista de (arquivo, início_em_s)) ao vídeo, com os efeitos mais baixos."""
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", video]
    for f, _ in clips:
        cmd += ["-i", f]
    parts = [f"[0:a]volume={sfx_vol}[sfx]"]
    labels = ["[sfx]"]
    for i, (_, t) in enumerate(clips, start=1):
        ms = int(t * 1000)
        parts.append(f"[{i}:a]aresample=44100,volume={voice_vol},adelay={ms}|{ms}[v{i}]")
        labels.append(f"[v{i}]")
    parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,"
                 "alimiter=limit=0.95[a]")
    cmd += ["-filter_complex", ";".join(parts), "-map", "0:v", "-map", "[a]",
            "-c:v", "libx264", "-crf", "22", "-preset", "slow", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("ok ->", out)
