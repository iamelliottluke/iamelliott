from pathlib import Path
import json, subprocess, time
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa-output'
OUT.mkdir(exist_ok=True)
server=subprocess.Popen(['python','-m','http.server','8123','--bind','127.0.0.1'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
time.sleep(1.0)
PAGES=['index.html','work/greendoor.html','work/campaigns.html','work/collaborations.html','work/moving-imagery.html','work/practical-solutions.html','work/welcome-mat.html']
SIZES=[(1440,900),(1280,720),(768,900),(390,844),(360,640),(844,390)]
issues=[]
records=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  for width,height in SIZES:
   ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
   pg=ctx.new_page()
   pg.on('pageerror',lambda e:issues.append('SCRIPT ERROR '+str(e)))
   for site in PAGES:
    pg.goto('http://127.0.0.1:8123/'+site,wait_until='domcontentloaded',timeout=25000)
    pg.wait_for_timeout(210)
    view=pg.evaluate('''() => {
      const h=document.querySelector('.hero,.case-hero');
      return {path:location.pathname,scrollWidth:document.documentElement.scrollWidth,clientWidth:document.documentElement.clientWidth,header:document.querySelector('.masthead').getBoundingClientRect().height,hero:h?.getBoundingClientRect().height||0,hash:location.hash};
    }''')
    records.append(dict(view,width=width,height=height))
    if view['scrollWidth']>view['clientWidth']+2:
     issues.append(f'HORIZONTAL OVERFLOW {width}x{height} {site}: {view["scrollWidth"]}>{view["clientWidth"]}')
    if height>540 and view['hero']>height-view['header']+3:
     issues.append(f'HERO TOO TALL {width}x{height} {site}: {view["hero"]} vs viewport {height}')
    if site=='index.html':
     if width in (390,1440):
      pg.screenshot(path=str(OUT/f'home-{width}.png'),full_page=False)
      pg.locator('a[href="work/campaigns.html"].tile-visual').first.click()
      pg.wait_for_url('**/work/campaigns.html',timeout=12000)
      pg.screenshot(path=str(OUT/f'campaigns-{width}.png'),full_page=False)
      pg.go_back(wait_until='domcontentloaded')
     if width<=650:
      menu=pg.locator('.mobile-menu summary')
      menu.click()
      pg.locator('.mobile-menu a[href$="#about"]').first.click()
     else:
      pg.locator('.nav-desktop a[href$="#about"]').first.click()
     pg.wait_for_timeout(900)
     top=pg.eval_on_selector('#about','el=>Math.round(el.getBoundingClientRect().top)')
     if abs(top)>5:issues.append(f'ABOUT ANCHOR {width} => {top}')
    else:
     pg.locator('.jump').first.click()
     pg.wait_for_timeout(900)
     top=pg.eval_on_selector('#story','el=>Math.round(el.getBoundingClientRect().top)')
     if abs(top)>5:issues.append(f'STORY ANCHOR {width} {site} => {top}')
     if site=='work/welcome-mat.html':
      pg.locator('.case-next a[href$="#work"]').first.click()
      pg.wait_for_url('**/index.html#work',timeout=12000)
      pg.wait_for_timeout(900)
      top=pg.eval_on_selector('#work','el=>Math.round(el.getBoundingClientRect().top)')
      if abs(top)>5:issues.append(f'ALL THE WORK ANCHOR {width} => {top}')
     elif site=='work/campaigns.html':
      if width<=650:
       pg.locator('.mobile-menu summary').click()
       pg.locator('.mobile-menu a[href$="#contact"]').first.click()
      else: pg.locator('.nav-desktop a[href$="#contact"]').first.click()
      pg.wait_for_url('**/index.html#contact',timeout=12000)
      pg.wait_for_timeout(900)
      top=pg.eval_on_selector('#contact','el=>Math.round(el.getBoundingClientRect().top)')
      if abs(top)>5:issues.append(f'PROJECT CONTACT ANCHOR {width} => {top}')
   ctx.close()
  browser.close()
finally:
 server.terminate()
(OUT/'report.json').write_text(json.dumps({'records':records,'issues':issues},indent=2))
print(f'Tested {len(records)} page/viewport combinations')
for issue in issues:print('FAIL:',issue)
if issues:raise SystemExit(1)
print('PASS: all responsive, navigation and anchor smoke checks')
