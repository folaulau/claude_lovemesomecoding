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
solution("121-best-time-to-buy-and-sell-stock.html", "S121")
solution("200-number-of-islands.html", "S200")
solution("347-top-k-frequent-elements.html", "S347")
solution("543-diameter-of-binary-tree.html", "S543")
solution("041-first-missing-positive.html", "S41")
solution("042-trapping-rain-water.html", "S42")
solution("043-multiply-strings.html", "S43")
solution("046-permutations.html", "S46")
solution("047-permutations-ii.html", "S47")
solution("049-group-anagrams.html", "S49")
solution("051-n-queens.html", "S51")
solution("052-n-queens-ii.html", "S52")
solution("053-maximum-subarray.html", "S53")
solution("055-jump-game.html", "S55")
solution("056-merge-intervals.html", "S56")
solution("057-insert-interval.html", "S57")
solution("058-length-of-last-word.html", "S58")
solution("062-unique-paths.html", "S62")
solution("063-unique-paths-ii.html", "S63")
solution("064-minimum-path-sum.html", "S64")
solution("065-valid-number.html", "S65")
solution("067-add-binary.html", "S67")
solution("068-text-justification.html", "S68")
solution("069-sqrtx.html", "S69")
solution("070-climbing-stairs.html", "S70")
solution("071-simplify-path.html", "S71")
solution("072-edit-distance.html", "S72")
solution("076-minimum-window-substring.html", "S76")
solution("078-subsets.html", "S78")
solution("081-search-in-rotated-sorted-array-ii.html", "S81")
solution("083-remove-duplicates-from-sorted-list.html", "S83")
solution("088-merge-sorted-array.html", "S88")
solution("091-decode-ways.html", "S91")
solution("094-binary-tree-inorder-traversal.html", "S94")
solution("098-validate-binary-search-tree.html", "S98")
solution("100-same-tree.html", "S100")
solution("101-symmetric-tree.html", "S101")
solution("102-binary-tree-level-order-traversal.html", "S102")
solution("103-binary-tree-zigzag-level-order-traversal.html", "S103")
solution("104-maximum-depth-of-binary-tree.html", "S104")
solution("105-construct-binary-tree-from-preorder-and-inorder-traversal.html", "S105")
solution("110-balanced-binary-tree.html", "S110")
solution("111-minimum-depth-of-binary-tree.html", "S111")
solution("112-path-sum.html", "S112")
solution("114-flatten-binary-tree-to-linked-list.html", "S114")
solution("118-pascals-triangle.html", "S118")
solution("119-pascals-triangle-ii.html", "S119")

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

# LeetCode 200: the BFS alternative, shown as a loose method.
fragment("200-number-of-islands.html", -1, "S200Bfs",
         "  int numIslands(char[][] g) {\n"
         "    int n = 0;\n"
         "    for (int r = 0; r < g.length; r++)\n"
         "      for (int c = 0; c < g[0].length; c++)\n"
         "        if (g[r][c] == '1') { n++; sinkBfs(g, r, c); }\n"
         "    return n;\n  }")

# LeetCode 347: the min-heap alternative is a bare fragment; wrap it.
heapfrag = blocks("347-top-k-frequent-elements.html")[-1]
parts.append("class S347Heap {\n"
             "  int[] topKFrequent(int[] nums, int k) {\n"
             "    Map<Integer, Integer> freq = new HashMap<>();\n"
             "    for (int num : nums) freq.merge(num, 1, Integer::sum);\n"
             + heapfrag + "\n"
             "    int[] out = new int[heap.size()];\n"
             "    for (int i = out.length - 1; i >= 0; i--) out[i] = heap.poll().getKey();\n"
             "    return out;\n  }\n}")

# LeetCode 42: the prefix/suffix-maxima alternative is a bare body.
prefix = blocks("042-trapping-rain-water.html")[-1]
parts.append("class S42Prefix {\n  int trap(int[] height) {\n" + prefix + "\n    return water;\n  }\n}")

# LeetCode 46: the swap-based variant, presented as a loose method.
swapvar = blocks("046-permutations.html")[-1]
parts.append("class S46Swap {\n"
             "  List<List<Integer>> permute(int[] nums) {\n"
             "    List<List<Integer>> r = new ArrayList<>();\n"
             "    permute(nums, 0, r);\n    return r;\n  }\n"
             "  void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }\n"
             + swapvar + "\n}")

# LeetCode 52: the bitmask variant, presented as a loose method.
fragment("052-n-queens-ii.html", -1, "S52Bits",
         "  int totalNQueens(int n) { return n == 0 ? 0 : place(n, 0, 0, 0); }")

# LeetCode 53: the index-tracking variant is a bare loop body; wrap it and expose
# the indices it computes so the test can check them.
idx = blocks("053-maximum-subarray.html")[-1]
parts.append("class S53Index {\n"
             "  int reportedStart, reportedEnd;\n"
             "  int maxSubArray(int[] nums) {\n"
             + idx + "\n"
             "    reportedStart = bestStart; reportedEnd = bestEnd;\n"
             "    return best;\n  }\n}")

# LeetCode 55: the backward greedy is a bare body.
backward = blocks("055-jump-game.html")[-1]
parts.append("class S55Backward {\n  boolean canJump(int[] nums) {\n"
             + backward + "\n  }\n}")

# LeetCode 58: the trim()/lastIndexOf one-liner is a bare body.
trimmed = blocks("058-length-of-last-word.html")[-1]
parts.append("class S58Trim {\n  int lengthOfLastWord(String s) {\n" + trimmed + "\n  }\n}")

# LeetCode 67: the XOR/AND adder, presented as a loose method.
fragment("067-add-binary.html", -1, "S67Bits")

# LeetCode 72: the one-row version with the carried diagonal.
onerow = blocks("072-edit-distance.html")[-1]
parts.append("class S72Row {\n  int minDistance(String word1, String word2) {\n"
             "    int m = word1.length(), n = word2.length();\n"
             + onerow + "\n    return row[n];\n  }\n}")

# LeetCode 78: the bitmask enumeration, presented as a loose method.
fragment("078-subsets.html", -1, "S78Bits")

# LeetCode 94: the recursive helper, shown before the iterative solution.
fragment("094-binary-tree-inorder-traversal.html", 0, "S94Recursive",
         "  List<Integer> inorderTraversal(TreeNode root) {\n"
         "    List<Integer> out = new ArrayList<>();\n"
         "    walk(root, out);\n    return out;\n  }")

# LeetCode 100: the queue-of-pairs variant, presented as a loose method.
fragment("100-same-tree.html", -1, "S100Iterative")

# LeetCode 101: the queue-of-pairs variant, presented as a loose method.
fragment("101-symmetric-tree.html", -1, "S101Iterative")

# LeetCode 112: the two-parallel-stacks variant, presented as a loose method.
fragment("112-path-sum.html", -1, "S112Iterative")

# --- legacy rewrites: bare static methods and fragments, each needing a wrapper ---
two = blocks("legacy-two-number-sum.html")
parts.append("class L2Brute {\n" + two[0] + "\n}")
parts.append("class L2Sort {\n" + two[1] + "\n}")
parts.append("class L2Set {\n" + two[2] + "\n}")
parts.append("class L2Idx {\n" + two[3] + "\n}")

three = blocks("legacy-three-number-sum.html")
parts.append("class L3 {\n" + three[0] + "\n}")
# The duplicate-skip snippet references loop variables; give it some.
parts.append("class L3Skip {\n  void f(int[] array, int i, int left, int right) {\n"
             "    while (true) {\n" + three[1] + "\n    break; }\n  }\n}")

rec = blocks("legacy-recursion.html")
parts.append("class RecDepth {\n  int call(TreeNode n) { return depth(n); }\n" + rec[0] + "\n}")
parts.append("class RecDiameter {\n  int best = 0;\n  int call(TreeNode n) { return depth(n); }\n" + rec[1] + "\n}")
parts.append("class RecFib {\n" + rec[2] + "\n}")
parts.append("class RecBacktrack {\n"
             "  java.util.List<java.util.List<Integer>> result = new ArrayList<>();\n"
             "  java.util.List<Integer> path = new ArrayList<>();\n"
             "  void backtrack(java.util.List<java.util.List<Integer>> result,\n"
             "                 java.util.List<Integer> path, int[] candidates,\n"
             "                 int start, int remaining) {}\n"
             "  void f(int[] candidates, int start, int remaining) {\n"
             + rec[3] + "\n  }\n}")

