"""Extract every Python code block from the round-1 posts and exercise it.

The blocks are pulled straight out of the published HTML, so this tests what a
reader would copy, not a retyped copy of it.
"""
import collections
import functools
import html
import math
import random
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

print("LeetCode 62 - Unique Paths")
s = load("062-unique-paths.html")
check("m=3 n=7", s.uniquePaths(3, 7), 28)
check("m=3 n=2", s.uniquePaths(3, 2), 3)
check("m=1 n=1 (already there)", s.uniquePaths(1, 1), 1)
check("m=1 n=10 (a corridor)", s.uniquePaths(1, 10), 1)
check("m=10 n=1 (the other corridor)", s.uniquePaths(10, 1), 1)
check("m=7 n=3 (symmetric)", s.uniquePaths(7, 3), 28)
# The closed form the post names: C(m+n-2, m-1).
bad = []
for m in range(1, 12):
    for n in range(1, 12):
        want = math.comb(m + n - 2, m - 1)
        if s.uniquePaths(m, n) != want:
            bad.append((m, n))
check("matches C(m+n-2, m-1) for every grid up to 11x11", bad, [])
check("reusable: 3x7 twice", (s.uniquePaths(3, 7), s.uniquePaths(3, 7)), (28, 28))

print("LeetCode 63 - Unique Paths II")
s63 = load("063-unique-paths-ii.html")
check("blocked centre", s63.uniquePathsWithObstacles([[0,0,0],[0,1,0],[0,0,0]]), 2)
check("[[0,1],[0,0]]", s63.uniquePathsWithObstacles([[0,1],[0,0]]), 1)
check("[[1]] (start blocked)", s63.uniquePathsWithObstacles([[1]]), 0)
check("[[0]] (single free cell)", s63.uniquePathsWithObstacles([[0]]), 1)
check("[[0,0],[1,1],[0,0]] (a wall across)", s63.uniquePathsWithObstacles([[0,0],[1,1],[0,0]]), 0)
check("finish blocked", s63.uniquePathsWithObstacles([[0,0],[0,1]]), 0)
# The first-row trap: everything past an obstacle in row 0 is unreachable.
check("obstacle in the top row cuts off the rest",
      s63.uniquePathsWithObstacles([[0,1,0],[0,0,0]]), 1)
check("obstacle in the left column can be walked around",
      s63.uniquePathsWithObstacles([[0,0],[1,0],[0,0]]), 1)
check("...but not in a single-column grid",
      s63.uniquePathsWithObstacles([[0],[1],[0]]), 0)
# With no obstacles it must agree with problem 62, on every small grid.
bad = []
for m in range(1, 7):
    for n in range(1, 7):
        if s63.uniquePathsWithObstacles([[0] * n for _ in range(m)]) != s.uniquePaths(m, n):
            bad.append((m, n))
check("obstacle-free grids agree with problem 62", bad, [])
# Brute-force path enumeration on every small grid with obstacles.
def count_paths(grid):
    m, n = len(grid), len(grid[0])
    if grid[0][0] or grid[m-1][n-1]:
        return 0
    seen = {}
    def go(r, c):
        if r == m - 1 and c == n - 1:
            return 1
        if (r, c) in seen:
            return seen[(r, c)]
        total = 0
        if r + 1 < m and not grid[r+1][c]:
            total += go(r + 1, c)
        if c + 1 < n and not grid[r][c+1]:
            total += go(r, c + 1)
        seen[(r, c)] = total
        return total
    return go(0, 0)

bad = []
for m in range(1, 4):
    for n in range(1, 4):
        for mask in range(1 << (m * n)):
            grid = [[(mask >> (r * n + c)) & 1 for c in range(n)] for r in range(m)]
            if s63.uniquePathsWithObstacles([row[:] for row in grid]) != count_paths(grid):
                bad.append(grid)
check("matches path enumeration on every obstacle layout up to 3x3", bad, [])

print("LeetCode 64 - Minimum Path Sum")
s64 = load("064-minimum-path-sum.html")
check("[[1,3,1],[1,5,1],[4,2,1]]", s64.minPathSum([[1,3,1],[1,5,1],[4,2,1]]), 7)
check("[[1,2,3],[4,5,6]]", s64.minPathSum([[1,2,3],[4,5,6]]), 12)
check("[[5]] (start counts)", s64.minPathSum([[5]]), 5)
check("[[0]]", s64.minPathSum([[0]]), 0)
check("single row", s64.minPathSum([[1,2,3,4]]), 10)
check("single column", s64.minPathSum([[1],[2],[3]]), 6)
# The grid from the post where the greedy loses.
check("greedy counterexample from the post",
      s64.minPathSum([[1,2,100],[1,100,100],[1,1,1]]), 5)
check("returns an int, not a float", isinstance(s64.minPathSum([[1,2],[3,4]]), int), True)
# Brute force over every monotone path, on every small grid of small values.
def best_path(grid):
    m, n = len(grid), len(grid[0])
    best = [None]
    def go(r, c, total):
        total += grid[r][c]
        if r == m - 1 and c == n - 1:
            if best[0] is None or total < best[0]:
                best[0] = total
            return
        if r + 1 < m:
            go(r + 1, c, total)
        if c + 1 < n:
            go(r, c + 1, total)
    go(0, 0, 0)
    return best[0]

bad = []
for m in range(1, 4):
    for n in range(1, 4):
        for combo in itertools.product([0, 1, 5], repeat=m * n):
            grid = [list(combo[r * n:(r + 1) * n]) for r in range(m)]
            if s64.minPathSum([row[:] for row in grid]) != best_path(grid):
                bad.append(grid)
check("matches brute-force path enumeration on every grid up to 3x3 over {0,1,5}", bad, [])

print("LeetCode 65 - Valid Number")
s = load("065-valid-number.html")
VALID = ["2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3", "3e+7",
         "+6e-1", "53.5e93", "-123.456e789", "0", "0.1", ".1", "1.", "+.8", "46e6"]
INVALID = ["abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53", ".",
           "+", "", "4e+", "e", ".e1", "1e2e3", "1..2", "+-", " 1", "1 ", "1e.5",
           ".-4", "6+1", "infinity", "1e2.5"]
for t in VALID:
    check(f"valid: {t!r}", s.isNumber(t), True)
for t in INVALID:
    check(f"invalid: {t!r}", s.isNumber(t), False)
# Cross-check against the grammar the post writes as a regex, over generated strings.
GRAMMAR = re.compile(r"^[+-]?((\d+\.?\d*)|(\.\d+))([eE][+-]?\d+)?$")
bad = []
for n in range(0, 5):
    for combo in itertools.product("01.eE+-", repeat=n):
        t = "".join(combo)
        if s.isNumber(t) != bool(GRAMMAR.match(t)):
            bad.append(t)
check("agrees with the grammar on every string up to length 4 over 01.eE+-", bad, [])

print("LeetCode 67 - Add Binary")
s = load("067-add-binary.html")
check('"11" + "1"', s.addBinary("11", "1"), "100")
check('"1010" + "1011"', s.addBinary("1010", "1011"), "10101")
check('"0" + "0"', s.addBinary("0", "0"), "0")
check('"1" + "111" (carry all the way out)', s.addBinary("1", "111"), "1000")
check('"0" + "1"', s.addBinary("0", "1"), "1")
# Well past what a 64-bit integer could hold -- the constraint the post calls out.
big = "1" * 200
check("200 ones + 1", s.addBinary(big, "1"), "1" + "0" * 200)
check("200 ones + 200 ones",
      s.addBinary(big, big), bin(int(big, 2) * 2)[2:])
bad = []
for x in range(0, 64):
    for y in range(0, 64):
        got = s.addBinary(bin(x)[2:], bin(y)[2:])
        if got != bin(x + y)[2:]:
            bad.append((x, y, got))
check("agrees with integer addition for all x,y in 0..63", bad, [])
# The constraints exclude leading zeros in the input, so the output cannot have
# any either: adding two such numbers keeps the leading 1 in place.
bad = [(x, y) for x in range(1, 40) for y in range(1, 40)
       if s.addBinary(bin(x)[2:], bin(y)[2:]).startswith("0")]
check("never emits a leading zero on in-spec input", bad, [])

print("LeetCode 68 - Text Justification")
s = load("068-text-justification.html")
check("the canonical example",
      s.fullJustify(["This","is","an","example","of","text","justification."], 16),
      ["This    is    an", "example  of text", "justification.  "])
check("single word line is NOT stretched",
      s.fullJustify(["What","must","be","acknowledgment","shall","be"], 16),
      ["What   must   be", "acknowledgment  ", "shall be        "])
check("one word total", s.fullJustify(["a"], 5), ["a    "])
check("word exactly maxWidth", s.fullJustify(["abcde"], 5), ["abcde"])
check("a single line is the LAST line, so left-justified",
      s.fullJustify(["a", "b"], 5), ["a b  "])
check("two words, spaces divide evenly",
      s.fullJustify(["a", "b", "cccc"], 5), ["a   b", "cccc "])
check("extra spaces go to the LEFT gaps",
      s.fullJustify(["aa", "b", "cc", "ddddd"], 8), ["aa  b cc", "ddddd   "])
