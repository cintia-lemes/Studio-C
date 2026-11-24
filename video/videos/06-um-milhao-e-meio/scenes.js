// Cenas do vídeo 06 — "E se você ganhasse R$ 1,5 milhão hoje?"
// Muita ilustração: app do banco com chuva de notas, itens "comprados" descontando do saldo,
// contas caindo, bifurcação de caminhos, pote que rende, engrenagem, rosca 20/80, coroa.
window.buildVideo = function (roteiro) {
  const N = window.NEON;
  const { text, stroke, curve, person, pill, ground, arrow, xmark, check, icon, money, clamp, lerp, easeOut, easeInOut, easeBack, shape, rrect, withAlpha, arcPts, popTransform, confetti } = N;
  const CX = 540;
  const groups = [];
  const label = (ctx, s, x, y, a, o = {}) => text(ctx, s, x, y, { size: 24, weight: 800, spacing: 4, alpha: a, glowK: 0.2, ...o });
  const brl = v => 'R$ ' + money(v);

  function gear(ctx, x, y, r, rot, a = 1) {
    const pts = [];
    for (let i = 0; i <= 96; i++) { const A = i / 96 * Math.PI * 2; const tooth = (Math.floor(i / 4) % 2) ? 1 : 0.8; pts.push([x + r * tooth * Math.cos(A + rot), y + r * tooth * Math.sin(A + rot)]); }
    stroke(ctx, pts, { width: 7, alpha: a });
    shape(ctx, c => { c.beginPath(); c.arc(x, y, r * 0.35, 0, 7); }, { width: 6, alpha: a });
  }
  function crown(ctx, x, y, s, a = 1) {
    stroke(ctx, [[x - 70 * s, y + 40 * s], [x - 80 * s, y - 40 * s], [x - 35 * s, y], [x, y - 60 * s], [x + 35 * s, y], [x + 80 * s, y - 40 * s], [x + 70 * s, y + 40 * s], [x - 70 * s, y + 40 * s]], { width: 7 * s, alpha: a });
  }
  function infinity(ctx, x, y, s, p) {
    stroke(ctx, curve(u => { const t = u * Math.PI * 2; const d = 1 + Math.sin(t) ** 2; return [x + 180 * s * Math.cos(t) / d, y + 180 * s * Math.sin(t) * Math.cos(t) / d]; }, 120), { width: 10 * s, p, glowK: 1.3 });
  }
  function phoneApp(ctx, T, bal, a) {
    const x = CX, y = 1020, w = 520, h = 880;
    withAlpha(ctx, a, () => {
      shape(ctx, c => rrect(c, x - w / 2, y - h / 2, w, h, 60), { width: 7 });
      stroke(ctx, [[x - 45, y - h / 2 + 36], [x + 45, y - h / 2 + 36]], { width: 6 });
      label(ctx, 'SALDO DISPONÍVEL', x, y - 200, 0.7, { size: 22, glowK: 0 });
      text(ctx, brl(bal) + ',00', x, y - 130, { size: bal >= 1e6 ? 46 : 56, glowK: 1 });
      for (let i = 0; i < 3; i++) shape(ctx, c => rrect(c, x - 200, y + 10 + i * 110, 400, 80, 18), { width: 3, alpha: 0.3, glowK: 0 });
    });
  }

  // 0–2 · o app do banco: notificação, saldo explodindo, confete
  groups.push({
    from: 0, draw(ctx, T) {
      const bal = 1500000 * easeOut(T.lin(1, 1.4, 0.1));
      phoneApp(ctx, T, bal, T.ap(0, 0.4));
      // notificação
      const n = T.lin(0, 0.4, 0.6) * (1 - T.ap(1, 0.3, 1.2));
      ctx.save(); popTransform(ctx, CX, 700, lerp(0.6, 1, easeBack(n)));
      withAlpha(ctx, n, () => {
        shape(ctx, c => rrect(c, CX - 300, 640, 600, 120, 30), { fill: true, glowK: 1.4 });
        withAlpha(ctx, 1, () => { ctx.font = '900 30px Inter'; ctx.letterSpacing = '2px'; ctx.textAlign = 'left'; ctx.fillStyle = '#000'; ctx.fillText('PIX RECEBIDO', CX - 170, 685); ctx.font = '700 24px Inter'; ctx.fillText('Toque para ver o saldo', CX - 170, 722); });
      });
      ctx.restore();
      if (n > 0) withAlpha(ctx, n, () => N.icons.bell(ctx, CX - 235, 695, 0.42, { alpha: 1 }));
      // chuva de notas + confete
      if (T.since(1) > 0.6) { confetti(ctx, T.t, { n: 26, alpha: T.ap(1, 0.5, 0.6), notes: true, y0: 300, fall: 1500, speed: 0.4 }); confetti(ctx, T.t + 3, { n: 60, alpha: T.ap(1, 0.5, 0.6), y0: 250, fall: 1500, speed: 0.55 }); }
      // "o que faria primeiro?" — interrogações
      ['?', '?', '?'].forEach((q, i) => text(ctx, q, [230, 860, 820][i], [760, 820, 1420][i] + 12 * Math.sin(T.t * 3 + i), { size: [110, 80, 70][i], alpha: T.ap(2, 0.4, i * 0.15), glowK: 0.9 }));
    }
  });

  // 3–4 · 2 anos… ou a vida inteira
  groups.push({
    from: 3, draw(ctx, T) {
      const o = 1 - T.ap(4, 0.3);
      withAlpha(ctx, o, () => {
        // ampulheta escorrendo
        const x = CX, y = 1000, s = 1.2, f = T.lin(3, 2.5, 0.2);
        stroke(ctx, [[x - 110 * s, y - 160 * s], [x + 110 * s, y - 160 * s], [x + 10 * s, y], [x + 110 * s, y + 160 * s], [x - 110 * s, y + 160 * s], [x - 10 * s, y], [x - 110 * s, y - 160 * s]], { width: 7, p: T.ap(3, 0.6) });
        withAlpha(ctx, 0.5, () => {
          ctx.fillStyle = '#fff';
          const top = (1 - f); ctx.beginPath(); ctx.moveTo(x - 95 * s * top, y - 20 * s - 120 * s * top); ctx.lineTo(x + 95 * s * top, y - 20 * s - 120 * s * top); ctx.lineTo(x, y - 8 * s); ctx.fill();
          ctx.beginPath(); ctx.moveTo(x - 95 * s * f, y + 150 * s); ctx.lineTo(x + 95 * s * f, y + 150 * s); ctx.lineTo(x, y + 150 * s - 110 * s * f); ctx.fill();
        });
        pill(ctx, '2 ANOS', x, 700, { p: T.lin(3, 0.4, 0.8), size: 34 });
      });
      withAlpha(ctx, T.ap(4, 0.3), () => { infinity(ctx, CX, 1000, 1.3, T.lin(4, 1.0, 0.1)); label(ctx, 'A VIDA INTEIRA', CX, 1250, T.ap(4, 0.4, 0.6), { size: 30 }); });
    }
  });

  // 5–11 · caminho 1: gastar (saldo descontando a cada item)
  const BUY = [[6, 'house', 'CASA', 800000], [7, 'car', 'CARRO', 250000], [8, 'plane', 'VIAGEM', 100000], [9, null, 'FAMÍLIA', 150000], [10, 'gift', 'FESTAS', 200000]];
  groups.push({
    from: 5, draw(ctx, T) {
      let bal = 1500000;
      BUY.forEach(([bi, , , v]) => { bal -= v * easeOut(T.lin(bi, 0.8, 0.5)); });
      const zero = T.ap(11, 0.3);
      // placa "caminho 1"
      withAlpha(ctx, T.ap(5, 0.4) * (1 - T.ap(6, 0.3)), () => {
        stroke(ctx, [[CX, 1350], [CX, 900]], { width: 8 });
        shape(ctx, c => { c.beginPath(); c.moveTo(CX - 200, 820); c.lineTo(CX + 150, 820); c.lineTo(CX + 220, 880); c.lineTo(CX + 150, 940); c.lineTo(CX - 200, 940); c.closePath(); }, { width: 7 });
        text(ctx, 'GASTAR', CX - 10, 882, { size: 50, glowK: 0.8 });
      });
      // saldo no topo
      withAlpha(ctx, T.ap(6, 0.3), () => {
        label(ctx, 'SALDO', CX, 610, 0.7, { glowK: 0 });
        text(ctx, brl(Math.max(0, bal)), CX, 680, { size: 76, glowK: 1, alpha: 1 - 0.3 * zero });
      });
      // grade de itens
      const pos = [[300, 950], [780, 950], [300, 1230], [780, 1230], [CX, 1480]];
      BUY.forEach(([bi, nm, lb, v], i) => {
        const p = T.lin(bi, 0.45), [x, y] = pos[i];
        if (p <= 0) return;
        withAlpha(ctx, 1 - 0.55 * zero, () => {
          if (nm) icon(ctx, nm, x, y - 20, nm === 'car' ? 0.9 : nm === 'plane' ? 0.8 : 0.8, p);
          else { person(ctx, x - 70, y + 50, { s: 0.6, pop: p }); person(ctx, x, y + 50, { s: 0.75, pop: p }); person(ctx, x + 70, y + 50, { s: 0.6, pop: p }); }
          pill(ctx, '− ' + brl(v / 1000) + ' MIL', x, y + 110, { p: T.lin(bi, 0.4, 0.3), size: 24, filled: false });
        });
        if (i === 4 && T.since(10) > 0.2) confetti(ctx, T.t, { n: 30, alpha: T.ap(10, 0.4) * (1 - zero), x0: 330, x1: 750, y0: 1250, fall: 400, speed: 0.6 });
      });
      xmark(ctx, CX + 300, 680, 44, T.lin(11, 0.4, 0.2));
    }
  });

  // 12–16 · as contas não acabam
  const BILLS = ['IPTU', 'CONDOMÍNIO', 'IPVA', 'SEGURO', 'MANUTENÇÃO'];
  groups.push({
    from: 12, draw(ctx, T) {
      const mil = T.ap(15, 0.4);
      // casa + carro ao fundo (patrimônio)
      withAlpha(ctx, 0.35 + 0.65 * mil, () => { N.icons.house(ctx, 270, 1210, 0.9, {}); N.icons.car(ctx, 820, 1250, 0.75, {}); });
      ground(ctx, 1320, 1, 0.5);
      person(ctx, CX, 1320, { s: 1.1, pop: 1, dim: T.ap(16, 0.5) * 0.6 });
      withAlpha(ctx, mil * (1 - T.ap(16, 0.4) * 0.5), () => crown(ctx, CX, 1095 + 4 * Math.sin(T.t * 3), 0.7));
      // contas caindo / empilhando
      BILLS.forEach((b, i) => {
        const p = T.lin(13, 0.5, i * 0.3) || 0, fall = T.since(12) > 0 && i < 2 ? T.lin(12, 0.6, i * 0.25) : 0;
        const k = Math.max(p, fall);
        if (k <= 0) return;
        const y = lerp(450, 640 + i * 68, easeOut(k));
        pill(ctx, b, CX + (i % 2 ? 160 : -160) * (1 - mil * 0.6), y, { p: k, size: 24, filled: false, alpha: 1 - 0.5 * mil });
      });
      pill(ctx, '+ R$ 5.000 / MÊS', CX, 1000, { p: T.lin(14, 0.45, 0.2), size: 36, alpha: 1 - 0.3 * mil });
      pill(ctx, 'SALÁRIO: O MESMO', CX, 1470, { p: T.lin(16, 0.45, 0.2), size: 28, filled: false });
    }
  });

  // 17–19 · caminho 2: o milhão vai trabalhar
  groups.push({
    from: 17, draw(ctx, T) {
      const o = 1 - T.ap(18, 0.3);
      withAlpha(ctx, o, () => {
        // bifurcação: caminho 1 apagado, caminho 2 acende
        stroke(ctx, [[CX, 1500], [CX, 1150]], { width: 8, p: T.ap(17, 0.4) });
        stroke(ctx, curve(u => [CX - 280 * u, 1150 - 380 * u - 40 * Math.sin(u * 3)], 30), { width: 8, p: T.ap(17, 0.5, 0.2), color: '120,120,120', glowK: 0.2 });
        stroke(ctx, curve(u => [CX + 280 * u, 1150 - 380 * u - 40 * Math.sin(u * 3)], 30), { width: 9, p: T.ap(17, 0.6, 0.4), glowK: 1.4 });
        label(ctx, 'CAMINHO 1', CX - 300, 720, 0.4 * T.ap(17, 0.4, 0.3), { glowK: 0 });
        label(ctx, 'CAMINHO 2', CX + 300, 720, T.ap(17, 0.4, 0.6), { size: 30 });
      });
      withAlpha(ctx, T.ap(18, 0.3), () => {
        // pilha de moedas + engrenagens girando
        for (let i = 0; i < 7; i++) shape(ctx, c => { c.beginPath(); c.ellipse(420, 1320 - i * 46, 120, 34, 0, 0, 7); }, { width: 6, alpha: T.ap(18, 0.2, i * 0.08) });
        text(ctx, 'R$ 1,5 MI', 420, 950, { size: 54, alpha: T.ap(18, 0.3, 0.4), glowK: 1 });
        const g = T.ap(19, 0.4);
        gear(ctx, 760, 1080, 110, T.t * 1.2, g);
        gear(ctx, 880, 1270, 75, -T.t * 1.8 + 0.2, g);
        pill(ctx, 'TRABALHANDO', 760, 1450, { p: T.lin(19, 0.4, 0.4), size: 26 });
      });
    }
  });

  // 20–24 · rende R$ 12 mil por mês, todo mês
  groups.push({
    from: 20, draw(ctx, T) {
      icon(ctx, 'jar', 300, 900, 1.2, T.lin(20, 0.4), { level: 0.85, t: T.t });
      label(ctx, 'R$ 1,5 MI', 300, 1140, T.ap(20, 0.4, 0.2), { size: 28 });
      pill(ctx, '0,8% AO MÊS', 300, 1220, { p: T.lin(20, 0.4, 0.6), size: 26 });
      // fluxo de moedas do pote para a pessoa
      ground(ctx, 1300, T.ap(21, 0.4), 0.5);
      person(ctx, 820, 1300, { s: 1.0, pop: T.lin(21, 0.4) });
      if (T.since(21) > 0) for (let k = 0; k < 4; k++) {
        const ph = ((T.since(21) * 0.9 + k / 4) % 1 + 1) % 1;
        withAlpha(ctx, Math.sin(Math.PI * ph) * T.ap(21, 0.3), () => N.icons.coin(ctx, lerp(400, 760, ph), 860 - 160 * Math.sin(Math.PI * ph), 0.26, {}));
      }
      pill(ctx, '+ R$ 12.000 / MÊS', 700, 720, { p: T.lin(21, 0.45, 0.4), size: 32 });
      // 12 meses acendendo
      const ms = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
      ms.forEach((m, i) => {
        const p = T.lin(22, 0.08, 0.1 + i * 0.1), x = 160 + i * 69;
        shape(ctx, c => rrect(c, x - 27, 1400, 54, 64, 10), { fill: p > 0.5, width: 3, alpha: T.ap(22, 0.3) * (0.35 + 0.65 * p), glowK: p > 0.5 ? 0.6 : 0.1 });
        text(ctx, m, x, 1433, { size: 22, color: p > 0.5 ? '0,0,0' : '255,255,255', alpha: T.ap(22, 0.3), glowK: 0 });
      });
      // segundo salário que nunca pede demissão
      withAlpha(ctx, T.ap(23, 0.3), () => {
        pill(ctx, 'SALÁRIO 1', 820, 960, { p: T.lin(23, 0.4), size: 24, filled: false });
        pill(ctx, 'SALÁRIO 2', 820, 1040, { p: T.lin(23, 0.4, 0.4), size: 24 });
      });
      check(ctx, 960, 1040, 32, T.lin(24, 0.5, 0.3));
    }
  });

  // 25–30 · ter os dois: rosca 20/80, sonhos + renda
  groups.push({
    from: 25, draw(ctx, T) {
      const cx = CX, cy = 930, r = 230;
      const p20 = T.lin(26, 0.6, 0.1), p80 = T.lin(27, 0.9, 0.1);
      const a0 = -Math.PI / 2;
      stroke(ctx, arcPts(cx, cy, r, a0 + 0.05, a0 + 0.05 + (Math.PI * 2 * 0.2 - 0.1) * easeOut(p20), 30), { width: 46, glowK: 1.3 });
      stroke(ctx, arcPts(cx, cy, r, a0 + Math.PI * 0.4 + 0.05, a0 + Math.PI * 0.4 + 0.05 + (Math.PI * 2 * 0.8 - 0.1) * easeOut(p80), 90), { width: 40, color: '150,150,150', glowK: 0.3 });
      text(ctx, '20%', cx + 250, cy - 270, { size: 40, alpha: T.ap(26, 0.4, 0.3), glowK: 0.6 });
      text(ctx, '80%', cx - 345, cy + 215, { size: 40, alpha: T.ap(27, 0.4, 0.4), color: '190,190,190', glowK: 0.2 });
      // "os dois": casa + pote no centro
      withAlpha(ctx, T.ap(25, 0.4) * (1 - T.ap(28, 0.3)), () => { N.icons.plane(ctx, cx, cy - 40, 0.55, {}); label(ctx, 'SONHOS + RENDA', cx, cy + 80, 1); });
      // renda caindo no centro
      withAlpha(ctx, T.ap(28, 0.3), () => {
        text(ctx, brl(lerp(0, 9600, easeOut(T.lin(28, 1.0, 0.1)))), cx, cy - 10, { size: 64, glowK: 1 });
        label(ctx, 'POR MÊS', cx, cy + 55, 0.8);
      });
      pill(ctx, 'SONHOS: R$ 300 MIL', 300, 1330, { p: T.lin(26, 0.45, 0.4), size: 24 });
      pill(ctx, 'RENDENDO: R$ 1,2 MI', 780, 1330, { p: T.lin(27, 0.45, 0.4), size: 24, filled: false });
      // reinvestir: seta circular devolvendo parte pro pote
      withAlpha(ctx, T.ap(29, 0.4), () => {
        const sp = T.t * 1.5;
        stroke(ctx, arcPts(cx, cy, r + 90, sp, sp + Math.PI * 1.2, 40), { width: 5, dash: [14, 12], glowK: 0.6 });
        pill(ctx, 'REINVESTE', cx, 1460, { p: T.lin(29, 0.4, 0.3), size: 26 });
      });
      check(ctx, cx + 200, cy + 200, 44, T.lin(30, 0.5, 0.2));
    }
  });

  // 31–34 · a diferença é o que você faz
  groups.push({
    from: 31, draw(ctx, T) {
      const hl = T.ap(32, 0.4);
      const o = 1 - T.ap(33, 0.3);
      withAlpha(ctx, o, () => {
        [[300, 'CAMINHO 1', 'R$ 0', '+ CONTAS'], [780, 'CAMINHO 2', 'R$ 1,2 MI', '+ RENDA']].forEach(([x, a, b, c], i) => {
          const dim = i === 0 ? hl * 0.6 : 0;
          withAlpha(ctx, T.ap(31, 0.4, i * 0.3) * (1 - dim), () => {
            shape(ctx, cc => rrect(cc, x - 200, 800, 400, 440, 34), { width: 6, glowK: i === 1 ? 0.8 + hl : 0.4 });
            label(ctx, a, x, 880, 1, { size: 26 });
            text(ctx, b, x, 1010, { size: 62, glowK: 0.9 });
            label(ctx, c, x, 1110, 0.8, { size: 26 });
          });
        });
        check(ctx, 960, 790, 40, T.lin(32, 0.5, 0.3));
      });
      withAlpha(ctx, T.ap(33, 0.3) * (1 - T.ap(34, 0.3)), () => {
        N.icons.coin(ctx, CX, 950, 1.2, {});
        pill(ctx, 'R$ 1.000', CX, 1200, { p: T.lin(33, 0.4, 0.3), size: 34 });
      });
      withAlpha(ctx, T.ap(34, 0.3), () => {
        ground(ctx, 1320, 1, 0.5);
        person(ctx, CX, 1320, { s: 1.3, pop: T.lin(34, 0.4) });
        crown(ctx, CX, 1040 + 4 * Math.sin(T.t * 3), 0.85, T.ap(34, 0.4, 0.4));
        confetti(ctx, T.t, { n: 40, alpha: T.ap(34, 0.4, 0.6), y0: 400, fall: 1100, speed: 0.4 });
      });
    }
  });

  groups.push({ from: 35, draw(ctx, T) { N.cta(ctx, T, 35); } });

  return {
    beats: roteiro.beats,
    groups,
    overlay(ctx, T) {
      const d = T.ap(12, 0.6) * 0.75;
      if (d > 0) text(ctx, roteiro.aviso, CX, 1660, { size: 19, weight: 700, color: '160,160,160', spacing: 3, alpha: d, glowK: 0 });
    }
  };
};
