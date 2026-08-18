"""The React track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and lesson 25 is the newest.

17 of these slugs were published in 2019 and are indexed. They are being
rewritten in place, NOT replaced: changing one of those slugs changes a live URL.
The 8 marked `new` below did not exist before.

Because the old posts carry 2019 dates and `upsert_post` never overwrites an
existing date, seeding this track needs `seed.py --force-dates` for the reading
order to come out right. See progress_report.md.
"""

CATEGORY = {
    "slug": "react",
    "name": "React",
    "description": (
        "React from the ground up — components, JSX, props, state, hooks, context, "
        "routing and performance, every example lifted from a real ordering app."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts.
NAV_GROUP = "JavaScript"

# The app every code sample is taken from, so a reader can go and see the whole
# thing in context rather than a fragment invented for the tutorial.
DEMO_APP = "lovemesomecoding_demo_project/pizza/pizza-react-frontend"

POSTS = [
    # ---------------------------------------------------------- getting started
    {
        "slug": "react-set-up",
        "title": "React – Set Up a Project with Vite",
        "file": "01-react-set-up.html",
        "date": "2026-06-06T09:00:00",
        "tags": ["react", "vite", "typescript"],
        "excerpt": (
            "Create React App is retired; Vite is what the React docs point you at now. One "
            "command to scaffold a TypeScript project, what each generated file is actually for, "
            "why the entry point is a .tsx file and not index.html, and the four scripts you will "
            "run every day. Ends with the project layout the rest of this track uses."
        ),
    },
    {
        "slug": "react-es6",
        "title": "React – The JavaScript You Need First",
        "file": "02-react-es6.html",
        "date": "2026-06-09T09:00:00",
        "tags": ["react", "javascript", "es6"],
        "excerpt": (
            "Most of what looks like React syntax is plain modern JavaScript. Destructuring, the "
            "spread operator, arrow functions, template strings, optional chaining, modules and "
            "array methods — each one shown twice: the language feature on its own, then the line "
            "of real component code that depends on it."
        ),
    },
    {
        "slug": "react-render-html",
        "title": "React – Rendering to the DOM",
        "file": "03-react-render-html.html",
        "date": "2026-06-12T09:00:00",
        "tags": ["react", "dom"],
        "excerpt": (
            "How a React app actually starts: one <div id=\"root\"> in the HTML, createRoot in the "
            "entry file, and everything else built by React. Why ReactDOM.render is gone, what "
            "StrictMode's double render is really telling you, and where providers belong in the "
            "tree."
        ),
    },
    # ------------------------------------------------------- describing the UI
    {
        "slug": "react-components",
        "title": "React – Your First Component",
        "file": "04-react-components.html",
        "date": "2026-06-15T09:00:00",
        "tags": ["react", "components"],
        "excerpt": (
            "A component is a function that returns markup — that is the whole idea. Naming and "
            "capitalisation rules React enforces, importing and exporting, why components must be "
            "declared at the top level, what \"keeping a component pure\" buys you, and an honest "
            "note on the class components you will still meet in older code."
        ),
    },
    {
        "slug": "react-jsx",
        "title": "React – JSX",
        "file": "05-react-jsx.html",
        "date": "2026-06-18T09:00:00",
        "tags": ["react", "jsx"],
        "excerpt": (
            "JSX is a syntax for calling functions, not a template language, and the differences "
            "show. One root element and what fragments are for, className over class, curly "
            "braces for values and double braces for objects, why {} renders nothing for false "
            "but prints a bare 0, and how to write comments inside markup."
        ),
    },
    {
        "slug": "react-props",
        "title": "React – Props",
        "file": "06-react-props.html",
        "date": "2026-06-21T09:00:00",
        "tags": ["react", "props", "typescript"],
        "excerpt": (
            "Props are the arguments a component takes. Destructuring them in the signature, "
            "typing them with TypeScript, default values, the children prop, and passing "
            "functions down so a child can talk back to its parent. Plus the rule that explains "
            "half of all React bugs: props are read-only."
        ),
    },
    {
        "slug": "react-conditional-rendering",
        "title": "React – Conditional Rendering",
        "file": "07-react-conditional-rendering.html",
        "date": "2026-06-24T09:00:00",
        "tags": ["react", "jsx"],
        "excerpt": (
            "Four ways to render something only sometimes — if before the return, the ternary, "
            "&&, and returning null — and when each one reads best. Includes the && trap that "
            "renders a literal 0 on the page, and the early-return pattern that guards a whole "
            "route."
        ),
    },
    {
        "slug": "react-keys",
        "title": "React – Rendering Lists and Keys",
        "file": "08-react-keys.html",
        "date": "2026-06-27T09:00:00",
        "tags": ["react", "lists", "keys"],
        "excerpt": (
            "Rendering an array with map, and the key prop React nags you about. What a key is "
            "actually for, why the array index is a bug waiting for the list to reorder, what to "
            "use when the items have no id, and why keys must be unique among siblings but not "
            "globally."
        ),
    },
    # ------------------------------------------------------------ interactivity
    {
        "slug": "react-events",
        "title": "React – Handling Events",
        "file": "09-react-events.html",
        "date": "2026-06-30T09:00:00",
        "tags": ["react", "events"],
        "excerpt": (
            "onClick takes a function, not a call — the single most common beginner mistake, and "
            "why the arrow function fixes it. Passing arguments to a handler, typing the event in "
            "TypeScript, preventDefault on form submits, and how event propagation differs from "
            "the DOM you already know."
        ),
    },
    {
        "slug": "react-state",
        "title": "React – State with useState",
        "file": "10-react-state.html",
        "date": "2026-07-03T09:00:00",
        "tags": ["react", "state", "hooks"],
        "excerpt": (
            "State is what a component remembers between renders. Why a plain variable will not "
            "do, the array destructuring useState returns, the rules that govern where hooks may "
            "be called, one state variable versus several, and the moment to stop and lift state "
            "up to a shared parent instead."
        ),
    },
    {
        "slug": "react-update-state",
        "title": "React – Updating State Correctly",
        "file": "11-react-update-state.html",
        "date": "2026-07-06T09:00:00",
        "tags": ["react", "state", "hooks"],
        "excerpt": (
            "Setting state does not change the variable you are holding — it schedules a render "
            "with a new one. State as a snapshot, why two increments in a row only count once, "
            "the updater function that fixes it, and updating objects and arrays without mutating "
            "them so React can still tell that something changed."
        ),
    },
    {
        "slug": "react-forms",
        "title": "React – Forms and Controlled Inputs",
        "file": "12-react-forms.html",
        "date": "2026-07-09T09:00:00",
        "tags": ["react", "forms"],
        "excerpt": (
            "A controlled input is one whose value comes from state, which is what makes "
            "validation, formatting and disabled submit buttons possible at all. value plus "
            "onChange, one handler for many fields, checkboxes and selects and radios, submitting "
            "without reloading the page, and useId for labels that actually work."
        ),
    },
    # ---------------------------------------------------------- managing state
    {
        "slug": "react-context",
        "title": "React – Passing Data Deeply with Context",
        "file": "13-react-context.html",
        "date": "2026-07-12T09:00:00",
        "tags": ["react", "context", "hooks"],
        "excerpt": (
            "Prop drilling is passing a value through five components that do not use it. Context "
            "is the way out: createContext, a provider component that owns the state, useContext "
            "to read it anywhere below. What belongs in context and what does not, why every "
            "consumer re-renders when the value changes, and how to keep that from hurting."
        ),
    },
    {
        "slug": "react-usereducer",
        "title": "React – useReducer",
        "file": "14-react-usereducer.html",
        "date": "2026-07-15T09:00:00",
        "tags": ["react", "state", "hooks"],
        "excerpt": (
            "When a component grows six setState calls that must agree with each other, a reducer "
            "collapses them into one function you can read top to bottom. Actions, the reducer's "
            "purity requirement, typing actions as a discriminated union, and the useReducer + "
            "context pairing that gives you Redux's shape without Redux."
        ),
    },
    {
        "slug": "react-custom-hooks",
        "title": "React – Custom Hooks",
        "file": "15-react-custom-hooks.html",
        "date": "2026-07-18T09:00:00",
        "tags": ["react", "hooks"],
        "excerpt": (
            "A custom hook is a function whose name starts with use and that calls other hooks. "
            "That is the entire specification. Extracting stateful logic so two components can "
            "share it, why hooks share logic and never state, the one-line hook that turns a "
            "context into a typed API and throws when used outside its provider."
        ),
    },
    {
        "slug": "react-redux",
        "title": "React – Redux, and Whether You Need It",
        "file": "16-react-redux.html",
        "date": "2026-07-21T09:00:00",
        "tags": ["react", "redux", "state"],
        "excerpt": (
            "Redux Toolkit as it is actually written today — configureStore, createSlice, "
            "useSelector, useDispatch — and an honest comparison against the context plus reducer "
            "you already know. What Redux gives you that React does not, what it costs, and the "
            "question to ask before adding it."
        ),
    },
    # --------------------------------------------------------- escape hatches
    {
        "slug": "react-lifecycle",
        "title": "React – The Component Lifecycle with useEffect",
        "file": "17-react-lifecycle.html",
        "date": "2026-07-24T09:00:00",
        "tags": ["react", "hooks", "useeffect"],
        "excerpt": (
            "The old three phases map onto one hook. What the dependency array really means, the "
            "cleanup function and the requests it cancels, why StrictMode runs your effect twice "
            "on purpose, the infinite loop everyone writes once — and the larger point that most "
            "effects should not exist at all."
        ),
    },
    {
        "slug": "react-useref",
        "title": "React – Refs",
        "file": "18-react-useref.html",
        "date": "2026-07-27T09:00:00",
        "tags": ["react", "hooks", "dom"],
        "excerpt": (
            "A ref is a value a component remembers that does not trigger a render when it "
            "changes. Reaching a real DOM node to focus, measure or scroll it, holding a timer id "
            "between renders, why reading or writing a ref during render is a bug, and how ref "
            "differs from state in one table."
        ),
    },
    {
        "slug": "react-error-boundary",
        "title": "React – Error Boundaries",
        "file": "19-react-error-boundary.html",
        "date": "2026-07-30T09:00:00",
        "tags": ["react", "errors"],
        "excerpt": (
            "One thrown error in one component blanks the entire page — React unmounts the whole "
            "tree rather than show something broken. An error boundary is the only thing that "
            "stops it, it is still the one thing you need a class component for, and it does not "
            "catch event handlers or async code. Here is what to do about all three."
        ),
    },
    # ------------------------------------------------------ going to production
    {
        "slug": "react-route",
        "title": "React – Routing with React Router",
        "file": "20-react-route.html",
        "date": "2026-08-02T09:00:00",
        "tags": ["react", "react-router"],
        "excerpt": (
            "React has no router, so everyone uses this one. BrowserRouter, Routes and Route, "
            "Link instead of an anchor tag, URL params and query strings, programmatic navigation "
            "with useNavigate, layout routes with Outlet, and a guarded route that bounces "
            "signed-out users to the login page and back again."
        ),
    },
    {
        "slug": "react-usememo-usecallback",
        "title": "React – useMemo, useCallback and memo",
        "file": "21-react-usememo-usecallback.html",
        "date": "2026-08-05T09:00:00",
        "tags": ["react", "hooks", "performance"],
        "excerpt": (
            "Three tools that all do the same thing — skip work when nothing relevant changed — "
            "and are all easy to use wrongly. What each one actually caches, why memo does "
            "nothing until the props are stable, the cases that genuinely need them, and why the "
            "React Compiler may make all of this optional."
        ),
    },
    {
        "slug": "react-lazy-suspense",
        "title": "React – Code Splitting with lazy and Suspense",
        "file": "22-react-lazy-suspense.html",
        "date": "2026-08-08T09:00:00",
        "tags": ["react", "performance", "suspense"],
        "excerpt": (
            "Everything imported at the top of your app ships to every visitor, including the "
            "admin screens 99% of them will never open. lazy turns an import into its own bundle "
            "fetched on demand, Suspense says what to show while it is in flight, and the route "
            "boundary is where to draw the line. With before-and-after bundle numbers."
        ),
    },
    {
        "slug": "react-css",
        "title": "React – Styling",
        "file": "23-react-css.html",
        "date": "2026-08-11T09:00:00",
        "tags": ["react", "css"],
        "excerpt": (
            "className not class, the inline style object and its camelCased keys, conditional "
            "and combined class names, CSS Modules for scoping, importing a stylesheet in the "
            "entry file and why import order decides which rule wins. Plus where CSS-in-JS and "
            "Tailwind fit, and the case for CSS custom properties."
        ),
    },
    {
        "slug": "react-with-bootstrap",
        "title": "React – Bootstrap",
        "file": "24-react-with-bootstrap.html",
        "date": "2026-08-14T09:00:00",
        "tags": ["react", "bootstrap", "css"],
        "excerpt": (
            "Two ways to use Bootstrap in React: the plain stylesheet with className, or "
            "react-bootstrap's real components. Why you should not load Bootstrap's JavaScript "
            "bundle alongside React, controlled modals and offcanvas drawers, and overriding the "
            "theme with custom properties instead of fighting specificity."
        ),
    },
    {
        "slug": "react-sass",
        "title": "React – Sass",
        "file": "25-react-sass.html",
        "date": "2026-08-17T09:00:00",
        "tags": ["react", "sass", "css"],
        "excerpt": (
            "Sass in a Vite project is one dependency and a file rename — no config. Nesting, "
            "variables, partials and mixins in a component stylesheet, .module.scss to get "
            "scoping and Sass at once, and the one thing Sass still does that plain CSS cannot: "
            "recompile Bootstrap itself with your own colours."
        ),
    },
]
