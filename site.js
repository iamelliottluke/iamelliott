(() => {
  const prefix = document.documentElement.dataset.root || '';
  const MEDIA = window.IAM_MEDIA || {};
  const preferReduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const asset = key => {
    const value = MEDIA[key] || key || '';
    return /^(https?:|data:|\/)/.test(value) ? value : prefix + encodeURI(value);
  };

  document.querySelectorAll('img[data-media]').forEach(img => {
    img.src = asset(img.dataset.media);
    img.loading ||= 'lazy';
    img.addEventListener('error', () => {
      if (img.dataset.fallback) { img.src = asset(img.dataset.fallback); img.removeAttribute('data-fallback'); }
      else img.classList.add('media-error');
    }, { once: true });
  });

  document.querySelectorAll('a[data-media-href]').forEach(link => link.href = asset(link.dataset.mediaHref));

  document.querySelectorAll('video[data-media]').forEach(video => {
    const key = video.dataset.media;
    const source = video.querySelector('source');
    if (!source) return;
    source.src = asset(key);
    if (video.dataset.poster) video.poster = asset(video.dataset.poster);
    video.load();
    video.addEventListener('error', () => video.classList.add('video-error'));
  });

  const previewVideos = [...document.querySelectorAll('video[data-preview]')];
  if ('IntersectionObserver' in window) {
    const mediaObserver = new IntersectionObserver(entries => {
      for (const entry of entries) {
        const video = entry.target;
        if (entry.isIntersecting && !preferReduced) video.play().catch(() => {});
        else video.pause();
      }
    }, { rootMargin: '80px', threshold: 0.15 });
    previewVideos.forEach(video => mediaObserver.observe(video));
  } else if (!preferReduced) {
    previewVideos.forEach(video => video.play().catch(() => {}));
  }
  if (preferReduced) previewVideos.forEach(v => { v.pause(); v.removeAttribute('autoplay'); });

  // Reveal on scroll, without hiding any content when JavaScript is unavailable.
  if ('IntersectionObserver' in window && !preferReduced) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } });
    }, { threshold: 0.04, rootMargin: '0px 0px -24px 0px' });
    document.querySelectorAll('[data-reveal]').forEach(el => { el.classList.add('will-reveal'); observer.observe(el); });
  }

  // The source image is pre-keyed once in CI, not per browser visit.
  // Its original overlay5.webp is retained untouched for future replacements.
  const methodOverlay = document.querySelector('[data-method-overlay]');
  if (methodOverlay && MEDIA.overlayMethod) {
    const source = new Image();
    source.onload = () => {
      methodOverlay.style.backgroundImage = 'url("' + asset('overlayMethod') + '")';
      methodOverlay.classList.add('is-ready');
    };
    source.onerror = () => { methodOverlay.hidden = true; };
    source.src = asset('overlayMethod');
  }

  // Work menus: native keyboard-accessible details, dismiss on Escape/outside click.
  const allWorkMenus = document.querySelectorAll('.work-menu, .work-mobile-submenu');
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      allWorkMenus.forEach(menu => { menu.open = false; });
      const mainMenu = document.querySelector('[data-menu]');
      if (mainMenu) mainMenu.open = false;
    }
  });
  document.addEventListener('click', event => {
    allWorkMenus.forEach(menu => {
      if (!menu.contains(event.target)) menu.open = false;
    });
  });

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());

  // Mobile navigation closes after an in-page selection.
  const nav = document.querySelector('[data-menu]');
  nav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { nav.open = false; }));

  // Existing, already-used Formspree endpoint. Update destination inside Formspree account.
  const form = document.querySelector('[data-enquiry]');
  if (form) {
    const feedback = form.querySelector('[data-form-feedback]');
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const button = form.querySelector('button[type=submit]');
      button.disabled = true;
      feedback.textContent = 'Sending...';
      try {
        const result = await fetch(form.action, {
          method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' }
        });
        if (!result.ok) throw new Error('Request not accepted');
        form.reset();
        feedback.textContent = 'Sent. Thanks for getting in touch.';
      } catch (_) {
        feedback.textContent = 'Could not confirm delivery. Please email hello@iamelliott.me directly instead.';
      } finally { button.disabled = false; }
    });
  }
})();
