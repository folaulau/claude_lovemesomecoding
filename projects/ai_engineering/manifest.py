"""The AI-Assisted Engineering track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site (archives and the
sitemap sort newest first, prev/next walks the category oldest-first), so dates ascend with the
track and the capstone is the newest.

Dates are COMPUTED from START_DATE + STEP_DAYS so re-basing the whole track at publish time is one
edit. They are provisional until the track ships.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "ai-engineering",
    "name": "AI-Assisted Engineering",
    "description": (
        "How a working engineer uses an AI assistant across the whole job: analysis, requirements, "
        "planning, code, tests, debugging, AWS, UI walkthroughs, pull requests, review and "
        "customer support. One real feature on a real app, followed from ticket to pull request, with "
        "every prompt and every diff taken from an actual session. The theme throughout: the "
        "assistant writes, you read. Clicking Accept is not a review."
    ),
}

# The existing AI group in lovemesomecoding_frontend/src/lib/nav.ts already carries `claude`.
# This category is appended after it; seed.py cannot do that.
NAV_GROUP = "AI"

# Every example comes from real sessions against this app. Paths in SNIPPET_SOURCES are relative
# to it.
DEMO_APP = "lovemesomecoding_demo_project/pizza"
BACKEND = "pizza-springboot-backend"
WEB = "pizza-react-frontend"

# The feature the series follows from ticket to pull request. Chosen because the demo app's own CLAUDE.md
# lists it as the open item, so it is real work rather than a feature invented for a blog post.
FEATURE = "Pay with a saved card at checkout (backend + React frontend)"

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# ⚠️ The pipeline's wordCount counts PROSE AND CODE together, then
# readingMinutes = max(1, round(words / 220)). Budget the total, not the writing.
#
# 5-8 minutes, agreed 2026-10-04: one workflow per post.
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (5, 8)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 1,100
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 1,760

# This is a practice track, not a syntax track: the transcripts and diffs illustrate an argument
# about how to work. When code passes half the words, the post has turned into a session dump.
MIN_PROSE_SHARE = 0.55

# Every post must close with this section. It is the series' core theme (Folau, 2026-10-04):
# read the code and follow the plan, don't just click Accept.
REQUIRED_HEADING = "Before you accept"

# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------
START_DATE = datetime(2026, 9, 4, 9, 0, 0)
STEP_DAYS = 2


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=index * STEP_DAYS)).strftime("%Y-%m-%dT%H:%M:%S")


# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
_TRACK = [
    {
        "slug": "ai-engineering-mindset",
        "title": "AI-Assisted Engineering – You Own the Output",
        "tags": ["ai", "claude", "career"],
        "excerpt": (
            "What actually changes when an assistant writes most of the first draft, and what "
            "does not. Responsibility stays with the person who merges. The new split of the "
            "job, the habits that separate engineers who get faster from those who get sloppier, "
            "and the feature this series follows from ticket to pull request."
        ),
    },
    {
        "slug": "ai-engineering-read-before-you-accept",
        "title": "AI-Assisted Engineering – Read the Code, Follow the Plan",
        "tags": ["ai", "claude", "code-review"],
        "excerpt": (
            "Clicking Accept is not a review. The job moves from writing code to reading it: how "
            "to read an AI-written diff quickly, what to check first, how to hold the assistant "
            "to the agreed plan and spot drift, and a real case where accepting blind would have "
            "shipped a bug."
        ),
    },
    {
        "slug": "ai-engineering-setup",
        "title": "AI-Assisted Engineering – Setting Claude Up for a Real Codebase",
        "tags": ["ai", "claude", "tooling"],
        "excerpt": (
            "An assistant is only as good as the context it starts with. CLAUDE.md as standing "
            "instructions, a progress report as shared state, memory, permission modes, and MCP "
            "servers for GitHub, AWS and the browser. What to put in each, and what to leave out."
        ),
    },
    {
        "slug": "ai-engineering-codebase-analysis",
        "title": "AI-Assisted Engineering – Analysing an Unfamiliar Codebase",
        "tags": ["ai", "claude", "analysis"],
        "excerpt": (
            "Before changing anything, understand it. Using Claude read-only to trace checkout "
            "from the button to Stripe, size the change, and find the rules the code already "
            "enforces. Plus how to check that the explanation you got is true."
        ),
    },
    {
        "slug": "ai-engineering-requirements",
        "title": "AI-Assisted Engineering – Turning a Ticket into Requirements",
        "tags": ["ai", "claude", "requirements"],
        "excerpt": (
            "A one-line ticket is not a spec. Using the assistant to draw out clarifying "
            "questions, edge cases and conflicts with existing behaviour before any code exists, "
            "and why the answers have to come from a person, not the model."
        ),
    },
    {
        "slug": "ai-engineering-planning",
        "title": "AI-Assisted Engineering – Planning: The Plan Is the Contract",
        "tags": ["ai", "claude", "planning"],
        "excerpt": (
            "Plan mode, a written plan split into reviewable steps, and a progress report that "
            "survives the session. The plan is what you review every later diff against, so it "
            "is worth more of your attention than any single line of code."
        ),
    },
    {
        "slug": "ai-engineering-writing-code",
        "title": "AI-Assisted Engineering – Writing Code in Small, Readable Diffs",
        "tags": ["ai", "claude", "coding"],
        "excerpt": (
            "One plan step at a time, in the codebase's own style, verified before the next. How "
            "to keep diffs small enough to actually read, what drift looks like in practice, and "
            "how to push back when the assistant wanders off the plan."
        ),
    },
    {
        "slug": "ai-engineering-writing-tests",
        "title": "AI-Assisted Engineering – Writing Tests That Prove Something",
        "tags": ["ai", "claude", "testing"],
        "excerpt": (
            "An assistant will happily write tests that pass. The question is whether they fail "
            "when the code is wrong. Asking for behaviour rather than coverage, proving a test "
            "by breaking the code, and the test changes you should never accept."
        ),
    },
    {
        "slug": "ai-engineering-debugging",
        "title": "AI-Assisted Engineering – Debugging and Incidents",
        "tags": ["ai", "claude", "debugging"],
        "excerpt": (
            "Giving the assistant the evidence rather than your theory, letting it read logs and "
            "stack traces, and insisting on a root cause before a fix. A real failure met while "
            "building this feature, from first symptom to the line that caused it."
        ),
    },
    {
        "slug": "ai-engineering-aws-investigation",
        "title": "AI-Assisted Engineering – Investigating AWS",
        "tags": ["ai", "claude", "aws"],
        "excerpt": (
            "Letting an assistant drive the AWS CLI: a read-only profile, CloudWatch, cost "
            "questions and configuration drift. The guardrails that make it safe, and the real "
            "investigations behind this site's own infrastructure."
        ),
    },
    {
        "slug": "ai-engineering-ui-walkthrough",
        "title": "AI-Assisted Engineering – Feature Walkthroughs in the Browser",
        "tags": ["ai", "claude", "playwright"],
        "excerpt": (
            "Having the assistant drive the running app to prove a feature works: a Playwright "
            "script, screenshots at desktop and phone width, and the checks it could not do. Why a "
            "green test suite is not the same as a working screen."
        ),
    },
    {
        "slug": "ai-engineering-pull-requests",
        "title": "AI-Assisted Engineering – Commits and Pull Requests",
        "tags": ["ai", "claude", "git"],
        "excerpt": (
            "Commit messages that explain why, a PR description a reviewer can act on, and the "
            "check that matters most: does the description match the diff? Drafting with the "
            "assistant, and what to cut before it goes to a human."
        ),
    },
    {
        "slug": "ai-engineering-pr-review",
        "title": "AI-Assisted Engineering – Responding to Code Review",
        "tags": ["ai", "claude", "code-review"],
        "excerpt": (
            "Working through review comments with the assistant: deciding which are right, "
            "answering the ones that are not, and making each fix a small, separate change. Plus "
            "using AI as a first reviewer before a human sees the PR."
        ),
    },
    {
        "slug": "ai-engineering-customer-support",
        "title": "AI-Assisted Engineering – Customer Support Tickets",
        "tags": ["ai", "claude", "support"],
        "excerpt": (
            "From a customer's confused message to a reproduced bug and a reply a human would "
            "send. Triage, reproduction against the real app, what never goes into a prompt, and "
            "why the reply needs your judgement more than your typing."
        ),
    },
    {
        "slug": "ai-engineering-guardrails",
        "title": "AI-Assisted Engineering – Guardrails and When Not to Use It",
        "tags": ["ai", "claude", "security"],
        "excerpt": (
            "Secrets, destructive commands, production access, confident wrong answers and "
            "invented APIs. The settings and habits that contain each risk, and the tasks where "
            "doing it yourself is still the faster, safer choice."
        ),
    },
    {
        "slug": "ai-engineering-capstone",
        "title": "AI-Assisted Engineering – One Feature, Ticket to Pull Request",
        "tags": ["ai", "claude", "workflow"],
        "excerpt": (
            "The whole series in one pass: pay with a saved card at checkout, from the ticket to "
            "the pull request. Every step, how long it took, where the assistant helped most, and "
            "every point where reading the diff mattered."
        ),
    },
]

POSTS = [
    {
        "slug": entry["slug"],
        "title": entry["title"],
        "file": f"{i + 1:02d}-{entry['slug']}.html",
        "date": _date(i),
        "tags": entry["tags"],
        "excerpt": entry["excerpt"],
    }
    for i, entry in enumerate(_TRACK)
]

# Files each post may quote, relative to DEMO_APP. Filled in as each post is written.
SNIPPET_SOURCES: dict[str, list[str]] = {}

# Nothing is published under /ai-engineering yet, so no slug is an indexed URL.
FROZEN_SLUGS: set[str] = set()

NEW_SLUGS = {e["slug"] for e in _TRACK}
