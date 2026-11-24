// Renderiza um vídeo: node video/engine/render.cjs <pasta-do-video> [--stills 1.5,10,22] [--workers 4]
// Saída: <pasta>/saida/video.mp4 (1080x1920, 30fps, H.264 + narração AAC)
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const dir = path.resolve(process.argv[2]);
const args = process.argv.slice(3);
const opt = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const FPS = 30, TAIL = 1.2; // segundos extras no final
const roteiro = JSON.parse(fs.readFileSync(path.join(dir, 'roteiro.json'), 'utf8'));
const timings = JSON.parse(fs.readFileSync(path.join(dir, 'timings.json'), 'utf8'));
const outDir = path.join(dir, 'saida');
fs.mkdirSync(outDir, { recursive: true });

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.setContent('<html><body style="margin:0;background:#000"><canvas id="c" width="1080" height="1920"></canvas></body></html>');
  await page.addScriptTag({ path: path.join(__dirname, 'engine.js') });
  await page.addScriptTag({ path: path.join(dir, 'scenes.js') });
  await page.evaluate(async ([r, t]) => {
    await document.fonts.load('900 40px Inter'); await document.fonts.load('800 40px Inter'); await document.fonts.load('700 40px Inter');
    window.setupVideo(window.buildVideo(r), t);
  }, [roteiro, timings]);
  return page;
}
const grab = (page, t, type = 'jpeg') => page.evaluate(([t, type]) => {
  window.renderFrame(t);
  return document.getElementById('c').toDataURL('image/' + type, 0.95).split(',')[1];
}, [t, type]);

// Junta vídeo + narração (+ trilha.mp3 opcional, em loop, abaixando sob a voz)
function mixAudio(videoIn) {
  const out = path.join(outDir, 'video.mp4');
  const tmp = path.join(outDir, 'tmp_mix.mp4');
  const trilha = path.join(dir, 'trilha.mp3');
  const D = (timings.duration + TAIL).toFixed(2);
  const vol = parseFloat(opt('--music-vol') || '0.22');
  const a = ['-y', '-v', 'error', '-i', videoIn, '-i', path.join(dir, 'narracao.mp3')];
  if (fs.existsSync(trilha)) {
    a.push('-stream_loop', '-1', '-i', trilha, '-filter_complex',
      `[1:a]apad,asplit[v1][v2];` +
      `[2:a]atrim=0:${D},volume=${vol},afade=t=in:d=1.5,afade=t=out:st=${(D - 2.5).toFixed(2)}:d=2.5[m];` +
      `[m][v2]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=500[md];` +
      `[v1][md]amix=inputs=2:normalize=0:duration=first,atrim=0:${D},loudnorm=I=-14:TP=-1.5:LRA=11[a]`,
      '-map', '0:v', '-map', '[a]');
  } else {
    a.push("-af", "apad,loudnorm=I=-14:TP=-1.5:LRA=11", "-map", "0:v", "-map", "1:a");
  }
  a.push('-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', tmp);
  execFileSync('ffmpeg', a);
  fs.renameSync(tmp, out);
  console.log('Áudio: narração' + (fs.existsSync(trilha) ? ' + trilha (vol ' + vol + ')' : ''));
}

(async () => {
  if (args.includes('--audio-only')) { // remixa o áudio sem renderizar os frames de novo
    const src = path.join(outDir, 'sem_audio.mp4');
    execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', path.join(outDir, 'video.mp4'), '-an', '-c', 'copy', src]);
    mixAudio(src); fs.unlinkSync(src); return;
  }
  const browser = await chromium.launch();
  const stills = opt('--stills');
  if (stills) {
    const page = await openPage(browser);
    for (const s of stills.split(',')) {
      const f = path.join(outDir, `still_${s}.png`);
      fs.writeFileSync(f, Buffer.from(await grab(page, parseFloat(s), 'png'), 'base64'));
      console.log(f);
    }
    await browser.close(); return;
  }
  const total = Math.ceil((timings.duration + TAIL) * FPS);
  const workers = parseInt(opt('--workers') || '3');
  const per = Math.ceil(total / workers);
  const t0 = Date.now();
  const parts = await Promise.all([...Array(workers)].map(async (_, w) => {
    const a = w * per, b = Math.min(total, a + per);
    const file = path.join(outDir, `part_${w}.mp4`);
    const page = await openPage(browser);
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(FPS), file], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = a; i < b; i++) {
      const buf = Buffer.from(await grab(page, i / FPS), 'base64');
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (w === 0 && i % 60 === 0) process.stdout.write(`\r${Math.round(100 * (i - a) / (b - a))}% `);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    return file;
  }));
  await browser.close();
  const list = path.join(outDir, 'parts.txt');
  fs.writeFileSync(list, parts.map(p => `file '${p}'`).join('\n'));
  const silent = path.join(outDir, 'sem_audio.mp4');
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', silent]);
  mixAudio(silent);
  fs.unlinkSync(silent);
  parts.forEach(p => fs.unlinkSync(p)); fs.unlinkSync(list);
  console.log(`\nPronto: ${path.join(outDir, 'video.mp4')} (${total} frames em ${((Date.now() - t0) / 1000).toFixed(0)}s)`);
})();
