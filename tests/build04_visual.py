from pathlib import Path
import subprocess,time,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa-output'
OUT.mkdir(exist_ok=True)
server=subprocess.Popen(['python','-m','http.server','8124','--bind','127.0.0.1'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
time.sleep(.8)
problems=[]
pages=['index.html','work/greendoor.html','work/campaigns.html','work/collaborations.html','work/moving-imagery.html','work/practical-solutions.html','work/welcome-mat.html']
sizes=[('desktop',1440,900),('laptop',1280,800),('tablet',768,900),('mobile',390,844),('small-mobile',360,640)]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  for name,w,h in sizes:
   ctx=browser.new_context(viewport={'width':w,'height':h},reduced_motion='reduce')
   page=ctx.new_page()
   for url in pages:
    page.goto('http://127.0.0.1:8124/'+url,wait_until='domcontentloaded')
    page.wait_for_timeout(190)
    title=Path(url).stem
    if name in ('desktop','mobile'):
     page.screenshot(path=str(OUT/f'{title}-{name}-hero.png'),full_page=False)
    measures=page.evaluate('''() => {
      const R = sel => [...document.querySelectorAll(sel)].map(el=>{const a=el.getBoundingClientRect();return {x:a.x,y:a.y,w:a.width,h:a.height,b:a.bottom,right:a.right}});
      const hero=document.querySelector('.hero,.case-hero');
      const primary=document.querySelector('.hero h1,.case-heading h1');
      const bounds=primary?.getBoundingClientRect();
      return {sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,hero:hero?.getBoundingClientRect().height||0,
        h1:bounds?{x:bounds.x,y:bounds.y,w:bounds.width,h:bounds.height,r:bounds.right,b:bounds.bottom}:null,
        mosaic:R('.film-mosaic .media-film'),campaigns:R('.campaign-section>.media-film'),model:R('.model-door'),
        work: R('.work-title'),method:R('.method-butterflies'),butterfly:R('.butterfly-spot'),
        receipt:R('.tile-systems .tile-visual>video'),loading:document.querySelector('img[data-media="butterflyStill"]')?.getAttribute('src')||'none'};
    }''')
    if measures['sw']>measures['cw']+2:problems.append(f'{name} {url}: horizontal overflow')
    if measures['h1'] and (measures['h1']['x']<-20 or measures['h1']['r']>w+22):problems.append(f'{name} {url}: headline extends outside viewport {measures["h1"]}')
    if url.endswith('campaigns.html'):
     font=page.locator('.ntwi-title').evaluate('el=>getComputedStyle(el).fontFamily')
     if 'DM Sans' not in font:problems.append(f'{name}: campaign title not one sans font: {font}')
     if name in ('mobile','desktop'):
      page.locator('.campaign-section').first.screenshot(path=str(OUT/f'ntwi-{name}.png'))
      page.locator('.film-mosaic').first.screenshot(path=str(OUT/f'campaign-gallery-{name}.png'))
    if url.endswith('greendoor.html') and name in ('mobile','desktop'):
     page.locator('.model-with-film').screenshot(path=str(OUT/f'green-model-{name}.png'))
     page.locator('.film-mosaic').first.screenshot(path=str(OUT/f'green-gallery-{name}.png'))
    if url.endswith('moving-imagery.html') and name in ('mobile','desktop'):
     page.locator('.film-mosaic.mosaic-2').first.screenshot(path=str(OUT/f'film-gallery-{name}.png'))
    if url=='index.html' and name in ('mobile','desktop'):
     page.locator('.about-section').screenshot(path=str(OUT/f'about-{name}.png'))
     page.locator('.work-title').screenshot(path=str(OUT/f'work-title-{name}.png'))
     page.locator('.tile-systems').screenshot(path=str(OUT/f'receipt-tile-{name}.png'))
    if w<=740:
     for key in ['mosaic','campaigns']:
      boxes=measures[key]
      if len(boxes)>1:
       prev=boxes[0]
       for b in boxes[1:]:
        if b['y']<prev['b']-4:problems.append(f'{name} {url}: {key} gallery overlaps or shares row')
        prev=b
    if url=='index.html':
     try:
      assert page.locator('.tile-systems video[data-media="receipt"]').count()==1
      assert page.locator('.method-butterflies[data-media="butterflyDark"]').count()==1
      assert page.locator('.butterfly-spot img[data-media="butterflyStill"]').count()==1
      assert 'IE / 001' not in page.locator('body').inner_text()
     except AssertionError:problems.append(f'{name}: home visual assets not mapped')
   ctx.close()
  browser.close()
finally:
 server.terminate()
(OUT/'visual-report.json').write_text(json.dumps({'issues':problems,'pages':len(pages),'viewports':sizes},indent=2))
print('Optical test checked',len(pages)*len(sizes),'page/viewport combinations')
for item in problems:print('ERROR:',item)
if problems:raise SystemExit(1)
print('PASS: optical and content checks')
