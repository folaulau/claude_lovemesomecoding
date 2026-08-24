"""Extract every Python code block from the round-1 posts and exercise it.

The blocks are pulled straight out of the published HTML, so this tests what a
reader would copy, not a retyped copy of it.
"""
import html
import re
import sys
from pathlib import Path

POSTS = Path("/Users/folaukaveinga/Github/claude_lovemesomecoding/projects/leetcode/posts")
PY = re.compile(r'<pre class="language-python"><code class="language-python">(.*?)</code></pre>', re.S)


def blocks(name):
    raw = (POSTS / name).read_text()
    return [html.unescape(b) for b in PY.findall(raw)]


def load_fn(name, fn):
    """Legacy posts expose module-level functions, not a Solution class."""
    ns = {}
    exec(compile("\n".join(blocks(name)), name, "exec"), ns)
    return ns[fn]


def load(name, extra="", only=None):
    """`only` picks specific blocks by index, for posts that show more than one
    complete `class Solution` -- otherwise the later one silently wins."""
    ns = {}
    chosen = blocks(name) if only is None else [blocks(name)[i] for i in only]
    src = extra + "\n" + "\n".join(chosen)
    exec(compile(src, name, "exec"), ns)
    return ns["Solution"]()


LISTNODE = """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

def to_list(xs):
    head = tail = ListNode(0)
    for x in xs:
        tail.next = ListNode(x); tail = tail.next
    return head.next

def to_arr(node):
    out = []
    while node:
        out.append(node.val); node = node.next
    return out
"""

fails = []


def check(label, got, want):
    if got != want:
        fails.append(f"{label}: got {got!r}, want {want!r}")
    print(f"  {'ok ' if got == want else 'FAIL'} {label}: {got!r}")


print("LeetCode 1 - Two Sum")
s = load("001-two-sum.html")
check("[2,7,11,15] t=9", s.twoSum([2, 7, 11, 15], 9), [0, 1])
check("[3,2,4] t=6", s.twoSum([3, 2, 4], 6), [1, 2])
check("[3,3] t=6 (duplicates)", s.twoSum([3, 3], 6), [0, 1])
check("[0,4,3,0] t=0", s.twoSum([0, 4, 3, 0], 0), [0, 3])
check("[-1,-2,-3,-4] t=-6", s.twoSum([-1, -2, -3, -4], -6), [1, 3])

print("LeetCode 2 - Add Two Numbers")
ns = {}
exec(compile(LISTNODE + "\n" + "\n".join(blocks("002-add-two-numbers.html")), "2", "exec"), ns)
s = ns["Solution"]()
check("342+465", ns["to_arr"](s.addTwoNumbers(ns["to_list"]([2, 4, 3]), ns["to_list"]([5, 6, 4]))), [7, 0, 8])
check("999+1 (carry grows)", ns["to_arr"](s.addTwoNumbers(ns["to_list"]([9, 9, 9]), ns["to_list"]([1]))), [0, 0, 0, 1])
check("0+0", ns["to_arr"](s.addTwoNumbers(ns["to_list"]([0]), ns["to_list"]([0]))), [0])
check("uneven lengths", ns["to_arr"](s.addTwoNumbers(ns["to_list"]([9, 9, 9, 9, 9, 9, 9]), ns["to_list"]([9, 9, 9, 9]))), [8, 9, 9, 9, 0, 0, 0, 1])

print("LeetCode 5 - Longest Palindromic Substring")
s = load("005-longest-palindromic-substring.html")
check("babad", s.longestPalindrome("babad") in ("bab", "aba"), True)
check("cbbd (even centre)", s.longestPalindrome("cbbd"), "bb")
check("abcdzdcab", s.longestPalindrome("abcdzdcab"), "cdzdc")
check("a", s.longestPalindrome("a"), "a")
check("'' (empty)", s.longestPalindrome(""), "")
check("ac", s.longestPalindrome("ac") in ("a", "c"), True)
check("aaaa", s.longestPalindrome("aaaa"), "aaaa")
s.longestPalindrome("aaaa")   # no instance state: a second call must not go stale
check("reused instance", s.longestPalindrome("cbbd"), "bb")

print("LeetCode 7 - Reverse Integer")
s = load("007-reverse-integer.html")
check("123", s.reverse(123), 321)
check("-123", s.reverse(-123), -321)
check("120 (trailing zero)", s.reverse(120), 21)
check("0", s.reverse(0), 0)
check("1534236469 (overflows)", s.reverse(1534236469), 0)
check("-2147483648 (INT_MIN)", s.reverse(-2147483648), 0)
check("-2147483412", s.reverse(-2147483412), -2143847412)

print("LeetCode 8 - atoi")
s = load("008-string-to-integer-atoi.html")
check('"42"', s.myAtoi("42"), 42)
check('"   -42"', s.myAtoi("   -42"), -42)
check('"4193 with words"', s.myAtoi("4193 with words"), 4193)
check('"words and 987"', s.myAtoi("words and 987"), 0)
check('"-91283472332" (clamps)', s.myAtoi("-91283472332"), -2147483648)
check('"91283472332" (clamps)', s.myAtoi("91283472332"), 2147483647)
check('"+-12"', s.myAtoi("+-12"), 0)
check('"" (empty)', s.myAtoi(""), 0)
check('"   " (spaces only)', s.myAtoi("   "), 0)
check('"  0000123"', s.myAtoi("  0000123"), 123)
check('"\\t42" (tab is not space)', s.myAtoi("\t42"), 0)
check('"-2147483648" (exactly INT_MIN)', s.myAtoi("-2147483648"), -2147483648)
check('"2147483647" (exactly INT_MAX)', s.myAtoi("2147483647"), 2147483647)
check('"٣" (non-ASCII digit)', s.myAtoi("٣"), 0)
check('"+1"', s.myAtoi("+1"), 1)
check('"3.14"', s.myAtoi("3.14"), 3)

print("LeetCode 9 - Palindrome Number")
s = load("009-palindrome-number.html")
check("121", s.isPalindrome(121), True)
check("-121", s.isPalindrome(-121), False)
check("10 (trailing zero)", s.isPalindrome(10), False)
check("0", s.isPalindrome(0), True)
check("12321 (odd length)", s.isPalindrome(12321), True)
check("1221 (even length)", s.isPalindrome(1221), True)
check("1231", s.isPalindrome(1231), False)
check("2147483647", s.isPalindrome(2147483647), False)

