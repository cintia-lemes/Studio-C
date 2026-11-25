# Studio-C
Estúdio de vídeos em animação 2D minimalista (pictogramas brancos em fundo preto).

- `docs/analise-estilo.md`: análise quadro a quadro do vídeo de referência e a fórmula do estilo.
- `anim/engine.py`: motor de animação em Python (Pillow + numpy + ffmpeg), com pop, contador, câmera, whip pan, glow e efeitos sonoros.
- `anim/video_01.py`: vídeo 01, "1% por dia", com o roteiro de narração no topo do arquivo.

```bash
pip install pillow numpy      # ffmpeg precisa estar instalado
python3 anim/video_01.py --stills   # prévia rápida em out/stills/
python3 anim/video_01.py            # vídeo final em out/video_01.mp4
```
