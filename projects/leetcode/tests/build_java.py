"""Pull every Java block out of the round-1 posts and assemble a runnable test.

Each `class Solution` block becomes a uniquely named class so they can all live
in one file, and the loose method fragments are wrapped so they at least have to
compile. Everything comes straight from the published HTML.
"""
import html
import re
from pathlib import Path

POSTS = Path("/Users/folaukaveinga/Github/claude_lovemesomecoding/projects/leetcode/posts")
OUT = Path(__file__).parent / "Main.java"
JAVA = re.compile(r'<pre class="language-java"><code class="language-java">(.*?)</code></pre>', re.S)


def blocks(name):
    return [html.unescape(b) for b in JAVA.findall((POSTS / name).read_text())]


def rename(src, new):
    """`class Solution` -> `class <new>`, so every post's solution can coexist."""
    return re.sub(r'\bclass\s+Solution\b', f'class {new}', src)


parts = []


def solution(file, new):
    """The block that defines class Solution, renamed."""
    for b in blocks(file):
        if re.search(r'\bclass\s+Solution\b', b):
            parts.append(rename(b, new))
            return
    raise SystemExit(f"no class Solution in {file}")


def fragment(file, index, wrapper_name, extra=""):
    """A loose method, wrapped in a class so the compiler still checks it."""
    body = blocks(file)[index]
    parts.append(f"class {wrapper_name} {{\n{extra}\n{body}\n}}")


solution("001-two-sum.html", "S1")
solution("002-add-two-numbers.html", "S2")
solution("005-longest-palindromic-substring.html", "S5")
solution("007-reverse-integer.html", "S7")
solution("008-string-to-integer-atoi.html", "S8")
solution("009-palindrome-number.html", "S9")
solution("010-regular-expression-matching.html", "S10")
solution("012-integer-to-roman.html", "S12")
solution("013-roman-to-integer.html", "S13")
solution("014-longest-common-prefix.html", "S14")
solution("015-3sum.html", "S15")
solution("019-remove-nth-node-from-end-of-list.html", "S19")
solution("020-valid-parentheses.html", "S20")
solution("021-merge-two-sorted-lists.html", "S21")
solution("022-generate-parentheses.html", "S22")
solution("023-merge-k-sorted-lists.html", "S23")
solution("028-implement-strstr.html", "S28")
solution("031-next-permutation.html", "S31")
solution("033-search-in-rotated-sorted-array.html", "S33")
solution("034-find-first-and-last-position.html", "S34")
solution("036-valid-sudoku.html", "S36")
solution("039-combination-sum.html", "S39")
solution("040-combination-sum-ii.html", "S40")

# Fragments that are presented as alternatives rather than the main solution.
# LeetCode 1: the sorted two-pointer snippet is a bare loop; wrap it in a method.
two_pointer = blocks("001-two-sum.html")[-1]
parts.append("class S1TwoPointer {\n  int[] f(int[] nums, int target) {\n"
             + two_pointer + "\n    return new int[0];\n  }\n}")

# LeetCode 5: the interval-DP alternative.
fragment("005-longest-palindromic-substring.html", -1, "S5Dp")

# LeetCode 10: the top-down recursion, which needs no state beyond its arguments.
fragment("010-regular-expression-matching.html", 0, "S10Dfs",
         "  boolean isMatch(String s, String p) { return dfs(s, 0, p, 0); }")

# LeetCode 14: the sort-first-and-last alternative is a bare body; wrap it.
sort_trick = blocks("014-longest-common-prefix.html")[-1]
parts.append("class S14Sort {\n  String longestCommonPrefix(String[] strs) {\n"
             + sort_trick + "\n  }\n}")

# LeetCode 21: the one-line splice, shown on its own before the full solution.
splice = blocks("021-merge-two-sorted-lists.html")[0]
parts.append("class S21Splice {\n  void f(ListNode tail, ListNode list1, ListNode list2) {\n"
             + splice + "\n  }\n}")

# LeetCode 23: the min-heap alternative, presented as a loose method.
fragment("023-merge-k-sorted-lists.html", -1, "S23Heap")

# LeetCode 36: the bitmask alternative is a bare method body.
bits = blocks("036-valid-sudoku.html")[-1]
parts.append("class S36Bits {\n  boolean isValidSudoku(char[][] board) {\n" + bits + "\n  }\n}")