print("LeetCode 10 - Regular Expression Matching")
s = load("010-regular-expression-matching.html")
check('"aa","a"', s.isMatch("aa", "a"), False)
check('"aa","a*"', s.isMatch("aa", "a*"), True)
check('"ab",".*"', s.isMatch("ab", ".*"), True)
check('"aab","c*a*b"', s.isMatch("aab", "c*a*b"), True)
check('"mississippi","mis*is*p*."', s.isMatch("mississippi", "mis*is*p*."), False)
check('"","a*" (empty vs x*)', s.isMatch("", "a*"), True)
check('"","a*b*"', s.isMatch("", "a*b*"), True)
check('"","."', s.isMatch("", "."), False)
check('"",""', s.isMatch("", ""), True)
check('"a",""', s.isMatch("a", ""), False)
check('"aaa","a*a"', s.isMatch("aaa", "a*a"), True)
check('"aaaaaaaaaaaaaaaaaaab","a*a*a*a*a*b" (pathological)',
      s.isMatch("aaaaaaaaaaaaaaaaaaab", "a*a*a*a*a*b"), True)

print("LeetCode 12 - Integer to Roman")
s = load("012-integer-to-roman.html")
check("3", s.intToRoman(3), "III")
check("4 (subtractive)", s.intToRoman(4), "IV")
check("9", s.intToRoman(9), "IX")
check("58", s.intToRoman(58), "LVIII")
check("1994 (CM XC IV)", s.intToRoman(1994), "MCMXCIV")
check("1 (min)", s.intToRoman(1), "I")
check("3999 (max)", s.intToRoman(3999), "MMMCMXCIX")
check("3888 (longest)", s.intToRoman(3888), "MMMDCCCLXXXVIII")
check("40", s.intToRoman(40), "XL")
check("400", s.intToRoman(400), "CD")
check("900", s.intToRoman(900), "CM")

print("LeetCode 13 - Roman to Integer")
s13 = load("013-roman-to-integer.html")
check("III", s13.romanToInt("III"), 3)
check("IV", s13.romanToInt("IV"), 4)
check("IX", s13.romanToInt("IX"), 9)
check("LVIII", s13.romanToInt("LVIII"), 58)
check("MCMXCIV", s13.romanToInt("MCMXCIV"), 1994)
check("MMMCMXCIX (max)", s13.romanToInt("MMMCMXCIX"), 3999)
check("I (min)", s13.romanToInt("I"), 1)
# 12 and 13 must be exact inverses across the whole valid range.
roundtrip = [n for n in range(1, 4000) if s13.romanToInt(s.intToRoman(n)) != n]
check("12 <-> 13 round-trip, all 1..3999", roundtrip, [])

print("LeetCode 14 - Longest Common Prefix")
s = load("014-longest-common-prefix.html")
check("flower/flow/flight", s.longestCommonPrefix(["flower", "flow", "flight"]), "fl")
check("dog/racecar/car (none)", s.longestCommonPrefix(["dog", "racecar", "car"]), "")
check("interspecies/...", s.longestCommonPrefix(["interspecies", "interstellar", "interstate"]), "inters")
check("single string", s.longestCommonPrefix(["a"]), "a")
check("empty array", s.longestCommonPrefix([]), "")
check("empty string present", s.longestCommonPrefix(["ab", ""]), "")
check("shorter is the prefix", s.longestCommonPrefix(["flow", "flower"]), "flow")
check("all identical", s.longestCommonPrefix(["abc", "abc"]), "abc")
check("mismatch at column 0", s.longestCommonPrefix(["a", "b"]), "")

print("LeetCode 15 - 3Sum")
s = load("015-3sum.html")
def norm(r):
    return sorted(tuple(t) for t in r)
check("[-1,0,1,2,-1,-4]", norm(s.threeSum([-1, 0, 1, 2, -1, -4])), norm([[-1, -1, 2], [-1, 0, 1]]))
check("[0,1,1] (no answer)", s.threeSum([0, 1, 1]), [])
check("[0,0,0]", norm(s.threeSum([0, 0, 0])), [(0, 0, 0)])
check("[0,0,0,0] (dup guard)", norm(s.threeSum([0, 0, 0, 0])), [(0, 0, 0)])
check("[-2,0,0,2,2] (inner dup)", norm(s.threeSum([-2, 0, 0, 2, 2])), [(-2, 0, 2)])
check("[] (empty)", s.threeSum([]), [])
check("[1,2] (too short)", s.threeSum([1, 2]), [])
check("all positive (early break)", s.threeSum([1, 2, 3, 4]), [])
check("[-1,-1,-1,2] ", norm(s.threeSum([-1, -1, -1, 2])), [(-1, -1, 2)])

print("LeetCode 19 - Remove Nth Node From End")
ns = {}
exec(compile(LISTNODE + "\n" + "\n".join(blocks("019-remove-nth-node-from-end-of-list.html")), "19", "exec"), ns)
s = ns["Solution"]()
tl, ta = ns["to_list"], ns["to_arr"]
check("1..5, n=2", ta(s.removeNthFromEnd(tl([1, 2, 3, 4, 5]), 2)), [1, 2, 3, 5])
check("[1], n=1 (empties list)", ta(s.removeNthFromEnd(tl([1]), 1)), [])
check("[1,2], n=2 (removes head)", ta(s.removeNthFromEnd(tl([1, 2]), 2)), [2])
check("[1,2], n=1 (removes tail)", ta(s.removeNthFromEnd(tl([1, 2]), 1)), [1])
check("1..5, n=5 (removes head)", ta(s.removeNthFromEnd(tl([1, 2, 3, 4, 5]), 5)), [2, 3, 4, 5])
check("1..5, n=1 (removes tail)", ta(s.removeNthFromEnd(tl([1, 2, 3, 4, 5]), 1)), [1, 2, 3, 4])

print("LeetCode 20 - Valid Parentheses")
s = load("020-valid-parentheses.html")
check("()", s.isValid("()"), True)
check("()[]{}", s.isValid("()[]{}"), True)
check("{[()]}", s.isValid("{[()]}"), True)
check("(] (wrong type)", s.isValid("(]"), False)
check("([)] (interleaved)", s.isValid("([)]"), False)
check("( (never closed)", s.isValid("("), False)
check(")( (closes nothing)", s.isValid(")("), False)
check("'' (empty)", s.isValid(""), True)
check("]", s.isValid("]"), False)
check("((((", s.isValid("(((("), False)
check("(((())))", s.isValid("(((())))"), True)

