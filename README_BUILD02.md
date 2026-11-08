# IAMELLIOTT / Build 02

**Status:** Unpublished site source for review. Not yet deployed, domain not connected, no account settings changed.

## What's included

- `index.html` — editorial homepage, six featured work areas, the About section, portrait GIF, contact form.
- `work/` — six individually linkable project pages: Green Door, Campaigns, Collaborations, Moving Imagery, Practical Solutions, The Welcome Mat.
- `site.css` — responsive design, accessible type scaling, warm neutral palette and brighter Green Door green.
- `media.js` — **the single place to change media filenames**. Asset keys stay fixed across the site.
- `site.js` — deferred video playback, basic motion/reduced-motion support, navigation and contact-form state.
- `docs/LAUNCH_NOTES.md` — safe domain, email and Formspree setup steps.

## How to use it

This is a **source overlay**, not a standalone archive of every media file. The original media, font, `about.gif`, butterfly images and PDF already live in the GitHub repository's `new-branch`. The source in this archive should eventually be merged into that same repository only after review. **Do not overwrite the repository's `CNAME` file during preview.**

No backend, build tool, framework or recurring software subscription is required for the static site itself.

### Replacing photos, GIFs or videos

1. Add your replacement image or video to the repository.
2. Open `media.js`.
3. Replace the corresponding filename, for example: `about: 'about.gif'` → `about: 'portrait.webp'`.
4. Keep the media key to the left of the colon unchanged. The update will propagate everywhere that asset is used.

The existing `about.gif` is in use. Replace it with a JPG/PNG/WEBP through `media.js` at any time. The custom handwriting is loaded from `ElliottsHandwriting-Regular.ttf` by the `@font-face` rule at the top of `site.css`.

### Editing copy

Each case study is plain HTML in `work/`. The homepage is `index.html`. Changing copy does not require rebuilding or editing a JavaScript configuration. Keep normal semantic headings (`h1`, `h2`) intact and update `<title>` and meta descriptions if the project identity changes.

### Previewing properly

The media files are intentionally not duplicated here to avoid another 120MB+ download. You can double-click `index.html` from the extracted review ZIP while online: it will attempt to load original media from your public GitHub `new-branch`. **The deployed version does not depend on GitHub raw media URLs**: when served over HTTP(S), it uses the real files beside the source in the repository. For the most reliable media testing, preview inside a checkout of the original repository.

For a local preview, copy the source overlay into a local checkout of your existing GitHub repository, preferably on a separate preview branch. Then run `python3 -m http.server 8080` from the repository root and open `http://localhost:8080` in a browser. Do not switch the configured GitHub Pages deployment branch until launch is approved.

### Notes about motion

- Project preview videos begin only when visible. Larger project videos load on demand and show native controls.
- The butterfly emergence video was not added as a blocking page loader. The photographs are more intentional here, with less complexity and better accessibility.
- Motion is disabled where `prefers-reduced-motion` is enabled.

### Contact form and email

The form retains the existing working Formspree endpoint `https://formspree.io/f/xqapyzld`. Its notification recipient must be changed in the Formspree account **after** `hello@iamelliott.me` exists and is verified. The mailbox is not yet created; the mailto link will not work until then.

### Content integrity

- Green Door event description is intentionally focused on progression, experience and creative/business model rather than a profitability claim.
- The Gatherings shown are III and IV only.
- The two campaigns are NTWI and EQUINOX, with numerical results attributed to specific screenshots or archived working records.
- Hike Society and MTM are presented as commercial work with roles and deliverables that match available source evidence.
- The Backroom Layout Helper diagram uses a fictitious van and sample sequence values. It is not confidential store operational data.
- The Coles recognition is included only as short text; obtain approval before publishing a quote attributed to Coles or naming colleagues.

## Prelaunch requirements

1. Review actual video and photo composition at laptop, phone and desktop sizes **using real assets**. The source-level checks were carried out, but media playback from the GitHub branch could not be verified locally during this build.
2. Confirm all media rights and any recognitions or client brand names are allowed to be published.
3. Establish the full `hello@iamelliott.me` mailbox and update Formspree notifications.
4. Review any remaining brand handles and metadata and verify the external links.
5. Test the contact form to completion with a real email delivery and mobile devices.
6. Change DNS/GitHub Pages `CNAME` and old-domain redirect **only at the approved launch**.
