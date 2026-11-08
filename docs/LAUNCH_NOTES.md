# IAMELLIOTT · Launch plan (for later approval)

Nothing in these notes is an instruction to change DNS or the live site before final review.

## 1 — New domain on GitHub Pages + Cloudflare

The verified intended domain is `iamelliott.me`. Existing site files and domain remain unchanged until approval. Before the cutover, check **Settings → Pages** in the repo to see the exact source branch and the existing custom domain. Do not accidentally publish `new-branch` or a preview branch.

At launch, prepare the new custom-domain configuration with Cloudflare DNS:
- GitHub Pages apex IPv4 A records according to the latest GitHub documentation: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
- `www` CNAME pointing to the GitHub Pages hostname `iamelliottluke.github.io`.
- Configure GitHub Pages `Custom domain` as `iamelliott.me`; add/rewrite the repository `CNAME` **only then**, replacing the old hostname.
- Start Cloudflare records as DNS-only until TLS has been verified. Turn on GitHub Pages **Enforce HTTPS** when the certificate is issued. Verify root and www URLs and canonical redirects.
- Plan the old `iamelliottfilms.com` redirect separately and only after validating the new site. Keep the old domain renewed until the redirect is reliable.

DNS records and host features can change. Confirm the records against GitHub's current Pages custom-domain documentation at launch.

## 2 — Full send/receive email

Wanted address: `hello@iamelliott.me`. A forwarding-only alias is **not** enough because the requirement is to send and receive under the branded address.

Preferred starting point: examine the existing Zoho Mail plan already used for Green Door. Check whether it supports a second hosted domain; the entry-level free plan may not. If not, compare the least-cost Zoho Mail mailbox subscription with an alternative provider before buying anything. No new mail subscription has been purchased.

When the provider is selected: verify domain ownership through Cloudflare, add the provider's **exact account-specific** MX/TXT/SPF/DKIM entries, configure DMARC and enable the mailbox. Do not mix Cloudflare Email Routing MX records with active Zoho Mail MX records on the same domain.

Verify externally: send from the new mailbox to an outside address, reply back, check sent-folder copies and spam results. Then update Formspree delivery email and test a live enquiry.

## 3 — Formspree

The existing endpoint `https://formspree.io/f/xqapyzld` receives the request. It is carried over unchanged. Formspree destination/notification address is an account-level setting and is not changed by writing `hello@iamelliott.me` in page code. After the mailbox is operational, edit the Formspree notification destination and verify it using the provider's confirmation flow.

## 4 — Publishing checks

- HTML semantics and responsive viewport: locally reviewed in desktop, laptop and two mobile browser emulations.
- JavaScript: parser checks passed.
- Media file existence: cross-checked against GitHub `new-branch` manifest.
- Audio: project preview loops are muted; full pieces are user-controlled.
- Contact form: retained known endpoint but **not tested end-to-end** on this build.
- GitHub Pages deployment, Cloudflare routing, production HTTPS, custom font rendering and real video playback: to be checked **after an authorised preview/deployment**.
