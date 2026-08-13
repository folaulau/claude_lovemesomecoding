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


def load(name, extra=""):
    ns = {}
    src = extra + "\n" + "\n".join(blocks(name))
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

print()
if fails:
    print(f"{len(fails)} FAILURES:")
    for f in fails:
        print("  x", f)
    sys.exit(1)
print("all python solutions pass")
