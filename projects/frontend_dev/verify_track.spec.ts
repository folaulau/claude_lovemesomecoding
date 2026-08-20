import { expect, test } from '@playwright/test';

/**
 * Delivery check for the Frontend Dev track.
 *
 * Drives the built site through a real browser and asserts the things a curl
 * status check cannot see: that the archive lists all 12 in reading order, that
 * the two pre-existing 2019 URLs still resolve to the rewritten posts, that code
 * samples are actually highlighted, and that the cross-track links to the live
 * /backend-dev posts work.
 *
 * Run against `npm run preview` (:4321) from the frontend repo:
 *
 *   cd lovemesomecoding_frontend && npm run preview
 *   cd ../lovemesomecoding_demo_project/pizza/pizza-react-frontend
 *   npx playwright test ../../../projects/frontend_dev/verify_track.spec.ts \
 *     --config /dev/null --reporter=list
 */

const BASE = process.env.SITE_BASE_URL ?? 'http://localhost:4321';

/** The 12 posts, in reading order. Slugs 2 and 5 are the pre-existing indexed ones. */
const TRACK = [
  ['frontend-dev-get-started', 'Frontend Dev – Get Started'],
  ['frontend-dev-what-is-a-frontend-engineer', 'Frontend Dev – What a Frontend Engineer Actually Does'],
  ['frontend-dev-html-css-and-the-browser', 'Frontend Dev – The HTML, CSS and Browser You Actually Need'],
  ['frontend-dev-javascript-and-typescript', 'Frontend Dev – The JavaScript and TypeScript You Actually Need'],
  ['frontend-dev-what-to-learn-in-a-framework-as-a-frontend-engineer', 'Frontend Dev – What to Learn in a Framework'],
  ['frontend-dev-state-management', 'Frontend Dev – State Management'],
  ['frontend-dev-talking-to-the-backend', 'Frontend Dev – Talking to the Backend'],
  ['frontend-dev-routing-and-forms', 'Frontend Dev – Routing, Forms and Validation'],
  ['frontend-dev-auth-and-security', 'Frontend Dev – Authentication and Security in the Browser'],
  ['frontend-dev-performance-and-accessibility', 'Frontend Dev – Performance and Accessibility'],
  ['frontend-dev-testing', 'Frontend Dev – Testing'],
  ['frontend-dev-build-and-deployment', 'Frontend Dev – Build Tooling and Deployment'],
] as const;

test('the archive lists all 12 posts', async ({ page }) => {
  await page.goto(`${BASE}/frontend-dev`);
  await expect(page.getByRole('heading', { name: 'Frontend Development', level: 1 })).toBeVisible();

  for (const [slug, title] of TRACK) {
    await expect(
      page.locator(`a[href="/frontend-dev/${slug}"]`).first(),
      `archive should link ${slug}`,
    ).toHaveCount(1);
    expect(await page.locator(`a[href="/frontend-dev/${slug}"]`).first().isVisible()).toBe(true);
    expect(title.startsWith('Frontend Dev')).toBe(true);
  }
});

test('every post renders with its title and a table of contents worth of headings', async ({ page }) => {
  for (const [slug, title] of TRACK) {
    const response = await page.goto(`${BASE}/frontend-dev/${slug}`);
    expect(response?.status(), `${slug} status`).toBe(200);

    await expect(page.getByRole('heading', { name: title, level: 1 })).toBeVisible();

    // Every post needs a real navigable outline. The old 2019 posts had ZERO
    // headings of any level, which is why neither had a table of contents.
    //
    // Counted across h2+h3 rather than h2 alone: two posts in this track are
    // organised as two big halves with deep h3 nesting (javascript-and-typescript
    // is 4 h2 / 10 h3), which is a legitimate shape, and an h2-only floor
    // wrongly fails them. 7 is the floor the published /backend-dev track sets.
    const headings = await page.locator('article :is(h2, h3), main :is(h2, h3)').count();
    expect(headings, `${slug} should have a real outline`).toBeGreaterThanOrEqual(7);

    // Every heading needs an id, or its deep link is dead.
    const withoutId = await page
      .locator('article :is(h2, h3):not([id]), main :is(h2, h3):not([id])')
      .count();
    expect(withoutId, `${slug} has headings with no anchor`).toBe(0);
  }
});

test('the two pre-existing 2019 URLs still resolve to the rewritten posts', async ({ page }) => {
  // These were published 2019-02-06 and are indexed. Losing either is a real cost.
  for (const slug of [
    'frontend-dev-what-is-a-frontend-engineer',
    'frontend-dev-what-to-learn-in-a-framework-as-a-frontend-engineer',
  ]) {
    const response = await page.goto(`${BASE}/frontend-dev/${slug}`);
    expect(response?.status(), `${slug} must not 404`).toBe(200);

    // Rewritten, not the 2019 text: the WordPress wrapper is gone...
    await expect(page.locator('.boldgrid-section')).toHaveCount(0);
    // ...and the truncated "#8 Cache" dead end is gone from the framework post.
    await expect(page.getByText('#8 Cache', { exact: true })).toHaveCount(0);
  }
});

test('code samples are highlighted in the shape the build-time highlighter emits', async ({ page }) => {
  await page.goto(`${BASE}/frontend-dev/frontend-dev-talking-to-the-backend`);

  const blocks = page.locator('pre[class^="language-"] > code[class^="language-"]');
  expect(await blocks.count()).toBeGreaterThan(5);

  // Prism ran: if it had not, there would be no token spans at all.
  expect(await page.locator('pre .token').count()).toBeGreaterThan(20);
});

test('cross-track links to the live /backend-dev posts resolve', async ({ page }) => {
  await page.goto(`${BASE}/frontend-dev/frontend-dev-get-started`);

  const link = page.locator('a[href="/backend-dev"]').first();
  await expect(link).toBeVisible();
  await link.click();

  await expect(page).toHaveURL(/\/backend-dev$/);
  await expect(page.getByRole('heading', { name: 'Backend Development', level: 1 })).toBeVisible();
});

test('the track reads as a track — each post links to the next', async ({ page }) => {
  for (let i = 0; i < TRACK.length - 1; i++) {
    const [slug] = TRACK[i];
    const [nextSlug] = TRACK[i + 1];
    await page.goto(`${BASE}/frontend-dev/${slug}`);
    await expect(
      page.locator(`a[href="/frontend-dev/${nextSlug}"]`).first(),
      `${slug} should point at ${nextSlug}`,
    ).toHaveCount(1);
  }
});
