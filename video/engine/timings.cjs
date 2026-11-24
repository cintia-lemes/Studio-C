// Detecta o início/fim de cada frase da narração pelas pausas (silêncios)
// Uso: node video/engine/timings.cjs <pasta-do-video>
// Lê roteiro.json (lista de frases) e narracao.mp3, grava timings.json
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const dir = process.argv[2];
const roteiro = JSON.parse(fs.readFileSync(path.join(dir, 'roteiro.json'), 'utf8'));
const audio = path.join(dir, 'narracao.mp3');
const N = roteiro.beats.length;

const dur = parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', audio]).toString());
// Preferência: tempos por palavra (palavras.json da transcrição ElevenLabs) — frases separadas por [pause]
const wordsFile = path.join(dir, 'palavras.json');
if (fs.existsSync(wordsFile)) {
  const words = JSON.parse(fs.readFileSync(wordsFile, 'utf8')).words.filter(w => w.type === 'word');
  const sents = []; let curW = [];
  for (const w of words) {
    if (/^\[pause\]$/i.test(w.text)) { if (curW.length) sents.push(curW); curW = []; continue; }
    if (/^\[.*\]$/.test(w.text)) continue; // outras tags de direção ([serious] etc.)
    curW.push(w);
  }
  if (curW.length) sents.push(curW);
  if (sents.length !== N) { console.error(`palavras.json tem ${sents.length} frases, roteiro tem ${N}.`); process.exit(1); }
  const beats = sents.map((s, i) => ({ start: s[0].start, end: s[s.length - 1].end, text: roteiro.beats[i].fala }));
  fs.writeFileSync(path.join(dir, 'timings.json'), JSON.stringify({ duration: dur, beats }, null, 2));
  beats.forEach((b, i) => console.log(String(i).padStart(2), b.start.toFixed(2), b.end.toFixed(2), b.text, '| ouvido:', sents[i].map(w => w.text).join(' ')));
  process.exit(0);
}

// Sem tempos por palavra: alinha pelas pausas do áudio.
// Programação dinâmica: escolhe N-1 pausas de modo que a duração de cada frase
// combine com o tamanho do texto (números contam como mais longos) e prefere pausas longas.
let out = '';
try { out = execFileSync('sh', ['-c', `ffmpeg -i "${audio}" -af silencedetect=n=-38dB:d=0.1 -f null - 2>&1`]).toString(); } catch (e) { out = e.stdout.toString(); }
let sil = [], cur = null;
for (const line of out.split('\n')) {
  let m = line.match(/silence_start: ([\d.]+)/);
  if (m) cur = { s: parseFloat(m[1]) };
  m = line.match(/silence_end: ([\d.]+)/);
  if (m && cur) { cur.e = parseFloat(m[1]); sil.push(cur); cur = null; }
}
let t0 = 0, t1 = dur;
if (sil.length && sil[0].s <= 0.05) { t0 = sil[0].e; sil.shift(); }
if (sil.length && sil[sil.length - 1].e >= dur - 0.05) { t1 = sil[sil.length - 1].s; sil.pop(); }
const M = sil.length;
if (M < N - 1) { console.error(`Achei só ${M} pausas para ${N} frases.`); process.exit(1); }
const weight = str => str.replace(/["“”.,:;!?…]/g, '').replace(/\d/g, '#####').length; // dígito ≈ 5 letras faladas
const W = roteiro.beats.map(b => weight(b.fala));
const speech = (t1 - t0) - sil.reduce((a, x) => a + (x.e - x.s), 0) * 0.5;
const k = speech / W.reduce((a, b) => a + b, 0);
const segCost = (i, a, b) => { const d = Math.max(0.05, b - a); const r = Math.log(d / (W[i] * k)); return r * r; };
const pauseBonus = j => 0.8 * Math.log((sil[j].e - sil[j].s) / 0.1);
// dp[i][j]: frases 0..i, frase i termina na pausa j
const INF = 1e18, dp = [], from = [];
for (let i = 0; i < N - 1; i++) {
  dp.push(new Array(M).fill(INF)); from.push(new Array(M).fill(-1));
  for (let j = i; j < M; j++) {
    if (i === 0) { dp[0][j] = segCost(0, t0, sil[j].s) - pauseBonus(j); continue; }
    for (let p = i - 1; p < j; p++) {
      if (dp[i - 1][p] >= INF) continue;
      const c = dp[i - 1][p] + segCost(i, sil[p].e, sil[j].s) - pauseBonus(j);
      if (c < dp[i][j]) { dp[i][j] = c; from[i][j] = p; }
    }
  }
}
let best = INF, bj = -1;
for (let j = N - 2; j < M; j++) { const c = dp[N - 2][j] + segCost(N - 1, sil[j].e, t1); if (c < best) { best = c; bj = j; } }
const cuts = []; for (let i = N - 2, j = bj; i >= 0; i--) { cuts.unshift(j); j = from[i][j]; }
const beats = [];
for (let i = 0; i < N; i++) {
  const start = i === 0 ? t0 : sil[cuts[i - 1]].e, end = i === N - 1 ? t1 : sil[cuts[i]].s;
  beats.push({ start: +start.toFixed(3), end: +end.toFixed(3), text: roteiro.beats[i].fala });
}
fs.writeFileSync(path.join(dir, 'timings.json'), JSON.stringify({ duration: dur, beats }, null, 2));
beats.forEach((b, i) => console.log(String(i).padStart(2), b.start.toFixed(2), b.end.toFixed(2), b.text));
