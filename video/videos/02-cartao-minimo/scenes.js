// Cenas do vídeo 02 — "Cartão de crédito: a armadilha do mínimo da fatura"
window.buildVideo = function (roteiro) {
  const N = window.NEON;
  const { text, stroke, curve, person, pill, ground, arrow, xmark, check, icon, money, clamp, lerp, easeOut, easeInOut, easeBack, shape, rrect, withAlpha, arcPts, popTransform } = N;
  const CX = 540;
  const groups = [];

  // botão de app (rrect com texto) — filled = branco com texto preto
  function button(ctx, label, x, y, w, h, o = {}) {
    const { p = 1, filled = false, alpha = 1, size = 32, glowK = 1, scale = 1 } = o;
    if (p <= 0) return;
    ctx.save(); popTransform(ctx, x, y, scale * lerp(0.6, 1, easeBack(p)));
    withAlpha(ctx, alpha * clamp(p * 3), () => {
      shape(ctx, c => rrect(c, x - w / 2, y - h / 2, w, h, h / 2), { fill: filled, width: 5, glowK });
      ctx.font = `900 ${size}px Inter`; ctx.letterSpacing = '4px'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillStyle = filled ? '#000' : '#fff'; ctx.fillText(label, x, y + 2);
    });
    ctx.restore();
  }
  const label = (ctx, s, x, y, a, o = {}) => text(ctx, s, x, y, { size: 24, weight: 800, spacing: 4, alpha: a, glowK: 0.2, ...o });

  // 0–3 · a fatura e o botão "pagar o mínimo"
  groups.push({
    from: 0, draw(ctx, T) {
      const x = CX, top = 600, w = 640, h = 860;
      const relief = T.ap(3, 0.5);
      withAlpha(ctx, T.ap(0, 0.4), () => {
        shape(ctx, c => rrect(c, x - w / 2, top, w, h, 40), { width: 6 });
        label(ctx, 'FATURA DO CARTÃO', x, top + 80, 0.8);
        icon(ctx, 'card', x, top + 230, 0.65, T.lin(0, 0.45, 0.1));
        text(ctx, 'R$ ' + money(lerp(0, 2000, easeOut(T.lin(0, 1.0, 0.3)))), x, top + 430, { size: 110, glowK: 0.9 });
        label(ctx, 'TOTAL', x, top + 510, 0.6, { glowK: 0 });
      });
      button(ctx, 'PAGAR TOTAL', x, top + 620, 470, 84, { p: T.lin(1, 0.4), alpha: 0.4, glowK: 0.2 });
      const pulse = 1 + 0.04 * Math.sin(T.t * 7) * (1 - T.ap(2, 0.3, 1.2));
      const tapped = T.lin(2, 0.2, 1.2);
      button(ctx, T.since(2) > 0.4 ? 'MÍNIMO · R$ 300' : 'PAGAR MÍNIMO', x, top + 740, 470, 84, { p: T.lin(1, 0.45, 0.3), filled: true, scale: pulse * (1 - 0.07 * Math.sin(Math.PI * tapped)), glowK: 1.4 });
      N.finger(ctx, T, 2, x + 300, top + 1050, x + 120, top + 760, 0.3, 1.2);
      // "parece alívio": check grande + bonequinho
      withAlpha(ctx, relief, () => check(ctx, x, top + h + 200, 70, T.lin(3, 0.5)));
    }
  });

  // 4–6 · os R$ 1.700 restantes vão pro rotativo
  groups.push({
    from: 4, draw(ctx, T) {
      const bx = 190, bw = 700, by = 760, bh = 70;
      const payW = bw * 0.15;
      // barra da fatura dividida
      shape(ctx, c => rrect(c, bx, by, payW, bh, [20, 0, 0, 20]), { fill: true, alpha: T.ap(4, 0.4) });
      label(ctx, 'PAGO R$ 300', bx + payW / 2 + 10, by - 40, T.ap(4, 0.4, 0.2));
      // bloco 1.700: fica parado e depois "cai" para o rotativo
      const fall = T.io(5, 0.8, 0.1);
      const restX = lerp(bx + payW + 10, CX - 190, fall), restY = lerp(by, 1270 - 35, fall), restW = lerp(bw - payW - 10, 380, fall);
      shape(ctx, c => rrect(c, restX, restY, restW, bh, lerp(0, 35, fall) + (fall < 0.01 ? 0 : 0)), { width: 5, alpha: T.ap(4, 0.4, 0.3) });
      text(ctx, 'R$ 1.700', restX + restW / 2, restY + bh / 2 + 2, { size: 40, alpha: T.ap(4, 0.4, 0.5), glowK: 0.6 });
      // ciclo do rotativo
      const rp = T.ap(5, 0.5);
      const spin = T.t * (2 + 4 * T.ap(6, 0.6));
      withAlpha(ctx, rp, () => {
        const r = 270, cy = 1270;
        for (let k = 0; k < 3; k++) {
          const a0 = spin + k * (Math.PI * 2 / 3), a1 = a0 + Math.PI * 2 / 3 - 0.35;
          stroke(ctx, arcPts(CX, cy, r, a0, a1, 40), { width: 6, p: rp });
          const ex = CX + r * Math.cos(a1), ey = cy + r * Math.sin(a1), ta = a1 + Math.PI / 2;
          stroke(ctx, [[ex - 22 * Math.cos(ta - 0.6), ey - 22 * Math.sin(ta - 0.6)], [ex, ey], [ex - 22 * Math.cos(ta + 0.6), ey - 22 * Math.sin(ta + 0.6)]], { width: 6, alpha: rp });
        }
        label(ctx, 'ROTATIVO', CX, cy - 90, 1, { size: 30 });
        // "%" orbitando quando os juros aparecem
        const pa = T.ap(6, 0.5);
        for (let k = 0; k < 6; k++) {
          const a = -spin * 0.7 + k * Math.PI / 3;
          text(ctx, '%', CX + (r + 90) * Math.cos(a), cy + (r + 90) * Math.sin(a), { size: 46, alpha: pa * 0.9, glowK: 0.7 });
        }
      });
    }
  });

  // 7–8 · 12% ao mês → deve R$ 1.904
  groups.push({
    from: 7, draw(ctx, T) {
      const up = T.io(8, 0.6);
      text(ctx, '12%', CX, lerp(920, 720, up), { size: lerp(210, 120, up), alpha: T.ap(7, 0.4), glowK: 1 });
      label(ctx, 'AO MÊS · EXEMPLO', CX, lerp(1060, 810, up), T.ap(7, 0.4, 0.4) * 0.8);
      withAlpha(ctx, T.ap(8, 0.4, 0.2), () => {
        text(ctx, 'R$ 1.700', CX, 1000, { size: 56, color: '170,170,170', glowK: 0 });
        text(ctx, '+ R$ 204 DE JUROS', CX, 1080, { size: 40, alpha: T.ap(8, 0.4, 0.7), glowK: 0.4 });
        stroke(ctx, [[CX - 260, 1140], [CX + 260, 1140]], { width: 4, p: T.ap(8, 0.4, 1.1), alpha: 0.7 });
        text(ctx, 'R$ ' + money(lerp(1700, 1904, easeOut(T.lin(8, 0.9, 1.3)))), CX, 1260, { size: 120, alpha: T.ap(8, 0.4, 1.2), glowK: 1 });
        pill(ctx, 'VOCÊ DEVE', CX, 1400, { p: T.lin(8, 0.4, 2.2), size: 30 });
      });
    }
  });

  // 9–11 · dos R$ 300 pagos, só R$ 96 abateram a dívida; R$ 204 foram pro banco
  groups.push({
    from: 9, draw(ctx, T) {
      const bx = 190, bw = 700, by = 920, bh = 90;
      text(ctx, 'R$ 300', CX, 790, { size: 90, alpha: T.ap(9, 0.4), glowK: 0.9 });
      shape(ctx, c => rrect(c, bx, by, bw, bh, 24), { width: 5, alpha: T.ap(9, 0.4, 0.3) });
      const debtW = bw * 96 / 300;
      const d = T.ap(10, 0.6, 0.3);
      shape(ctx, c => rrect(c, bx, by, Math.max(1, debtW * d), bh, [24, 0, 0, 24]), { fill: true, alpha: d });
      label(ctx, 'R$ 96', bx + debtW / 2, by + bh + 50, T.ap(10, 0.4, 0.8), { size: 30 });
      label(ctx, 'DÍVIDA', bx + debtW / 2, by + bh + 90, T.ap(10, 0.4, 0.9) * 0.7, { glowK: 0 });
      const j = T.ap(11, 0.6);
      shape(ctx, c => rrect(c, bx + debtW + 8, by + 8, Math.max(1, (bw - debtW - 16) * j), bh - 16, 16), { fill: true, color: '110,110,110', alpha: j, glowK: 0.2 });
      label(ctx, 'R$ 204 · JUROS', bx + debtW + (bw - debtW) / 2, by + bh + 50, j, { size: 30 });
      // o dinheiro "escorre" pro banco
      icon(ctx, 'bank', CX + 120, 1420, 0.9, T.lin(11, 0.45, 0.3));
      arrow(ctx, bx + debtW + (bw - debtW) / 2, by + bh + 90, CX + 120, 1270, { p: T.ap(11, 0.6, 0.4), width: 5 });
    }
  });

  // 12–15 · o limite continua lá → compras → bola de neve
  groups.push({
    from: 12, draw(ctx, T) {
      // "e o mais perigoso": pulso de luz
      withAlpha(ctx, (1 - T.ap(13, 0.3)) * T.ap(12, 0.4), () => shape(ctx, c => { c.beginPath(); c.arc(CX, 1000, 8 + 4 * Math.sin(T.t * 6), 0, 7); }, { fill: true }));
      const sn = T.ap(15, 0.4);
      withAlpha(ctx, T.ap(13, 0.3) * (1 - sn), () => {
        icon(ctx, 'card', CX, 900, 1.3, T.lin(13, 0.45));
        pill(ctx, 'LIMITE DISPONÍVEL ✓', CX, 1130, { p: T.lin(13, 0.4, 0.4), size: 28, filled: false });
        // compras saindo do cartão
        const buys = ['+ R$ 89', '+ R$ 250', '+ R$ 47', '+ R$ 130'];
        const dests = [[250, 1270], [830, 1270], [330, 1420], [750, 1420]];
        buys.forEach((b, i) => {
          const k = T.lin(14, 0.9, i * 0.22);
          if (k <= 0) return;
          const e = easeOut(k);
          pill(ctx, b, lerp(CX, dests[i][0], e), lerp(900, dests[i][1], e), { p: k, size: 26, alpha: 1 - 0.3 * k });
        });
      });
      // bola de neve rolando ladeira abaixo e crescendo
      withAlpha(ctx, sn, () => {
        const x0 = 120, y0 = 820, x1 = 960, y1 = 1420;
        stroke(ctx, [[x0, y0], [x1, y1]], { width: 4, alpha: 0.6, glowK: 0.3, p: T.ap(15, 0.5) });
        const u = easeInOut(T.lin(15, 1.6, 0.1));
        const r = lerp(25, 125, u);
        const nl = Math.hypot(x1 - x0, y1 - y0), nx = (y1 - y0) / nl, ny = -(x1 - x0) / nl;
        const px = lerp(x0 + 60, x1 - 300, u) + nx * (r + 4), py = lerp(y0 + 43, y1 - 214, u) + ny * (r + 4);
        shape(ctx, c => { c.beginPath(); c.arc(px, py, r, 0, 7); }, { width: 7 });
        const rot = u * 12;
        stroke(ctx, [[px + r * 0.6 * Math.cos(rot), py + r * 0.6 * Math.sin(rot)], [px - r * 0.6 * Math.cos(rot), py - r * 0.6 * Math.sin(rot)]], { width: 4, alpha: 0.5, glowK: 0 });
        text(ctx, 'R$ ' + money(lerp(1904, 3100, u)), px, py - r - 50, { size: 36, alpha: clamp(u * 3), glowK: 0.5 });
      });
    }
  });

  // 16–17 · teto legal: juros ≤ valor da dívida → pode dobrar
  groups.push({
    from: 16, draw(ctx, T) {
      const x0 = 170, y0 = 1400, x1 = 900, cap = 800, base = 1150;
      stroke(ctx, [[x0, 720], [x0, y0], [x1, y0]], { p: T.ap(16, 0.5), width: 3, alpha: 0.6, glowK: 0.3 });
      label(ctx, 'MESES', x1 - 40, y0 + 40, 0.6, { glowK: 0, size: 20 });
      stroke(ctx, [[x0, cap], [x1, cap]], { p: T.ap(16, 0.6, 0.6), width: 4, dash: [16, 14], alpha: 0.8, glowK: 0.3 });
      label(ctx, 'TETO', x1 - 60, cap - 36, T.ap(16, 0.4, 1.0));
      stroke(ctx, [[x0 + 10, base], [x1 - 20, base]], { p: T.ap(16, 0.5, 0.4), width: 3, dash: [6, 12], alpha: 0.5, glowK: 0 });
      label(ctx, 'R$ 1.700', x0 + 100, base + 36, T.ap(16, 0.4, 0.5) * 0.7, { glowK: 0 });
      const debt = curve(u => [lerp(x0 + 10, x1 - 20, u), lerp(base, cap, 1 - Math.exp(-3.2 * u)) ], 80);
      stroke(ctx, debt, { p: T.lin(16, 2.0, 1.0), width: 7, dot: true });
      pill(ctx, '2× A DÍVIDA', CX, 660, { p: T.lin(17, 0.45, 0.6), size: 34 });
      text(ctx, 'R$ 1.700 → R$ 3.400', CX, 1530, { size: 52, alpha: T.ap(17, 0.4, 0.2), glowK: 0.7 });
    }
  });

  // 18–19 · o mínimo não é solução: alívio → empréstimo caro (máscara virando)
  groups.push({
    from: 18, draw(ctx, T) {
      button(ctx, 'PAGAR MÍNIMO', CX, 860, 520, 96, { p: T.lin(18, 0.45), filled: true, glowK: 1.2, alpha: 1 - T.ap(19, 0.3) * 0.6 });
      xmark(ctx, CX + 330, 860, 50, T.lin(18, 0.4, 0.6));
      // cartão-máscara que gira: frente "ALÍVIO", verso "EMPRÉSTIMO CARO"
      const f = T.io(19, 0.7, 1.0);
      const sx = Math.abs(Math.cos(f * Math.PI));
      const back = f > 0.5;
      const a = T.ap(19, 0.4);
      ctx.save(); ctx.translate(CX, 1200); ctx.scale(Math.max(0.02, sx), 1); ctx.translate(-CX, -1200);
      withAlpha(ctx, a, () => {
        shape(ctx, c => rrect(c, CX - 300, 1110, 600, 180, 36), { fill: back, width: 6, glowK: back ? 1.4 : 1 });
        ctx.font = `900 ${back ? 46 : 56}px Inter`; ctx.letterSpacing = '5px'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillStyle = back ? '#000' : '#fff';
        ctx.fillText(back ? 'EMPRÉSTIMO CARO' : 'ALÍVIO', CX, 1203);
      });
      ctx.restore();
    }
  });

  // 20–22 · o que fazer: comparar opções, tirar o cartão da rotina
  groups.push({
    from: 20, draw(ctx, T) {
      const o1 = 1 - T.ap(21, 0.3);
      withAlpha(ctx, o1, () => {
        ground(ctx, 1250, T.ap(20, 0.5));
        person(ctx, CX, 1250, { s: 1.15, pop: T.lin(20, 0.4) });
        pill(ctx, 'R$ 1.904', CX, 920, { p: T.lin(20, 0.4, 0.3), size: 34, filled: false });
        text(ctx, '?', CX + 150, 1010, { size: 90, alpha: T.ap(20, 0.4, 0.6), glowK: 0.8 });
      });
      const o2 = T.ap(21, 0.3) * (1 - T.ap(22, 0.3));
      withAlpha(ctx, o2, () => {
        const cards = [[310, 'PARCELAR', 'A FATURA'], [770, 'EMPRÉSTIMO', 'MAIS BARATO']];
        cards.forEach(([x, l1, l2], i) => {
          const p = T.lin(21, 0.45, 0.3 + i * 0.5);
          ctx.save(); popTransform(ctx, x, 1000, lerp(0.6, 1, easeBack(p)));
          withAlpha(ctx, clamp(p * 3), () => {
            shape(ctx, c => rrect(c, x - 175, 820, 350, 360, 30), { width: 6 });
            label(ctx, l1, x, 950, 1, { size: 32 });
            label(ctx, l2, x, 1000, 0.8, { size: 26 });
            label(ctx, 'TAXA: ?%', x, 1100, 0.7, { size: 26, glowK: 0 });
          });
          ctx.restore();
        });
        text(ctx, 'VS', CX, 1000, { size: 46, alpha: T.ap(21, 0.4, 0.6), glowK: 0.6 });
        pill(ctx, 'ESCOLHA O MENOR CUSTO TOTAL', CX, 1330, { p: T.lin(21, 0.45, 1.6), size: 26 });
      });
      // cartão sendo cortado
      withAlpha(ctx, T.ap(22, 0.3), () => {
        const cut = T.io(22, 0.5, 0.9), sep = 60 * T.io(22, 0.5, 1.3);
        const y = 1000;
        ctx.save(); ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(1080, 0); ctx.lineTo(1080, y - 140); ctx.lineTo(0, y + 140); ctx.closePath(); ctx.clip();
        ctx.translate(-sep * 0.6, -sep);
        N.icons.card(ctx, CX, y, 1.5, {});
        ctx.restore();
        ctx.save(); ctx.beginPath(); ctx.moveTo(1080, y - 140); ctx.lineTo(1080, 1920); ctx.lineTo(0, 1920); ctx.lineTo(0, y + 140); ctx.closePath(); ctx.clip();
        ctx.translate(sep * 0.6, sep);
        N.icons.card(ctx, CX, y, 1.5, {});
        ctx.restore();
        if (cut < 1) stroke(ctx, [[80, y + 160], [1000, y - 160]], { p: cut, width: 4, dash: [18, 14], alpha: 0.9 * (1 - T.ap(22, 0.3, 1.3)), glowK: 0.5 });
        pill(ctx, 'ATÉ ZERAR', CX, 1350, { p: T.lin(22, 0.4, 1.6), size: 32 });
      });
    }
  });

  // 23 · CTA
  groups.push({ from: 23, draw(ctx, T) { N.cta(ctx, T, 23); } });

  return {
    beats: roteiro.beats,
    groups,
    overlay(ctx, T) {
      const a = T.ap(7, 0.6) * 0.75;
      if (a > 0) text(ctx, roteiro.aviso, CX, 1600, { size: 20, weight: 700, color: '160,160,160', spacing: 3, alpha: a, glowK: 0 });
    }
  };
};
