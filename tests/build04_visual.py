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
     page.locator('.contact-section').screenshot(path=str(OUT/f'contact-{name}.png'))
    if url=='index.html':
     assert page.locator('.portrait-frame>span').count()==0, 'About portrait caption remains'
     assert page.locator('.butterfly-spot img[data-media="butterfly"]').count()==1, 'Hero butterfly GIF missing'
     assert page.locator('.method-butterflies[data-media="butterfly"]').count()==1, 'Method butterfly GIF missing'
     assert page.locator('.contact-butterfly[data-media="butterfly"]').count()==1, 'Contact butterfly GIF missing'
     assert page.locator('#method-heading').inner_text().strip().endswith('I make it real.'), 'Method headline still contains redaction'
     assert page.locator('.work-title .quote-translation').inner_text()=='why not both?', 'Translation missing'
     assert 'Mia Agraviador' in page.locator('.work-intro small').inner_text(), 'Old El Paso credit missing'
     assert page.locator('.film-quote blockquote').evaluate("el=>getComputedStyle(el).fontStyle")=='italic', 'Film quote not italic'
     assert abs(float(page.locator('.hero .overlay-motion').evaluate("el=>getComputedStyle(el).opacity"))-.29)<.005, 'Hero opacity differs'
     if name in ('mobile','desktop'):
      page.locator('.method').screenshot(path=str(OUT/f'method-{name}.png'))
     about=page.locator('.handwriting').bounding_box()
     if about and (about['x']<-12 or about['x']+about['width']>w+12):
      problems.append(f'{name}: Elliott handwriting offscreen {about}')
     heading=page.locator('.work-title h2').bounding_box()
     quote=page.locator('.work-intro').bounding_box()
     pitch=page.locator('.work-pitch').bounding_box()
     if heading and quote and pitch:
      if w>=1200:
       if heading['x']+heading['width']>quote['x']+4 or quote['x']+quote['width']>pitch['x']+4:
        problems.append(f'{name}: three-column Show/Dont Tell content overlaps horizontally')
       if abs((heading['y']+heading['height']/2)-(quote['y']+quote['height']/2))>135:
        problems.append(f'{name}: three-column work content lacks vertical balance')
      else:
       if quote['y']<heading['y']+heading['height']-5 or pitch['y']<quote['y']+quote['height']-5:
        problems.append(f'{name}: stacked Show/Dont Tell content overlaps vertically')
    if url.endswith('greendoor.html'):
     if page.locator('.story-feature-film video[data-media="greenDoor01"]').count()!=1:
      problems.append(f'{name}: gd1 missing beside idea')
     if name in ('desktop','mobile'):
      page.locator('.story-with-feature').first.screenshot(path=str(OUT/f'gd-idea-{name}.png'))
    if url.endswith('moving-imagery.html'):
     if page.locator('.story-with-feature video[data-media="hikeSociety"]').count()!=1:
      problems.append(f'{name}: Hike Society misplaced')
     if name in ('desktop','mobile'):
      page.locator('.story-with-feature').first.screenshot(path=str(OUT/f'hike-story-{name}.png'))
    if url.endswith('welcome-mat.html'):
     if page.locator('.story-feature-illustration img[data-media="welcomeMatIllustration01"]').count()!=1 or page.locator('.story-feature-illustration img[data-media="welcomeMatIllustration02"]').count()!=1:
      problems.append(f'{name}: Welcome Mat illustrations missing')
     if name in ('desktop','mobile'):
      for i,fig in enumerate(page.locator('.story-with-illustration').all()):
       fig.screenshot(path=str(OUT/f'wm-illustration-{i+1}-{name}.png'))
    if url.endswith('greendoor.html'):
     names=page.locator('.film-mosaic.mosaic-3 figcaption').all_inner_texts()
     if names!=['save the date.','aftermath','anywhere']:problems.append(f'{name}: Green Door captions are {names}')
     if page.locator('.timeline strong').count()!=2:problems.append(f'{name}: Gathering timeline outcomes incomplete')
     cap=page.locator('.model-door figcaption')
     if cap.count():
      box=cap.bounding_box()
      parent=page.locator('.model-door').bounding_box()
      if box and parent and abs((box['x']+box['width']/2)-(parent['x']+parent['width']/2))>9:
       problems.append(f'{name}: knock knock not centered')
    if url.endswith('collaborations.html'):
     medusa=page.locator('.collab-split article').nth(0).inner_text()
     jess=page.locator('.collab-split article').nth(1).inner_text()
     if 'The perfect' not in medusa or 'Final Girl' not in jess or 'DJ KAYELO' not in jess:
      problems.append(f'{name}: collaboration copy mismatch')
     if name in ('mobile','desktop'):
      page.locator('.collab-split').screenshot(path=str(OUT/f'collaborations-{name}.png'))
    if url.endswith('practical-solutions.html'):
     if page.locator('.receipt-story-side video[data-media="receipt"]').count()!=1:
      problems.append(f'{name}: receipt video not aligned inside SDA block')
     if page.locator('.receipt-case-visual figcaption').inner_text()!='custom workplace information receipts':
      problems.append(f'{name}: receipt caption mismatch')
     if name in ('mobile','desktop'):
      page.locator('.receipt-story').screenshot(path=str(OUT/f'receipt-story-{name}.png'))
     side=page.locator('.receipt-story-side').bounding_box()
     body=page.locator('.receipt-story>div:last-child').bounding_box()
     if side and body:
      if w>900 and side['x']>=body['x']:problems.append(f'{name}: receipt is not left of SDA copy')
      if w<=740 and side['y']>body['y']:problems.append(f'{name}: SDA receipt mobile order wrong')
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
      assert page.locator('.method-butterflies[data-media="butterfly"]').count()==1
      assert page.locator('.butterfly-spot img[data-media="butterfly"]').count()==1
      assert page.locator('.contact-butterfly[data-media="butterfly"]').count()==1
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
