"""The Docker track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and the last lesson is the
newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because
this track is authored before it is published: when the publish date is finally
known, move START_DATE and every lesson re-bases in order.

One slug here is not new. `docker-what-is-docker` was published 2020-10-11 with a
352-word body and its URL is indexed. It is being rewritten in place, NOT
replaced — changing that slug changes a live URL. Because it carries a 2020 date
and `upsert_post` never overwrites an existing date, seeding needs
`seed.py --force-dates` for the reading order to come out right.
See progress_report.md.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "docker",
    "name": "Docker",
    "description": (
        "Docker from the ground up — images, Dockerfiles, layer caching, multi-stage builds, "
        "networking, volumes, Compose and shipping to production, every example lifted from a "
        "real ordering app."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, which already lists `docker`
# under DevOps with the display name "Docker" — nothing to add there.
NAV_GROUP = "DevOps"

# The app every code sample is taken from. The Docker artifacts did not exist
# when this track started; they were added by it and are built and run before
# being quoted. See progress_report.md.
DEMO_APP = "lovemesomecoding_demo_project/pizza"

# The versions the whole track is written against. Lesson 1 prints this table,
# and every other lesson assumes it.
#
# These are READ OFF THIS MACHINE, not chosen — `docker version`, `docker compose
# version`, `docker buildx version`, `docker info`. The host architecture is in
# here on purpose: lesson 19 is about arm64-vs-amd64 and is written from a
# machine that actually has the problem.
VERSIONS = {
    "docker engine": "27.4.0",
    "docker compose": "v2.31.0",
    "buildx": "v0.19.2",
    "host": "Docker Desktop on aarch64 (Apple Silicon)",
    "storage driver": "overlay2",
}

# What the demo app itself is built from, quoted by the image lessons.
APP_VERSIONS = {
    "java": "21 (Spring Boot 4.1.0)",
    "mysql": "8.4",
    "node": "22",
    "nginx": "1.27-alpine",
}

# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later,
# so the pager reads lesson 1 -> lesson 22. Re-base the whole track by editing
# these two values; nothing else needs to change.
START_DATE = datetime(2026, 6, 15, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    """The publish timestamp for the index-th lesson, 0-based."""
    return (START_DATE + timedelta(days=STEP_DAYS * index)).strftime("%Y-%m-%dT%H:%M:%S")


# Authored in reading order. `state` is documentation, not data: "rewrite" means
# the slug already exists on the live site and must not change.
_TRACK = [
    # ------------------------------------------------------------ foundations
    {
        "slug": "docker-what-is-docker",
        "title": "Docker – What It Is and Why It Exists",
        "state": "rewrite",  # published 2020-10-11, 352 words, URL is indexed
        "tags": ["docker", "containers", "devops"],
        "excerpt": (
            "Start here. What a container actually is and how it differs from a virtual machine, "
            "the \"works on my machine\" problem it was built to solve, the difference between an "
            "image and a container, the exact versions this track is written against, the demo "
            "application every example is taken from, and the full lesson index in reading order."
        ),
    },
    {
        "slug": "docker-install-and-first-container",
        "title": "Docker – Install It and Run Your First Container",
        "state": "new",
        "tags": ["docker", "containers", "devops"],
        "excerpt": (
            "Docker Desktop or Docker Engine, and how to tell which one you have. Then the six "
            "commands you will use every day — `run`, `ps`, `logs`, `exec`, `stop`, `rm` — what "
            "each flag in `docker run -d -p 8080:80 nginx` is doing, and why your container "
            "exited the instant it started."
        ),
    },
    {
        "slug": "docker-images-and-layers",
        "title": "Docker – Images, Layers and Tags",
        "state": "new",
        "tags": ["docker", "images", "containers"],
        "excerpt": (
            "An image is a stack of read-only layers and a container is a thin writable layer on "
            "top — which explains sharing, caching, image size and why editing a file in a "
            "running container changes nothing permanent. Reading `docker history`, what a tag "
            "really is, and why a digest is the only thing that pins an image."
        ),
    },
    # -------------------------------------------------------- building images
    {
        "slug": "docker-dockerfile",
        "title": "Docker – Writing a Dockerfile",
        "state": "new",
        "tags": ["docker", "dockerfile", "images"],
        "excerpt": (
            "The instructions that actually matter: `FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV`, "
            "`EXPOSE`, `USER`, and the `CMD` versus `ENTRYPOINT` distinction that trips up "
            "everyone once. Built up line by line into the real Dockerfile that produces the "
            "pizza API image."
        ),
    },
    {
        "slug": "docker-build-context-and-dockerignore",
        "title": "Docker – The Build Context and .dockerignore",
        "state": "new",
        "tags": ["docker", "dockerfile", "build"],
        "excerpt": (
            "`docker build .` uploads that entire directory to the builder before it reads a "
            "single instruction — which is why a build can sit for a minute doing apparently "
            "nothing. What the context is, why `node_modules` and `target/` must never be in it, "
            "and the `.dockerignore` files that took one build from 900 MB of context to 2 MB."
        ),
    },
    {
        "slug": "docker-layer-caching",
        "title": "Docker – Layer Caching and Build Speed",
        "state": "new",
        "tags": ["docker", "dockerfile", "build", "performance"],
        "excerpt": (
            "One rule explains most fast Dockerfiles: copy the dependency manifest and install "
            "dependencies *before* copying your source. How the cache is keyed, why one changed "
            "line can invalidate every layer after it, the `pom.xml`-first and "
            "`package.json`-first patterns, and BuildKit cache mounts."
        ),
    },
    {
        "slug": "docker-multi-stage-builds",
        "title": "Docker – Multi-Stage Builds",
        "state": "new",
        "tags": ["docker", "dockerfile", "build"],
        "excerpt": (
            "Build in one image, ship from another. The pizza API compiles with Maven and a full "
            "JDK, then copies one jar into a JRE image — no Maven, no source, no build cache in "
            "the result. The frontends do the same with Node and nginx. Named stages, "
            "`COPY --from`, and stopping at a stage with `--target`."
        ),
    },
    {
        "slug": "docker-image-size-and-base-images",
        "title": "Docker – Choosing a Base Image and Keeping It Small",
        "state": "new",
        "tags": ["docker", "images", "performance"],
        "excerpt": (
            "`-slim`, `-alpine` and distroless, what each actually removes, and the musl-versus-glibc "
            "surprise that makes Alpine the wrong default for some runtimes. Measured sizes from "
            "the pizza images, what genuinely shrinks a build versus what only looks like it does, "
            "and why a smaller image matters most at pull time."
        ),
    },
    {
        "slug": "docker-non-root-and-image-security",
        "title": "Docker – Don't Run as Root",
        "state": "new",
        "tags": ["docker", "security", "images"],
        "excerpt": (
            "A container runs as root unless you say otherwise, and root in the container is root "
            "on the kernel it shares with you. Creating and switching to a non-root user, why "
            "port 80 then stops working, keeping secrets out of image layers, scanning with "
            "`docker scout`, and pinning a base image by digest."
        ),
    },
    # ------------------------------------------------------ running containers
    {
        "slug": "docker-ports-and-networking",
        "title": "Docker – Ports, Networks and Container DNS",
        "state": "new",
        "tags": ["docker", "networking", "containers"],
        "excerpt": (
            "`-p 3308:3306` has a host side and a container side and mixing them up is the single "
            "most common Docker mistake. Bridge networks, how containers resolve each other by "
            "service name, why `localhost` inside a container is not your laptop, and the "
            "`host.docker.internal` escape hatch."
        ),
    },
    {
        "slug": "docker-volumes-and-persistence",
        "title": "Docker – Volumes, Bind Mounts and Keeping Your Data",
        "state": "new",
        "tags": ["docker", "volumes", "containers"],
        "excerpt": (
            "A container's filesystem dies with it, so a database in a container needs somewhere "
            "else to write. Named volumes versus bind mounts, which to use for a database and "
            "which for live-reloading source, what `docker compose down -v` throws away, and why "
            "a bind-mounted database is measurably slower on a Mac."
        ),
    },
    {
        "slug": "docker-environment-and-configuration",
        "title": "Docker – Environment Variables, Build Args and Secrets",
        "state": "new",
        "tags": ["docker", "configuration", "security"],
        "excerpt": (
            "One image, many environments — the whole point of configuring from outside. `ENV` "
            "versus `ARG` and why a build arg is baked into the image forever, `--env-file`, "
            "Spring Boot's relaxed binding turning `SPRING_DATASOURCE_URL` into a property, "
            "frontend config that is baked at build time, and where secrets actually go."
        ),
    },
    {
        "slug": "docker-logs-and-debugging",
        "title": "Docker – Logs, Exec and Debugging a Container",
        "state": "new",
        "tags": ["docker", "debugging", "containers"],
        "excerpt": (
            "Your container exited, or it says `unhealthy`, or it will not connect to the "
            "database. `logs -f`, `exec -it sh` into a running container, `inspect` for the "
            "config it actually got, `stats` for resources, what the exit code means, and the "
            "healthcheck that reported unhealthy forever because the image had no `curl` in it."
        ),
    },
    # ---------------------------------------------------------------- compose
    {
        "slug": "docker-compose",
        "title": "Docker Compose – Running a Multi-Container Stack",
        "state": "new",
        "tags": ["docker", "docker-compose", "devops"],
        "excerpt": (
            "Once an app needs a database, `docker run` becomes a shell script nobody can read. "
            "The compose file, `up` and `down`, what a service is, the network and project name "
            "you get for free, `--build` versus `--force-recreate`, and why `docker-compose` with "
            "a hyphen is the old one."
        ),
    },
    {
        "slug": "docker-compose-depends-on-and-healthchecks",
        "title": "Docker Compose – depends_on, Healthchecks and Startup Order",
        "state": "new",
        "tags": ["docker", "docker-compose", "devops"],
        "excerpt": (
            "`depends_on` waits for the container to start, not for the service inside it to be "
            "ready — so the app races MySQL and dies on a connection refused that looks like a "
            "database bug. Writing a healthcheck, `condition: service_healthy`, `up --wait`, and "
            "why the app should still retry anyway."
        ),
    },
    {
        "slug": "docker-compose-profiles-and-overrides",
        "title": "Docker Compose – Profiles, Overrides and Multiple Files",
        "state": "new",
        "tags": ["docker", "docker-compose", "devops"],
        "excerpt": (
            "Not every service should start every time. Compose profiles put Elasticsearch, a "
            "message broker and a mail sink behind opt-in flags so the default `up` starts one "
            "container. Then `compose.override.yaml`, stacking `-f` files for dev and prod, and "
            "how `${VAR}` and `.env` interpolation works."
        ),
    },
    {
        "slug": "docker-compose-full-stack",
        "title": "Docker Compose – The Whole Application in One File",
        "state": "new",
        "tags": ["docker", "docker-compose", "devops"],
        "excerpt": (
            "Putting it together: MySQL, a Spring Boot API and an nginx-served single-page app, "
            "started with one command and torn down with another. The SPA rewrite rule every "
            "static host needs, reverse-proxying `/api` so the browser sees one origin and CORS "
            "stops mattering, and what this file is still not good enough for."
        ),
    },
    # --------------------------------------------------------------- shipping
    {
        "slug": "docker-registry-push-and-tag",
        "title": "Docker – Registries, Tagging and Pushing an Image",
        "state": "new",
        "tags": ["docker", "registry", "devops"],
        "excerpt": (
            "How an image gets from your laptop to a server. What a registry reference is really "
            "made of, `login` and `push`, Docker Hub versus ECR versus GHCR, a tagging scheme "
            "that survives a rollback, and why deploying `:latest` means you cannot answer the "
            "question \"what is actually running?\""
        ),
    },
    {
        "slug": "docker-multi-platform-builds",
        "title": "Docker – Multi-Platform Builds and exec format error",
        "state": "new",
        "tags": ["docker", "buildx", "devops"],
        "excerpt": (
            "You build on an Apple Silicon Mac, you push, the server says `exec format error`. "
            "Why that happens, what buildx and QEMU do about it, `--platform` for one target and "
            "a manifest list for both, what emulated builds cost in time, and the "
            "`--platform=$BUILDPLATFORM` trick that makes a cross build fast again."
        ),
    },
    {
        "slug": "docker-ci-github-actions",
        "title": "Docker – Building and Pushing from GitHub Actions",
        "state": "new",
        "tags": ["docker", "ci-cd", "github-actions", "devops"],
        "excerpt": (
            "A workflow that builds the image, tags it from the git ref, pushes it to a registry "
            "and does not leak a credential. `docker/build-push-action`, why a CI runner starts "
            "with an empty layer cache and what `cache-from`/`cache-to` do about it, and using "
            "GitHub's OIDC token instead of storing a long-lived key."
        ),
    },
    {
        "slug": "docker-production",
        "title": "Docker – Running Containers in Production",
        "state": "new",
        "tags": ["docker", "production", "devops"],
        "excerpt": (
            "What changes when it is not your laptop. Restart policies, memory and CPU limits and "
            "what the JVM does when you forget them, log drivers and why logs go to stdout, "
            "graceful shutdown and `SIGTERM`, read-only filesystems, and an honest account of "
            "where plain Docker stops and an orchestrator starts."
        ),
    },
    {
        "slug": "docker-interview-questions",
        "title": "Docker – Interview Questions",
        "state": "new",
        "tags": ["docker", "interview", "devops"],
        "excerpt": (
            "The questions Docker interviews actually ask, answered the way you would say them "
            "out loud. Container versus VM, image versus container, `CMD` versus `ENTRYPOINT`, "
            "`COPY` versus `ADD`, how layer caching works, where volumes fit, and the "
            "\"why is my image 1.2 GB\" question that separates people who have shipped one."
        ),
    },
]

# Slug -> filename, and the dates, are derived so a reorder is one edit.
POSTS = [
    {
        "slug": entry["slug"],
        "title": entry["title"],
        "file": f"{i + 1:02d}-{entry['slug']}.html",
        "date": _date(i),
        "tags": entry["tags"],
        "excerpt": entry["excerpt"],
        "state": entry["state"],
    }
    for i, entry in enumerate(_TRACK)
]

# Slugs that already exist on the live site and must never change.
FROZEN_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "rewrite"}
