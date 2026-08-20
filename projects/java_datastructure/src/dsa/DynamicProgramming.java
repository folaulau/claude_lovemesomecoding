package dsa;

import java.util.Arrays;

/**
 * Dynamic programming: solve each subproblem once, remember the answer.
 *
 * <p>It applies when a problem has <b>overlapping subproblems</b> (the same subproblem comes up
 * again and again) and <b>optimal substructure</b> (the best answer is built from best answers to
 * smaller versions). Both conditions matter - without overlap, memoising is pure overhead, which
 * is why merge sort is divide-and-conquer and not DP.
 *
 * <p>Two ways to write it. <b>Top-down</b> is the recursion plus a cache; <b>bottom-up</b> fills a
 * table in order and has no recursion at all. Same complexity, and bottom-up cannot overflow the
 * stack.
 */
public final class DynamicProgramming {

    private DynamicProgramming() {}

    /**
     * Fibonacci bottom-up: O(n) time and O(1) space.
     *
     * <p>Against {@link Recursion#fibonacciNaive}'s O(2^n), this is the whole argument for DP in
     * one function. Note it keeps two numbers rather than a whole table - the general table is
     * O(n) space, but this recurrence only ever looks back two steps.
     */
    public static long fibonacci(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("negative index");
        }
        if (n < 2) {
            return n;
        }
        long previous = 0;
        long current = 1;
        for (int i = 2; i <= n; i++) {
            long next = previous + current;
            previous = current;
            current = next;
        }
        return current;
    }

    /** The top-down form, for contrast: the naive recursion plus one array. */
    public static long fibonacciMemoised(int n) {
        return fibMemo(n, new long[n + 1], new boolean[n + 1]);
    }

    private static long fibMemo(int n, long[] cache, boolean[] known) {
        if (n < 2) {
            return n;
        }
        if (known[n]) {
            return cache[n];
        }
        known[n] = true;
        return cache[n] = fibMemo(n - 1, cache, known) + fibMemo(n - 2, cache, known);
    }

    /**
     * Fewest coins making up an amount, or -1 if it cannot be made.
     *
     * <p>The example that shows why greedy is not enough: with coins {1, 3, 4} and amount 6,
     * greedy takes 4 then 1 then 1 - three coins - while the answer is 3 + 3, two coins. DP tries
     * every option and keeps the best. See {@link Greedy#coinChangeGreedy}.
     */
    public static int coinChange(int[] coins, int amount) {
        int impossible = amount + 1;                  // larger than any real answer
        int[] best = new int[amount + 1];
        Arrays.fill(best, impossible);
        best[0] = 0;                                  // zero coins make zero

        for (int value = 1; value <= amount; value++) {
            for (int coin : coins) {
                if (coin <= value && best[value - coin] + 1 < best[value]) {
                    best[value] = best[value - coin] + 1;
                }
            }
        }
        return best[amount] >= impossible ? -1 : best[amount];
    }

    /** Longest common subsequence - the classic two-dimensional table. */
    public static int longestCommonSubsequence(String a, String b) {
        int[][] table = new int[a.length() + 1][b.length() + 1];
        for (int i = 1; i <= a.length(); i++) {
            for (int j = 1; j <= b.length(); j++) {
                table[i][j] = a.charAt(i - 1) == b.charAt(j - 1)
                        ? table[i - 1][j - 1] + 1
                        : Math.max(table[i - 1][j], table[i][j - 1]);
            }
        }
        return table[a.length()][b.length()];
    }

    /** 0/1 knapsack: each item taken once or not at all. */
    public static int knapsack(int[] weights, int[] values, int capacity) {
        int[] best = new int[capacity + 1];
        for (int i = 0; i < weights.length; i++) {
            // DOWNWARDS. Ascending would let one item be taken twice, which is the unbounded
            // knapsack - a different problem with a different answer.
            for (int c = capacity; c >= weights[i]; c--) {
                best[c] = Math.max(best[c], best[c - weights[i]] + values[i]);
            }
        }
        return best[capacity];
    }

    /** Kadane's algorithm: largest sum of any contiguous subarray. O(n), one pass. */
    public static int maxSubarraySum(int[] a) {
        if (a.length == 0) {
            throw new IllegalArgumentException("empty array has no subarray");
        }
        int best = a[0];
        int endingHere = a[0];
        for (int i = 1; i < a.length; i++) {
            // Either extend the run, or start again at this element.
            endingHere = Math.max(a[i], endingHere + a[i]);
            best = Math.max(best, endingHere);
        }
        return best;
    }

    static void check() {
        Check.section("DynamicProgramming");

        Check.eq(fibonacci(0), 0L, "fib(0)");
        Check.eq(fibonacci(10), 55L, "fib(10)");
        Check.eq(fibonacci(50), 12586269025L, "fib(50) - instant, unlike the naive version");
        Check.eq(fibonacci(90), 2880067194370816120L, "fib(90) still fits in a long");
        Check.eq(fibonacciMemoised(50), fibonacci(50), "top-down and bottom-up agree");
        Check.threw(() -> fibonacci(-1), IllegalArgumentException.class, "negative index");

        Check.eq(coinChange(new int[] {1, 3, 4}, 6), 2, "3+3 beats greedy's 4+1+1");
        Check.eq(coinChange(new int[] {1, 5, 10, 25}, 30), 2, "25+5");
        Check.eq(coinChange(new int[] {2}, 3), -1, "cannot be made");
        Check.eq(coinChange(new int[] {1, 2, 5}, 0), 0, "zero needs no coins");

        Check.eq(longestCommonSubsequence("ABCBDAB", "BDCABA"), 4, "LCS length");
        Check.eq(longestCommonSubsequence("abc", "abc"), 3, "identical strings");
        Check.eq(longestCommonSubsequence("abc", "xyz"), 0, "nothing in common");
        Check.eq(longestCommonSubsequence("", "abc"), 0, "empty string");

        Check.eq(knapsack(new int[] {1, 3, 4, 5}, new int[] {1, 4, 5, 7}, 7), 9, "knapsack 4+5 -> 9");
        Check.eq(knapsack(new int[] {5}, new int[] {10}, 3), 0, "nothing fits");

        Check.eq(maxSubarraySum(new int[] {-2, 1, -3, 4, -1, 2, 1, -5, 4}), 6, "Kadane");
        Check.eq(maxSubarraySum(new int[] {-5, -2, -9}), -2, "all negative returns the largest");
        Check.eq(maxSubarraySum(new int[] {3}), 3, "single element");
        Check.threw(() -> maxSubarraySum(new int[0]), IllegalArgumentException.class, "empty array");
    }
}