# Structural invariants on generated inputs: every line is exactly maxWidth, words
# come back in order, and no line has leading spaces.
bad = []
for width in range(4, 12):
    for n in range(1, 7):
        for combo in itertools.product(["a", "bb", "ccc"], repeat=n):
            if max(len(w) for w in combo) > width:
                continue
            out = s.fullJustify(list(combo), width)
            if any(len(line) != width for line in out):
                bad.append(("width", combo, width, out)); continue
            if [w for line in out for w in line.split()] != list(combo):
                bad.append(("order", combo, width, out)); continue
            if any(line.startswith(" ") for line in out):
                bad.append(("leading space", combo, width, out)); continue
            # Only the last line, or a line holding one word, may end in a space.
            for line in out[:-1]:
                if line.endswith(" ") and len(line.split()) > 1:
                    bad.append(("not justified", combo, width, out))
check("every line is exactly maxWidth, words in order, no leading spaces", bad, [])

print("LeetCode 69 - Sqrt(x)")
s = load("069-sqrtx.html")
check("x=4", s.mySqrt(4), 2)
check("x=8 (floor of 2.828)", s.mySqrt(8), 2)
check("x=0", s.mySqrt(0), 0)
check("x=1", s.mySqrt(1), 1)
check("x=2", s.mySqrt(2), 1)
check("x=2147483647 (the overflow case)", s.mySqrt(2147483647), 46340)
check("x=2147395600 (46340 squared exactly)", s.mySqrt(2147395600), 46340)
bad = [x for x in range(0, 5000) if s.mySqrt(x) != math.isqrt(x)]
check("matches math.isqrt for every x in 0..4999", bad, [])
bad = [x for x in (10**k for k in range(1, 10)) if s.mySqrt(x) != math.isqrt(x)]
check("matches math.isqrt on powers of ten up to 10^9", bad, [])
# Perfect squares and the values either side of them must land correctly.
bad = []
for k in range(1, 1000):
    sq = k * k
    if (s.mySqrt(sq), s.mySqrt(sq - 1), s.mySqrt(sq + 1)) != (k, k - 1, k):
        bad.append(k)
check("k*k, k*k-1 and k*k+1 for every k in 1..999", bad, [])

