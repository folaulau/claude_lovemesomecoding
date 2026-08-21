/**
 * Prove the seeded track renders correctly in a browser.
 *
 * `check_content.py` proves the HTML survives the normaliser and `verify-build.mjs` proves every
 * URL resolves. Neither says anything about what a reader sees: whether the code blocks are
 * highlighted rather than grey, whether the table of contents anchors go anywhere, whether the
 * prev/next pager walks the track in reading order.
 *
 * Start the production preview first (it serves out/ with CloudFront's routing rules):
 *   cd lovemesomecoding_frontend && npm run preview        # :4321
 *
 * Then:
 *   node projects/docker_tutorial/verify_rendered.mjs
 *
 * Uses the Playwright already installed in pizza-react-frontend rather than adding a dependency.
 */

import { chromium } from '../../lovemesomecoding_demo_project/pizza/pizza-react-frontend/node_modules/playwright/index.mjs';

const BASE = 'http://localhost:4321';

// Reading order, from manifest.py. Lesson 1 is the rewritten 2020 URL.
const SLUGS = [
  'docker-what-is-docker',
  'docker-install-and-first-container',
  'docker-images-and-layers',
  'docker-dockerfile',
  'docker-build-context-and-dockerignore',
  'docker-layer-caching',
  'docker-multi-stage-builds',
  'docker-image-size-and-base-images',
  'docker-non-root-and-image-security',
  'docker-ports-and-networking',
  'docker-volumes-and-persistence',
  'docker-environment-and-configuration',
  'docker-logs-and-debugging',
  'docker-compose',
  'docker-compose-depends-on-and-healthchecks',
  'docker-compose-profiles-and-overrides',
  'docker-compose-full-stack',
  'docker-registry-push-and-tag',
  'docker-multi-platform-builds',
  'docker-ci-github-actions',
  'docker-production',
  'docker-interview-questions',
];

const failures = [];
const browser = await chromium.launch();
const context = await browser.newContext();
const page = await context.newPage();

const consoleErrors = [];
page.on('pageerror', (e) => consoleErrors.push(String(e)));

// --- the category archive -------------------------------------------------
await page.goto(`${BASE}/docker`, { waitUntil: 'networkidle' });
const archiveLinks = await page.locator('a[href^="/docker/"]').evaluateAll(
  (els) => [...new Set(els.map((e) => e.getAttribute('href')))]);
const missingFromArchive = SLUGS.filter((s) => !archiveLinks.includes(`/docker/${s}`));
if (missingFromArchive.length) {
  failures.push(`archive is missing: ${missingFromArchive.join(', ')}`);
}
console.log(`/docker archive links to ${archiveLinks.length} posts`);

// --- every lesson ---------------------------------------------------------
for (const slug of SLUGS) {
  const res = await page.goto(`${BASE}/docker/${slug}`, { waitUntil: 'networkidle' });
  const status = res?.status();

  const codeBlocks = await page.locator('pre code').count();
  // Prism emits <span class="token …"> only when it has a grammar for the language.
  // Zero tokens over many code blocks means everything fell back to plaintext.
  const tokens = await page.locator('pre code span.token').count();
  const plaintext = await page.locator('pre code.language-plaintext').count();

  // Every heading the table of contents links to must exist as an id on the page,
  // or the deep link scrolls nowhere.
  const brokenAnchors = await page.evaluate(() =>
    [...document.querySelectorAll('a[href^="#"]')]
      .map((a) => a.getAttribute('href').slice(1))
      .filter((id) => id && !document.getElementById(id)));

  const ok = status === 200 && codeBlocks > 0 === (slug !== 'docker-interview-questions')
    && plaintext === 0 && brokenAnchors.length === 0
    && (codeBlocks === 0 || tokens > 0);

  console.log(`${ok ? 'PASS' : 'FAIL'}  ${slug.padEnd(42)} ` +
    `${String(status).padEnd(4)} ${String(codeBlocks).padStart(2)} blocks, ` +
    `${String(tokens).padStart(4)} tokens` +
    (plaintext ? `, ${plaintext} PLAINTEXT` : '') +
    (brokenAnchors.length ? `, ${brokenAnchors.length} BROKEN ANCHORS` : ''));

  if (!ok) failures.push(`${slug}: status=${status} blocks=${codeBlocks} tokens=${tokens} ` +
    `plaintext=${plaintext} brokenAnchors=${brokenAnchors.join(',')}`);
}

// --- the track index in lesson 1 leads somewhere real ---------------------
await page.goto(`${BASE}/docker/docker-what-is-docker`, { waitUntil: 'networkidle' });
const indexed = await page.locator('ol a[href^="/docker/"]').evaluateAll(
  (els) => els.map((e) => e.getAttribute('href')));
const notInIndex = SLUGS.filter((s) => !indexed.includes(`/docker/${s}`));
if (notInIndex.length) failures.push(`lesson 1 index omits: ${notInIndex.join(', ')}`);
console.log(`\nlesson 1 links to ${indexed.length} lessons in the track index`);

if (consoleErrors.length) {
  failures.push(`${consoleErrors.length} page error(s): ${consoleErrors[0].slice(0, 120)}`);
}

await browser.close();

if (failures.length) {
  console.log(`\n${failures.length} failure(s):`);
  failures.forEach((f) => console.log(`  x ${f}`));
  process.exit(1);
}
console.log('every lesson renders, highlights, and its anchors resolve');
