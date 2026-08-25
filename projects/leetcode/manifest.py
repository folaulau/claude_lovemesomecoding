"""The LeetCode track: category metadata plus one entry per problem.

One post per problem, published in rounds of ten LeetCode numbers. The source
repo does not have every number, so a round only contains the problems that
exist in it — round 1 covers LeetCode 1-10 and holds seven posts.

`date` drives ordering everywhere on the site: archives and the sitemap sort
newest first, and `siblings()` in the frontend reverses the category index so
prev/next walks oldest-first. The dates therefore ascend with the LeetCode
number, which is what makes the ‹ prev / next › pager read 1 -> 2 -> 5 -> 7.
Identical timestamps would leave that ordering up to sort stability.

The LeetCode dates are randomly spread from 2022 onward (generated once with a
fixed seed per round, then sorted) rather than clustered on the day they were
written. The track originally targeted 2022-2024; that window was exhausted at
round 15, so later rounds run past 2024. See README.md.
They are random but strictly ascending with the LeetCode number, because the
ordering above depends on it. seed.py --redate is what applies a change here to
posts that already exist -- upsert_post never re-applies `date` on its own.

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

# The algorithm taxonomy every post is filed under, alphabetical. This is the
# standard HackerRank algorithm-domain list; `algorithm` on each entry must be
# one of these exactly, which check_content.py enforces.
#
# seed.py emits the slugified value as the FIRST tag on the post, ahead of the
# free-form ones. Nothing on the public site renders tags today -- they are
# stored and editable in /admin only -- so this is metadata waiting for a browse
# UI, not something a reader sees.
ALGORITHMS = (
    "Bit Manipulation",
    "Constructive Algorithms",
    "Dynamic Programming",
    "Game Theory",
    "Graph Theory",
    "Greedy",
    "Implementation",
    "Recursion",
    "Searching",
    "Sorting",
    "Strings",
    "Warmup",
)

# Round 1 - LeetCode 1-10. Missing from the source repo: 3, 4, 6.
POSTS = [
    {
        "number": 1,
        "slug": "leetcode-1-two-sum",
        "algorithm": "Searching",
        "title": "LeetCode 1 – Two Sum",
        "file": "001-two-sum.html",
        "date": "2022-03-04T16:30:56",
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
        "algorithm": "Implementation",
        "title": "LeetCode 2 – Add Two Numbers",
        "file": "002-add-two-numbers.html",
        "date": "2022-03-12T15:27:05",
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
        "algorithm": "Strings",
        "title": "LeetCode 5 – Longest Palindromic Substring",
        "file": "005-longest-palindromic-substring.html",
        "date": "2022-03-24T12:13:12",
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
        "algorithm": "Implementation",
        "title": "LeetCode 7 – Reverse Integer",
        "file": "007-reverse-integer.html",
        "date": "2022-04-14T21:10:58",
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
        "algorithm": "Strings",
        "title": "LeetCode 8 – String to Integer (atoi)",
        "file": "008-string-to-integer-atoi.html",
        "date": "2022-08-30T23:48:30",
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
        "algorithm": "Implementation",
        "title": "LeetCode 9 – Palindrome Number",
        "file": "009-palindrome-number.html",
        "date": "2022-09-28T03:08:31",
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
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 10 – Regular Expression Matching",
        "file": "010-regular-expression-matching.html",
        "date": "2022-10-03T18:55:13",
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
        "algorithm": "Greedy",
        "title": "LeetCode 12 – Integer to Roman",
        "file": "012-integer-to-roman.html",
        "date": "2022-10-10T14:53:30",
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
        "algorithm": "Strings",
        "title": "LeetCode 13 – Roman to Integer",
        "file": "013-roman-to-integer.html",
        "date": "2022-11-11T13:41:51",
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
        "algorithm": "Strings",
        "title": "LeetCode 14 – Longest Common Prefix",
        "file": "014-longest-common-prefix.html",
        "date": "2023-01-09T12:21:34",
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
        "algorithm": "Sorting",
        "title": "LeetCode 15 – 3Sum",
        "file": "015-3sum.html",
        "date": "2023-02-17T16:48:52",
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
        "algorithm": "Implementation",
        "title": "LeetCode 19 – Remove Nth Node From End of List",
        "file": "019-remove-nth-node-from-end-of-list.html",
        "date": "2023-04-05T16:33:26",
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
        "algorithm": "Strings",
        "title": "LeetCode 20 – Valid Parentheses",
        "file": "020-valid-parentheses.html",
        "date": "2023-04-07T15:31:46",
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
        "algorithm": "Sorting",
        "title": "LeetCode 21 – Merge Two Sorted Lists",
        "file": "021-merge-two-sorted-lists.html",
        "date": "2023-04-21T23:53:58",
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
        "algorithm": "Recursion",
        "title": "LeetCode 22 – Generate Parentheses",
        "file": "022-generate-parentheses.html",
        "date": "2023-07-10T16:57:34",
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
        "algorithm": "Sorting",
        "title": "LeetCode 23 – Merge k Sorted Lists",
        "file": "023-merge-k-sorted-lists.html",
        "date": "2023-10-13T13:35:32",
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
        "algorithm": "Strings",
        "title": "LeetCode 28 – Implement strStr()",
        "file": "028-implement-strstr.html",
        "date": "2023-12-23T09:00:22",
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
        "algorithm": "Implementation",
        "title": "LeetCode 31 – Next Permutation",
        "file": "031-next-permutation.html",
        "date": "2023-12-28T03:29:48",
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
        "algorithm": "Searching",
        "title": "LeetCode 33 – Search in Rotated Sorted Array",
        "file": "033-search-in-rotated-sorted-array.html",
        "date": "2024-01-19T01:31:30",
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
        "algorithm": "Searching",
        "title": "LeetCode 34 – Find First and Last Position of Element in Sorted Array",
        "file": "034-find-first-and-last-position.html",
        "date": "2024-06-25T02:07:34",
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
        "algorithm": "Implementation",
        "title": "LeetCode 36 – Valid Sudoku",
        "file": "036-valid-sudoku.html",
        "date": "2024-07-03T08:06:22",
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
        "algorithm": "Recursion",
        "title": "LeetCode 39 – Combination Sum",
        "file": "039-combination-sum.html",
        "date": "2024-07-18T11:21:02",
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
        "algorithm": "Recursion",
        "title": "LeetCode 40 – Combination Sum II",
        "file": "040-combination-sum-ii.html",
        "date": "2024-08-09T01:50:35",
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
    # Round 5 - LeetCode 41-50. Missing from the source repo: 44, 45, 48, 50.
    # Dated inside the gap between LeetCode 40 and 121 so the manifest's number
    # and date ordering stay consistent.
    {
        "number": 41,
        "slug": "leetcode-41-first-missing-positive",
        "algorithm": "Sorting",
        "title": "LeetCode 41 \u2013 First Missing Positive",
        "file": "041-first-missing-positive.html",
        "date": "2024-08-11T16:47:48",
        "difficulty": "Hard",
        "tags": ["leetcode", "array", "hash-table"],
        "excerpt": (
            "Hard because of its constraints, not its question — a hash set solves it instantly, and "
            "O(1) space forbids one. Everything follows from a single observation: with n elements "
            "the answer is always in [1, n + 1], so every other value is noise. Cyclic sort uses the "
            "array as its own hash table, and the nested loop really is O(n)."
        ),
    },
    {
        "number": 42,
        "slug": "leetcode-42-trapping-rain-water",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 42 \u2013 Trapping Rain Water",
        "file": "042-trapping-rain-water.html",
        "date": "2024-08-18T06:40:16",
        "difficulty": "Hard",
        "tags": ["leetcode", "array", "two-pointers", "stack"],
        "excerpt": (
            "One of the most-asked Hard problems, and it defeats people because they try to find the "
            "puddles. Do not. Ask how deep the water is above one column and the answer is one line: "
            "min(maxLeft, maxRight) − height. Why two pointers can decide with half the information, "
            "and the line ordering that silently returns a number slightly too small."
        ),
    },
    {
        "number": 43,
        "slug": "leetcode-43-multiply-strings",
        "algorithm": "Strings",
        "title": "LeetCode 43 \u2013 Multiply Strings",
        "file": "043-multiply-strings.html",
        "date": "2024-08-18T11:21:32",
        "difficulty": "Medium",
        "tags": ["leetcode", "string", "math", "simulation"],
        "excerpt": (
            "Long multiplication as you learned it at school and then forgot. It hinges on one piece "
            "of index arithmetic — the product of digits i and j lands at i + j + 1, carrying into "
            "i + j — which is worth deriving rather than memorising. Why the result needs exactly "
            "m + n slots, and why an intermediate slot going above 9 is harmless."
        ),
    },
    {
        "number": 46,
        "slug": "leetcode-46-permutations",
        "algorithm": "Recursion",
        "title": "LeetCode 46 \u2013 Permutations",
        "file": "046-permutations.html",
        "date": "2024-08-23T17:28:38",
        "difficulty": "Medium",
        "tags": ["leetcode", "backtracking", "recursion", "array"],
        "excerpt": (
            "The reference implementation of backtracking, and its value is the contrast with the "
            "combination problems. There a start index stops the same set appearing in different "
            "orders; here the different orders are the answer, so start disappears and used[] takes "
            "its job. Undo both pieces of state, or you get one permutation and then nothing."
        ),
    },
    {
        "number": 47,
        "slug": "leetcode-47-permutations-ii",
        "algorithm": "Recursion",
        "title": "LeetCode 47 \u2013 Permutations II",
        "file": "047-permutations-ii.html",
        "date": "2024-09-01T07:22:28",
        "difficulty": "Medium",
        "tags": ["leetcode", "backtracking", "recursion", "array"],
        "excerpt": (
            "Permutations with duplicates, and the extra line is a different extra line from the one "
            "Combination Sum II uses — which catches people who think they already learned this "
            "trick. With no start index, used[] is the only signal of depth, so the rule becomes "
            "!used[i-1]. All three de-duplication rules compared side by side."
        ),
    },
    {
        "number": 49,
        "slug": "leetcode-49-group-anagrams",
        "algorithm": "Strings",
        "title": "LeetCode 49 \u2013 Group Anagrams",
        "file": "049-group-anagrams.html",
        "date": "2024-09-14T17:07:10",
        "difficulty": "Medium",
        "tags": ["leetcode", "hash-table", "string", "sorting"],
        "excerpt": (
            "A hashing problem wearing a string problem's clothes. Find something identical for "
            "anagrams and different for everything else, then group by it. Sorting each word works; "
            "counting letters is better. And the separator everyone forgets — without it a word with "
            "1 a and 11 b's collides with one that has 11 a's and 1 b."
        ),
    },
    {
        "number": 51,
        "slug": "leetcode-51-n-queens",
        "algorithm": "Recursion",
        "title": "LeetCode 51 \u2013 N-Queens",
        "file": "051-n-queens.html",
        "date": "2024-09-14T22:22:32",
        "difficulty": "Hard",
        "tags": ["leetcode", "backtracking", "recursion", "array"],
        "excerpt": (
            "The problem people point at when they say backtracking, and it collapses once you see "
            "that every row holds exactly one queen \u2014 the board stops being a grid and becomes an "
            "int[n]. Both diagonals in one test, why no row check is needed, and why this version "
            "can skip the undo when the next one cannot."
        ),
    },
    {
        "number": 52,
        "slug": "leetcode-52-n-queens-ii",
        "algorithm": "Recursion",
        "title": "LeetCode 52 \u2013 N-Queens II",
        "file": "052-n-queens-ii.html",
        "date": "2024-09-15T07:29:27",
        "difficulty": "Hard",
        "tags": ["leetcode", "backtracking", "recursion"],
        "excerpt": (
            "The same search asked for a count instead of the boards, and calling problem 51 and "
            "returning size() is exactly the answer it is designed to catch. Marking row - col and "
            "row + col makes the legality test O(1), the undo becomes mandatory, and the bitmask "
            "version is there if you are asked to go faster."
        ),
    },
    {
        "number": 53,
        "slug": "leetcode-53-maximum-subarray",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 53 \u2013 Maximum Subarray",
        "file": "053-maximum-subarray.html",
        "date": "2024-09-16T15:34:44",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "dynamic-programming", "divide-and-conquer"],
        "excerpt": (
            "The smallest problem that is genuinely dynamic programming, and almost everyone gets "
            "it nearly right then fails on an all-negative array. Deriving Kadane rather than "
            "recalling it, why best = 0 is the near-miss, keeping best and endingHere distinct, and "
            "the follow-up that asks where the subarray actually starts."
        ),
    },
    {
        "number": 55,
        "slug": "leetcode-55-jump-game",
        "algorithm": "Greedy",
        "title": "LeetCode 55 \u2013 Jump Game",
        "file": "055-jump-game.html",
        "date": "2024-09-17T03:17:21",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "greedy", "dynamic-programming"],
        "excerpt": (
            "A greedy problem that spends most of its time disguised as dynamic programming. "
            "nums[i] is a maximum, not an exact jump, which makes the reachable set a prefix with "
            "no holes \u2014 and that is the justification the greedy needs. One variable replaces the "
            "whole DP table, plus the backward version for when you are asked to flip it."
        ),
    },
    {
        "number": 56,
        "slug": "leetcode-56-merge-intervals",
        "algorithm": "Sorting",
        "title": "LeetCode 56 \u2013 Merge Intervals",
        "file": "056-merge-intervals.html",
        "date": "2024-09-17T11:09:41",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "sorting", "intervals"],
        "excerpt": (
            "The gateway to every interval problem, carried almost entirely by one decision: sort "
            "by start. Why that reduces overlap to a single comparison against the last output, why "
            "the merged end must be a max, why a[0] - b[0] as a comparator is a production bug, and "
            "when to sort by end instead."
        ),
    },
    {
        "number": 57,
        "slug": "leetcode-57-insert-interval",
        "algorithm": "Implementation",
        "title": "LeetCode 57 \u2013 Insert Interval",
        "file": "057-insert-interval.html",
        "date": "2024-09-17T11:36:25",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "intervals", "two-pointers"],
        "excerpt": (
            "The list arrives sorted and non-overlapping, and re-sorting it throws away the "
            "precondition the problem went out of its way to give you. Three sequential loops "
            "sharing one index and no if statements, why absorbing needs a min as well as a max, "
            "and why the binary-search refinement does not change the complexity."
        ),
    },
    {
        "number": 58,
        "slug": "leetcode-58-length-of-last-word",
        "algorithm": "Strings",
        "title": "LeetCode 58 \u2013 Length of Last Word",
        "file": "058-length-of-last-word.html",
        "date": "2024-09-17T15:43:20",
        "difficulty": "Easy",
        "tags": ["leetcode", "string", "two-pointers"],
        "excerpt": (
            "A warm-up, and on the list because it is one \u2014 easy problems are where interviewers "
            "watch how you write rather than whether you can. split()[-1] is correct and allocates "
            "the whole string to read one word. Scan backwards instead: O(1) space, and end - i "
            "needs no plus one."
        ),
    },
    {
        "number": 62,
        "slug": "leetcode-62-unique-paths",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 62 \u2013 Unique Paths",
        "file": "062-unique-paths.html",
        "date": "2024-09-18T03:52:29",
        "difficulty": "Medium",
        "tags": ["leetcode", "dynamic-programming", "math", "combinatorics"],
        "excerpt": (
            "The cleanest introduction to grid DP there is, and worth doing carefully because the "
            "next two problems are this one with a single detail changed. Deriving the recurrence "
            "from what was the last move, compressing the table to one row and why the sweep "
            "direction makes that work, and why the combinatorial closed form is a footnote."
        ),
    },
    {
        "number": 63,
        "slug": "leetcode-63-unique-paths-ii",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 63 \u2013 Unique Paths II",
        "file": "063-unique-paths-ii.html",
        "date": "2024-09-24T12:08:57",
        "difficulty": "Medium",
        "tags": ["leetcode", "dynamic-programming", "matrix"],
        "excerpt": (
            "Unique Paths with obstacles: the recurrence is unchanged, one guard goes in front of "
            "it. An obstacle means zero paths, and zeros propagate on their own with no "
            "unreachable-region detection. The trap is the first row and column, where one "
            "obstacle cuts off everything after it."
        ),
    },
    {
        "number": 64,
        "slug": "leetcode-64-minimum-path-sum",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 64 \u2013 Minimum Path Sum",
        "file": "064-minimum-path-sum.html",
        "date": "2024-09-25T01:49:36",
        "difficulty": "Medium",
        "tags": ["leetcode", "dynamic-programming", "matrix", "greedy"],
        "excerpt": (
            "Same table, one operator changed, and with it the entire class of problem. Building "
            "the grid where the greedy loses instead of just claiming it does, why a missing "
            "neighbour is infinity here when it was zero in the counting version, and why "
            "Integer.MAX_VALUE as the sentinel overflows into a path through the wall."
        ),
    },
    {
        "number": 65,
        "slug": "leetcode-65-valid-number",
        "algorithm": "Implementation",
        "title": "LeetCode 65 \u2013 Valid Number",
        "file": "065-valid-number.html",
        "date": "2024-10-05T11:28:37",
        "difficulty": "Hard",
        "tags": ["leetcode", "string", "parsing"],
        "excerpt": (
            "Not an algorithms problem at all \u2014 it tests whether you can pin down an ambiguous "
            "spec with questions and turn it into code that does not sprawl. Three flags and one "
            "pass beat the finite-state machine, and resetting seenDigit on e is the single line "
            "that rejects 1e while accepting 3e+7."
        ),
    },
    {
        "number": 67,
        "slug": "leetcode-67-add-binary",
        "algorithm": "Bit Manipulation",
        "title": "LeetCode 67 \u2013 Add Binary",
        "file": "067-add-binary.html",
        "date": "2024-10-06T10:52:23",
        "difficulty": "Easy",
        "tags": ["leetcode", "string", "bit-manipulation", "math"],
        "excerpt": (
            "Looks like string manipulation, is really about carries \u2014 and the parse-to-integer "
            "answer everyone writes first is exactly what the 10,000-character constraint rules "
            "out. Why the carry belongs in the loop condition, why you build and reverse instead of "
            "prepending, and XOR and AND as sum-without-carry and carry."
        ),
    },
    {
        "number": 68,
        "slug": "leetcode-68-text-justification",
        "algorithm": "Implementation",
        "title": "LeetCode 68 \u2013 Text Justification",
        "file": "068-text-justification.html",
        "date": "2024-10-14T01:30:48",
        "difficulty": "Hard",
        "tags": ["leetcode", "string", "simulation", "greedy"],
        "excerpt": (
            "No algorithmic difficulty and one of the highest failure rates on the list, because "
            "the spacing rules have four interacting cases and each is a silent off-by-one. Split "
            "packing from padding before typing, collapse the four cases into two, and remember the "
            "single-word line where gaps would be zero."
        ),
    },
    {
        "number": 69,
        "slug": "leetcode-69-sqrtx",
        "algorithm": "Searching",
        "title": "LeetCode 69 \u2013 Sqrt(x)",
        "file": "069-sqrtx.html",
        "date": "2024-10-20T10:33:41",
        "difficulty": "Easy",
        "tags": ["leetcode", "binary-search", "math"],
        "excerpt": (
            "A binary search problem that never mentions a sorted array \u2014 binary search is for any "
            "monotonic predicate, and spotting one with no array in sight is the lesson. Plus the "
            "overflow that is really the point: mid * mid goes negative near MAX_VALUE and the "
            "search silently walks the wrong way."
        ),
    },
    {
        "number": 70,
        "slug": "leetcode-70-climbing-stairs",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 70 \u2013 Climbing Stairs",
        "file": "070-climbing-stairs.html",
        "date": "2024-10-29T05:44:23",
        "difficulty": "Easy",
        "tags": ["leetcode", "dynamic-programming", "math", "memoization"],
        "excerpt": (
            "Fibonacci wearing a hard hat, and the smallest problem where the recursion-to-DP "
            "conversation happens naturally. Recognising the sequence is nice; being able to say "
            "why it is Fibonacci is the answer, because the recurrence is what survives when the "
            "step sizes become arbitrary and it turns into Coin Change."
        ),
    },
    {
        "number": 71,
        "slug": "leetcode-71-simplify-path",
        "algorithm": "Implementation",
        "title": "LeetCode 71 \u2013 Simplify Path",
        "file": "071-simplify-path.html",
        "date": "2024-10-29T21:06:47",
        "difficulty": "Medium",
        "tags": ["leetcode", "string", "stack"],
        "excerpt": (
            "A stack problem disguised as string manipulation, and the stack is not an optimisation "
            "\u2014 it is the only structure that models what .. means. Splitting on / handles doubled "
            "and trailing slashes for free, popping an empty stack must be a no-op, and \"...\" is an "
            "ordinary filename."
        ),
    },
    {
        "number": 72,
        "slug": "leetcode-72-edit-distance",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 72 \u2013 Edit Distance",
        "file": "072-edit-distance.html",
        "date": "2024-11-04T01:56:29",
        "difficulty": "Hard",
        "tags": ["leetcode", "string", "dynamic-programming"],
        "excerpt": (
            "The two-dimensional DP problem \u2014 if you get one 2-D table fluent, make it this one. "
            "Why dp[i][j] must be defined over prefix lengths rather than indices, why the extra row "
            "and column remove every edge case, and how to work out which neighbour is the insert "
            "instead of guessing."
        ),
    },
    {
        "number": 76,
        "slug": "leetcode-76-minimum-window-substring",
        "algorithm": "Strings",
        "title": "LeetCode 76 \u2013 Minimum Window Substring",
        "file": "076-minimum-window-substring.html",
        "date": "2024-11-04T18:31:10",
        "difficulty": "Hard",
        "tags": ["leetcode", "string", "sliding-window", "hash-table"],
        "excerpt": (
            "The hardest sliding window on most lists, and the difficulty is not the window \u2014 it is "
            "knowing when it is valid without recounting. One integer does it, the counts are allowed "
            "to go negative because the sign carries the surplus, and t = \"aa\" is the case that "
            "separates working from nearly working."
        ),
    },
    {
        "number": 78,
        "slug": "leetcode-78-subsets",
        "algorithm": "Recursion",
        "title": "LeetCode 78 \u2013 Subsets",
        "file": "078-subsets.html",
        "date": "2024-11-05T15:42:30",
        "difficulty": "Medium",
        "tags": ["leetcode", "backtracking", "bit-manipulation", "array"],
        "excerpt": (
            "The cleanest backtracking problem there is, with one structural difference worth "
            "spotting: every node of the recursion tree is an answer, not just the leaves, so the "
            "base case disappears. Plus the two bugs \u2014 i + 1 rather than start + 1, and the copy "
            "without which all 2^n entries alias one list."
        ),
    },
    {
        "number": 81,
        "slug": "leetcode-81-search-in-rotated-sorted-array-ii",
        "algorithm": "Searching",
        "title": "LeetCode 81 \u2013 Search in Rotated Sorted Array II",
        "file": "081-search-in-rotated-sorted-array-ii.html",
        "date": "2024-11-06T15:13:31",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "binary-search"],
        "excerpt": (
            "Problem 33 with duplicates, which looks like a one-line change and is not. Two arrays "
            "with the pivot in different halves can present identical evidence at every point the "
            "algorithm may look, so no decision is right for both. The worst case is O(n) \u2014 and "
            "that bound is on the problem, not on your approach."
        ),
    },
    {
        "number": 83,
        "slug": "leetcode-83-remove-duplicates-from-sorted-list",
        "algorithm": "Implementation",
        "title": "LeetCode 83 \u2013 Remove Duplicates from Sorted List",
        "file": "083-remove-duplicates-from-sorted-list.html",
        "date": "2024-11-08T21:44:36",
        "difficulty": "Easy",
        "tags": ["leetcode", "linked-list", "two-pointers"],
        "excerpt": (
            "Five lines with one bug in them that nearly everyone writes first: advancing after a "
            "deletion skips the node that just became the successor, and only three equal values in "
            "a row exposes it. Also the cleanest place to learn when a linked list needs a dummy "
            "head \u2014 exactly when the head itself can be removed."
        ),
    },
    {
        "number": 88,
        "slug": "leetcode-88-merge-sorted-array",
        "algorithm": "Sorting",
        "title": "LeetCode 88 \u2013 Merge Sorted Array",
        "file": "088-merge-sorted-array.html",
        "date": "2024-11-09T03:58:42",
        "difficulty": "Easy",
        "tags": ["leetcode", "array", "two-pointers", "sorting"],
        "excerpt": (
            "Tagged Easy, with one idea worth more than most Mediums: when you write into an array "
            "you are also reading, go backwards. The trailing zeros are reserved space rather than "
            "data, forwards clobbers values it has not consumed, and looping on nums2 alone is what "
            "makes the remainder handle itself."
        ),
    },
    {
        "number": 91,
        "slug": "leetcode-91-decode-ways",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 91 \u2013 Decode Ways",
        "file": "091-decode-ways.html",
        "date": "2024-11-11T17:55:24",
        "difficulty": "Medium",
        "tags": ["leetcode", "string", "dynamic-programming"],
        "excerpt": (
            "Climbing Stairs with the steps made conditional, and that one change means most wrong "
            "answers come from a single character: '0'. The recurrence takes a minute; the zeros "
            "take the rest of the interview. Why the two-digit gate needs a LOWER bound of 10, and "
            "why ways(0) must be 1."
        ),
    },
    {
        "number": 94,
        "slug": "leetcode-94-binary-tree-inorder-traversal",
        "algorithm": "Graph Theory",
        "title": "LeetCode 94 \u2013 Binary Tree Inorder Traversal",
        "file": "094-binary-tree-inorder-traversal.html",
        "date": "2024-11-12T13:32:53",
        "difficulty": "Easy",
        "tags": ["leetcode", "tree", "stack", "depth-first-search"],
        "excerpt": (
            "Four lines recursively, which is why the statement ends with \"could you do it "
            "iteratively?\" \u2014 the recursion is the warm-up and the explicit stack is the question. "
            "Why the loop needs both halves of its condition, why no visited flag is required, and "
            "Morris traversal for when O(1) space is asked for."
        ),
    },
    {
        "number": 98,
        "slug": "leetcode-98-validate-binary-search-tree",
        "algorithm": "Graph Theory",
        "title": "LeetCode 98 \u2013 Validate Binary Search Tree",
        "file": "098-validate-binary-search-tree.html",
        "date": "2024-11-13T05:30:40",
        "difficulty": "Medium",
        "tags": ["leetcode", "tree", "binary-search-tree", "depth-first-search"],
        "excerpt": (
            "The most famous wrong answer on the list: checking each node against its immediate "
            "children is not the BST property. A node's bounds come from every ancestor and narrow "
            "on the way down. Plus the Integer.MIN_VALUE sentinel trap, and the inorder alternative "
            "that generalises to Recover BST."
        ),
    },
    {
        "number": 100,
        "slug": "leetcode-100-same-tree",
        "algorithm": "Graph Theory",
        "title": "LeetCode 100 \u2013 Same Tree",
        "file": "100-same-tree.html",
        "date": "2024-11-13T16:15:12",
        "difficulty": "Easy",
        "tags": ["leetcode", "tree", "depth-first-search", "recursion"],
        "excerpt": (
            "The smallest possible tree recursion, and the template the harder tree problems are "
            "written against. Three base cases and one recursive step \u2014 and the ORDER of those base "
            "cases is the only thing that can go wrong, because each one protects the next from a "
            "null dereference."
        ),
    },
    {
        "number": 101,
        "slug": "leetcode-101-symmetric-tree",
        "algorithm": "Graph Theory",
        "title": "LeetCode 101 \u2013 Symmetric Tree",
        "file": "101-symmetric-tree.html",
        "date": "2024-11-14T18:05:22",
        "difficulty": "Easy",
        "tags": ["leetcode", "tree", "depth-first-search", "recursion"],
        "excerpt": (
            "Same Tree with two characters changed, and worth doing straight after it for exactly "
            "that reason. Symmetry is a property of a PAIR of nodes, so the recursion takes two "
            "arguments and crosses them. Plus the inorder-palindrome shortcut, and the tree that "
            "kills it."
        ),
    },
    {
        "number": 102,
        "slug": "leetcode-102-binary-tree-level-order-traversal",
        "algorithm": "Graph Theory",
        "title": "LeetCode 102 \u2013 Binary Tree Level Order Traversal",
        "file": "102-binary-tree-level-order-traversal.html",
        "date": "2024-11-15T02:28:19",
        "difficulty": "Medium",
        "tags": ["leetcode", "tree", "breadth-first-search", "queue"],
        "excerpt": (
            "The problem that teaches BFS on trees, and everything depends on one line: capture the "
            "queue's size BEFORE draining the level. Looping on queue.size() re-evaluates a moving "
            "target and takes a meaningless slice. Also why deque beats a list in Python by a whole "
            "factor of n."
        ),
    },
    {
        "number": 103,
        "slug": "leetcode-103-binary-tree-zigzag-level-order-traversal",
        "algorithm": "Graph Theory",
        "title": "LeetCode 103 \u2013 Binary Tree Zigzag Level Order Traversal",
        "file": "103-binary-tree-zigzag-level-order-traversal.html",
        "date": "2024-11-15T10:29:53",
        "difficulty": "Medium",
        "tags": ["leetcode", "tree", "breadth-first-search", "queue"],
        "excerpt": (
            "Level order with the direction alternating, and the answer people reach for first \u2014 "
            "reversing the queue \u2014 is the one that breaks. How you traverse and how you report are "
            "different things, and modifying the traversal to change the output is a category "
            "error."
        ),
    },
    {
        "number": 104,
        "slug": "leetcode-104-maximum-depth-of-binary-tree",
        "algorithm": "Graph Theory",
        "title": "LeetCode 104 \u2013 Maximum Depth of Binary Tree",
        "file": "104-maximum-depth-of-binary-tree.html",
        "date": "2024-11-17T05:54:48",
        "difficulty": "Easy",
        "tags": ["leetcode", "tree", "depth-first-search", "recursion"],
        "excerpt": (
            "Three lines, and the smallest problem where the recursive shape of tree algorithms is "
            "visible. The real value is the trap it sets up: swapping max for min does NOT give "
            "minimum depth, because a node with one child is not a leaf and the null branch reports "
            "a path ending in mid-air."
        ),
    },
    {
        "number": 105,
        "slug": "leetcode-105-construct-binary-tree-from-preorder-and-inorder-traversal",
        "algorithm": "Graph Theory",
        "title": "LeetCode 105 \u2013 Construct Binary Tree from Preorder and Inorder Traversal",
        "file": "105-construct-binary-tree-from-preorder-and-inorder-traversal.html",
        "date": "2024-11-22T00:19:17",
        "difficulty": "Medium",
        "tags": ["leetcode", "tree", "hash-table", "divide-and-conquer"],
        "excerpt": (
            "The problem that makes traversal orders click: preorder tells you the root, inorder "
            "tells you the split. Why the hash map is what makes it O(n), why slicing arrays "
            "quietly reintroduces the quadratic, why the left subtree must be built first, and why "
            "preorder plus postorder is not enough."
        ),
    },
    {
        "number": 110,
        "slug": "leetcode-110-balanced-binary-tree",
        "algorithm": "Graph Theory",
        "title": "LeetCode 110 \u2013 Balanced Binary Tree",
        "file": "110-balanced-binary-tree.html",
        "date": "2024-11-23T17:51:05",
        "difficulty": "Easy",
        "tags": ["leetcode", "tree", "depth-first-search", "recursion"],
        "excerpt": (
            "A correct answer most people write and a better one the same length. The gap is one "
            "idea: make the return value carry two things. Heights are never negative, so -1 is a "
            "free sentinel for \"unbalanced\" \u2014 and that turns O(n log n) into O(n) with an early "
            "exit for free."
        ),
    },
    {
        "number": 111,
        "slug": "leetcode-111-minimum-depth-of-binary-tree",
        "algorithm": "Graph Theory",
        "title": "LeetCode 111 \u2013 Minimum Depth of Binary Tree",
        "file": "111-minimum-depth-of-binary-tree.html",
        "date": "2024-11-24T14:56:31",
        "difficulty": "Easy",
        "tags": ["leetcode", "tree", "breadth-first-search", "depth-first-search"],
        "excerpt": (
            "The payoff for the trap set in problem 104: swapping max for min is wrong, because a "
            "node with one child is not a leaf and its missing side still reports zero. A missing "
            "child is infinity, not zero \u2014 and this is where BFS genuinely beats DFS, since it can "
            "stop at the first leaf."
        ),
    },
    {
        "number": 112,
        "slug": "leetcode-112-path-sum",
        "algorithm": "Graph Theory",
        "title": "LeetCode 112 \u2013 Path Sum",
        "file": "112-path-sum.html",
        "date": "2024-11-25T04:00:41",
        "difficulty": "Easy",
        "tags": ["leetcode", "tree", "depth-first-search", "recursion"],
        "excerpt": (
            "A three-line recursion containing a base case almost everyone writes wrong. Returning "
            "targetSum == 0 at a null accepts a path that stops at a non-leaf, and it passes the "
            "examples while failing on a four-node tree. Null is not a leaf. Plus why negative "
            "values kill the obvious pruning."
        ),
    },
    {
        "number": 114,
        "slug": "leetcode-114-flatten-binary-tree-to-linked-list",
        "algorithm": "Graph Theory",
        "title": "LeetCode 114 \u2013 Flatten Binary Tree to Linked List",
        "file": "114-flatten-binary-tree-to-linked-list.html",
        "date": "2024-11-26T08:41:43",
        "difficulty": "Medium",
        "tags": ["leetcode", "tree", "linked-list", "stack"],
        "excerpt": (
            "The best problem on the list for the idea that pointer surgery can replace a data "
            "structure. Three solutions using O(n), O(h) and O(1) space \u2014 the last one splices the "
            "right subtree onto the left subtree's rightmost node, which is Morris threading kept "
            "rather than undone."
        ),
    },
    {
        "number": 118,
        "slug": "leetcode-118-pascals-triangle",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 118 \u2013 Pascal's Triangle",
        "file": "118-pascals-triangle.html",
        "date": "2024-11-29T08:17:04",
        "difficulty": "Easy",
        "tags": ["leetcode", "array", "dynamic-programming"],
        "excerpt": (
            "The gentlest bottom-up DP there is, and on the list as the setup for its follow-up. "
            "The edges are where the rule runs out of inputs rather than a special case bolted on, "
            "the output size IS the complexity so there is nothing to optimise \u2014 which is exactly "
            "why problem 119 asks for one row."
        ),
    },
    {
        "number": 119,
        "slug": "leetcode-119-pascals-triangle-ii",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 119 \u2013 Pascal's Triangle II",
        "file": "119-pascals-triangle-ii.html",
        "date": "2024-12-05T01:41:56",
        "difficulty": "Easy",
        "tags": ["leetcode", "array", "dynamic-programming"],
        "excerpt": (
            "One row, in O(k) space, which turns a warm-up into a real exercise in updating an "
            "array without destroying what you are about to read. Sweep right to left so the stale "
            "values survive \u2014 the same rule that separates 0/1 knapsack from unbounded, and the "
            "question is always which values the cell needs."
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
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 121 – Best Time to Buy and Sell Stock",
        "file": "121-best-time-to-buy-and-sell-stock.html",
        "date": "2024-12-08T10:41:05",
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
        "number": 122,
        "slug": "leetcode-122-best-time-to-buy-and-sell-stock-ii",
        "algorithm": "Greedy",
        "title": "LeetCode 122 \u2013 Best Time to Buy and Sell Stock II",
        "file": "122-best-time-to-buy-and-sell-stock-ii.html",
        "date": "2024-12-10T18:35:50",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "greedy", "dynamic-programming"],
        "excerpt": (
            "A rare case where removing a constraint makes the problem easier. Every profit is a "
            "sum of consecutive daily deltas, so take every positive one \u2014 and that derivation is "
            "what turns a greedy that looks like cheating into one that is obviously optimal. Plus "
            "the two-state form that survives fees, cooldowns and caps."
        ),
    },
    {
        "number": 124,
        "slug": "leetcode-124-binary-tree-maximum-path-sum",
        "algorithm": "Graph Theory",
        "title": "LeetCode 124 \u2013 Binary Tree Maximum Path Sum",
        "file": "124-binary-tree-maximum-path-sum.html",
        "date": "2024-12-10T21:45:12",
        "difficulty": "Hard",
        "tags": ["leetcode", "tree", "depth-first-search", "recursion"],
        "excerpt": (
            "The hardest version of the pattern this track has been building toward since Diameter: "
            "the recursion returns one quantity and records another. A path that uses both children "
            "cannot also reach the parent, which is the geometric fact behind the whole solution. "
            "Twelve lines, and no debugging helps if the two are confused."
        ),
    },
    {
        "number": 125,
        "slug": "leetcode-125-valid-palindrome",
        "algorithm": "Strings",
        "title": "LeetCode 125 \u2013 Valid Palindrome",
        "file": "125-valid-palindrome.html",
        "date": "2024-12-14T17:10:27",
        "difficulty": "Easy",
        "tags": ["leetcode", "string", "two-pointers"],
        "excerpt": (
            "A two-pointer warm-up with one nasty trap: '0' and 'P' differ by exactly 32, so the "
            "popular case-insensitive shortcut says they match. The 32 gap is a fact about letters, "
            "and it stops meaning anything the moment digits are in scope. Also why each skip loop "
            "needs its own bound."
        ),
    },
    {
        "number": 131,
        "slug": "leetcode-131-palindrome-partitioning",
        "algorithm": "Recursion",
        "title": "LeetCode 131 \u2013 Palindrome Partitioning",
        "file": "131-palindrome-partitioning.html",
        "date": "2024-12-14T21:12:31",
        "difficulty": "Medium",
        "tags": ["leetcode", "backtracking", "string", "dynamic-programming"],
        "excerpt": (
            "Backtracking with a filter, and the cleanest illustration of where the recording "
            "happens: Subsets records at every node, this records only when the string is fully "
            "consumed. Get that wrong and partial partitions land in the output. Plus the "
            "precomputed palindrome table for the repeated work."
        ),
    },
    {
        "number": 133,
        "slug": "leetcode-133-clone-graph",
        "algorithm": "Graph Theory",
        "title": "LeetCode 133 \u2013 Clone Graph",
        "file": "133-clone-graph.html",
        "date": "2024-12-17T13:16:06",
        "difficulty": "Medium",
        "tags": ["leetcode", "graph", "hash-table", "depth-first-search"],
        "excerpt": (
            "The traversal is the easy part. One hash map does two jobs \u2014 visited set and "
            "old-to-new mapping \u2014 and one line decides whether the function terminates at all: "
            "register the clone BEFORE recursing, or an undirected edge sends you straight back and "
            "never bottoms out."
        ),
    },
    {
        "number": 134,
        "slug": "leetcode-134-gas-station",
        "algorithm": "Greedy",
        "title": "LeetCode 134 \u2013 Gas Station",
        "file": "134-gas-station.html",
        "date": "2024-12-17T19:51:21",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "greedy"],
        "excerpt": (
            "Eight lines of code and a proof that is the entire interview. Why a non-negative total "
            "guarantees a solution exists, and why running dry at station i rules out every start "
            "from the current candidate through i \u2014 which is what makes it one pass instead of "
            "quadratic. The reset is Kadane, read differently."
        ),
    },
    {
        "number": 136,
        "slug": "leetcode-136-single-number",
        "algorithm": "Bit Manipulation",
        "title": "LeetCode 136 \u2013 Single Number",
        "file": "136-single-number.html",
        "date": "2024-12-18T00:18:45",
        "difficulty": "Easy",
        "tags": ["leetcode", "array", "bit-manipulation"],
        "excerpt": (
            "The problem that teaches XOR as a tool rather than a curiosity. Linear time and "
            "constant space rule out both obvious answers, and what is left is a one-line fold \u2014 "
            "which looks like magic until you name the three properties, including the "
            "commutativity that handles unsorted input."
        ),
    },
    {
        "number": 138,
        "slug": "leetcode-138-copy-list-with-random-pointer",
        "algorithm": "Implementation",
        "title": "LeetCode 138 \u2013 Copy List with Random Pointer",
        "file": "138-copy-list-with-random-pointer.html",
        "date": "2024-12-18T20:52:32",
        "difficulty": "Medium",
        "tags": ["leetcode", "linked-list", "hash-table"],
        "excerpt": (
            "Clone Graph in a linked list's clothes: you cannot point at a node that does not exist "
            "yet, and random pointers point forwards. The map answer is short and correct. The "
            "O(1) answer stores the mapping inside the list itself by weaving each copy in after "
            "its original."
        ),
    },
    {
        "number": 139,
        "slug": "leetcode-139-word-break",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 139 \u2013 Word Break",
        "file": "139-word-break.html",
        "date": "2024-12-19T03:56:45",
        "difficulty": "Medium",
        "tags": ["leetcode", "string", "dynamic-programming", "hash-table"],
        "excerpt": (
            "Where greedy string matching visibly fails and DP visibly saves it, with a "
            "counterexample small enough for a whiteboard. The reframing is the usual one \u2014 can the "
            "first i characters be built? \u2014 and dp[0] = true is doing real work. Plus why the "
            "dictionary must be a set."
        ),
    },
    {
        "number": 141,
        "slug": "leetcode-141-linked-list-cycle",
        "algorithm": "Implementation",
        "title": "LeetCode 141 \u2013 Linked List Cycle",
        "file": "141-linked-list-cycle.html",
        "date": "2024-12-19T17:49:58",
        "difficulty": "Easy",
        "tags": ["leetcode", "linked-list", "two-pointers", "hash-table"],
        "excerpt": (
            "Where Floyd's tortoise and hare earns its keep. The hash set is correct and obvious; "
            "the two-pointer version is constant space and rests on an argument you should be able "
            "to give, because \"they meet eventually\" is an assertion. The gap closes by exactly "
            "one per step, so it must pass through zero."
        ),
    },
    {
        "number": 142,
        "slug": "leetcode-142-linked-list-cycle-ii",
        "algorithm": "Implementation",
        "title": "LeetCode 142 \u2013 Linked List Cycle II",
        "file": "142-linked-list-cycle-ii.html",
        "date": "2024-12-21T09:31:36",
        "difficulty": "Medium",
        "tags": ["leetcode", "linked-list", "two-pointers", "hash-table"],
        "excerpt": (
            "Reset one pointer to the head after they meet and both walk to the cycle's entrance. "
            "It looks like a coincidence and it is four lines of algebra: t = k*c - m. Deriving "
            "that is what separates recall from understanding \u2014 and it is the same trick behind "
            "Find the Duplicate Number."
        ),
    },
    {
        "number": 144,
        "slug": "leetcode-144-binary-tree-preorder-traversal",
        "algorithm": "Graph Theory",
        "title": "LeetCode 144 \u2013 Binary Tree Preorder Traversal",
        "file": "144-binary-tree-preorder-traversal.html",
        "date": "2024-12-25T22:50:19",
        "difficulty": "Easy",
        "tags": ["leetcode", "tree", "stack", "depth-first-search"],
        "excerpt": (
            "The easiest of the three traversals to write iteratively, and worth doing right after "
            "inorder because the contrast explains why: a preorder node is emitted the moment you "
            "arrive, so there is nothing to come back for. Push right before left, since a stack "
            "reverses what you give it."
        ),
    },
    {
        "number": 145,
        "slug": "leetcode-145-binary-tree-postorder-traversal",
        "algorithm": "Graph Theory",
        "title": "LeetCode 145 \u2013 Binary Tree Postorder Traversal",
        "file": "145-binary-tree-postorder-traversal.html",
        "date": "2024-12-28T00:52:03",
        "difficulty": "Easy",
        "tags": ["leetcode", "tree", "stack", "depth-first-search"],
        "excerpt": (
            "The hardest traversal to write iteratively, and the standard answer avoids writing it "
            "at all: postorder reversed is node-right-left, which is preorder with the children "
            "swapped. Two lines changed and every awkwardness disappears \u2014 plus what it costs when "
            "you genuinely need it bottom-up."
        ),
    },
    {
        "number": 146,
        "slug": "leetcode-146-lru-cache",
        "algorithm": "Implementation",
        "title": "LeetCode 146 \u2013 LRU Cache",
        "file": "146-lru-cache.html",
        "date": "2025-01-01T21:43:41",
        "difficulty": "Medium",
        "tags": ["leetcode", "design", "hash-table", "linked-list"],
        "excerpt": (
            "The most common design question on the list, and a design question rather than an "
            "algorithms one: no single structure does the job, and two together give O(1) "
            "everywhere. Why the list must be doubly linked, why sentinels delete a dozen branches, "
            "and why the node has to store its own key."
        ),
    },
    {
        "number": 149,
        "slug": "leetcode-149-max-points-on-a-line",
        "algorithm": "Implementation",
        "title": "LeetCode 149 \u2013 Max Points on a Line",
        "file": "149-max-points-on-a-line.html",
        "date": "2025-01-03T01:03:48",
        "difficulty": "Hard",
        "tags": ["leetcode", "array", "hash-table", "math"],
        "excerpt": (
            "A Hard problem whose algorithm is trivial and whose difficulty is entirely how you "
            "represent a slope. Floating point is unsound as a hash key and fails silently on large "
            "coordinates; an unreduced pair splits equal slopes; a reduced pair without a sign "
            "convention splits opposite directions."
        ),
    },
    {
        "number": 151,
        "slug": "leetcode-151-reverse-words-in-a-string",
        "algorithm": "Strings",
        "title": "LeetCode 151 \u2013 Reverse Words in a String",
        "file": "151-reverse-words-in-a-string.html",
        "date": "2025-01-06T21:53:01",
        "difficulty": "Medium",
        "tags": ["leetcode", "string", "two-pointers"],
        "excerpt": (
            "One line in Python and a real exercise in Java, which is what makes it a good "
            "question. Reverse the whole string, then reverse each word back \u2014 the first pass fixes "
            "the order and breaks the spelling, the second fixes the spelling without moving "
            "anything. The spaces are the fiddly part."
        ),
    },
    {
        "number": 152,
        "slug": "leetcode-152-maximum-product-subarray",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 152 \u2013 Maximum Product Subarray",
        "file": "152-maximum-product-subarray.html",
        "date": "2025-01-08T19:10:17",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "dynamic-programming"],
        "excerpt": (
            "Kadane with multiplication, and the change is bigger than it looks: a large negative is "
            "not a bad prefix, it is a latent good one waiting for another negative. Carry the "
            "minimum as well as the maximum, and watch the assignment order \u2014 curMin needs the OLD "
            "curMax."
        ),
    },
    {
        "number": 156,
        "slug": "leetcode-156-binary-tree-upside-down",
        "algorithm": "Graph Theory",
        "title": "LeetCode 156 \u2013 Binary Tree Upside Down",
        "file": "156-binary-tree-upside-down.html",
        "date": "2025-01-09T16:30:18",
        "difficulty": "Medium",
        "tags": ["leetcode", "tree", "recursion"],
        "excerpt": (
            "Pure pointer surgery with no search and no complexity to argue about. The whole problem "
            "is doing four assignments in an order that does not destroy what the next one needs \u2014 "
            "null out root.left before reading it and the subtree is gone. Both pointers must be "
            "nulled, not just one."
        ),
    },
    {
        "number": 157,
        "slug": "leetcode-157-read-n-characters-given-read4",
        "algorithm": "Implementation",
        "title": "LeetCode 157 \u2013 Read N Characters Given Read4",
        "file": "157-read-n-characters-given-read4.html",
        "date": "2025-01-14T10:27:27",
        "difficulty": "Easy",
        "tags": ["leetcode", "array", "simulation", "interactive"],
        "excerpt": (
            "An API-adaptation problem: a primitive that reads in 4-character chunks, a caller that "
            "wants exactly n. A short read means end of file, and both limits need guarding \u2014 "
            "writing past n is a buffer overrun into the caller's memory, not a wrong answer."
        ),
    },
    {
        "number": 158,
        "slug": "leetcode-158-read-n-characters-given-read4-ii-call-multiple-times",
        "algorithm": "Implementation",
        "title": "LeetCode 158 \u2013 Read N Characters Given Read4 II \u2013 Call Multiple Times",
        "file": "158-read-n-characters-given-read4-ii-call-multiple-times.html",
        "date": "2025-01-14T19:59:36",
        "difficulty": "Hard",
        "tags": ["leetcode", "array", "simulation", "design"],
        "excerpt": (
            "The same API with one sentence changed, and that sentence changes the design rather "
            "than the code. Problem 157 discards the surplus from its last chunk; called twice, that "
            "surplus is lost data. Three fields of state, and you have written a buffered reader."
        ),
    },
    {
        "number": 159,
        "slug": "leetcode-159-longest-substring-with-at-most-two-distinct-characters",
        "algorithm": "Strings",
        "title": "LeetCode 159 \u2013 Longest Substring with At Most Two Distinct Characters",
        "file": "159-longest-substring-with-at-most-two-distinct-characters.html",
        "date": "2025-01-18T17:34:44",
        "difficulty": "Medium",
        "tags": ["leetcode", "string", "sliding-window", "hash-table"],
        "excerpt": (
            "The sliding window at its most reusable, and unlike Minimum Window Substring it "
            "generalises to k by changing one literal. The single bug it has: a count that reaches "
            "zero must be DELETED, not left sitting there, or the map size counts characters that "
            "have already left the window."
        ),
    },
    {
        "number": 160,
        "batch": "round-17",
        "slug": "leetcode-160-intersection-of-two-linked-lists",
        "algorithm": "Implementation",
        "title": "LeetCode 160 \u2013 Intersection of Two Linked Lists",
        "file": "160-intersection-of-two-linked-lists.html",
        "date": "2025-01-21T17:00:29",
        "difficulty": "Easy",
        "tags": ["leetcode", "linked-list", "two-pointers", "hash-table"],
        "excerpt": (
            "An O(1)-space solution that looks like sleight of hand: when a pointer runs off one "
            "list, restart it on the other. The trick is two lines and the reason is one equation \u2014 "
            "a + c + b = b + c + a, so both arrive together. Switch on null, not on the last node."
        ),
    },
    {
        "number": 168,
        "batch": "round-17",
        "slug": "leetcode-168-excel-sheet-column-title",
        "algorithm": "Strings",
        "title": "LeetCode 168 \u2013 Excel Sheet Column Title",
        "file": "168-excel-sheet-column-title.html",
        "date": "2025-01-23T15:33:17",
        "difficulty": "Easy",
        "tags": ["leetcode", "string", "math"],
        "excerpt": (
            "Looks like base-26 and is not: Excel's digits run A to Z representing 1 to 26, with no "
            "symbol for zero. That single missing digit is the entire problem, the fix is one "
            "decrement inside the loop, and 26 vs 27 is where every wrong solution shows itself."
        ),
    },
    {
        "number": 169,
        "batch": "round-17",
        "slug": "leetcode-169-majority-element",
        "algorithm": "Implementation",
        "title": "LeetCode 169 \u2013 Majority Element",
        "file": "169-majority-element.html",
        "date": "2025-01-25T15:16:20",
        "difficulty": "Easy",
        "tags": ["leetcode", "array", "divide-and-conquer", "sorting"],
        "excerpt": (
            "Boyer-Moore voting is four lines that look like they cannot be correct, and the "
            "counting argument is short enough to give out loud: every disagreement cancels a pair, "
            "and a strict majority cannot be exhausted. The algorithm does not find the majority \u2014 "
            "it eliminates everything that cannot be it."
        ),
    },
    {
        "number": 170,
        "batch": "round-17",
        "slug": "leetcode-170-two-sum-iii-data-structure-design",
        "algorithm": "Implementation",
        "title": "LeetCode 170 \u2013 Two Sum III \u2013 Data Structure Design",
        "file": "170-two-sum-iii-data-structure-design.html",
        "date": "2025-01-28T11:03:28",
        "difficulty": "Easy",
        "tags": ["leetcode", "design", "hash-table", "two-pointers"],
        "excerpt": (
            "Not an algorithms problem \u2014 a question about which operation gets called more often. "
            "Two designs with opposite costs, and the answer the interviewer wants is the sentence "
            "that chooses between them. Plus why it must count rather than use a set: find(4) after "
            "one add(2) is false."
        ),
    },
    {
        "number": 173,
        "slug": "leetcode-173-binary-search-tree-iterator",
        "algorithm": "Graph Theory",
        "title": "LeetCode 173 \u2013 Binary Search Tree Iterator",
        "file": "173-binary-search-tree-iterator.html",
        "date": "2025-01-30T13:48:01",
        "difficulty": "Medium",
        "tags": ["leetcode", "tree", "stack", "design", "binary-search-tree"],
        "excerpt": (
            "Inorder traversal split across two methods, and that is the whole insight \u2014 the "
            "descend-left loop becomes the advance step and the stack becomes the object's state. "
            "Plus the amortised argument that makes next() O(1) on average when a single call can "
            "clearly do O(h) work."
        ),
    },
    {
        "number": 189,
        "slug": "leetcode-189-rotate-array",
        "algorithm": "Implementation",
        "title": "LeetCode 189 \u2013 Rotate Array",
        "file": "189-rotate-array.html",
        "date": "2025-02-04T02:27:36",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "two-pointers", "math"],
        "excerpt": (
            "The array version of Reverse Words in a String, using the identical three-reversal "
            "trick. It is also where forgetting k %= n turns a correct algorithm into an exception, "
            "and where the Python one-liner rebinds a local name so the caller sees nothing at all."
        ),
    },
    {
        "number": 198,
        "slug": "leetcode-198-house-robber",
        "algorithm": "Dynamic Programming",
        "title": "LeetCode 198 \u2013 House Robber",
        "file": "198-house-robber.html",
        "date": "2025-02-11T19:13:59",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "dynamic-programming"],
        "excerpt": (
            "The DP that introduces a choice: Climbing Stairs counted branches and added them, this "
            "picks the better of two. Same dependencies, different combiner. And the alternating "
            "greedy everyone proposes fails on [2,1,1,2], where the best answer skips two houses in "
            "a row."
        ),
    },
    {
        "number": 199,
        "slug": "leetcode-199-binary-tree-right-side-view",
        "algorithm": "Graph Theory",
        "title": "LeetCode 199 \u2013 Binary Tree Right Side View",
        "file": "199-binary-tree-right-side-view.html",
        "date": "2025-02-14T22:51:44",
        "difficulty": "Medium",
        "tags": ["leetcode", "tree", "breadth-first-search", "depth-first-search"],
        "excerpt": (
            "The clearest illustration that how you traverse and what you record are independent: "
            "level order with one line changed. The visible node may be a LEFT child \u2014 rightmost at "
            "its depth, not on the right spine \u2014 which is what any walk-down-the-right-side answer "
            "gets wrong."
        ),
    },
    {
        "number": 200,
        "batch": "interview-essentials",
        "slug": "leetcode-200-number-of-islands",
        "algorithm": "Graph Theory",
        "title": "LeetCode 200 – Number of Islands",
        "file": "200-number-of-islands.html",
        "date": "2025-02-15T11:47:03",
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
        "number": 202,
        "slug": "leetcode-202-happy-number",
        "algorithm": "Implementation",
        "title": "LeetCode 202 \u2013 Happy Number",
        "file": "202-happy-number.html",
        "date": "2025-02-16T12:36:16",
        "difficulty": "Easy",
        "tags": ["leetcode", "hash-table", "math", "two-pointers"],
        "excerpt": (
            "Linked List Cycle with the list replaced by a function. No nodes, no next pointer, and Floyd's algorithm works anyway \u2014 which is the point: cycle detection needs a successor function, not a data structure. Plus why the sequence must terminate at all."
        ),
    },
    {
        "number": 203,
        "slug": "leetcode-203-remove-linked-list-elements",
        "algorithm": "Implementation",
        "title": "LeetCode 203 \u2013 Remove Linked List Elements",
        "file": "203-remove-linked-list-elements.html",
        "date": "2025-02-17T22:45:12",
        "difficulty": "Easy",
        "tags": ["leetcode", "linked-list", "recursion"],
        "excerpt": (
            "The problem that proves the dummy-head rule problem 83 stated. Here the head CAN be removed, repeatedly, so the dummy stops being a preference and becomes what makes the code short. And you must return dummy.next, never head."
        ),
    },
    {
        "number": 204,
        "slug": "leetcode-204-count-primes",
        "algorithm": "Implementation",
        "title": "LeetCode 204 \u2013 Count Primes",
        "file": "204-count-primes.html",
        "date": "2025-02-23T00:09:04",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "math", "enumeration"],
        "excerpt": (
            "A problem about knowing an algorithm rather than deriving one. What is actually tested is the two optimisations that make the sieve fast \u2014 stop at sqrt(n), start the inner loop at p*p \u2014 and whether you can say why both follow from one fact."
        ),
    },
    {
        "number": 205,
        "slug": "leetcode-205-isomorphic-strings",
        "algorithm": "Strings",
        "title": "LeetCode 205 \u2013 Isomorphic Strings",
        "file": "205-isomorphic-strings.html",
        "date": "2025-02-24T16:11:54",
        "difficulty": "Easy",
        "tags": ["leetcode", "string", "hash-table"],
        "excerpt": (
            "A one-map solution that is wrong and a two-map solution that is right, separated by a single word in the problem statement. The pair badc / baba passes every consistency check and is still not isomorphic, because b and d both map to b."
        ),
    },
    {
        "number": 206,
        "slug": "leetcode-206-reverse-linked-list",
        "algorithm": "Implementation",
        "title": "LeetCode 206 \u2013 Reverse Linked List",
        "file": "206-reverse-linked-list.html",
        "date": "2025-02-26T15:06:16",
        "difficulty": "Easy",
        "tags": ["leetcode", "linked-list", "recursion"],
        "excerpt": (
            "The most-asked list question there is, and it is asked because four assignments in the wrong order lose the rest of the list. Save the successor before overwriting the link, return previous rather than current \u2014 and it is a building block for half the harder list problems."
        ),
    },
    {
        "number": 207,
        "slug": "leetcode-207-course-schedule",
        "algorithm": "Graph Theory",
        "title": "LeetCode 207 \u2013 Course Schedule",
        "file": "207-course-schedule.html",
        "date": "2025-02-27T18:15:50",
        "difficulty": "Medium",
        "tags": ["leetcode", "graph", "topological-sort", "breadth-first-search"],
        "excerpt": (
            "Cycle detection in a directed graph wearing a scheduling problem's clothes. Kahn's algorithm never looks for the cycle \u2014 it notices what is left over. And the DFS version needs THREE node states, because already-finished and currently-above-me are different facts."
        ),
    },
    {
        "number": 208,
        "slug": "leetcode-208-implement-trie-prefix-tree",
        "algorithm": "Implementation",
        "title": "LeetCode 208 \u2013 Implement Trie (Prefix Tree)",
        "file": "208-implement-trie-prefix-tree.html",
        "date": "2025-03-01T18:24:08",
        "difficulty": "Medium",
        "tags": ["leetcode", "design", "trie", "string"],
        "excerpt": (
            "A build-the-structure question where the interview is really two things: why a trie beats a hash set for prefix queries, and the one boolean separating a word from a prefix. Every operation is independent of how many words are stored."
        ),
    },
    {
        "number": 210,
        "slug": "leetcode-210-course-schedule-ii",
        "algorithm": "Graph Theory",
        "title": "LeetCode 210 \u2013 Course Schedule II",
        "file": "210-course-schedule-ii.html",
        "date": "2025-03-01T20:26:03",
        "difficulty": "Medium",
        "tags": ["leetcode", "graph", "topological-sort", "breadth-first-search"],
        "excerpt": (
            "Problem 207 asked whether an ordering exists; this wants the ordering, which Kahn's algorithm already had and threw away. The list IS the count. Plus why the DFS version comes out backwards, and the heap that gives the lexicographically smallest order."
        ),
    },
    {
        "number": 211,
        "slug": "leetcode-211-design-add-and-search-words",
        "algorithm": "Implementation",
        "title": "LeetCode 211 \u2013 Design Add and Search Words Data Structure",
        "file": "211-design-add-and-search-words.html",
        "date": "2025-03-04T05:30:53",
        "difficulty": "Medium",
        "tags": ["leetcode", "design", "trie", "depth-first-search"],
        "excerpt": (
            "Implement Trie with one wildcard added, and that wildcard is the whole problem. A trie search is a walk down one path; a dot turns it into a search over all of them, so the lookup stops being a loop and the complexity stops being linear."
        ),
    },
    {
        "number": 215,
        "slug": "leetcode-215-kth-largest-element-in-an-array",
        "algorithm": "Sorting",
        "title": "LeetCode 215 \u2013 Kth Largest Element in an Array",
        "file": "215-kth-largest-element-in-an-array.html",
        "date": "2025-03-04T11:02:00",
        "difficulty": "Medium",
        "tags": ["leetcode", "array", "heap", "quickselect", "sorting"],
        "excerpt": (
            "A menu problem: three standard answers with genuinely different trade-offs, and the interview is choosing among them out loud. Why a MIN-heap answers a largest question, why quickselect is O(n) on average, and why the random pivot is not optional."
        ),
    },
    {
        "number": 217,
        "slug": "leetcode-217-contains-duplicate",
        "algorithm": "Warmup",
        "title": "LeetCode 217 \u2013 Contains Duplicate",
        "file": "217-contains-duplicate.html",
        "date": "2025-03-04T15:15:33",
        "difficulty": "Easy",
        "tags": ["leetcode", "array", "hash-table", "sorting"],
        "excerpt": (
            "A warm-up with one real decision in it, and the decision is about space. The hash set is the default; sorting is the O(1)-space alternative that mutates the input. Noticing a time-for-space trade in an Easy problem is most of what there is to say."
        ),
    },
    {
        "number": 218,
        "slug": "leetcode-218-the-skyline-problem",
        "algorithm": "Sorting",
        "title": "LeetCode 218 \u2013 The Skyline Problem",
        "file": "218-the-skyline-problem.html",
        "date": "2025-03-06T22:04:48",
        "difficulty": "Hard",
        "tags": ["leetcode", "heap", "sorting", "sweep-line", "divide-and-conquer"],
        "excerpt": (
            "The hardest problem on this track, and almost none of it is the algorithm. Sweep left to right and emit a point when the tallest active building changes. The difficulty is three tie-break rules and deleting from a heap \u2014 and one sign trick gives all three rules from a single sort."
        ),
    },
    {
        "number": 219,
        "slug": "leetcode-219-contains-duplicate-ii",
        "algorithm": "Implementation",
        "title": "LeetCode 219 \u2013 Contains Duplicate II",
        "file": "219-contains-duplicate-ii.html",
        "date": "2025-03-11T15:24:08",
        "difficulty": "Easy",
        "tags": ["leetcode", "array", "hash-table", "sliding-window"],
        "excerpt": (
            "Contains Duplicate with a distance limit, and the limit is what turns a set into a sliding window. Bound the set to k and a hit implies proximity for free. Plus why the last-seen map may overwrite: a closer occurrence dominates the older one forever."
        ),
    },
    {
        "number": 347,
        "batch": "interview-essentials",
        "slug": "leetcode-347-top-k-frequent-elements",
        "algorithm": "Sorting",
        "title": "LeetCode 347 – Top K Frequent Elements",
        "file": "347-top-k-frequent-elements.html",
        "date": "2025-07-05T16:22:41",
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
        "algorithm": "Graph Theory",
        "title": "LeetCode 543 – Diameter of Binary Tree",
        "file": "543-diameter-of-binary-tree.html",
        "date": "2025-09-23T09:14:58",
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
    # Legacy rewrites - posts migrated from WordPress in 2019 that already own
    # their URLs. They have no LeetCode number, so they are excluded from the
    # manifest's number/date ordering checks (see check_content.py).
    #
    # upsert_post keeps an existing post's `date`, so the dates below are only
    # documentation -- re-seeding will NOT move these in the archive. Their slugs
    # are live and must not change.
    {
        "batch": "legacy-rewrite",
        "slug": "fundamental-problem-two-number-sum",
        "algorithm": "Searching",
        "title": "Two Number Sum",
        "file": "legacy-two-number-sum.html",
        "date": "2019-02-09T22:38:47",
        "difficulty": "Easy",
        "tags": ["array", "hash-table", "two-pointers"],
        "excerpt": (
            "Three reasonable answers with genuinely different trade-offs, and laying all three out "
            "before choosing is the actual skill being tested. Why the inner loop starts at x + 1 "
            "rather than 0, why you must check the set before inserting or an element pairs with "
            "itself, and why sorting quietly reorders the caller's array. Java and Python, plus the "
            "indices variant."
        ),
    },
    {
        "batch": "legacy-rewrite",
        "slug": "fundamental-problem-three-number-sum",
        "algorithm": "Sorting",
        "title": "Three Number Sum",
        "file": "legacy-three-number-sum.html",
        "date": "2019-02-10T05:47:15",
        "difficulty": "Medium",
        "tags": ["array", "two-pointers", "sorting"],
        "excerpt": (
            "Where the two-pointer technique stops being a curiosity and becomes the tool — sorting "
            "buys three separate things at once and no hash-based approach gets all three. Why both "
            "pointers move after a hit, why the result should be List<List<Integer>> rather than "
            "List<Integer[]>, and exactly what changes when duplicates are allowed."
        ),
    },
    {
        "batch": "legacy-rewrite",
        "slug": "fundamental-problem-recursion",
        "algorithm": "Recursion",
        "title": "Recursion in Coding Interviews",
        "file": "legacy-recursion.html",
        "date": "2018-02-07T07:48:22",
        "difficulty": None,
        "tags": ["recursion", "backtracking", "interview"],
        "excerpt": (
            "Most people can explain what recursion is and still freeze when a problem needs it "
            "under time pressure. The three questions that turn a blank page into a fill-in-the-"
            "blanks exercise, the leap of faith that stops you tracing calls in your head, when "
            "recursion is the wrong tool, and how to reason about the cost of a branching search."
        ),
    },
]
