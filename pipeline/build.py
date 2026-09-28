"""Build HTML + MP4 for AI Music Surge from cues.json (+ optional vo.mp3)."""
import base64, json, os, subprocess, sys, asyncio
import numpy as np
from sfx import render_sfx, SR

import os as _os
OUT = _os.environ.get('OUT', _os.getcwd())
C = json.load(open(f'{OUT}/cues.json'))
VO = f'{OUT}/vo.mp3' if os.path.exists(f'{OUT}/vo.mp3') else None
FPS = 30
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()


def load_audio(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def mix():
    n = int(C['dur'] * SR)
    fx = render_sfx(C)
    fx = np.pad(fx, (0, max(0, n - len(fx))))[:n]
    vo = np.zeros(n)
    if VO:
        v = load_audio(VO)
        off = int(C.get('vo_offset', 0) * SR)
        v = v[:n - off]
        vo[off:off + len(v)] = v
        # duck SFX ~55% under speech
        win = int(0.05 * SR)
        rms = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, 'same'))
        act = np.clip(rms / 0.03, 0, 1)
        act = np.convolve(act, np.ones(int(0.12 * SR)) / int(0.12 * SR), 'same')
        fx *= 1 - 0.55 * act
    m = vo + fx * 0.5
    # short fades so the loop point never clicks
    f = int(0.02 * SR)
    m[:f] *= np.linspace(0, 1, f); m[-f:] *= np.linspace(1, 0, f)
    m = m / max(1.0, np.max(np.abs(m)) / 0.97)
    m.astype(np.float32).tofile(f'{OUT}/mix.f32')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', f'{OUT}/mix.f32',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), '-c:a', 'libmp3lame', '-b:a', '192k',
                    f'{OUT}/mix.mp3'], check=True)


def build_html(audio_path):
    tpl = open(f'{OUT}/template.html').read()
    f = f'{OUT}/fonts'
    html = (tpl.replace('/*ANTON*/', b64(f'{f}/fontsource-anton-5.3.0/files/anton-latin-400-normal.woff2'))
               .replace('/*MONO*/', b64(f'{f}/fontsource-jetbrains-mono-5.3.0/files/jetbrains-mono-latin-400-normal.woff2'))
               .replace('/*CUES*/', json.dumps({k: v for k, v in C.items()}))
               .replace('/*AUDIO*/', ('data:audio/mpeg;base64,' + b64(audio_path)) if audio_path else ''))
    open(f'{OUT}/ai_music_surge.html', 'w').write(html)


async def frames(times, outdir=None, pipe=None):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.add_init_script('window.__capture = true;')
        await pg.goto(f'file://{OUT}/ai_music_surge.html')
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(500)
        assert await pg.evaluate("document.fonts.check('50px Anton')")
        canvas = pg.locator('canvas')
        for i, t in enumerate(times):
            await pg.evaluate(f'renderAt({t})')
            img = await canvas.screenshot(type='jpeg', quality=95) if pipe else None
            if pipe:
                pipe.write(img)
            else:
                await canvas.screenshot(path=f'{outdir}/f_{t:06.2f}.png')
        await b.close()


def contact(times):
    os.makedirs(f'{OUT}/cs', exist_ok=True)
    for f in os.listdir(f'{OUT}/cs'):
        os.remove(f'{OUT}/cs/{f}')
    asyncio.run(frames(times, f'{OUT}/cs'))
    from PIL import Image, ImageDraw
    fs = sorted(os.listdir(f'{OUT}/cs'))
    cols = 7
    rows = (len(fs) + cols - 1) // cols
    sheet = Image.new('RGB', (270 * cols, 500 * rows), (90, 90, 90))
    d = ImageDraw.Draw(sheet)
    for i, fn in enumerate(fs):
        im = Image.open(f'{OUT}/cs/{fn}').resize((270, 480))
        sheet.paste(im, ((i % cols) * 270, (i // cols) * 500))
        d.text(((i % cols) * 270 + 5, (i // cols) * 500 + 482), fn[2:-4], fill=(255, 255, 0))
    sheet.save(f'{OUT}/sheet.png')


def video():
    n = int(round(C['dur'] * FPS))
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                           '-i', f'{OUT}/mix.mp3', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17',
                           '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart',
                           f'{OUT}/ai_music_surge.mp4'], stdin=subprocess.PIPE)
    asyncio.run(frames([i / FPS for i in range(n)], pipe=ff.stdin))
    ff.stdin.close(); ff.wait()


if __name__ == '__main__':
    step = sys.argv[1]
    if step == 'audio':
        mix()
    elif step == 'html':
        build_html(f'{OUT}/mix.mp3' if os.path.exists(f'{OUT}/mix.mp3') else None)
    elif step == 'sheet':
        contact([float(x) for x in sys.argv[2].split(',')])
    elif step == 'video':
        video()
