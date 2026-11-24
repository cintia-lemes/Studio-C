// Studio-C · motor de animação "neon minimalista" (canvas 2D, 1080x1920)
// Roda no navegador (Chromium via Playwright). Cada vídeo define window.VIDEO = { groups:[...] }
// e o motor desenha qualquer instante t com renderFrame(t) — determinístico, frame a frame.
(function () {
  const W = 1080, H = 1920;
  const WHITE = '255,255,255';
  const GREY = '150,150,150';

  // ---------- easing / util ----------
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const easeOut = t => 1 - Math.pow(1 - clamp(t), 3);
  const easeInOut = t => { t = clamp(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  const easeBack = t => { t = clamp(t); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };

  // ---------- estilo ----------
  function glow(ctx, draw, k = 1) {
    // brilho: 2 passadas com sombra branca desfocada + traço nítido
    ctx.save();
    ctx.shadowColor = `rgba(${WHITE},0.85)`;
    ctx.shadowBlur = 38 * k; draw();
    ctx.shadowBlur = 12 * k; draw();
    ctx.restore();
  }
  function rgba(c, a) { return `rgba(${c},${a})`; }
  function withAlpha(ctx, a, fn) { if (a <= 0.001) return; ctx.save(); ctx.globalAlpha *= clamp(a); fn(); ctx.restore(); }
  function popTransform(ctx, x, y, s) { ctx.translate(x, y); ctx.scale(s, s); ctx.translate(-x, -y); }

  // ---------- fundo ----------
  let dotGrid = null;
  function background(ctx, t) {
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
    const pulse = 0.075 + 0.01 * Math.sin(t * 0.8);
    const g = ctx.createRadialGradient(W / 2, 1000, 0, W / 2, 1000, 950);
    g.addColorStop(0, rgba(WHITE, pulse)); g.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    if (!dotGrid) {
      dotGrid = document.createElement('canvas'); dotGrid.width = W; dotGrid.height = H;
      const d = dotGrid.getContext('2d'); d.fillStyle = rgba(WHITE, 0.05);
      for (let y = 20; y < H; y += 44) for (let x = 20; x < W; x += 44) { d.beginPath(); d.arc(x, y, 1.6, 0, 7); d.fill(); }
    }
    ctx.drawImage(dotGrid, 0, 0);
  }

  // ---------- texto ----------
  function text(ctx, str, x, y, o = {}) {
    const { size = 40, weight = 900, color = WHITE, alpha = 1, align = 'center', spacing = 0, glowK = 0.5, base = 'middle' } = o;
    withAlpha(ctx, alpha, () => {
      ctx.font = `${weight} ${size}px Inter`;
      ctx.letterSpacing = `${spacing}px`;
      ctx.textAlign = align; ctx.textBaseline = base;
      ctx.fillStyle = rgba(color, 1);
      if (glowK > 0) glow(ctx, () => ctx.fillText(str, x, y), glowK); else ctx.fillText(str, x, y);
    });
  }
  function typed(str, p) { // efeito máquina de escrever
    const n = Math.floor(clamp(p) * str.length + 0.0001);
    return str.slice(0, n);
  }

  // ---------- formas ----------
  function polyLen(pts) { let L = 0; for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return L; }
  function partial(pts, p) { // recorta a polilinha até a fração p do comprimento
    p = clamp(p); if (p >= 1) return pts; if (p <= 0) return [pts[0]];
    const L = polyLen(pts) * p; const out = [pts[0]]; let acc = 0;
    for (let i = 1; i < pts.length; i++) {
      const seg = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
      if (acc + seg >= L) { const k = (L - acc) / seg; out.push([lerp(pts[i - 1][0], pts[i][0], k), lerp(pts[i - 1][1], pts[i][1], k)]); return out; }
      acc += seg; out.push(pts[i]);
    }
    return out;
  }
  function stroke(ctx, pts, o = {}) {
    const { p = 1, width = 6, color = WHITE, alpha = 1, dash = null, glowK = 1, dot = false } = o;
    if (p <= 0) return;
    const q = partial(pts, p);
    withAlpha(ctx, alpha, () => {
      ctx.lineWidth = width; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.strokeStyle = rgba(color, 1); ctx.setLineDash(dash || []);
      const draw = () => { ctx.beginPath(); ctx.moveTo(q[0][0], q[0][1]); for (let i = 1; i < q.length; i++) ctx.lineTo(q[i][0], q[i][1]); ctx.stroke(); };
      glowK > 0 ? glow(ctx, draw, glowK) : draw();
      ctx.setLineDash([]);
      if (dot) { const e = q[q.length - 1]; ctx.fillStyle = rgba(color, 1); glow(ctx, () => { ctx.beginPath(); ctx.arc(e[0], e[1], width * 1.8, 0, 7); ctx.fill(); }); }
    });
    return q[q.length - 1];
  }
  function curve(fn, n = 80) { const pts = []; for (let i = 0; i <= n; i++) pts.push(fn(i / n)); return pts; }
  function arcPts(cx, cy, r, a0, a1, n = 60) { return curve(t => [cx + r * Math.cos(lerp(a0, a1, t)), cy + r * Math.sin(lerp(a0, a1, t))], n); }
  function rrect(ctx, x, y, w, h, r) {
    const rr = Array.isArray(r) ? r : [r, r, r, r];
    ctx.beginPath(); ctx.roundRect(x, y, w, h, rr);
  }
  function shape(ctx, path, o = {}) { // path(ctx) desenha o caminho; fill/stroke com brilho
    const { fill = false, color = WHITE, alpha = 1, width = 6, glowK = 1 } = o;
    withAlpha(ctx, alpha, () => {
      ctx.lineWidth = width; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.strokeStyle = rgba(color, 1); ctx.fillStyle = rgba(color, 1);
      const d = () => { path(ctx); fill ? ctx.fill() : ctx.stroke(); };
      glowK > 0 ? glow(ctx, d, glowK) : d();
    });
  }

  // ---------- personagens / elementos ----------
  // boneco sem rosto: x = centro, y = pés
  function person(ctx, x, y, o = {}) {
    const { s = 1, alpha = 1, dim = 0, pop = 1 } = o;
    if (pop <= 0) return;
    const sc = s * lerp(0.6, 1, easeBack(pop));
    const col = dim > 0 ? `${Math.round(lerp(255, 110, dim))},${Math.round(lerp(255, 110, dim))},${Math.round(lerp(255, 110, dim))}` : WHITE;
    withAlpha(ctx, alpha * clamp(pop * 2), () => {
      ctx.save();
      if (dim > 0) ctx.filter = `blur(${(dim * 2.5).toFixed(1)}px)`;
      ctx.translate(x, y); ctx.scale(sc, sc);
      shape(ctx, c => { rrect(c, -40, -112, 80, 112, [40, 40, 8, 8]); }, { fill: true, color: col, glowK: 1 - dim * 0.7 });
      shape(ctx, c => { c.beginPath(); c.arc(0, -150, 28, 0, 7); }, { fill: true, color: col, glowK: 1 - dim * 0.7 });
      ctx.restore();
    });
  }

  function pill(ctx, str, x, y, o = {}) {
    const { p = 1, filled = true, size = 34, alpha = 1 } = o;
    if (p <= 0) return;
    ctx.save();
    popTransform(ctx, x, y, lerp(0.5, 1, easeBack(p)));
    withAlpha(ctx, alpha * clamp(p * 3), () => {
      ctx.font = `900 ${size}px Inter`; ctx.letterSpacing = '3px';
      const w = ctx.measureText(str).width + size * 1.3, h = size * 1.9;
      shape(ctx, c => rrect(c, x - w / 2, y - h / 2, w, h, h / 2), { fill: filled, width: 5 });
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillStyle = filled ? '#000' : '#fff';
      ctx.fillText(str, x, y + 2);
    });
    ctx.restore();
  }

  function ground(ctx, y, p = 1, alpha = 0.7) {
    if (p <= 0) return;
    const half = W / 2 * easeOut(p) + 2;
    stroke(ctx, [[W / 2 - half, y], [W / 2 + half, y]], { width: 3, alpha, glowK: 0.4 });
  }

  function arrow(ctx, x1, y1, x2, y2, o = {}) {
    const { p = 1, width = 6, head = 22, alpha = 1, color = WHITE } = o;
    if (p <= 0) return;
    const e = stroke(ctx, [[x1, y1], [x2, y2]], { p: easeOut(p), width, alpha, color });
    if (p > 0.6) {
      const a = Math.atan2(y2 - y1, x2 - x1), k = clamp((p - 0.6) / 0.4);
      stroke(ctx, [[e[0] - head * Math.cos(a - 0.6), e[1] - head * Math.sin(a - 0.6)], e, [e[0] - head * Math.cos(a + 0.6), e[1] - head * Math.sin(a + 0.6)]], { width, alpha: alpha * k, color });
    }
  }

  function xmark(ctx, x, y, r, p) { // ⊗
    if (p <= 0) return;
    ctx.save(); popTransform(ctx, x, y, lerp(0.3, 1, easeBack(p)));
    withAlpha(ctx, clamp(p * 3), () => {
      shape(ctx, c => { c.beginPath(); c.arc(x, y, r, 0, 7); }, { width: 5 });
      const k = r * 0.45;
      stroke(ctx, [[x - k, y - k], [x + k, y + k]], { width: 5 });
      stroke(ctx, [[x + k, y - k], [x - k, y + k]], { width: 5 });
    });
    ctx.restore();
  }
  function check(ctx, x, y, r, p) {
    if (p <= 0) return;
    shape(ctx, c => { c.beginPath(); c.arc(x, y, r, 0, 7); }, { width: 5, alpha: clamp(p * 3) });
    stroke(ctx, [[x - r * 0.45, y], [x - r * 0.1, y + r * 0.35], [x + r * 0.5, y - r * 0.35]], { width: 6, p: clamp(p * 1.5 - 0.3) });
  }

  // ---------- ícones (line art), centrados em (x,y), escala s ----------
  const icons = {
    coin(ctx, x, y, s = 1, o = {}) {
      const r = 100 * s;
      shape(ctx, c => { c.beginPath(); c.arc(x, y, r, 0, 7); }, { width: 8 * s, ...o });
      shape(ctx, c => { c.beginPath(); c.arc(x, y, r * 0.78, 0, 7); }, { width: 3 * s, alpha: 0.5 * (o.alpha ?? 1), glowK: 0.4 });
      text(ctx, '$', x, y + 6 * s, { size: 120 * s, alpha: o.alpha ?? 1, glowK: 0.8 });
    },
    phone(ctx, x, y, s = 1, o = {}) {
      shape(ctx, c => rrect(c, x - 55 * s, y - 100 * s, 110 * s, 200 * s, 20 * s), { width: 6 * s, ...o });
      stroke(ctx, [[x - 15 * s, y - 82 * s], [x + 15 * s, y - 82 * s]], { width: 5 * s, alpha: o.alpha ?? 1 });
      shape(ctx, c => { c.beginPath(); c.arc(x, y + 78 * s, 7 * s, 0, 7); }, { width: 4 * s, ...o });
    },
    pump(ctx, x, y, s = 1, o = {}) { // bomba de gasolina
      shape(ctx, c => rrect(c, x - 60 * s, y - 90 * s, 90 * s, 180 * s, 12 * s), { width: 6 * s, ...o });
      shape(ctx, c => rrect(c, x - 42 * s, y - 70 * s, 54 * s, 45 * s, 6 * s), { width: 5 * s, ...o });
      stroke(ctx, [[x + 30 * s, y - 50 * s], [x + 62 * s, y - 30 * s], [x + 62 * s, y + 40 * s], [x + 48 * s, y + 52 * s]], { width: 6 * s, alpha: o.alpha ?? 1 });
      stroke(ctx, [[x - 75 * s, y + 90 * s], [x + 45 * s, y + 90 * s]], { width: 6 * s, alpha: o.alpha ?? 1 });
    },
    bread(ctx, x, y, s = 1, o = {}) {
      shape(ctx, c => { c.beginPath(); c.ellipse(x, y, 100 * s, 55 * s, 0, 0, 7); }, { width: 6 * s, ...o });
      for (const dx of [-45, 0, 45]) stroke(ctx, [[x + dx * s - 14 * s, y + 20 * s], [x + dx * s + 14 * s, y - 20 * s]], { width: 5 * s, alpha: o.alpha ?? 1 });
    },
    cart(ctx, x, y, s = 1, o = {}) {
      stroke(ctx, [[x - 110 * s, y - 70 * s], [x - 80 * s, y - 70 * s], [x - 50 * s, y + 30 * s], [x + 70 * s, y + 30 * s], [x + 95 * s, y - 45 * s], [x - 70 * s, y - 45 * s]], { width: 7 * s, alpha: o.alpha ?? 1 });
      for (const dx of [-35, 55]) shape(ctx, c => { c.beginPath(); c.arc(x + dx * s, y + 62 * s, 14 * s, 0, 7); }, { width: 6 * s, ...o });
    },
    sofa(ctx, x, y, s = 1, o = {}) { // y = chão
      const a = o.alpha ?? 1;
      shape(ctx, c => rrect(c, x - 150 * s, y - 150 * s, 300 * s, 80 * s, 18 * s), { width: 6 * s, alpha: a });
      shape(ctx, c => rrect(c, x - 150 * s, y - 75 * s, 300 * s, 55 * s, 10 * s), { width: 6 * s, alpha: a });
      shape(ctx, c => rrect(c, x - 185 * s, y - 115 * s, 40 * s, 100 * s, 16 * s), { width: 6 * s, alpha: a });
      shape(ctx, c => rrect(c, x + 145 * s, y - 115 * s, 40 * s, 100 * s, 16 * s), { width: 6 * s, alpha: a });
      stroke(ctx, [[x - 150 * s, y - 15 * s], [x - 150 * s, y]], { width: 6 * s, alpha: a });
      stroke(ctx, [[x + 150 * s, y - 15 * s], [x + 150 * s, y]], { width: 6 * s, alpha: a });
    },
    shield(ctx, x, y, s = 1, o = {}) {
      const pts = [[x, y - 130 * s], [x + 105 * s, y - 90 * s], [x + 100 * s, y + 10 * s], [x + 60 * s, y + 85 * s], [x, y + 130 * s], [x - 60 * s, y + 85 * s], [x - 100 * s, y + 10 * s], [x - 105 * s, y - 90 * s], [x, y - 130 * s]];
      stroke(ctx, pts, { width: 8 * s, p: o.p ?? 1, alpha: o.alpha ?? 1 });
    },
    bulb(ctx, x, y, s = 1, o = {}) {
      const a = o.alpha ?? 1;
      stroke(ctx, arcPts(x, y - 20 * s, 75 * s, Math.PI * 0.78, Math.PI * 2.22), { width: 7 * s, alpha: a });
      stroke(ctx, [[x - 38 * s, y + 42 * s], [x - 38 * s, y + 75 * s], [x + 38 * s, y + 75 * s], [x + 38 * s, y + 42 * s]], { width: 7 * s, alpha: a });
      stroke(ctx, [[x - 28 * s, y + 98 * s], [x + 28 * s, y + 98 * s]], { width: 7 * s, alpha: a });
      stroke(ctx, [[x - 25 * s, y + 10 * s], [x, y - 20 * s], [x + 25 * s, y + 10 * s]], { width: 6 * s, alpha: a });
      if (o.rays) for (const ang of [-150, -115, -90, -65, -30]) {
        const r1 = 105 * s, r2 = 135 * s, A = ang * Math.PI / 180;
        stroke(ctx, [[x + r1 * Math.cos(A), y - 20 * s + r1 * Math.sin(A)], [x + r2 * Math.cos(A), y - 20 * s + r2 * Math.sin(A)]], { width: 6 * s, alpha: a * o.rays });
      }
    },
    globe(ctx, x, y, s = 1, o = {}) {
      const r = 95 * s, a = o.alpha ?? 1;
      shape(ctx, c => { c.beginPath(); c.arc(x, y, r, 0, 7); }, { width: 7 * s, alpha: a });
      shape(ctx, c => { c.beginPath(); c.ellipse(x, y, r * 0.45, r, 0, 0, 7); }, { width: 5 * s, alpha: a * 0.8, glowK: 0.5 });
      stroke(ctx, [[x - r, y], [x + r, y]], { width: 5 * s, alpha: a * 0.8, glowK: 0.5 });
      stroke(ctx, curve(t => [x + r * 0.87 * Math.cos(Math.PI * (1 + t)), y - r * 0.5 + 10 * s * Math.sin(Math.PI * t)]), { width: 4 * s, alpha: a * 0.6, glowK: 0.4 });
      stroke(ctx, curve(t => [x + r * 0.87 * Math.cos(Math.PI * (1 + t)), y + r * 0.5 + 10 * s * Math.sin(Math.PI * t)]), { width: 4 * s, alpha: a * 0.6, glowK: 0.4 });
    },
  };
  icons.card = function (ctx, x, y, s = 1, o = {}) { // cartão de crédito
    const a = o.alpha ?? 1, w = 300 * s, h = 190 * s;
    shape(ctx, c => rrect(c, x - w / 2, y - h / 2, w, h, 22 * s), { width: 7 * s, alpha: a });
    stroke(ctx, [[x - w / 2, y - h / 2 + 50 * s], [x + w / 2, y - h / 2 + 50 * s]], { width: 14 * s, alpha: a * 0.8, glowK: 0.5 });
    shape(ctx, c => rrect(c, x - w / 2 + 30 * s, y - 5 * s, 50 * s, 38 * s, 6 * s), { width: 4 * s, alpha: a });
    stroke(ctx, [[x - w / 2 + 30 * s, y + 60 * s], [x + 20 * s, y + 60 * s]], { width: 6 * s, alpha: a * 0.6, glowK: 0.3 });
  };
  icons.bank = function (ctx, x, y, s = 1, o = {}) {
    const a = o.alpha ?? 1;
    stroke(ctx, [[x - 120 * s, y - 50 * s], [x, y - 120 * s], [x + 120 * s, y - 50 * s], [x - 120 * s, y - 50 * s]], { width: 7 * s, alpha: a });
    for (const dx of [-80, -27, 27, 80]) stroke(ctx, [[x + dx * s, y - 30 * s], [x + dx * s, y + 60 * s]], { width: 8 * s, alpha: a });
    stroke(ctx, [[x - 125 * s, y + 85 * s], [x + 125 * s, y + 85 * s]], { width: 8 * s, alpha: a });
  };

  // CTA final padrão: celular com perfil + botão SEGUIR tocado (frase bi)
  function cta(ctx, T, bi) {
    const p = T.lin(bi, 0.5);
    const x = 540, y = 1020, w = 470, h = 820;
    withAlpha(ctx, p, () => {
      shape(ctx, c => rrect(c, x - w / 2, y - h / 2, w, h, 56), { width: 7 });
      stroke(ctx, [[x - 40, y - h / 2 + 34], [x + 40, y - h / 2 + 34]], { width: 6 });
      shape(ctx, c => { c.beginPath(); c.arc(x, y - 190, 95, 0, 7); }, { width: 6 });
      ctx.save(); ctx.beginPath(); ctx.arc(x, y - 190, 92, 0, 7); ctx.clip();
      person(ctx, x, y - 95, { s: 0.85 });
      ctx.restore();
      stroke(ctx, [[x - 120, y - 40], [x + 120, y - 40]], { width: 14, alpha: 0.8 });
      stroke(ctx, [[x - 80, y + 5], [x + 80, y + 5]], { width: 10, alpha: 0.4, glowK: 0 });
      for (let i = 0; i < 3; i++) for (let j = 0; j < 2; j++)
        shape(ctx, c => rrect(c, x - 190 + i * 130, y + 165 + j * 120, 115, 105, 12), { width: 3, alpha: 0.35, glowK: 0 });
    });
    const tap = T.lin(bi, 0.15, 1.3), done = tap >= 1;
    const bs = 1 - 0.08 * Math.sin(Math.PI * tap);
    ctx.save(); popTransform(ctx, x, y + 95, bs * lerp(0.5, 1, easeBack(T.lin(bi, 0.4, 0.4))));
    withAlpha(ctx, T.ap(bi, 0.3, 0.4), () => {
      shape(ctx, c => rrect(c, x - 150, y + 60, 300, 72, 36), { fill: !done, width: 5, glowK: 1.2 });
      ctx.font = '900 32px Inter'; ctx.letterSpacing = '4px'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillStyle = done ? '#fff' : '#000';
      ctx.fillText(done ? 'SEGUINDO ✓' : 'SEGUIR', x, y + 98);
    });
    ctx.restore();
    finger(ctx, T, bi, x + 330, y + 400, x + 40, y + 120, 0.6, 1.3);
  }
  // dedo que desliza até (x1,y1) e toca no instante tapAt (s após o início da frase)
  function finger(ctx, T, bi, x0, y0, x1, y1, delay, tapAt) {
    const fp = T.io(bi, tapAt - delay, delay), fx = lerp(x0, x1, fp), fy = lerp(y0, y1, fp);
    const tap = T.lin(bi, 0.3, tapAt);
    withAlpha(ctx, T.ap(bi, 0.3, delay) * (1 - T.ap(bi, 0.4, tapAt + 0.5)), () => {
      shape(ctx, c => { c.beginPath(); c.arc(fx, fy, 30, 0, 7); }, { width: 5 });
      if (tap > 0 && tap < 1) shape(ctx, c => { c.beginPath(); c.arc(fx, fy, 30 + 60 * tap, 0, 7); }, { width: 3, alpha: 1 - tap });
    });
  }

  function icon(ctx, name, x, y, s, p, o = {}) { // ícone com "pop"
    if (p <= 0) return;
    ctx.save(); popTransform(ctx, x, y, lerp(0.5, 1, easeBack(p)));
    withAlpha(ctx, clamp(p * 3) * (o.alpha ?? 1), () => icons[name](ctx, x, y, s, { ...o, alpha: 1 }));
    ctx.restore();
  }

  // contador animado de valores ("R$ 5,00" → "R$ 6,00")
  function money(v, dec = 0) {
    const s = v.toFixed(dec).split('.');
    s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return s.join(',');
  }

  // ---------- linha do tempo ----------
  let VID = null, TIM = null;
  const TR = 0.4; // duração da transição entre grupos (s)

  function makeT(t) {
    const b = i => (i < TIM.beats.length ? TIM.beats[i].start : TIM.duration) - 0.08;
    const since = i => t - b(i);
    return {
      t, b, since,
      dur: i => TIM.beats[i].end - TIM.beats[i].start,
      ap: (i, d = 0.5, delay = 0) => easeOut((since(i) - delay) / d),
      lin: (i, d = 0.5, delay = 0) => clamp((since(i) - delay) / d),
      io: (i, d = 0.5, delay = 0) => easeInOut((since(i) - delay) / d),
    };
  }

  function drawTitles(ctx, T) {
    const beats = VID.beats; let i = beats.length - 1;
    while (i > 0 && T.t < T.b(i)) i--;
    const cur = beats[i], prev = i > 0 ? beats[i - 1] : null;
    const k = T.since(i);
    const sameT = prev && prev.titulo === cur.titulo, sameS = prev && (prev.sub || '') === (cur.sub || '');
    const typeDur = Math.min(0.5, Math.max(0.25, T.dur(i) * 0.35));
    // título anterior some rapidinho
    if (prev && k < 0.15) {
      const a = 1 - k / 0.15;
      if (!sameT) drawTitleLines(ctx, prev.titulo, 330, 50, a);
      if (!sameS && prev.sub) drawSub(ctx, prev.sub, a, prev.titulo);
    }
    const tp = sameT ? 1 : clamp((k - 0.05) / typeDur);
    drawTitleLines(ctx, typed(cur.titulo, tp), 330, 50, 1, cur.titulo);
    if (cur.sub) drawSub(ctx, typed(cur.sub, sameS ? 1 : clamp((k - 0.05 - typeDur * 0.6) / (typeDur * 1.2))), 1, cur.titulo);
  }
  function titleLayout(full) { // quebra o título em até 2 linhas se for largo
    return full.length > 24 ? splitHalf(full) : [full];
  }
  function splitHalf(s) {
    const mid = s.length / 2; let best = -1;
    for (let i = 0; i < s.length; i++) if (s[i] === ' ' && (best < 0 || Math.abs(i - mid) < Math.abs(best - mid))) best = i;
    return best < 0 ? [s] : [s.slice(0, best), s.slice(best + 1)];
  }
  function drawTitleLines(ctx, shown, y, size, alpha, full) {
    full = full || shown;
    const lines = titleLayout(full); let rem = shown.length;
    lines.forEach((ln, j) => {
      const part = ln.slice(0, Math.max(0, rem)); rem -= ln.length + 1;
      if (part) text(ctx, part, W / 2, y + j * size * 1.25, { size, spacing: 5, alpha, glowK: 0.45 });
    });
  }
  function drawSub(ctx, s, alpha, full) {
    const y = 330 + (titleLayout(full).length - 1) * 62 + 70;
    text(ctx, s, W / 2, y, { size: 27, weight: 800, color: '185,185,185', spacing: 4, alpha, glowK: 0 });
  }

  function renderFrame(t) {
    const ctx = document.getElementById('c').getContext('2d');
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.filter = 'none';
    background(ctx, t);
    const T = makeT(t);
    const G = VID.groups;
    let g = G.length - 1;
    while (g > 0 && t < T.b(G[g].from)) g--;
    const k = g > 0 ? clamp((t - T.b(G[g].from)) / TR) : 1;
    const drawGroup = (gi, alpha, dx) => withAlpha(ctx, alpha, () => {
      ctx.save();
      // câmera: leve zoom contínuo dentro do grupo + deslize na transição
      const z = 1 + 0.035 * clamp((t - T.b(G[gi].from)) / 8);
      ctx.translate(W / 2 + dx, 1000); ctx.scale(z, z); ctx.translate(-W / 2, -1000);
      G[gi].draw(ctx, T);
      ctx.restore();
    });
    if (k < 1) drawGroup(g - 1, 1 - easeOut(k), -90 * easeOut(k));
    drawGroup(g, easeOut(k), 90 * (1 - easeOut(k)));
    drawTitles(ctx, T);
    if (VID.overlay) VID.overlay(ctx, T);
  }

  window.NEON = { W, H, clamp, lerp, easeOut, easeInOut, easeBack, glow, text, typed, stroke, curve, arcPts, rrect, shape, person, pill, ground, arrow, xmark, check, icons, icon, money, withAlpha, cta, finger, popTransform, partial };
  window.setupVideo = (vid, tim) => { VID = vid; TIM = tim; };
  window.renderFrame = renderFrame;
})();
