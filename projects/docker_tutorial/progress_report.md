# Docker tutorial track — progress report

**Status:** ✅ **LIVE.** All 22 published to https://lovemesomecoding.com/docker on 2026-08-21.
**Started:** 2026-08-21
**Where it lands:** https://lovemesomecoding.com/docker

---

## What this is

`/docker` currently holds **exactly one post**: `docker-what-is-docker`, published 2020-10-11,
352 words, two headings. The URL is indexed and the content is thin.

This project builds a **22-post Docker track** in that collection — 21 new posts plus
`docker-what-is-docker` rewritten in place at its existing URL.

Every code sample comes from `lovemesomecoding_demo_project/pizza`, which means the images and
compose files the track teaches have to **exist and run** before the posts can quote them.

## Where it stands

| | |
|---|---|
| Topic table | ✅ 22 lessons, agreed 2026-08-21 |
| `manifest.py` | ✅ every lesson has slug, title, tags, excerpt, computed date |
| `seed.py` / `check_content.py` / `check_snippets.py` | ✅ all three run clean |
| Content pipeline | ✅ one small change — `nginx`, see below |
| Demo app Docker artifacts | ✅ **written, built and verified in a browser** |
| Post bodies | ✅ **22 of 22** written, verified in a browser, **published to prod** |

### The content pipeline needed one change

The Angular track had to teach the normaliser about `scss`. This one needed **`nginx`** and
nothing else.

Already supported before this project started, checked 2026-08-21: `app/services/content.py` lists
**`docker`**, **`yaml`**, `bash` and `properties` in `SUPPORTED_LANGUAGES`, with `dockerfile →
docker` and `yml → yaml` aliases, and `lovemesomecoding_frontend/src/lib/content.ts` statically
imports `prism-docker` and `prism-yaml`.

**Added:** `"nginx"` to `SUPPORTED_LANGUAGES` and `import 'prismjs/components/prism-nginx'` to
`content.ts`. Both frontends are served by nginx, so several lessons quote an `nginx.conf`; without
this each one renders as plaintext. `prismjs` already ships the grammar — no dependency change.

`docker` is also already in the **DevOps** nav group and has a display name (`nav.ts:28`, `nav.ts:53`).

## The versions this track is written against

Read off **this machine**, not chosen — same rule as the Angular track. A lesson claiming a version
the verified snippet was not produced by is exactly the drift nobody spots later.

| | |
|---|---|
| Docker Engine | 27.4.0 |
| Docker Compose | v2.31.0-desktop.2 |
| buildx | v0.19.2-desktop.1 |
| Host | Docker Desktop, **aarch64** (Apple Silicon) |
| Storage driver | overlay2 |

The aarch64 host is load-bearing for lesson 19: an image built here is arm64 by default, and
pushing it to an amd64 host is where `exec format error` comes from. That lesson is written from a
machine that actually has the problem.

## The gap — the demo app had no images

`lovemesomecoding_demo_project/pizza` had **no Dockerfile anywhere** when this project started.
What already existed:

| File | What it is |
|---|---|
| `pizza-springboot-backend/docker-compose.yml` | **dev backing services only** — MySQL required, plus Elasticsearch / Artemis / Mailpit behind compose profiles. Its header says the app is deliberately NOT in it, so a code change is a restart rather than a rebuild. |
| `src/main/resources/application-docker.properties` | points the app at that MySQL on host port 3308 |
| `stayhub/docker-compose.yml` | the same idea for StayHub (not used by this track) |

⚠️ **The existing `docker-compose.yml` must not be repurposed.** It is the daily dev loop for the
pizza app and its "app runs on the host" design is a deliberate decision recorded in its own
header. The full-stack file this track needs is a **separate** file.

### What was added

| Added | Serves lessons |
|---|---|
| `pizza-springboot-backend/Dockerfile` — multi-stage Maven → JRE, layer-extracted, non-root | 4, 6, 7, 8, 9 |
| `pizza-springboot-backend/.dockerignore` | 5 |
| `pizza-react-frontend/Dockerfile` — Node → nginx, `VITE_API_BASE_URL` build arg | 6, 7, 12 |
| `pizza-react-frontend/nginx.conf` — SPA fallback + `/api` reverse proxy | 10, 17 |
| `pizza-react-frontend/.dockerignore` | 5 |
| `pizza-angular-frontend/Dockerfile` — Node → nginx, `--configuration container` | 6, 7, 12 |
| `pizza-angular-frontend/nginx.conf` | 10, 17 |
| `pizza-angular-frontend/.dockerignore` | 5 |
| `pizza-angular-frontend/src/environments/environment.container.ts` + a `container` build configuration in `angular.json` | 12 |
| `pizza/compose.yaml` — MySQL + API + both frontends | 14, 15, 16, 17 |
| `pizza/.github/workflows/docker.yml` | 19, 20 |

