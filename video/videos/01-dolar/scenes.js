// Cenas do vídeo 01 — "O dólar subiu: trabalhador x influenciador"
// Cada grupo cobre um conjunto de frases (beats). T.ap(i, dur, delay) = progresso suave a partir da frase i.
window.buildVideo = function (roteiro) {
  const N = window.NEON;
  const { text, stroke, curve, person, pill, ground, arrow, xmark, check, icon, money, clamp, lerp, easeOut, easeInOut, shape, rrect, withAlpha, arcPts } = N;
  const CX = 540, GY = 1200;

  const groups = [];

  // 0 · O DÓLAR SUBIU — moeda + gráfico subindo
  groups.push({
    from: 0, draw(ctx, T) {
      const lift = easeOut(T.lin(0, 1.6, 0.2));
      icon(ctx, 'coin', CX, 820 - 60 * lift, 1.1, T.ap(0, 0.5));
      const x0 = 190, y0 = 1380, x1 = 890;
      stroke(ctx, [[x0, 1000], [x0, y0], [x1, y0]], { p: T.ap(0, 0.5), width: 3, alpha: 0.6, glowK: 0.3 });
      const pts = [[x0 + 10, 1340], [300, 1300], [370, 1320], [450, 1250], [520, 1270], [610, 1190], [680, 1210], [770, 1110], [860, 1060]];
      stroke(ctx, pts, { p: T.lin(0, 1.4, 0.15), width: 7, dot: true });
      arrow(ctx, 900, 1150, 900, 1030, { p: T.ap(0, 0.4, 1.0), alpha: 0.9 });
    }
  });

  // 1–4 · dois brasileiros: trabalhador x influenciador
  groups.push({
    from: 1, draw(ctx, T) {
      ground(ctx, GY, T.ap(1, 0.7));
      stroke(ctx, [[CX, 700], [CX, GY - 10]], { p: T.ap(1, 0.8, 0.3), width: 3, alpha: 0.35, dash: [14, 16], glowK: 0 });
      const dimR = T.ap(2, 0.4) * (1 - T.ap(4, 0.4));
      const dimL = T.ap(4, 0.4);
      person(ctx, 300, GY, { s: 1.15, pop: T.lin(1, 0.5, 0.15), dim: dimL * 0.8 });
      person(ctx, 780, GY, { s: 1.15, pop: T.lin(1, 0.5, 0.35), dim: dimR * 0.8 });
      text(ctx, 'TRABALHADOR', 300, GY + 60, { size: 26, weight: 800, spacing: 4, alpha: T.ap(2, 0.4) * (1 - 0.6 * dimL), glowK: 0.2 });
      text(ctx, 'INFLUENCIADOR', 780, GY + 60, { size: 26, weight: 800, spacing: 4, alpha: T.ap(4, 0.4), glowK: 0.2 });
      pill(ctx, 'R$ 3.000/MÊS', 300, GY - 300, { p: T.lin(3, 0.45), filled: false, size: 30, alpha: 1 - 0.6 * dimL });
      pill(ctx, 'US$ 1.000', 780, GY - 300, { p: T.lin(4, 0.45, 0.9), size: 32 });
      icon(ctx, 'phone', 900, GY - 120, 0.55, T.lin(4, 0.45, 0.5));
    }
  });

  // 5 · câmbio: R$ 5 → R$ 6
  groups.push({
    from: 5, draw(ctx, T) {
      icon(ctx, 'coin', CX, 720, 0.75, T.ap(5, 0.4));
      const v = lerp(5, 6, easeInOut(T.lin(5, 1.1, 0.9)));
      text(ctx, 'R$ ' + money(v, 2), CX - 30, 1000, { size: 150, alpha: T.ap(5, 0.4, 0.2), glowK: 0.9 });
      arrow(ctx, 900, 1060, 900, 930, { p: T.ap(5, 0.5, 1.7) });
      // barra comparando
      const bx = 230, bw = 620;
      shape(ctx, c => rrect(c, bx, 1200, bw, 26, 13), { width: 3, alpha: 0.5 * T.ap(5, 0.4, 0.3), glowK: 0.3 });
      const fill = lerp(5 / 6, 1, easeInOut(T.lin(5, 1.1, 0.9))) * bw * T.ap(5, 0.6, 0.3);
      shape(ctx, c => rrect(c, bx, 1200, Math.max(26, fill), 26, 13), { fill: true, alpha: T.ap(5, 0.4, 0.3) });
      pill(ctx, '+20%', CX, 1350, { p: T.lin(5, 0.45, 2.0), size: 34 });
    }
  });

  // 6–8 · influenciador: US$ 1.000 → R$ 6.000, no sofá, +20%
  groups.push({
    from: 6, draw(ctx, T) {
      ground(ctx, GY, 1);
      const sit = T.io(7, 0.6, 0.1);
      icon(ctx, 'sofa', 310, GY, 1.0, T.lin(7, 0.45));
      person(ctx, 310, GY - 55 * sit, { s: 1.1 - 0.12 * sit, pop: T.lin(6, 0.4) });
      // barras ANTES / AGORA
      const base = GY, bw = 120;
      const h1 = 380 * T.ap(6, 0.6, 0.3), h2 = 456 * easeOut(T.lin(6, 0.9, 1.1));
      const glow2 = 1 + 0.6 * T.ap(8, 0.4);
      shape(ctx, c => rrect(c, 640 - bw / 2, base - h1, bw, Math.max(1, h1), [14, 14, 0, 0]), { width: 5, alpha: 0.55 * T.ap(6, 0.3, 0.3), glowK: 0.4 });
      shape(ctx, c => rrect(c, 850 - bw / 2, base - h2, bw, Math.max(1, h2), [14, 14, 0, 0]), { fill: true, alpha: T.ap(6, 0.3, 1.1), glowK: glow2 });
      text(ctx, 'R$ 5.000', 640, base - h1 - 40, { size: 30, alpha: 0.7 * T.ap(6, 0.4, 0.6), glowK: 0.2 });
      text(ctx, 'R$ ' + money(lerp(5000, 6000, easeOut(T.lin(6, 0.9, 1.1)))), 850, base - h2 - 40, { size: 34, alpha: T.ap(6, 0.4, 1.1) });
      text(ctx, 'ANTES', 640, base + 50, { size: 24, weight: 800, spacing: 4, alpha: 0.6 * T.ap(6, 0.4, 0.3), glowK: 0 });
      text(ctx, 'AGORA', 850, base + 50, { size: 24, weight: 800, spacing: 4, alpha: T.ap(6, 0.4, 1.1), glowK: 0.2 });
      pill(ctx, '+20%', 850, base - 456 - 130, { p: T.lin(8, 0.45, 0.2), size: 36 });
      pill(ctx, 'ZERO ESFORÇO EXTRA', 310, GY - 330, { p: T.lin(7, 0.45, 0.4), filled: false, size: 24, alpha: 1 - T.ap(8, 0.3) * 0.5 });
    }
  });

  // 9–14 · trabalhador: mesmo salário, preços subindo → gráfico salário x preços
  groups.push({
    from: 9, draw(ctx, T) {
      const out = T.ap(13, 0.4);
      withAlpha(ctx, 1 - out, () => {
        ground(ctx, GY, 1);
        person(ctx, CX, GY, { s: 1.15, pop: T.lin(9, 0.4) });
        pill(ctx, 'R$ 3.000', CX, GY - 310, { p: T.lin(9, 0.45, 0.8), filled: false, size: 34 });
        const row = 1420;
        const items = [['phone', 250, 10, 0.75], ['pump', 540, 11, 0.75], ['bread', 830, 12, 0.85]];
        for (const [nm, x, bi, s] of items) {
          icon(ctx, nm, x, row, s, T.lin(bi, 0.45));
          arrow(ctx, x + 95, row + 50, x + 95, row - 60, { p: T.ap(bi, 0.45, 0.35), width: 5, head: 16 });
        }
      });
      // gráfico
      withAlpha(ctx, out, () => {
        const x0 = 170, y0 = 1400, x1 = 900;
        stroke(ctx, [[x0, 720], [x0, y0], [x1, y0]], { p: T.ap(13, 0.5), width: 3, alpha: 0.6, glowK: 0.3 });
        text(ctx, 'TEMPO', x1 - 40, y0 + 40, { size: 20, weight: 800, spacing: 4, alpha: 0.6, glowK: 0 });
        stroke(ctx, [[x0 + 10, 1150], [x1 - 40, 1150]], { p: T.lin(13, 0.8, 0.2), width: 6, dot: true });
        text(ctx, 'SALÁRIO', 760, 1105, { size: 26, weight: 800, spacing: 4, alpha: T.ap(13, 0.4, 0.7), glowK: 0.2 });
        const pr = curve(u => [lerp(x0 + 10, x1 - 40, u), 1150 - 380 * Math.pow(u, 1.8)]);
        stroke(ctx, pr, { p: T.lin(14, 1.0), width: 6, dot: true, dash: null });
        icon(ctx, 'cart', 700, 760, 0.6, T.lin(14, 0.45, 0.9));
        text(ctx, 'PREÇOS', 470, 930, { size: 26, weight: 800, spacing: 4, alpha: T.ap(14, 0.4, 0.6), glowK: 0.2 });
      });
    }
  });

  // 15–16 · gangorra: o mesmo dólar empobrece um e enriquece o outro
  groups.push({
    from: 15, draw(ctx, T) {
      const show = T.ap(16, 0.5);
      // "e o mais cruel": só um pulso de luz
      withAlpha(ctx, (1 - show) * T.ap(15, 0.4), () => shape(ctx, c => { c.beginPath(); c.arc(CX, 1000, 8 + 4 * Math.sin(T.t * 6), 0, 7); }, { fill: true }));
      withAlpha(ctx, show, () => seesaw(ctx, T, 16, -0.24 * T.io(16, 1.2, 0.6), [
        { u: -1, label: 'TRABALHADOR', dimOnTilt: true },
        { u: 1, label: 'INFLUENCIADOR' },
      ]));
    }
  });

  // gangorra genérica com moeda $ como apoio
  function seesaw(ctx, T, bi, ang, riders, opts = {}) {
    const px = CX, py = 1110, L = 380;
    icon(ctx, 'coin', px, py + 72, 0.62, T.ap(bi, 0.4));
    ground(ctx, py + 140, 1, 0.5);
    ctx.save(); ctx.translate(px, py); ctx.rotate(ang);
    stroke(ctx, [[-L, 0], [L, 0]], { p: T.ap(bi, 0.5), width: 8 });
    for (const r of riders) {
      const x = (r.u ?? 0) * (L - 60);
      const dim = r.dimOnTilt ? clamp(Math.abs(ang) / 0.24) * 0.75 : 0;
      ctx.save(); ctx.translate(x, -4); ctx.rotate(-ang);
      person(ctx, 0, 0, { s: r.s || 0.95, pop: r.pop ?? T.lin(bi, 0.4, 0.2), dim });
      if (r.label) text(ctx, r.label, 0, -250, { size: 24, weight: 800, spacing: 4, alpha: T.ap(bi, 0.4, 0.4) * (1 - dim * 0.5), glowK: 0.2 });
      ctx.restore();
    }
    if (opts.endLabels) {
      for (const [u, s] of opts.endLabels) {
        ctx.save(); ctx.translate(u * L, 50); ctx.rotate(-ang);
        text(ctx, s, 0, 0, { size: 24, weight: 800, spacing: 3, alpha: T.ap(bi, 0.4, 0.3), glowK: 0.2 });
        ctx.restore();
      }
    }
    ctx.restore();
    // setas indicando quem sobe / desce
    if (opts.arrows !== false) {
      const k = clamp(Math.abs(ang) / 0.2);
      arrow(ctx, px - L - 40, 1040, px - L - 40, 1160, { p: k, width: 5, head: 16, alpha: 0.7 });
      arrow(ctx, px + L + 40, 1160, px + L + 40, 1040, { p: k, width: 5, head: 16 });
    }
  }

  // 17–19 · o salário em dólar caiu; ficou mais pobre
  groups.push({
    from: 17, draw(ctx, T) {
      const v = lerp(600, 500, easeInOut(T.lin(17, 1.0, 1.6)));
      text(ctx, 'US$ ' + money(v), CX - 20, 800, { size: 130, alpha: T.ap(17, 0.4), glowK: 0.9 });
      arrow(ctx, 905, 730, 905, 860, { p: T.ap(17, 0.5, 2.4) });
      const bx = 230, bw = 620;
      shape(ctx, c => rrect(c, bx, 920, bw, 24, 12), { width: 3, alpha: 0.5 * T.ap(17, 0.4, 0.2), glowK: 0.3 });
      shape(ctx, c => rrect(c, bx, 920, bw * (v / 600) * T.ap(17, 0.6, 0.2), 24, 12), { fill: true, alpha: T.ap(17, 0.4, 0.2) });
      ground(ctx, GY + 120, T.ap(18, 0.5));
      const poor = T.ap(19, 0.6);
      person(ctx, CX, GY + 120, { s: 1.1 - 0.15 * poor, pop: T.lin(18, 0.45), dim: poor * 0.7 });
      pill(ctx, 'EMPREGO MANTIDO', CX, GY - 150, { p: T.lin(18, 0.45, 0.35), filled: false, size: 26, alpha: 1 - poor });
      pill(ctx, '− PODER DE COMPRA', CX, GY - 150, { p: T.lin(19, 0.45, 0.2), size: 28 });
    }
  });

  // 20–21 · você não controla o dólar / escolha o lado da balança
  groups.push({
    from: 20, draw(ctx, T) {
      const out = T.ap(21, 0.4);
      withAlpha(ctx, 1 - out, () => {
        const pts = curve(u => {
          const x = lerp(160, 920, u);
          const y = 1050 - 120 * Math.sin(u * 9) * Math.cos(u * 4.3) - 60 * Math.sin(u * 23) - 120 * u;
          return [x, y];
        }, 140);
        stroke(ctx, pts, { p: T.lin(20, 1.0), width: 6, dot: true });
        xmark(ctx, CX, 1330, 60, T.lin(20, 0.4, 0.8));
      });
      withAlpha(ctx, out, () => {
        const walk = T.io(21, 1.2, 0.5);
        seesaw(ctx, T, 21, -0.2 * T.io(21, 0.8, 0.2), [
          { u: lerp(0, 1, walk), label: 'VOCÊ', s: 0.95 },
        ], { endLabels: [[-1, 'SÓ EM REAL'], [1, 'PARTE EM DÓLAR']], arrows: false });
      });
    }
  });

  // 22–23 · reserva em dólar = proteção (rosca + escudo)
  groups.push({
    from: 22, draw(ctx, T) {
      const cx = CX, cy = 980, r = 250;
      const p = T.lin(22, 1.2, 0.2);
      const a0 = -Math.PI / 2, split = a0 + Math.PI * 2 * 0.8;
      stroke(ctx, arcPts(cx, cy, r, a0, split - 0.06, 100), { p: clamp(p / 0.8), width: 34, color: '120,120,120', glowK: 0.2 });
      const usd = arcPts(cx, cy, r, split + 0.06, a0 + Math.PI * 2 - 0.06, 40);
      stroke(ctx, usd, { p: clamp((p - 0.8) / 0.2), width: 40, glowK: 1.2 + 0.8 * T.ap(23, 0.4) });
      text(ctx, 'R$', cx - r - 70, cy + 120, { size: 40, color: '170,170,170', alpha: T.ap(22, 0.4, 0.6), glowK: 0 });
      text(ctx, 'US$', cx - 150, cy - r - 70, { size: 40, alpha: T.ap(22, 0.4, 1.3) });
      // conteúdo central: "luxo" riscado → escudo
      const sh = T.ap(23, 0.4);
      withAlpha(ctx, 1 - sh, () => {
        text(ctx, 'LUXO', cx, cy, { size: 54, spacing: 6, alpha: T.ap(22, 0.4, 1.4), glowK: 0.4 });
        stroke(ctx, [[cx - 110, cy + 5], [cx + 110, cy - 5]], { p: T.ap(22, 0.4, 1.9), width: 7 });
      });
      withAlpha(ctx, sh, () => {
        N.icons.shield(ctx, cx, cy, 1.05, { p: T.lin(23, 0.7) });
        text(ctx, '$', cx, cy + 6, { size: 110, alpha: T.ap(23, 0.4, 0.3), glowK: 0.9 });
      });
    }
  });

  // 24 · habilidade paga em dólar
  groups.push({
    from: 24, draw(ctx, T) {
      icon(ctx, 'bulb', 280, 900, 1.0, T.lin(24, 0.45), { rays: T.ap(24, 0.4, 0.3) });
      stroke(ctx, [[400, 900], [650, 900]], { p: T.ap(24, 0.6, 0.5), width: 4, dash: [14, 14], alpha: 0.7, glowK: 0 });
      icon(ctx, 'globe', 780, 900, 1.0, T.lin(24, 0.45, 0.9));
      stroke(ctx, [[780, 1020], [780, 1230]], { p: T.ap(24, 0.6, 1.5), width: 4, dash: [14, 14], alpha: 0.7, glowK: 0 });
      icon(ctx, 'coin', 780, 1340, 0.85, T.lin(24, 0.45, 2.0));
      pill(ctx, '+ US$', 560, 1340, { p: T.lin(24, 0.45, 2.5), size: 32 });
      text(ctx, 'HABILIDADE', 280, 1080, { size: 24, weight: 800, spacing: 4, alpha: T.ap(24, 0.4, 0.4), glowK: 0.2 });
      text(ctx, 'MUNDO', 900, 1050, { size: 24, weight: 800, spacing: 4, alpha: T.ap(24, 0.4, 1.1), glowK: 0.2 });
    }
  });

  // 25 · CTA: siga o perfil
  groups.push({
    from: 25, draw(ctx, T) {
      const p = T.lin(25, 0.5);
      const x = CX, y = 1020, w = 470, h = 820;
      withAlpha(ctx, p, () => {
        shape(ctx, c => rrect(c, x - w / 2, y - h / 2, w, h, 56), { width: 7 });
        stroke(ctx, [[x - 40, y - h / 2 + 34], [x + 40, y - h / 2 + 34]], { width: 6 });
        // avatar
        shape(ctx, c => { c.beginPath(); c.arc(x, y - 190, 95, 0, 7); }, { width: 6 });
        ctx.save(); ctx.beginPath(); ctx.arc(x, y - 190, 92, 0, 7); ctx.clip();
        person(ctx, x, y - 95, { s: 0.85 });
        ctx.restore();
        stroke(ctx, [[x - 120, y - 40], [x + 120, y - 40]], { width: 14, alpha: 0.8 });
        stroke(ctx, [[x - 80, y + 5], [x + 80, y + 5]], { width: 10, alpha: 0.4, glowK: 0 });
        for (let i = 0; i < 3; i++) for (let j = 0; j < 2; j++)
          shape(ctx, c => rrect(c, x - 190 + i * 130, y + 200 + j * 140, 115, 125, 12), { width: 3, alpha: 0.35, glowK: 0 });
      });
      // botão seguir → seguindo
      const tap = T.lin(25, 0.15, 1.3), done = tap >= 1;
      const bs = 1 - 0.08 * Math.sin(Math.PI * tap);
      ctx.save(); N.popTransform(ctx, x, y + 95, bs * N.lerp(0.5, 1, N.easeBack(T.lin(25, 0.4, 0.4))));
      withAlpha(ctx, T.ap(25, 0.3, 0.4), () => {
        shape(ctx, c => rrect(c, x - 150, y + 60, 300, 72, 36), { fill: !done, width: 5, glowK: 1.2 });
        ctx.font = '900 32px Inter'; ctx.letterSpacing = '4px'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillStyle = done ? '#fff' : '#000';
        ctx.fillText(done ? 'SEGUINDO ✓' : 'SEGUIR', x, y + 98);
      });
      ctx.restore();
      // dedo tocando
      const fp = T.io(25, 0.7, 0.6), fx = lerp(x + 330, x + 40, fp), fy = lerp(y + 400, y + 120, fp);
      withAlpha(ctx, T.ap(25, 0.3, 0.6) * (1 - T.ap(25, 0.4, 1.8)), () => {
        shape(ctx, c => { c.beginPath(); c.arc(fx, fy, 30, 0, 7); }, { width: 5 });
        if (tap > 0 && tap < 1) shape(ctx, c => { c.beginPath(); c.arc(fx, fy, 30 + 60 * tap, 0, 7); }, { width: 3, alpha: 1 - tap });
      });
    }
  });

  return {
    beats: roteiro.beats,
    groups,
    overlay(ctx, T) {
      // aviso legal discreto a partir da frase 22
      const a = T.ap(22, 0.6) * 0.75;
      if (a > 0) text(ctx, roteiro.aviso, CX, 1600, { size: 20, weight: 700, color: '160,160,160', spacing: 3, alpha: a, glowK: 0 });
    }
  };
};
