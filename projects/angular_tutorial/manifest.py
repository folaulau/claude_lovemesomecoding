"""The Angular track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and the last lesson is the
newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because
this track is authored before it is published: when the publish date is finally
known, move START_DATE and every lesson re-bases in order. The React manifest
hard-codes its dates; that only worked because it shipped the day it was written.

One slug here is not new. `angular-component` was published 2019-07-31 with an
EMPTY body (wordCount 0) and its URL is indexed. It is being rewritten in place,
NOT replaced — changing that slug changes a live URL. Because it carries a 2019
date and `upsert_post` never overwrites an existing date, seeding needs
`seed.py --force-dates` for the reading order to come out right.
See progress_report.md.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "angular",
    "name": "Angular",
    "description": (
        "Angular from the ground up — components, templates, signals, dependency injection, "
        "routing, forms and shipping to production, every example lifted from a real "
        "ordering app."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts.
NAV_GROUP = "JavaScript"

# The app every code sample is taken from, so a reader can go and see the whole
# thing in context rather than a fragment invented for the tutorial. Built and
# ready as of 2026-08-20: standalone, zoneless, OnPush everywhere, signals for
# customer state and NgRx for admin.
DEMO_APP = "lovemesomecoding_demo_project/pizza/pizza-angular-frontend"

# The versions the whole track is written against. Lesson 1 prints this table,
# and every other lesson assumes it. When these move, that table is the first edit.
#
# These are READ OFF THE DEMO APP, not chosen. Angular 22 is out, but the app is
# on 21 and the snippets have to match the code they were copied from — a lesson
# claiming 22 over a 21 snippet is the kind of thing that ages badly and is
# impossible to spot later.
VERSIONS = {
    "angular": "21.2",
    "@angular/cli": "21.2",
    "typescript": "5.9",
    "rxjs": "7.8",
    "@ngrx/store": "21.1",
    "bootstrap": "5.3 (with Sass overrides)",
    "node": "22 (20.19 is Angular 21's minimum)",
}

# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later,
# so the pager reads lesson 1 -> lesson 29. Re-base the whole track by editing
# these two values; nothing else needs to change.
START_DATE = datetime(2026, 5, 28, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    """The publish timestamp for the index-th lesson, 0-based."""
    return (START_DATE + timedelta(days=STEP_DAYS * index)).strftime("%Y-%m-%dT%H:%M:%S")


# Authored in reading order. `state` is documentation, not data: "rewrite" means
# the slug already exists on the live site and must not change.
_TRACK = [
    # ------------------------------------------------------------- start here
    {
        "slug": "angular-get-started",
        "title": "Angular – Get Started",
        "state": "new",
        "tags": ["angular", "typescript"],
        "excerpt": (
            "Start here. What Angular is and what problem it solves, how it differs from React "
            "and when a team picks it, the exact versions this track is written against — "
            "Angular 21, TypeScript 5.9, Bootstrap 5 — one command to create a project and see it "
            "running, the demo application every example is taken from, and the full lesson "
            "index in reading order."
        ),
    },
    {
        "slug": "angular-set-up",
        "title": "Angular – Set Up a Project with the Angular CLI",
        "state": "new",
        "tags": ["angular", "angular-cli", "typescript"],
        "excerpt": (
            "One command scaffolds the project: what `ng new` actually generates, what each file "
            "is for, how `angular.json` and the three tsconfigs fit together, where "
            "`bootstrapApplication` and `app.config.ts` replaced the old root NgModule, and the "
            "handful of `ng` commands you will run every day."
        ),
    },
    {
        "slug": "angular-typescript",
        "title": "Angular – The TypeScript You Need First",
        "state": "new",
        "tags": ["angular", "typescript"],
        "excerpt": (
            "Angular is TypeScript-first, and the parts of the language it leans on hardest are "
            "the ones tutorials skip. Interfaces for API shapes, generics, decorators and why "
            "Angular uses them, strict null checks, and the `readonly` and `as const` habits that "
            "keep a component's inputs honest."
        ),
    },
    # ------------------------------------------------- components & templates
    {
        "slug": "angular-component",
        "title": "Angular – Your First Component",
        "state": "rewrite",  # published 2019-07-31, body is empty, URL is indexed
        "tags": ["angular", "components", "typescript"],
        "excerpt": (
            "A component is a class with a template and a selector, and in modern Angular that is "
            "all it is — no NgModule required. The `@Component` decorator field by field, "
            "standalone components and why they are now the default, inline versus separate "
            "template files, and how a component ends up on the page."
        ),
    },
    {
        "slug": "angular-templates",
        "title": "Angular – Templates and Data Binding",
        "state": "new",
        "tags": ["angular", "templates", "data-binding"],
        "excerpt": (
            "Four kinds of binding and when each applies: `{{ }}` interpolation, `[property]` "
            "binding, `(event)` binding and `[(ngModel)]` two-way binding. Why `[src]` is not the "
            "same as `src=`, what a template reference variable is for, and the expression rules "
            "Angular enforces inside a template."
        ),
    },
    {
        "slug": "angular-events",
        "title": "Angular – Handling Events",
        "state": "new",
        "tags": ["angular", "events", "templates"],
        "excerpt": (
            "`(click)`, `(submit)`, `(input)` and the rest: binding a DOM event to a method, what "
            "`$event` holds, keyboard event filters like `(keydown.enter)`, and why putting real "
            "logic in the template instead of the class is the mistake that costs you later."
        ),
    },
    {
        "slug": "angular-control-flow",
        "title": "Angular – Control Flow with @if, @for and @switch",
        "state": "new",
        "tags": ["angular", "templates", "control-flow"],
        "excerpt": (
            "Angular 17 replaced `*ngIf`, `*ngFor` and `*ngSwitch` with built-in block syntax, and "
            "the old directives are on the way out. `@if` / `@else`, `@for` with its mandatory "
            "`track` and its `@empty` block, `@switch`, and what to do when you meet the "
            "structural-directive form in an older codebase."
        ),
    },
    {
        "slug": "angular-inputs-outputs",
        "title": "Angular – Inputs, Outputs and Two-Way Binding",
        "state": "new",
        "tags": ["angular", "components", "signals"],
        "excerpt": (
            "How data goes down and events come back up. The signal-based `input()`, `output()` "
            "and `model()` functions that replaced the `@Input` and `@Output` decorators, required "
            "versus optional inputs, input transforms, and how `model()` gives you `[(value)]` on "
            "your own component for free."
        ),
    },
    {
        "slug": "angular-content-projection",
        "title": "Angular – Content Projection and ng-template",
        "state": "new",
        "tags": ["angular", "components", "templates"],
        "excerpt": (
            "Writing a component that wraps content it does not own. Single-slot and multi-slot "
            "`<ng-content>`, selecting what lands where, `<ng-template>` and `<ng-container>` and "
            "the difference between them, and `ngTemplateOutlet` for the cases where a slot is not "
            "flexible enough."
        ),
    },
    {
        "slug": "angular-directives",
        "title": "Angular – Directives",
        "state": "new",
        "tags": ["angular", "directives"],
        "excerpt": (
            "A directive is a component without a template — behaviour you attach to an element "
            "you did not write. The built-in attribute directives, writing your own with "
            "`@Directive`, `host` bindings and listeners, and `hostDirectives` for composing "
            "behaviour without inheritance."
        ),
    },
    {
        "slug": "angular-pipes",
        "title": "Angular – Pipes",
        "state": "new",
        "tags": ["angular", "pipes", "templates"],
        "excerpt": (
            "Formatting values in the template without cluttering the class. `DatePipe`, "
            "`CurrencyPipe`, `DecimalPipe` and `AsyncPipe`, chaining pipes and passing arguments, "
            "writing a custom pipe, and the pure-versus-impure distinction that decides whether "
            "your pipe runs once or on every change detection pass."
        ),
    },
    {
        "slug": "angular-styles",
        "title": "Angular – Component Styles, Sass and Bootstrap",
        "state": "new",
        "tags": ["angular", "css", "sass", "bootstrap"],
        "excerpt": (
            "Angular scopes a component's styles to that component by default, which changes how "
            "you think about CSS. View encapsulation and the attribute selectors it emits, "
            "`:host` and `:host-context`, `[class]` and `[style]` bindings, and layering Sass "
            "overrides on Bootstrap in `angular.json` so they win without a single `!important`."
        ),
    },
    # ------------------------------------------------------------- reactivity
    {
        "slug": "angular-signals",
        "title": "Angular – Signals",
        "state": "new",
        "tags": ["angular", "signals", "reactivity"],
        "excerpt": (
            "Signals are how Angular tracks state now, and they are the biggest change to the "
            "framework in years. What a signal is, `signal()`, `set()` and `update()`, why reading "
            "one inside a template subscribes that template to it, and how signals let Angular "
            "skip change detection for everything that did not change."
        ),
    },
    {
        "slug": "angular-computed-effect",
        "title": "Angular – computed, effect and linkedSignal",
        "state": "new",
        "tags": ["angular", "signals", "reactivity"],
        "excerpt": (
            "Derived state without the bugs. `computed()` for values that follow from other "
            "signals, `effect()` for the side effects that must run when they change — and the "
            "rule about not writing to signals inside one — plus `linkedSignal()` for state that "
            "is derived but still needs to be locally overridable."
        ),
    },
    {
        "slug": "angular-lifecycle",
        "title": "Angular – The Component Lifecycle",
        "state": "new",
        "tags": ["angular", "components", "lifecycle"],
        "excerpt": (
            "The hooks Angular calls on your component and the order they fire in: `ngOnInit`, "
            "`ngOnChanges`, `ngAfterViewInit`, `ngOnDestroy` and the rest. Which ones you still "
            "need now that signals and `effect()` cover most of what they used to, and how "
            "`DestroyRef` and `takeUntilDestroyed` replace the manual unsubscribe boilerplate."
        ),
    },
    # -------------------------------------------------- services, DI and data
    {
        "slug": "angular-services-dependency-injection",
        "title": "Angular – Services and Dependency Injection",
        "state": "new",
        "tags": ["angular", "dependency-injection", "services"],
        "excerpt": (
            "Dependency injection is the part of Angular that most repays understanding properly. "
            "Writing a service, `@Injectable({ providedIn: 'root' })` and what tree-shakeable "
            "providers buy you, the `inject()` function versus constructor injection, injection "
            "tokens for values that are not classes, and how the injector hierarchy decides which "
            "instance you get."
        ),
    },
    {
        "slug": "angular-http-client",
        "title": "Angular – Talking to an API with HttpClient",
        "state": "new",
        "tags": ["angular", "http", "api"],
        "excerpt": (
            "Every real app is mostly API calls. `provideHttpClient()`, typed `get` / `post` / "
            "`put` / `delete`, query params and headers, unwrapping observables with the "
            "`async` pipe or `toSignal`, the newer `httpResource()` for read-only data, and where "
            "to put error handling so it is not repeated in every component."
        ),
    },
    {
        "slug": "angular-interceptors",
        "title": "Angular – HTTP Interceptors",
        "state": "new",
        "tags": ["angular", "http", "security"],
        "excerpt": (
            "One place to attach the auth token, and one place to catch a 401. Functional "
            "interceptors and how they chain, adding an `Authorization` header, translating server "
            "errors into something the UI can show, a loading indicator driven by in-flight "
            "requests, and why interceptor order is not an implementation detail."
        ),
    },
    {
        "slug": "angular-rxjs",
        "title": "Angular – RxJS, and How Much of It You Still Need",
        "state": "new",
        "tags": ["angular", "rxjs", "reactivity"],
        "excerpt": (
            "Signals took over state, but observables still own events over time. The operators "
            "that actually earn their place — `map`, `filter`, `switchMap`, `debounceTime`, "
            "`catchError`, `shareReplay` — why `switchMap` is the right answer for a search box, "
            "and how `toSignal` and `toObservable` let the two models meet."
        ),
    },
    # ---------------------------------------------------------------- routing
    {
        "slug": "angular-router",
        "title": "Angular – Routing",
        "state": "new",
        "tags": ["angular", "router"],
        "excerpt": (
            "Turning URLs into components. `provideRouter()` and the route table, "
            "`<router-outlet>`, `routerLink` and `routerLinkActive`, route parameters and query "
            "parameters as signals via `withComponentInputBinding`, child routes and layouts, and "
            "the wildcard route that catches everything else."
        ),
    },
    {
        "slug": "angular-route-guards",
        "title": "Angular – Guards, Resolvers and Lazy Loading",
        "state": "new",
        "tags": ["angular", "router", "security", "performance"],
        "excerpt": (
            "Keeping signed-out visitors out of the admin area, and keeping the admin area out of "
            "everyone else's download. Functional `CanActivate` and `CanMatch` guards, "
            "`CanDeactivate` for unsaved forms, resolvers for data a route cannot render without, "
            "and `loadComponent` / `loadChildren` lazy loading with proof in the build output."
        ),
    },
    # ------------------------------------------------------------------ forms
    {
        "slug": "angular-forms",
        "title": "Angular – Template-Driven Forms",
        "state": "new",
        "tags": ["angular", "forms"],
        "excerpt": (
            "The quicker of Angular's two form systems, and the right choice for a short form. "
            "`FormsModule` and `ngModel`, `ngForm` and template reference variables, the built-in "
            "validators, showing an error only once the field has been touched, and the point at "
            "which you should stop and reach for reactive forms instead."
        ),
    },
    {
        "slug": "angular-reactive-forms",
        "title": "Angular – Reactive Forms and Validation",
        "state": "new",
        "tags": ["angular", "forms", "validation"],
        "excerpt": (
            "Forms defined in the class, where they can be typed and tested. `FormControl`, "
            "`FormGroup` and `FormArray`, typed forms and why `nonNullable` matters, sync and "
            "async validators, cross-field validation, and mapping the server's field errors back "
            "onto the right controls after a failed submit."
        ),
    },
    # ------------------------------------------------------------- shipping it
    {
        "slug": "angular-state-management",
        "title": "Angular – State Management",
        "state": "new",
        "tags": ["angular", "signals", "ngrx", "state-management"],
        "excerpt": (
            "Most Angular apps do not need a state library, and the ones that do should be able to "
            "say why. The demo app splits it deliberately: signal-based services injected from the "
            "root for the customer screens, NgRx for the admin section. What each is good at, what "
            "`createFeature` buys you, and why registering the store on a lazy route keeps it out "
            "of everyone else's download."
        ),
    },
    {
        "slug": "angular-testing",
        "title": "Angular – Testing",
        "state": "new",
        "tags": ["angular", "testing"],
        "excerpt": (
            "Testing a component, a service and an HTTP call. `TestBed` and `ComponentFixture`, "
            "what `fixture.detectChanges()` is for, testing a service in isolation with fakes, "
            "`HttpTestingController` for asserting on requests, and where end-to-end tests take "
            "over from unit tests."
        ),
    },
    {
        "slug": "angular-performance",
        "title": "Angular – Change Detection, OnPush, Zoneless and @defer",
        "state": "new",
        "tags": ["angular", "performance", "change-detection"],
        "excerpt": (
            "Why an Angular app gets slow and what to do about it. How change detection actually "
            "works, what `OnPush` changes, the zoneless mode signals made possible, `@defer` for "
            "loading a heavy component only when it is needed, and measuring with Angular DevTools "
            "instead of guessing."
        ),
    },
    {
        "slug": "angular-ssr",
        "title": "Angular – Server-Side Rendering and Hydration",
        "state": "new",
        "tags": ["angular", "ssr", "performance"],
        "excerpt": (
            "What `ng add @angular/ssr` sets up and whether you want it. Server-side rendering "
            "versus prerendering versus a plain SPA, full and incremental hydration, the browser "
            "APIs that are not there on the server and how to guard against them, and the SEO and "
            "first-paint case for turning it on."
        ),
    },
    {
        "slug": "angular-build-deploy",
        "title": "Angular – Build and Deploy to Production",
        "state": "new",
        "tags": ["angular", "deployment", "angular-cli"],
        "excerpt": (
            "The last mile. What `ng build` produces and how to read the bundle report, budgets "
            "that fail the build when a bundle grows, environment configuration without leaking "
            "secrets, the SPA rewrite rule every static host needs, cache headers for hashed "
            "assets, and a GitHub Actions workflow that ships it."
        ),
    },
    {
        "slug": "angular-interview-questions",
        "title": "Angular – Interview Questions",
        "state": "new",
        "tags": ["angular", "interview"],
        "excerpt": (
            "The questions Angular interviews actually ask, answered the way you would say them "
            "out loud. Signals versus observables, why standalone replaced NgModules, how "
            "dependency injection resolves, what `OnPush` really does, template-driven versus "
            "reactive forms, and the change-detection question that separates people who have "
            "shipped Angular from people who have read about it."
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
