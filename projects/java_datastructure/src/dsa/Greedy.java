package dsa;

import java.util.Arrays;
import java.util.Comparator;

/**
 * Greedy algorithms: take the best-looking option at each step and never reconsider.
 *
 * <p>Fast and simple, and correct only when the problem has the <b>greedy choice property</b> -
 * a locally optimal choice is always part of a globally optimal answer. When it does not, greedy
 * gives a plausible wrong answer rather than an error, which is what makes it dangerous.
 *
 * <p>The two methods below are deliberately paired: interval scheduling, where greedy is provably
 * optimal, and coin change, where it is not.
 */
public final class Greedy {

    private Greedy() {}

    public record Interval(int start, int end) {}

    /**
     * The most non-overlapping intervals you can pick - the classic correct greedy.
     *
     * <p>Sort by END time and take everything that fits. Finishing earliest leaves the most room
     * for what follows, and that can be proved optimal. Sorting by START time, or by duration,
     * both look just as reasonable and are both wrong.
     */
    public static int maxNonOverlapping(Interval[] intervals) {
        if (intervals.length == 0) {
            return 0;
        }
        Interval[] sorted = intervals.clone();
        Arrays.sort(sorted, Comparator.comparingInt(Interval::end));

        int count = 0;
        int lastEnd = Integer.MIN_VALUE;
        for (Interval interval : sorted) {
            if (interval.start() >= lastEnd) {
                count++;
                lastEnd = interval.end();
            }
        }
        return count;
    }

    /**
     * Coin change, greedily - biggest coin first.
     *
     * <p>Correct for the US/euro coin systems, which are "canonical". Wrong in general: with
     * {1, 3, 4} and 6 this returns 3 coins where 2 suffice. Compare
     * {@link DynamicProgramming#coinChange}, which is always right.
     *
     * @return the number of coins used, or -1 if this method cannot make the amount at all
     */
    public static int coinChangeGreedy(int[] coins, int amount) {
        int[] descending = coins.clone();
        Arrays.sort(descending);
        int count = 0;
        int remaining = amount;
        for (int i = descending.length - 1; i >= 0; i--) {
            while (remaining >= descending[i]) {
                remaining -= descending[i];
                count++;
            }
        }
        return remaining == 0 ? count : -1;
    }

    /** Fractional knapsack - greedy IS optimal here, because items can be split. */
    public static double fractionalKnapsack(int[] weights, int[] values, int capacity) {
        Integer[] order = new Integer[weights.length];
        for (int i = 0; i < order.length; i++) {
            order[i] = i;
        }
        // Best value per unit of weight first.
        Arrays.sort(order, (a, b) -> Double.compare(
                (double) values[b] / weights[b], (double) values[a] / weights[a]));

        double total = 0;
        int remaining = capacity;
        for (int i : order) {
            if (remaining == 0) {
                break;
            }
            int take = Math.min(weights[i], remaining);
            total += (double) values[i] * take / weights[i];
            remaining -= take;
        }
        return total;
    }

    static void check() {
        Check.section("Greedy");

        Interval[] intervals = {
            new Interval(1, 3), new Interval(2, 5), new Interval(4, 7),
            new Interval(6, 9), new Interval(8, 10),
        };
        Check.eq(maxNonOverlapping(intervals), 3, "earliest-finish-first picks three");
        Check.eq(maxNonOverlapping(new Interval[0]), 0, "no intervals");
        Check.eq(maxNonOverlapping(new Interval[] {new Interval(1, 2)}), 1, "one interval");
        Check.eq(maxNonOverlapping(new Interval[] {
            new Interval(1, 10), new Interval(2, 3), new Interval(4, 5),
        }), 2, "the long one is correctly skipped");

        Check.eq(coinChangeGreedy(new int[] {1, 5, 10, 25}, 30), 2, "greedy is right on US coins");
        Check.eq(coinChangeGreedy(new int[] {1, 5, 10, 25}, 41), 4, "25+10+5+1");

        // The headline result: greedy and DP disagree, and DP is the correct one.
        Check.eq(coinChangeGreedy(new int[] {1, 3, 4}, 6), 3, "greedy takes 4+1+1");
        Check.eq(DynamicProgramming.coinChange(new int[] {1, 3, 4}, 6), 2, "DP finds 3+3");
        Check.isTrue(coinChangeGreedy(new int[] {1, 3, 4}, 6)
                > DynamicProgramming.coinChange(new int[] {1, 3, 4}, 6),
                "greedy is strictly worse here");

        Check.eq(String.format("%.1f", fractionalKnapsack(
                new int[] {10, 20, 30}, new int[] {60, 100, 120}, 50)), "240.0", "fractional knapsack");
    }
}
