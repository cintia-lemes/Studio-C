// Cenas do vídeo 04 — "A regra 50-30-20"
// Elementos fixos: rosca dividida 50/30/20 e os 3 potes (ESSENCIAL · DESEJOS · FUTURO).
window.buildVideo = function (roteiro) {
  const N = window.NEON;
  const { text, stroke, curve, person, pill, ground, arrow, xmark, check, icon, money, clamp, lerp, easeOut, easeInOut, easeBack, shape, rrect, withAlpha, arcPts, popTransform } = N;
  const CX = 540, GY = 1250;
  const groups = [];
  const label = (ctx, s, x, y, a, o = {}) => text(ctx, s, x, y, { size: 24, weight: 800, spacing: 4, alpha: a, glowK: 0.2, ...o });
  const POTS = [['ESSENCIAL', 0.5, '255,255,255'], ['DESEJOS', 0.3, '170,170,170'], ['FUTURO', 0.2, '255,255,255']];

  // 3 potes lado a lado; lv = [níveis], vals = [rótulos de valor]
  function pots(ctx, T, y, o = {}) {
    const { pop = [1, 1, 1], lv = [0, 0, 0], vals = [], dim = [0, 0, 0], s = 0.85 } = o;
    POTS.forEach(([nm], i) => {
      const x = 230 + i * 310;
      if (pop[i] <= 0) return;
      icon(ctx, 'jar', x, y, s, pop[i], { level: lv[i], t: T.t + i, alpha: 1 - dim[i] * 0.65 });
      label(ctx, nm, x, y + 175 * s + 40, clamp(pop[i] * 2) * (1 - dim[i] * 0.6), { size: 24 });
      if (vals[i]) pill(ctx, vals[i][0], x, y - 150 * s - 60, { p: vals[i][1], size: 30, filled: i === 2 });
    });
  }

  // rosca 50/30/20; p = [progresso de cada fatia], hl = fatia em destaque
  function donut(ctx, T, cx, cy, r, p, hl) {
    let a = -Math.PI / 2;
    POTS.forEach(([nm, f, col], i) => {
      const a0 = a + 0.05, a1 = a + Math.PI * 2 * f - 0.05; a += Math.PI * 2 * f;
      if (p[i] <= 0) return;
      const on = hl === i;
      stroke(ctx, arcPts(cx, cy, r, a0, lerp(a0, a1, easeOut(p[i])), 60), { width: on ? 52 : 40, color: col, alpha: hl == null || on ? 1 : 0.35, glowK: on ? 1.3 : (i === 1 ? 0.2 : 0.5) });
      const am = (a0 + a1) / 2;
      text(ctx, Math.round(f * 100) + '%', cx + (r + 85) * Math.cos(am), cy + (r + 85) * Math.sin(am), { size: 34, alpha: clamp(p[i] * 2) * (hl == null || on ? 1 : 0.5), glowK: 0.4 });
    });
  }

  // 0–3 · abertura: 50 · 30 · 20 → três potes
  groups.push({
    from: 0, draw(ctx, T) {
      const o0 = 1 - T.ap(1, 0.3);
      withAlpha(ctx, o0, () => {
        ground(ctx, GY, T.ap(0, 0.6));
        person(ctx, CX, GY, { s: 1.15, pop: T.lin(0, 0.4) });
        pill(ctx, 'SALÁRIO', CX, GY - 310, { p: T.lin(0, 0.45, 0.4), size: 30, filled: false });
        text(ctx, '?', CX + 150, GY - 200, { size: 90, alpha: T.ap(0, 0.4, 1.0), glowK: 0.8 });
      });
      const j = T.io(2, 0.5);
      ['50', '30', '20'].forEach((n, i) => {
        const x = lerp(250 + i * 290, 320 + i * 220, j);
        text(ctx, n, x, lerp(950, 900, j), { size: lerp(190, 120, j), alpha: T.ap(1, 0.4, 0.15 + i * 0.25) * (1 - T.ap(3, 0.3)), glowK: 1 });
        if (i < 2) text(ctx, '-', x + 110, 900, { size: 100, alpha: j * (1 - T.ap(3, 0.3)), glowK: 0.6 });
      });
      label(ctx, 'A REGRA', CX, 790, T.ap(2, 0.4, 0.3) * (1 - T.ap(3, 0.3)));
      withAlpha(ctx, T.ap(3, 0.3), () => pots(ctx, T, 1000, { pop: [0, 1, 2].map(i => T.lin(3, 0.4, 0.2 + i * 0.2)) }));
    }
  });

  // 4–11 · rosca enchendo fatia por fatia + ícones de cada pote
  groups.push({
    from: 4, draw(ctx, T) {
      const hl = T.since(10) > 0 ? 2 : T.since(7) > 0 ? 1 : 0;
      const cy = 900, r = 230;
      donut(ctx, T, CX, cy, r, [T.lin(4, 0.9, 0.2), T.lin(7, 0.8, 0.2), T.lin(10, 0.7, 0.2)], hl);
      const centers = [['50%', 'ESSENCIAL', 4], ['30%', 'DESEJOS', 7], ['20%', 'FUTURO', 10]];
      centers.forEach(([n, l, bi], i) => {
        const a = T.ap(bi, 0.3, 0.3) * (i < 2 ? 1 - T.ap(centers[i + 1][2], 0.25) : 1);
        text(ctx, n, CX, cy - 15, { size: 96, alpha: a, glowK: 0.9 });
        label(ctx, l, CX, cy + 65, a);
      });
      // linha de ícones abaixo
      const rows = [
        [['house', 0.6], ['cart', 0.65], ['pump', 0.55]], // 5
        [['bag', 0.6], ['playTile', 0.6], ['cup', 0.6]],   // 8
        [['shield', 0.55], ['coin', 0.6], ['calendar', 0.5]], // 11
      ];
      [5, 8, 11].forEach((bi, k) => {
        const a = T.ap(bi, 0.3) * (k < 2 ? 1 - T.ap([7, 10][k], 0.3) : 1);
        if (a <= 0) return;
        rows[k].forEach(([nm, s], i) => withAlpha(ctx, a, () => icon(ctx, nm, 270 + i * 270, 1360, s, T.lin(bi, 0.4, i * 0.25), { t: T.t, label: '%' })));
      });
      pill(ctx, 'OBRIGATÓRIO', CX, 1250, { p: T.lin(6, 0.45, 0.3), size: 28, filled: false, alpha: 1 - T.ap(7, 0.3) });
      pill(ctx, 'SEM CULPA ✓', CX, 1250, { p: T.lin(9, 0.45, 0.4), size: 28, alpha: 1 - T.ap(10, 0.3) });
    }
  });

  // 12–16 · na prática: R$ 3.000 → 1.500 / 900 / 600
  groups.push({
    from: 12, draw(ctx, T) {
      const sal = T.ap(13, 0.4) * (1 - 0.5 * T.ap(14, 0.4));
      text(ctx, 'R$ 3.000', CX, 720, { size: 110, alpha: sal, glowK: 1 });
      label(ctx, 'LÍQUIDO', CX, 800, sal * 0.7, { glowK: 0 });
      const lv = [T.io(14, 0.8, 0.2) * 0.5 * 1.6, T.io(15, 0.8, 0.2) * 0.3 * 1.6, T.io(16, 0.8, 0.2) * 0.2 * 1.6];
      pots(ctx, T, 1150, {
        pop: [0, 1, 2].map(i => T.lin(12, 0.4, 0.2 + i * 0.15)),
        lv, vals: [['R$ 1.500', T.lin(14, 0.4, 0.3)], ['R$ 900', T.lin(15, 0.4, 0.3)], ['R$ 600', T.lin(16, 0.4, 0.3)]],
      });
      // fluxo do salário para os potes
      [14, 15, 16].forEach((bi, i) => {
        const p = T.lin(bi, 0.6);
        if (p > 0 && p < 1) N.icons.coin(ctx, lerp(CX, 230 + i * 310, easeInOut(p)), lerp(800, 1000, easeInOut(p)), 0.3, { alpha: 1 - p * 0.3 });
      });
    }
  });

  // 17–19 · R$ 600 × 12 = R$ 7.200 (+ rendimento)
  groups.push({
    from: 17, draw(ctx, T) {
      pill(ctx, 'R$ 600 / MÊS', CX, 680, { p: T.lin(17, 0.45), size: 34, filled: false });
      text(ctx, '?', CX + 230, 680, { size: 70, alpha: T.ap(17, 0.4, 0.4) * (1 - T.ap(18, 0.3)), glowK: 0.6 });
      const base = 1450, bw = 46;
      for (let i = 0; i < 12; i++) {
        const p = T.lin(18, 0.1, 0.2 + i * 0.09);
        const x = 190 + i * 62, h = 40 + i * 42;
        shape(ctx, c => rrect(c, x, base - h * easeOut(p), bw, Math.max(1, h * easeOut(p)), 8), { fill: true, alpha: p * (0.55 + 0.45 * i / 11), glowK: 0.6 });
      }
      ground(ctx, base, T.ap(18, 0.4), 0.5);
      text(ctx, 'R$ ' + money(lerp(0, 7200, easeOut(T.lin(18, 1.3, 0.2)))), CX, 810, { size: 110, alpha: T.ap(18, 0.3), glowK: 1 });
      label(ctx, '12 MESES', CX, base + 40, T.ap(18, 0.4, 0.4) * 0.7, { glowK: 0 });
      // rendimento: curva tracejada acima das barras
      const rc = curve(u => [190 + u * 730, base - 40 - u * 470 - 60 * u * u], 40);
      stroke(ctx, rc, { p: T.lin(19, 0.9, 0.1), width: 4, dash: [12, 12], alpha: 0.85, dot: true, glowK: 0.6 });
      pill(ctx, '+ RENDIMENTO', 340, 1150, { p: T.lin(19, 0.4, 0.8), size: 24 });
    }
  });

  // 20–24 · a ordem: guardar o que sobra (R$ 0) → separar 20% primeiro
  groups.push({
    from: 20, draw(ctx, T) {
      const sw = T.io(23, 0.8, 0.3); // troca de ordem
      const box = (lbl, slot, a, filled = false) => {
        const x = 220 + slot * 320;
        withAlpha(ctx, a, () => {
          shape(ctx, c => rrect(c, x - 130, 920, 260, 130, 26), { width: 5, fill: filled, glowK: filled ? 1.2 : 0.8 });
          ctx.font = '900 28px Inter'; ctx.letterSpacing = '3px'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillStyle = filled ? '#000' : '#fff'; ctx.fillText(lbl, x, 987);
        });
      };
      const a1 = T.ap(21, 0.4);
      box('SALÁRIO', 0, T.ap(20, 0.4));
      box('GASTOS', lerp(1, 2, sw), a1 * T.ap(21, 0.3, 0.3));
      box(sw > 0.5 ? '20% FUTURO' : 'O QUE SOBRA', lerp(2, 1, sw), a1 * T.ap(21, 0.3, 0.7), sw > 0.5);
      arrow(ctx, 360, 985, 400, 985, { p: a1, width: 5, head: 14 });
      arrow(ctx, 680, 985, 720, 985, { p: a1, width: 5, head: 14 });
      // "quase nunca sobra"
      const zero = T.ap(22, 0.4) * (1 - T.ap(23, 0.3));
      text(ctx, 'R$ 0', 860, 1140, { size: 56, alpha: zero, glowK: 0.6 });
      xmark(ctx, 860, 1250, 40, T.lin(22, 0.4, 0.4) * (1 - T.ap(23, 0.3)));
      // dia do pagamento
      withAlpha(ctx, T.ap(23, 0.4, 1.0), () => icon(ctx, 'calendar', 540, 1300, 0.7, T.lin(23, 0.4, 1.0), { label: '5' }));
      label(ctx, 'DIA DO PAGAMENTO', 540, 1460, T.ap(23, 0.4, 1.3) * (1 - T.ap(24, 0.3)));
      pill(ctx, 'PAGUE-SE PRIMEIRO', CX, 1460, { p: T.lin(24, 0.45, 0.2), size: 32 });
    }
  });

  // 25–27 · ajuste: essencial 65% → 60/25/15
  groups.push({
    from: 25, draw(ctx, T) {
      const bx = 140, bw = 800, by = 980, bh = 110;
      const adj = T.io(27, 1.0, 0.1);
      const f = [lerp(0.65, 0.6, adj), lerp(0.25, 0.25, adj), lerp(0.10, 0.15, adj)];
      const show = T.ap(25, 0.5);
      let x = bx;
      ['ESSENCIAL', 'DESEJOS', 'FUTURO'].forEach((nm, i) => {
        const w = bw * f[i] * show;
        if (w > 2) {
          shape(ctx, c => rrect(c, x + 4, by, w - 8, bh, 18), { fill: i !== 1, color: i === 1 ? '255,255,255' : '255,255,255', width: 5, alpha: i === 2 ? 0.75 : 1, glowK: i === 0 ? 1 : 0.6 });
          text(ctx, Math.round(f[i] * 100) + '%', x + w / 2, by + bh / 2 + 2, { size: 36, color: i === 1 ? '255,255,255' : '0,0,0', glowK: 0, alpha: T.ap(25, 0.4, 0.4) });
          label(ctx, nm, x + w / 2, by + bh + 45, T.ap(25, 0.4, 0.5), { size: 20 });
        }
        x += bw * f[i] * show;
      });
      // marca dos 50%
      const m = T.ap(25, 0.4, 0.6) * (1 - T.ap(27, 0.3));
      stroke(ctx, [[bx + bw * 0.5, by - 70], [bx + bw * 0.5, by + bh + 10]], { width: 4, dash: [10, 10], alpha: m, glowK: 0.4 });
      label(ctx, 'META 50%', bx + bw * 0.5, by - 100, m);
      pill(ctx, 'TUDO BEM ✓', CX, 1330, { p: T.lin(26, 0.45, 0.1), size: 30, filled: false, alpha: 1 - T.ap(27, 0.3) });
      pill(ctx, 'O POSSÍVEL AGORA', CX, 1330, { p: T.lin(27, 0.45, 1.2), size: 30 });
    }
  });

  // 28–29 · não é prisão, é mapa
  groups.push({
    from: 28, draw(ctx, T) {
      const open = T.io(29, 0.7);
      for (let i = 0; i < 6; i++) {
        const x = 290 + i * 100, dy = open * (i % 2 ? -1 : 1) * 900;
        stroke(ctx, [[x, 700 + dy], [x, 1350 + dy]], { width: 10, p: T.ap(28, 0.5, i * 0.05), alpha: 1 - open });
      }
      stroke(ctx, [[260, 700], [820, 700]], { width: 10, p: T.ap(28, 0.5), alpha: 1 - open });
      stroke(ctx, [[260, 1350], [820, 1350]], { width: 10, p: T.ap(28, 0.5), alpha: 1 - open });
      xmark(ctx, CX, 1025, 70, T.lin(28, 0.4, 0.6) * (1 - open));
      withAlpha(ctx, T.ap(29, 0.4, 0.2), () => N.icons.map(ctx, CX, 1020, 1.4, { p: T.lin(29, 0.9, 0.4) }));
    }
  });

  // 30–31 · futuro nunca zero / comece este mês
  groups.push({
    from: 30, draw(ctx, T) {
      const o1 = 1 - T.ap(31, 0.3);
      withAlpha(ctx, o1, () => {
        icon(ctx, 'jar', CX, 1000, 1.4, T.lin(30, 0.4), { level: lerp(0, 0.25, T.io(30, 1.0, 0.5)), t: T.t });
        label(ctx, 'FUTURO', CX, 1290, T.ap(30, 0.4), { size: 30 });
        pill(ctx, 'NUNCA ZERO', CX, 680, { p: T.lin(30, 0.45, 1.2), size: 32 });
      });
      withAlpha(ctx, T.ap(31, 0.3), () => {
        icon(ctx, 'calendar', CX, 1000, 1.4, T.lin(31, 0.45), { label: '1' });
        check(ctx, CX + 200, 830, 50, T.lin(31, 0.5, 0.5));
      });
    }
  });

  groups.push({ from: 32, draw(ctx, T) { N.cta(ctx, T, 32); } });

  return {
    beats: roteiro.beats,
    groups,
    overlay(ctx, T) {
      const d = T.ap(13, 0.6) * 0.75;
      if (d > 0) text(ctx, roteiro.aviso, CX, 1640, { size: 20, weight: 700, color: '160,160,160', spacing: 3, alpha: d, glowK: 0 });
    }
  };
};
