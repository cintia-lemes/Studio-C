# Studio-C · Fábrica de vídeos (estilo neon minimalista)

Vídeos 9:16 (1080×1920, 30 fps) de finanças no estilo "linha branca brilhante sobre preto",
gerados 100% por código: roteiro → narração com IA (ElevenLabs) → animação sincronizada → MP4.

## Estrutura
- `engine/engine.js` — motor de desenho (boneco, ícones, gráficos, balões, brilho, títulos digitando, transições)
- `engine/timings.cjs` — acha o início/fim de cada frase da narração pelas pausas
- `engine/render.cjs` — renderiza no Chromium e monta o MP4 com ffmpeg
- `videos/<nn-tema>/` — um vídeo: `roteiro.json`, `narracao.mp3`, `timings.json`, `scenes.js`, `saida/video.mp4`

## Como fazer um vídeo novo
1. Copie `videos/01-dolar` para `videos/02-<tema>` e escreva o `roteiro.json` (1 frase curta por beat, com `titulo`/`sub`).
2. Gere a narração (mesmas frases, separadas por `[pause]`) e salve como `narracao.mp3`. Transcreva-a (ElevenLabs Scribe) e salve os tempos por palavra como `palavras.json` — o alinhamento fica exato. Sem esse arquivo, o script usa as pausas do áudio.
3. `node video/engine/timings.cjs video/videos/02-<tema>` — confere se cada frase caiu no tempo certo.
4. Escreva as cenas em `scenes.js` (cada grupo desenha um conjunto de frases).
5. Pré-visualizar quadros: `node video/engine/render.cjs video/videos/02-<tema> --stills 1,5,10`
6. Renderizar: `node video/engine/render.cjs video/videos/02-<tema> --workers 4`

Regras de estilo: 1 ideia por frase, algo muda na tela a cada 1,5–3 s, só branco/cinza,
títulos no topo (funcionam como legenda), aviso "conteúdo educativo" em vídeos de investimento.