### Verification — all of it was built and run

- **Every image builds.** `pizza-api:dev` 460 MB, `pizza-web:dev` 50 MB, `pizza-web-angular:dev` 50 MB.
- **The stack comes up.** `docker compose --profile angular up -d --build` → mysql healthy, api
  serving, both nginx containers serving.
- **It works in a real browser.** `projects/docker_tutorial/verify_stack.mjs` drives headless
  Chromium at both frontends: a deep link (`/menu`) returns the app rather than a 404, 14 product
  cards render, all three `/api/` requests go to the SPA's **own origin**, and there are no console
  errors. Both PASS.
- **Non-root confirmed.** `pizza-api` runs as uid 999, `pizza-web` as uid 101; stock
  `nginx:1.27-alpine` runs as uid 0 for contrast. The API user cannot write `/etc` and can write
  `/app/uploads`.
- **The workflow parses** as YAML. It has never *run* — see its own header.

### Measurements the posts quote

All read off this machine on 2026-08-21.

| | |
|---|---|
| `pizza-api` build stage vs runtime | **957 MB → 460 MB** |
| `pizza-api` layers | JRE base 340 MB · dependencies 120 MB · application 336 kB |
| `pizza-web` layers | nginx base 49 MB · built app **1.09 MB** |
| Base images | temurin 21-jdk 500 · 21-jre 340 · 21-jre-alpine 207 · node:22-alpine 160 · nginx-unprivileged 49 · alpine 8 |
| Alpine JRE experiment | `pizza-api` on `21-jre-alpine` is **327 MB**, and it boots — a real 133 MB saving |
| Cross-platform build, `pizza-web` | native arm64 **11 s**, emulated amd64 **30 s** (no cache) |
| Emulation tax, isolated | **2.69 s native vs 3.25 s emulated** — identical CPU-bound work (600 MB hashed) in `alpine:3.21` |

⚠️ **Do not quote a build-time ratio as the emulation tax.** The same test on `pizza-api` produced
87 s native and **20 s emulated** — emulation "faster", which is nonsense. Both figures are
dominated by Maven and npm downloading over the network, not by CPU, and `--no-cache` does not make
two such runs comparable. The isolated hash benchmark above is the honest number, and at ~1.2× it
is far below the 5–10× that older writing about QEMU reports. Lesson 19 states the measured figure,
says it is machine-specific, and does not generalise it.

⚠️ **`docker scout` could not be run.** It requires a Docker Hub login and I did not sign in on
Folau's behalf. Lesson 9 therefore teaches `docker scout cves` as a command with its login
requirement stated, and leads with the two things that *are* reproducible here: the non-root user,
and a secret being recoverable from `docker history` after a later `RUN rm`.

## The track as written

22 posts, 19,623 words, 183 code blocks. **Live on prod since 2026-08-21.**

- `check_content.py` — every code sample round-trips byte-for-byte; the manifest is consistent;
  lesson 1's index links all 22 lessons.
- `check_snippets.py` — **55 blocks matched the demo app verbatim**, 29 illustrative, 0 drift.
- `npm run build` — 643/643 posts served, 42/42 category counts agree, all indexed URLs
  accounted for. The build guard that fails if any of the 512 migrated URLs stops resolving passes.
- `verify_rendered.mjs` — all 22 pages return 200, every code block is genuinely tokenised by
  Prism (no plaintext fallback anywhere), every table-of-contents anchor resolves, no page errors.

Language usage across the track: 198 `bash`, 88 `yaml`, 66 `docker`, 8 `nginx`, 2 each of
`typescript`, `properties` and `json`. The `nginx` blocks are why the pipeline needed its one
change.

### Four snippets were caught by `check_snippets.py` and corrected

Worth recording, because it is exactly what the tool exists for. Four blocks had been condensed for
readability in a way that made them no longer true of the files they claimed to quote:

