# Android Tutorial

## About
- this is for the native Android (Kotlin + Jetpack Compose) tutorial — the Android mirror of the
  iOS track at https://lovemesomecoding.com/ios (`projects/ios_tutorial/`).

## Requirements
- create a new tutorial collection for Android, under the existing **Mobile** nav dropdown, next to
  iOS.
- **mirror the iOS series, adapted to Android** (Folau, 2026-10-10): same backbone and order, but
  merge or swap topics where Android genuinely differs (Gradle and build variants, process death and
  `SavedStateHandle`, the Keystore instead of the Keychain, Hilt).
- **build the demo app first** (Folau, 2026-10-10): `lovemesomecoding_demo_project/pizza/pizza-android-mobile`,
  Kotlin + Jetpack Compose, against the same Spring Boot API as the other four apps. Customer flows
  only, no `/admin` — same rule as the iOS and React Native apps.
- **Hilt for DI** (Folau, 2026-10-10). The DI lesson contrasts it with the iOS app's hand-written
  composition root.
- code in these posts must be code that runs: every block is quoted from the app and checked by
  `check_snippets.py`.
- keep posts to the point; cover the topics that matter.

---

## Layout

Same as `projects/ios_tutorial/`:

```
projects/android_tutorial/
  manifest.py         category metadata + one entry per post (slug, title, date, tags, excerpt, sources)
  posts/NN-slug.html  the post bodies, plain semantic HTML
  seed.py             writes the category and posts into a content tree
  check_content.py    length budget, prose share, heading and markup rules (no AWS needed)
  check_snippets.py   proves every quoted snippet still matches the demo app (no AWS needed)
  progress_report.md  status, decisions and the topic table — read this first
```

## Running it

```bash
python projects/android_tutorial/check_content.py
python projects/android_tutorial/check_snippets.py
python projects/android_tutorial/seed.py              # dry run against the local tree
python projects/android_tutorial/seed.py --env local --write
```

The nav is a **separate step** — add `android` to the Mobile group in
`lovemesomecoding_frontend/src/lib/nav.ts`.