print("LeetCode 21 - Merge Two Sorted Lists")
ns = {}
exec(compile(LISTNODE + "\n" + "\n".join(blocks("021-merge-two-sorted-lists.html")), "21", "exec"), ns)
s = ns["Solution"]()
tl, ta = ns["to_list"], ns["to_arr"]
check("[1,2,4] + [1,3,4]", ta(s.mergeTwoLists(tl([1, 2, 4]), tl([1, 3, 4]))), [1, 1, 2, 3, 4, 4])
check("both empty", ta(s.mergeTwoLists(None, None)), [])
check("empty + [0]", ta(s.mergeTwoLists(None, tl([0]))), [0])
check("[0] + empty", ta(s.mergeTwoLists(tl([0]), None)), [0])
check("disjoint, l1 first", ta(s.mergeTwoLists(tl([1, 2]), tl([3, 4]))), [1, 2, 3, 4])
check("disjoint, l2 first", ta(s.mergeTwoLists(tl([3, 4]), tl([1, 2]))), [1, 2, 3, 4])
check("all equal", ta(s.mergeTwoLists(tl([2, 2]), tl([2, 2]))), [2, 2, 2, 2])
check("very uneven", ta(s.mergeTwoLists(tl([1]), tl([2, 3, 4, 5]))), [1, 2, 3, 4, 5])

print("LeetCode 22 - Generate Parentheses")
s = load("022-generate-parentheses.html")
def valid(x):
    d = 0
    for c in x:
        d += 1 if c == "(" else -1
        if d < 0:
            return False
    return d == 0
CATALAN = [1, 1, 2, 5, 14, 42, 132, 429, 1430]
check("n=1", sorted(s.generateParenthesis(1)), ["()"])
check("n=3", sorted(s.generateParenthesis(3)),
      sorted(["((()))", "(()())", "(())()", "()(())", "()()()"]))
for n in range(1, 9):
    got = s.generateParenthesis(n)
    check(f"n={n}: count is Catalan({n})", len(got), CATALAN[n])
    check(f"n={n}: all unique", len(set(got)), CATALAN[n])
    check(f"n={n}: all well-formed and length 2n",
          all(valid(x) and len(x) == 2 * n for x in got), True)

print("LeetCode 23 - Merge k Sorted Lists")
ns = {}
exec(compile(LISTNODE + "\n" + "\n".join(blocks("023-merge-k-sorted-lists.html")), "23", "exec"), ns)
s = ns["Solution"]()
tl, ta = ns["to_list"], ns["to_arr"]
check("3 lists", ta(s.mergeKLists([tl([1, 4, 5]), tl([1, 3, 4]), tl([2, 6])])),
      [1, 1, 2, 3, 4, 4, 5, 6])
check("empty array", ta(s.mergeKLists([])), [])
check("[None] (null entry)", ta(s.mergeKLists([None])), [])
check("nulls around a real list", ta(s.mergeKLists([None, tl([1, 2]), None])), [1, 2])
check("all null", ta(s.mergeKLists([None, None, None])), [])
check("single list", ta(s.mergeKLists([tl([1, 2, 3])])), [1, 2, 3])
check("two lists", ta(s.mergeKLists([tl([2]), tl([1])])), [1, 2])
check("negatives", ta(s.mergeKLists([tl([2, 4]), None, tl([-1])])), [-1, 2, 4])
big = [tl(list(range(i, 40, 7))) for i in range(7)]
check("7 interleaved lists", ta(s.mergeKLists(big)), sorted(range(40)))

print("LeetCode 28 - Implement strStr")
s = load("028-implement-strstr.html")
check('"sadbutsad","sad"', s.strStr("sadbutsad", "sad"), 0)
check('"leetcode","leeto"', s.strStr("leetcode", "leeto"), -1)
check('"hello","" (empty needle)', s.strStr("hello", ""), 0)
check('"a","aaaa" (needle longer)', s.strStr("a", "aaaa"), -1)
check('"mississippi","issip"', s.strStr("mississippi", "issip"), 4)
check('"abc","abc" (exact, bound test)', s.strStr("abc", "abc"), 0)
check('"aaaaaaaaab","aaab" (worst case)', s.strStr("aaaaaaaaab", "aaab"), 6)
check('"","" (both empty)', s.strStr("", ""), 0)
check('"","a"', s.strStr("", "a"), -1)
check('"abc","c" (last position)', s.strStr("abc", "c"), 2)
# Cross-check against str.find over a brute-force space.
import itertools
mismatch = [(h, nd) for h in ("".join(p) for r in range(5) for p in itertools.product("ab", repeat=r))
            for nd in ("a", "b", "ab", "ba", "aab", "abab")
            if s.strStr(h, nd) != h.find(nd)]
check("agrees with str.find on all a/b strings up to length 4", mismatch, [])

print("LeetCode 31 - Next Permutation")
s = load("031-next-permutation.html")
def nxt(xs):
    xs = list(xs)
    s.nextPermutation(xs)
    return xs
check("[1,2,3]", nxt([1, 2, 3]), [1, 3, 2])
check("[1,3,2]", nxt([1, 3, 2]), [2, 1, 3])
check("[3,2,1] (wraps)", nxt([3, 2, 1]), [1, 2, 3])
check("[1,1,5] (duplicates)", nxt([1, 1, 5]), [1, 5, 1])
check("[1] (single)", nxt([1]), [1])
check("[2,2,2] (all equal)", nxt([2, 2, 2]), [2, 2, 2])
check("[1,5,8,4,7,6,5,3,1]", nxt([1, 5, 8, 4, 7, 6, 5, 3, 1]), [1, 5, 8, 5, 1, 3, 4, 6, 7])
check("[] (empty)", nxt([]), [])
# Exhaustive: walking next-permutation through every arrangement of 1..6 must
# reproduce exactly the lexicographic order, then wrap to the first.
import itertools
perms = sorted(itertools.permutations(range(1, 7)))
walked = all(nxt(perms[i]) == list(perms[(i + 1) % len(perms)]) for i in range(len(perms)))
check(f"walks all {len(perms)} permutations of 1..6 in order, and wraps", walked, True)
# With duplicates too.
dperms = sorted(set(itertools.permutations([1, 1, 2, 2, 3])))
dwalk = all(nxt(dperms[i]) == list(dperms[(i + 1) % len(dperms)]) for i in range(len(dperms)))
check(f"walks all {len(dperms)} distinct permutations of [1,1,2,2,3]", dwalk, True)

