IAMELLIOTT / ASSET INVENTORY AND DISPLAY GUIDE
Updated 10 November 2026

SOURCE OF TRUTH
- media.js controls named image/video assets. Change filenames there to replace media.
- index.html contains the homepage, About, Selected Work, How I Work and contact.
- work/*.html contain the six case studies.
- site.css, build03.css and build04.css are loaded in that order. Build04 contains the latest layout rules.
- GIFs, images and video files live at the repository root.
- Keep instructions flexible for mobile readability; desktop alignments need not be repeated exactly on narrow screens.

HOMEPAGE
- overlay6.webp → header-overlay behind "I make good ideas into good work." via media.js overlayHome.
- butterfly.gif → hero, How I Work and contact, at individually controlled sizes/positions.
- about.gif → looping portrait in About via media.js about.
- e.gif → original animated handwritten Elliott above the About heading via media.js elliottSignature (replaces the older typeset handwritten text).
- overlay5.webp → How I Work background, via media.js overlayMethod and site.js client-side green-screen key. It is present in the repository, stretched to cover the section at low opacity above the existing acid background. Its pixels are keyed in a canvas at page load; the original source is preserved.
- Selected Work videos → door.mp4, ntwi2.mp4, collab1.mp4, hs.mp4, receipt.mp4, wm1.mp4 (mapped in media.js).

CASE-STUDY HEADER OVERLAYS
- overlay2.mp4 → Green Door / "I built a world, then opened the door."
- overlay1.webp → Campaigns / "Make them look."
- overlay1.mp4 → Collaborations / "Good work, good company."
- overlay3.mp4 → Moving Imagery / "Imagery that moves."
- overlay4.mp4 → Practical Solutions / "Working smarter, not harder."
- overlay8.gif → The Welcome Mat.
These are deliberately low-opacity, cover-fitted decorative media.

PROJECT FILMS AND PHOTOS
- gd1.mp4–gd4.mp4 → Green Door storytelling films.
- door.mp4 → door opening visual, looping on the Green Door tile and the case study.
- ntwi1.mp4–ntwi3.mp4 → Nowhere to Wear It campaign.
- eq1.mp4–eq6.mp4 → Gathering IV / EQUINOX.
- collab1.mp4 and collab2.mp4 → DJ and Medusa collaboration films.
- hs.mp4 → Hike Society film alongside "People first. Pretty landscapes second."
- mtm1michael.mp4 / mtm2tim.mp4 / mtm3marcus.mp4 → MTM interview edits.
- reel1.mp4–reel4.mp4 → moving imagery / personal short film previews.
- wm1.mp4–wm4.mp4 → The Welcome Mat video excerpts.
- wm1.png and wm2.png → illustrations beside "Something to read before you knock" and "A little longer than a reel."
- welcome mat print.pdf → downloadable The Welcome Mat Volume I PDF.
- receipt.mp4 → loop and visual within "A fair go should be easier to find."
- receipt.pdf → original source of receipt-divider.png, the long horizontal visual dividing the final two Practical Solutions sections; the final QR portion is excluded from the rendered artwork.
- fallback.gif → video/image loading/error artwork where configured.

FAVICON / INSTALLATION
- favicon.svg → adaptive light/dark site favicon.
- favicon-96x96.png and favicon.ico → browser fallback icons.
- apple-touch-icon.png → Apple home-screen icon.
- web-app-manifest-192x192.png and web-app-manifest-512x512.png → installable app icons.
- site.webmanifest → IAMELLIOTT app metadata.
- favicon.png → legacy image retained for existing Open Graph metadata. Not the primary browser icon.

BEHAVIOUR / ACCURACY
- Autoplay/scroll-based muted preview behaviour is controlled by site.js and build03.js.
- WORK navigation dropdowns link to all six portfolio case studies on desktop and mobile.
- New overlays and GIFs are never synthetically recreated: original files must be uploaded first.
- Do not remove assets solely because they are not referenced in current HTML; archived work may still need them.

BUILD 06 OPTICAL FINISH
- e.gif is rendered 20% larger above the redacted jack, its centre aligned near the top of the word, with responsive width limits.
- How I Work overlay5.webp is a still background keyed by the existing JS, not a new video.
- Selected Work prioritises Show. Don't Tell..., then Pick a project below.; on mobile the headline breaks into two deliberately larger lines and the quotation follows as a secondary item.
- Practical Solutions section 03 keeps its original receipt video dimensions and left-aligned copy, centring the text column vertically beside the film on desktop. Mobile remains stacked.
