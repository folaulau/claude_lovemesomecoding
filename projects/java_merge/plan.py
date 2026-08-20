"""The merge plan: what moves, what dies, and what redirects where.

`/java-8` (36 posts) and `/java-advanced` (7) fold into `/java` (29), which then
holds 64. Every decision here changes a live indexed URL, so nothing in this file
is cosmetic.

READ THIS FIRST — the frontend's build guard does NOT cover this operation.
`verify-build.mjs` checks post URLs against the CURRENT index, not a frozen list
of what Google has indexed. Move a post to another category and the old URL simply
stops existing, the index no longer mentions it, and the build passes. Every
redirect below therefore has to be right by construction; nothing will catch a
missing one. `check_redirects.py` is the compensating control.
"""

# Slugs are global and a post's URL is /{category}/{slug}, so moving a post to
# `java` changes its URL. These 43 all move; none collides with an existing
# `/java` slug (checked, not assumed).
MOVE_TO_JAVA = {
    # --- from /java-8: the original Java 8 feature posts (2019) -------------
    "java-8-lambda-expression", "java-8-functional-interfaces",
    "java-8-method-references", "java-8-streams", "java-8-collectors-class",
    "java-8-optional", "java-8-foreach", "java-8-date-time-api",
    "java-8-stringjoiner", "java-8-array-parallel-sort",
    "java-8-completablefuture",
    "java-8-interface-default-methods-and-static-methods",
    # --- from /java-8: Java 11 ---------------------------------------------
    "java-11-string-methods", "java-11-api-improvements", "java-11-httpclient",
    "java-11-single-file-execution", "java-11-migration-guide",
    # --- from /java-8: Java 17 ---------------------------------------------
    "java-17-records", "java-17-sealed-classes", "java-17-switch-expressions",
    "java-17-text-blocks", "java-17-pattern-matching-instanceof",
    "java-17-other-improvements", "java-17-migration-guide",
    # --- from /java-8: Java 21 ---------------------------------------------
    "java-21-virtual-threads", "java-21-pattern-matching-switch",
    "java-21-record-patterns", "java-21-sequenced-collections",
    "java-21-unnamed-variables", "java-21-other-improvements",
    "java-21-migration-guide",
    # --- from /java-8: Java 25 ---------------------------------------------
    "java-25-stream-gatherers", "java-25-flexible-constructors",
    "java-25-simplified-java", "java-25-other-improvements",
    "java-25-migration-guide",
    # --- from /java-advanced ------------------------------------------------
    "java-advanced-generics", "java-advanced-multithreading",
    "java-advanced-regex", "java-advanced-database", "java-advanced-log4j",
    "java-advanced-encryption-and-decryption", "java-advanced-eclipse-hot-keys",
}

# Folau's call: where an incoming post covers the SAME GROUND as one written in
# projects/java_tutorial, the incoming one wins and the newer post is deleted and
# redirected to it. Anything worth keeping from the deleted post is merged into
# the survivor before it goes — that is what "consolidate" means here.
#
# These 8 are true duplicates: same topic, same scope.
RETIRE_IN_FAVOUR_OF = {
    "java-lambda-expression":  "java-8-lambda-expression",
    "java-stream":             "java-8-streams",
    "java-optional":           "java-8-optional",
    "java-method-reference":   "java-8-method-references",
    "java-completablefuture":  "java-8-completablefuture",
    "java-date":               "java-8-date-time-api",
    "java-record":             "java-17-records",
    "java-sealed-class":       "java-17-sealed-classes",
}

# NOT retired, though an earlier pass listed them as duplicates. Each incoming
# post is narrower than the one it appeared to duplicate — a version-specific
# feature rather than the fundamentals — so both earn a place and the pair is
# cross-linked instead. Retiring the left column would leave a Java tutorial with
# no post on what a String is, what a List is, how a loop works, what an
# interface is, or how `if` works.
KEEP_BOTH = {
    "java-string":                 "java-11-string-methods",
    "java-collections":            "java-21-sequenced-collections",
    "java-for-loop":               "java-8-foreach",
    "java-interface":              "java-8-interface-default-methods-and-static-methods",
    "java-conditional-statements": "java-17-switch-expressions",
    "java-lambda-expression-fn":   "java-8-functional-interfaces",   # pairs with the lambda post
}

# The two categories being retired. delete_category refuses while any post still
# points at it, so the moves must all land first.
RETIRE_CATEGORIES = ["java-8", "java-advanced"]

# Every URL that stops resolving, and where it goes. Built rather than typed —
# see build_redirects().
def build_redirects(old_category_of: dict) -> dict:
    """old_category_of maps slug -> the category it lives in TODAY."""
    r = {}
    for slug in sorted(MOVE_TO_JAVA):
        old = old_category_of.get(slug)
        if old:
            r[f"/{old}/{slug}"] = f"/java/{slug}"
    for dead, survivor in sorted(RETIRE_IN_FAVOUR_OF.items()):
        r[f"/java/{dead}"] = f"/java/{survivor}"
    for cat in RETIRE_CATEGORIES:
        r[f"/{cat}"] = "/java"
    return r


TARGET_CATEGORY = "java"
WORD_TARGET = (900, 1800)   # same band as the rest of /java
