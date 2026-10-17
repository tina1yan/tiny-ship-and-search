---
name: publish-cloudflare-search-console
description: Publish a small personal website to Cloudflare Pages and verify the live site, crawlability, Google Search Console ownership, sitemap submission, and observed indexing status. Use for a short publish-and-check workflow, rather than a broad SEO audit.
---

# Tiny Ship & Search

A deliberately small skill: ship a personal website, inspect the real result, and report exactly how far Google discovery has progressed.

## Start from the existing project

- Read the project's instructions. Recover its source/build folder, Cloudflare account and Pages project, production branch, and intended public URL from available context. Ask only for details that cannot be established.
- Reuse the existing deployment method. For a new static site, Cloudflare Pages dashboard Direct Upload is a simple option; Git integration suits ongoing automatic deployments. Direct Upload cannot later be switched to Git integration in the same project. Check [current Cloudflare guidance](https://developers.cloudflare.com/pages/get-started/direct-upload/) before choosing.
- Use the existing free plan where suitable; check [current limits](https://developers.cloudflare.com/pages/platform/limits/). Do not enable billing, buy a domain, or add unrelated services without authorization. A custom domain is optional.
- Prepare and inspect the public build. Publish only the personal project and its required public assets. Exclude private files and credentials. Follow existing authorization for publishing; a read-only check does not authorize deployment.

## Publish, then inspect production

1. Build with the project's own command, or use the intended static folder. Publish through the existing dashboard, connected Cloudflare tools, or installed CLI. Dashboard drag-and-drop does not compile a `functions/` directory; use a supported method if the project needs Functions.
2. Wait for terminal deployment success. Record the deployment identifier or dashboard evidence and the intended production URL. A build log alone does not prove the production site is current.
3. Fetch that exact production URL with GET, following redirects. Confirm a final successful HTML response and a distinctive marker from the intended version. Check the actual response body as well as its status.
4. Open production in a browser. Check the page visually and exercise its main link or action. Record unavailable checks honestly. Use the production hostname, rather than submitting a hash or branch preview to Google. [Pages preview deployments](https://developers.cloudflare.com/pages/configuration/preview-deployments/) normally have an `X-Robots-Tag: noindex` header.

## Check discovery files on the deployed host

- Inspect the final page's HTTP `X-Robots-Tag` and HTML robots/googlebot directives for `noindex` or `none`. Review any bot-specific rule in context. Inspect `robots.txt` for rules that block the intended pages or their required resources. A missing robots file is not automatically a crawl block.
- Confirm a useful page title and description, an intentional canonical URL, and real page content. If content depends on JavaScript, inspect the rendered page; an HTML shell alone cannot verify what Google renders.
- Fetch the actual sitemap URL. Confirm a real XML sitemap or sitemap index, not an HTML fallback that merely returns 200. Check that entries are intended, absolute, canonical production URLs, and inspect their responses. For a tiny site, check every entry; disclose sampling on larger sites. A sitemap is useful for discovery, not a guarantee of indexing.
- Confirm `robots.txt` advertises the intended sitemap where provided. Do not treat title/description/canonical tags or a sitemap as a promise of ranking.
- Make only necessary, authorized fixes in the source, redeploy, and repeat the affected checks on production. Keep intentional preview exclusions intact.

## Verify Google Search Console

1. Use the property matching the intended production URL. For a `pages.dev` address, use a URL-prefix property and an available HTML file or HTML tag method. A Domain property requires DNS control; do not attempt to verify ownership of `pages.dev` itself. See [ownership methods](https://support.google.com/webmasters/answer/9008080).
2. Deploy the exact verification file or tag Google provides. Fetch it from production and compare its content; a successful HTTP status or an SPA fallback is insufficient. Keep the verification method in place after success.
3. Complete verification in the authenticated Search Console session and observe the success state. A public verification file alone does not prove ownership was accepted. If login, MFA, CAPTCHA, or unavailable account access blocks the step, preserve a precise checkpoint for the user; do not invent success or bypass the gate.
4. Submit the canonical sitemap once and record the observed submission/processing state and sitemap URL. A submitted sitemap and a successfully processed sitemap are separate observations. See [Google's sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
5. Inspect the exact canonical page with [URL Inspection](https://support.google.com/webmasters/answer/9012289). Separate the indexed result from a live test. If appropriate and authorized, request indexing once and record the result. A live test saying the URL is available to Google does not prove that it is indexed.

Google controls crawling and indexing. [A request is not a guarantee](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl). Do not repeatedly submit the same URL, promise a deadline, or use the Indexing API for an ordinary personal website. Do not create a monitoring schedule unless requested.

## Close with evidence

Use [the short result template](references/result-template.md). Give each step its own status, time, URL, and observation. Keep evidence local unless public sharing is requested; redact account details and credential material.

- **DEPLOYED:** Cloudflare success and the intended version observed on production.
- **PUBLIC_CHECKS_PASSED:** specified public checks passed; this is not proof of Google crawlability or indexing.
- **OWNERSHIP_VERIFIED:** Search Console accepted ownership.
- **SITEMAP_SUBMITTED / SITEMAP_PROCESSED:** only the state actually observed.
- **INDEXING_REQUESTED:** an accepted request was observed.
- **INDEXED_CONFIRMED:** the indexed URL Inspection result confirms indexing for that exact URL; report Google's selected canonical too.
- **PENDING / NEEDS_USER / FAILED / NOT_CHECKED:** use these whenever evidence stops short.

State the last confirmed step and the next useful action. Never collapse the chain into a single “done” or infer account-level success from public files.
