# IAMELLIOTT | How to edit the site

The site is ordinary HTML, CSS and JavaScript. You can edit copy directly in GitHub and preview edits before publishing.

## Change written copy
- `index.html`: homepage, About, "Show. Don't Tell...", How I Work, contact form text, and card descriptions.
- `work/greendoor.html`: Green Door world-building and event case study.
- `work/campaigns.html`: [Nowhere to Wear It] and [EQUINOX] campaign case studies.
- `work/collaborations.html`: Medusa and DJ Kayelo case studies.
- `work/moving-imagery.html`: Hike Society, MTM, and original film descriptions.
- `work/practical-solutions.html`: workplace tool and receipt communications case studies.
- `work/welcome-mat.html`: newsletter, editorial and publication case study.

Find the sentence you want in GitHub's editor, replace only the words between HTML tags, then commit to a **review branch**. Don't remove tags like `<h2>`, `<p>`, or `</div>`.

## Swap an image, GIF or video
1. Upload the replacement file to the root of the repository.
2. Open `media.js`, find its descriptive key, and change the filename in quotes.
3. Save. You do **not** need to change all the page HTML references.

Examples: `butterfly: 'butterfly.gif'`, `greenDoor01: 'gd1.mp4'`, `welcomeMatIllustration01: 'wm1.png'`, `hikeSociety: 'hs.mp4'`.

The same butterfly GIF is currently reused in the homepage hero, How I Work and Contact sections. Its size and placement are controlled in `build04.css`.

## Change visual layout
`build04.css` holds the final component-specific layout rules. The older `site.css` and `build03.css` are retained until the separate post-approval CSS cleanup, to avoid changing the appearance unexpectedly.

## Publish safely
Review changes on a separate branch first. Do not edit `CNAME` or Cloudflare DNS until the final cutover to `iamelliott.me` is approved.

## Contact
The Formspree form action lives in `index.html`. Enquiry notifications are configured in your Formspree account; confirm delivery there after launch.