print("LeetCode 33 - Search in Rotated Sorted Array")
s = load("033-search-in-rotated-sorted-array.html")
check("[4,5,6,7,0,1,2] t=0", s.search([4, 5, 6, 7, 0, 1, 2], 0), 4)
check("[4,5,6,7,0,1,2] t=3 (absent)", s.search([4, 5, 6, 7, 0, 1, 2], 3), -1)
check("[1] t=0", s.search([1], 0), -1)
check("[1] t=1", s.search([1], 1), 0)
check("[3,1] t=1", s.search([3, 1], 1), 1)
check("[] (empty)", s.search([], 5), -1)
check("[1,2,3] unrotated t=3", s.search([1, 2, 3], 3), 2)
# Exhaustive over every rotation of every size up to 8, every target in range.
bad = []
for n in range(1, 9):
    base = list(range(n))
    for r in range(n):
        arr = base[r:] + base[:r]
        for t_ in range(-1, n + 1):
            want = arr.index(t_) if t_ in arr else -1
            if s.search(arr, t_) != want:
                bad.append((arr, t_))
check("exhaustive: all rotations of size 1..8, all targets", bad, [])

print("LeetCode 34 - Find First and Last Position")
s = load("034-find-first-and-last-position.html")
check("[5,7,7,8,8,10] t=8", s.searchRange([5, 7, 7, 8, 8, 10], 8), [3, 4])
check("[5,7,7,8,8,10] t=6 (absent)", s.searchRange([5, 7, 7, 8, 8, 10], 6), [-1, -1])
check("[] (empty)", s.searchRange([], 0), [-1, -1])
check("[1,1,1,1,1] t=1 (all same)", s.searchRange([1, 1, 1, 1, 1], 1), [0, 4])
check("[1] t=1", s.searchRange([1], 1), [0, 0])
check("[2,2] t=1 (below all)", s.searchRange([2, 2], 1), [-1, -1])
check("[2,2] t=3 (above all)", s.searchRange([2, 2], 3), [-1, -1])
bad = []
for n in range(0, 9):
    for arr in set(tuple(sorted(c)) for c in itertools.product(range(4), repeat=n)):
        for t_ in range(-1, 5):
            xs = list(arr)
            want = [xs.index(t_), len(xs) - 1 - xs[::-1].index(t_)] if t_ in xs else [-1, -1]
            if s.searchRange(xs, t_) != want:
                bad.append((xs, t_))
check("exhaustive: all sorted arrays over 0..3 up to length 8", bad, [])