| Post | What was wrong |
|---|---|
| 7 (multi-stage) | the backend Dockerfile skeleton dropped the layer-extract steps and the `--chown` on the `COPY` |
| 7 (multi-stage) | the frontend skeleton omitted the `ARG`/`ENV` pair between `WORKDIR` and `COPY` |
| 12 (environment) | the `angular.json` excerpt ended `}` where the file has `},` |
| 14 (compose) | the mysql service excerpt omitted `command:` and `healthcheck:` |

All four now quote the real files with explicit `...` elision markers, so the parts that are quoted
are verified rather than merely plausible.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Existing `docker-what-is-docker` | Rewrite in place, keep the slug | Indexed URL with 352 words on it. Rewriting deepens the page without losing it. |
| Track size | **22 posts** | Folau chose it from a three-way option. Angular is 28, React 27; the README asks for "just the important things", so this is deliberately tighter. |
| Demo app | **pizza** | Richest Docker surface: a JVM multi-stage build, two SPA→nginx builds, MySQL with a healthcheck, and four services already behind compose profiles. |
| Verification | **Build and run everything** | Every Dockerfile is `docker build`-ed and the full stack is `compose up`-ed and exercised before a line of it is quoted. |
| Docker versions | Read off this machine | See the table above. |
| `docker-compose.yml` vs `compose.yaml` | Add a **new** `compose.yaml` at `pizza/`, leave the backend's dev file alone | The dev file's design is a recorded decision; overwriting it would break the daily loop the other tracks depend on. Using the modern `compose.yaml` name for the new one also makes the two impossible to confuse. |
| How the browser reaches the API | **nginx reverse-proxies `/api` in both frontends** | The first plan was to publish the API on host 8085 and let the frontends' baked `http://localhost:8085` find it. That died on contact with the machine: 8085, 4200 and 5173 were all already bound by Folau's running dev servers, and 3308 by the dev compose stack. Proxying is both the fix and the better production shape — one origin, so no CORS, and the image does not care what host port anything is published on. |
| Making the Angular app use a relative URL | A new `environment.container.ts` **plus** a `container` configuration in `angular.json` | Angular has no `import.meta.env` and no runtime environment mechanism, so `fileReplacements` is the only lever. Purely additive: `ng serve`, `ng build` and the test suites are untouched. The contrast with React's one-line build arg became lesson 12's central point rather than a workaround. |
| Host ports for the new stack | mysql **3309**, api **8086**, react **8080**, angular **4201** | Every dev-loop port was taken (3308 dev compose, 8085 `mvnw spring-boot:run`, 4200 `ng serve`, 5173 `vite`). Both stacks now run at once. |
| `container_name:` in `compose.yaml` | **Omitted entirely** | The dev compose file already owns the name `pizza-mysql`, and a container name is global to the daemon — `up` failed with "the container name is already in use". Compose's project-derived names (`pizza-mysql-1`) have no such problem. |
| App→MySQL inside compose | `SPRING_DATASOURCE_URL` env var, not a new properties file | Spring's relaxed binding turns the env var into `spring.datasource.url`, which is the twelve-factor shape lesson 12 is about — and it avoids a fifth `application-*.properties`. |
| CORS in compose | **Not configured, deliberately** | Superseded by the proxy decision above: both frontends call the API on their own origin, so the browser never makes a cross-origin request. Lesson 17 explains what would have been needed otherwise, since a containerised SPA hitting CORS is a common first failure. |

## Topic list

Reading order. `date` ascends so the prev/next pager reads lesson 1 → lesson 22.
All slugs new except lesson 1.

### Part 1 — Foundations

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 1 | `docker-what-is-docker` | **rewrite** | the track index; the versions table |
| 2 | `docker-install-and-first-container` | new | — (illustrative: `hello-world`, `nginx`) |
| 3 | `docker-images-and-layers` | new | `docker history` of the pizza API image |

### Part 2 — Building images

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 4 | `docker-dockerfile` | new | `pizza-springboot-backend/Dockerfile` |
| 5 | `docker-build-context-and-dockerignore` | new | the three `.dockerignore` files |
| 6 | `docker-layer-caching` | new | the `pom.xml`-then-`src/` and `package.json`-then-`src/` ordering |
| 7 | `docker-multi-stage-builds` | new | backend Dockerfile (JDK→JRE), frontend Dockerfile (Node→nginx) |
| 8 | `docker-image-size-and-base-images` | new | measured `docker image ls` output for both |
| 9 | `docker-non-root-and-image-security` | new | the `USER` lines; `docker scout` output |