HEADER = """import java.util.*;

class TreeNode {
    int val; TreeNode left, right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
}

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

    /** Order-PRESERVING set of results. norm() sorts each inner list, which is
     *  right for combinations and destroys the distinction between permutations. */
    static TreeSet<String> permSet(List<List<Integer>> r) {
        TreeSet<String> out = new TreeSet<>();
        for (List<Integer> p : r) out.add(p.toString());
        return out;
    }

    /** Canonical, order-independent rendering of grouped strings. */
    static String groups(List<List<String>> gs) {
        List<String> out = new ArrayList<>();
        for (List<String> g : gs) { List<String> c = new ArrayList<>(g); Collections.sort(c); out.add(c.toString()); }
        Collections.sort(out);
        return out.toString();
    }

    /** Independent N-Queens validator: no two queens share a row, column or diagonal. */
    static boolean legalBoard(List<String> board) {
        int n = board.size();
        int[] col = new int[n];
        for (int r = 0; r < n; r++) {
            String row = board.get(r);
            if (row.length() != n || row.chars().filter(c -> c == 'Q').count() != 1) return false;
            if (row.chars().filter(c -> c == '.').count() != n - 1) return false;
            col[r] = row.indexOf('Q');
        }
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                if (col[i] == col[j] || Math.abs(i - j) == Math.abs(col[i] - col[j])) return false;
        return true;
    }

    /** Reachability by explicit search, to check Jump Game's greedy against. */
    static boolean reachable(int[] nums) {
        boolean[] seen = new boolean[nums.length];
        Deque<Integer> stack = new ArrayDeque<>();
        seen[0] = true; stack.push(0);
        while (!stack.isEmpty()) {
            int i = stack.pop();
            for (int j = i + 1; j <= Math.min(i + nums[i], nums.length - 1); j++)
                if (!seen[j]) { seen[j] = true; stack.push(j); }
        }
        return seen[nums.length - 1];
    }

    /** Intervals as a comparable string, so results can be compared directly. */
    static String ivs(int[][] xs) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < xs.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(Arrays.toString(xs[i]));
        }
        return sb.append("]").toString();
    }

    /** Count monotone right/down paths by explicit enumeration, obstacles honoured. */
    static int enumeratePaths(int[][] g) {
        int m = g.length, n = g[0].length;
        if (g[0][0] == 1 || g[m - 1][n - 1] == 1) return 0;
        int[][] memo = new int[m][n];
        for (int[] row : memo) Arrays.fill(row, -1);
        return pathsFrom(g, 0, 0, memo);
    }

    static int pathsFrom(int[][] g, int r, int c, int[][] memo) {
        int m = g.length, n = g[0].length;
        if (r == m - 1 && c == n - 1) return 1;
        if (memo[r][c] >= 0) return memo[r][c];
        int total = 0;
        if (r + 1 < m && g[r + 1][c] == 0) total += pathsFrom(g, r + 1, c, memo);
        if (c + 1 < n && g[r][c + 1] == 0) total += pathsFrom(g, r, c + 1, memo);
        return memo[r][c] = total;
    }

    /** Cheapest monotone path by explicit enumeration, to check the DP against. */
    static int enumerateBest(int[][] g, int r, int c) {
        int m = g.length, n = g[0].length;
        if (r == m - 1 && c == n - 1) return g[r][c];
        int best = Integer.MAX_VALUE;
        if (r + 1 < m) best = Math.min(best, enumerateBest(g, r + 1, c));
        if (c + 1 < n) best = Math.min(best, enumerateBest(g, r, c + 1));
        return g[r][c] + best;
    }

    /** Independent path canonicaliser, to check Simplify Path against. */
    static String canonical(String path) {
        Deque<String> out = new ArrayDeque<>();
        for (String part : path.split("/")) {
            if (part.isEmpty() || part.equals(".")) continue;
            if (part.equals("..")) out.pollLast();
            else out.addLast(part);
        }
        StringBuilder sb = new StringBuilder();
        for (String d : out) sb.append('/').append(d);
        return sb.length() == 0 ? "/" : sb.toString();
    }

    /** Independent Levenshtein distance. */
    static int lev(String a, String b) {
        int[] prev = new int[b.length() + 1];
        for (int j = 0; j <= b.length(); j++) prev[j] = j;
        for (int i = 1; i <= a.length(); i++) {
            int[] cur = new int[b.length() + 1];
            cur[0] = i;
            for (int j = 1; j <= b.length(); j++) {
                cur[j] = a.charAt(i - 1) == b.charAt(j - 1)
                        ? prev[j - 1]
                        : 1 + Math.min(prev[j - 1], Math.min(prev[j], cur[j - 1]));
            }
            prev = cur;
        }
        return prev[b.length()];
    }

    /** Does `window` contain every character of `t`, with multiplicity? */
    static boolean covers(String window, String t) {
        int[] have = new int[128];
        for (char c : window.toCharArray()) have[c]++;
        for (char c : t.toCharArray()) if (--have[c] < 0) return false;
        return true;
    }

    /** Shortest covering window by brute force. */
    static String bruteWindow(String s, String t) {
        if (t.isEmpty()) return "";
        String best = null;
        for (int i = 0; i < s.length(); i++)
            for (int j = i + 1; j <= s.length(); j++)
                if (covers(s.substring(i, j), t)) {
                    if (best == null || j - i < best.length()) best = s.substring(i, j);
                    break;
                }
        return best == null ? "" : best;
    }

    /** Count decodings by explicit enumeration. */
    static int countDecodings(String text) {
        if (text.isEmpty()) return 1;
        int total = 0;
        if (text.charAt(0) != '0') total += countDecodings(text.substring(1));
        if (text.length() >= 2) {
            int pair = Integer.parseInt(text.substring(0, 2));
            if (pair >= 10 && pair <= 26) total += countDecodings(text.substring(2));
        }
        return total;
    }

    static void inorderModel(TreeNode node, List<Integer> out) {
        if (node == null) return;
        inorderModel(node.left, out);
        out.add(node.val);
        inorderModel(node.right, out);
    }

    static boolean sameModel(TreeNode a, TreeNode b) {
        if (a == null && b == null) return true;
        if (a == null || b == null) return false;
        return a.val == b.val && sameModel(a.left, b.left) && sameModel(a.right, b.right);
    }

    static int depthModel(TreeNode node) {
        return node == null ? 0 : 1 + Math.max(depthModel(node.left), depthModel(node.right));
    }

    static boolean balancedModel(TreeNode node) {
        if (node == null) return true;
        return Math.abs(depthModel(node.left) - depthModel(node.right)) <= 1
                && balancedModel(node.left) && balancedModel(node.right);
    }

    static boolean mirrorModel(TreeNode a, TreeNode b) {
        if (a == null && b == null) return true;
        if (a == null || b == null) return false;
        return a.val == b.val && mirrorModel(a.left, b.right) && mirrorModel(a.right, b.left);
    }

    static void preorderModel(TreeNode node, List<Integer> out) {
        if (node == null) return;
        out.add(node.val);
        preorderModel(node.left, out);
        preorderModel(node.right, out);
    }

    /** Structural rendering, so two trees can be compared as strings. */
    static String shape(TreeNode node) {
        if (node == null) return ".";
        return "(" + node.val + " " + shape(node.left) + " " + shape(node.right) + ")";
    }

    /** Level-indexed traversal, as an independent model for problems 102 and 103. */
    static void levelsModel(TreeNode node, int depth, List<List<Integer>> acc) {
        if (node == null) return;
        if (depth == acc.size()) acc.add(new ArrayList<>());
        acc.get(depth).add(node.val);
        levelsModel(node.left, depth + 1, acc);
        levelsModel(node.right, depth + 1, acc);
    }

    /** Every distinct-valued tree shape on n slots, as level-order arrays. */
    static List<Integer[]> treeShapesOfSize(int n) {
        List<Integer[]> out = new ArrayList<>();
        for (int mask = 0; mask < (1 << (n - 1)); mask++) {
            Integer[] xs = new Integer[n];
            int next = 1;
            xs[0] = next++;
            for (int i = 1; i < n; i++) xs[i] = (mask >> (i - 1) & 1) == 1 ? next++ : null;
            out.add(xs);
        }
        return out;
    }

    /** Leaf-aware minimum depth, as an independent model. */
    static int minDepthModel(TreeNode node) {
        if (node == null) return 0;
        if (node.left == null && node.right == null) return 1;
        int best = Integer.MAX_VALUE;
        if (node.left != null) best = Math.min(best, minDepthModel(node.left));
        if (node.right != null) best = Math.min(best, minDepthModel(node.right));
        return 1 + best;
    }

    /** Every root-to-leaf path sum. */
    static void leafSums(TreeNode node, int acc, Set<Integer> out) {
        if (node == null) return;
        acc += node.val;
        if (node.left == null && node.right == null) { out.add(acc); return; }
        leafSums(node.left, acc, out);
        leafSums(node.right, acc, out);
    }

    /** Binomial coefficient, built multiplicatively so it does not overflow early. */
    static int binomial(int n, int k) {
        long r = 1;
        for (int i = 1; i <= k; i++) r = r * (n - k + i) / i;
        return (int) r;
    }

    static int[] sortedInts(int[] xs) { int[] c = xs.clone(); Arrays.sort(c); return c; }

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

    /** LeetCode level-order form; Integer null means a missing child. */
    static TreeNode buildTree(Integer... xs) {
        if (xs.length == 0 || xs[0] == null) return null;
        TreeNode root = new TreeNode(xs[0]);
        Deque<TreeNode> q = new ArrayDeque<>();
        q.add(root);
        int i = 1;
        while (!q.isEmpty() && i < xs.length) {
            TreeNode node = q.poll();
            if (i < xs.length) {
                Integer v = xs[i++];
                if (v != null) { node.left = new TreeNode(v); q.add(node.left); }
            }
            if (i < xs.length) {
                Integer v = xs[i++];
                if (v != null) { node.right = new TreeNode(v); q.add(node.right); }
            }
        }
        return root;
    }

    static char[][] toGrid(String... rows) {
        char[][] g = new char[rows.length][];
        for (int i = 0; i < rows.length; i++) g[i] = rows[i].toCharArray();
        return g;
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

        System.out.println("LeetCode 121 - Best Time to Buy and Sell Stock");
        S121 s121 = new S121();
        check("[7,1,5,3,6,4]", s121.maxProfit(new int[]{7,1,5,3,6,4}), 5);
        check("[7,6,4,3,1] (falling -> 0)", s121.maxProfit(new int[]{7,6,4,3,1}), 0);
        check("[1,2]", s121.maxProfit(new int[]{1,2}), 1);
        check("[5] (single day)", s121.maxProfit(new int[]{5}), 0);
        check("[] (empty)", s121.maxProfit(new int[]{}), 0);
        check("[2,2,2] (flat)", s121.maxProfit(new int[]{2,2,2}), 0);
        check("[3,2,6,5,0,3]", s121.maxProfit(new int[]{3,2,6,5,0,3}), 4);
        int profitBad = 0;
        for (int n = 0; n <= 6; n++) {
            for (int mask = 0; mask < (int) Math.pow(4, n); mask++) {
                int[] xs = new int[n];
                int m = mask;
                for (int i = 0; i < n; i++) { xs[i] = m % 4; m /= 4; }
                int expect = 0;
                for (int i = 0; i < n; i++)
                    for (int j = i + 1; j < n; j++) expect = Math.max(expect, xs[j] - xs[i]);
                if (s121.maxProfit(xs) != expect) profitBad++;
            }
        }
        check("agrees with brute force on all sequences over 0..3 up to length 6", profitBad, 0);

        System.out.println("LeetCode 200 - Number of Islands");
        S200 s200 = new S200();
        S200Bfs s200b = new S200Bfs();
        check("one island", s200.numIslands(toGrid("11110","11010","11000","00000")), 1);
        check("three islands", s200.numIslands(toGrid("11000","11000","00100","00011")), 3);
        check("all water", s200.numIslands(toGrid("000","000")), 0);
        check("all land", s200.numIslands(toGrid("111","111")), 1);
        check("single cell land", s200.numIslands(toGrid("1")), 1);
        check("null grid", s200.numIslands(null), 0);
        check("diagonal is NOT connected", s200.numIslands(toGrid("10","01")), 2);
        check("checkerboard", s200.numIslands(toGrid("101","010","101")), 5);
        check("single column", s200.numIslands(toGrid("1","0","1")), 2);
        check("snake (one long island)", s200.numIslands(toGrid("1111","0001","1111","1000")), 1);
        // The BFS alternative must agree with the DFS one everywhere.
        String[][] boards = {{"11110","11010","11000","00000"}, {"11000","11000","00100","00011"},
                             {"101","010","101"}, {"1111","0001","1111","1000"}, {"1"}, {"000","000"}};
        int bfsDisagree = 0;
        for (String[] board : boards) {
            if (s200.numIslands(toGrid(board)) != s200b.numIslands(toGrid(board))) bfsDisagree++;
        }
        check("[bfs] agrees with dfs on every board", bfsDisagree, 0);

        System.out.println("LeetCode 347 - Top K Frequent Elements");
        S347 s347 = new S347();
        S347Heap s347h = new S347Heap();
        check("[1,1,1,2,2,3] k=2", sortedInts(s347.topKFrequent(new int[]{1,1,1,2,2,3}, 2)), new int[]{1,2});
        check("[1] k=1", s347.topKFrequent(new int[]{1}, 1), new int[]{1});
        check("[1,2] k=2 (tie)", sortedInts(s347.topKFrequent(new int[]{1,2}, 2)), new int[]{1,2});
        check("k=1 with a tie returns exactly 1", s347.topKFrequent(new int[]{1,1,2,2}, 1).length, 1);
        check("all same value", s347.topKFrequent(new int[]{4,4,4,4}, 1), new int[]{4});
        check("negatives", sortedInts(s347.topKFrequent(new int[]{-1,-1,-2,-2,-2,3}, 2)), new int[]{-2,-1});
        check("[heap] [1,1,1,2,2,3] k=2", sortedInts(s347h.topKFrequent(new int[]{1,1,1,2,2,3}, 2)), new int[]{1,2});
        check("[heap] negatives", sortedInts(s347h.topKFrequent(new int[]{-1,-1,-2,-2,-2,3}, 2)), new int[]{-2,-1});

        System.out.println("LeetCode 543 - Diameter of Binary Tree");
        S543 s543 = new S543();
        check("[1,2,3,4,5]", s543.diameterOfBinaryTree(buildTree(1,2,3,4,5)), 3);
        check("[1,2]", s543.diameterOfBinaryTree(buildTree(1,2)), 1);
        check("[1] (single node)", s543.diameterOfBinaryTree(buildTree(1)), 0);
        check("null (empty tree)", s543.diameterOfBinaryTree(null), 0);
        TreeNode chain = new TreeNode(1), cur = chain;
        for (int v = 2; v <= 5; v++) { cur.left = new TreeNode(v); cur = cur.left; }
        check("left chain of 5", s543.diameterOfBinaryTree(chain), 4);
        check("reused instance", s543.diameterOfBinaryTree(buildTree(1,2)), 1);
        check("full tree of 7", s543.diameterOfBinaryTree(buildTree(1,2,3,4,5,6,7)), 4);
        check("diameter buried in the left subtree, not through the root",
              s543.diameterOfBinaryTree(buildTree(1,2,null,3,4,5,null,null,6)), 4);

        System.out.println("Legacy - Two Number Sum");
        int[][] pairCases = {{3,5,-4,8,11,1,-1,6}, {4,6}, {3}, {}, {5,1}, {-3,-7,-2}};
        int[] pairTargets = {10, 10, 6, 0, 10, -9};
        int[][] pairWant = {{-1,11}, {4,6}, {}, {}, {}, {-7,-2}};
        for (int i = 0; i < pairCases.length; i++) {
            check("[brute] case " + i, sortedInts(new L2Brute().twoNumberSum(pairCases[i].clone(), pairTargets[i])), pairWant[i]);
            check("[sort]  case " + i, sortedInts(new L2Sort().twoNumberSum(pairCases[i].clone(), pairTargets[i])), pairWant[i]);
            check("[set]   case " + i, sortedInts(new L2Set().twoNumberSum(pairCases[i].clone(), pairTargets[i])), pairWant[i]);
        }
        check("indices variant [2,7,11,15] t=9", new L2Idx().twoNumberSumIndices(new int[]{2,7,11,15}, 9), new int[]{0,1});
        check("indices variant, no pair", new L2Idx().twoNumberSumIndices(new int[]{1,2}, 99), new int[]{});
        // All three approaches must agree on every distinct-value array over -3..3.
        int agreeBad = 0;
        for (int mask = 0; mask < (1 << 7); mask++) {
            List<Integer> pick = new ArrayList<>();
            for (int bit = 0; bit < 7; bit++) if ((mask & (1 << bit)) != 0) pick.add(bit - 3);
            int[] xs = pick.stream().mapToInt(Integer::intValue).toArray();
            for (int t2 = -6; t2 <= 6; t2++) {
                boolean hasPair = false;
                for (int i = 0; i < xs.length; i++)
                    for (int j = i + 1; j < xs.length; j++) if (xs[i] + xs[j] == t2) hasPair = true;
                int[] byBrute = new L2Brute().twoNumberSum(xs.clone(), t2);
                int[] bySort = new L2Sort().twoNumberSum(xs.clone(), t2);
                int[] bySet = new L2Set().twoNumberSum(xs.clone(), t2);
                for (int[] got : new int[][]{byBrute, bySort, bySet}) {
                    boolean ok = hasPair ? (got.length == 2 && got[0] + got[1] == t2) : got.length == 0;
                    if (!ok) agreeBad++;
                }
            }
        }
        check("all three approaches agree with brute force over -3..3", agreeBad, 0);

        System.out.println("Legacy - Three Number Sum");
        L3 l3 = new L3();
        check("[12,3,1,2,-6,5,-8,6] t=0",
              l3.threeNumberSum(new int[]{12,3,1,2,-6,5,-8,6}, 0).toString(),
              "[[-8, 2, 6], [-8, 3, 5], [-6, 1, 5]]");
        check("[1,2,3] t=100 (none)", l3.threeNumberSum(new int[]{1,2,3}, 100), List.of());
        check("[1,2] t=3 (too short)", l3.threeNumberSum(new int[]{1,2}, 3), List.of());
        check("[] (empty)", l3.threeNumberSum(new int[]{}, 0), List.of());
        check("[1,2,3] t=6", l3.threeNumberSum(new int[]{1,2,3}, 6), List.of(List.of(1,2,3)));
        check("triplets come out ascending", l3.threeNumberSum(new int[]{5,1,3}, 9), List.of(List.of(1,3,5)));
        int tripleBad = 0;
        for (int mask = 0; mask < (1 << 9); mask++) {
            List<Integer> pick = new ArrayList<>();
            for (int bit = 0; bit < 9; bit++) if ((mask & (1 << bit)) != 0) pick.add(bit - 4);
            int[] xs = pick.stream().mapToInt(Integer::intValue).toArray();
            for (int t2 : new int[]{-3, 0, 3}) {
                TreeSet<String> expect = new TreeSet<>();
                for (int i = 0; i < xs.length; i++)
                    for (int j = i + 1; j < xs.length; j++)
                        for (int k = j + 1; k < xs.length; k++)
                            if (xs[i] + xs[j] + xs[k] == t2) {
                                List<Integer> tri = new ArrayList<>(List.of(xs[i], xs[j], xs[k]));
                                Collections.sort(tri);
                                expect.add(tri.toString());
                            }
                TreeSet<String> got = new TreeSet<>();
                for (List<Integer> tri : l3.threeNumberSum(xs.clone(), t2)) got.add(tri.toString());
                if (!got.equals(expect)) tripleBad++;
            }
        }
        check("agrees with brute force on all distinct arrays over -4..4", tripleBad, 0);

        System.out.println("Legacy - Recursion");
        check("depth of a 3-level tree", new RecDepth().call(buildTree(1,2,3,4,5)), 3);
        check("depth of null", new RecDepth().call(null), 0);
        RecDiameter rd = new RecDiameter();
        rd.call(buildTree(1,2,3,4,5));
        check("diameter snippet records 3", rd.best, 3);
        check("memoised fib(30)", new RecFib().fib(30, new Long[31]), 832040);
        check("memoised fib(0)", new RecFib().fib(0, new Long[1]), 0);
        check("memoised fib(1)", new RecFib().fib(1, new Long[2]), 1);
        check("naive fib(20) agrees with memoised", new RecFib().fib(20), new RecFib().fib(20, new Long[21]));

        System.out.println("LeetCode 41 - First Missing Positive");
        S41 s41 = new S41();
        check("[1,2,0]", s41.firstMissingPositive(new int[]{1,2,0}), 3);
        check("[3,4,-1,1]", s41.firstMissingPositive(new int[]{3,4,-1,1}), 2);
        check("[7,8,9,11,12]", s41.firstMissingPositive(new int[]{7,8,9,11,12}), 1);
        check("[1,2,3] (answer past the end)", s41.firstMissingPositive(new int[]{1,2,3}), 4);
        check("[] (empty)", s41.firstMissingPositive(new int[]{}), 1);
        check("[1,1] (duplicate guard, must terminate)", s41.firstMissingPositive(new int[]{1,1}), 2);
        check("[2,2,2]", s41.firstMissingPositive(new int[]{2,2,2}), 1);
        check("[-1,-2]", s41.firstMissingPositive(new int[]{-1,-2}), 1);
        int fmpBad = 0;
        for (int n = 0; n <= 6; n++) {
            for (int mask = 0; mask < (int) Math.pow(8, n); mask++) {
                int[] xs = new int[n];
                int mm = mask;
                for (int i = 0; i < n; i++) { xs[i] = (mm % 8) - 2; mm /= 8; }
                Set<Integer> present = new HashSet<>();
                for (int v : xs) present.add(v);
                int expect = 1;
                while (present.contains(expect)) expect++;
                if (s41.firstMissingPositive(xs.clone()) != expect) fmpBad++;
            }
        }
        check("exhaustive over values -2..5, lengths 0..6", fmpBad, 0);

        System.out.println("LeetCode 42 - Trapping Rain Water");
        S42 s42 = new S42();
        S42Prefix s42p = new S42Prefix();
        check("[0,1,0,2,1,0,1,3,2,1,2,1]", s42.trap(new int[]{0,1,0,2,1,0,1,3,2,1,2,1}), 6);
        check("[4,2,0,3,2,5]", s42.trap(new int[]{4,2,0,3,2,5}), 9);
        check("[] (empty)", s42.trap(new int[]{}), 0);
        check("[3] (single)", s42.trap(new int[]{3}), 0);
        check("[1,2,3,4] (increasing)", s42.trap(new int[]{1,2,3,4}), 0);
        check("[5,0,5]", s42.trap(new int[]{5,0,5}), 5);
        int trapBad = 0, trapPrefixBad = 0;
        for (int n = 0; n <= 7; n++) {
            for (int mask = 0; mask < (int) Math.pow(4, n); mask++) {
                int[] xs = new int[n];
                int mm = mask;
                for (int i = 0; i < n; i++) { xs[i] = mm % 4; mm /= 4; }
                int expect = 0;
                for (int i = 0; i < n; i++) {
                    int ml = 0, mr = 0;
                    for (int k = 0; k <= i; k++) ml = Math.max(ml, xs[k]);
                    for (int k = i; k < n; k++) mr = Math.max(mr, xs[k]);
                    expect += Math.min(ml, mr) - xs[i];
                }
                if (s42.trap(xs.clone()) != expect) trapBad++;
                if (s42p.trap(xs.clone()) != expect) trapPrefixBad++;
            }
        }
        check("two pointers agree with the per-column formula, all profiles over 0..3", trapBad, 0);
        check("[prefix] agrees too", trapPrefixBad, 0);

        System.out.println("LeetCode 43 - Multiply Strings");
        S43 s43 = new S43();
        check("2 x 3", s43.multiply("2", "3"), "6");
        check("123 x 456", s43.multiply("123", "456"), "56088");
        check("0 x 52 (must be 0)", s43.multiply("0", "52"), "0");
        check("0 x 0", s43.multiply("0", "0"), "0");
        check("11 x 11 (m+n-1 digits)", s43.multiply("11", "11"), "121");
        check("101 x 101 (interior zeros)", s43.multiply("101", "101"), "10201");
        int mulBad = 0;
        for (int x = 0; x < 60; x++)
            for (int y = 0; y < 60; y++)
                if (!s43.multiply(String.valueOf(x), String.valueOf(y)).equals(String.valueOf(x * y))) mulBad++;
        check("agrees with integer multiplication for all a,b in 0..59", mulBad, 0);
        check("60 digits x 60 digits", s43.multiply("9".repeat(60), "9".repeat(60)),
              new java.math.BigInteger("9".repeat(60)).multiply(new java.math.BigInteger("9".repeat(60))).toString());

        System.out.println("LeetCode 46 - Permutations");
        S46 s46 = new S46();
        S46Swap s46s = new S46Swap();
        check("[1,2,3] count", s46.permute(new int[]{1,2,3}).size(), 6);
        check("[1] (single)", s46.permute(new int[]{1}), List.of(List.of(1)));
        check("[] (empty yields one empty permutation)", s46.permute(new int[]{}).size(), 1);
        int fact = 1;
        for (int n = 1; n <= 6; n++) {
            fact *= n;
            int[] xs = new int[n];
            for (int i = 0; i < n; i++) xs[i] = i;
            List<List<Integer>> got = s46.permute(xs.clone());
            check("n=" + n + ": exactly " + fact + " permutations", got.size(), fact);
            check("n=" + n + ": all distinct", new HashSet<>(got).size(), fact);
            check("n=" + n + ": [swap] agrees",
                  permSet(s46s.permute(xs.clone())).equals(permSet(got)), true);
        }

        System.out.println("LeetCode 47 - Permutations II");
        S47 s47 = new S47();
        check("[1,1,2] (order matters: must be 3 distinct orderings)",
              permSet(s47.permuteUnique(new int[]{1,1,2})),
              permSet(List.of(List.of(1,1,2), List.of(1,2,1), List.of(2,1,1))));
        check("[1,2,3] (all distinct)", s47.permuteUnique(new int[]{1,2,3}).size(), 6);
        check("[2,2,2] (exactly one)", s47.permuteUnique(new int[]{2,2,2}), List.of(List.of(2,2,2)));
        check("[] (empty)", s47.permuteUnique(new int[]{}).size(), 1);
        int uniqBad = 0;
        for (int n = 1; n <= 6; n++) {
            for (int mask = 0; mask < (int) Math.pow(4, n); mask++) {
                int[] xs = new int[n];
                int mm = mask;
                int[] pool = {1, 1, 2, 3};
                for (int i = 0; i < n; i++) { xs[i] = pool[mm % 4]; mm /= 4; }
                List<List<Integer>> got = s47.permuteUnique(xs.clone());
                if (got.size() != new HashSet<>(got).size()) uniqBad++;     // no duplicates
                // every result is a rearrangement of the input multiset
                int[] sortedIn = xs.clone(); Arrays.sort(sortedIn);
                for (List<Integer> perm : got) {
                    int[] out = perm.stream().mapToInt(Integer::intValue).toArray();
                    Arrays.sort(out);
                    if (!Arrays.equals(out, sortedIn)) uniqBad++;
                }
            }
        }
        check("results are distinct rearrangements of the input multiset", uniqBad, 0);

        System.out.println("LeetCode 49 - Group Anagrams");
        S49 s49 = new S49();
        check("eat/tea/tan/ate/nat/bat", groups(s49.groupAnagrams(
                new String[]{"eat","tea","tan","ate","nat","bat"})),
              "[[ate, eat, tea], [bat], [nat, tan]]");
        check("empty string", groups(s49.groupAnagrams(new String[]{""})), "[[]]");
        check("[] (empty input)", s49.groupAnagrams(new String[]{}).size(), 0);
        check("no anagrams at all", s49.groupAnagrams(new String[]{"abc","def","ghi"}).size(), 3);
        String w1 = "a" + "b".repeat(11), w2 = "a".repeat(11) + "b";
        check("1a+11b must NOT group with 11a+1b", s49.groupAnagrams(new String[]{w1, w2}).size(), 2);
        check("genuine anagrams still group",
              s49.groupAnagrams(new String[]{w1, new StringBuilder(w1).reverse().toString()}).size(), 1);

        System.out.println("LeetCode 51 - N-Queens");
        S51 s51 = new S51();
        check("n=1", s51.solveNQueens(1), List.of(List.of("Q")));
        check("n=2 (no solutions, not an error)", s51.solveNQueens(2).size(), 0);
        check("n=3 (no solutions)", s51.solveNQueens(3).size(), 0);
        check("n=4 exact boards",
              new TreeSet<>(List.of(s51.solveNQueens(4).get(0).toString(),
                                    s51.solveNQueens(4).get(1).toString())),
              new TreeSet<>(List.of(List.of(".Q..", "...Q", "Q...", "..Q.").toString(),
                                    List.of("..Q.", "Q...", "...Q", ".Q..").toString())));
        int[] queenCounts = {1, 0, 0, 2, 10, 4, 40, 92, 352};
        for (int n = 1; n <= 9; n++) {
            List<List<String>> nq = s51.solveNQueens(n);
            check("n=" + n + ": " + queenCounts[n - 1] + " solutions", nq.size(), queenCounts[n - 1]);
            boolean allLegal = true;
            for (List<String> nqBoard : nq) if (!legalBoard(nqBoard)) allLegal = false;
            check("n=" + n + ": every board is legal", allLegal, true);
            check("n=" + n + ": all boards distinct", new HashSet<>(nq).size(), queenCounts[n - 1]);
        }
        check("reusable: n=6 twice", s51.solveNQueens(6).equals(s51.solveNQueens(6)), true);

        System.out.println("LeetCode 52 - N-Queens II");
        S52 s52 = new S52();
        S52Bits s52b = new S52Bits();
        for (int n = 1; n <= 9; n++) {
            check("n=" + n, s52.totalNQueens(n), queenCounts[n - 1]);
            check("n=" + n + ": [bitmask] agrees", s52b.totalNQueens(n), queenCounts[n - 1]);
            check("n=" + n + ": agrees with problem 51",
                  s52.totalNQueens(n), s51.solveNQueens(n).size());
        }
        // The marks are shared across branches, so a missing undo shows up here.
        check("reusable: n=8 twice", s52.totalNQueens(8) + s52.totalNQueens(8), 184);

        System.out.println("LeetCode 53 - Maximum Subarray");
        S53 s53 = new S53();
        S53Index s53i = new S53Index();
        check("[-2,1,-3,4,-1,2,1,-5,4]", s53.maxSubArray(new int[]{-2,1,-3,4,-1,2,1,-5,4}), 6);
        check("[1]", s53.maxSubArray(new int[]{1}), 1);
        check("[5,4,-1,7,8]", s53.maxSubArray(new int[]{5,4,-1,7,8}), 23);
        check("[-1] (single negative)", s53.maxSubArray(new int[]{-1}), -1);
        check("[-3,-1,-2] (ALL negative: must not return 0)",
              s53.maxSubArray(new int[]{-3,-1,-2}), -1);
        check("[0]", s53.maxSubArray(new int[]{0}), 0);
        check("[5,4,-1,7,8,-100] (run in progress is not the answer)",
              s53.maxSubArray(new int[]{5,4,-1,7,8,-100}), 23);
        check("[-1,-2,-3,100]", s53.maxSubArray(new int[]{-1,-2,-3,100}), 100);
        check("[index variant] [-2,1,-3,4,-1,2,1,-5,4] sum",
              s53i.maxSubArray(new int[]{-2,1,-3,4,-1,2,1,-5,4}), 6);
        check("[index variant] ...and reports [3,6]",
              s53i.reportedStart + "," + s53i.reportedEnd, "3,6");
        int kadaneBad = 0, idxBad = 0;
        int[] alphabet = {-2, -1, 0, 1, 3};
        for (int n = 1; n <= 6; n++) {
            int combos = (int) Math.pow(alphabet.length, n);
            for (int mask = 0; mask < combos; mask++) {
                int[] xs = new int[n];
                int mm = mask;
                for (int i = 0; i < n; i++) { xs[i] = alphabet[mm % alphabet.length]; mm /= alphabet.length; }
                int bestSum = Integer.MIN_VALUE;
                for (int i = 0; i < n; i++) {
                    int run = 0;
                    for (int j = i; j < n; j++) { run += xs[j]; bestSum = Math.max(bestSum, run); }
                }
                if (s53.maxSubArray(xs.clone()) != bestSum) kadaneBad++;
                S53Index fresh = new S53Index();
                int got = fresh.maxSubArray(xs.clone());
                int slice = 0;
                for (int k = fresh.reportedStart; k <= fresh.reportedEnd; k++) slice += xs[k];
                if (got != bestSum || slice != bestSum) idxBad++;   // the reported slice must sum to it
            }
        }
        check("matches brute force on every array of length 1..6 over {-2,-1,0,1,3}", kadaneBad, 0);
        check("index variant's reported slice actually sums to the answer", idxBad, 0);

        System.out.println("LeetCode 55 - Jump Game");
        S55 s55 = new S55();
        S55Backward s55b = new S55Backward();
        check("[2,3,1,1,4]", s55.canJump(new int[]{2,3,1,1,4}), true);
        check("[3,2,1,0,4] (index 3 is a dead end)", s55.canJump(new int[]{3,2,1,0,4}), false);
        check("[0] (already at the last index)", s55.canJump(new int[]{0}), true);
        check("[1,0]", s55.canJump(new int[]{1,0}), true);
        check("[0,1]", s55.canJump(new int[]{0,1}), false);
        check("[2,0,0]", s55.canJump(new int[]{2,0,0}), true);
        check("[5,0,0,0,0,0]", s55.canJump(new int[]{5,0,0,0,0,0}), true);
        int jumpBad = 0, jumpBackBad = 0;
        for (int n = 1; n <= 7; n++) {
            int combos = (int) Math.pow(4, n);
            for (int mask = 0; mask < combos; mask++) {
                int[] xs = new int[n];
                int mm = mask;
                for (int i = 0; i < n; i++) { xs[i] = mm % 4; mm /= 4; }
                boolean canReach = reachable(xs.clone());
                if (s55.canJump(xs.clone()) != canReach) jumpBad++;
                if (s55b.canJump(xs.clone()) != canReach) jumpBackBad++;
            }
        }
        check("matches explicit reachability on every array of length 1..7 over {0,1,2,3}", jumpBad, 0);
        check("[backward] agrees on the same inputs", jumpBackBad, 0);

        System.out.println("LeetCode 56 - Merge Intervals");
        S56 s56 = new S56();
        check("[[1,3],[2,6],[8,10],[15,18]]",
              ivs(s56.merge(new int[][]{{1,3},{2,6},{8,10},{15,18}})), "[[1, 6], [8, 10], [15, 18]]");
        check("[[1,4],[4,5]] (touching merges)",
              ivs(s56.merge(new int[][]{{1,4},{4,5}})), "[[1, 5]]");
        check("[[1,4],[0,4]] (unsorted input)",
              ivs(s56.merge(new int[][]{{1,4},{0,4}})), "[[0, 4]]");
        check("[[1,4],[2,3]] (fully contained -- the max(end) case)",
              ivs(s56.merge(new int[][]{{1,4},{2,3}})), "[[1, 4]]");
        check("[[1,10],[2,3],[4,5]] (several contained)",
              ivs(s56.merge(new int[][]{{1,10},{2,3},{4,5}})), "[[1, 10]]");
        check("[[1,4],[5,6]] (adjacent but not touching)",
              ivs(s56.merge(new int[][]{{1,4},{5,6}})), "[[1, 4], [5, 6]]");
        check("[[1,4]] (single)", ivs(s56.merge(new int[][]{{1,4}})), "[[1, 4]]");
        check("[] (empty)", s56.merge(new int[][]{}).length, 0);
        // The comparator must not overflow, and the caller's arrays must survive.
        check("extreme bounds do not overflow the comparator",
              ivs(s56.merge(new int[][]{{Integer.MAX_VALUE - 1, Integer.MAX_VALUE},
                                        {Integer.MIN_VALUE, Integer.MIN_VALUE + 1}})),
              "[[" + Integer.MIN_VALUE + ", " + (Integer.MIN_VALUE + 1) + "], ["
                   + (Integer.MAX_VALUE - 1) + ", " + Integer.MAX_VALUE + "]]");
        int[][] src = {{1,10},{2,3}};
        s56.merge(new int[][]{src[0].clone(), src[1].clone()});
        int[][] src2 = {{1,10},{2,3}};
        s56.merge(src2);
        check("does not mutate the caller's intervals", ivs(src2), "[[1, 10], [2, 3]]");

        System.out.println("LeetCode 57 - Insert Interval");
        S57 s57 = new S57();
        check("[[1,3],[6,9]] + [2,5]",
              ivs(s57.insert(new int[][]{{1,3},{6,9}}, new int[]{2,5})), "[[1, 5], [6, 9]]");
        check("[[1,2],[3,5],[6,7],[8,10],[12,16]] + [4,8]",
              ivs(s57.insert(new int[][]{{1,2},{3,5},{6,7},{8,10},{12,16}}, new int[]{4,8})),
              "[[1, 2], [3, 10], [12, 16]]");
        check("[] + [5,7]", ivs(s57.insert(new int[][]{}, new int[]{5,7})), "[[5, 7]]");
        check("[[1,5]] + [2,3] (swallowed)",
              ivs(s57.insert(new int[][]{{1,5}}, new int[]{2,3})), "[[1, 5]]");
        check("[[1,5]] + [6,8] (after everything)",
              ivs(s57.insert(new int[][]{{1,5}}, new int[]{6,8})), "[[1, 5], [6, 8]]");
        check("[[1,5]] + [0,0] (before everything)",
              ivs(s57.insert(new int[][]{{1,5}}, new int[]{0,0})), "[[0, 0], [1, 5]]");
        check("[[1,5]] + [5,7] (touching on the right merges)",
              ivs(s57.insert(new int[][]{{1,5}}, new int[]{5,7})), "[[1, 7]]");
        check("[[3,5]] + [1,3] (touching on the left merges)",
              ivs(s57.insert(new int[][]{{3,5}}, new int[]{1,3})), "[[1, 5]]");
        check("[[3,5]] + [4,8] (min() case: starts at 3, not 4)",
              ivs(s57.insert(new int[][]{{3,5}}, new int[]{4,8})), "[[3, 8]]");
        check("[[1,2],[3,10]] + [2,4] (running end chains)",
              ivs(s57.insert(new int[][]{{1,2},{3,10}}, new int[]{2,4})), "[[1, 10]]");
        // Must agree with the correct-but-slower append-sort-merge answer.
        int insBad = 0;
        for (int n = 0; n <= 4; n++) {
            int[][] base = new int[n][];
            for (int i = 0; i < n; i++) base[i] = new int[]{2 * i, 2 * i + 1};
            for (int lo = -1; lo <= 2 * n + 1; lo++) {
                for (int hi = lo; hi <= 2 * n + 2; hi++) {
                    int[][] copy = new int[n][];
                    for (int i = 0; i < n; i++) copy[i] = base[i].clone();
                    String got = ivs(s57.insert(copy, new int[]{lo, hi}));

                    int[][] combined = new int[n + 1][];
                    for (int i = 0; i < n; i++) combined[i] = base[i].clone();
                    combined[n] = new int[]{lo, hi};
                    String viaMerge = ivs(s56.merge(combined));
                    if (!got.equals(viaMerge)) insBad++;
                }
            }
        }
        check("agrees with sort-then-merge on every insertion into a sorted list", insBad, 0);

        System.out.println("LeetCode 58 - Length of Last Word");
        S58 s58 = new S58();
        S58Trim s58t = new S58Trim();
        check("Hello World", s58.lengthOfLastWord("Hello World"), 5);
        check("trailing spaces and runs of spaces",
              s58.lengthOfLastWord("   fly me   to   the moon  "), 4);
        check("luffy is still joyboy", s58.lengthOfLastWord("luffy is still joyboy"), 6);
        check("single char, no space at all (the i >= 0 guard)", s58.lengthOfLastWord("a"), 1);
        check("a with one trailing space", s58.lengthOfLastWord("a "), 1);
        check("day", s58.lengthOfLastWord("day"), 3);
        check("leading spaces only", s58.lengthOfLastWord("   day"), 3);
        int wordBad = 0, trimBad = 0;
        for (int n = 1; n <= 7; n++) {
            for (int mask = 0; mask < (1 << n); mask++) {
                StringBuilder sb = new StringBuilder();
                for (int i = 0; i < n; i++) sb.append((mask >> i & 1) == 1 ? 'a' : ' ');
                String text = sb.toString();
                if (text.trim().isEmpty()) continue;   // at least one word is guaranteed
                String[] words = text.trim().split("\\s+");
                int lastLen = words[words.length - 1].length();
                if (s58.lengthOfLastWord(text) != lastLen) wordBad++;
                if (s58t.lengthOfLastWord(text) != lastLen) trimBad++;
            }
        }
        check("agrees with split on every a/space string up to length 7", wordBad, 0);
        check("[trim/lastIndexOf] agrees on the same inputs", trimBad, 0);

        System.out.println("LeetCode 62 - Unique Paths");
        S62 s62 = new S62();
        check("m=3 n=7", s62.uniquePaths(3, 7), 28);
        check("m=3 n=2", s62.uniquePaths(3, 2), 3);
        check("m=1 n=1 (already there)", s62.uniquePaths(1, 1), 1);
        check("m=1 n=10 (a corridor)", s62.uniquePaths(1, 10), 1);
        check("m=10 n=1 (the other corridor)", s62.uniquePaths(10, 1), 1);
        check("m=7 n=3 (symmetric)", s62.uniquePaths(7, 3), 28);
        // Against the closed form C(m+n-2, m-1), computed without factorials.
        int pathBad = 0;
        for (int m = 1; m <= 11; m++) {
            for (int n = 1; n <= 11; n++) {
                long binomial = 1;
                for (int k = 1; k <= m - 1; k++) binomial = binomial * (n - 1 + k) / k;
                if (s62.uniquePaths(m, n) != binomial) pathBad++;
            }
        }
        check("matches C(m+n-2, m-1) for every grid up to 11x11", pathBad, 0);
        check("reusable: 3x7 twice", s62.uniquePaths(3, 7) + s62.uniquePaths(3, 7), 56);

        System.out.println("LeetCode 63 - Unique Paths II");
        S63 s63 = new S63();
        check("blocked centre",
              s63.uniquePathsWithObstacles(new int[][]{{0,0,0},{0,1,0},{0,0,0}}), 2);
        check("[[0,1],[0,0]]", s63.uniquePathsWithObstacles(new int[][]{{0,1},{0,0}}), 1);
        check("[[1]] (start blocked)", s63.uniquePathsWithObstacles(new int[][]{{1}}), 0);
        check("[[0]] (single free cell)", s63.uniquePathsWithObstacles(new int[][]{{0}}), 1);
        check("a wall across", s63.uniquePathsWithObstacles(new int[][]{{0,0},{1,1},{0,0}}), 0);
        check("finish blocked", s63.uniquePathsWithObstacles(new int[][]{{0,0},{0,1}}), 0);
        check("obstacle in the top row cuts off the rest",
              s63.uniquePathsWithObstacles(new int[][]{{0,1,0},{0,0,0}}), 1);
        check("single-column grid with an obstacle",
              s63.uniquePathsWithObstacles(new int[][]{{0},{1},{0}}), 0);
        int obsBad = 0, freeBad = 0;
        for (int m = 1; m <= 3; m++) {
            for (int n = 1; n <= 3; n++) {
                int[][] empty = new int[m][n];
                if (s63.uniquePathsWithObstacles(empty) != s62.uniquePaths(m, n)) freeBad++;
                for (int mask = 0; mask < (1 << (m * n)); mask++) {
                    int[][] g = new int[m][n];
                    for (int r = 0; r < m; r++)
                        for (int c = 0; c < n; c++) g[r][c] = (mask >> (r * n + c)) & 1;
                    int[][] copy = new int[m][];
                    for (int r = 0; r < m; r++) copy[r] = g[r].clone();
                    if (s63.uniquePathsWithObstacles(copy) != enumeratePaths(g)) obsBad++;
                }
            }
        }
        check("obstacle-free grids agree with problem 62", freeBad, 0);
        check("matches path enumeration on every obstacle layout up to 3x3", obsBad, 0);

        System.out.println("LeetCode 64 - Minimum Path Sum");
        S64 s64 = new S64();
        check("[[1,3,1],[1,5,1],[4,2,1]]",
              s64.minPathSum(new int[][]{{1,3,1},{1,5,1},{4,2,1}}), 7);
        check("[[1,2,3],[4,5,6]]", s64.minPathSum(new int[][]{{1,2,3},{4,5,6}}), 12);
        check("[[5]] (start counts)", s64.minPathSum(new int[][]{{5}}), 5);
        check("[[0]]", s64.minPathSum(new int[][]{{0}}), 0);
        check("single row", s64.minPathSum(new int[][]{{1,2,3,4}}), 10);
        check("single column", s64.minPathSum(new int[][]{{1},{2},{3}}), 6);
        check("greedy counterexample from the post",
              s64.minPathSum(new int[][]{{1,2,100},{1,100,100},{1,1,1}}), 5);
        int sumBad = 0;
        int[] cellValues = {0, 1, 5};
        for (int m = 1; m <= 3; m++) {
            for (int n = 1; n <= 3; n++) {
                int combos = (int) Math.pow(cellValues.length, m * n);
                for (int mask = 0; mask < combos; mask++) {
                    int[][] g = new int[m][n];
                    int mm = mask;
                    for (int r = 0; r < m; r++)
                        for (int c = 0; c < n; c++) {
                            g[r][c] = cellValues[mm % cellValues.length];
                            mm /= cellValues.length;
                        }
                    int[][] copy = new int[m][];
                    for (int r = 0; r < m; r++) copy[r] = g[r].clone();
                    if (s64.minPathSum(copy) != enumerateBest(g, 0, 0)) sumBad++;
                }
            }
        }
        check("matches brute-force enumeration on every grid up to 3x3 over {0,1,5}", sumBad, 0);

        System.out.println("LeetCode 65 - Valid Number");
        S65 s65 = new S65();
        String[] validNums = {"2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3",
                              "3e+7", "+6e-1", "53.5e93", "-123.456e789", "0", ".1", "1.", "46e6"};
        String[] invalidNums = {"abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53",
                                ".", "+", "", "4e+", "e", ".e1", "1e2e3", "1..2", "+-",
                                " 1", "1 ", "1e.5", ".-4", "6+1", "1e2.5"};
        int numBad = 0;
        for (String t : validNums) if (!s65.isNumber(t)) { numBad++; check("valid: " + t, false, true); }
        for (String t : invalidNums) if (s65.isNumber(t)) { numBad++; check("invalid: " + t, true, false); }
        check("all " + (validNums.length + invalidNums.length) + " spec cases classified", numBad, 0);
        // Against the grammar the post writes out, over generated strings.
        java.util.regex.Pattern grammar =
            java.util.regex.Pattern.compile("^[+-]?(([0-9]+[.]?[0-9]*)|([.][0-9]+))([eE][+-]?[0-9]+)?$");
        char[] numAlphabet = {'0', '1', '.', 'e', 'E', '+', '-'};
        int grammarBad = 0;
        for (int len = 0; len <= 4; len++) {
            int combos = (int) Math.pow(numAlphabet.length, len);
            for (int mask = 0; mask < combos; mask++) {
                StringBuilder sb = new StringBuilder();
                int mm = mask;
                for (int i = 0; i < len; i++) { sb.append(numAlphabet[mm % numAlphabet.length]); mm /= numAlphabet.length; }
                String t = sb.toString();
                if (s65.isNumber(t) != grammar.matcher(t).matches()) grammarBad++;
            }
        }
        check("agrees with the grammar on every string up to length 4", grammarBad, 0);

        System.out.println("LeetCode 67 - Add Binary");
        S67 s67 = new S67();
        S67Bits s67b = new S67Bits();
        check("11 + 1", s67.addBinary("11", "1"), "100");
        check("1010 + 1011", s67.addBinary("1010", "1011"), "10101");
        check("0 + 0", s67.addBinary("0", "0"), "0");
        check("1 + 111 (carry all the way out)", s67.addBinary("1", "111"), "1000");
        int addBad = 0, leadingZero = 0;
        for (int x = 0; x < 64; x++)
            for (int y = 0; y < 64; y++) {
                String got = s67.addBinary(Integer.toBinaryString(x), Integer.toBinaryString(y));
                if (!got.equals(Integer.toBinaryString(x + y))) addBad++;
                if (got.length() > 1 && got.charAt(0) == '0') leadingZero++;
            }
        check("agrees with integer addition for all x,y in 0..63", addBad, 0);
        check("never emits a leading zero on in-spec input", leadingZero, 0);
        // Far beyond 64 bits -- the constraint that rules out parsing.
        String bigOnes = "1".repeat(200);
        check("200 ones + 1", s67.addBinary(bigOnes, "1"), "1" + "0".repeat(200));
        check("200 ones + 200 ones", s67.addBinary(bigOnes, bigOnes),
              new java.math.BigInteger(bigOnes, 2).add(new java.math.BigInteger(bigOnes, 2)).toString(2));
        // The XOR/AND adder shown as the follow-up, at machine width.
        int bitAddBad = 0;
        for (int x = -500; x <= 500; x++)
            for (int y = -500; y <= 500; y += 7)
                if (s67b.add(x, y) != x + y) bitAddBad++;
        check("[XOR/AND adder] agrees with + over a range including negatives", bitAddBad, 0);

        System.out.println("LeetCode 68 - Text Justification");
        S68 s68 = new S68();
        check("the canonical example",
              s68.fullJustify(new String[]{"This","is","an","example","of","text","justification."}, 16),
              List.of("This    is    an", "example  of text", "justification.  "));
        check("single word line is NOT stretched",
              s68.fullJustify(new String[]{"What","must","be","acknowledgment","shall","be"}, 16),
              List.of("What   must   be", "acknowledgment  ", "shall be        "));
        check("one word total", s68.fullJustify(new String[]{"a"}, 5), List.of("a    "));
        check("word exactly maxWidth", s68.fullJustify(new String[]{"abcde"}, 5), List.of("abcde"));
        check("a single line is the LAST line, so left-justified",
              s68.fullJustify(new String[]{"a", "b"}, 5), List.of("a b  "));
        check("two words, spaces divide evenly",
              s68.fullJustify(new String[]{"a", "b", "cccc"}, 5), List.of("a   b", "cccc "));
        check("extra spaces go to the LEFT gaps",
              s68.fullJustify(new String[]{"aa", "b", "cc", "ddddd"}, 8),
              List.of("aa  b cc", "ddddd   "));
        // Structural invariants over generated inputs.
        String[] wordPool = {"a", "bb", "ccc"};
        int justBad = 0;
        for (int width = 4; width <= 11; width++) {
            for (int n = 1; n <= 6; n++) {
                int combos = (int) Math.pow(wordPool.length, n);
                for (int mask = 0; mask < combos; mask++) {
                    String[] ws = new String[n];
                    int mm = mask;
                    for (int i = 0; i < n; i++) { ws[i] = wordPool[mm % wordPool.length]; mm /= wordPool.length; }
                    List<String> out = s68.fullJustify(ws.clone(), width);
                    StringBuilder seen = new StringBuilder();
                    for (int li = 0; li < out.size(); li++) {
                        String line = out.get(li);
                        if (line.length() != width) justBad++;
                        if (line.startsWith(" ")) justBad++;
                        String[] onLine = line.trim().split(" +");
                        for (String w : onLine) seen.append(w).append(',');
                        // Only the last line, or a one-word line, may end in a space.
                        if (li < out.size() - 1 && line.endsWith(" ") && onLine.length > 1) justBad++;
                    }
                    StringBuilder expect = new StringBuilder();
                    for (String w : ws) expect.append(w).append(',');
                    if (!seen.toString().equals(expect.toString())) justBad++;
                }
            }
        }
        check("every line is exactly maxWidth, justified, words in order", justBad, 0);

        System.out.println("LeetCode 69 - Sqrt(x)");
        S69 s69 = new S69();
        check("x=4", s69.mySqrt(4), 2);
        check("x=8 (floor of 2.828)", s69.mySqrt(8), 2);
        check("x=0", s69.mySqrt(0), 0);
        check("x=1", s69.mySqrt(1), 1);
        check("x=2", s69.mySqrt(2), 1);
        check("x=2147483647 (THE overflow case)", s69.mySqrt(2147483647), 46340);
        check("x=2147395600 (46340 squared exactly)", s69.mySqrt(2147395600), 46340);
        int sqrtBad = 0;
        for (int x = 0; x < 5000; x++) {
            int r = s69.mySqrt(x);
            if ((long) r * r > x || (long) (r + 1) * (r + 1) <= x) sqrtBad++;
        }
        check("r*r <= x < (r+1)*(r+1) for every x in 0..4999", sqrtBad, 0);
        int edgeBad = 0;
        for (int k = 1; k < 1000; k++) {
            int sq = k * k;
            if (s69.mySqrt(sq) != k || s69.mySqrt(sq - 1) != k - 1 || s69.mySqrt(sq + 1) != k) edgeBad++;
        }
        check("k*k, k*k-1 and k*k+1 for every k in 1..999", edgeBad, 0);
        // The largest values, where mid*mid would overflow.
        int bigBad = 0;
        for (int x = Integer.MAX_VALUE; x > Integer.MAX_VALUE - 200; x--) {
            int r = s69.mySqrt(x);
            if ((long) r * r > x || (long) (r + 1) * (r + 1) <= x) bigBad++;
        }
        check("correct for the 200 largest int values", bigBad, 0);

        System.out.println("LeetCode 70 - Climbing Stairs");
        S70 s70 = new S70();
        check("n=1", s70.climbStairs(1), 1);
        check("n=2", s70.climbStairs(2), 2);
        check("n=3", s70.climbStairs(3), 3);
        check("n=4", s70.climbStairs(4), 5);
        check("n=5", s70.climbStairs(5), 8);
        check("n=45 (the constraint bound)", s70.climbStairs(45), 1836311903);
        int stairBad = 0;
        int fa = 1, fb = 1;
        for (int n = 0; n <= 40; n++) {
            if (s70.climbStairs(n) != fa) stairBad++;
            int next = fa + fb; fa = fb; fb = next;
        }
        check("matches an independent Fibonacci model for n in 0..40", stairBad, 0);

        System.out.println("LeetCode 71 - Simplify Path");
        S71 s71 = new S71();
        check("/home/", s71.simplifyPath("/home/"), "/home");
        check("/home//foo/", s71.simplifyPath("/home//foo/"), "/home/foo");
        check("/../ (root parent is root)", s71.simplifyPath("/../"), "/");
        check("/a/./b/../../c/", s71.simplifyPath("/a/./b/../../c/"), "/c");
        check("/... (three dots is a NAME)", s71.simplifyPath("/..."), "/...");
        check("/ (root)", s71.simplifyPath("/"), "/");
        check("/a//b////c/d//././/..", s71.simplifyPath("/a//b////c/d//././/.."), "/a/b/c");
        check("/../../../a", s71.simplifyPath("/../../../a"), "/a");
        check("/a/..", s71.simplifyPath("/a/.."), "/");
        check("/..hidden", s71.simplifyPath("/..hidden"), "/..hidden");
        check("/a..b", s71.simplifyPath("/a..b"), "/a..b");
        String[] pathParts = {"a", ".", "..", "", "..."};
        int simplifyBad = 0, shapeBad = 0;
        for (int n = 1; n <= 5; n++) {
            int combos = (int) Math.pow(pathParts.length, n);
            for (int mask = 0; mask < combos; mask++) {
                StringBuilder sb = new StringBuilder();
                int mm = mask;
                for (int i = 0; i < n; i++) { sb.append('/').append(pathParts[mm % pathParts.length]); mm /= pathParts.length; }
                String path = sb.toString();
                String got = s71.simplifyPath(path);
                if (!got.equals(canonical(path))) simplifyBad++;
                if (!got.startsWith("/")) shapeBad++;
                else if (!got.equals("/") && got.endsWith("/")) shapeBad++;
                else if (!got.equals("/")) {
                    for (String part : got.substring(1).split("/", -1))
                        if (part.isEmpty() || part.equals(".") || part.equals("..")) shapeBad++;
                }
            }
        }
        check("matches an independent model on every path up to 5 components", simplifyBad, 0);
        check("output is absolute, has no trailing slash, and resolves every . and ..", shapeBad, 0);

        System.out.println("LeetCode 72 - Edit Distance");
        S72 s72 = new S72();
        S72Row s72r = new S72Row();
        check("horse -> ros", s72.minDistance("horse", "ros"), 3);
        check("intention -> execution", s72.minDistance("intention", "execution"), 5);
        check("empty -> abc (three inserts)", s72.minDistance("", "abc"), 3);
        check("abc -> empty (three deletes)", s72.minDistance("abc", ""), 3);
        check("empty -> empty", s72.minDistance("", ""), 0);
        check("abc -> abc", s72.minDistance("abc", "abc"), 0);
        check("a -> b (one replace)", s72.minDistance("a", "b"), 1);
        check("sunday -> saturday", s72.minDistance("sunday", "saturday"), 3);
        int editBad = 0, editAsym = 0, rowBad = 0;
        for (int m = 0; m <= 4; m++) {
            for (int n = 0; n <= 4; n++) {
                for (int am = 0; am < (1 << m); am++) {
                    for (int bm = 0; bm < (1 << n); bm++) {
                        StringBuilder sa = new StringBuilder(), sb2 = new StringBuilder();
                        for (int i = 0; i < m; i++) sa.append((am >> i & 1) == 1 ? 'a' : 'b');
                        for (int i = 0; i < n; i++) sb2.append((bm >> i & 1) == 1 ? 'a' : 'b');
                        String wordA = sa.toString(), wordB = sb2.toString();
                        int dist = s72.minDistance(wordA, wordB);
                        if (dist != lev(wordA, wordB)) editBad++;
                        if (dist != s72.minDistance(wordB, wordA)) editAsym++;
                        if (s72r.minDistance(wordA, wordB) != dist) rowBad++;
                    }
                }
            }
        }
        check("matches Levenshtein on every pair of a/b strings up to length 4", editBad, 0);
        check("distance is symmetric", editAsym, 0);
        check("[one-row version] agrees with the table on the same pairs", rowBad, 0);

        System.out.println("LeetCode 76 - Minimum Window Substring");
        S76 s76 = new S76();
        check("ADOBECODEBANC / ABC", s76.minWindow("ADOBECODEBANC", "ABC"), "BANC");
        check("a / a", s76.minWindow("a", "a"), "a");
        check("a / aa (duplicates must be counted)", s76.minWindow("a", "aa"), "");
        check("ab / b", s76.minWindow("ab", "b"), "b");
        check("ab / A (case sensitive)", s76.minWindow("ab", "A"), "");
        check("empty s", s76.minWindow("", "a"), "");
        check("empty t", s76.minWindow("abc", ""), "");
        check("bba / ab", s76.minWindow("bba", "ab"), "ba");
        check("cabwefgewcwaefgcf / cae", s76.minWindow("cabwefgewcwaefgcf", "cae"), "cwae");
        int winBad = 0;
        for (int n = 0; n <= 6; n++) {
            int sCombos = (int) Math.pow(3, n);
            for (int sm = 0; sm < sCombos; sm++) {
                StringBuilder sb = new StringBuilder();
                int mm = sm;
                for (int i = 0; i < n; i++) { sb.append((char) ('a' + mm % 3)); mm /= 3; }
                String sv = sb.toString();
                for (int m = 1; m <= 2; m++) {
                    for (int tm = 0; tm < (1 << m); tm++) {
                        StringBuilder tb = new StringBuilder();
                        for (int i = 0; i < m; i++) tb.append((tm >> i & 1) == 1 ? 'a' : 'b');
                        String tv = tb.toString();
                        String win = s76.minWindow(sv, tv), bruteWin = bruteWindow(sv, tv);
                        if (win.length() != bruteWin.length()) winBad++;
                        else if (!win.isEmpty() && !covers(win, tv)) winBad++;
                    }
                }
            }
        }
        check("matches brute force on every s up to length 6 over abc, t up to length 2", winBad, 0);

        System.out.println("LeetCode 78 - Subsets");
        S78 s78 = new S78();
        S78Bits s78b = new S78Bits();
        check("[1,2,3]", norm(s78.subsets(new int[]{1,2,3})),
              norm(List.of(List.of(), List.of(1), List.of(2), List.of(3),
                           List.of(1,2), List.of(1,3), List.of(2,3), List.of(1,2,3))));
        check("[0]", s78.subsets(new int[]{0}).size(), 2);
        check("[] returns [[]], not []", s78.subsets(new int[]{}), List.of(List.of()));
        check("the empty subset is present", s78.subsets(new int[]{1,2,3}).contains(List.of()), true);
        int subBad = 0, bitsBad = 0;
        for (int n = 0; n <= 10; n++) {
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = i;
            List<List<Integer>> got = s78.subsets(nums.clone());
            if (got.size() != (1 << n)) subBad++;
            if (new HashSet<>(got).size() != (1 << n)) subBad++;
            for (List<Integer> sub : got)
                if (new HashSet<>(sub).size() != sub.size()) subBad++;
            if (!norm(s78b.subsetsBits(nums.clone())).equals(norm(got))) bitsBad++;
        }
        check("2^n distinct subsets of the input for every n in 0..10", subBad, 0);
        check("[bitmask] agrees with the backtracking version", bitsBad, 0);
        // Without the defensive copy, all 2^n entries would alias one list.
        List<List<Integer>> subs = new ArrayList<>(s78.subsets(new int[]{1,2,3}));
        subs.get(0).add(999);
        int carrying = 0;
        for (List<Integer> sub : subs) if (sub.contains(999)) carrying++;
        check("mutating one returned subset does not touch the others", carrying, 1);

        System.out.println("LeetCode 81 - Search in Rotated Sorted Array II");
        S81 s81 = new S81();
        check("[2,5,6,0,0,1,2] t=0", s81.search(new int[]{2,5,6,0,0,1,2}, 0), true);
        check("[2,5,6,0,0,1,2] t=3", s81.search(new int[]{2,5,6,0,0,1,2}, 3), false);
        check("[1,0,1,1,1] t=0 (the ambiguous case)", s81.search(new int[]{1,0,1,1,1}, 0), true);
        check("[1,1,1,0,1] t=0 (pivot on the other side)", s81.search(new int[]{1,1,1,0,1}, 0), true);
        check("[1,1,1,1,1] t=2", s81.search(new int[]{1,1,1,1,1}, 2), false);
        check("[1] t=1", s81.search(new int[]{1}, 1), true);
        check("[1] t=0", s81.search(new int[]{1}, 0), false);
        check("[3,1] t=1 (rotated pair)", s81.search(new int[]{3,1}, 1), true);
        int rotDupBad = 0;
        for (int n = 1; n <= 7; n++) {
            int combos = (int) Math.pow(3, n);
            for (int mask = 0; mask < combos; mask++) {
                int[] base = new int[n];
                int mm = mask;
                for (int i = 0; i < n; i++) { base[i] = mm % 3; mm /= 3; }
                Arrays.sort(base);
                for (int k = 0; k < n; k++) {
                    int[] rotated = new int[n];
                    for (int i = 0; i < n; i++) rotated[i] = base[(k + i) % n];
                    for (int target = -1; target <= 3; target++) {
                        boolean present = false;
                        for (int v : rotated) if (v == target) present = true;
                        if (s81.search(rotated.clone(), target) != present) rotDupBad++;
                    }
                }
            }
        }
        check("every rotation of every sorted array up to length 7 over {0,1,2}", rotDupBad, 0);
        // The worst case: a single 0 hiding among 1s, every rotation.
        int worstBad = 0;
        for (int n = 1; n <= 12; n++) {
            for (int pos = 0; pos < n; pos++) {
                int[] base = new int[n];
                Arrays.fill(base, 1);
                base[0] = 0;                       // sorted form
                for (int k = 0; k < n; k++) {
                    int[] rotated = new int[n];
                    for (int i = 0; i < n; i++) rotated[i] = base[(k + i) % n];
                    if (!s81.search(rotated.clone(), 0)) worstBad++;
                    if (s81.search(rotated.clone(), 2)) worstBad++;
                }
            }
        }
        check("single 0 among 1s, every rotation, terminates and is correct", worstBad, 0);

        System.out.println("LeetCode 83 - Remove Duplicates from Sorted List");
        S83 s83 = new S83();
        check("1->1->2", toArr(s83.deleteDuplicates(toList(1,1,2))), new int[]{1,2});
        check("1->1->2->3->3", toArr(s83.deleteDuplicates(toList(1,1,2,3,3))), new int[]{1,2,3});
        check("1->1->1 (THREE in a row)", toArr(s83.deleteDuplicates(toList(1,1,1))), new int[]{1});
        check("1->1->1->1 (four in a row)", toArr(s83.deleteDuplicates(toList(1,1,1,1))), new int[]{1});
        check("empty list", toArr(s83.deleteDuplicates(null)), new int[]{});
        check("single node", toArr(s83.deleteDuplicates(toList(1))), new int[]{1});
        check("no duplicates at all", toArr(s83.deleteDuplicates(toList(1,2,3))), new int[]{1,2,3});
        check("duplicates at the tail", toArr(s83.deleteDuplicates(toList(1,2,3,3,3))), new int[]{1,2,3});
        int listBad = 0;
        int[] listPool = {1, 1, 2, 3};
        for (int n = 0; n <= 8; n++) {
            int combos = (int) Math.pow(listPool.length, n);
            for (int mask = 0; mask < combos; mask++) {
                int[] xs = new int[n];
                int mm = mask;
                for (int i = 0; i < n; i++) { xs[i] = listPool[mm % listPool.length]; mm /= listPool.length; }
                Arrays.sort(xs);
                List<Integer> uniq = new ArrayList<>();
                for (int i = 0; i < n; i++) if (i == 0 || xs[i] != xs[i - 1]) uniq.add(xs[i]);
                int[] wantUniq = uniq.stream().mapToInt(Integer::intValue).toArray();
                if (!Arrays.equals(toArr(s83.deleteDuplicates(toList(xs))), wantUniq)) listBad++;
            }
        }
        check("matches sorted-unique on every sorted list up to length 8", listBad, 0);
        // The head is never removed, so the same object must come back.
        ListNode headNode = toList(1, 1, 2);
        check("returns the original head object", s83.deleteDuplicates(headNode) == headNode, true);

        System.out.println("LeetCode 88 - Merge Sorted Array");
        S88 s88 = new S88();
        int[] mergeTarget = {1,2,3,0,0,0};
        s88.merge(mergeTarget, 3, new int[]{2,5,6}, 3);
        check("[1,2,3,0,0,0] + [2,5,6]", mergeTarget, new int[]{1,2,2,3,5,6});
        int[] onlyOne = {1};
        s88.merge(onlyOne, 1, new int[]{}, 0);
        check("[1] m=1, [] n=0", onlyOne, new int[]{1});
        int[] emptyFirst = {0};
        s88.merge(emptyFirst, 0, new int[]{1}, 1);
        check("[0] m=0, [1] n=1 (nums1 contributes nothing)", emptyFirst, new int[]{1});
        int[] allSecond = {4,5,6,0,0,0};
        s88.merge(allSecond, 3, new int[]{1,2,3}, 3);
        check("[4,5,6,0,0,0] + [1,2,3] (all of nums2 first)", allSecond, new int[]{1,2,3,4,5,6});
        int[] negatives = {-3,-1,0,0};
        s88.merge(negatives, 3, new int[]{-2}, 1);
        check("negatives", negatives, new int[]{-3,-2,-1,0});
        int mergeBad = 0;
        for (int m = 0; m <= 4; m++) {
            for (int n = 0; n <= 4; n++) {
                int aCombos = (int) Math.pow(4, m), bCombos = (int) Math.pow(4, n);
                for (int am = 0; am < aCombos; am++) {
                    int[] left = new int[m];
                    int mm = am;
                    for (int i = 0; i < m; i++) { left[i] = mm % 4; mm /= 4; }
                    Arrays.sort(left);
                    for (int bm = 0; bm < bCombos; bm++) {
                        int[] right = new int[n];
                        int nn = bm;
                        for (int i = 0; i < n; i++) { right[i] = nn % 4; nn /= 4; }
                        Arrays.sort(right);

                        int[] slot = new int[m + n];
                        System.arraycopy(left, 0, slot, 0, m);
                        s88.merge(slot, m, right.clone(), n);

                        int[] wantMerged = new int[m + n];
                        System.arraycopy(left, 0, wantMerged, 0, m);
                        System.arraycopy(right, 0, wantMerged, m, n);
                        Arrays.sort(wantMerged);
                        if (!Arrays.equals(slot, wantMerged)) mergeBad++;
                    }
                }
            }
        }
        check("matches sorted(a + b) for every pair of sorted inputs up to length 4", mergeBad, 0);

        System.out.println("LeetCode 91 - Decode Ways");
        S91 s91 = new S91();
        check("12", s91.numDecodings("12"), 2);
        check("226", s91.numDecodings("226"), 3);
        check("06 (leading zero in a pair)", s91.numDecodings("06"), 0);
        check("0", s91.numDecodings("0"), 0);
        check("10", s91.numDecodings("10"), 1);
        check("100 (the 0 has no partner)", s91.numDecodings("100"), 0);
        check("2101", s91.numDecodings("2101"), 1);
        check("27 (27 is not a letter)", s91.numDecodings("27"), 1);
        check("1111", s91.numDecodings("1111"), 5);
        check("11106", s91.numDecodings("11106"), 2);
        check("230", s91.numDecodings("230"), 0);
        check("1201234", s91.numDecodings("1201234"), 3);
        int decodeBad = 0;
        for (int n = 1; n <= 8; n++) {
            int combos = (int) Math.pow(4, n);
            for (int mask = 0; mask < combos; mask++) {
                StringBuilder sb = new StringBuilder();
                int mm = mask;
                for (int i = 0; i < n; i++) { sb.append((char) ('0' + mm % 4)); mm /= 4; }
                String text = sb.toString();
                if (s91.numDecodings(text) != countDecodings(text)) decodeBad++;
            }
        }
        check("matches enumeration on every string of 0-3 digits up to length 8", decodeBad, 0);
        int fibBad = 0, fa91 = 1, fb91 = 1;
        for (int n = 1; n <= 17; n++) {
            int next = fa91 + fb91; fa91 = fb91; fb91 = next;
            if (s91.numDecodings("1".repeat(n)) != fa91) fibBad++;
        }
        check("all-ones strings follow Fibonacci", fibBad, 0);

        System.out.println("LeetCode 94 - Binary Tree Inorder Traversal");
        S94 s94 = new S94();
        S94Recursive s94r = new S94Recursive();
        check("[1,null,2,3]", s94.inorderTraversal(buildTree(1, null, 2, 3)), List.of(1, 3, 2));
        check("empty tree", s94.inorderTraversal(null), List.of());
        check("single node", s94.inorderTraversal(buildTree(1)), List.of(1));
        check("a BST comes out sorted",
              s94.inorderTraversal(buildTree(4, 2, 6, 1, 3, 5, 7)), List.of(1,2,3,4,5,6,7));
        // A degenerate left chain: where the recursive stack depth would bite.
        TreeNode leftChain = new TreeNode(1), leftChainTail = leftChain;
        List<Integer> chainWant = new ArrayList<>();
        for (int v = 2; v < 60; v++) { leftChainTail.left = new TreeNode(v); leftChainTail = leftChainTail.left; }
        for (int v = 59; v >= 1; v--) chainWant.add(v);
        check("left chain of 59 nodes", s94.inorderTraversal(leftChain), chainWant);
        int inorderBad = 0;
        for (int n = 1; n <= 8; n++) {
            for (int mask = 0; mask < (1 << (n - 1)); mask++) {
                Integer[] xs = new Integer[n];
                int next = 1;
                xs[0] = next++;
                for (int i = 1; i < n; i++) xs[i] = (mask >> (i - 1) & 1) == 1 ? next++ : null;
                TreeNode t = buildTree(xs);
                List<Integer> model = new ArrayList<>();
                inorderModel(t, model);
                if (!s94.inorderTraversal(t).equals(model)) inorderBad++;
                if (!s94r.inorderTraversal(t).equals(model)) inorderBad++;
            }
        }
        check("iterative and recursive both match a model on every small tree shape", inorderBad, 0);

        System.out.println("LeetCode 98 - Validate Binary Search Tree");
        S98 s98 = new S98();
        check("[2,1,3]", s98.isValidBST(buildTree(2, 1, 3)), true);
        check("[5,1,4,null,null,3,6]", s98.isValidBST(buildTree(5, 1, 4, null, null, 3, 6)), false);
        check("the naive-check counterexample [5,1,6,null,null,4,7]",
              s98.isValidBST(buildTree(5, 1, 6, null, null, 4, 7)), false);
        check("empty tree", s98.isValidBST(null), true);
        check("single node", s98.isValidBST(buildTree(1)), true);
        check("duplicates are invalid", s98.isValidBST(buildTree(2, 2)), false);
        // The sentinel trap: a lone Integer.MIN_VALUE / MAX_VALUE node is valid.
        check("Integer.MIN_VALUE as the only node", s98.isValidBST(buildTree(Integer.MIN_VALUE)), true);
        check("Integer.MAX_VALUE as the only node", s98.isValidBST(buildTree(Integer.MAX_VALUE)), true);
        check("[MIN_VALUE, null, MAX_VALUE]",
              s98.isValidBST(buildTree(Integer.MIN_VALUE, null, Integer.MAX_VALUE)), true);
        int bstBad = 0;
        for (int n = 1; n <= 7; n++) {
            int combos = (int) Math.pow(3, n);
            for (int mask = 0; mask < combos; mask++) {
                Integer[] xs = new Integer[n];
                int mm = mask;
                for (int i = 0; i < n; i++) { xs[i] = 1 + mm % 3; mm /= 3; }
                TreeNode t = buildTree(xs);
                List<Integer> seq = new ArrayList<>();
                inorderModel(t, seq);
                boolean strictlyIncreasing = true;
                for (int i = 0; i + 1 < seq.size(); i++)
                    if (seq.get(i) >= seq.get(i + 1)) strictlyIncreasing = false;
                if (s98.isValidBST(t) != strictlyIncreasing) bstBad++;
            }
        }
        check("agrees with strictly-increasing-inorder on every small tree", bstBad, 0);

        System.out.println("LeetCode 100 - Same Tree");
        S100 s100 = new S100();
        S100Iterative s100i = new S100Iterative();
        check("identical trees", s100.isSameTree(buildTree(1,2,3), buildTree(1,2,3)), true);
        check("same values, different shape",
              s100.isSameTree(buildTree(1,2), buildTree(1,null,2)), false);
        check("same shape, different values",
              s100.isSameTree(buildTree(1,2,1), buildTree(1,1,2)), false);
        check("both empty", s100.isSameTree(null, null), true);
        check("one empty", s100.isSameTree(null, buildTree(1)), false);
        check("one empty, the other way round", s100.isSameTree(buildTree(1), null), false);
        check("a node valued 0 is not treated as absent",
              s100.isSameTree(buildTree(0), buildTree(0)), true);
        // Exhaustive over pairs of small trees, with the iterative version agreeing.
        List<Integer[]> treeShapes = new ArrayList<>();
        for (int n = 1; n <= 4; n++) {
            int combos = (int) Math.pow(3, n - 1);
            for (int mask = 0; mask < combos; mask++) {
                Integer[] xs = new Integer[n];
                xs[0] = 1;
                int mm = mask;
                for (int i = 1; i < n; i++) {
                    int pick = mm % 3; mm /= 3;
                    xs[i] = pick == 2 ? null : 1 + pick;
                }
                treeShapes.add(xs);
            }
        }
        int sameBad = 0, sameIterBad = 0;
        for (Integer[] xa : treeShapes) {
            for (Integer[] xb : treeShapes) {
                boolean model = sameModel(buildTree(xa), buildTree(xb));
                if (s100.isSameTree(buildTree(xa), buildTree(xb)) != model) sameBad++;
                if (s100i.isSameTreeIterative(buildTree(xa), buildTree(xb)) != model) sameIterBad++;
            }
        }
        check("matches an independent comparison on every pair of small trees", sameBad, 0);
        check("[iterative] agrees on the same pairs", sameIterBad, 0);

        System.out.println("LeetCode 101 - Symmetric Tree");
        S101 s101 = new S101();
        S101Iterative s101i = new S101Iterative();
        check("[1,2,2,3,4,4,3]", s101.isSymmetric(buildTree(1,2,2,3,4,4,3)), true);
        check("[1,2,2,null,3,null,3]", s101.isSymmetric(buildTree(1,2,2,null,3,null,3)), false);
        check("empty tree", s101.isSymmetric(null), true);
        check("single node", s101.isSymmetric(buildTree(1)), true);
        check("[1,2,3] (values differ)", s101.isSymmetric(buildTree(1,2,3)), false);
        // The tree that defeats the inorder-palindrome shortcut.
        TreeNode palindromic = new TreeNode(1);
        palindromic.left = new TreeNode(2); palindromic.left.left = new TreeNode(2);
        palindromic.right = new TreeNode(2); palindromic.right.left = new TreeNode(2);
        List<Integer> palSeq = new ArrayList<>();
        inorderModel(palindromic, palSeq);
        check("inorder is a palindrome but the tree is NOT symmetric",
              palSeq + " " + s101.isSymmetric(palindromic), "[2, 2, 1, 2, 2] false");
        int symBad = 0, symIterBad = 0;
        for (int n = 1; n <= 7; n++) {
            int combos = (int) Math.pow(3, n - 1);
            for (int mask = 0; mask < combos; mask++) {
                Integer[] xs = new Integer[n];
                xs[0] = 1;
                int mm = mask;
                for (int i = 1; i < n; i++) { int pick = mm % 3; mm /= 3; xs[i] = pick == 2 ? null : 1 + pick; }
                TreeNode t = buildTree(xs);
                boolean model = t == null || mirrorModel(t.left, t.right);
                if (s101.isSymmetric(buildTree(xs)) != model) symBad++;
                if (s101i.isSymmetricIterative(buildTree(xs)) != model) symIterBad++;
            }
        }
        check("matches a mirror model on every small tree", symBad, 0);
        check("[iterative] agrees on the same trees", symIterBad, 0);

        System.out.println("LeetCode 102 - Binary Tree Level Order Traversal");
        S102 s102 = new S102();
        check("[3,9,20,null,null,15,7]",
              s102.levelOrder(buildTree(3,9,20,null,null,15,7)),
              List.of(List.of(3), List.of(9,20), List.of(15,7)));
        check("empty tree returns [], not [[]]", s102.levelOrder(null), List.of());
        check("single node", s102.levelOrder(buildTree(1)), List.of(List.of(1)));
        check("left chain", s102.levelOrder(buildTree(1,2,null,3)),
              List.of(List.of(1), List.of(2), List.of(3)));
        int levelBad = 0;
        for (int n = 1; n <= 8; n++) {
            for (Integer[] xs : treeShapesOfSize(n)) {
                List<List<Integer>> model = new ArrayList<>();
                levelsModel(buildTree(xs), 0, model);
                if (!s102.levelOrder(buildTree(xs)).equals(model)) levelBad++;
            }
        }
        check("matches a depth-indexed model on every small tree shape", levelBad, 0);

        System.out.println("LeetCode 103 - Binary Tree Zigzag Level Order Traversal");
        S103 s103 = new S103();
        check("[3,9,20,null,null,15,7]",
              s103.zigzagLevelOrder(buildTree(3,9,20,null,null,15,7)),
              List.of(List.of(3), List.of(20,9), List.of(15,7)));
        check("empty tree", s103.zigzagLevelOrder(null), List.of());
        check("single node", s103.zigzagLevelOrder(buildTree(1)), List.of(List.of(1)));
        check("four levels, so the alternation repeats",
              s103.zigzagLevelOrder(buildTree(1,2,3,4,5,6,7,8)),
              List.of(List.of(1), List.of(3,2), List.of(4,5,6,7), List.of(8)));
        int zigBad = 0;
        for (int n = 1; n <= 8; n++) {
            for (Integer[] xs : treeShapesOfSize(n)) {
                List<List<Integer>> zigWant = new ArrayList<>();
                for (List<Integer> lvl : s102.levelOrder(buildTree(xs))) {
                    List<Integer> copy = new ArrayList<>(lvl);
                    if (zigWant.size() % 2 == 1) Collections.reverse(copy);
                    zigWant.add(copy);
                }
                if (!s103.zigzagLevelOrder(buildTree(xs)).equals(zigWant)) zigBad++;
            }
        }
        check("equals level order with every odd level reversed, on every small tree", zigBad, 0);

        System.out.println("LeetCode 104 - Maximum Depth of Binary Tree");
        S104 s104 = new S104();
        check("[3,9,20,null,null,15,7]", s104.maxDepth(buildTree(3,9,20,null,null,15,7)), 3);
        check("empty tree", s104.maxDepth(null), 0);
        check("single node (depth counts NODES)", s104.maxDepth(buildTree(1)), 1);
        check("[1,null,2]", s104.maxDepth(buildTree(1,null,2)), 2);
        int depthBad = 0;
        for (int n = 1; n <= 8; n++)
            for (Integer[] xs : treeShapesOfSize(n))
                if (s104.maxDepth(buildTree(xs)) != depthModel(buildTree(xs))) depthBad++;
        check("matches a recursive model on every small tree shape", depthBad, 0);

        System.out.println("LeetCode 105 - Construct Binary Tree from Preorder and Inorder");
        S105 s105 = new S105();
        check("the canonical example",
              shape(s105.buildTree(new int[]{3,9,20,15,7}, new int[]{9,3,15,20,7})),
              shape(buildTree(3,9,20,null,null,15,7)));
        check("single node", shape(s105.buildTree(new int[]{1}, new int[]{1})), shape(buildTree(1)));
        check("empty input", s105.buildTree(new int[]{}, new int[]{}), null);
        check("left chain", shape(s105.buildTree(new int[]{1,2,3}, new int[]{3,2,1})),
              shape(buildTree(1,2,null,3)));
        check("right chain", shape(s105.buildTree(new int[]{1,2,3}, new int[]{1,2,3})),
              shape(buildTree(1,null,2,null,3)));
        int buildBad = 0;
        for (int n = 1; n <= 8; n++) {
            for (Integer[] xs : treeShapesOfSize(n)) {
                TreeNode original = buildTree(xs);
                List<Integer> pre = new ArrayList<>(), ino = new ArrayList<>();
                preorderModel(original, pre);
                inorderModel(original, ino);
                int[] preArr = pre.stream().mapToInt(Integer::intValue).toArray();
                int[] inoArr = ino.stream().mapToInt(Integer::intValue).toArray();
                if (!shape(s105.buildTree(preArr, inoArr)).equals(shape(original))) buildBad++;
            }
        }
        check("round-trips every small tree through its own traversals", buildBad, 0);
        // Instance state must be reset -- a second call on the same object has to work.
        check("reusable: same object, two calls",
              shape(s105.buildTree(new int[]{3,9,20,15,7}, new int[]{9,3,15,20,7})),
              shape(s105.buildTree(new int[]{3,9,20,15,7}, new int[]{9,3,15,20,7})));

        System.out.println("LeetCode 110 - Balanced Binary Tree");
        S110 s110 = new S110();
        check("[3,9,20,null,null,15,7]", s110.isBalanced(buildTree(3,9,20,null,null,15,7)), true);
        check("[1,2,2,3,3,null,null,4,4]",
              s110.isBalanced(buildTree(1,2,2,3,3,null,null,4,4)), false);
        check("empty tree", s110.isBalanced(null), true);
        check("single node", s110.isBalanced(buildTree(1)), true);
        check("[1,2,null,3] (chain of 3)", s110.isBalanced(buildTree(1,2,null,3)), false);
        // Balanced at the root, unbalanced deeper -- what "at every node" means.
        TreeNode deepImbalance = new TreeNode(1);
        deepImbalance.left = new TreeNode(2); deepImbalance.right = new TreeNode(3);
        deepImbalance.left.left = new TreeNode(4);
        deepImbalance.left.left.left = new TreeNode(5);
        check("root looks fine, imbalance is deeper", s110.isBalanced(deepImbalance), false);
        int balBad = 0;
        for (int n = 1; n <= 9; n++)
            for (Integer[] xs : treeShapesOfSize(n))
                if (s110.isBalanced(buildTree(xs)) != balancedModel(buildTree(xs))) balBad++;
        check("matches the naive definition on every small tree shape", balBad, 0);

        System.out.println("LeetCode 111 - Minimum Depth of Binary Tree");
        S111 s111 = new S111();
        check("[3,9,20,null,null,15,7]", s111.minDepth(buildTree(3,9,20,null,null,15,7)), 2);
        check("[1,null,2] (THE case: 1 is not a leaf)", s111.minDepth(buildTree(1,null,2)), 2);
        check("right chain of 5", s111.minDepth(buildTree(2,null,3,null,4,null,5,null,6)), 5);
        check("empty tree", s111.minDepth(null), 0);
        check("single node", s111.minDepth(buildTree(1)), 1);
        check("[1,2,null,3] (left chain)", s111.minDepth(buildTree(1,2,null,3)), 3);
        int minDepthBad = 0, vsMaxBad = 0;
        S104 s104ref = new S104();
        for (int n = 1; n <= 9; n++) {
            for (Integer[] xs : treeShapesOfSize(n)) {
                if (s111.minDepth(buildTree(xs)) != minDepthModel(buildTree(xs))) minDepthBad++;
                if (s111.minDepth(buildTree(xs)) > s104ref.maxDepth(buildTree(xs))) vsMaxBad++;
            }
        }
        check("matches a leaf-aware model on every small tree shape", minDepthBad, 0);
        check("minDepth never exceeds maxDepth", vsMaxBad, 0);
        check("equal on a perfect tree",
              s111.minDepth(buildTree(1,2,3,4,5,6,7)), s104ref.maxDepth(buildTree(1,2,3,4,5,6,7)));

        System.out.println("LeetCode 112 - Path Sum");
        S112 s112 = new S112();
        S112Iterative s112i = new S112Iterative();
        TreeNode pathTree = buildTree(5,4,8,11,null,13,4,7,2,null,null,null,1);
        check("the canonical example, target 22", s112.hasPathSum(pathTree, 22), true);
        check("same tree, target 26", s112.hasPathSum(pathTree, 26), true);
        check("same tree, target 100", s112.hasPathSum(pathTree, 100), false);
        check("[1,2,3] target 5", s112.hasPathSum(buildTree(1,2,3), 5), false);
        check("[1,2,3] target 3", s112.hasPathSum(buildTree(1,2,3), 3), true);
        check("empty tree, target 0 (no path at all)", s112.hasPathSum(null, 0), false);
        check("[1,2] target 1 -- THE base-case bug", s112.hasPathSum(buildTree(1,2), 1), false);
        check("[1,2] target 3", s112.hasPathSum(buildTree(1,2), 3), true);
        check("[-2,null,-3] target -5 (negatives)", s112.hasPathSum(buildTree(-2,null,-3), -5), true);
        int pathBadCount = 0, pathIterBad = 0;
        for (int n = 1; n <= 7; n++) {
            for (Integer[] xs : treeShapesOfSize(n)) {
                Set<Integer> sums = new HashSet<>();
                leafSums(buildTree(xs), 0, sums);
                for (int target = -2; target <= 20; target++) {
                    boolean model = sums.contains(target);
                    if (s112.hasPathSum(buildTree(xs), target) != model) pathBadCount++;
                    if (s112i.hasPathSumIterative(buildTree(xs), target) != model) pathIterBad++;
                }
            }
        }
        check("matches root-to-leaf enumeration on every small tree", pathBadCount, 0);
        check("[iterative] agrees on the same trees", pathIterBad, 0);

        System.out.println("LeetCode 114 - Flatten Binary Tree to Linked List");
        S114 s114 = new S114();
        int flatBad = 0;
        for (int n = 1; n <= 9; n++) {
            for (Integer[] xs : treeShapesOfSize(n)) {
                TreeNode t = buildTree(xs);
                List<Integer> flatWant = new ArrayList<>();
                preorderModel(t, flatWant);

                TreeNode flat = buildTree(xs);
                s114.flatten(flat);

                List<Integer> got = new ArrayList<>();
                boolean leftNulled = true;
                for (TreeNode node = flat; node != null; node = node.right) {
                    if (node.left != null) leftNulled = false;
                    got.add(node.val);
                }
                if (!leftNulled || !got.equals(flatWant)) flatBad++;
            }
        }
        check("equals preorder with every left pointer nulled, on every small tree", flatBad, 0);
        TreeNode single = buildTree(0);
        s114.flatten(single);
        check("single node", single.val + "," + (single.left == null) + "," + (single.right == null),
              "0,true,true");
        s114.flatten(null);   // must not throw
        check("empty tree does not throw", true, true);

        System.out.println("LeetCode 118 - Pascal's Triangle");
        S118 s118 = new S118();
        check("numRows=5", s118.generate(5),
              List.of(List.of(1), List.of(1,1), List.of(1,2,1), List.of(1,3,3,1), List.of(1,4,6,4,1)));
        check("numRows=1", s118.generate(1), List.of(List.of(1)));
        check("numRows=0", s118.generate(0), List.of());
        int triBad = 0;
        for (int n = 0; n <= 30; n++) {
            List<List<Integer>> rows = s118.generate(n);
            if (rows.size() != n) { triBad++; continue; }
            for (int r = 0; r < n; r++) {
                List<Integer> row = rows.get(r);
                if (row.size() != r + 1) { triBad++; break; }
                for (int c = 0; c <= r; c++)
                    if (row.get(c) != binomial(r, c)) { triBad++; break; }
            }
        }
        check("every row matches the binomial coefficients, for numRows 0..30", triBad, 0);

        System.out.println("LeetCode 119 - Pascal's Triangle II");
        S119 s119 = new S119();
        check("rowIndex=3", s119.getRow(3), List.of(1,3,3,1));
        check("rowIndex=0", s119.getRow(0), List.of(1));
        check("rowIndex=1", s119.getRow(1), List.of(1,1));
        check("rowIndex=4", s119.getRow(4), List.of(1,4,6,4,1));
        int pascalRowBad = 0, pascalAgreeBad = 0;
        for (int k = 0; k <= 30; k++) {
            List<Integer> row = s119.getRow(k);
            if (row.size() != k + 1) { pascalRowBad++; continue; }
            for (int c = 0; c <= k; c++) if (row.get(c) != binomial(k, c)) { pascalRowBad++; break; }
            if (!row.equals(s118.generate(k + 1).get(k))) pascalAgreeBad++;
        }
        check("matches the binomial coefficients for rowIndex 0..30", pascalRowBad, 0);
        check("agrees with the last row of problem 118", pascalAgreeBad, 0);
        check("reusable: two calls give the same row",
              s119.getRow(5).equals(s119.getRow(5)) && s119.getRow(5).equals(List.of(1,5,10,10,5,1)), true);

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