print("LeetCode 70 - Climbing Stairs")
s = load("070-climbing-stairs.html")
check("n=1", s.climbStairs(1), 1)
check("n=2", s.climbStairs(2), 2)
check("n=3", s.climbStairs(3), 3)
check("n=4", s.climbStairs(4), 5)
check("n=5", s.climbStairs(5), 8)
check("n=45 (the constraint bound)", s.climbStairs(45), 1836311903)
# Independent model: count sequences of 1s and 2s summing to n.
def ways(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a
bad = [n for n in range(0, 40) if s.climbStairs(n) != ways(n)]
check("matches an independent Fibonacci model for n in 0..39", bad, [])
# And against brute-force enumeration for small n, which is what the problem means.
def enumerate_ways(n):
    if n == 0:
        return 1
    if n < 0:
        return 0
    return enumerate_ways(n - 1) + enumerate_ways(n - 2)
bad = [n for n in range(1, 16) if s.climbStairs(n) != enumerate_ways(n)]
check("matches brute-force enumeration for n in 1..15", bad, [])

print("LeetCode 71 - Simplify Path")
s = load("071-simplify-path.html")
check('"/home/"', s.simplifyPath("/home/"), "/home")
check('"/home//foo/"', s.simplifyPath("/home//foo/"), "/home/foo")
check('"/../" (root parent is root)', s.simplifyPath("/../"), "/")
check('"/a/./b/../../c/"', s.simplifyPath("/a/./b/../../c/"), "/c")
check('"/..." (three dots is a NAME)', s.simplifyPath("/..."), "/...")
check('"/"', s.simplifyPath("/"), "/")
check('"/a//b////c/d//././/.."', s.simplifyPath("/a//b////c/d//././/.."), "/a/b/c")
check('"/../../../a"', s.simplifyPath("/../../../a"), "/a")
check('"/a/.."', s.simplifyPath("/a/.."), "/")
check('"/..hidden"', s.simplifyPath("/..hidden"), "/..hidden")
check('"/a..b"', s.simplifyPath("/a..b"), "/a..b")
check('"/.."', s.simplifyPath("/.."), "/")
# Cross-check against an independent model on generated paths.
def canonical(path):
    out = []
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if out:
                out.pop()
        else:
            out.append(part)
    return "/" + "/".join(out)

bad = []
for n in range(1, 6):
    for combo in itertools.product(["a", ".", "..", "", "..."], repeat=n):
        path = "/" + "/".join(combo)
        got = s.simplifyPath(path)
        if got != canonical(path):
            bad.append((path, got, canonical(path)))
check("matches an independent model on every path up to 5 components", bad, [])
# Structural invariants: always absolute, never a trailing slash, no . or .. left.
bad = []
for n in range(1, 6):
    for combo in itertools.product(["a", "bb", ".", "..", ""], repeat=n):
        got = s.simplifyPath("/" + "/".join(combo))
        if not got.startswith("/"):
            bad.append(("not absolute", got))
        elif got != "/" and got.endswith("/"):
            bad.append(("trailing slash", got))
        elif any(p in (".", "..", "") for p in got.split("/")[1:]) and got != "/":
            bad.append(("unresolved", got))
check("output is absolute, has no trailing slash, and resolves every . and ..", bad, [])

print("LeetCode 72 - Edit Distance")
s = load("072-edit-distance.html")
check('"horse" -> "ros"', s.minDistance("horse", "ros"), 3)
check('"intention" -> "execution"', s.minDistance("intention", "execution"), 5)
check('"" -> "abc" (three inserts)', s.minDistance("", "abc"), 3)
check('"abc" -> "" (three deletes)', s.minDistance("abc", ""), 3)
check('"" -> ""', s.minDistance("", ""), 0)
check('"abc" -> "abc"', s.minDistance("abc", "abc"), 0)
check('"a" -> "b" (one replace)', s.minDistance("a", "b"), 1)
check('"sunday" -> "saturday"', s.minDistance("sunday", "saturday"), 3)
# Independent Levenshtein, plus the symmetry the post claims.
def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(prev[j - 1] if ca == cb else 1 + min(prev[j - 1], prev[j], cur[j - 1]))
        prev = cur
    return prev[len(b)]

bad, asym = [], []
for m in range(0, 5):
    for n in range(0, 5):
        for wa in itertools.product("ab", repeat=m):
            for wb in itertools.product("ab", repeat=n):
                a, b = "".join(wa), "".join(wb)
                got = s.minDistance(a, b)
                if got != lev(a, b):
                    bad.append((a, b, got))
                if got != s.minDistance(b, a):
                    asym.append((a, b))
check("matches Levenshtein on every pair of a/b strings up to length 4", bad, [])
check("distance is symmetric", asym, [])
# The answer is never more than the longer string, nor less than the length difference.
bad = []
for a, b in [("abcdef", ""), ("kitten", "sitting"), ("flaw", "lawn"), ("a" * 20, "b" * 20)]:
    d = s.minDistance(a, b)
    if not (abs(len(a) - len(b)) <= d <= max(len(a), len(b))):
        bad.append((a, b, d))
check("|len(a)-len(b)| <= distance <= max(len(a), len(b))", bad, [])

print("LeetCode 76 - Minimum Window Substring")
s = load("076-minimum-window-substring.html")
check('"ADOBECODEBANC", "ABC"', s.minWindow("ADOBECODEBANC", "ABC"), "BANC")
check('"a", "a"', s.minWindow("a", "a"), "a")
check('"a", "aa" (duplicates must be counted)', s.minWindow("a", "aa"), "")
check('"ab", "b"', s.minWindow("ab", "b"), "b")
check('"ab", "A" (case sensitive)', s.minWindow("ab", "A"), "")
check('"aa", "aa"', s.minWindow("aa", "aa"), "aa")
check('"", "a"', s.minWindow("", "a"), "")
check('"abc", ""', s.minWindow("abc", ""), "")
check('"bba", "ab"', s.minWindow("bba", "ab"), "ba")
check('"cabwefgewcwaefgcf", "cae"', s.minWindow("cabwefgewcwaefgcf", "cae"), "cwae")
# Brute force over every substring, on generated inputs.
def brute(sv, tv):
    if not tv:
        return ""
    needc = collections.Counter(tv)
    best = None
    for i in range(len(sv)):
        for j in range(i + 1, len(sv) + 1):
            window = collections.Counter(sv[i:j])
            if all(window[c] >= k for c, k in needc.items()):
                if best is None or j - i < len(best):
                    best = sv[i:j]
                break            # shortest window starting at i
    return best or ""

bad = []
for n in range(0, 7):
    for sv in itertools.product("abc", repeat=n):
        for m in range(1, 3):
            for tv in itertools.product("ab", repeat=m):
                a, b = "".join(sv), "".join(tv)
                got, want = s.minWindow(a, b), brute(a, b)
                # Any window of the right length is acceptable; compare lengths and validity.
                if len(got) != len(want):
                    bad.append((a, b, got, want))
                elif got and not all(collections.Counter(got)[c] >= k
                                     for c, k in collections.Counter(b).items()):
                    bad.append(("invalid window", a, b, got))
check("matches brute force on every s up to length 6 over abc, t up to length 2", bad, [])

print("LeetCode 78 - Subsets")
s = load("078-subsets.html")
def sset(r):
    return sorted(tuple(x) for x in r)
check("[1,2,3]", sset(s.subsets([1,2,3])),
      sset([[],[1],[2],[3],[1,2],[1,3],[2,3],[1,2,3]]))
check("[0]", sset(s.subsets([0])), sset([[], [0]]))
check("[] returns [[]], not []", s.subsets([]), [[]])
check("[1,2] ", sset(s.subsets([1,2])), sset([[],[1],[2],[1,2]]))
check("the empty subset is present", [] in s.subsets([1,2,3]), True)
# 2^n subsets, all distinct, each a sub-multiset of the input, for every n.
bad = []
for n in range(0, 11):
    nums = list(range(n))
    got = s.subsets(nums)
    if len(got) != 2 ** n:
        bad.append(("count", n, len(got)))
    elif len({tuple(x) for x in got}) != 2 ** n:
        bad.append(("duplicates", n))
    elif any(len(set(x)) != len(x) or not set(x) <= set(nums) for x in got):
        bad.append(("bad member", n))
check("2^n distinct subsets of the input for every n in 0..10", bad, [])
# Against itertools.combinations, which is an independent generator.
bad = []
for n in range(0, 7):
    nums = list(range(n))
    want = sorted(c for k in range(n + 1) for c in itertools.combinations(nums, k))
    if sset(s.subsets(nums)) != want:
        bad.append(n)
check("matches itertools.combinations over all sizes for n in 0..6", bad, [])
# Aliasing: the returned lists must be independent objects.
# If the recursion stored `path` instead of a copy, every entry is the same object
# and this marker would appear in all 8 of them.
out = s.subsets([1, 2, 3])
out[0].append(999)
check("mutating one returned subset does not touch the others",
      sum(999 in x for x in out), 1)
check("...and the other 7 still hold the right sizes",
      sorted(len(x) for x in out[1:]), [1, 1, 1, 2, 2, 2, 3])

print("LeetCode 81 - Search in Rotated Sorted Array II")
s = load("081-search-in-rotated-sorted-array-ii.html")
check("[2,5,6,0,0,1,2] t=0", s.search([2,5,6,0,0,1,2], 0), True)
check("[2,5,6,0,0,1,2] t=3", s.search([2,5,6,0,0,1,2], 3), False)
check("[1,0,1,1,1] t=0 (the ambiguous case)", s.search([1,0,1,1,1], 0), True)
check("[1,1,1,0,1] t=0 (pivot on the other side)", s.search([1,1,1,0,1], 0), True)
check("[1,1,1,1,1] t=2", s.search([1,1,1,1,1], 2), False)
check("[1] t=1", s.search([1], 1), True)
check("[1] t=0", s.search([1], 0), False)
check("[1,1] t=1", s.search([1,1], 1), True)
check("[3,1] t=1 (rotated pair)", s.search([3,1], 1), True)
# Every rotation of every sorted array over a small alphabet, against membership.
bad = []
for n in range(1, 8):
    for combo in itertools.product([0, 1, 2], repeat=n):
        base = sorted(combo)
        for k in range(n):
            rotated = base[k:] + base[:k]
            for target in range(-1, 4):
                if s.search(list(rotated), target) != (target in rotated):
                    bad.append((rotated, target))
check("every rotation of every sorted array up to length 7 over {0,1,2}", bad, [])
# Arrays that are mostly one value -- the worst case the post describes.
bad = []
for n in range(1, 12):
    for pos in range(n):
        arr = [1] * n
        arr[pos] = 0
        base = sorted(arr)
        for k in range(n):
            rotated = base[k:] + base[:k]
            if s.search(list(rotated), 0) is not True or s.search(list(rotated), 2) is not False:
                bad.append((rotated,))
check("single 0 among 1s, every rotation, terminates and is correct", bad, [])

print("LeetCode 83 - Remove Duplicates from Sorted List")
ns = {}
exec(compile(LISTNODE, "listnode", "exec"), ns)
s = load("083-remove-duplicates-from-sorted-list.html", extra=LISTNODE)
def dedupe(xs):
    return to_arr83(s.deleteDuplicates(to_list83(xs)))
to_list83, to_arr83 = ns["to_list"], ns["to_arr"]
check("1->1->2", dedupe([1,1,2]), [1,2])
check("1->1->2->3->3", dedupe([1,1,2,3,3]), [1,2,3])
check("1->1->1 (THREE in a row)", dedupe([1,1,1]), [1])
check("1->1->1->1 (four in a row)", dedupe([1,1,1,1]), [1])
check("empty list", dedupe([]), [])
check("single node", dedupe([1]), [1])
check("no duplicates at all", dedupe([1,2,3]), [1,2,3])
check("duplicates at the tail", dedupe([1,2,3,3,3]), [1,2,3])
check("every value duplicated", dedupe([1,1,2,2,3,3]), [1,2,3])
bad = []
for n in range(0, 9):
    for combo in itertools.product([1, 1, 2, 3], repeat=n):
        xs = sorted(combo)
        want = [v for i, v in enumerate(xs) if i == 0 or v != xs[i - 1]]
        if dedupe(xs) != want:
            bad.append(xs)
check("matches sorted-unique on every sorted list up to length 8", bad, [])
# The head node object itself must be returned, not a rebuilt list.
node = to_list83([1, 1, 2])
check("returns the original head object", s.deleteDuplicates(node) is node, True)

print("LeetCode 88 - Merge Sorted Array")
s = load("088-merge-sorted-array.html")
def merged(a, m, b, n):
    a = list(a)
    s.merge(a, m, list(b), n)
    return a
check("[1,2,3,0,0,0] + [2,5,6]", merged([1,2,3,0,0,0], 3, [2,5,6], 3), [1,2,2,3,5,6])
check("[1] m=1, [] n=0", merged([1], 1, [], 0), [1])
check("[0] m=0, [1] n=1 (nums1 contributes nothing)", merged([0], 0, [1], 1), [1])
check("[4,5,6,0,0,0] + [1,2,3] (all of nums2 first)",
      merged([4,5,6,0,0,0], 3, [1,2,3], 3), [1,2,3,4,5,6])
check("[] m=0, [] n=0", merged([], 0, [], 0), [])
check("negatives", merged([-3,-1,0,0], 3, [-2], 1), [-3,-2,-1,0])
check("all equal", merged([2,2,2,0,0], 3, [2,2], 2), [2,2,2,2,2])
check("returns None, mutating in place", s.merge([1,0], 1, [2], 1), None)
# Exhaustive over every pair of small sorted inputs.
bad = []
for m in range(0, 5):
    for n in range(0, 5):
        for a in itertools.combinations_with_replacement(range(4), m):
            for b in itertools.combinations_with_replacement(range(4), n):
                got = merged(list(a) + [0] * n, m, list(b), n)
                if got != sorted(list(a) + list(b)):
                    bad.append((a, b, got))
check("matches sorted(a + b) for every pair of sorted inputs up to length 4", bad, [])

print("LeetCode 91 - Decode Ways")
s = load("091-decode-ways.html")
check('"12"', s.numDecodings("12"), 2)
check('"226"', s.numDecodings("226"), 3)
check('"06" (leading zero in a pair)', s.numDecodings("06"), 0)
check('"0"', s.numDecodings("0"), 0)
check('"10"', s.numDecodings("10"), 1)
check('"100" (the 0 has no partner)', s.numDecodings("100"), 0)
check('"2101"', s.numDecodings("2101"), 1)
check('"27" (27 is not a letter)', s.numDecodings("27"), 1)
check('"1111"', s.numDecodings("1111"), 5)
check('"11106"', s.numDecodings("11106"), 2)
check('"230"', s.numDecodings("230"), 0)
check('"1201234"', s.numDecodings("1201234"), 3)
# Brute force by explicit enumeration, over every digit string up to length 8.
def decodings(text):
    if not text:
        return 1
    total = 0
    if text[0] != "0":
        total += decodings(text[1:])
    if len(text) >= 2 and 10 <= int(text[:2]) <= 26:
        total += decodings(text[2:])
    return total

bad = []
for n in range(1, 9):
    for combo in itertools.product("0123", repeat=n):
        text = "".join(combo)
        if s.numDecodings(text) != decodings(text):
            bad.append((text, s.numDecodings(text), decodings(text)))
check("matches enumeration on every string of 0-3 digits up to length 8", bad, [])
# All-ones is Fibonacci, which is the post's claim about the shape.
fib = [1, 1]
while len(fib) < 20:
    fib.append(fib[-1] + fib[-2])
bad = [n for n in range(1, 18) if s.numDecodings("1" * n) != fib[n]]
check("all-ones strings follow Fibonacci", bad, [])

print("LeetCode 94 - Binary Tree Inorder Traversal")
TREE = """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build(xs):
    if not xs or xs[0] is None:
        return None
    root = TreeNode(xs[0])
    queue, i = [root], 1
    while queue and i < len(xs):
        node = queue.pop(0)
        if i < len(xs):
            v = xs[i]; i += 1
            if v is not None:
                node.left = TreeNode(v); queue.append(node.left)
        if i < len(xs):
            v = xs[i]; i += 1
            if v is not None:
                node.right = TreeNode(v); queue.append(node.right)
    return root
"""
ns94 = {}
exec(compile(TREE, "tree", "exec"), ns94)
build = ns94["build"]
s = load("094-binary-tree-inorder-traversal.html", extra=TREE)
check("[1,null,2,3]", s.inorderTraversal(build([1, None, 2, 3])), [1, 3, 2])
check("empty tree", s.inorderTraversal(None), [])
check("single node", s.inorderTraversal(build([1])), [1])
check("a BST comes out sorted",
      s.inorderTraversal(build([4, 2, 6, 1, 3, 5, 7])), [1, 2, 3, 4, 5, 6, 7])
# A degenerate left chain and right chain, which is where recursion depth bites.
left_chain = ns94["TreeNode"](1)
node = left_chain
for v in range(2, 60):
    node.left = ns94["TreeNode"](v); node = node.left
check("left chain of 59 nodes", s.inorderTraversal(left_chain), list(range(59, 0, -1)))
# Cross-check against an independent recursive traversal on generated trees.
def inorder_model(node):
    return inorder_model(node.left) + [node.val] + inorder_model(node.right) if node else []

bad = []
for n in range(1, 9):
    for combo in itertools.product([None, 1], repeat=n - 1):
        xs = [0] + [None if c is None else 1 for c in combo]
        # give every present node a distinct value so ordering is observable
        vals = itertools.count(1)
        xs = [next(vals) if v is not None else None for v in xs]
        tree = build(xs)
        if s.inorderTraversal(tree) != inorder_model(tree):
            bad.append(xs)
check("matches a recursive model on every small tree shape", bad, [])
# The Morris variant, if the post shows one, must agree and restore the tree.
if hasattr(s, "inorderMorris"):
    bad = []
    for xs in ([4,2,6,1,3,5,7], [1,None,2,3], [1], [1,2], [1,None,2]):
        tree = build(xs)
        got = s.inorderMorris(tree)
        if got != inorder_model(build(xs)):
            bad.append((xs, got))
        elif inorder_model(tree) != got:
            bad.append(("tree not restored", xs))
    check("[Morris] agrees and leaves the tree restored", bad, [])

print("LeetCode 98 - Validate Binary Search Tree")
s = load("098-validate-binary-search-tree.html", extra=TREE)
check("[2,1,3]", s.isValidBST(build([2, 1, 3])), True)
check("[5,1,4,null,null,3,6]", s.isValidBST(build([5, 1, 4, None, None, 3, 6])), False)
check("the naive-check counterexample [5,1,6,null,null,4,7]",
      s.isValidBST(build([5, 1, 6, None, None, 4, 7])), False)
check("empty tree", s.isValidBST(None), True)
check("single node", s.isValidBST(build([1])), True)
check("duplicates are invalid", s.isValidBST(build([2, 2])), False)
check("Integer.MIN_VALUE as the only node (sentinel trap)",
      s.isValidBST(build([-2147483648])), True)
check("Integer.MAX_VALUE as the only node", s.isValidBST(build([2147483647])), True)
check("[-2147483648, null, 2147483647]",
      s.isValidBST(build([-2147483648, None, 2147483647])), True)
# Independent model: inorder must be strictly increasing.
bad = []
for n in range(1, 8):
    for vals in itertools.product([1, 2, 3], repeat=n):
        tree = build(list(vals))
        seq = inorder_model(tree)
        want = all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))
        if s.isValidBST(tree) != want:
            bad.append((vals, s.isValidBST(tree), want))
