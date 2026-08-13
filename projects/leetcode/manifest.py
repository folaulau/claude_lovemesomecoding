"""The LeetCode track: category metadata plus one entry per problem.

One post per problem, published in rounds of ten LeetCode numbers. The source
repo does not have every number, so a round only contains the problems that
exist in it — round 1 covers LeetCode 1-10 and holds seven posts.

`date` drives ordering everywhere on the site: archives and the sitemap sort
newest first, and `siblings()` in the frontend reverses the category index so
prev/next walks oldest-first. The dates therefore ascend with the LeetCode
number, which is what makes the ‹ prev / next › pager read 1 -> 2 -> 5 -> 7.
Identical timestamps would leave that ordering up to sort stability.

Posts land in the existing `fundamental-problem` category, so the URLs are
/fundamental-problem/leetcode-{n}-{title}. That category already holds 11
legacy posts from 2019; the LeetCode dates sit after them so the pager reaches
the track as one contiguous run.

Slugs are frozen the moment this is published. Changing one changes a URL.
"""

# The category already exists (11 posts, created in the WordPress migration).
# Seeding it only fills in the name and description, which the migration left
# empty. The slug is unchanged, so no URL moves.
CATEGORY = {
    "slug": "fundamental-problem",
    "name": "Fundamental Problems",
    "description": (
        "Coding interview problems worked end to end — the brute force, why it is not enough, "
        "the idea that fixes it, and clean Java and Python solutions with the edge cases that "
        "actually get you rejected."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, which already lists
# `fundamental-problem` under "Software Engineering" as "Fundamental Problems".
NAV_GROUP = "Software Engineering"

# Round 1 - LeetCode 1-10. Missing from the source repo: 3, 4, 6.
POSTS = [
    {
        "number": 1,
        "slug": "leetcode-1-two-sum",
        "title": "LeetCode 1 – Two Sum",
        "file": "001-two-sum.html",
        "date": "2026-08-12T09:00:00",
        "difficulty": "Easy",
        "tags": ["leetcode", "array", "hash-table"],
        "excerpt": (
            "The first problem on LeetCode, and still the most common phone-screen warm-up. It is "
            "not a test of whether you can find two numbers — it is a test of whether you reach "
            "for a hash map the moment you catch yourself writing a nested loop. One pass, look up "
            "before you insert, and the target = 2 × nums[i] case that lets an element pair with "
            "itself. Java and Python, plus the sorted two-pointer variant that 3Sum is built on."
        ),
    },
    {
        "number": 2,
        "slug": "leetcode-2-add-two-numbers",
        "title": "LeetCode 2 – Add Two Numbers",
        "file": "002-add-two-numbers.html",
        "date": "2026-08-12T10:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "linked-list", "math"],
        "excerpt": (
            "Long addition wearing a linked list costume. Reverse digit order is a gift, not an "
            "obstacle — it points the lists the same way the carry travels. The dummy head that "
            "removes the first-node special case, the carry in the loop condition that gives "
            "999 + 1 its fourth node, and why converting to an integer overflows on the real test "
            "cases. Java and Python, plus the forward-order follow-up."
        ),
    },
    {
        "number": 5,
        "slug": "leetcode-5-longest-palindromic-substring",
        "title": "LeetCode 5 – Longest Palindromic Substring",
        "file": "005-longest-palindromic-substring.html",
        "date": "2026-08-12T11:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "string", "dynamic-programming"],
        "excerpt": (
            "Counting substrings is O(n³) and the DP table costs O(n²) memory. Neither is the "
            "answer you want: a string has only 2n − 1 centres, and expanding around each one is "
            "O(n²) time in O(1) space and about fifteen lines. The even-length centre everyone "
            "forgets, the hi − lo − 1 off-by-one, the interval DP for when you need it, and where "
            "Manacher's linear algorithm fits."
        ),
    },
    {
        "number": 7,
        "slug": "leetcode-7-reverse-integer",
        "title": "LeetCode 7 – Reverse Integer",
        "file": "007-reverse-integer.html",
        "date": "2026-08-12T12:00:00",
        "difficulty": "Easy",
        "tags": ["leetcode", "math"],
        "excerpt": (
            "Tagged Easy, and it is not quite. Reversing the digits takes four lines; the problem "
            "is detecting 32-bit overflow without being allowed a 64-bit type. Two ways to check — "
            "undo the step, or rearrange the inequality — plus why Java's truncating % carries the "
            "sign for free, why Math.abs breaks on Integer.MIN_VALUE, and why Python needs the "
            "opposite care because its integers never overflow."
        ),
    },
    {
        "number": 8,
        "slug": "leetcode-8-string-to-integer-atoi",
        "title": "LeetCode 8 – String to Integer (atoi)",
        "file": "008-string-to-integer-atoi.html",
        "date": "2026-08-12T13:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "string", "math"],
        "excerpt": (
            "Almost no algorithm — a specification-reading exercise dressed as a coding problem, "
            "asked because sloppy engineers write parsers that eat production data. The rule that "
            "catches people is that atoi clamps to INT_MIN/INT_MAX where Reverse Integer returns "
            "zero. Four ordered steps, overflow detected before it happens, and the two Python "
            "traps: str.isdigit() and unbounded integers."
        ),
    },
    {
        "number": 9,
        "slug": "leetcode-9-palindrome-number",
        "title": "LeetCode 9 – Palindrome Number",
        "file": "009-palindrome-number.html",
        "date": "2026-08-12T14:00:00",
        "difficulty": "Easy",
        "tags": ["leetcode", "math"],
        "excerpt": (
            "Trivial with toString, which is why the follow-up — solve it without converting to a "
            "string — is the real question. Reversing only half the number cannot overflow, unlike "
            "reversing all of it. The loop that stops at the midpoint, the odd-digit case that "
            "needs reversed / 10, and the trailing-zero guard that makes 10 return false instead "
            "of true."
        ),
    },
    {
        "number": 10,
        "slug": "leetcode-10-regular-expression-matching",
        "title": "LeetCode 10 – Regular Expression Matching",
        "file": "010-regular-expression-matching.html",
        "date": "2026-08-12T15:00:00",
        "difficulty": "Hard",
        "tags": ["leetcode", "string", "dynamic-programming", "recursion"],
        "excerpt": (
            "The first genuinely Hard problem on the list, and the difficulty is not the code. "
            "'*' is not a character — it is a modifier on the character to its left, so x* is one "
            "indivisible unit with two branches you must both try. The recursion, why it is "
            "exponential, the memo that needs Boolean rather than boolean, the bottom-up table, "
            "and the first row that is not all false."
        ),
    },
    # Round 2 - LeetCode 11-20. Missing from the source repo: 11, 16, 17, 18.
    {
        "number": 12,
        "slug": "leetcode-12-integer-to-roman",
        "title": "LeetCode 12 – Integer to Roman",
        "file": "012-integer-to-roman.html",
        "date": "2026-08-12T16:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "math", "string", "greedy"],
        "excerpt": (
            "It looks like it needs a pile of special cases — four is IV, nine is IX, forty is XL. "
            "It does not. Put the six subtractive pairs into the symbol table as if they were "
            "symbols in their own right, and the problem collapses into a plain greedy loop with no "
            "branches at all. Why greedy is provably safe once the table is descending, and why "
            "String += is the wrong way to build the answer."
        ),
    },
    {
        "number": 13,
        "slug": "leetcode-13-roman-to-integer",
        "title": "LeetCode 13 – Roman to Integer",
        "file": "013-roman-to-integer.html",
        "date": "2026-08-12T17:00:00",
        "difficulty": "Easy",
        "tags": ["leetcode", "math", "string"],
        "excerpt": (
            "The inverse of Integer to Roman, and the trick that solved that one does not transfer. "
            "Going this way, all six subtractive pairs are handled by a single comparison: if a "
            "symbol is smaller than the one after it, subtract it. No table of pairs, no lookahead "
            "bookkeeping, and you never need to recognise CM as a unit. Java and Python, plus why "
            "not to rebuild a HashMap on every call."
        ),
    },
    {
        "number": 14,
        "slug": "leetcode-14-longest-common-prefix",
        "title": "LeetCode 14 – Longest Common Prefix",
        "file": "014-longest-common-prefix.html",
        "date": "2026-08-12T18:00:00",
        "difficulty": "Easy",
        "tags": ["leetcode", "string"],
        "excerpt": (
            "A five-minute problem whose only real content is the edge cases. Scanning vertically — "
            "one character position down the whole array before moving right — is shorter than the "
            "horizontal version, exits at the first mismatched column, and makes the bounds check "
            "handle both short strings and empty ones in a single line. Plus the sorting trick, and "
            "why it is the worse answer."
        ),
    },
    {
        "number": 15,
        "slug": "leetcode-15-3sum",
        "title": "LeetCode 15 – 3Sum",
        "file": "015-3sum.html",
        "date": "2026-08-12T19:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "two-pointers", "sorting"],
        "excerpt": (
            "The problem that teaches sort-then-two-pointers. The algorithm is the easy half; the "
            "half that decides whether you pass is de-duplication, and there are two separate places "
            "a duplicate gets in. Why sorting buys three things at once, why the anchor skip must "
            "compare backwards, and why no solution can beat O(n²) when the output itself can hold "
            "that many triplets."
        ),
    },
    {
        "number": 19,
        "slug": "leetcode-19-remove-nth-node-from-end-of-list",
        "title": "LeetCode 19 – Remove Nth Node From End of List",
        "file": "019-remove-nth-node-from-end-of-list.html",
        "date": "2026-08-12T20:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "linked-list", "two-pointers"],
        "excerpt": (
            "You cannot walk a singly linked list backwards, so the nth node from the end has to be "
            "found from the front. Two pointers held a fixed distance apart do it in one pass — but "
            "the gap is n + 1, not n, because unlinking a node needs the node before it. Why the "
            "dummy head is not optional here, and an honest note on what 'one pass' actually buys."
        ),
    },
    {
        "number": 20,
        "slug": "leetcode-20-valid-parentheses",
        "title": "LeetCode 20 – Valid Parentheses",
        "file": "020-valid-parentheses.html",
        "date": "2026-08-12T21:00:00",
        "difficulty": "Easy",
        "tags": ["leetcode", "string", "stack"],
        "excerpt": (
            "The canonical 'you should have reached for a stack' problem. Nesting means the thing "
            "you must close next is the thing you opened most recently. The trick that shortens the "
            "code: push the closer you expect, not the opener, so the check becomes one equality "
            "test. Three failure modes, three checks — and why ArrayDeque beats the legacy Stack."
        ),
    },
    # Round 3 - LeetCode 21-30. Missing from the source repo: 24, 25, 26, 27, 29, 30.
    {
        "number": 21,
        "slug": "leetcode-21-merge-two-sorted-lists",
        "title": "LeetCode 21 – Merge Two Sorted Lists",
        "file": "021-merge-two-sorted-lists.html",
        "date": "2026-08-13T09:00:00",
        "difficulty": "Easy",
        "tags": ["leetcode", "linked-list", "two-pointers"],
        "excerpt": (
            "The merge step of merge sort, isolated. Worth writing carefully rather than quickly, "
            "because Merge k Sorted Lists calls it and so does sorting a linked list. The part "
            "people over-engineer: splice the remaining list on in a single assignment instead of "
            "looping it out. Why the space is O(1), and why <= rather than < is the detail that "
            "shows you were thinking."
        ),
    },
    {
        "number": 22,
        "slug": "leetcode-22-generate-parentheses",
        "title": "LeetCode 22 – Generate Parentheses",
        "file": "022-generate-parentheses.html",
        "date": "2026-08-13T10:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "backtracking", "recursion", "string"],
        "excerpt": (
            "The problem that teaches constrained backtracking. The lazy solution builds all 4^n "
            "bracket strings and filters; the intended one never builds an invalid string, because "
            "two small rules make it impossible. Why close < open is sufficient — not just true — "
            "the undo step everyone forgets, and why the output being Catalan-sized bounds any "
            "possible solution."
        ),
    },
    {
        "number": 23,
        "slug": "leetcode-23-merge-k-sorted-lists",
        "title": "LeetCode 23 – Merge k Sorted Lists",
        "file": "023-merge-k-sorted-lists.html",
        "date": "2026-08-13T11:00:00",
        "difficulty": "Hard",
        "tags": ["leetcode", "linked-list", "divide-and-conquer", "heap"],
        "excerpt": (
            "Merging two lists is solved; the question is in what order you merge k of them, and "
            "the obvious order costs a factor of k. Where that extra factor comes from, why "
            "pairwise merging gets it to O(N log k), and an honest comparison of divide-and-conquer "
            "against a min-heap — same time, different space, and only one of them survives the "
            "streaming follow-up."
        ),
    },
    {
        "number": 28,
        "slug": "leetcode-28-implement-strstr",
        "title": "LeetCode 28 – Implement strStr()",
        "file": "028-implement-strstr.html",
        "date": "2026-08-13T12:00:00",
        "difficulty": "Easy",
        "tags": ["leetcode", "string", "two-pointers"],
        "excerpt": (
            "Reimplement indexOf. The honest answer to 'do I need to write KMP?' is almost always "
            "no — the interviewer wants a clean nested loop with correct bounds, and the bounds are "
            "the entire problem. Why i <= n - m is not a typo, how it handles a too-long needle for "
            "free, why not to allocate a substring per position, and how to raise KMP without "
            "walking into it."
        ),
    },
    # Round 4 - LeetCode 31-40. Missing from the source repo: 32, 35, 37, 38.
    {
        "number": 31,
        "slug": "leetcode-31-next-permutation",
        "title": "LeetCode 31 – Next Permutation",
        "file": "031-next-permutation.html",
        "date": "2026-08-14T09:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "two-pointers"],
        "excerpt": (
            "A problem you either see or you do not — no data structure, no recursion, just three "
            "passes in the right order. It starts from one observation: a descending suffix is "
            "already maximal, so the change has to reach further left than it goes. Finding the "
            "pivot, why scanning from the right finds the smallest larger value for free, and why "
            "reversing beats sorting the suffix."
        ),
    },
    {
        "number": 33,
        "slug": "leetcode-33-search-in-rotated-sorted-array",
        "title": "LeetCode 33 – Search in Rotated Sorted Array",
        "file": "033-search-in-rotated-sorted-array.html",
        "date": "2026-08-14T10:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "binary-search"],
        "excerpt": (
            "A rotated array is not sorted, so binary search should not work on it. It does, "
            "because however you cut it in half at least one half is properly sorted — and telling "
            "which is a single comparison. Why that comparison needs <= and not <, the "
            "overflow-safe midpoint, and why the duplicates variant provably degrades to O(n)."
        ),
    },
    {
        "number": 34,
        "slug": "leetcode-34-find-first-and-last-position",
        "title": "LeetCode 34 – Find First and Last Position of Element in Sorted Array",
        "file": "034-find-first-and-last-position.html",
        "date": "2026-08-14T11:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "binary-search"],
        "excerpt": (
            "Plain binary search finds an occurrence; this wants the first and the last, and "
            "expanding outwards from a hit is O(n) the moment the array is all one value. The clean "
            "answer is one primitive — lower bound — called twice, with target + 1 giving the "
            "second answer. Why the window is half-open, and why removing the equality test removes "
            "the bugs."
        ),
    },
    {
        "number": 36,
        "slug": "leetcode-36-valid-sudoku",
        "title": "LeetCode 36 – Valid Sudoku",
        "file": "036-valid-sudoku.html",
        "date": "2026-08-14T12:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "hash-table", "matrix"],
        "excerpt": (
            "No algorithm at all — a bookkeeping problem. Rows, columns and all nine boxes can be "
            "checked in a single pass, and the only interesting line is the formula mapping a cell "
            "to its box: (row / 3) * 3 + col / 3. Encoding three facts per cell into one set, why "
            "valid is not the same as solvable, and the bitmask version for when you are asked to "
            "drop the hashing."
        ),
    },
    {
        "number": 39,
        "slug": "leetcode-39-combination-sum",
        "title": "LeetCode 39 – Combination Sum",
        "file": "039-combination-sum.html",
        "date": "2026-08-14T13:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "backtracking", "array", "recursion"],
        "excerpt": (
            "The backtracking template with one twist: candidates may be reused without limit, "
            "which changes exactly one character in the recursive call. Why recursing from i rather "
            "than i + 1 is the whole difference, how the start index makes results unique "
            "structurally instead of by filtering, and why all-positive candidates are what "
            "guarantee the recursion terminates."
        ),
    },
    {
        "number": 40,
        "slug": "leetcode-40-combination-sum-ii",
        "title": "LeetCode 40 – Combination Sum II",
        "file": "040-combination-sum-ii.html",
        "date": "2026-08-14T14:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "backtracking", "array", "recursion"],
        "excerpt": (
            "Combination Sum with two changes: each element used once, and the input may contain "
            "duplicates. The first is one character; the second is one line — and `i > start` "
            "rather than `i > 0` is the most misunderstood condition in the backtracking family. "
            "Getting it wrong does not duplicate answers, it loses them, which is far harder to "
            "notice."
        ),
    },
    # Interview essentials - published out of round order, on request, because they
    # cover patterns rounds 1-4 leave out: one-pass scanning, grid BFS/DFS, bucket
    # sort, and the return-one-record-another tree recursion. `batch` groups them for
    # seed.py; their numbers put them far beyond the rounds published so far.
    {
        "number": 121,
        "batch": "interview-essentials",
        "slug": "leetcode-121-best-time-to-buy-and-sell-stock",
        "title": "LeetCode 121 – Best Time to Buy and Sell Stock",
        "file": "121-best-time-to-buy-and-sell-stock.html",
        "date": "2026-08-15T09:00:00",
        "difficulty": "Easy",
        "tags": ["leetcode", "array", "dynamic-programming"],
        "excerpt": (
            "Worth more than its Easy tag, because the reframing it teaches is the one behind "
            "Kadane's algorithm and most 1-D DP. The brute force asks which pair of days is best; "
            "the linear solution asks what the best buy was if I sell today — and that has a "
            "one-variable answer. Why a falling market returns 0, and why this is Maximum Subarray "
            "in disguise."
        ),
    },
    {
        "number": 200,
        "batch": "interview-essentials",
        "slug": "leetcode-200-number-of-islands",
        "title": "LeetCode 200 – Number of Islands",
        "file": "200-number-of-islands.html",
        "date": "2026-08-15T10:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "graph", "depth-first-search", "breadth-first-search", "matrix"],
        "excerpt": (
            "The most common graph question in interviews, and it does not look like one — "
            "recognising that a grid is a graph is most of what is being tested. Count starts and "
            "erase the island so it cannot be counted twice. Why you must mark visited before "
            "recursing, the input-mutation trade to say out loud, and when the recursion depth "
            "forces BFS."
        ),
    },
    {
        "number": 347,
        "batch": "interview-essentials",
        "slug": "leetcode-347-top-k-frequent-elements",
        "title": "LeetCode 347 – Top K Frequent Elements",
        "file": "347-top-k-frequent-elements.html",
        "date": "2026-08-15T11:00:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "hash-table", "heap", "sorting"],
        "excerpt": (
            "The statement contains its own hint: better than O(n log n). That sentence exists to "
            "rule out sorting and a max-heap of everything — and the defence that there are usually "
            "few unique values is not a complexity argument. A min-heap capped at k works; bucket "
            "sort gets it to O(n), because frequencies are small bounded integers you can index by."
        ),
    },
    {
        "number": 543,
        "batch": "interview-essentials",
        "slug": "leetcode-543-diameter-of-binary-tree",
        "title": "LeetCode 543 – Diameter of Binary Tree",
        "file": "543-diameter-of-binary-tree.html",
        "date": "2026-08-15T12:00:00",
        "difficulty": "Easy",
        "tags": ["leetcode", "tree", "depth-first-search", "recursion"],
        "excerpt": (
            "Tagged Easy, and the pattern carries most of the Hard tree problems: the recursion "
            "returns one quantity to its caller while updating a different one globally. Depth goes "
            "up, diameter gets recorded. Why left + right is already in edges despite counting "
            "nodes, and why nonlocal in Python is the difference between working and silently "
            "returning zero."
        ),
    },
]
