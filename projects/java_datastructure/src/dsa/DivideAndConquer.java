package dsa;

/**
 * Divide and conquer: split the problem into independent subproblems, solve each, combine.
 *
 * <p>The word that separates it from dynamic programming is <b>independent</b>. Merge sort's two
 * halves share nothing, so there is nothing to memoise. Fibonacci's two branches overlap
 * enormously, which is why that one needs DP. Same recursive shape, different property, different
 * technique.
 *
 * <p>{@link Sorting#mergeSort}, {@link Sorting#quickSort} and {@link Searching#binarySearch} are
 * all divide and conquer; the ones here are the smaller illustrations.
 */
public final class DivideAndConquer {

    private DivideAndConquer() {}

    /** Maximum of an array, split down the middle. A loop is better - this shows the shape. */
    public static int max(int[] a, int low, int high) {
        if (low == high) {
            return a[low];                 // base case: one element
        }
        int mid = low + (high - low) / 2;
        return Math.max(max(a, low, mid), max(a, mid + 1, high));
    }

    /**
     * x^n by repeated squaring - O(log n) rather than the loop's O(n).
     *
     * <p>Here divide and conquer genuinely wins: x^20 is (x^10)^2, so each step halves the
     * exponent instead of decrementing it.
     */
    public static long power(long base, int exponent) {
        if (exponent < 0) {
            throw new IllegalArgumentException("negative exponent");
        }
        if (exponent == 0) {
            return 1;
        }
        long half = power(base, exponent / 2);
        // Computed ONCE and squared. Writing power(b, e/2) * power(b, e/2) is the same value
        // and O(n) again, because the compiler will not share those two calls for you.
        return exponent % 2 == 0 ? half * half : half * half * base;
    }

    /**
     * Counts inversions - pairs out of order - while merge sorting. O(n log n).
     *
     * <p>The best small example of the "combine" step doing real work: the merge already walks
     * both halves, so counting costs nothing extra, where the brute-force count is O(n^2).
     */
    public static long countInversions(int[] a) {
        int[] working = a.clone();
        return countInversions(working, new int[a.length], 0, a.length - 1);
    }

    private static long countInversions(int[] a, int[] buffer, int low, int high) {
        if (low >= high) {
            return 0;
        }
        int mid = low + (high - low) / 2;
        long count = countInversions(a, buffer, low, mid)
                + countInversions(a, buffer, mid + 1, high);

        System.arraycopy(a, low, buffer, low, high - low + 1);
        int left = low;
        int right = mid + 1;
        for (int i = low; i <= high; i++) {
            if (left > mid) {
                a[i] = buffer[right++];
            } else if (right > high) {
                a[i] = buffer[left++];
            } else if (buffer[right] < buffer[left]) {
                // Every remaining element in the left half is greater than this one,
                // so this single comparison accounts for all of them at once.
                count += mid - left + 1;
                a[i] = buffer[right++];
            } else {
                a[i] = buffer[left++];
            }
        }
        return count;
    }

    static void check() {
        Check.section("DivideAndConquer");

        int[] a = {3, 9, 1, 7, 4};
        Check.eq(max(a, 0, a.length - 1), 9, "max by splitting");
        Check.eq(max(new int[] {5}, 0, 0), 5, "single element");
        Check.eq(max(new int[] {-3, -1, -7}, 0, 2), -1, "all negative");

        Check.eq(power(2, 0), 1L, "anything to the zero");
        Check.eq(power(2, 10), 1024L, "2^10");
        Check.eq(power(3, 5), 243L, "odd exponent");
        Check.eq(power(2, 62), 4611686018427387904L, "2^62 still fits in a long");
        Check.threw(() -> power(2, -1), IllegalArgumentException.class, "negative exponent");

        Check.eq(countInversions(new int[] {1, 2, 3}), 0L, "sorted has no inversions");
        Check.eq(countInversions(new int[] {3, 2, 1}), 3L, "reversed has n(n-1)/2");
        Check.eq(countInversions(new int[] {2, 4, 1, 3, 5}), 3L, "mixed");
        Check.eq(countInversions(new int[0]), 0L, "empty");

        // Cross-check against the O(n^2) definition, which is what makes the clever
        // version trustworthy rather than merely plausible.
        int[] sample = {5, 2, 9, 1, 7, 3, 8, 4};
        long brute = 0;
        for (int i = 0; i < sample.length; i++) {
            for (int j = i + 1; j < sample.length; j++) {
                if (sample[i] > sample[j]) {
                    brute++;
                }
            }
        }
        Check.eq(countInversions(sample), brute, "agrees with the brute-force count");
    }
}
