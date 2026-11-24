// Cenas do vídeo 03 — "Pequenos vazamentos do dia a dia"
// Metáfora central: o pote de dinheiro com furos (vaza gota por gota) → no final, gota por gota ele enche.
window.buildVideo = function (roteiro) {
  const N = window.NEON;
  const { text, stroke, curve, person, pill, ground, arrow, xmark, check, icon, money, clamp, lerp, easeOut, easeInOut, easeBack, shape, rrect, withAlpha, arcPts, popTransform } = N;
  const CX = 540, GY = 1250;
  const groups = [];
  const label = (ctx, s, x, y, a, o = {}) => text(ctx, s, x, y, { size: 24, weight: 800, spacing: 4, alpha: a, glowK: 0.2, ...o });
  const big = (ctx, s, x, y, a, size = 110) => text(ctx, s, x, y, { size, alpha: a, glowK: 0.9 });

  // gotas caindo de um ponto (x,y) — determinístico pelo tempo
  function drips(ctx, t, x, y, o = {}) {
    const { rate = 1.6, fall = 260, s = 0.8, alpha = 1, seed = 0 } = o;
    for (let k = 0; k < 4; k++) {
      const ph = ((t * rate + k / 4 + seed) % 1 + 1) % 1;
      const yy = y + 10 + ph * ph * fall;
      icons(ctx, 'drop', x, yy, s * (1 - ph * 0.3), alpha * (ph < 0.85 ? 1 : (1 - ph) / 0.15));
    }
  }
  const icons = (ctx, nm, x, y, s, a, o = {}) => withAlpha(ctx, a, () => N.icons[nm](ctx, x, y, s, o));

  // barra "TOTAL NO ANO" acumulando os vazamentos (beats 10, 12, 16, 18)
  const LEAKS = [[3640, 10], [3168, 12], [3324, 16], [540, 18]];
  const TOTAL = 10672;
  function tally(ctx, T, x, y, w, h, o = {}) {
    const { showLabel = true } = o;
    shape(ctx, c => rrect(c, x, y, w, h, h / 2), { width: 3, alpha: 0.5, glowK: 0.2 });
    let acc = 0, shown = 0;
    LEAKS.forEach(([v, bi], i) => {
      const p = o.full ? 1 : T.ap(bi, 0.6, 0.4);
      const sw = w * v / TOTAL;
      if (p > 0) {
        const x0 = x + w * acc / TOTAL;
        shape(ctx, c => rrect(c, x0 + 3, y + 3, Math.max(1, (sw - 6) * p), h - 6, (h - 6) / 2), { fill: true, alpha: i % 2 ? 0.75 : 1, glowK: 0.6 });
      }
      shown += v * p; acc += v;
    });
    if (showLabel) {
      label(ctx, 'VAZOU NO ANO', x, y - 34, 0.7, { align: 'left', glowK: 0 });
      text(ctx, 'R$ ' + money(shown), x + w, y - 36, { size: 34, align: 'right', glowK: 0.5 });
    }
  }

  // 0–3 · as frases do "só"
  groups.push({
    from: 0, draw(ctx, T) {
      ground(ctx, GY, T.ap(0, 0.6));
      person(ctx, CX, GY, { s: 1.15, pop: T.lin(0, 0.4) });
      const nada = T.io(3, 0.6, 0.2);
      const bubbles = [['SÓ HOJE EU PEÇO DELIVERY', 0, 300, 820], ['SÓ ESSA PARCELA NÃO PESA', 1, 780, 940], ['SÓ UM CAFEZINHO', 2, 330, 1060]];
      bubbles.forEach(([s, bi, x, y]) => {
        ctx.save(); popTransform(ctx, CX, 1000, lerp(1, 0.25, nada));
        const xx = lerp(x, CX, nada), yy = lerp(y, 1000, nada);
        pill(ctx, s, xx, yy, { p: T.lin(bi, 0.45), filled: false, size: 26, alpha: 1 - nada * 0.6 });
        ctx.restore();
      });
      pill(ctx, 'R$ 0,00?', CX, 860, { p: T.lin(3, 0.45, 0.7), size: 30 });
    }
  });

  // 4–6 · o pote vaza
  groups.push({
    from: 4, draw(ctx, T) {
      const lvl = lerp(0.8, 0.62, T.lin(5, 6));
      icon(ctx, 'jar', CX, 980, 1.35, T.lin(4, 0.45), { level: lvl * T.ap(4, 0.8), t: T.t });
      const holes = [[CX - 60, 1180], [CX + 40, 1182], [CX + 140, 1100]];
      holes.forEach(([hx, hy], i) => {
        const on = i === 0 ? T.ap(5, 0.3) : T.ap(6, 0.3, (i - 1) * 0.3);
        if (on <= 0) return;
        shape(ctx, c => { c.beginPath(); c.arc(hx, hy, 7, 0, 7); }, { fill: true, alpha: on });
        drips(ctx, T.t, hx, hy, { alpha: on, seed: i * 0.37, rate: 1.3 + i * 0.25 });
      });
      ground(ctx, 1500, T.ap(5, 0.5), 0.4);
    }
  });

  // 7–10 · delivery: R$ 35 × 2/semana → R$ 70 → R$ 3.640/ano
  groups.push({
    from: 7, draw(ctx, T) {
      // "vamos fazer a conta": recibo sendo desenhado
      const r = 1 - T.ap(8, 0.3);
      withAlpha(ctx, r * T.ap(7, 0.3), () => {
        const pts = [[CX - 170, 700], [CX + 170, 700], [CX + 170, 1250]];
        for (let i = 0; i <= 8; i++) pts.push([CX + 170 - i * 42.5, 1250 + (i % 2 ? 25 : 0)]);
        pts.push([CX - 170, 700]);
        stroke(ctx, pts, { p: T.lin(7, 0.7), width: 6 });
        for (let i = 0; i < 6; i++) stroke(ctx, [[CX - 110, 800 + i * 70], [CX + (i % 2 ? 40 : 110), 800 + i * 70]], { p: T.lin(7, 0.25, 0.25 + i * 0.07), width: 6, alpha: 0.6, glowK: 0.3 });
      });
      withAlpha(ctx, T.ap(8, 0.3), () => {
        icon(ctx, 'bag', CX - 170, 760, 0.9, T.lin(8, 0.45));
        pill(ctx, 'R$ 35', CX + 150, 740, { p: T.lin(8, 0.45, 0.4), size: 40 });
        // semana: 7 bolinhas, 2 acesas
        const days = ['S', 'T', 'Q', 'Q', 'S', 'S', 'D'];
        days.forEach((d, i) => {
          const x = 230 + i * 103, y = 990, lit = (i === 2 || i === 5);
          const p = T.lin(8, 0.3, 0.9 + i * 0.06);
          const on = lit ? T.ap(8, 0.3, 1.6 + (i === 5 ? 0.25 : 0)) : 0;
          shape(ctx, c => { c.beginPath(); c.arc(x, y, 36, 0, 7); }, { fill: on > 0.5, width: 4, alpha: p * (lit ? 1 : 0.45), glowK: lit ? 1 : 0.2 });
          text(ctx, d, x, y + 2, { size: 26, alpha: p, color: on > 0.5 ? '0,0,0' : '255,255,255', glowK: 0 });
        });
        text(ctx, '= R$ 70 / SEMANA', CX, 1110, { size: 44, alpha: T.ap(9, 0.4), glowK: 0.6 });
        // ano: 52 semanas
        for (let i = 0; i < 52; i++) {
          const col = i % 13, row = Math.floor(i / 13);
          const p = T.lin(10, 0.04, 0.2 + i * 0.03);
          shape(ctx, c => rrect(c, 205 + col * 52, 1190 + row * 52, 40, 40, 8), { fill: p > 0.5, width: 3, alpha: 0.35 + 0.65 * p, glowK: p > 0.5 ? 0.6 : 0.1 });
        }
        label(ctx, '52 SEMANAS', CX, 1420, T.ap(10, 0.3) * 0.7, { glowK: 0 });
      });
    }
  });

  // 11–12 · lanchinho R$ 12 × dia útil → R$ 3.168/ano
  groups.push({
    from: 11, draw(ctx, T) {
      icon(ctx, 'cup', CX - 170, 800, 1.0, T.lin(11, 0.45), { t: T.t });
      pill(ctx, 'R$ 12', CX + 150, 780, { p: T.lin(11, 0.45, 0.4), size: 40 });
      const days = ['S', 'T', 'Q', 'Q', 'S', 'S', 'D'];
      days.forEach((d, i) => {
        const x = 230 + i * 103, y = 1010, lit = i < 5;
        const p = T.lin(11, 0.3, 0.9 + i * 0.06);
        const on = lit ? T.ap(11, 0.25, 1.3 + i * 0.12) : 0;
        shape(ctx, c => { c.beginPath(); c.arc(x, y, 36, 0, 7); }, { fill: on > 0.5, width: 4, alpha: p * (lit ? 1 : 0.45), glowK: lit ? 1 : 0.2 });
        text(ctx, d, x, y + 2, { size: 26, alpha: p, color: on > 0.5 ? '0,0,0' : '255,255,255', glowK: 0 });
      });
      text(ctx, 'R$ ' + money(lerp(0, 3168, easeOut(T.lin(12, 1.0, 0.1)))), CX, 1210, { size: 90, alpha: T.ap(12, 0.3), glowK: 0.9 });
      label(ctx, 'POR ANO', CX, 1290, T.ap(12, 0.3, 0.3) * 0.7, { glowK: 0 });
    }
  });

  // 13–16 · as 3 parcelas → R$ 277/mês → R$ 3.324/ano
  groups.push({
    from: 13, draw(ctx, T) {
      icon(ctx, 'card', CX, 720, 0.9, T.lin(13, 0.45));
      const ps = [['R$ 89', 0], ['R$ 129', 0.45], ['R$ 59', 0.9]];
      ps.forEach(([s, d], i) => {
        const p = T.lin(13, 0.4, 0.5 + i * 0.25);
        const hl = T.ap(14, 0.3, d);
        pill(ctx, s, 300 + i * 240, 930, { p, size: 36, filled: hl > 0.5, alpha: 0.6 + 0.4 * hl });
        label(ctx, `PARCELA ${i + 1}/12`, 300 + i * 240, 1010, p * 0.6, { size: 18, glowK: 0 });
      });
      stroke(ctx, [[180, 1060], [900, 1060]], { p: T.ap(15, 0.4), width: 4, alpha: 0.7 });
      text(ctx, '= R$ 277 / MÊS', CX, 1140, { size: 52, alpha: T.ap(15, 0.4, 0.3), glowK: 0.7 });
      // 12 meses
      const ms = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
      ms.forEach((m, i) => {
        const p = T.lin(16, 0.08, 0.1 + i * 0.07);
        const x = 160 + i * 69;
        shape(ctx, c => rrect(c, x - 27, 1230, 54, 70, 10), { fill: p > 0.5, width: 3, alpha: 0.35 + 0.65 * p, glowK: p > 0.5 ? 0.6 : 0.1 });
        text(ctx, m, x, 1266, { size: 22, color: p > 0.5 ? '0,0,0' : '255,255,255', alpha: 0.4 + 0.6 * p, glowK: 0 });
      });
    }
  });

  // 17–18 · assinaturas esquecidas
  groups.push({
    from: 17, draw(ctx, T) {
      [0, 1, 2].forEach(i => {
        const x = 270 + i * 270, p = T.lin(17, 0.45, i * 0.2);
        icon(ctx, 'playTile', x, 900, 1.0, p, { alpha: 0.55 });
        text(ctx, 'z', x + 70, 790 - 10 * Math.sin(T.t * 2 + i), { size: 34, alpha: T.ap(17, 0.4, 0.6 + i * 0.1) * 0.8, glowK: 0.4 });
        text(ctx, 'z', x + 95, 755 - 10 * Math.sin(T.t * 2 + i + 1), { size: 26, alpha: T.ap(17, 0.4, 0.7 + i * 0.1) * 0.6, glowK: 0.3 });
      });
      label(ctx, 'R$ 45 / MÊS NO TOTAL', CX, 1060, T.ap(17, 0.4, 0.8) * 0.8);
      pill(ctx, '+ R$ 540 / ANO', CX, 1180, { p: T.lin(18, 0.45), size: 40 });
    }
  });

  // 19–20 · junta tudo: R$ 10.672
  groups.push({
    from: 19, draw(ctx, T) {
      const g = T.io(19, 0.6);
      tally(ctx, T, lerp(190, 140, g), lerp(1480, 1080, g), lerp(700, 800, g), lerp(40, 90, g), { full: true, showLabel: false });
      const lbls = [['DELIVERY', 3640], ['LANCHE', 3168], ['PARCELAS', 3324]];
      let acc = 0;
      lbls.forEach(([s, v]) => { label(ctx, s, 140 + 800 * (acc + v / 2) / TOTAL, 1220, T.ap(19, 0.4, 0.5), { size: 20 }); acc += v; });
      text(ctx, 'R$ ' + money(lerp(0, TOTAL, easeOut(T.lin(20, 1.1)))), CX, 870, { size: 140, alpha: T.ap(20, 0.3), glowK: 1.1 });
      label(ctx, 'POR ANO', CX, 980, T.ap(20, 0.4, 0.5) * 0.8);
    }
  });

  // 21–22 · mais de 3 salários
  groups.push({
    from: 21, draw(ctx, T) {
      ground(ctx, 1000, T.ap(21, 0.5), 0.6);
      person(ctx, CX, 1000, { s: 1.0, pop: T.lin(21, 0.4) });
      pill(ctx, 'R$ 3.000 / MÊS', CX, 700, { p: T.lin(21, 0.45, 0.4), size: 30, filled: false });
      // 3,56 salários
      for (let i = 0; i < 4; i++) {
        const x = 200 + i * 175, w = 150, p = T.lin(22, 0.4, i * 0.3);
        const frac = i < 3 ? 1 : 0.56;
        shape(ctx, c => rrect(c, x, 1120, w, 220, 16), { width: 4, alpha: p * 0.6, glowK: 0.3 });
        shape(ctx, c => rrect(c, x + 6, 1120 + 6 + (208 * (1 - frac)) * p, w - 12, Math.max(1, 208 * frac * p), 12), { fill: true, alpha: p * (i < 3 ? 1 : 0.8) });
        text(ctx, i < 3 ? 'R$ 3.000' : '+', x + w / 2, 1380, { size: 26, alpha: p, glowK: 0.3 });
      }
    }
  });

  // 23 · pelo ralo
  groups.push({
    from: 23, draw(ctx, T) {
      icon(ctx, 'drain', CX, 1250, 1.4, T.lin(23, 0.45));
      for (let k = 0; k < 7; k++) {
        const ph = ((T.since(23) * 0.9 + k / 7) % 1 + 1) % 1;
        const sx = CX + Math.sin(k * 2.3) * 300 * (1 - ph);
        const sy = lerp(650, 1240, ph * ph);
        withAlpha(ctx, T.ap(23, 0.3) * (1 - ph * 0.8), () => {
          const sc = 1 - 0.6 * ph;
          ctx.save(); popTransform(ctx, sx, sy, sc);
          N.icons.coin(ctx, sx, sy, 0.35, {});
          ctx.restore();
        });
      }
    }
  });

  // 24–27 · nenhum gasto parece grande / o "só hoje" vira toda semana
  groups.push({
    from: 24, draw(ctx, T) {
      const o1 = 1 - T.ap(26, 0.3);
      withAlpha(ctx, o1, () => {
        const items = [['R$ 35', 240], ['R$ 12', 420], ['R$ 89', 600], ['R$ 45', 780]];
        items.forEach(([s, x], i) => pill(ctx, s, x + 30, 900, { p: T.lin(24, 0.4, 0.3 + i * 0.15), size: 26, filled: false }));
        label(ctx, 'TUDO "PEQUENO"', CX, 1000, T.ap(24, 0.4, 1.0) * 0.8);
        // ninguém sente: pessoa tranquila enquanto gotas passam
        ground(ctx, 1400, T.ap(25, 0.4), 0.5);
        person(ctx, CX, 1400, { s: 0.95, pop: T.lin(25, 0.4) });
        if (T.since(25) > 0) for (let k = 0; k < 3; k++) drips(ctx, T.t, 260 + k * 280, 1080, { fall: 280, alpha: T.ap(25, 0.4) * 0.7, seed: k * 0.3, rate: 1.1 });
      });
      withAlpha(ctx, T.ap(26, 0.3), () => {
        icon(ctx, 'bag', CX, 800, 1.1, T.lin(26, 0.45));
        check(ctx, CX + 170, 700, 40, T.lin(26, 0.5, 0.5));
        label(ctx, 'DELIVERY DE VEZ EM QUANDO', CX, 990, T.ap(26, 0.4, 0.6) * (1 - T.ap(27, 0.3)));
        // o "só hoje" se multiplicando pela semana
        const days = ['S', 'T', 'Q', 'Q', 'S', 'S', 'D'];
        days.forEach((d, i) => {
          const x = 230 + i * 103, y = 1150;
          const on = T.ap(27, 0.25, 0.3 + i * 0.12);
          shape(ctx, c => { c.beginPath(); c.arc(x, y, 38, 0, 7); }, { fill: on > 0.5, width: 4, alpha: 0.4 + 0.6 * T.ap(27, 0.3) , glowK: on > 0.5 ? 1 : 0.2 });
          text(ctx, d, x, y + 2, { size: 26, alpha: T.ap(27, 0.3), color: on > 0.5 ? '0,0,0' : '255,255,255', glowK: 0 });
        });
        pill(ctx, '"SÓ HOJE" × 7', CX, 1300, { p: T.lin(27, 0.45, 1.3), size: 30 });
      });
    }
  });

  // 28–29 · não precisa cortar tudo; precisa enxergar (lupa sobre os furos)
  groups.push({
    from: 28, draw(ctx, T) {
      icon(ctx, 'jar', CX, 980, 1.35, T.lin(28, 0.4), { level: 0.55, t: T.t });
      const holes = [[CX - 60, 1180], [CX + 40, 1182], [CX + 140, 1100]];
      holes.forEach(([hx, hy], i) => { shape(ctx, c => { c.beginPath(); c.arc(hx, hy, 7, 0, 7); }, { fill: true }); drips(ctx, T.t, hx, hy, { seed: i * 0.37, rate: 1.3 + i * 0.25, alpha: T.ap(28, 0.3) }); });
      // tesoura riscada → lupa
      xmark(ctx, CX + 300, 690, 46, T.lin(28, 0.4, 0.5));
      label(ctx, 'CORTAR TUDO', CX + 300, 775, T.ap(28, 0.4, 0.5) * 0.7 * (1 - T.ap(29, 0.3)), { glowK: 0 });
      const m = T.io(29, 0.8, 0.1);
      const mx = lerp(CX + 320, holes[0][0] + 10, m), my = lerp(1400, holes[0][1] - 10, m);
      withAlpha(ctx, T.ap(29, 0.3), () => N.icons.magnifier(ctx, mx, my, 0.9, {}));
    }
  });

  // 30–32 · plano de ação (checklist)
  groups.push({
    from: 30, draw(ctx, T) {
      const rows = [['ANOTE TUDO POR 30 DIAS', 30], ['CANCELE O QUE NÃO USA', 31], ['FECHE 1 VAZAMENTO POR MÊS', 32]];
      rows.forEach(([s, bi], i) => {
        const y = 820 + i * 190, p = T.lin(bi, 0.4);
        withAlpha(ctx, p, () => {
          shape(ctx, c => rrect(c, 175, y - 45, 90, 90, 18), { width: 5 });
          text(ctx, s, 305, y, { size: 34, align: 'left', alpha: 1, glowK: 0.4 });
        });
        if (p > 0) stroke(ctx, [[195, y], [217, y + 24], [247, y - 22]], { p: T.lin(bi, 0.4, 0.5), width: 8 });
      });
    }
  });

  // 33 · gota por gota, o pote enche
  groups.push({
    from: 33, draw(ctx, T) {
      const lv = lerp(0.2, 0.85, easeInOut(T.lin(33, 2.2, 0.2)));
      icon(ctx, 'jar', CX, 1050, 1.35, T.lin(33, 0.4), { level: lv, t: T.t });
      for (let k = 0; k < 4; k++) {
        const ph = ((T.since(33) * 1.4 + k / 4) % 1 + 1) % 1;
        withAlpha(ctx, T.ap(33, 0.3), () => N.icons.drop(ctx, CX, lerp(620, 1000 - lv * 200, ph * ph), 1.1, { alpha: 1 - ph * 0.3 }));
      }
    }
  });

  // 34 · CTA
  groups.push({ from: 34, draw(ctx, T) { N.cta(ctx, T, 34); } });

  return {
    beats: roteiro.beats,
    groups,
    overlay(ctx, T) {
      // contador acumulado dos vazamentos (enquanto as contas são feitas)
      const a = T.ap(8, 0.5) * (1 - T.ap(19, 0.3));
      if (a > 0) withAlpha(ctx, a, () => tally(ctx, T, 190, 1500, 700, 40));
      const d = T.ap(8, 0.6) * 0.75;
      if (d > 0) text(ctx, roteiro.aviso, CX, 1640, { size: 20, weight: 700, color: '160,160,160', spacing: 3, alpha: d, glowK: 0 });
    }
  };
};
