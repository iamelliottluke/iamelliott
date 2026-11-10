from pathlib import Path
import subprocess,time,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa-output';OUT.mkdir(exist_ok=True)
server=subprocess.Popen(['python','-m','http.server','8125','--bind','127.0.0.1'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
time.sleep(.7)
issues=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  for width,height in [(1440,900),(1280,800),(1100,800),(768,900),(390,844),(360,740)]:
   context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
   page=context.new_page()
   page.goto('http://127.0.0.1:8125/index.html',wait_until='networkidle')
   page.wait_for_timeout(200)
   result=page.evaluate('''() => {
    const b=s=>{const a=document.querySelector(s)?.getBoundingClientRect();return a?{x:a.x,y:a.y,right:a.right,bottom:a.bottom,width:a.width,height:a.height}:null}
    return {scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,
      title:b('.work-title h2'),quote:b('.work-title .work-intro'),pitch:b('.work-title .work-pitch'),
      sigLoaded:!!document.querySelector('.handwriting img')?.naturalWidth,
      hasMethod:!!document.querySelector('[data-method-overlay]'),
      desktopMenu:getComputedStyle(document.querySelector('.nav-desktop')).display}
   }''')
   if result['scroll']>result['client']+2:issues.append(f'{width}: horizontal overflow: {result["scroll"]} > {result["client"]}')
   if not result['sigLoaded']:issues.append(f'{width}: original e.gif signature failed')
   if not result['hasMethod']:issues.append(f'{width}: method overlay slot missing')
   t,q,body=result['title'],result['quote'],result['pitch']
   if t and (t['x'] < -5 or t['right']>width+5):issues.append(f'{width}: Show Dont Tell heading clipped: {t}')
   if width>1100:
    if t and q and t['right']>q['x']+5:issues.append(f'{width}: heading and quote overlap: {t} / {q}')
    if body and t and body['y']<t['bottom']-5:issues.append(f'{width}: intro pitch overlaps heading')
   else:
    if t and q and q['y']<t['bottom']-5:issues.append(f'{width}: quote overlaps heading')
    if body and q and body['y']<q['bottom']-5:issues.append(f'{width}: pitch overlaps quote')
   page.locator('.work-title').screenshot(path=str(OUT/f'work-{width}.png'))
   page.locator('.about-heading').screenshot(path=str(OUT/f'about-{width}.png'))
   if width>740:
    page.locator('.work-menu summary').click()
    if not page.locator('.work-menu').evaluate('(e)=>e.open'):issues.append(f'{width}: desktop work menu not opening')
    if page.locator('.work-menu-list a').count()!=6:issues.append(f'{width}: desktop 6 links missing')
    page.keyboard.press('Escape')
    if page.locator('.work-menu').evaluate('(e)=>e.open'):issues.append(f'{width}: Escape does not dismiss menu')
   else:
    page.locator('.mobile-menu>summary').click()
    page.locator('.work-mobile-submenu>summary').click()
    if page.locator('.work-mobile-list a').count()!=7:issues.append(f'{width}: mobile project list incomplete')
    page.locator('.work-mobile-list a').first.click()
   page.goto('http://127.0.0.1:8125/work/practical-solutions.html',wait_until='domcontentloaded')
   if page.locator('.receipt-divider img').count()!=1:issues.append(f'{width}: receipt divider missing')
   if page.locator('.receipt-followup').count()!=1:issues.append(f'{width}: final receipt mini-section missing')
   context.close()
  browser.close()
finally:
 server.terminate()
(OUT/'build05-report.json').write_text(json.dumps({'issues':issues},indent=2))
for x in issues:print('ERROR:',x)
if issues:raise SystemExit(1)
print('PASS: responsive layouts, original signature, menus, case study section')
