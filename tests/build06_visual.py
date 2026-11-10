from pathlib import Path
import subprocess,time,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa-output';OUT.mkdir(exist_ok=True)
server=subprocess.Popen(['python','-m','http.server','8126','--bind','127.0.0.1'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
time.sleep(1)
issues=[];measurements=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  for width,height in [(1440,900),(1280,800),(1100,800),(768,900),(390,844),(360,740)]:
   ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='no-preference')
   page=ctx.new_page()
   errors=[]
   page.on('pageerror',lambda e: errors.append(str(e)))
   page.goto('http://127.0.0.1:8126/index.html',wait_until='domcontentloaded')
   page.locator('.work-title').scroll_into_view_if_needed()
   page.wait_for_function('''() => {
    const x=document.querySelector('.handwriting img');
    const o=document.querySelector('.method-overlay');
    return x && x.complete && x.naturalWidth>0 && o && o.classList.contains('is-ready');
   }''',timeout=18000)
   page.wait_for_timeout(120)
   data=page.evaluate('''() => {
      function box(sel) {let e=document.querySelector(sel);if(!e)return null;let r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,w:r.width,h:r.height};}
      return {
        viewport:innerWidth,scroll:document.documentElement.scrollWidth,
        title:box('.work-title h2'),first:box('.work-title h2 span'),second:box('.work-title h2 em'),
        pitch:box('.work-pitch'),quote:box('.work-intro'),
        signature:box('.handwriting'),redaction:box('.loose-redact'),sigImage:box('.handwriting img'),
        overlayReady:document.querySelector('.method-overlay').classList.contains('is-ready'),
        overlayStyle:getComputedStyle(document.querySelector('.method-overlay')).backgroundImage.length,
        headingFont:parseFloat(getComputedStyle(document.querySelector('.work-title h2')).fontSize)
      };
   }''')
   measurements.append(data)
   if errors:issues.append(f'{width}: JS errors: {errors[:2]}')
   if data['scroll']>width+2:issues.append(f'{width}: horizontal overflow: {data["scroll"]}')
   if not data['overlayReady'] or data['overlayStyle']<50:issues.append(f'{width}: green-screen overlay did not composite')
   if not data['signature'] or data['signature']['w']<185:issues.append(f'{width}: Elliott signature not enlarged')
   title=data['title']
   if title and (title['x']<-5 or title['right']>width+5):issues.append(f'{width}: Show headline clipped {title}')
   if width>1100:
    if data['quote'] and title and title['right']>data['quote']['x']+6:issues.append(f'{width}: desktop title collides with quote')
    if data['pitch'] and title and data['pitch']['y']<title['bottom']-4:issues.append(f'{width}: title/pitch collision')
   else:
    if data['first'] and data['second'] and width<=740 and data['second']['y']<data['first']['bottom']-3:issues.append(f'{width}: mobile headline lines overlap')
   page.locator('.work-title').screenshot(path=str(OUT/f'build06-work-{width}.png'))
   page.locator('.about-heading').screenshot(path=str(OUT/f'build06-about-{width}.png'))
   page.locator('.method').screenshot(path=str(OUT/f'build06-method-{width}.png'))
   page.goto('http://127.0.0.1:8126/work/practical-solutions.html',wait_until='domcontentloaded')
   section=page.locator('.receipt-story')
   section.scroll_into_view_if_needed()
   geometry=page.evaluate('''() => {
     const b=s=>{let r=document.querySelector(s).getBoundingClientRect();return {x:r.x,y:r.y,b:r.bottom,h:r.height}};
     return {video:b('.receipt-story video'),text:b('.receipt-story>div:last-child'),section:b('.receipt-story')};
   }''')
   if width>740:
    mid1=(geometry['video']['y']+geometry['video']['b'])/2
    mid2=(geometry['text']['y']+geometry['text']['b'])/2
    if abs(mid1-mid2)>95:issues.append(f'{width}: video and text not vertically balanced: {round(mid1-mid2)}')
   section.screenshot(path=str(OUT/f'build06-receipt-{width}.png'))
   ctx.close()
  browser.close()
finally:
 server.terminate()
(OUT/'build06-report.json').write_text(json.dumps({'issues':issues,'measurements':measurements},indent=2))
for e in issues:print('ERROR',e)
print('MEASUREMENTS:',json.dumps(measurements,indent=2))
if issues:raise SystemExit(1)
print('PASS: responsive hierarchy, signature, chroma key, receipt alignment')