print("LeetCode 36 - Valid Sudoku")
s = load("036-valid-sudoku.html")
GOOD = [["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]]
BAD = [r[:] for r in GOOD]
BAD[0][0] = "8"          # duplicate 8 in the top-left box
check("valid board", s.isValidSudoku([r[:] for r in GOOD]), True)
check("duplicate in box", s.isValidSudoku([r[:] for r in BAD]), False)
empty = [["." for _ in range(9)] for _ in range(9)]
check("all empty (dots must not clash)", s.isValidSudoku([r[:] for r in empty]), True)
rowdup = [r[:] for r in empty]; rowdup[0][0] = rowdup[0][8] = "1"
check("duplicate in row", s.isValidSudoku(rowdup), False)
coldup = [r[:] for r in empty]; coldup[0][0] = coldup[8][0] = "1"
check("duplicate in column", s.isValidSudoku(coldup), False)
boxdup = [r[:] for r in empty]; boxdup[0][0] = boxdup[2][2] = "1"
check("duplicate in box only", s.isValidSudoku(boxdup), False)
ok = [r[:] for r in empty]; ok[0][0] = ok[3][3] = "1"
check("same digit, different row/col/box", s.isValidSudoku(ok), True)
ok2 = [r[:] for r in empty]; ok2[0][3] = ok2[1][0] = "1"
check("same digit, adjacent boxes", s.isValidSudoku(ok2), True)

print("LeetCode 39 - Combination Sum")
s39 = load("039-combination-sum.html")
def nrm(r):
    return sorted(tuple(sorted(x)) for x in r)
check("[2,3,6,7] t=7", nrm(s39.combinationSum([2, 3, 6, 7], 7)), nrm([[2, 2, 3], [7]]))
check("[2,3,5] t=8", nrm(s39.combinationSum([2, 3, 5], 8)), nrm([[2, 2, 2, 2], [2, 3, 3], [3, 5]]))
check("[2] t=1 (unreachable)", s39.combinationSum([2], 1), [])
check("[1] t=2 (reuse)", nrm(s39.combinationSum([1], 2)), [(1, 1)])
check("[8,7,4,3] t=11 (unsorted input)", nrm(s39.combinationSum([8, 7, 4, 3], 11)),
      nrm([[3, 4, 4], [3, 8], [4, 7]]))
check("no duplicate combinations", len(s39.combinationSum([2, 3, 5], 20)),
      len(set(nrm(s39.combinationSum([2, 3, 5], 20)))))

print("LeetCode 40 - Combination Sum II")
s40 = load("040-combination-sum-ii.html")
check("[10,1,2,7,6,1,5] t=8", nrm(s40.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8)),
      nrm([[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]))
check("[2,5,2,1,2] t=5", nrm(s40.combinationSum2([2, 5, 2, 1, 2], 5)), nrm([[1, 2, 2], [5]]))
check("[1,1] t=2 (both 1s usable)", nrm(s40.combinationSum2([1, 1], 2)), [(1, 1)])
check("[1,1,1] t=1 (reported once)", nrm(s40.combinationSum2([1, 1, 1], 1)), [(1,)])
check("[2] t=1 (unreachable)", s40.combinationSum2([2], 1), [])
# Cross-check against brute force over every subset, deduplicated.
bad = []
for cand in ([1, 1, 2, 2, 3], [2, 3, 6, 7], [1, 1, 1, 1], [4, 4, 2, 1, 4, 2, 2, 1, 3]):
    for t_ in range(1, 10):
        want = set()
        for r in range(1, len(cand) + 1):
            for combo in itertools.combinations(cand, r):
                if sum(combo) == t_:
                    want.add(tuple(sorted(combo)))
        if set(nrm(s40.combinationSum2(list(cand), t_))) != want:
            bad.append((cand, t_))
check("agrees with brute-force subset enumeration", bad, [])

print("LeetCode 121 - Best Time to Buy and Sell Stock")
s = load("121-best-time-to-buy-and-sell-stock.html")
check("[7,1,5,3,6,4]", s.maxProfit([7, 1, 5, 3, 6, 4]), 5)
check("[7,6,4,3,1] (falling -> 0)", s.maxProfit([7, 6, 4, 3, 1]), 0)
check("[1,2]", s.maxProfit([1, 2]), 1)
check("[5] (single day)", s.maxProfit([5]), 0)
check("[] (empty)", s.maxProfit([]), 0)
check("[2,2,2] (flat)", s.maxProfit([2, 2, 2]), 0)
check("[3,2,6,5,0,3]", s.maxProfit([3, 2, 6, 5, 0, 3]), 4)
# Cross-check against the O(n^2) definition on every short sequence over 0..3.
bad = []
for n in range(0, 7):
    for combo in itertools.product(range(4), repeat=n):
        xs = list(combo)
        want = max([xs[j] - xs[i] for i in range(n) for j in range(i + 1, n)] + [0])
        if s.maxProfit(xs) != want:
            bad.append(xs)
check("agrees with brute force on all sequences over 0..3 up to length 6", bad, [])

print("LeetCode 200 - Number of Islands")
s = load("200-number-of-islands.html")
def g(rows):
    return [list(r) for r in rows]
check("one island", s.numIslands(g(["11110", "11010", "11000", "00000"])), 1)
check("three islands", s.numIslands(g(["11000", "11000", "00100", "00011"])), 3)
check("all water", s.numIslands(g(["000", "000"])), 0)
check("all land", s.numIslands(g(["111", "111"])), 1)
check("single cell land", s.numIslands(g(["1"])), 1)
check("[] (empty grid)", s.numIslands([]), 0)
check("diagonal is NOT connected", s.numIslands(g(["10", "01"])), 2)
check("checkerboard", s.numIslands(g(["101", "010", "101"])), 5)
check("single column", s.numIslands(g(["1", "0", "1"])), 2)
check("snake (one long island)", s.numIslands(g(["1111", "0001", "1111", "1000"])), 1)

print("LeetCode 347 - Top K Frequent Elements")
s = load("347-top-k-frequent-elements.html")
check("[1,1,1,2,2,3] k=2", sorted(s.topKFrequent([1, 1, 1, 2, 2, 3], 2)), [1, 2])
check("[1] k=1", s.topKFrequent([1], 1), [1])
check("[1,2] k=2 (tie)", sorted(s.topKFrequent([1, 2], 2)), [1, 2])
check("all unique k=1", len(s.topKFrequent([1, 2, 3, 4, 5], 1)), 1)
check("k=1 with a tie returns exactly 1", len(s.topKFrequent([1, 1, 2, 2], 1)), 1)
check("all same value", sorted(s.topKFrequent([4, 4, 4, 4], 1)), [4])
check("negatives", sorted(s.topKFrequent([-1, -1, -2, -2, -2, 3], 2)), [-2, -1])
# The returned k values must be a valid top-k by frequency, for random-ish inputs.
bad = []
for xs in ([1,1,2,2,3], [5,5,5,4,4,3,2,1], [7], [0,0,1,1,2,2,3], list(range(10)) + [3, 3]):
    freq = {}
    for x in xs:
        freq[x] = freq.get(x, 0) + 1
    for k in range(1, len(freq) + 1):
        got = s.topKFrequent(list(xs), k)
        counts = sorted((freq[v] for v in got), reverse=True)
        want = sorted(freq.values(), reverse=True)[:k]
        if len(got) != k or len(set(got)) != k or counts != want:
            bad.append((xs, k, got))
check("returns exactly k distinct values with a valid top-k frequency profile", bad, [])

print("LeetCode 543 - Diameter of Binary Tree")
TREE = """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build(xs):
    '''LeetCode level-order list, None for a missing child.'''
    if not xs or xs[0] is None:
        return None
    root = TreeNode(xs[0])
    q, i = [root], 1
    while q and i < len(xs):
        node = q.pop(0)
        if i < len(xs):
            v = xs[i]; i += 1
            if v is not None:
                node.left = TreeNode(v); q.append(node.left)
        if i < len(xs):
            v = xs[i]; i += 1
            if v is not None:
                node.right = TreeNode(v); q.append(node.right)
    return root
"""
ns = {}
exec(compile(TREE + "\n" + "\n".join(blocks("543-diameter-of-binary-tree.html")), "543", "exec"), ns)
s = ns["Solution"]()
build = ns["build"]
check("[1,2,3,4,5]", s.diameterOfBinaryTree(build([1, 2, 3, 4, 5])), 3)
check("[1,2]", s.diameterOfBinaryTree(build([1, 2])), 1)
check("[1] (single node)", s.diameterOfBinaryTree(build([1])), 0)
check("None (empty tree)", s.diameterOfBinaryTree(None), 0)
# A left-leaning chain of 5 nodes: diameter is 4 edges, and never touches a right child.
chain = ns["TreeNode"](1)
node = chain
for v in range(2, 6):
    node.left = ns["TreeNode"](v)
    node = node.left
check("left chain of 5 (diameter misses the root's right side)", s.diameterOfBinaryTree(chain), 4)
check("reused instance", s.diameterOfBinaryTree(build([1, 2])), 1)
# Balanced tree of 7 nodes: longest path is leaf-up-to-root-down-to-leaf = 4 edges.
check("full tree of 7", s.diameterOfBinaryTree(build([1, 2, 3, 4, 5, 6, 7])), 4)
# The diameter here is 5-3-2-4-6 (4 edges), entirely inside the left subtree.
# Through the root it would only be 3, so this fails any root-only solution.
#       1
#      /
#     2
#    / \
#   3   4
#  /     \
# 5       6
deep = build([1, 2, None, 3, 4, 5, None, None, 6])
check("diameter buried in the left subtree, not through the root",
      s.diameterOfBinaryTree(deep), 4)

print("Legacy - Two Number Sum")
f = load_fn("legacy-two-number-sum.html", "two_number_sum")
check("[3,5,-4,8,11,1,-1,6] t=10", sorted(f([3, 5, -4, 8, 11, 1, -1, 6], 10)), [-1, 11])
check("[4,6] t=10", sorted(f([4, 6], 10)), [4, 6])
check("[4,6] t=11 (no pair)", f([4, 6], 11), [])
check("[3] t=6 (cannot pair with itself)", f([3], 6), [])
check("[] (empty)", f([], 0), [])
check("[5,1] t=10 (5+5 must NOT match)", f([5, 1], 10), [])
check("negatives only", sorted(f([-3, -7, -2], -9)), [-7, -2])
# Cross-check against brute force over every distinct-value array up to length 6.
bad = []
for n in range(0, 7):
    for combo in itertools.combinations(range(-3, 4), n):
        xs = list(combo)
        for t_ in range(-6, 7):
            want = any(xs[i] + xs[j] == t_ for i in range(n) for j in range(i + 1, n))
            got = f(list(xs), t_)
            ok = (len(got) == 2 and got[0] + got[1] == t_ and sorted(got) != []) if want else got == []
            if not ok:
                bad.append((xs, t_, got))
check("agrees with brute force on all distinct arrays over -3..3", bad, [])

print("Legacy - Three Number Sum")
f3 = load_fn("legacy-three-number-sum.html", "three_number_sum")
check("[12,3,1,2,-6,5,-8,6] t=0", f3([12, 3, 1, 2, -6, 5, -8, 6], 0),
      [[-8, 2, 6], [-8, 3, 5], [-6, 1, 5]])
check("[1,2,3] t=100 (none)", f3([1, 2, 3], 100), [])
check("[1,2] t=3 (too short)", f3([1, 2], 3), [])
check("[] (empty)", f3([], 0), [])
check("[1,2,3] t=6", f3([1, 2, 3], 6), [[1, 2, 3]])
check("output triplets are ascending", f3([5, 1, 3], 9), [[1, 3, 5]])
# Cross-check against brute force, and confirm the documented ordering guarantees.
bad = []
for n in range(0, 8):
    for combo in itertools.combinations(range(-4, 5), n):
        xs = list(combo)
        for t_ in (-3, 0, 3):
            want = sorted([sorted(c) for c in itertools.combinations(xs, 3) if sum(c) == t_])
            got = f3(list(xs), t_)
            if got != want:
                bad.append((xs, t_, got, want))
check("agrees with brute force, in ascending order, on all distinct arrays over -4..4", bad, [])

print("LeetCode 41 - First Missing Positive")
s = load("041-first-missing-positive.html")
def fmp(xs):
    return s.firstMissingPositive(list(xs))
check("[1,2,0]", fmp([1, 2, 0]), 3)
check("[3,4,-1,1]", fmp([3, 4, -1, 1]), 2)
check("[7,8,9,11,12]", fmp([7, 8, 9, 11, 12]), 1)
check("[1,2,3] (answer past the end)", fmp([1, 2, 3]), 4)
check("[] (empty)", fmp([]), 1)
check("[1,1] (duplicate guard, must terminate)", fmp([1, 1]), 2)
check("[2,2,2]", fmp([2, 2, 2]), 1)
check("[-1,-2]", fmp([-1, -2]), 1)
check("[1]", fmp([1]), 2)
bad = []
for n in range(0, 7):
    for combo in itertools.product(range(-2, 6), repeat=n):
        xs = list(combo)
        want = next(v for v in itertools.count(1) if v not in xs)
        if fmp(xs) != want:
            bad.append((xs, fmp(xs), want))
            break
    if bad:
        break
check("exhaustive over values -2..5, lengths 0..6", bad, [])

print("LeetCode 42 - Trapping Rain Water")
s = load("042-trapping-rain-water.html")
check("[0,1,0,2,1,0,1,3,2,1,2,1]", s.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), 6)
check("[4,2,0,3,2,5]", s.trap([4, 2, 0, 3, 2, 5]), 9)
check("[] (empty)", s.trap([]), 0)
check("[3] (single)", s.trap([3]), 0)
check("[1,2,3,4] (increasing)", s.trap([1, 2, 3, 4]), 0)
check("[4,3,2,1] (decreasing)", s.trap([4, 3, 2, 1]), 0)
check("[2,2,2] (flat)", s.trap([2, 2, 2]), 0)
check("[5,0,5]", s.trap([5, 0, 5]), 5)
# Cross-check against the min(maxLeft, maxRight) definition on every short profile.
bad = []
for n in range(0, 8):
    for combo in itertools.product(range(4), repeat=n):
        xs = list(combo)
        want = sum(min(max(xs[:i + 1]), max(xs[i:])) - xs[i] for i in range(n))
        if s.trap(xs) != want:
            bad.append((xs, want))
check("agrees with the per-column formula on all profiles over 0..3 up to length 7", bad, [])

print("LeetCode 43 - Multiply Strings")
s = load("043-multiply-strings.html")
check('"2" x "3"', s.multiply("2", "3"), "6")
check('"123" x "456"', s.multiply("123", "456"), "56088")
check('"0" x "52" (must be "0")', s.multiply("0", "52"), "0")
check('"52" x "0"', s.multiply("52", "0"), "0")
check('"0" x "0"', s.multiply("0", "0"), "0")
check('"11" x "11" (m+n-1 digits)', s.multiply("11", "11"), "121")
check('"99" x "99"', s.multiply("99", "99"), "9801")
check('"101" x "101" (interior zeros)', s.multiply("101", "101"), "10201")
big1, big2 = "9" * 60, "9" * 60
check("60 digits x 60 digits", s.multiply(big1, big2), str(int(big1) * int(big2)))
bad = [(a, b) for a in range(0, 60) for b in range(0, 60)
       if s.multiply(str(a), str(b)) != str(a * b)]
check("agrees with integer multiplication for all a,b in 0..59", bad, [])

print("LeetCode 46 - Permutations")
s = load("046-permutations.html")
def nrm2(r):
    return sorted(tuple(x) for x in r)
check("[1,2,3]", nrm2(s.permute([1, 2, 3])),
      nrm2([[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]))
check("[0,1]", nrm2(s.permute([0, 1])), nrm2([[0,1],[1,0]]))
check("[1] (single)", s.permute([1]), [[1]])
check("[] (empty yields one empty permutation)", s.permute([]), [[]])
for n in range(1, 7):
    got = s.permute(list(range(n)))
    fact = 1
    for k in range(2, n + 1):
        fact *= k
    check(f"n={n}: exactly {fact} distinct permutations", (len(got), len(set(map(tuple, got)))), (fact, fact))
    check(f"n={n}: matches itertools.permutations",
          nrm2(got) == sorted(itertools.permutations(range(n))), True)

print("LeetCode 47 - Permutations II")
s = load("047-permutations-ii.html")
check("[1,1,2]", nrm2(s.permuteUnique([1, 1, 2])), nrm2([[1,1,2],[1,2,1],[2,1,1]]))
check("[1,2,3] (all distinct)", len(s.permuteUnique([1, 2, 3])), 6)
check("[2,2,2] (exactly one)", s.permuteUnique([2, 2, 2]), [[2, 2, 2]])
check("[1] (single)", s.permuteUnique([1]), [[1]])
check("[] (empty)", s.permuteUnique([]), [[]])
bad = []
for n in range(0, 7):
    for combo in itertools.product([1, 1, 2, 3], repeat=n):
        xs = list(combo)
        want = sorted(set(itertools.permutations(xs)))
        got = s.permuteUnique(list(xs))
        if nrm2(got) != want or len(got) != len(want):
            bad.append((xs, got))
check("matches set(itertools.permutations) on every multiset over {1,1,2,3}", bad, [])

print("LeetCode 49 - Group Anagrams")
s = load("049-group-anagrams.html")
def grp(r):
    return sorted(sorted(g) for g in r)
check("eat/tea/tan/ate/nat/bat", grp(s.groupAnagrams(["eat","tea","tan","ate","nat","bat"])),
      grp([["eat","tea","ate"], ["tan","nat"], ["bat"]]))
check('[""] (empty string)', s.groupAnagrams([""]), [[""]])
check('["a"]', s.groupAnagrams(["a"]), [["a"]])
check("[] (empty input)", s.groupAnagrams([]), [])
check("no anagrams at all", grp(s.groupAnagrams(["abc","def","ghi"])),
      grp([["abc"],["def"],["ghi"]]))
# The double-digit-count collision the post warns about: 1 a + 11 b vs 11 a + 1 b.
w1, w2 = "a" + "b" * 11, "a" * 11 + "b"
check("1a+11b must NOT group with 11a+1b", grp(s.groupAnagrams([w1, w2])), grp([[w1], [w2]]))
check("genuine anagrams of those still group", len(s.groupAnagrams([w1, w1[::-1]])), 1)
# Cross-check grouping against sorted-string equivalence.
bad = []
for words in (["ab","ba","abc","cab","bca","x"], ["", "", "a"], ["aa","aa","a"]):
    want = {}
    for w in words:
        want.setdefault("".join(sorted(w)), []).append(w)
    if grp(s.groupAnagrams(list(words))) != grp(want.values()):
        bad.append(words)
check("grouping agrees with sorted-string equivalence", bad, [])

print("LeetCode 51 - N-Queens")
s = load("051-n-queens.html")
def legal(board):
    """Independent validator: re-derive the queen positions and check every pair."""
    n = len(board)
    pos = []
    for r, row in enumerate(board):
        if len(row) != n or row.count("Q") != 1 or row.count(".") != n - 1:
            return False
        pos.append((r, row.index("Q")))
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            (r1, c1), (r2, c2) = pos[i], pos[j]
            if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                return False
    return True

check("n=1", s.solveNQueens(1), [["Q"]])
check("n=2 (no solutions, not an error)", s.solveNQueens(2), [])
check("n=3 (no solutions)", s.solveNQueens(3), [])
check("n=4 exact boards", sorted(map(tuple, s.solveNQueens(4))),
      sorted([tuple([".Q..", "...Q", "Q...", "..Q."]),
              tuple(["..Q.", "Q...", "...Q", ".Q.."])]))
# The known solution counts for n = 1..9.
COUNTS = [1, 0, 0, 2, 10, 4, 40, 92, 352]
for n, want in enumerate(COUNTS, start=1):
    got = s.solveNQueens(n)
    check(f"n={n}: {want} solutions", len(got), want)
    check(f"n={n}: every board is legal", all(legal(b) for b in got), True)
    check(f"n={n}: all boards distinct", len({tuple(b) for b in got}), want)
check("reusable: n=6 twice gives the same answer",
      s.solveNQueens(6) == s.solveNQueens(6), True)

print("LeetCode 52 - N-Queens II")
s52 = load("052-n-queens-ii.html")
for n, want in enumerate(COUNTS, start=1):
    check(f"n={n}", s52.totalNQueens(n), want)
check("agrees with problem 51 for n=1..8",
      [s52.totalNQueens(n) for n in range(1, 9)],
      [len(s.solveNQueens(n)) for n in range(1, 9)])
# The marks must be undone: a second call on the same object must not see stale state.
check("reusable: n=8 twice", (s52.totalNQueens(8), s52.totalNQueens(8)), (92, 92))

print("LeetCode 53 - Maximum Subarray")
s = load("053-maximum-subarray.html")
check("[-2,1,-3,4,-1,2,1,-5,4]", s.maxSubArray([-2,1,-3,4,-1,2,1,-5,4]), 6)
check("[1]", s.maxSubArray([1]), 1)
check("[5,4,-1,7,8]", s.maxSubArray([5,4,-1,7,8]), 23)
check("[-1] (single negative)", s.maxSubArray([-1]), -1)
check("[-3,-1,-2] (ALL negative: must not return 0)", s.maxSubArray([-3,-1,-2]), -1)
check("[-2,-1] (all negative, two elements)", s.maxSubArray([-2,-1]), -1)
check("[0]", s.maxSubArray([0]), 0)
check("[5,4,-1,7,8,-100] (run in progress is not the answer)",
      s.maxSubArray([5,4,-1,7,8,-100]), 23)
check("[-1,-2,-3,100]", s.maxSubArray([-1,-2,-3,100]), 100)
# Brute force over every subarray, on every small array over a mixed alphabet.
bad = []
for n in range(1, 8):
    for combo in itertools.product([-2, -1, 0, 1, 3], repeat=n):
        xs = list(combo)
        want = max(sum(xs[i:j]) for i in range(n) for j in range(i + 1, n + 1))
        if s.maxSubArray(list(xs)) != want:
            bad.append((xs, want))
check("matches brute force on every array of length 1..7 over {-2,-1,0,1,3}", bad, [])

print("LeetCode 55 - Jump Game")
s = load("055-jump-game.html")
check("[2,3,1,1,4]", s.canJump([2,3,1,1,4]), True)
check("[3,2,1,0,4] (index 3 is a dead end)", s.canJump([3,2,1,0,4]), False)
check("[0] (already at the last index)", s.canJump([0]), True)
check("[1,0]", s.canJump([1,0]), True)
check("[0,1]", s.canJump([0,1]), False)
check("[2,0,0]", s.canJump([2,0,0]), True)
check("[1,1,1,1,1]", s.canJump([1,1,1,1,1]), True)
check("[5,0,0,0,0,0]", s.canJump([5,0,0,0,0,0]), True)
# Brute force by explicit reachability, on every small array of jump lengths.
def reachable(xs):
    seen, stack = {0}, [0]
    while stack:
        i = stack.pop()
        for j in range(i + 1, min(i + xs[i], len(xs) - 1) + 1):
            if j not in seen:
                seen.add(j); stack.append(j)
    return len(xs) - 1 in seen

bad = []
for n in range(1, 8):
    for combo in itertools.product([0, 1, 2, 3], repeat=n):
        xs = list(combo)
        if s.canJump(list(xs)) != reachable(xs):
            bad.append(xs)
check("matches explicit reachability on every array of length 1..7 over {0,1,2,3}", bad, [])

print("LeetCode 56 - Merge Intervals")
s = load("056-merge-intervals.html")
def iv(r):
    return [list(x) for x in r]
check("[[1,3],[2,6],[8,10],[15,18]]",
      iv(s.merge([[1,3],[2,6],[8,10],[15,18]])), [[1,6],[8,10],[15,18]])
check("[[1,4],[4,5]] (touching merges)", iv(s.merge([[1,4],[4,5]])), [[1,5]])
check("[[1,4],[0,4]] (unsorted input)", iv(s.merge([[1,4],[0,4]])), [[0,4]])
check("[[1,4],[2,3]] (fully contained -- the max(end) case)",
      iv(s.merge([[1,4],[2,3]])), [[1,4]])
check("[[1,10],[2,3],[4,5]] (several contained)",
      iv(s.merge([[1,10],[2,3],[4,5]])), [[1,10]])
check("[[1,4],[5,6]] (adjacent but not touching)", iv(s.merge([[1,4],[5,6]])), [[1,4],[5,6]])
check("[[1,4]] (single)", iv(s.merge([[1,4]])), [[1,4]])
check("[] (empty)", iv(s.merge([])), [])
check("[[1,1],[1,1]] (degenerate points)", iv(s.merge([[1,1],[1,1]])), [[1,1]])
# The caller's input must survive unmutated.
src = [[1,10],[2,3]]
s.merge(src)
check("does not mutate the caller's intervals", src, [[1,10],[2,3]])
# Cross-check against a set-of-covered-points model on every small interval set.
bad = []
for n in range(0, 4):
    for combo in itertools.product([(0,0),(0,2),(1,1),(1,3),(2,4),(3,3),(4,6)], repeat=n):
        ivs = [list(x) for x in combo]
        covered = set()
        for a, b in combo:
            covered |= set(range(a, b + 1))
        got = s.merge([list(x) for x in combo])
        out = set()
        ok = True
        for a, b in got:
            if a > b or out & set(range(a, b + 1)):
                ok = False
            out |= set(range(a, b + 1))
        # merged output must cover the same points, be disjoint, and not be adjacent
        starts = [a for a, _ in got]
        if not ok or out != covered or starts != sorted(starts):
            bad.append((ivs, got))
check("output covers the same points, is disjoint and sorted", bad, [])

print("LeetCode 57 - Insert Interval")
s = load("057-insert-interval.html")
check("[[1,3],[6,9]] + [2,5]", iv(s.insert([[1,3],[6,9]], [2,5])), [[1,5],[6,9]])
check("[[1,2],[3,5],[6,7],[8,10],[12,16]] + [4,8]",
      iv(s.insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8])), [[1,2],[3,10],[12,16]])
