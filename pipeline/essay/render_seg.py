import asyncio, subprocess, sys, os
OUT = os.getcwd(); FPS = 30
a, b, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
async def main():
    from playwright.async_api import async_playwright
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', out], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={'width': 1920, 'height': 1080})
        await pg.add_init_script('window.__capture = true;')
        await pg.goto(f'file://{OUT}/essay.html')
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        assert await pg.evaluate("document.fonts.check('50px Anton')")
        cv = pg.locator('canvas')
        for i in range(a, b):
            await pg.evaluate(f'renderAt({i / FPS})')
            ff.stdin.write(await cv.screenshot(type='jpeg', quality=95))
        await br.close()
    ff.stdin.close(); ff.wait()
asyncio.run(main())
