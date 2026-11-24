// Cenas do vídeo 07 — "Ego, disciplina e obsessão"
// Três símbolos guiam o vídeo: COROA (ego), CALENDÁRIO (disciplina), ALVO (obsessão).
window.buildVideo = function (roteiro) {
  const N = window.NEON;
  const { text, stroke, curve, person, pill, ground, arrow, xmark, check, icon, money, clamp, lerp, easeOut, easeInOut, easeBack, shape, rrect, withAlpha, arcPts, popTransform, confetti } = N;
  const CX = 540;
  const groups = [];
  const label = (ctx, s, x, y, a, o = {}) => text(ctx, s, x, y, { size: 24, weight: 800, spacing: 4, alpha: a, glowK: 0.2, ...o });

  // ---------- símbolos ----------
  function crown(ctx, x, y, s, a = 1, p = 1) {
    stroke(ctx, [[x - 70 * s, y + 40 * s], [x - 80 * s, y - 40 * s], [x - 35 * s, y], [x, y - 60 * s], [x + 35 * s, y], [x + 80 * s, y - 40 * s], [x + 70 * s, y + 40 * s], [x - 70 * s, y + 40 * s]], { width: 7 * s, alpha: a, p });
  }
  function target(ctx, x, y, s, a = 1, p = 1) {
    [1, 0.66, 0.33].forEach((k, i) => stroke(ctx, arcPts(x, y, 110 * s * k, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * clamp(p * 1.4 - i * 0.2), 60), { width: 7 * s, alpha: a }));
    if (p > 0.8) shape(ctx, c => { c.beginPath(); c.arc(x, y, 10 * s, 0, 7); }, { fill: true, alpha: a });
  }
  function calCheck(ctx, x, y, s, a = 1) { withAlpha(ctx, a, () => { N.icons.calendar(ctx, x, y, s, { label: ' ' }); stroke(ctx, [[x - 40 * s, y + 30 * s], [x - 10 * s, y + 60 * s], [x + 45 * s, y]], { width: 10 * s }); }); }
  function bolt(ctx, x, y, s, a = 1) { shape(ctx, c => { c.beginPath(); c.moveTo(x + 10 * s, y - 60 * s); c.lineTo(x - 30 * s, y + 8 * s); c.lineTo(x, y + 8 * s); c.lineTo(x - 10 * s, y + 60 * s); c.lineTo(x + 30 * s, y - 8 * s); c.lineTo(x, y - 8 * s); c.closePath(); }, { fill: true, alpha: a, glowK: 1.3 }); }
  function sun(ctx, x, y, s, a = 1, t = 0) { withAlpha(ctx, a, () => { shape(ctx, c => { c.beginPath(); c.arc(x, y, 34 * s, 0, 7); }, { width: 6 * s }); for (let k = 0; k < 8; k++) { const A = k * Math.PI / 4 + t * 0.5; stroke(ctx, [[x + 50 * s * Math.cos(A), y + 50 * s * Math.sin(A)], [x + 66 * s * Math.cos(A), y + 66 * s * Math.sin(A)]], { width: 5 * s }); } }); }
  function cloud(ctx, x, y, s, a = 1, t = 0) {
    withAlpha(ctx, a, () => {
      stroke(ctx, [...arcPts(x - 40 * s, y, 30 * s, Math.PI * 0.5, Math.PI * 1.5, 14), ...arcPts(x - 5 * s, y - 25 * s, 38 * s, Math.PI, Math.PI * 1.95, 14), ...arcPts(x + 40 * s, y, 30 * s, Math.PI * 1.5, Math.PI * 2.5, 14), [x - 40 * s, y + 30 * s]], { width: 6 * s });
      for (let k = 0; k < 3; k++) { const ph = (t * 1.5 + k / 3) % 1; stroke(ctx, [[x - 30 * s + k * 30 * s, y + 45 * s + ph * 50 * s], [x - 38 * s + k * 30 * s, y + 65 * s + ph * 50 * s]], { width: 5 * s, alpha: 1 - ph }); }
    });
  }
  function moon(ctx, x, y, s, a = 1) { withAlpha(ctx, a, () => { ctx.save(); shape(ctx, c => { c.beginPath(); c.arc(x, y, 50 * s, Math.PI * 0.35, Math.PI * 1.65); c.arc(x + 28 * s, y - 10 * s, 40 * s, Math.PI * 1.5, Math.PI * 0.55, true); c.closePath(); }, { width: 6 * s }); ctx.restore(); }); }
  function dice(ctx, x, y, s, a = 1, rot = 0) {
    withAlpha(ctx, a, () => { ctx.save(); ctx.translate(x, y); ctx.rotate(rot); shape(ctx, c => rrect(c, -70 * s, -70 * s, 140 * s, 140 * s, 22 * s), { width: 7 * s }); for (const [dx, dy] of [[-35, -35], [0, 0], [35, 35], [35, -35], [-35, 35]]) shape(ctx, c => { c.beginPath(); c.arc(dx * s, dy * s, 10 * s, 0, 7); }, { fill: true }); ctx.restore(); });
  }

  // 0–1 · três coisas: coroa · calendário · alvo
  groups.push({
    from: 0, draw(ctx, T) {
      const j = T.ap(1, 0.4);
      // abertura: duas pessoas — uma "parece rico" (coroa brilhando), outra "é rico" (pote cheio)
      withAlpha(ctx, 1 - j, () => {
        ground(ctx, 1250, T.ap(0, 0.5), 0.5);
        person(ctx, 330, 1250, { s: 1.1, pop: T.lin(0, 0.4) });
        crown(ctx, 330, 1020 + 4 * Math.sin(T.t * 3), 0.6, T.ap(0, 0.4, 0.5));
        label(ctx, 'PARECE RICO', 330, 1300, T.ap(0, 0.4, 0.6));
        person(ctx, 750, 1250, { s: 1.1, pop: T.lin(0, 0.4, 0.3) });
        icon(ctx, 'jar', 860, 1170, 0.4, T.lin(0, 0.4, 1.0), { level: 0.8, t: T.t });
        label(ctx, 'É RICO', 750, 1300, T.ap(0, 0.4, 1.1));
      });
      const syms = [[260, (x, y, a) => crown(ctx, x, y, 1.1, a, T.ap(1, 0.5))], [CX, (x, y, a) => calCheck(ctx, x, y, 0.85, a)], [820, (x, y, a) => target(ctx, x, y, 0.9, a, T.lin(1, 0.7, 0.8))]];
      syms.forEach(([x, fn], i) => {
        const p = T.lin(1, 0.4, i * 0.4);
        if (p <= 0) return;
        ctx.save(); popTransform(ctx, x, 980, lerp(0.5, 1, easeBack(p))); fn(x, 980, clamp(p * 3)); ctx.restore();
        label(ctx, ['EGO', 'DISCIPLINA', 'OBSESSÃO'][i], x, 1160, p, { size: 28 });
      });
    }
  });

  // 2–7 · ego: o balão do ego infla com compras… e estoura
  groups.push({
    from: 2, draw(ctx, T) {
      const inflate = T.io(3, 1.0) * 0.5 + T.io(4, 1.2) * 0.4 + T.io(5, 1.0) * 0.25;
      const pop = T.lin(6, 0.35, 0.3);
      const o = 1 - T.ap(7, 0.3);
      withAlpha(ctx, o, () => {
        ground(ctx, 1380, T.ap(2, 0.5), 0.5);
        person(ctx, CX, 1380, { s: 1.0, pop: T.lin(2, 0.4) });
        crown(ctx, CX, 1150, 0.6, T.ap(2, 0.4, 0.3) * (1 - pop));
        // balão do ego
        const r = lerp(70, 195, inflate);
        if (pop < 1) withAlpha(ctx, T.ap(3, 0.3) * (1 - pop), () => {
          stroke(ctx, [[CX, 1110], [CX, 1000 - r * 0.1]], { width: 3, alpha: 0.6, glowK: 0 });
          shape(ctx, c => { c.beginPath(); c.ellipse(CX, 960 - r, r * 0.9, r, 0, 0, 7); }, { width: 7, glowK: 1.2 });
          text(ctx, 'EGO', CX, 960 - r, { size: lerp(40, 110, inflate), glowK: 0.9 });
        });
        // estouro
        if (pop > 0 && pop < 1) for (let k = 0; k < 12; k++) { const A = k * Math.PI / 6; stroke(ctx, [[CX + Math.cos(A) * (80 + 200 * pop), 700 + Math.sin(A) * (80 + 200 * pop)], [CX + Math.cos(A) * (130 + 260 * pop), 700 + Math.sin(A) * (130 + 260 * pop)]], { width: 6, alpha: 1 - pop }); }
        // compras que inflam o ego
        const items = [['car', 220, 'FINANCIADO'], ['bag', 860, 'MARCA'], ['phone', 860, 'FOTO']];
        items.forEach(([nm, x, lb], i) => {
          const p = T.lin(4, 0.4, i * 0.35), y = [1150, 1000, 1280][i];
          withAlpha(ctx, 1 - T.ap(6, 0.3), () => { icon(ctx, nm, x, y, nm === 'car' ? 0.6 : 0.5, p); label(ctx, lb, x, y + 90, p * 0.8, { size: 20 }); });
        });
        // plateia que nem lembra: bonecos virando cinza e sumindo
        [150, 930].forEach((x, i) => person(ctx, x, 1380, { s: 0.7, pop: T.lin(5, 0.4, i * 0.2), dim: T.ap(5, 0.8, 0.8) * 0.9, alpha: 1 - T.ap(5, 0.6, 1.4) * 0.7 }));
        pill(ctx, 'EGO ✕', CX, 700, { p: T.lin(6, 0.4, 0.6), size: 34 });
      });
      // ser > parecer
      withAlpha(ctx, T.ap(7, 0.3), () => {
        const bx = 220, base = 1300;
        shape(ctx, c => rrect(c, bx, base - 520 * T.ap(7, 0.6, 0.2), 220, 520 * T.ap(7, 0.6, 0.2), 16), { fill: true, glowK: 1.2 });
        shape(ctx, c => rrect(c, bx + 420, base - 160 * T.ap(7, 0.6, 0.4), 220, 160 * T.ap(7, 0.6, 0.4), 16), { width: 5, glowK: 0.3 });
        label(ctx, 'SER RICO', bx + 110, base + 45, 1, { size: 28 });
        label(ctx, 'PARECER RICO', bx + 530, base + 45, 0.7, { size: 28, glowK: 0 });
        text(ctx, '>', CX, 1150, { size: 120, glowK: 1, alpha: T.ap(7, 0.4, 0.6) });
        ground(ctx, base, 1, 0.5);
      });
    }
  });

  // 8–13 · disciplina: 1 dia de motivação × todos os dias de disciplina; aporte faça chuva ou sol
  groups.push({
    from: 8, draw(ctx, T) {
      const o1 = 1 - T.ap(11, 0.3);
      withAlpha(ctx, o1, () => {
        calCheck(ctx, CX, 800, 0.8, T.ap(8, 0.4) * (1 - T.ap(9, 0.3)));
        // grade de 30 dias
        for (let i = 0; i < 30; i++) {
          const col = i % 7, row = Math.floor(i / 7), x = 230 + col * 103, y = 860 + row * 100;
          const ga = T.ap(9, 0.3);
          const motiv = i === 3 ? T.ap(9, 0.3, 0.4) : 0;
          const disc = T.lin(10, 0.06, 0.1 + i * 0.045);
          shape(ctx, c => rrect(c, x - 40, y - 40, 80, 80, 14), { fill: disc > 0.5, width: 3, alpha: ga * (0.35 + 0.65 * Math.max(motiv, disc)), glowK: disc > 0.5 ? 0.6 : 0.1 });
          if (motiv > 0 && disc < 0.5) bolt(ctx, x, y, 0.5, motiv);
          if (disc > 0.5) stroke(ctx, [[x - 18, y], [x - 4, y + 15], [x + 20, y - 14]], { width: 6, color: '0,0,0', glowK: 0 });
        }
        label(ctx, 'MOTIVAÇÃO', 230 + 3 * 103, 790, T.ap(9, 0.3, 0.6) * (1 - T.ap(10, 0.3)), { size: 22 });
      });
      // investir quando ninguém olha: noite, lua, pessoa sozinha + pote
      const o2 = T.ap(11, 0.3) * (1 - T.ap(12, 0.3));
      withAlpha(ctx, o2, () => {
        moon(ctx, 820, 720, 1.2, 1);
        for (let k = 0; k < 10; k++) shape(ctx, c => { c.beginPath(); c.arc(150 + (k * 97) % 800, 640 + (k * 53) % 260, 3, 0, 7); }, { fill: true, alpha: 0.5 + 0.5 * Math.sin(T.t * 2 + k) });
        ground(ctx, 1350, 1, 0.5);
        person(ctx, 360, 1350, { s: 1.0, pop: 1 });
        icon(ctx, 'jar', 680, 1200, 0.8, 1, { level: 0.4 + 0.1 * T.lin(11, 1.5), t: T.t });
        const ph = (T.since(11) * 0.8) % 1;
        withAlpha(ctx, Math.sin(Math.PI * ph), () => N.icons.coin(ctx, lerp(420, 680, ph), 1000 - 100 * Math.sin(Math.PI * ph), 0.25, {}));
      });
      // mês bom, ruim, sem vontade → mesmo aporte
      withAlpha(ctx, T.ap(12, 0.3), () => {
        const cols = [[230, 'BOM'], [CX, 'RUIM'], [850, 'SEM VONTADE']];
        cols.forEach(([x, lb], i) => {
          const p = T.lin(12, 0.4, i * 0.35);
          withAlpha(ctx, p, () => {
            if (i === 0) sun(ctx, x, 820, 1.1, 1, T.t); else if (i === 1) cloud(ctx, x, 820, 1.2, 1, T.t); else { text(ctx, 'z', x - 20, 830, { size: 60, glowK: 0.6 }); text(ctx, 'z', x + 25, 780, { size: 44, glowK: 0.5 }); text(ctx, 'z', x + 55, 740, { size: 30, glowK: 0.4 }); }
            label(ctx, 'MÊS ' + lb, x, 940, 1, { size: 20 });
          });
          icon(ctx, 'jar', x, 1200, 0.65, T.lin(13, 0.4, i * 0.15), { level: 0.55, t: T.t + i });
          pill(ctx, 'APORTE ✓', x, 1370, { p: T.lin(13, 0.4, 0.4 + i * 0.25), size: 22 });
        });
      });
    }
  });

  // 14–19 · obsessão pelo processo: alvo, ciclo, atalho x caminho construído
  const LOOP = ['APRENDER', 'MELHORAR', 'GANHAR +', 'GASTAR −'];
  groups.push({
    from: 14, draw(ctx, T) {
      const o1 = 1 - T.ap(16, 0.3);
      withAlpha(ctx, o1, () => {
        target(ctx, CX, 950, 1.6, 1, T.lin(14, 0.9));
        // flecha chegando no centro
        const f = T.io(14, 0.5, 0.8);
        if (f > 0) arrow(ctx, lerp(950, CX + 30, f), lerp(700, 930, f), CX + 10, 945, { p: 1, width: 6, head: 22 });
        withAlpha(ctx, T.ap(15, 0.3), () => { text(ctx, 'R$', CX, 1300, { size: 80, glowK: 0.8 }); });
        xmark(ctx, CX + 110, 1290, 40, T.lin(15, 0.4, 0.3));
      });
      // ciclo do processo
      const o2 = T.ap(16, 0.3) * (1 - T.ap(18, 0.3));
      withAlpha(ctx, o2, () => {
        const cx = CX, cy = 1000, R = 300, spin = T.t * (0.6 + 1.6 * T.ap(17, 0.5));
        stroke(ctx, arcPts(cx, cy, R, spin, spin + Math.PI * 1.7, 80), { width: 5, dash: [16, 14], glowK: 0.6 });
        LOOP.forEach((s, i) => {
          const A = -Math.PI / 2 + i * Math.PI / 2;
          pill(ctx, s, cx + R * Math.cos(A), cy + R * Math.sin(A), { p: T.lin(17, 0.35, 0.1 + i * 0.35), size: 24, filled: i % 2 === 0 });
        });
        text(ctx, '↻', cx, cy, { size: 140, alpha: T.ap(16, 0.4, 0.3), glowK: 1 });
        label(ctx, 'REPETIR', cx, cy + 110, T.ap(17, 0.4, 1.6), { size: 28 });
      });
      // atalho x caminho
      withAlpha(ctx, T.ap(18, 0.3), () => {
        // atalho: placa com seta para um buraco
        shape(ctx, c => { c.beginPath(); c.moveTo(130, 760); c.lineTo(380, 760); c.lineTo(430, 810); c.lineTo(380, 860); c.lineTo(130, 860); c.closePath(); }, { width: 5 });
        text(ctx, 'ATALHO', 270, 812, { size: 34, glowK: 0.6 });
        stroke(ctx, [[260, 860], [260, 1000]], { width: 6 });
        [170, 260, 350].forEach((x, i) => person(ctx, x, 1150, { s: 0.6, pop: T.lin(18, 0.3, i * 0.15), dim: 0.6 }));
        text(ctx, '?', 400, 1000, { size: 70, alpha: T.ap(18, 0.3, 0.6), glowK: 0.4 });
        // escada sendo construída degrau por degrau
        const steps = 6;
        for (let i = 0; i < steps; i++) {
          const p = T.lin(19, 0.18, 0.1 + i * 0.22);
          shape(ctx, c => rrect(c, 560 + i * 70, 1350 - (i + 1) * 70, 70, (i + 1) * 70, 6), { width: 4, fill: p > 0.5, alpha: 0.2 + 0.8 * p, glowK: p > 0.5 ? 0.6 : 0.1 });
        }
        const top = clamp(T.lin(19, 1.4, 0.2) * steps - 0.5, 0, steps - 1);
        person(ctx, 595 + top * 70, 1350 - (Math.floor(top) + 1) * 70, { s: 0.6, pop: T.lin(19, 0.3) });
        ground(ctx, 1350, 1, 0.5);
      });
    }
  });

  // 20–24 · os três juntos → curva que o tempo multiplica
  groups.push({
    from: 20, draw(ctx, T) {
      const m = T.io(20, 0.9, 0.2);
      // símbolos convergindo
      withAlpha(ctx, 1 - T.ap(21, 0.3), () => {
        crown(ctx, lerp(240, CX - 60, m), lerp(900, 980, m), 0.8, 1 - m * 0.5);
        calCheck(ctx, CX, lerp(800, 980, m), 0.6, 1 - m * 0.5);
        target(ctx, lerp(840, CX + 60, m), lerp(900, 980, m), 0.7, 1 - m * 0.5);
        if (m > 0.8) shape(ctx, c => { c.beginPath(); c.arc(CX, 980, 40 + 400 * (m - 0.8), 0, 7); }, { width: 5, alpha: 1 - (m - 0.8) * 5 });
      });
      // três linhas de efeito
      const rows = [[21, 'SEM EGO', 'GASTA MENOS', '↓'], [22, 'DISCIPLINA', 'INVESTE SEMPRE', '✓'], [23, 'OBSESSÃO', 'GANHA MAIS', '↑']];
      const o = 1 - T.ap(24, 0.3);
      rows.forEach(([bi, a, b, sym], i) => {
        const p = T.lin(bi, 0.4), y = 800 + i * 200;
        withAlpha(ctx, p * o, () => {
          shape(ctx, c => rrect(c, 150, y - 70, 780, 140, 30), { width: 5, glowK: 0.6 });
          label(ctx, a, 330, y - 20, 0.7, { size: 22, glowK: 0 });
          text(ctx, b, 330, y + 25, { size: 34, glowK: 0.5 });
          text(ctx, sym, 820, y, { size: 80, glowK: 1 });
        });
      });
      // tempo multiplicando: curva exponencial + relógio
      withAlpha(ctx, T.ap(24, 0.3), () => {
        const ox = 170, oy = 1380, w = 740;
        stroke(ctx, [[ox, 680], [ox, oy], [ox + w, oy]], { width: 3, alpha: 0.6, glowK: 0.2 });
        stroke(ctx, curve(u => [ox + u * w, oy - 640 * (Math.exp(3 * u) - 1) / (Math.exp(3) - 1)], 80), { p: T.lin(24, 1.0, 0.2), width: 8, dot: true, glowK: 1.3 });
        label(ctx, 'TEMPO', ox + w - 50, oy + 40, 0.6, { size: 20, glowK: 0 });
        text(ctx, '×', 360, 820, { size: 120, alpha: T.ap(24, 0.4, 0.6), glowK: 1 });
      });
    }
  });

  // 25–26 · não é sorte, é caráter repetido
  groups.push({
    from: 25, draw(ctx, T) {
      const o = 1 - T.ap(26, 0.3);
      withAlpha(ctx, o, () => {
        dice(ctx, CX - 90, 980, 1.1, T.ap(25, 0.3), T.t * 1.5);
        dice(ctx, CX + 110, 1040, 0.9, T.ap(25, 0.3, 0.15), -T.t * 1.2);
        xmark(ctx, CX, 1250, 55, T.lin(25, 0.4, 0.5));
      });
      withAlpha(ctx, T.ap(26, 0.3), () => {
        for (let i = 0; i < 35; i++) {
          const col = i % 7, row = Math.floor(i / 7), x = 230 + col * 103, y = 780 + row * 103;
          const p = T.lin(26, 0.05, 0.2 + i * 0.045);
          shape(ctx, c => rrect(c, x - 40, y - 40, 80, 80, 14), { fill: p > 0.5, width: 3, alpha: 0.3 + 0.7 * p, glowK: p > 0.5 ? 0.6 : 0.1 });
          if (p > 0.5) stroke(ctx, [[x - 18, y], [x - 4, y + 15], [x + 20, y - 14]], { width: 6, color: '0,0,0', glowK: 0 });
        }
        crown(ctx, CX, 1360, 0.9, T.ap(26, 0.4, 1.9));
      });
    }
  });

  groups.push({ from: 27, draw(ctx, T) { N.cta(ctx, T, 27); } });

  return { beats: roteiro.beats, groups };
};