check("[] + [5,7]", iv(s.insert([], [5,7])), [[5,7]])
check("[[1,5]] + [2,3] (swallowed)", iv(s.insert([[1,5]], [2,3])), [[1,5]])
check("[[1,5]] + [6,8] (after everything)", iv(s.insert([[1,5]], [6,8])), [[1,5],[6,8]])
check("[[1,5]] + [0,0] (before everything)", iv(s.insert([[1,5]], [0,0])), [[0,0],[1,5]])
check("[[1,5]] + [5,7] (touching on the right merges)", iv(s.insert([[1,5]], [5,7])), [[1,7]])
check("[[3,5]] + [1,3] (touching on the left merges)", iv(s.insert([[3,5]], [1,3])), [[1,5]])
check("[[3,5]] + [4,8] (min() case: result starts at 3, not 4)",
      iv(s.insert([[3,5]], [4,8])), [[3,8]])
check("[[1,2],[3,10]] + [2,4] (running end chains)",
      iv(s.insert([[1,2],[3,10]], [2,4])), [[1,10]])
# Must agree with sort-then-merge, which is the correct-but-slower answer.
merger = load("056-merge-intervals.html")
bad = []
for n in range(0, 5):
    base = [[2*i, 2*i + 1] for i in range(n)]        # sorted, non-overlapping
    for a in range(-1, 2 * n + 2):
        for b in range(a, 2 * n + 3):
            got = iv(s.insert([list(x) for x in base], [a, b]))
            want = iv(merger.merge([list(x) for x in base] + [[a, b]]))
            if got != want:
                bad.append((base, [a, b], got, want))
