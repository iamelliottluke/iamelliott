# IAMELLIOTT | Editing and publishing guide

The live site at https://iamelliott.me is static HTML, CSS and JavaScript hosted through GitHub Pages from `main`. Cloudflare manages DNS, and GitHub Pages handles the HTTPS certificate.

## Edit copy
- `index.html`: homepage headline, About, Selected Work, How I Work and contact.
- `work/greendoor.html`: Green Door Community.
- `work/campaigns.html`: Nowhere to Wear It and Equinox.
- `work/collaborations.html`: Medusa and DJ collaborations.
- `work/moving-imagery.html`: Hike Society, MTM and films.
- `work/practical-solutions.html`: workplace tool, SDA communication and receipt story.
- `work/welcome-mat.html`: editorial, newsletter and print publication.

Edit the words between existing HTML tags. Avoid inadvertently removing surrounding tags or attributes.

## Replace media
1. Upload the replacement image, GIF, video or PDF to the repository root on a review branch.
2. Update the corresponding filename in `media.js` when the asset uses a media key.
3. Check the current mapping and intended placement in `assets readme.txt`.
4. Use the browser QA results and visually inspect the pages before publishing.

Some stills (including `receipt-divider.png`) and icons are referenced directly in HTML and are not mapped through `media.js`. The original `overlay5.webp` is preserved, while `overlay5-keyed.webp` is its transparent How I Work display derivative.

## Layout and colour
`site.css`, `build03.css`, and `build04.css` are **all loaded**, in that order. Most later page-specific optical adjustments live at the end of `build04.css`. Avoid deleting or consolidating these layers without screenshots showing identical rendering across the site.

The homepage's Corazón accent is `--accent-corazon: #CC2208`, scoped to the home page. Case-study palettes are separate. Responsive rules deliberately differ between desktop and mobile.

## Publish and verify
1. Make changes on a new review branch based on `main`.
2. Open a pull request; check the **Site QA** workflow and any screenshot artifacts.
3. Merge only after approving the result.
4. Confirm the GitHub Pages deployment workflow **concluded successfully**.
5. Test `https://iamelliott.me` and an affected case study in a private browser window.

The production custom domain is set by `CNAME`. Do not edit it, DNS records, the old-domain redirect, or email settings for ordinary content updates.

## Contact
The Formspree form endpoint is in `index.html`; the notification destination and delivery status are managed inside Formspree, not by the contact email displayed on the page.
