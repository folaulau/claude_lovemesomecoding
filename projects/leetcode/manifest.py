"""The LeetCode track: category metadata plus one entry per problem.

One post per problem, published in rounds of ten LeetCode numbers. The source
repo does not have every number, so a round only contains the problems that
exist in it — round 1 covers LeetCode 1-10 and holds seven posts.

`date` drives ordering everywhere on the site: archives and the sitemap sort
newest first, and `siblings()` in the frontend reverses the category index so
prev/next walks oldest-first. The dates therefore ascend with the LeetCode
number, which is what makes the ‹ prev / next › pager read 1 -> 2 -> 5 -> 7.
Identical timestamps would leave that ordering up to sort stability.

The LeetCode dates are randomly spread across 2022-2024 (generated once with a
fixed seed, then sorted) rather than clustered on the day they were written.
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
        "date": "2024-11-10T09:12:44",
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
        "algorithm": "Graph Theory",
        "title": "LeetCode 200 – Number of Islands",
        "file": "200-number-of-islands.html",
        "date": "2024-11-19T07:23:20",
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
        "algorithm": "Sorting",
        "title": "LeetCode 347 – Top K Frequent Elements",
        "file": "347-top-k-frequent-elements.html",
        "date": "2024-12-13T21:29:46",
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
        "date": "2024-12-28T03:27:23",
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