check("agrees with strictly-increasing-inorder on every small tree", bad, [])
if hasattr(s, "isValidBSTInorder"):
    bad = []
    for n in range(1, 7):
        for vals in itertools.product([1, 2, 3], repeat=n):
            if s.isValidBSTInorder(build(list(vals))) != s.isValidBST(build(list(vals))):
                bad.append(vals)
    check("[inorder version] agrees with the bounds version", bad, [])

print("LeetCode 100 - Same Tree")
s = load("100-same-tree.html", extra=TREE)
check("identical trees", s.isSameTree(build([1,2,3]), build([1,2,3])), True)
check("same values, different shape",
      s.isSameTree(build([1,2]), build([1,None,2])), False)
check("same shape, different values",
      s.isSameTree(build([1,2,1]), build([1,1,2])), False)
check("both empty", s.isSameTree(None, None), True)
check("one empty", s.isSameTree(None, build([1])), False)
check("one empty, the other way round", s.isSameTree(build([1]), None), False)
check("a node valued 0 is not treated as absent",
      s.isSameTree(build([0]), build([0])), True)
# Exhaustive over every pair of small trees, against an independent comparison.
def same_model(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and same_model(a.left, b.left) and same_model(a.right, b.right)

shapes = []
for n in range(0, 5):
    for vals in itertools.product([1, 2, None], repeat=n):
        xs = list(vals)
        if xs and xs[0] is None:
            continue
        shapes.append(xs)
bad = []
for xa in shapes[:60]:
    for xb in shapes[:60]:
        ta, tb = build(list(xa)), build(list(xb))
        if s.isSameTree(ta, tb) != same_model(build(list(xa)), build(list(xb))):
            bad.append((xa, xb))
check("matches an independent comparison on every pair of small trees", bad, [])

print("LeetCode 101 - Symmetric Tree")
s = load("101-symmetric-tree.html", extra=TREE)
check("[1,2,2,3,4,4,3]", s.isSymmetric(build([1,2,2,3,4,4,3])), True)
check("[1,2,2,null,3,null,3]", s.isSymmetric(build([1,2,2,None,3,None,3])), False)
check("empty tree", s.isSymmetric(None), True)
check("single node", s.isSymmetric(build([1])), True)
check("[1,2,2] (mirrored leaves)", s.isSymmetric(build([1,2,2])), True)
check("[1,2,3] (values differ)", s.isSymmetric(build([1,2,3])), False)
check("[1,2,null] (one-sided)", s.isSymmetric(build([1,2,None])), False)
# The tree that defeats the inorder-palindrome shortcut the post warns about.
palindromic = ns94["TreeNode"](1)
palindromic.left = ns94["TreeNode"](2); palindromic.left.left = ns94["TreeNode"](2)
palindromic.right = ns94["TreeNode"](2); palindromic.right.left = ns94["TreeNode"](2)
check("inorder is a palindrome but the tree is NOT symmetric",
      (inorder_model(palindromic), s.isSymmetric(palindromic)), ([2, 2, 1, 2, 2], False))
# Independent model: mirror the tree and compare.
def mirror_model(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return (a.val == b.val and mirror_model(a.left, b.right)
            and mirror_model(a.right, b.left))

bad = []
for n in range(1, 8):
    for vals in itertools.product([1, 2, None], repeat=n - 1):
        xs = [1] + list(vals)
        tree = build(xs)
        want = tree is None or mirror_model(tree.left, tree.right)
        if s.isSymmetric(build(xs)) != want:
            bad.append(xs)
check("matches a mirror model on every small tree", bad, [])

print("LeetCode 102 - Binary Tree Level Order Traversal")
s = load("102-binary-tree-level-order-traversal.html", extra=TREE)
check("[3,9,20,null,null,15,7]",
      s.levelOrder(build([3,9,20,None,None,15,7])), [[3],[9,20],[15,7]])
check("empty tree returns [], not [[]]", s.levelOrder(None), [])
check("single node", s.levelOrder(build([1])), [[1]])
check("left chain", s.levelOrder(build([1,2,None,3])), [[1],[2],[3]])
# Independent model by depth, on every small tree.
def levels_model(node, depth=0, acc=None):
    acc = [] if acc is None else acc
    if node is None:
        return acc
    if depth == len(acc):
        acc.append([])
    acc[depth].append(node.val)
    levels_model(node.left, depth + 1, acc)
    levels_model(node.right, depth + 1, acc)
    return acc

bad = []
for n in range(1, 9):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        if s.levelOrder(build(xs)) != levels_model(build(xs)):
            bad.append(xs)
check("matches a depth-indexed model on every small tree shape", bad, [])
if hasattr(s, "levelOrderDfs"):
    bad = [xs for xs in ([3,9,20,None,None,15,7], [1], [1,2,None,3], [1,2,3,4,5,6,7])
           if s.levelOrderDfs(build(xs)) != s.levelOrder(build(xs))]
    check("[DFS-by-depth version] agrees with BFS", bad, [])

print("LeetCode 103 - Binary Tree Zigzag Level Order Traversal")
s = load("103-binary-tree-zigzag-level-order-traversal.html", extra=TREE)
check("[3,9,20,null,null,15,7]",
      s.zigzagLevelOrder(build([3,9,20,None,None,15,7])), [[3],[20,9],[15,7]])
check("empty tree", s.zigzagLevelOrder(None), [])
check("single node", s.zigzagLevelOrder(build([1])), [[1]])
check("four levels, so the alternation repeats",
      s.zigzagLevelOrder(build([1,2,3,4,5,6,7,8])), [[1],[3,2],[4,5,6,7],[8]])
# Must equal level order with every odd level reversed.
plain = load("102-binary-tree-level-order-traversal.html", extra=TREE)
bad = []
for n in range(1, 9):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        want = [lvl if i % 2 == 0 else lvl[::-1]
                for i, lvl in enumerate(plain.levelOrder(build(xs)))]
        if s.zigzagLevelOrder(build(xs)) != want:
            bad.append(xs)
check("equals level order with every odd level reversed, on every small tree", bad, [])

print("LeetCode 104 - Maximum Depth of Binary Tree")
s = load("104-maximum-depth-of-binary-tree.html", extra=TREE)
check("[3,9,20,null,null,15,7]", s.maxDepth(build([3,9,20,None,None,15,7])), 3)
check("empty tree", s.maxDepth(None), 0)
check("single node (depth counts NODES)", s.maxDepth(build([1])), 1)
check("[1,null,2]", s.maxDepth(build([1,None,2])), 2)
def depth_model(node):
    return 0 if node is None else 1 + max(depth_model(node.left), depth_model(node.right))
bad = []
for n in range(1, 9):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        if s.maxDepth(build(xs)) != depth_model(build(xs)):
            bad.append(xs)
check("matches a recursive model on every small tree shape", bad, [])
if hasattr(s, "maxDepthBfs"):
    bad = []
    for n in range(1, 8):
        for mask in range(1 << (n - 1)):
            nxt = itertools.count(1)
            xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
            if s.maxDepthBfs(build(xs)) != s.maxDepth(build(xs)):
                bad.append(xs)
    check("[BFS version] agrees with the recursion", bad, [])

print("LeetCode 105 - Construct Binary Tree from Preorder and Inorder")
s = load("105-construct-binary-tree-from-preorder-and-inorder-traversal.html", extra=TREE)
def preorder_model(node):
    return [] if node is None else [node.val] + preorder_model(node.left) + preorder_model(node.right)

def shape(node):
    return None if node is None else (node.val, shape(node.left), shape(node.right))

check("the canonical example",
      shape(s.buildTree([3,9,20,15,7], [9,3,15,20,7])),
      shape(build([3,9,20,None,None,15,7])))
check("single node", shape(s.buildTree([1], [1])), shape(build([1])))
check("empty input", s.buildTree([], []), None)
check("left chain", shape(s.buildTree([1,2,3], [3,2,1])), shape(build([1,2,None,3])))
check("right chain", shape(s.buildTree([1,2,3], [1,2,3])), shape(build([1,None,2,None,3])))
# Round-trip: build a tree, take its traversals, reconstruct, compare shapes.
bad = []
for n in range(1, 9):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        original = build(xs)
        pre, ino = preorder_model(original), inorder_model(original)
        if shape(s.buildTree(pre, ino)) != shape(original):
            bad.append(xs)
check("round-trips every small tree through its own traversals", bad, [])
# Instance state must be reset: a second call has to work.
check("reusable: same object, two calls",
      shape(s.buildTree([3,9,20,15,7], [9,3,15,20,7])),
      shape(s.buildTree([3,9,20,15,7], [9,3,15,20,7])))

print("LeetCode 110 - Balanced Binary Tree")
s = load("110-balanced-binary-tree.html", extra=TREE)
check("[3,9,20,null,null,15,7]", s.isBalanced(build([3,9,20,None,None,15,7])), True)
check("[1,2,2,3,3,null,null,4,4]",
      s.isBalanced(build([1,2,2,3,3,None,None,4,4])), False)
check("empty tree", s.isBalanced(None), True)
check("single node", s.isBalanced(build([1])), True)
check("[1,2,null,3] (chain of 3)", s.isBalanced(build([1,2,None,3])), False)
check("[1,2,3] ", s.isBalanced(build([1,2,3])), True)
# Balanced at the root, unbalanced deeper: the case "at every node" is about.
deep = ns94["TreeNode"](1)
deep.left = ns94["TreeNode"](2); deep.right = ns94["TreeNode"](3)
deep.left.left = ns94["TreeNode"](4); deep.left.left.left = ns94["TreeNode"](5)
check("root looks fine, imbalance is deeper", s.isBalanced(deep), False)
def balanced_model(node):
    def h(n):
        return 0 if n is None else 1 + max(h(n.left), h(n.right))
    if node is None:
        return True
    return (abs(h(node.left) - h(node.right)) <= 1
            and balanced_model(node.left) and balanced_model(node.right))

bad = []
for n in range(1, 10):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        if s.isBalanced(build(xs)) != balanced_model(build(xs)):
            bad.append(xs)
check("matches the naive definition on every small tree shape", bad, [])

print("LeetCode 111 - Minimum Depth of Binary Tree")
s = load("111-minimum-depth-of-binary-tree.html", extra=TREE)
check("[3,9,20,null,null,15,7]", s.minDepth(build([3,9,20,None,None,15,7])), 2)
check("[1,null,2] (THE case: 1 is not a leaf)", s.minDepth(build([1,None,2])), 2)
check("[2,null,3,null,4,null,5,null,6] (right chain)",
      s.minDepth(build([2,None,3,None,4,None,5,None,6])), 5)
check("empty tree", s.minDepth(None), 0)
check("single node", s.minDepth(build([1])), 1)
check("[1,2,null,3] (left chain)", s.minDepth(build([1,2,None,3])), 3)
check("[1,2,3]", s.minDepth(build([1,2,3])), 2)
def min_depth_model(node):
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    best = float("inf")
    if node.left:
        best = min(best, min_depth_model(node.left))
    if node.right:
        best = min(best, min_depth_model(node.right))
    return 1 + best

bad = []
for n in range(1, 10):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        if s.minDepth(build(xs)) != min_depth_model(build(xs)):
            bad.append(xs)
check("matches a leaf-aware model on every small tree shape", bad, [])
# minDepth must never exceed maxDepth, and equals it exactly on perfect trees.
maxd = load("104-maximum-depth-of-binary-tree.html", extra=TREE)
bad = []
for n in range(1, 9):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        if s.minDepth(build(xs)) > maxd.maxDepth(build(xs)):
            bad.append(xs)
check("minDepth never exceeds maxDepth", bad, [])
check("equal on a perfect tree", s.minDepth(build([1,2,3,4,5,6,7])), maxd.maxDepth(build([1,2,3,4,5,6,7])))
if hasattr(s, "minDepthBfs"):
    bad = []
    for n in range(1, 9):
        for mask in range(1 << (n - 1)):
            nxt = itertools.count(1)
            xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
            if s.minDepthBfs(build(xs)) != s.minDepth(build(xs)):
                bad.append(xs)
    check("[BFS version] agrees with the recursion", bad, [])

print("LeetCode 112 - Path Sum")
s = load("112-path-sum.html", extra=TREE)
big = build([5,4,8,11,None,13,4,7,2,None,None,None,1])
check("the canonical example, target 22", s.hasPathSum(big, 22), True)
check("same tree, target 26 (5+8+13)", s.hasPathSum(big, 26), True)
check("same tree, target 100", s.hasPathSum(big, 100), False)
check("[1,2,3] target 5", s.hasPathSum(build([1,2,3]), 5), False)
check("[1,2,3] target 3", s.hasPathSum(build([1,2,3]), 3), True)
check("empty tree, target 0 (no path at all)", s.hasPathSum(None, 0), False)
check("[1,2] target 1 -- THE base-case bug", s.hasPathSum(build([1,2]), 1), False)
check("[1,2] target 3", s.hasPathSum(build([1,2]), 3), True)
check("[-2,null,-3] target -5 (negatives)", s.hasPathSum(build([-2,None,-3]), -5), True)
check("single node matching", s.hasPathSum(build([7]), 7), True)
check("single node not matching", s.hasPathSum(build([7]), 0), False)
# Enumerate every root-to-leaf path and check membership.
def leaf_paths(node, acc=0):
    if node is None:
        return []
    acc += node.val
    if node.left is None and node.right is None:
        return [acc]
    return leaf_paths(node.left, acc) + leaf_paths(node.right, acc)

bad = []
for n in range(1, 8):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        sums = set(leaf_paths(build(xs)))
        for target in range(-2, 20):
            if s.hasPathSum(build(xs), target) != (target in sums):
                bad.append((xs, target))
check("matches root-to-leaf path enumeration on every small tree", bad, [])

print("LeetCode 114 - Flatten Binary Tree to Linked List")
s = load("114-flatten-binary-tree-to-linked-list.html", extra=TREE)
def flat(xs):
    tree = build(xs)
    s.flatten(tree)
    out, node = [], tree
    while node:
        if node.left is not None:
            return ("left pointer not nulled", out)
        out.append(node.val)
        node = node.right
    return out

def preorder_of(xs):
    def walk(n):
        return [] if n is None else [n.val] + walk(n.left) + walk(n.right)
    return walk(build(xs))

check("[1,2,5,3,4,null,6]", flat([1,2,5,3,4,None,6]), [1,2,3,4,5,6])
check("empty tree", flat([]), [])
check("single node", flat([0]), [0])
check("already a right chain", flat([1,None,2,None,3]), [1,2,3])
check("pure left chain", flat([1,2,None,3]), [1,2,3])
check("returns None (mutates in place)", s.flatten(build([1,2,3])), None)
bad = []
for n in range(1, 10):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        if flat(xs) != preorder_of(xs):
            bad.append((xs, flat(xs), preorder_of(xs)))
check("equals preorder with every left pointer nulled, on every small tree", bad, [])

print("LeetCode 118 - Pascal's Triangle")
s = load("118-pascals-triangle.html")
check("numRows=5", s.generate(5), [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]])
check("numRows=1", s.generate(1), [[1]])
check("numRows=0", s.generate(0), [])
bad = []
for n in range(0, 31):
    rows = s.generate(n)
    if len(rows) != n:
        bad.append(("count", n)); continue
    for r, row in enumerate(rows):
        if len(row) != r + 1:
            bad.append(("width", n, r)); break
        if row[0] != 1 or row[-1] != 1:
            bad.append(("edges", n, r)); break
        if row != [math.comb(r, c) for c in range(r + 1)]:
            bad.append(("values", n, r)); break
check("every row matches the binomial coefficients, for numRows 0..30", bad, [])

print("LeetCode 119 - Pascal's Triangle II")
s = load("119-pascals-triangle-ii.html")
check("rowIndex=3", s.getRow(3), [1,3,3,1])
check("rowIndex=0", s.getRow(0), [1])
check("rowIndex=1", s.getRow(1), [1,1])
check("rowIndex=4", s.getRow(4), [1,4,6,4,1])
bad = [k for k in range(0, 34) if s.getRow(k) != [math.comb(k, c) for c in range(k + 1)]]
check("matches the binomial coefficients for rowIndex 0..33", bad, [])
# Must agree with problem 118's last row.
triangle = load("118-pascals-triangle.html")
bad = [k for k in range(0, 31) if s.getRow(k) != triangle.generate(k + 1)[-1]]
check("agrees with the last row of problem 118 for every rowIndex 0..30", bad, [])
check("reusable: two calls give the same row", (s.getRow(5), s.getRow(5)),
      ([1,5,10,10,5,1], [1,5,10,10,5,1]))

print("LeetCode 122 - Best Time to Buy and Sell Stock II")
s = load("122-best-time-to-buy-and-sell-stock-ii.html")
check("[7,1,5,3,6,4]", s.maxProfit([7,1,5,3,6,4]), 7)
check("[1,2,3,4,5] (hold vs daily trades: same total)", s.maxProfit([1,2,3,4,5]), 4)
check("[7,6,4,3,1] (falling market)", s.maxProfit([7,6,4,3,1]), 0)
check("[1]", s.maxProfit([1]), 0)
check("[] (empty)", s.maxProfit([]), 0)
check("[2,2,2] (flat)", s.maxProfit([2,2,2]), 0)
check("[1,5,1,5,1,5]", s.maxProfit([1,5,1,5,1,5]), 12)
# Brute force: every sequence of non-overlapping buy/sell pairs.
def best_unlimited(prices):
    n = len(prices)
    if n < 2:
        return 0
    cash, hold = 0, -prices[0]
    for i in range(1, n):
        prev = cash
        cash = max(cash, hold + prices[i])
        hold = max(hold, prev - prices[i])
    return cash

bad = []
for n in range(0, 9):
    for combo in itertools.product([1, 2, 3], repeat=n):
        if s.maxProfit(list(combo)) != best_unlimited(list(combo)):
            bad.append(combo)
check("matches a two-state DP on every price series up to length 8 over {1,2,3}", bad, [])
# It must never do worse than the single-transaction answer from problem 121.
single = load("121-best-time-to-buy-and-sell-stock.html")
bad = []
for n in range(1, 9):
    for combo in itertools.product([1, 4, 2, 7], repeat=n):
        if s.maxProfit(list(combo)) < single.maxProfit(list(combo)):
            bad.append(combo)
check("never worse than the single-transaction answer (problem 121)", bad, [])

print("LeetCode 124 - Binary Tree Maximum Path Sum")
s = load("124-binary-tree-maximum-path-sum.html", extra=TREE)
check("[1,2,3]", s.maxPathSum(build([1,2,3])), 6)
check("[-10,9,20,null,null,15,7] (best path skips the root)",
      s.maxPathSum(build([-10,9,20,None,None,15,7])), 42)
check("[-3] (single negative -- must NOT return 0)", s.maxPathSum(build([-3])), -3)
check("[2,-1] (take the node alone)", s.maxPathSum(build([2,-1])), 2)
check("[1]", s.maxPathSum(build([1])), 1)
check("[-2,-1] ", s.maxPathSum(build([-2,-1])), -1)
check("all negative", s.maxPathSum(build([-5,-4,-3,-2,-1])), -1)
# Reuse: the field must be reset between calls.
check("reusable: same object, two calls",
      (s.maxPathSum(build([1,2,3])), s.maxPathSum(build([1,2,3]))), (6, 6))
# Brute force: every simple path in the tree, enumerated directly.
def all_path_sums(root):
    nodes = []
    def collect(n):
        if n:
            nodes.append(n); collect(n.left); collect(n.right)
    collect(root)
    best = None
    # A simple path in a tree is determined by its highest node and one or two
    # downward chains from it.
    def chains(n):
        """Every downward-path sum starting at n."""
        if n is None:
            return []
        out = [n.val]
        for child in (n.left, n.right):
            for c in chains(child):
                out.append(n.val + c)
        return out
    for n in nodes:
        left = chains(n.left) or []
        right = chains(n.right) or []
        cands = [n.val]
        cands += [n.val + c for c in left]
        cands += [n.val + c for c in right]
        cands += [n.val + a + b for a in left for b in right]
        top = max(cands)
        best = top if best is None else max(best, top)
    return best

bad = []
for n in range(1, 7):
    for mask in range(1 << (n - 1)):
        for vals in itertools.product([-3, -1, 2], repeat=n):
            it = iter(vals)
            xs, taken = [next(it)], 1
            for i in range(n - 1):
                xs.append(next(it) if (mask >> i & 1) else None)
            xs = [v for v in xs]
            tree = build(xs)
            present = [v for v in xs if v is not None]
            if len(present) == 0:
                continue
            got, want = s.maxPathSum(build(xs)), all_path_sums(build(xs))
            if got != want:
                bad.append((xs, got, want))
    if bad:
        break
check("matches exhaustive path enumeration on small trees over {-3,-1,2}", bad, [])

print("LeetCode 125 - Valid Palindrome")
s = load("125-valid-palindrome.html")
check('"A man, a plan, a canal: Panama"',
      s.isPalindrome("A man, a plan, a canal: Panama"), True)
check('"race a car"', s.isPalindrome("race a car"), False)
check('" " (empty after filtering)', s.isPalindrome(" "), True)
check('"" (empty)', s.isPalindrome(""), True)
check('"0P" -- THE trap: 0 and P differ by exactly 32', s.isPalindrome("0P"), False)
check('"ab_a" (underscore is not alphanumeric)', s.isPalindrome("ab_a"), True)
check('"a" (single)', s.isPalindrome("a"), True)
check('".,;:!" (pure punctuation)', s.isPalindrome(".,;:!"), True)
check('"aba" (odd length, middle vs itself)', s.isPalindrome("aba"), True)
check('"0p" (genuinely different letters)', s.isPalindrome("0p"), False)
check('"1a2" ', s.isPalindrome("1a2"), False)
check('"1a1" (digits count)', s.isPalindrome("1a1"), True)
# Cross-check against the clean-and-reverse model on generated strings.
def clean_model(text):
    cleaned = [c.lower() for c in text if c.isalnum()]
    return cleaned == cleaned[::-1]

bad = []
for n in range(0, 6):
    for combo in itertools.product("aA0P, ", repeat=n):
        text = "".join(combo)
        if s.isPalindrome(text) != clean_model(text):
            bad.append(text)
check("matches clean-and-reverse on every string up to length 5 over aA0P, and space", bad, [])

print("LeetCode 131 - Palindrome Partitioning")
s = load("131-palindrome-partitioning.html")
def parts(r):
    return sorted(tuple(x) for x in r)
check('"aab"', parts(s.partition("aab")), parts([["a","a","b"], ["aa","b"]]))
check('"a"', s.partition("a"), [["a"]])
check('"aba"', parts(s.partition("aba")), parts([["a","b","a"], ["aba"]]))
check('"abc" (only single characters)', s.partition("abc"), [["a","b","c"]])
check('"aaa" (all 4 cuts are valid)', len(s.partition("aaa")), 4)
# Independent model: every way to cut, filtered to all-palindrome pieces.
def partitions_model(text):
    out = []
    def go(start, path):
        if start == len(text):
            out.append(list(path)); return
        for end in range(start + 1, len(text) + 1):
            piece = text[start:end]
            if piece == piece[::-1]:
                path.append(piece); go(end, path); path.pop()
    go(0, [])
    return out

bad = []
for n in range(1, 8):
    for combo in itertools.product("ab", repeat=n):
        text = "".join(combo)
        if parts(s.partition(text)) != parts(partitions_model(text)):
            bad.append(text)
check("matches an independent model on every a/b string up to length 7", bad, [])
# Every returned piece must be a palindrome, and concatenate back to the input.
bad = []
for n in range(1, 7):
    for combo in itertools.product("aba", repeat=n):
        text = "".join(combo)
        for p in s.partition(text):
            if "".join(p) != text or any(x != x[::-1] for x in p):
                bad.append((text, p))
check("every piece is a palindrome and the pieces reassemble the input", bad, [])
# 2^(n-1) partitions for an all-same string, which is the worst case the post names.
bad = [n for n in range(1, 10) if len(s.partition("a" * n)) != 2 ** (n - 1)]
check("all-same string yields 2^(n-1) partitions", bad, [])

print("LeetCode 133 - Clone Graph")
GRAPHNODE = """
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def build_graph(adjacency):
    if not adjacency:
        return None
    nodes = [Node(i + 1) for i in range(len(adjacency))]
    for i, neighbors in enumerate(adjacency):
        nodes[i].neighbors = [nodes[j - 1] for j in neighbors]
    return nodes[0]
"""
nsg = {}
exec(compile(GRAPHNODE, "graphnode", "exec"), nsg)
build_graph = nsg["build_graph"]
s = load("133-clone-graph.html", extra=GRAPHNODE)

def graph_shape(node):
    """Adjacency by value, plus the set of object ids, for comparison."""
    seen, order = {}, []
    stack = [node] if node else []
    while stack:
        n = stack.pop()
        if id(n) in seen:
            continue
        seen[id(n)] = n
        order.append(n)
        stack.extend(n.neighbors)
    return ({n.val: sorted(x.val for x in n.neighbors) for n in order},
            {id(n) for n in order})

for adjacency, label in (([[2,4],[1,3],[2,4],[1,3]], "the 4-cycle"),
                         ([[]], "single node, no neighbours"),
                         ([], "empty graph"),
                         ([[2],[1]], "two nodes"),
                         ([[1]], "self loop")):
    original = build_graph(adjacency)
    copy = s.cloneGraph(original)
    if original is None:
        check(f"{label}: null in, null out", copy, None)
        continue
    orig_shape, orig_ids = graph_shape(original)
    copy_shape, copy_ids = graph_shape(copy)
    check(f"{label}: same structure", copy_shape, orig_shape)
    check(f"{label}: shares no node objects", orig_ids & copy_ids, set())
# Mutating the copy must not touch the original.
original = build_graph([[2,4],[1,3],[2,4],[1,3]])
copy = s.cloneGraph(original)
copy.val = 999
check("mutating the copy leaves the original alone", original.val, 1)
# Reuse: a second call must not return the first call's nodes.
first = s.cloneGraph(original)
second = s.cloneGraph(original)
check("two calls produce independent copies",
      graph_shape(first)[1] & graph_shape(second)[1], set())
if hasattr(s, "cloneGraphBfs"):
    bfs_copy = s.cloneGraphBfs(build_graph([[2,4],[1,3],[2,4],[1,3]]))
    check("[BFS version] same structure", graph_shape(bfs_copy)[0],
          graph_shape(build_graph([[2,4],[1,3],[2,4],[1,3]]))[0])

print("LeetCode 134 - Gas Station")
s = load("134-gas-station.html")
check("[1,2,3,4,5] / [3,4,5,1,2]", s.canCompleteCircuit([1,2,3,4,5], [3,4,5,1,2]), 3)
check("[2,3,4] / [3,4,3] (impossible)", s.canCompleteCircuit([2,3,4], [3,4,3]), -1)
check("[5] / [4]", s.canCompleteCircuit([5], [4]), 0)
check("[4] / [5]", s.canCompleteCircuit([4], [5]), -1)
check("[3,3,4] / [3,4,4] (impossible)", s.canCompleteCircuit([3,3,4], [3,4,4]), -1)
check("exact balance", s.canCompleteCircuit([1,2], [2,1]), 1)
# Brute force: simulate from every start.
def circuit_model(gas, cost):
    n = len(gas)
    for start in range(n):
        tank, ok = 0, True
        for step in range(n):
            i = (start + step) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                ok = False; break
        if ok:
            return start
    return -1

bad = []
for n in range(1, 6):
    for g in itertools.product([0, 1, 2], repeat=n):
        for c in itertools.product([0, 1, 2], repeat=n):
            got, want = s.canCompleteCircuit(list(g), list(c)), circuit_model(list(g), list(c))
            # The problem guarantees uniqueness, so the indices must match exactly.
            if got != want:
                bad.append((g, c, got, want))
check("matches simulation from every start, for all gas/cost up to length 5", bad, [])

print("LeetCode 136 - Single Number")
s = load("136-single-number.html")
check("[2,2,1]", s.singleNumber([2,2,1]), 1)
check("[4,1,2,1,2]", s.singleNumber([4,1,2,1,2]), 4)
check("[1] (single element)", s.singleNumber([1]), 1)
check("[-1,-1,-2] (negatives)", s.singleNumber([-1,-1,-2]), -2)
check("[0,1,0]", s.singleNumber([0,1,0]), 1)
check("large values do not overflow",
      s.singleNumber([2147483647, -2147483648, 2147483647]), -2147483648)
bad = []
for n in range(0, 6):
    for combo in itertools.combinations(range(-3, 6), n):
        for lone in range(-3, 6):
            if lone in combo:
                continue
            nums = [lone] + [x for v in combo for x in (v, v)]
            for perm in itertools.islice(itertools.permutations(nums), 24):
                if s.singleNumber(list(perm)) != lone:
                    bad.append(perm)
                    break
check("finds the lone value regardless of order, for many pairings", bad, [])
if hasattr(s, "singleNumberLoop"):
    bad = [xs for xs in ([2,2,1], [4,1,2,1,2], [1], [-1,-1,-2])
           if s.singleNumberLoop(list(xs)) != s.singleNumber(list(xs))]
    check("[explicit loop] agrees with the fold", bad, [])

print("LeetCode 138 - Copy List with Random Pointer")
RNODE = """
class Node:
    def __init__(self, x, next=None, random=None):
        self.val, self.next, self.random = x, next, random

def build_random_list(spec):
    if not spec:
        return None
    nodes = [Node(v) for v, _ in spec]
    for i, (_, r) in enumerate(spec):
        nodes[i].next = nodes[i + 1] if i + 1 < len(nodes) else None
        nodes[i].random = nodes[r] if r is not None else None
    return nodes[0]

def describe(head):
    order, node = {}, head
    while node:
        order[id(node)] = len(order)
        node = node.next
    out, node = [], head
    while node:
        out.append((node.val, order.get(id(node.random)) if node.random else None))
        node = node.next
    return out

def ids_of(head):
    out, node = set(), head
    while node:
        out.add(id(node)); node = node.next
    return out
"""
nsr = {}
exec(compile(RNODE, "rnode", "exec"), nsr)
build_random_list, describe, ids_of = nsr["build_random_list"], nsr["describe"], nsr["ids_of"]
s = load("138-copy-list-with-random-pointer.html", extra=RNODE)

SPECS = [
    [(7, None), (13, 0), (11, 4), (10, 2), (1, 0)],
    [(1, 1), (2, 1)],
    [(3, None), (3, None), (3, None)],
    [(1, 0)],
    [],
]
for spec in SPECS:
    original = build_random_list(spec)
    copy = s.copyRandomList(original)
    check(f"{len(spec)} nodes: structure preserved", describe(copy), describe(original))
    check(f"{len(spec)} nodes: shares no node objects", ids_of(original) & ids_of(copy), set())
    check(f"{len(spec)} nodes: original still intact", describe(original), spec if spec else [])
if hasattr(s, "copyRandomListInterweaved"):
    for spec in SPECS:
        original = build_random_list(spec)
        copy = s.copyRandomListInterweaved(original)
        check(f"[interweaved] {len(spec)} nodes: structure", describe(copy), describe(build_random_list(spec)))
        check(f"[interweaved] {len(spec)} nodes: ORIGINAL restored", describe(original), spec if spec else [])
        check(f"[interweaved] {len(spec)} nodes: no shared objects",
              ids_of(original) & ids_of(copy), set())

print("LeetCode 139 - Word Break")
s = load("139-word-break.html")
check('"leetcode" / [leet, code]', s.wordBreak("leetcode", ["leet","code"]), True)
check('"applepenapple" (reuse)', s.wordBreak("applepenapple", ["apple","pen"]), True)
check('"catsandog" (false)',
      s.wordBreak("catsandog", ["cats","dog","sand","and","cat"]), False)
check('"" (empty string)', s.wordBreak("", ["a"]), True)
check('"aaaaaa" / [aaaa, aaa] -- kills longest-first greedy',
      s.wordBreak("aaaaaa", ["aaaa","aaa"]), True)
check('"aaaaa" / [aaaa, aaa]', s.wordBreak("aaaaa", ["aaaa","aaa"]), False)
check('"a" / [] (empty dictionary)', s.wordBreak("a", []), False)
check('"cars" / [car, ca, rs]', s.wordBreak("cars", ["car","ca","rs"]), True)
# Independent model by explicit search with memoisation.
def breakable(text, words):
    words = set(words)
    @functools.lru_cache(maxsize=None)
    def go(i):
        if i == len(text):
            return True
        return any(text[i:j] in words and go(j) for j in range(i + 1, len(text) + 1))
    return go(0)

bad = []
for n in range(0, 8):
    for combo in itertools.product("ab", repeat=n):
        text = "".join(combo)
        for dictionary in (["a","b"], ["aa","b"], ["ab","a"], ["aaa","aa"], ["b"]):
            if s.wordBreak(text, list(dictionary)) != breakable(text, tuple(dictionary)):
                bad.append((text, dictionary))
check("matches memoised search on every a/b string up to length 7", bad, [])

print("LeetCode 141 - Linked List Cycle")
CYCLE = LISTNODE + """
def build_cycle(values, pos):
    head = to_list(values)
    if head is None or pos < 0:
        return head
    nodes, node = [], head
    while node:
        nodes.append(node); node = node.next
    nodes[-1].next = nodes[pos]
    return head
"""
nsc = {}
exec(compile(CYCLE, "cycle", "exec"), nsc)
build_cycle = nsc["build_cycle"]
s = load("141-linked-list-cycle.html", extra=CYCLE)
check("[3,2,0,-4] pos=1", s.hasCycle(build_cycle([3,2,0,-4], 1)), True)
check("[1,2] pos=0", s.hasCycle(build_cycle([1,2], 0)), True)
check("[1] pos=-1 (no cycle)", s.hasCycle(build_cycle([1], -1)), False)
check("[] (empty)", s.hasCycle(build_cycle([], -1)), False)
check("[1] pos=0 (self loop)", s.hasCycle(build_cycle([1], 0)), True)
check("[1,2,3,4] pos=-1", s.hasCycle(build_cycle([1,2,3,4], -1)), False)
check("[1,1] pos=-1 (equal VALUES, not a cycle)", s.hasCycle(build_cycle([1,1], -1)), False)
bad = []
for n in range(1, 10):
    for pos in range(-1, n):
        # both parities of length, and every cycle entry point
        if s.hasCycle(build_cycle(list(range(n)), pos)) != (pos >= 0):
            bad.append((n, pos))
check("every list length 1..9 against every cycle entry point", bad, [])

print("LeetCode 142 - Linked List Cycle II")
s = load("142-linked-list-cycle-ii.html", extra=CYCLE)
def entry_index(head, node):
    i, cur = 0, head
    while cur is not node:
        cur = cur.next; i += 1
    return i
head = build_cycle([3,2,0,-4], 1)
check("[3,2,0,-4] pos=1 returns the node at index 1", entry_index(head, s.detectCycle(head)), 1)
head = build_cycle([1,2], 0)
check("[1,2] pos=0 returns the head", s.detectCycle(head) is head, True)
check("[1] no cycle", s.detectCycle(build_cycle([1], -1)), None)
check("[] empty", s.detectCycle(build_cycle([], -1)), None)
head = build_cycle([1], 0)
check("self loop returns the node itself", s.detectCycle(head) is head, True)
bad = []
for n in range(1, 10):
    for pos in range(-1, n):
        head = build_cycle(list(range(n)), pos)
        got = s.detectCycle(head)
        if pos < 0:
            if got is not None:
                bad.append((n, pos, "expected None"))
        elif got is None or entry_index(head, got) != pos:
            bad.append((n, pos))
check("returns the exact entry node for every length and entry point", bad, [])

print("LeetCode 144 - Binary Tree Preorder Traversal")
s = load("144-binary-tree-preorder-traversal.html", extra=TREE)
def preorder_of_tree(node):
    return [] if node is None else [node.val] + preorder_of_tree(node.left) + preorder_of_tree(node.right)
check("[1,null,2,3]", s.preorderTraversal(build([1,None,2,3])), [1,2,3])
check("empty tree", s.preorderTraversal(None), [])
check("single node", s.preorderTraversal(build([1])), [1])
check("[4,2,6,1,3,5,7]", s.preorderTraversal(build([4,2,6,1,3,5,7])), [4,2,1,3,6,5,7])
bad = []
for n in range(1, 10):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        if s.preorderTraversal(build(xs)) != preorder_of_tree(build(xs)):
            bad.append(xs)
check("matches a recursive model on every small tree shape", bad, [])
# A left-leaning chain: the shape that would expose a push-order mistake.
check("left chain", s.preorderTraversal(build([1,2,None,3])), [1,2,3])
check("right chain", s.preorderTraversal(build([1,None,2,None,3])), [1,2,3])

print("LeetCode 145 - Binary Tree Postorder Traversal")
s = load("145-binary-tree-postorder-traversal.html", extra=TREE)
def postorder_of_tree(node):
    return [] if node is None else postorder_of_tree(node.left) + postorder_of_tree(node.right) + [node.val]
check("[1,null,2,3]", s.postorderTraversal(build([1,None,2,3])), [3,2,1])
check("empty tree", s.postorderTraversal(None), [])
check("single node", s.postorderTraversal(build([1])), [1])
check("[4,2,6,1,3,5,7]", s.postorderTraversal(build([4,2,6,1,3,5,7])), [1,3,2,5,7,6,4])
bad = []
for n in range(1, 10):
    for mask in range(1 << (n - 1)):
        nxt = itertools.count(1)
        xs = [next(nxt)] + [next(nxt) if (mask >> i & 1) else None for i in range(n - 1)]
        tree = build(xs)
        got = s.postorderTraversal(tree)
        if got != postorder_of_tree(build(xs)):
            bad.append(xs)
        elif got and got[-1] != xs[0]:
            bad.append(("root not last", xs))
check("matches a model, and the root is always last, on every small tree", bad, [])

print("LeetCode 146 - LRU Cache")
ns146 = {}
exec(compile("\n".join(blocks("146-lru-cache.html")), "lru", "exec"), ns146)
LRUCache = ns146["LRUCache"]
cache = LRUCache(2)
cache.put(1, 1); cache.put(2, 2)
check("get(1) after two puts", cache.get(1), 1)
cache.put(3, 3)                      # evicts 2, because get(1) counted as a use
check("get(2) evicted", cache.get(2), -1)
cache.put(4, 4)                      # evicts 1
check("get(1) evicted", cache.get(1), -1)
check("get(3)", cache.get(3), 3)
check("get(4)", cache.get(4), 4)
# put on an existing key must UPDATE, not insert a duplicate.
cache = LRUCache(2)
cache.put(1, 1); cache.put(1, 10); cache.put(2, 2)
check("update does not consume capacity", (cache.get(1), cache.get(2)), (10, 2))
# capacity 1
cache = LRUCache(1)
cache.put(1, 1); cache.put(2, 2)
check("capacity 1 evicts immediately", (cache.get(1), cache.get(2)), (-1, 2))
check("missing key returns -1", LRUCache(2).get(99), -1)
# Cross-check against a plain list-based model on a long random operation sequence.
class ModelLRU:
    def __init__(self, capacity):
        self.capacity, self.order, self.values = capacity, [], {}
    def get(self, key):
        if key not in self.values:
            return -1
        self.order.remove(key); self.order.append(key)
        return self.values[key]
    def put(self, key, value):
        if key in self.values:
            self.order.remove(key)
        elif len(self.order) == self.capacity:
            oldest = self.order.pop(0)
            del self.values[oldest]
        self.order.append(key); self.values[key] = value

rng = random.Random(20260902)
bad = []
for capacity in (1, 2, 3, 5):
    real, model = LRUCache(capacity), ModelLRU(capacity)
    for step in range(400):
        key = rng.randrange(6)
        if rng.random() < 0.5:
            if real.get(key) != model.get(key):
                bad.append((capacity, step, "get", key)); break
        else:
            value = rng.randrange(100)
            real.put(key, value); model.put(key, value)
check("matches a reference LRU over 400 random ops at four capacities", bad, [])

print("LeetCode 149 - Max Points on a Line")
s = load("149-max-points-on-a-line.html")
check("[[1,1],[2,2],[3,3]]", s.maxPoints([[1,1],[2,2],[3,3]]), 3)
check("the six-point example",
      s.maxPoints([[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]), 4)
check("single point", s.maxPoints([[1,1]]), 1)
check("two identical points", s.maxPoints([[1,1],[1,1]]), 2)
check("vertical line", s.maxPoints([[0,0],[0,1],[0,2]]), 3)
check("horizontal line", s.maxPoints([[0,5],[1,5],[2,5]]), 3)
check("two points", s.maxPoints([[0,0],[1,1]]), 2)
# Opposite directions from the anchor must count as ONE line.
check("points on both sides of the anchor", s.maxPoints([[-1,-1],[0,0],[1,1]]), 3)
# Large coordinates, where a floating-point slope key loses precision.
check("large collinear coordinates",
      s.maxPoints([[0,0],[94911151,94911150],[94911152,94911151]]), 2)
# Brute force over every pair-defined line, using exact integer collinearity.
def brute_points(pts):
    n = len(pts)
    if n <= 2:
        return n
    best = 1
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            (x1, y1), (x2, y2) = pts[i], pts[j]
            if (x1, y1) == (x2, y2):
                continue
            count = 0
            for (x, y) in pts:
                # cross product zero <=> collinear, exact integer arithmetic
                if (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) == 0:
                    count += 1
            best = max(best, count)
    # all points identical
    if best == 1:
        best = max(best, max(pts.count(p) for p in pts))
    return best

bad = []
coords = [(x, y) for x in range(3) for y in range(3)]
for n in range(1, 5):
    for combo in itertools.combinations_with_replacement(coords, n):
        pts = [list(p) for p in combo]
        got, want = s.maxPoints([list(p) for p in pts]), brute_points(list(combo))
        if got != want:
            bad.append((pts, got, want))
check("matches exact-collinearity brute force on every point set up to size 4", bad, [])

print()
if fails:
    print(f"{len(fails)} FAILURES:")
    for f in fails:
        print("  x", f)
    sys.exit(1)
print("all python solutions pass")
