
(() => {
  'use strict';
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const root=document.documentElement.dataset.root||'';
  const media=window.IAM_MEDIA||{};
  const src=key=>{const file=media[key]||key;return /^(https?:|data:|\/)/.test(file)?file:root+encodeURI(file);};
  const fallback=src('fallback');
  const header=document.querySelector('.masthead');
  function measure(){if(header)document.documentElement.style.setProperty('--header-height',header.getBoundingClientRect().height+'px')}
  measure();addEventListener('resize',measure,{passive:true});
  if('ResizeObserver' in window&&header)new ResizeObserver(measure).observe(header);
  for(const image of document.querySelectorAll('img[data-media]')){
    if(image.dataset.media?.startsWith('overlay'))image.loading='eager';
    if(image.complete&&image.naturalWidth===0)image.src=fallback;
    image.addEventListener('error',()=>{if(!image.src.endsWith('fallback.gif')){image.src=fallback;image.classList.add('media-fallback');}});
  }
  const videos=[...document.querySelectorAll('video[data-media]')];
  for(const video of videos){
    video.poster=fallback;video.muted=true;video.loop=true;video.playsInline=true;
    if(!reduced.matches)video.setAttribute('autoplay','');
    video.addEventListener('error',()=>{
      if(video.dataset.failed)return;video.dataset.failed='true';video.style.display='none';
      const img=document.createElement('img');img.src=fallback;img.alt='Media unavailable';img.className='media-error-placeholder';video.insertAdjacentElement('beforebegin',img);
    });
  }
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>entries.forEach(({target,isIntersecting})=>isIntersecting&&!reduced.matches?target.play().catch(()=>{}):target.pause()),{threshold:.04});
    videos.forEach(v=>observer.observe(v));
  }else if(!reduced.matches)videos.forEach(v=>v.play().catch(()=>{}));
  if(reduced.matches)videos.forEach(v=>{v.pause();v.removeAttribute('autoplay');});
  const scroll= (hash,behavior='instant')=>{
    if(!hash||hash==='#')return false;
    const id=decodeURIComponent(hash.slice(1)),target=document.getElementById(id);if(!target)return false;
    target.scrollIntoView({block:'start',inline:'nearest',behavior:reduced.matches?'instant':behavior});return true;
  };
  document.querySelectorAll('a[href*="#"]').forEach(link=>link.addEventListener('click',e=>{
    let u;try{u=new URL(link.href)}catch{return}
    if(u.origin!==location.origin||u.pathname!==location.pathname||!u.hash||!document.getElementById(decodeURIComponent(u.hash.slice(1))))return;
    e.preventDefault();history.pushState(null,'',u.hash);scroll(u.hash,'smooth');
    const menu=document.querySelector('[data-menu]');if(menu)menu.open=false;
  }));
  if(location.hash){
    const sync=()=>scroll(location.hash);
    requestAnimationFrame(()=>requestAnimationFrame(sync));
    addEventListener('pageshow',()=>requestAnimationFrame(()=>requestAnimationFrame(sync)));
    addEventListener('load',()=>requestAnimationFrame(sync),{once:true});
  }
  addEventListener('hashchange',()=>scroll(location.hash,'smooth'));
})();
