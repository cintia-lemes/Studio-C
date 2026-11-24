// Cenas do vídeo 05 — "Juros compostos x juros compostos ao contrário"
// Fio visual: uma curva que sobe (juros a seu favor) e o espelho dela que desce (juros contra você).
window.buildVideo = function (roteiro) {
  const N = window.NEON;
  const { text, stroke, curve, person, pill, ground, arrow, xmark, check, icon, money, clamp, lerp, easeOut, easeInOut, easeBack, shape, rrect, withAlpha, arcPts, popTransform } = N;
  const CX = 540;
  const groups = [];
  const label = (ctx, s, x, y, a, o = {}) => text(ctx, s, x, y, { size: 24, weight: 800, spacing: 4, alpha: a, glowK: 0.2, ...o });
  const GREY = '150,150,150';
  const fv = (pmt, i, n) => pmt * ((1 + i) ** n - 1) / i;

  function clock(ctx, x, y, s, t, a = 1) {
    withAlpha(ctx, a, () => {
      shape(ctx, c => { c.beginPath(); c.arc(x, y, 110 * s, 0, 7); }, { width: 8 * s });
      for (let k = 0; k < 12; k++) { const A = k * Math.PI / 6; stroke(ctx, [[x + 88 * s * Math.cos(A), y + 88 * s * Math.sin(A)], [x + 98 * s * Math.cos(A), y + 98 * s * Math.sin(A)]], { width: 4 * s, alpha: 0.6, glowK: 0.2 }); }
      const h = t * 0.5 - Math.PI / 2, m = t * 6 - Math.PI / 2;
      stroke(ctx, [[x, y], [x + 50 * s * Math.cos(h), y + 50 * s * Math.sin(h)]], { width: 9 * s });
      stroke(ctx, [[x, y], [x + 80 * s * Math.cos(m), y + 80 * s * Math.sin(m)]], { width: 6 * s });
    });
  }

  // 0–2 · a mesma matemática dos dois lados
  groups.push({
    from: 0, draw(ctx, T) {
      const ox = 170, oy = 1000, w = 740;
      stroke(ctx, [[ox, 640], [ox, 1360]], { p: T.ap(0, 0.5), width: 3, alpha: 0.5, glowK: 0.2 });
      stroke(ctx, [[ox, oy], [ox + w, oy]], { p: T.ap(0, 0.5), width: 3, alpha: 0.5, glowK: 0.2 });
      const up = curve(u => [ox + u * w, oy - 320 * (Math.exp(2.4 * u) - 1) / (Math.exp(2.4) - 1)]);
      const dn = curve(u => [ox + u * w, oy + 320 * (Math.exp(2.4 * u) - 1) / (Math.exp(2.4) - 1)]);
      stroke(ctx, up, { p: T.lin(0, 1.2, 0.3), width: 8, dot: true, glowK: 1.2 });
      stroke(ctx, dn, { p: T.lin(1, 1.0, 0.1), width: 7, dot: true, color: GREY, glowK: 0.3 });
      label(ctx, 'VOCÊ RECEBE', ox + w - 120, 640, T.ap(2, 0.4, 0.2));
      label(ctx, 'VOCÊ PAGA', ox + w - 120, 1370, T.ap(2, 0.4, 0.5), { color: '180,180,180', glowK: 0 });
      stroke(ctx, [[ox, oy], [ox + w, oy]], { p: T.ap(2, 0.6, 0.1), width: 3, dash: [12, 12], alpha: 0.9, glowK: 0.6 });
    }
  });

  // 3–5 · juros sobre juros (barras com "camada" de juros) + bola de neve subindo
  groups.push({
    from: 3, draw(ctx, T) {
      const o = 1 - T.ap(5, 0.3);
      withAlpha(ctx, o, () => {
        const base = 1350, hs = [260, 330, 420, 540];
        hs.forEach((h, i) => {
          const x = 220 + i * 190, p = T.ap(3, 0.4, 0.2 + i * 0.25);
          const prev = i ? hs[i - 1] : 220;
          shape(ctx, c => rrect(c, x - 60, base - prev * p, 120, Math.max(1, prev * p), 10), { width: 5, alpha: p, glowK: 0.5 });
          const j = T.ap(3, 0.3, 0.5 + i * 0.25);
          shape(ctx, c => rrect(c, x - 60, base - prev - (h - prev) * j, 120, Math.max(1, (h - prev) * j), 10), { fill: true, alpha: j, glowK: 1 });
          label(ctx, `MÊS ${i + 1}`, x, base + 40, p * 0.7, { size: 20, glowK: 0 });
          if (i < 3) arrow(ctx, x + 40, base - h - 30, x + 150, base - hs[i + 1] - 40, { p: T.ap(4, 0.4, i * 0.3), width: 4, head: 14, alpha: 0.8 });
        });
        ground(ctx, base, T.ap(3, 0.4), 0.5);
        pill(ctx, 'JUROS', 790, 720, { p: T.lin(3, 0.4, 1.4), size: 26 });
      });
      withAlpha(ctx, T.ap(5, 0.3), () => {
        const x0 = 140, y0 = 1400, x1 = 940, y1 = 820;
        stroke(ctx, [[x0, y0], [x1, y1]], { width: 4, alpha: 0.6, glowK: 0.3, p: T.ap(5, 0.4) });
        const u = easeInOut(T.lin(5, 1.6, 0.1)), r = lerp(25, 115, u);
        const nl = Math.hypot(x1 - x0, y1 - y0), nx = (y1 - y0) / nl, ny = -(x1 - x0) / nl;
        const px = lerp(x0 + 60, x1 - 200, u) + nx * (r + 4), py = lerp(y0 - 43, y1 + 145, u) + ny * (r + 4);
        shape(ctx, c => { c.beginPath(); c.arc(px, py, r, 0, 7); }, { width: 7, glowK: 1.2 });
        text(ctx, '$', px, py + 4, { size: r * 1.1, alpha: clamp(u * 3), glowK: 0.8 });
      });
    }
  });

  // 6–10 · R$ 200/mês por 10 anos: colocou 24 mil, tem 46 mil
  groups.push({
    from: 6, draw(ctx, T) {
      icon(ctx, 'jar', 300, 900, 1.0, T.lin(6, 0.4), { level: 0.15 + 0.5 * T.lin(8, 1.6), t: T.t });
      for (let k = 0; k < 3; k++) {
        const ph = ((T.since(6) * 1.2 + k / 3) % 1 + 1) % 1;
        if (T.since(6) > 0.3) withAlpha(ctx, (1 - ph) * T.ap(6, 0.3) * (1 - T.ap(9, 0.4)), () => N.icons.coin(ctx, 300, lerp(600, 760, ph), 0.28, {}));
      }
      pill(ctx, 'R$ 200 / MÊS', 300, 1150, { p: T.lin(6, 0.4, 0.3), size: 28, filled: false });
      pill(ctx, '+1% AO MÊS', 300, 1240, { p: T.lin(7, 0.4, 0.2), size: 26 });
      // barra empilhada: aportes x juros
      const bx = 690, base = 1350, H = 620, max = 46008;
      const hA = H * 24000 / max * T.ap(8, 0.9, 0.1), hJ = H * 22008 / max * T.ap(9, 0.9, 0.1);
      shape(ctx, c => rrect(c, bx - 130, base - hA, 260, Math.max(1, hA), 12), { width: 5, alpha: T.ap(8, 0.3), glowK: 0.4 });
      shape(ctx, c => rrect(c, bx - 130, base - hA - hJ - 6, 260, Math.max(1, hJ), 12), { fill: true, alpha: T.ap(9, 0.3), glowK: 1.2 });
      label(ctx, 'VOCÊ COLOCOU', bx, base - hA / 2 - 20, T.ap(8, 0.3, 0.5), { size: 18, spacing: 2 });
      text(ctx, 'R$ 24.000', bx, base - hA / 2 + 18, { size: 30, alpha: T.ap(8, 0.3, 0.5), glowK: 0.4 });
      text(ctx, 'JUROS', bx, base - hA - hJ / 2 - 6, { size: 26, color: '0,0,0', alpha: T.ap(9, 0.3, 0.8), glowK: 0 });
      text(ctx, 'R$ ' + money(lerp(24000, 46008, easeOut(T.lin(9, 1.0, 0.1)))), bx, base - H - 70, { size: 60, alpha: T.ap(9, 0.3), glowK: 1 });
      ground(ctx, base, T.ap(8, 0.4), 0.5);
      label(ctx, '10 ANOS', bx, base + 40, T.ap(8, 0.3) * 0.7, { glowK: 0 });
      pill(ctx, '≈ 48% FOI JUROS', bx, 1450, { p: T.lin(10, 0.45, 0.2), size: 28 });
    }
  });

  // 11–14 · 20 anos: curva exponencial x linha dos aportes + relógio
  groups.push({
    from: 11, draw(ctx, T) {
      const ox = 150, oy = 1380, w = 760, h = 700, max = 197851;
      stroke(ctx, [[ox, oy - h - 20], [ox, oy], [ox + w + 20, oy]], { p: T.ap(11, 0.5), width: 3, alpha: 0.6, glowK: 0.2 });
      label(ctx, 'ANOS', ox + w - 20, oy + 40, T.ap(11, 0.4) * 0.6, { size: 20, glowK: 0 });
      [5, 10, 15, 20].forEach(a => label(ctx, String(a), ox + w * a / 20, oy + 40, T.ap(11, 0.4, 0.2) * 0.5, { size: 20, glowK: 0 }));
      const lin = curve(u => [ox + u * w, oy - h * (200 * 240 * u) / max], 20);
      stroke(ctx, lin, { p: T.lin(12, 1.0, 0.1), width: 5, dash: [14, 12], alpha: 0.85, dot: true, glowK: 0.4 });
      label(ctx, 'R$ 48 MIL', ox + w - 60, oy - h * 48000 / max - 40, T.ap(12, 0.4, 1.0) * 0.8);
      const ex = curve(u => [ox + u * w, oy - h * fv(200, 0.01, 240 * u + 1e-9) / max], 80);
      stroke(ctx, ex, { p: T.lin(13, 1.3, 0.1), width: 8, dot: true, glowK: 1.3 });
      text(ctx, 'R$ ' + money(lerp(48000, 197851, easeOut(T.lin(13, 1.3, 0.1)))), ox + w - 160, oy - h - 40, { size: 56, alpha: T.ap(13, 0.3), glowK: 1 });
      clock(ctx, 350, 820, 0.8, T.t * 3, T.ap(14, 0.4));
    }
  });

  // 15–16 · o lado escuro: a curva vira de cabeça pra baixo
  groups.push({
    from: 15, draw(ctx, T) {
      const dark = T.ap(15, 0.6);
      withAlpha(ctx, 0.85 * dark, () => { ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 1080, 1920); });
      const flip = T.io(16, 0.8, 0.1);
      ctx.save(); ctx.translate(CX, 1000); ctx.scale(1, lerp(1, -1, flip)); ctx.translate(-CX, -1000);
      const ox = 170, w = 740;
      stroke(ctx, curve(u => [ox + u * w, 1250 - 450 * (Math.exp(2.4 * u) - 1) / (Math.exp(2.4) - 1)]), { width: 8, dot: true, color: flip > 0.5 ? GREY : '255,255,255', glowK: flip > 0.5 ? 0.3 : 1, alpha: 0.4 + 0.6 * T.ap(15, 0.4) });
      ctx.restore();
      pill(ctx, 'AO CONTRÁRIO', CX, 1500, { p: T.lin(16, 0.4, 0.8), size: 30, filled: false });
    }
  });

  // 17–19 · celular em 24x: R$ 2.000 → R$ 3.148 = 1,5 celular
  groups.push({
    from: 17, draw(ctx, T) {
      const one = T.ap(19, 0.4);
      icon(ctx, 'phone', lerp(CX, 400, one), 780, 1.2, T.lin(17, 0.4));
      withAlpha(ctx, one, () => {
        ctx.save(); ctx.beginPath(); ctx.rect(620, 600, 1080, 180); ctx.clip();
        N.icons.phone(ctx, 690, 780, 1.2, { alpha: 1 });
        ctx.restore();
        N.icons.phone(ctx, 690, 780, 1.2, { alpha: 0.25 });
        text(ctx, '+ ½', 860, 700, { size: 56, glowK: 0.8 });
      });
      pill(ctx, 'R$ 2.000', CX, 1000, { p: T.lin(17, 0.4, 0.3), size: 32, filled: false, alpha: 1 - one });
      // 24 parcelas
      for (let i = 0; i < 24; i++) {
        const col = i % 8, row = Math.floor(i / 8), p = T.lin(17, 0.05, 1.0 + i * 0.07);
        shape(ctx, c => rrect(c, 180 + col * 92, 1090 + row * 70, 76, 54, 10), { fill: p > 0.5, width: 3, alpha: 0.3 + 0.7 * p, glowK: p > 0.5 ? 0.5 : 0.1 });
      }
      label(ctx, '24 × R$ 131', CX, 1330, T.ap(17, 0.4, 2.0) * 0.8);
      text(ctx, 'R$ ' + money(lerp(2000, 3148, easeOut(T.lin(18, 1.0, 0.1)))), CX, 1440, { size: 80, alpha: T.ap(18, 0.3), glowK: 1 });
    }
  });

  // 20–21 · rotativo: R$ 1.000 → R$ 2.000
  groups.push({
    from: 20, draw(ctx, T) {
      const r = 260, cy = 1020, spin = T.t * (2 + 3 * T.ap(21, 0.5));
      withAlpha(ctx, T.ap(20, 0.4), () => {
        for (let k = 0; k < 3; k++) {
          const a0 = spin + k * (Math.PI * 2 / 3), a1 = a0 + Math.PI * 2 / 3 - 0.35;
          stroke(ctx, arcPts(CX, cy, r, a0, a1, 40), { width: 6 });
          const ex = CX + r * Math.cos(a1), ey = cy + r * Math.sin(a1), ta = a1 + Math.PI / 2;
          stroke(ctx, [[ex - 22 * Math.cos(ta - 0.6), ey - 22 * Math.sin(ta - 0.6)], [ex, ey], [ex - 22 * Math.cos(ta + 0.6), ey - 22 * Math.sin(ta + 0.6)]], { width: 6 });
        }
        label(ctx, 'ROTATIVO', CX, cy - 80, 1, { size: 28 });
      });
      text(ctx, 'R$ ' + money(lerp(1000, 2000, easeOut(T.lin(21, 1.0, 0.1)))), CX, cy + 20, { size: 76, alpha: T.ap(20, 0.4, 0.3), glowK: 1 });
      pill(ctx, '2× A DÍVIDA', CX, cy + 380, { p: T.lin(21, 0.45, 0.8), size: 30 });
    }
  });

  // 22–24 · compras por impulso: R$ 150/mês somem; investidos seriam R$ 34.506
  groups.push({
    from: 22, draw(ctx, T) {
      const g = T.ap(24, 0.4);
      withAlpha(ctx, 1 - g, () => {
        icon(ctx, 'bag', CX, 880, 1.2, T.lin(22, 0.45));
        for (let k = 0; k < 5; k++) {
          const ph = ((T.since(23) * 0.7 + k / 5) % 1 + 1) % 1;
          if (T.since(23) > 0) pill(ctx, '− R$ 150', CX + Math.sin(k * 2.1) * 260, lerp(1050, 1500, ph), { p: 1, size: 24, filled: false, alpha: (1 - ph) * T.ap(23, 0.3) });
        }
      });
      withAlpha(ctx, g, () => {
        const ox = 170, oy = 1380, w = 740, h = 560;
        stroke(ctx, [[ox, oy - h - 20], [ox, oy], [ox + w, oy]], { width: 3, alpha: 0.6, glowK: 0.2 });
        const c = curve(u => [ox + u * w, oy - h * fv(150, 0.01, 120 * u + 1e-9) / 34506], 60);
        stroke(ctx, c, { p: T.lin(24, 1.2, 0.2), width: 6, dash: [14, 12], dot: true, glowK: 0.8 });
        text(ctx, 'R$ ' + money(lerp(0, 34506, easeOut(T.lin(24, 1.2, 0.2)))), CX, 740, { size: 80, glowK: 1 });
        label(ctx, 'O QUE PODERIA TER RENDIDO', CX, 820, 0.8);
        label(ctx, '10 ANOS', ox + w - 50, oy + 40, 0.6, { glowK: 0, size: 20 });
      });
    }
  });

  // 25–27 · aporte ao contrário: o dinheiro muda de direção
  groups.push({
    from: 25, draw(ctx, T) {
      ground(ctx, 1300, T.ap(25, 0.4), 0.5);
      person(ctx, 260, 1300, { s: 1.0, pop: T.lin(25, 0.4) });
      icon(ctx, 'bank', 820, 1190, 0.95, T.lin(25, 0.4, 0.2));
      // 26: setas do banco pra pessoa (como deveria ser); 27: da pessoa pro banco
      const rev = T.io(27, 0.5);
      for (let k = 0; k < 4; k++) {
        const ph = ((T.since(25) * 0.8 + k / 4) % 1 + 1) % 1;
        const fwd = rev < 0.5;
        const x = fwd ? lerp(720, 360, ph) : lerp(360, 720, ph);
        const y = 1050 - 120 * Math.sin(Math.PI * ph);
        withAlpha(ctx, T.ap(25, 0.3, 0.5) * Math.sin(Math.PI * ph) * (fwd ? 1 - T.ap(26, 0.3) * 0 : 1), () => N.icons.coin(ctx, x, y, 0.26, {}));
      }
      pill(ctx, 'JUROS → VOCÊ', CX, 800, { p: T.lin(26, 0.4, 0.2), size: 28, filled: false, alpha: 1 - rev });
      pill(ctx, 'VOCÊ → JUROS', CX, 800, { p: T.lin(27, 0.4, 0.3), size: 28 });
      xmark(ctx, CX + 230, 800, 32, T.lin(27, 0.4, 0.1) * 0);
    }
  });

  // 28–31 · virar o jogo: curva volta a subir + checklist
  groups.push({
    from: 28, draw(ctx, T) {
      const o = 1 - T.ap(29, 0.3);
      withAlpha(ctx, o, () => {
        const flip = T.io(28, 0.8, 0.2);
        ctx.save(); ctx.translate(CX, 1000); ctx.scale(1, lerp(-1, 1, flip)); ctx.translate(-CX, -1000);
        stroke(ctx, curve(u => [170 + u * 740, 1250 - 450 * (Math.exp(2.4 * u) - 1) / (Math.exp(2.4) - 1)]), { width: 8, dot: true, color: flip > 0.5 ? '255,255,255' : GREY, glowK: flip > 0.5 ? 1.3 : 0.3 });
        ctx.restore();
      });
      const rows = [['QUITE AS DÍVIDAS MAIS CARAS', 29], ['PERGUNTE O CUSTO TOTAL', 30], ['INVISTA, MESMO QUE POUCO', 31]];
      rows.forEach(([s, bi], i) => {
        const y = 820 + i * 190, p = T.lin(bi, 0.4);
        withAlpha(ctx, p, () => {
          shape(ctx, c => rrect(c, 175, y - 45, 90, 90, 18), { width: 5 });
          text(ctx, s, 305, y, { size: 32, align: 'left', glowK: 0.4 });
        });
        if (p > 0) stroke(ctx, [[195, y], [217, y + 24], [247, y - 22]], { p: T.lin(bi, 0.4, 0.5), width: 8 });
      });
    }
  });

  // 32–33 · ontem x hoje
  groups.push({
    from: 32, draw(ctx, T) {
      const h = T.io(33, 0.6);
      withAlpha(ctx, 1 - 0.6 * h, () => icon(ctx, 'calendar', lerp(CX, 300, h), 1000, lerp(1.3, 0.9, h), T.lin(32, 0.45), { label: '23' }));
      label(ctx, 'ONTEM', lerp(CX, 300, h), lerp(1220, 1160, h), T.ap(32, 0.4, 0.3) * (1 - 0.5 * h));
      withAlpha(ctx, h, () => {
        N.icons.calendar(ctx, 780, 1000, 1.1, { label: '24' });
        label(ctx, 'HOJE', 780, 1200, 1, { size: 30 });
        check(ctx, 920, 840, 44, T.lin(33, 0.5, 0.5));
      });
    }
  });

  groups.push({ from: 34, draw(ctx, T) { N.cta(ctx, T, 34); } });

  return {
    beats: roteiro.beats,
    groups,
    overlay(ctx, T) {
      const d = T.ap(7, 0.6) * 0.75;
      if (d > 0) text(ctx, roteiro.aviso, CX, 1640, { size: 19, weight: 700, color: '160,160,160', spacing: 3, alpha: d, glowK: 0 });
    }
  };
};