### Part 3 — Running containers

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 10 | `docker-ports-and-networking` | new | the 3308→3306 shift; compose-network DNS |
| 11 | `docker-volumes-and-persistence` | new | `mysql-data` and the other named volumes |
| 12 | `docker-environment-and-configuration` | new | `SPRING_DATASOURCE_URL`, `VITE_API_BASE_URL` as a build arg |
| 13 | `docker-logs-and-debugging` | new | the Artemis healthcheck-with-no-curl story |

### Part 4 — Compose

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 14 | `docker-compose` | new | `pizza/compose.yaml` |
| 15 | `docker-compose-depends-on-and-healthchecks` | new | the MySQL healthcheck; `condition: service_healthy` |
| 16 | `docker-compose-profiles-and-overrides` | new | `docker-compose.yml`'s four profiles |
| 17 | `docker-compose-full-stack` | new | `pizza/compose.yaml` in full |

### Part 5 — Shipping

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 18 | `docker-registry-push-and-tag` | new | tagging the pizza images |
| 19 | `docker-multi-platform-builds` | new | buildx on this arm64 machine |
| 20 | `docker-ci-github-actions` | new | the workflow added to the demo app |
| 21 | `docker-production` | new | restart policies, limits, log drivers |
| 22 | `docker-interview-questions` | new | — |

## Frozen slugs

`docker-what-is-docker` was published 2020-10-11 and its URL is indexed. It is rewritten in
place — that slug must never change. `check_content.py` fails if it leaves the manifest.

Because it already carries a 2020 date and `upsert_post` never overwrites an existing date,
the first prod publish needs `seed.py --force-dates` for the reading order to come out right.

## Log

- **2026-08-21** — Project started. Surveyed `/docker` (1 post, prod and local agree), confirmed the
  content pipeline already supports `docker`/`yaml`, found the demo app has no Dockerfiles, and
  agreed the three decisions above with Folau.
- **2026-08-21** — Tooling written (`manifest.py`, `seed.py`, `check_content.py`,
  `check_snippets.py`); all run clean against an empty `posts/`. Added `nginx` to the content
  pipeline.
- **2026-08-21** — All Docker artifacts written, built and verified. Hit and resolved the host-port
  and `container_name` collisions with Folau's running dev servers — see the two new decision rows.
  `verify_stack.mjs` passes against both containerised frontends.
- **2026-08-21** — All 22 post bodies written. `check_snippets.py` caught four condensed quotes
  that had drifted from the files they cited; fixed with elision markers. Seeded to the local tree
  (643 posts, was 622), built, and verified in a browser with `verify_rendered.mjs`.
- **2026-08-21** — Took the containerised stack back down (`down`, not `down -v`, so the volumes
  survive) and stopped the preview server. Folau's development `pizza-mysql` container was left
  running throughout and is untouched.

## The publish — 2026-08-21

Folau published without a read-through; the track went to prod straight from the draft.

```
seed.py --env prod --write --force-dates    622 -> 643 posts, /docker count 22
npm run deploy                              build 394b0bd
```

Verified live:

- all 22 lesson URLs return **200**, and so does `/docker`
- `docker-what-is-docker` still resolves at its indexed 2020 URL, now **1,706 words** and dated
  2026-06-15 — `--force-dates` moved it to the front of the track as intended
- 22 `/docker/` URLs in `sitemap.xml`
- highlighting survived the deploy: `nginx` blocks are tokenised at the edge, not plaintext
- `verify-build.mjs` passed before upload — 643/643 posts, 42/42 category counts agree, every
  indexed URL accounted for
- the CloudFront Function was republished (94 redirects, 6.2 KB of the 10 KB limit) and the edge
  reports build `394b0bd`

⚠️ `--force-dates` has now been used. **Do not pass it again** — every later run must leave the
archive's dates alone.

## What is left

1. **Read it on the live site.** It was published unreviewed, so this is now a
   read-and-fix-forward job rather than a gate. Corrections are `seed.py --env prod --write`
   (no `--force-dates`) plus a deploy.
2. **Commit.** The change touches four places: this project, the demo app's new Docker artifacts,
   one entry each in `content.py` and `content.ts` for `nginx`, and the additive `container` build
   configuration in `angular.json`.

   ⚠️ **`content.py` and `content.ts` already had uncommitted changes before this project touched
   them** — `properties`, `scss`, `typescript`/`jsx`/`tsx` and a `graphql` entry for an unstarted
   Hasura track. This project added only the two `nginx` lines. Do not assume the whole diff on
   those two files belongs to the Docker track.
4. **Consider a screenshot or two.** Every other track has them; this one has none.
