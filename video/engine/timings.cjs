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

let out = '';
try { out = execFileSync('sh', ['-c', `ffmpeg -i "${audio}" -af silencedetect=n=-38dB:d=0.15 -f null - 2>&1`]).toString(); } catch (e) { out = e.stdout.toString(); }

let sil = [];
let cur = null;
for (const line of out.split('\n')) {
  let m = line.match(/silence_start: ([\d.]+)/);
  if (m) cur = { s: parseFloat(m[1]) };
  m = line.match(/silence_end: ([\d.]+)/);
  if (m && cur) { cur.e = parseFloat(m[1]); sil.push(cur); cur = null; }
}
// ignora silêncio no começo/fim do arquivo
sil = sil.filter(x => x.s > 0.05 && x.e < dur - 0.05);
// mantém as N-1 pausas mais longas (pausas entre frases > vírgulas)
if (sil.length < N - 1) {
  console.error(`Achei só ${sil.length} pausas para ${N} frases. Ajuste o roteiro ou o áudio.`);
  process.exit(1);
}
sil = sil.sort((a, b) => (b.e - b.s) - (a.e - a.s)).slice(0, N - 1).sort((a, b) => a.s - b.s);

const beats = [];
let start = 0;
for (let i = 0; i < N; i++) {
  const end = i < N - 1 ? sil[i].s : dur;
  beats.push({ start: +start.toFixed(3), end: +end.toFixed(3), text: roteiro.beats[i].fala });
  if (i < N - 1) start = sil[i].e;
}
fs.writeFileSync(path.join(dir, 'timings.json'), JSON.stringify({ duration: dur, beats }, null, 2));
beats.forEach((b, i) => console.log(String(i).padStart(2), b.start.toFixed(2), b.end.toFixed(2), b.text));
