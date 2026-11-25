# Studio-C
Estúdio de vídeos em animação 2D minimalista (pictogramas brancos em fundo preto).

- `docs/analise-estilo.md`: análise quadro a quadro do vídeo de referência e a fórmula do estilo.
- `anim/engine.py`: motor de animação em Python (Pillow + numpy + ffmpeg), com pop, contador, câmera, whip pan, glow e efeitos sonoros.
- `anim/video_01.py`: vídeo 01, "1% por dia", com o roteiro de narração no topo do arquivo.
- `anim/video_02.py` (narração ElevenLabs em `anim/assets/voz02/`, mixada automaticamente): vídeo 02 da Guidelight, "Pare de correr atrás do dinheiro" (61 s, 1920×1080, com cores de destaque, inversão preto/branco e cartão final com a foto de perfil em `anim/assets/guidelight.jpg`).
- `anim/video_03.py`: vídeo 03 da Guidelight, "Black Friday × 13º" (9:16, 1080×1920, narração com a voz Letícia em `anim/assets/voz03/`, versão Jarnathan em `voz03_jarnathan/`; `--mix` refaz só a voz; roteiro em `docs/roteiros/`).
- `anim/video_04.py`: vídeo 04 da Guidelight, "Lei 3: oculte suas intenções" (9:16, ~71 s, voz Nassif em `anim/assets/voz04/`; 1ª versão com a Letícia em `voz04_leticia_v1/`; roteiro em `docs/roteiros/`).
- `anim/video_05.py`: vídeo 05 da Guidelight, "2027: imposto, SUS e posse" (9:16, ~89 s, voz Elvis em `anim/assets/voz05/`; roteiro e checagem de fatos em `docs/roteiros/`).

```bash
pip install pillow numpy      # ffmpeg precisa estar instalado
python3 anim/video_01.py --stills   # prévia rápida em out/stills/
python3 anim/video_01.py            # vídeo final em out/video_01.mp4
```
