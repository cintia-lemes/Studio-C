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

(async () => {
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
  const out = path.join(outDir, 'video.mp4');
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-i', path.join(dir, 'narracao.mp3'),
    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-af', 'apad', '-shortest', '-movflags', '+faststart', out]);
  parts.forEach(p => fs.unlinkSync(p)); fs.unlinkSync(list);
  console.log(`\nPronto: ${out} (${total} frames em ${((Date.now() - t0) / 1000).toFixed(0)}s)`);
})();