# LeetCode 40: the same-depth skip, shown on its own before the full solution.
skip = blocks("040-combination-sum-ii.html")[0]
parts.append("class S40Skip {\n  void f(int[] candidates, int start) {\n"
             + "    for (int i = start; i < candidates.length; i++) {\n"
             + skip + "\n    }\n  }\n}")

HEADER = """import java.util.*;

class ListNode {
    int val; ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}
"""

MAIN = """
public class Main {
    static int failures = 0;

    static void check(String label, Object got, Object want) {
        boolean ok = Objects.deepEquals(got, want);
        if (!ok) failures++;
        System.out.printf("  %s %s: %s%n", ok ? "ok  " : "FAIL", label, show(got));
    }

    static String show(Object o) {
        if (o instanceof int[] a) return Arrays.toString(a);
        return String.valueOf(o);
    }

    static int[] nextPerm(S31 s, int[] xs) { s.nextPermutation(xs); return xs; }

    static void permute(int[] xs, int k, List<int[]> out) {
        if (k == xs.length) { out.add(xs.clone()); return; }
        for (int i = k; i < xs.length; i++) {
            int t = xs[k]; xs[k] = xs[i]; xs[i] = t;
            permute(xs, k + 1, out);
            t = xs[k]; xs[k] = xs[i]; xs[i] = t;
        }
    }

    static char[][] grid(String[] rows) {
        char[][] g = new char[9][];
        for (int i = 0; i < 9; i++) g[i] = rows[i].toCharArray();
        return g;
    }

    /** Sorted multiset form, so result ordering does not matter. */
    static TreeSet<String> norm(List<List<Integer>> r) {
        TreeSet<String> out = new TreeSet<>();
        for (List<Integer> c : r) { List<Integer> cc = new ArrayList<>(c); Collections.sort(cc); out.add(cc.toString()); }
        return out;
    }

    static ListNode toList(int... xs) {
        ListNode head = new ListNode(0), tail = head;
        for (int x : xs) { tail.next = new ListNode(x); tail = tail.next; }
        return head.next;
    }

    static int[] toArr(ListNode n) {
        List<Integer> out = new ArrayList<>();
        for (; n != null; n = n.next) out.add(n.val);
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        System.out.println("LeetCode 1 - Two Sum");
        S1 s1 = new S1();
        check("[2,7,11,15] t=9", s1.twoSum(new int[]{2,7,11,15}, 9), new int[]{0,1});
        check("[3,2,4] t=6", s1.twoSum(new int[]{3,2,4}, 6), new int[]{1,2});
        check("[3,3] t=6 (duplicates)", s1.twoSum(new int[]{3,3}, 6), new int[]{0,1});
        check("[0,4,3,0] t=0", s1.twoSum(new int[]{0,4,3,0}, 0), new int[]{0,3});
        check("[-1,-2,-3,-4] t=-6", s1.twoSum(new int[]{-1,-2,-3,-4}, -6), new int[]{1,3});

        System.out.println("LeetCode 2 - Add Two Numbers");
        S2 s2 = new S2();
        check("342+465", toArr(s2.addTwoNumbers(toList(2,4,3), toList(5,6,4))), new int[]{7,0,8});
        check("999+1 (carry grows)", toArr(s2.addTwoNumbers(toList(9,9,9), toList(1))), new int[]{0,0,0,1});
        check("0+0", toArr(s2.addTwoNumbers(toList(0), toList(0))), new int[]{0});
        check("uneven lengths", toArr(s2.addTwoNumbers(toList(9,9,9,9,9,9,9), toList(9,9,9,9))),
              new int[]{8,9,9,9,0,0,0,1});

        System.out.println("LeetCode 5 - Longest Palindromic Substring");
        check("babad", Set.of("bab","aba").contains(new S5().longestPalindrome("babad")), true);
        check("cbbd (even centre)", new S5().longestPalindrome("cbbd"), "bb");
        check("abcdzdcab", new S5().longestPalindrome("abcdzdcab"), "cdzdc");
        check("a", new S5().longestPalindrome("a"), "a");
        check("'' (empty)", new S5().longestPalindrome(""), "");
        check("ac", Set.of("a","c").contains(new S5().longestPalindrome("ac")), true);
        check("aaaa", new S5().longestPalindrome("aaaa"), "aaaa");
        check("[dp] cbbd", new S5Dp().longestPalindrome("cbbd"), "bb");
        check("[dp] abcdzdcab", new S5Dp().longestPalindrome("abcdzdcab"), "cdzdc");
        check("[dp] '' (empty)", new S5Dp().longestPalindrome(""), "");
        check("[dp] a", new S5Dp().longestPalindrome("a"), "a");
        S5 reused = new S5();   // no instance state: a second call must not go stale
        reused.longestPalindrome("aaaa");
        check("reused instance", reused.longestPalindrome("cbbd"), "bb");

        System.out.println("LeetCode 7 - Reverse Integer");
        S7 s7 = new S7();
        check("123", s7.reverse(123), 321);
        check("-123", s7.reverse(-123), -321);
        check("120 (trailing zero)", s7.reverse(120), 21);
        check("0", s7.reverse(0), 0);
        check("1534236469 (overflows)", s7.reverse(1534236469), 0);
        check("-2147483648 (INT_MIN)", s7.reverse(-2147483648), 0);
        check("-2147483412", s7.reverse(-2147483412), -2143847412);

        System.out.println("LeetCode 8 - atoi");
        S8 s8 = new S8();
        check("\\"42\\"", s8.myAtoi("42"), 42);
        check("\\"   -42\\"", s8.myAtoi("   -42"), -42);
        check("\\"4193 with words\\"", s8.myAtoi("4193 with words"), 4193);
        check("\\"words and 987\\"", s8.myAtoi("words and 987"), 0);
        check("\\"-91283472332\\" (clamps)", s8.myAtoi("-91283472332"), Integer.MIN_VALUE);
        check("\\"91283472332\\" (clamps)", s8.myAtoi("91283472332"), Integer.MAX_VALUE);
        check("\\"+-12\\"", s8.myAtoi("+-12"), 0);
        check("\\"\\" (empty)", s8.myAtoi(""), 0);
        check("\\"   \\" (spaces only)", s8.myAtoi("   "), 0);
        check("\\"  0000123\\"", s8.myAtoi("  0000123"), 123);
        check("tab is not space", s8.myAtoi("\\t42"), 0);
        check("\\"-2147483648\\" (exactly INT_MIN)", s8.myAtoi("-2147483648"), Integer.MIN_VALUE);
        check("\\"2147483647\\" (exactly INT_MAX)", s8.myAtoi("2147483647"), Integer.MAX_VALUE);
        check("non-ASCII digit", s8.myAtoi("\\u0663"), 0);
        check("\\"+1\\"", s8.myAtoi("+1"), 1);
        check("\\"3.14\\"", s8.myAtoi("3.14"), 3);

        System.out.println("LeetCode 9 - Palindrome Number");
        S9 s9 = new S9();
        check("121", s9.isPalindrome(121), true);
        check("-121", s9.isPalindrome(-121), false);
        check("10 (trailing zero)", s9.isPalindrome(10), false);
        check("0", s9.isPalindrome(0), true);
        check("12321 (odd length)", s9.isPalindrome(12321), true);
        check("1221 (even length)", s9.isPalindrome(1221), true);
        check("1231", s9.isPalindrome(1231), false);
        check("2147483647", s9.isPalindrome(2147483647), false);

        System.out.println("LeetCode 10 - Regular Expression Matching");
        S10 a = new S10();
        S10Dfs b = new S10Dfs();
        String[][] cases = {
            {"aa","a","false"}, {"aa","a*","true"}, {"ab",".*","true"},
            {"aab","c*a*b","true"}, {"mississippi","mis*is*p*.","false"},
            {"","a*","true"}, {"","a*b*","true"}, {"",".","false"},
            {"","","true"}, {"a","","false"}, {"aaa","a*a","true"},
            {"aaaaaaaaaaaaaaaaaaab","a*a*a*a*a*b","true"},
        };
        for (String[] c : cases) {
            boolean want = Boolean.parseBoolean(c[2]);
            check("[dp]  \\"" + c[0] + "\\",\\"" + c[1] + "\\"", a.isMatch(c[0], c[1]), want);
            check("[dfs] \\"" + c[0] + "\\",\\"" + c[1] + "\\"", b.isMatch(c[0], c[1]), want);
        }

        System.out.println("LeetCode 12 - Integer to Roman");
        S12 s12 = new S12();
        check("3", s12.intToRoman(3), "III");
        check("4 (subtractive)", s12.intToRoman(4), "IV");
        check("9", s12.intToRoman(9), "IX");
        check("58", s12.intToRoman(58), "LVIII");
        check("1994 (CM XC IV)", s12.intToRoman(1994), "MCMXCIV");
        check("1 (min)", s12.intToRoman(1), "I");
        check("3999 (max)", s12.intToRoman(3999), "MMMCMXCIX");
        check("3888 (longest)", s12.intToRoman(3888), "MMMDCCCLXXXVIII");
        check("40", s12.intToRoman(40), "XL");
        check("400", s12.intToRoman(400), "CD");
        check("900", s12.intToRoman(900), "CM");

        System.out.println("LeetCode 13 - Roman to Integer");
        S13 s13 = new S13();
        check("III", s13.romanToInt("III"), 3);
        check("IV", s13.romanToInt("IV"), 4);
        check("IX", s13.romanToInt("IX"), 9);
        check("LVIII", s13.romanToInt("LVIII"), 58);
        check("MCMXCIV", s13.romanToInt("MCMXCIV"), 1994);
        check("MMMCMXCIX (max)", s13.romanToInt("MMMCMXCIX"), 3999);
        check("I (min)", s13.romanToInt("I"), 1);
        int bad = 0;
        for (int n = 1; n <= 3999; n++) {
            if (s13.romanToInt(s12.intToRoman(n)) != n) bad++;
        }
        check("12 <-> 13 round-trip, all 1..3999", bad, 0);

        System.out.println("LeetCode 14 - Longest Common Prefix");
        S14 s14 = new S14();
        check("flower/flow/flight", s14.longestCommonPrefix(new String[]{"flower","flow","flight"}), "fl");
        check("dog/racecar/car (none)", s14.longestCommonPrefix(new String[]{"dog","racecar","car"}), "");
        check("interspecies/...", s14.longestCommonPrefix(new String[]{"interspecies","interstellar","interstate"}), "inters");
        check("single string", s14.longestCommonPrefix(new String[]{"a"}), "a");
        check("empty array", s14.longestCommonPrefix(new String[]{}), "");
        check("null array", s14.longestCommonPrefix(null), "");
        check("empty string present", s14.longestCommonPrefix(new String[]{"ab",""}), "");
        check("shorter is the prefix", s14.longestCommonPrefix(new String[]{"flow","flower"}), "flow");
        check("all identical", s14.longestCommonPrefix(new String[]{"abc","abc"}), "abc");
        check("mismatch at column 0", s14.longestCommonPrefix(new String[]{"a","b"}), "");
        S14Sort s14b = new S14Sort();
        check("[sort] flower/flow/flight", s14b.longestCommonPrefix(new String[]{"flower","flow","flight"}), "fl");
        check("[sort] dog/racecar/car", s14b.longestCommonPrefix(new String[]{"dog","racecar","car"}), "");
        check("[sort] flow/flower", s14b.longestCommonPrefix(new String[]{"flow","flower"}), "flow");

        System.out.println("LeetCode 15 - 3Sum");
        S15 s15 = new S15();
        check("[-1,0,1,2,-1,-4]", s15.threeSum(new int[]{-1,0,1,2,-1,-4}),
              List.of(List.of(-1,-1,2), List.of(-1,0,1)));
        check("[0,1,1] (no answer)", s15.threeSum(new int[]{0,1,1}), List.of());
        check("[0,0,0]", s15.threeSum(new int[]{0,0,0}), List.of(List.of(0,0,0)));
        check("[0,0,0,0] (dup guard)", s15.threeSum(new int[]{0,0,0,0}), List.of(List.of(0,0,0)));
        check("[-2,0,0,2,2] (inner dup)", s15.threeSum(new int[]{-2,0,0,2,2}), List.of(List.of(-2,0,2)));
        check("[] (empty)", s15.threeSum(new int[]{}), List.of());
        check("[1,2] (too short)", s15.threeSum(new int[]{1,2}), List.of());
        check("all positive (early break)", s15.threeSum(new int[]{1,2,3,4}), List.of());
        check("[-1,-1,-1,2]", s15.threeSum(new int[]{-1,-1,-1,2}), List.of(List.of(-1,-1,2)));

        System.out.println("LeetCode 19 - Remove Nth Node From End");
        S19 s19 = new S19();
        check("1..5, n=2", toArr(s19.removeNthFromEnd(toList(1,2,3,4,5), 2)), new int[]{1,2,3,5});
        check("[1], n=1 (empties list)", toArr(s19.removeNthFromEnd(toList(1), 1)), new int[]{});
        check("[1,2], n=2 (removes head)", toArr(s19.removeNthFromEnd(toList(1,2), 2)), new int[]{2});
        check("[1,2], n=1 (removes tail)", toArr(s19.removeNthFromEnd(toList(1,2), 1)), new int[]{1});
        check("1..5, n=5 (removes head)", toArr(s19.removeNthFromEnd(toList(1,2,3,4,5), 5)), new int[]{2,3,4,5});
        check("1..5, n=1 (removes tail)", toArr(s19.removeNthFromEnd(toList(1,2,3,4,5), 1)), new int[]{1,2,3,4});

        System.out.println("LeetCode 20 - Valid Parentheses");
        S20 s20 = new S20();
        check("()", s20.isValid("()"), true);
        check("()[]{}", s20.isValid("()[]{}"), true);
        check("{[()]}", s20.isValid("{[()]}"), true);
        check("(] (wrong type)", s20.isValid("(]"), false);
        check("([)] (interleaved)", s20.isValid("([)]"), false);
        check("( (never closed)", s20.isValid("("), false);
        check(")( (closes nothing)", s20.isValid(")("), false);
        check("'' (empty)", s20.isValid(""), true);
        check("]", s20.isValid("]"), false);
        check("((((", s20.isValid("(((("), false);
        check("(((())))", s20.isValid("(((())))"), true);

        System.out.println("LeetCode 21 - Merge Two Sorted Lists");
        S21 s21 = new S21();
        check("[1,2,4] + [1,3,4]", toArr(s21.mergeTwoLists(toList(1,2,4), toList(1,3,4))),
              new int[]{1,1,2,3,4,4});
        check("both empty", toArr(s21.mergeTwoLists(null, null)), new int[]{});
        check("empty + [0]", toArr(s21.mergeTwoLists(null, toList(0))), new int[]{0});
        check("[0] + empty", toArr(s21.mergeTwoLists(toList(0), null)), new int[]{0});
        check("disjoint, l1 first", toArr(s21.mergeTwoLists(toList(1,2), toList(3,4))), new int[]{1,2,3,4});
        check("disjoint, l2 first", toArr(s21.mergeTwoLists(toList(3,4), toList(1,2))), new int[]{1,2,3,4});
        check("all equal", toArr(s21.mergeTwoLists(toList(2,2), toList(2,2))), new int[]{2,2,2,2});
        check("very uneven", toArr(s21.mergeTwoLists(toList(1), toList(2,3,4,5))), new int[]{1,2,3,4,5});

        System.out.println("LeetCode 22 - Generate Parentheses");
        S22 s22 = new S22();
        int[] catalan = {1, 1, 2, 5, 14, 42, 132, 429, 1430};
        check("n=1", s22.generateParenthesis(1), List.of("()"));
        check("n=3", new TreeSet<>(s22.generateParenthesis(3)),
              new TreeSet<>(List.of("((()))","(()())","(())()","()(())","()()()")));
        for (int n = 1; n <= 8; n++) {
            List<String> got = s22.generateParenthesis(n);
            check("n=" + n + ": count is Catalan(" + n + ")", got.size(), catalan[n]);
            check("n=" + n + ": all unique", new HashSet<>(got).size(), catalan[n]);
            boolean allGood = true;
            for (String x : got) {
                int d = 0;
                for (char c : x.toCharArray()) { d += (c == '(') ? 1 : -1; if (d < 0) allGood = false; }
                if (d != 0 || x.length() != 2 * n) allGood = false;
            }
            check("n=" + n + ": all well-formed and length 2n", allGood, true);
        }

        System.out.println("LeetCode 23 - Merge k Sorted Lists");
        S23 s23 = new S23();
        S23Heap s23h = new S23Heap();
        check("3 lists", toArr(s23.mergeKLists(new ListNode[]{toList(1,4,5), toList(1,3,4), toList(2,6)})),
              new int[]{1,1,2,3,4,4,5,6});
        check("empty array", toArr(s23.mergeKLists(new ListNode[]{})), new int[]{});
        check("null array", toArr(s23.mergeKLists(null)), new int[]{});
        check("[null] (null entry)", toArr(s23.mergeKLists(new ListNode[]{null})), new int[]{});
        check("nulls around a real list",
              toArr(s23.mergeKLists(new ListNode[]{null, toList(1,2), null})), new int[]{1,2});
        check("all null", toArr(s23.mergeKLists(new ListNode[]{null,null,null})), new int[]{});
        check("single list", toArr(s23.mergeKLists(new ListNode[]{toList(1,2,3)})), new int[]{1,2,3});
        check("negatives", toArr(s23.mergeKLists(new ListNode[]{toList(2,4), null, toList(-1)})),
              new int[]{-1,2,4});
        // The heap alternative must agree with divide and conquer.
        check("[heap] 3 lists",
              toArr(s23h.mergeKLists(new ListNode[]{toList(1,4,5), toList(1,3,4), toList(2,6)})),
              new int[]{1,1,2,3,4,4,5,6});
        check("[heap] nulls around a real list",
              toArr(s23h.mergeKLists(new ListNode[]{null, toList(1,2), null})), new int[]{1,2});
        check("[heap] all null", toArr(s23h.mergeKLists(new ListNode[]{null,null,null})), new int[]{});
        ListNode[] dcLists = new ListNode[7], heapLists = new ListNode[7];
        List<Integer> all = new ArrayList<>();
        for (int i = 0; i < 7; i++) {
            List<Integer> xs = new ArrayList<>();
            for (int v = i; v < 40; v += 7) { xs.add(v); all.add(v); }
            dcLists[i] = toList(xs.stream().mapToInt(Integer::intValue).toArray());
            heapLists[i] = toList(xs.stream().mapToInt(Integer::intValue).toArray());
        }
        Collections.sort(all);
        int[] want = all.stream().mapToInt(Integer::intValue).toArray();
        check("7 interleaved lists", toArr(s23.mergeKLists(dcLists)), want);
        check("[heap] 7 interleaved lists", toArr(s23h.mergeKLists(heapLists)), want);

        System.out.println("LeetCode 28 - Implement strStr");
        S28 s28 = new S28();
        check("sadbutsad / sad", s28.strStr("sadbutsad", "sad"), 0);
        check("leetcode / leeto", s28.strStr("leetcode", "leeto"), -1);
        check("empty needle", s28.strStr("hello", ""), 0);
        check("needle longer than haystack", s28.strStr("a", "aaaa"), -1);
        check("mississippi / issip", s28.strStr("mississippi", "issip"), 4);
        check("exact match (bound test)", s28.strStr("abc", "abc"), 0);
        check("worst case", s28.strStr("aaaaaaaaab", "aaab"), 6);
        check("both empty", s28.strStr("", ""), 0);
        check("empty haystack", s28.strStr("", "a"), -1);
        check("last position", s28.strStr("abc", "c"), 2);
        // Cross-check against String.indexOf over every a/b string up to length 4.
        List<String> hays = new ArrayList<>(List.of(""));
        for (int r = 1; r <= 4; r++) {
            List<String> next = new ArrayList<>();
            for (String h : hays) if (h.length() == r - 1) { next.add(h + "a"); next.add(h + "b"); }
            hays.addAll(next);
        }
        int disagree = 0;
        for (String h : hays) {
            for (String nd : List.of("a", "b", "ab", "ba", "aab", "abab")) {
                if (s28.strStr(h, nd) != h.indexOf(nd)) disagree++;
            }
        }
        check("agrees with String.indexOf on all a/b strings up to length 4", disagree, 0);

        System.out.println("LeetCode 31 - Next Permutation");
        S31 s31 = new S31();
        check("[1,2,3]", nextPerm(s31, new int[]{1,2,3}), new int[]{1,3,2});
        check("[1,3,2]", nextPerm(s31, new int[]{1,3,2}), new int[]{2,1,3});
        check("[3,2,1] (wraps)", nextPerm(s31, new int[]{3,2,1}), new int[]{1,2,3});
        check("[1,1,5] (duplicates)", nextPerm(s31, new int[]{1,1,5}), new int[]{1,5,1});
        check("[1] (single)", nextPerm(s31, new int[]{1}), new int[]{1});
        check("[2,2,2] (all equal)", nextPerm(s31, new int[]{2,2,2}), new int[]{2,2,2});
        check("[1,5,8,4,7,6,5,3,1]", nextPerm(s31, new int[]{1,5,8,4,7,6,5,3,1}),
              new int[]{1,5,8,5,1,3,4,6,7});
        check("[] (empty)", nextPerm(s31, new int[]{}), new int[]{});
        // Walk every permutation of 1..6 in lexicographic order and wrap.
        List<int[]> perms = new ArrayList<>();
        permute(new int[]{1,2,3,4,5,6}, 0, perms);
        perms.sort(Arrays::compare);
        boolean walked = true;
        for (int i = 0; i < perms.size(); i++) {
            int[] got = nextPerm(s31, perms.get(i).clone());
            if (!Arrays.equals(got, perms.get((i + 1) % perms.size()))) walked = false;
        }
        check("walks all " + perms.size() + " permutations of 1..6 in order, and wraps", walked, true);

        System.out.println("LeetCode 33 - Search in Rotated Sorted Array");
        S33 s33 = new S33();
        check("[4,5,6,7,0,1,2] t=0", s33.search(new int[]{4,5,6,7,0,1,2}, 0), 4);
        check("[4,5,6,7,0,1,2] t=3 (absent)", s33.search(new int[]{4,5,6,7,0,1,2}, 3), -1);
        check("[1] t=0", s33.search(new int[]{1}, 0), -1);
        check("[1] t=1", s33.search(new int[]{1}, 1), 0);
        check("[3,1] t=1", s33.search(new int[]{3,1}, 1), 1);
        check("[] (empty)", s33.search(new int[]{}, 5), -1);
        check("[1,2,3] unrotated t=3", s33.search(new int[]{1,2,3}, 3), 2);
        int rotBad = 0;
        for (int n = 1; n <= 8; n++) {
            for (int r = 0; r < n; r++) {
                int[] arr = new int[n];
                for (int i = 0; i < n; i++) arr[i] = (i + r) % n;
                for (int t2 = -1; t2 <= n; t2++) {
                    int expect = -1;
                    for (int i = 0; i < n; i++) if (arr[i] == t2) expect = i;
                    if (s33.search(arr, t2) != expect) rotBad++;
                }
            }
        }
        check("exhaustive: all rotations of size 1..8, all targets", rotBad, 0);

        System.out.println("LeetCode 34 - Find First and Last Position");
        S34 s34 = new S34();
        check("[5,7,7,8,8,10] t=8", s34.searchRange(new int[]{5,7,7,8,8,10}, 8), new int[]{3,4});
        check("[5,7,7,8,8,10] t=6 (absent)", s34.searchRange(new int[]{5,7,7,8,8,10}, 6), new int[]{-1,-1});
        check("[] (empty)", s34.searchRange(new int[]{}, 0), new int[]{-1,-1});
        check("[1,1,1,1,1] t=1 (all same)", s34.searchRange(new int[]{1,1,1,1,1}, 1), new int[]{0,4});
        check("[1] t=1", s34.searchRange(new int[]{1}, 1), new int[]{0,0});
        check("[2,2] t=1 (below all)", s34.searchRange(new int[]{2,2}, 1), new int[]{-1,-1});
        check("[2,2] t=3 (above all)", s34.searchRange(new int[]{2,2}, 3), new int[]{-1,-1});
        int rangeBad = 0;
        for (int n = 0; n <= 8; n++) {
            for (int mask = 0; mask < Math.pow(4, Math.min(n, 6)); mask++) {
                int[] xs = new int[n];
                int m = mask;
                for (int i = 0; i < n; i++) { xs[i] = m % 4; m /= 4; }
                Arrays.sort(xs);
                for (int t2 = -1; t2 <= 4; t2++) {
                    int lo = -1, hi = -1;
                    for (int i = 0; i < n; i++) if (xs[i] == t2) { if (lo == -1) lo = i; hi = i; }
                    if (!Arrays.equals(s34.searchRange(xs.clone(), t2), new int[]{lo, hi})) rangeBad++;
                }
            }
        }
        check("exhaustive: sorted arrays over 0..3", rangeBad, 0);

        System.out.println("LeetCode 36 - Valid Sudoku");
        S36 s36 = new S36();
        S36Bits s36b = new S36Bits();
        String[] good = {"53..7....", "6..195...", ".98....6.", "8...6...3",
                         "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"};
        check("valid board", s36.isValidSudoku(grid(good)), true);
        check("[bits] valid board", s36b.isValidSudoku(grid(good)), true);
        String[] dup = good.clone();
        dup[0] = "83..7....";                       // duplicate 8 in the top-left box
        check("duplicate in box", s36.isValidSudoku(grid(dup)), false);
        check("[bits] duplicate in box", s36b.isValidSudoku(grid(dup)), false);
        String[] blank = {".........", ".........", ".........", ".........", ".........",
                          ".........", ".........", ".........", "........."};
        check("all empty (dots must not clash)", s36.isValidSudoku(grid(blank)), true);
        char[][] rowDup = grid(blank); rowDup[0][0] = '1'; rowDup[0][8] = '1';
        check("duplicate in row", s36.isValidSudoku(rowDup), false);
        char[][] colDup = grid(blank); colDup[0][0] = '1'; colDup[8][0] = '1';
        check("duplicate in column", s36.isValidSudoku(colDup), false);
        char[][] boxDup = grid(blank); boxDup[0][0] = '1'; boxDup[2][2] = '1';
        check("duplicate in box only", s36.isValidSudoku(boxDup), false);
        char[][] fine = grid(blank); fine[0][0] = '1'; fine[3][3] = '1';
        check("same digit, different row/col/box", s36.isValidSudoku(fine), true);
        char[][] fine2 = grid(blank); fine2[0][3] = '1'; fine2[1][0] = '1';
        check("[bits] same digit, adjacent boxes", s36b.isValidSudoku(fine2), true);

        System.out.println("LeetCode 39 - Combination Sum");
        S39 s39 = new S39();
        check("[2,3,6,7] t=7", norm(s39.combinationSum(new int[]{2,3,6,7}, 7)),
              norm(List.of(List.of(2,2,3), List.of(7))));
        check("[2,3,5] t=8", norm(s39.combinationSum(new int[]{2,3,5}, 8)),
              norm(List.of(List.of(2,2,2,2), List.of(2,3,3), List.of(3,5))));
        check("[2] t=1 (unreachable)", s39.combinationSum(new int[]{2}, 1), List.of());
        check("[1] t=2 (reuse)", norm(s39.combinationSum(new int[]{1}, 2)), norm(List.of(List.of(1,1))));
        check("[8,7,4,3] t=11 (unsorted input)", norm(s39.combinationSum(new int[]{8,7,4,3}, 11)),
              norm(List.of(List.of(3,4,4), List.of(3,8), List.of(4,7))));

        System.out.println("LeetCode 40 - Combination Sum II");
        S40 s40 = new S40();
        check("[10,1,2,7,6,1,5] t=8", norm(s40.combinationSum2(new int[]{10,1,2,7,6,1,5}, 8)),
              norm(List.of(List.of(1,1,6), List.of(1,2,5), List.of(1,7), List.of(2,6))));
        check("[2,5,2,1,2] t=5", norm(s40.combinationSum2(new int[]{2,5,2,1,2}, 5)),
              norm(List.of(List.of(1,2,2), List.of(5))));
        check("[1,1] t=2 (both 1s usable)", norm(s40.combinationSum2(new int[]{1,1}, 2)),
              norm(List.of(List.of(1,1))));
        check("[1,1,1] t=1 (reported once)", norm(s40.combinationSum2(new int[]{1,1,1}, 1)),
              norm(List.of(List.of(1))));
        check("[2] t=1 (unreachable)", s40.combinationSum2(new int[]{2}, 1), List.of());
        // Cross-check against brute-force subset enumeration.
        int comboBad = 0;
        for (int[] cand : new int[][]{{1,1,2,2,3}, {2,3,6,7}, {1,1,1,1}, {4,4,2,1,4,2,2,1,3}}) {
            for (int t2 = 1; t2 <= 9; t2++) {
                TreeSet<String> expect = new TreeSet<>();
                for (int mask = 1; mask < (1 << cand.length); mask++) {
                    List<Integer> pick = new ArrayList<>();
                    int sum = 0;
                    for (int i = 0; i < cand.length; i++)
                        if ((mask & (1 << i)) != 0) { pick.add(cand[i]); sum += cand[i]; }
                    if (sum == t2) { Collections.sort(pick); expect.add(pick.toString()); }
                }
                TreeSet<String> got = new TreeSet<>();
                for (List<Integer> c : s40.combinationSum2(cand.clone(), t2)) {
                    List<Integer> cc = new ArrayList<>(c);
                    Collections.sort(cc);
                    got.add(cc.toString());
                }
                if (!got.equals(expect)) comboBad++;
            }
        }
        check("agrees with brute-force subset enumeration", comboBad, 0);

        System.out.println();
        if (failures > 0) {
            System.out.println(failures + " FAILURES");
            System.exit(1);
        }
        System.out.println("all java solutions pass");
    }
}
"""

OUT.write_text(HEADER + "\n" + "\n\n".join(parts) + "\n" + MAIN)
print(f"wrote {OUT} ({len(parts)} classes)")