check("agrees with sort-then-merge on every insertion into a sorted list", bad, [])

print("LeetCode 58 - Length of Last Word")
one_liner = load("058-length-of-last-word.html", only=[0])   # the split() version
s = load("058-length-of-last-word.html", only=[1])           # the backward scan
check('"Hello World"', s.lengthOfLastWord("Hello World"), 5)
check('"   fly me   to   the moon  " (trailing + runs of spaces)',
      s.lengthOfLastWord("   fly me   to   the moon  "), 4)
check('"luffy is still joyboy"', s.lengthOfLastWord("luffy is still joyboy"), 6)
check('"a" (no space at all -- the i >= 0 guard)', s.lengthOfLastWord("a"), 1)
check('"a "', s.lengthOfLastWord("a "), 1)
check('"day"', s.lengthOfLastWord("day"), 3)
check('"   day"', s.lengthOfLastWord("   day"), 3)
check('"day   "', s.lengthOfLastWord("day   "), 3)
bad = []
for n in range(1, 8):
    for combo in itertools.product(["a", " "], repeat=n):
        text = "".join(combo)
        if not text.strip():
            continue                       # the problem guarantees at least one word
        if s.lengthOfLastWord(text) != len(text.split()[-1]):
            bad.append(text)
        if one_liner.lengthOfLastWord(text) != len(text.split()[-1]):
            bad.append(("one-liner", text))
check("both versions agree with split()[-1] on every a/space string up to length 7", bad, [])

print()
if fails:
    print(f"{len(fails)} FAILURES:")
    for f in fails:
        print("  x", f)
    sys.exit(1)
print("all python solutions pass")
