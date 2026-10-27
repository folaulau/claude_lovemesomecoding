"""The Behavioral Questions track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site: archives and the
sitemap sort newest first, and prev/next walks the category oldest-first, so dates ascend with the
track and the last lesson is the newest.

Dates are COMPUTED from START_DATE + STEP_DAYS, the same mechanism as the System Design track.
Every date must stay in the past: a post dated ahead of today pins itself to the top of the site
and ships a sitemap <lastmod> that postdates the crawl.

⚠️ Every slug here is NEW, and post slugs are global across categories. seed.py refuses to write a
`new` slug that already exists in the target tree unless --republish says the track is ours.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "behavioral-questions",
    "name": "Behavioral Questions",
    "description": (
        "The non-technical half of a software engineering interview. What behavioral questions "
        "actually score, the STAR structure, building a story bank, and worked answers to the "
        "questions every company asks: the project you are proudest of, a failure, a conflict, "
        "ambiguity, ownership, learning fast, leadership and feedback, and why this company. "
        "The sample answers come from real projects, not invented ones."
    ),
}

# The nav entry lives in lovemesomecoding_frontend/src/lib/nav.ts, group "Software Engineering",
# placed directly after `system-design` because the two are read together before an interview.
NAV_GROUP = "Software Engineering"

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# Shorter than System Design's 15-20 minutes on purpose. A behavioral answer is two minutes out
# loud; a post about one question family that runs twenty minutes has stopped teaching the answer
# and started padding it. README: "keep posts to the point".
WORDS_PER_MINUTE = 220
#
# The floor was 7 minutes in the first draft and seven of the ten posts landed at 6. Each one had
# said what it needed to say, so the floor moved rather than the posts being padded to meet a
# number chosen before they were written.
TARGET_MINUTES = (6, 12)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 1,320
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 2,640

# Every post needs at least one plaintext block: the answer skeleton, the worksheet, or the
# question list. They are what a reader copies into their own notes.
MIN_PLAINTEXT_BLOCKS = 1

# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
_TRACK = [
    {
        "slug": "behavioral-interview-introduction",
        "title": "Behavioral Interviews – What They Score and How to Answer",
        "tags": ["interview", "behavioral", "career"],
        "excerpt": (
            "Why the non-technical round decides more offers than candidates expect, what an "
            "interviewer is actually writing down while you talk, the STAR structure and the two "
            "ways people misuse it, how long an answer should be, and the questions that come up "
            "at almost every company, grouped into the families the rest of this track works "
            "through."
        ),
    },
    {
        "slug": "behavioral-story-bank",
        "title": "Building Your Story Bank",
        "tags": ["interview", "behavioral", "career"],
        "excerpt": (
            "You do not need forty answers, you need eight good stories and a map from questions "
            "to stories. How to mine your own work for them, what makes a story strong enough to "
            "reuse, the worksheet to write each one down, and a real story bank built from the "
            "projects behind this site."
        ),
    },
    {
        "slug": "behavioral-proudest-project",
        "title": "Tell Me About a Project You Are Proud Of",
        "tags": ["interview", "behavioral", "career"],
        "excerpt": (
            "The question that opens more behavioral rounds than any other, and the one most "
            "people answer with a feature list. What the interviewer is listening for, how to "
            "pick the project, and a full worked answer from Sidecar Health: letting members "
            "compare doctors before booking, and moving search from MySQL to Elasticsearch."
        ),
    },
    {
        "slug": "behavioral-failure-and-mistakes",
        "title": "Tell Me About a Time You Failed",
        "tags": ["interview", "behavioral", "career"],
        "excerpt": (
            "The question candidates fear most and the easiest one to answer well. Picking a real "
            "failure rather than a disguised boast, owning it without self-punishment, and the "
            "part most answers skip: what you changed so it cannot happen again. Two worked "
            "answers from bugs that actually shipped."
        ),
    },
    {
        "slug": "behavioral-conflict-and-disagreement",
        "title": "Conflict, Disagreement and Disagreeing With Your Manager",
        "tags": ["interview", "behavioral", "career"],
        "excerpt": (
            "Tell me about a conflict with a teammate; tell me about a time you disagreed with "
            "your manager. What separates a mature answer from a story about being right, "
            "disagree-and-commit, arguing from evidence instead of opinion, and the skeleton to "
            "build your own answer, with a real example of changing a rule rather than bending "
            "the work."
        ),
    },
    {
        "slug": "behavioral-ambiguity-and-tradeoffs",
        "title": "Ambiguity, Trade-offs and Tight Deadlines",
        "tags": ["interview", "behavioral", "career"],
        "excerpt": (
            "Requirements that contradict each other, a deadline that does not fit the scope, a "
            "decision with no right answer. How to show judgement under uncertainty: naming the "
            "tension, choosing on purpose, cutting scope deliberately, and keeping a way back. "
            "Worked from real decisions with real costs."
        ),
    },
    {
        "slug": "behavioral-ownership-and-initiative",
        "title": "Ownership – Going Beyond the Ticket",
        "tags": ["interview", "behavioral", "career"],
        "excerpt": (
            "Tell me about a time you went beyond your role, fixed something nobody asked you to, "
            "or noticed a problem before anyone else. What ownership sounds like in an answer, "
            "where it tips into overstepping, and four real examples, from stepping in to get "
            "Sidecar Health's MVP out on time to a forgotten public API that was still switched on."
        ),
    },
    {
        "slug": "behavioral-learning-fast",
        "title": "Learning Something New Under Pressure",
        "tags": ["interview", "behavioral", "career"],
        "excerpt": (
            "Tell me about a time you had to learn a technology quickly. Interviewers are scoring "
            "how you learn, not what you already know. The worked answer: rehearsing a production "
            "MySQL 8.0 to 8.4 upgrade on a throwaway copy first, for about two dollars, so the "
            "real one would be the second time rather than the first."
        ),
    },
    {
        "slug": "behavioral-leadership-and-feedback",
        "title": "Leadership, Mentoring and Feedback",
        "tags": ["interview", "behavioral", "career"],
        "excerpt": (
            "Leadership questions get asked of every level, not just managers. Leading without "
            "authority, mentoring, giving hard feedback, receiving it, and the answer skeletons "
            "for each, with a real example of teaching at scale and honest guidance on what to "
            "say when you have never managed anyone."
        ),
    },
    {
        "slug": "behavioral-why-this-company",
        "title": "Why Us, Why Leave, and the Questions You Should Ask",
        "tags": ["interview", "behavioral", "career"],
        "excerpt": (
            "The motivation questions: why this company, why are you leaving, where do you see "
            "yourself. How to answer each without a script or a complaint, the salary question, "
            "and the questions you should ask them, which are scored too. Ends with a one-page "
            "checklist for the night before."
        ),
    },
]

# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------
# One lesson a day, ending the day before the track was written (2026-10-25). The stories inside
# the posts are dated August to October 2026, so a 2026 date is the only honest one here, unlike
# the System Design track, whose posts carry no dated events.
START_DATE = datetime(2026, 10, 15, 9, 0, 0)
STEP_DAYS = 1
DATE_RANGE = (datetime(2026, 10, 1), datetime(2026, 10, 24, 23, 59, 59))


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=index * STEP_DAYS)).strftime("%Y-%m-%dT%H:%M:%S")


POSTS = [
    {
        "slug": entry["slug"],
        "title": entry["title"],
        "file": f"{i + 1:02d}-{entry['slug']}.html",
        "date": _date(i),
        "tags": entry["tags"],
        "excerpt": entry["excerpt"],
        "state": "new",
    }
    for i, entry in enumerate(_TRACK)
]

FROZEN_SLUGS: set[str] = set()
NEW_SLUGS = {p["slug"] for p in POSTS}

assert len(POSTS) == 10, f"the track is 10 posts, got {len(POSTS)}"
_dates = [datetime.strptime(p["date"], "%Y-%m-%dT%H:%M:%S") for p in POSTS]
_out = [p["slug"] for p, d in zip(POSTS, _dates) if not DATE_RANGE[0] <= d <= DATE_RANGE[1]]
assert not _out, f"post dates must stay inside DATE_RANGE: {_out}"
