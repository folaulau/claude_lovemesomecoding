package dsa;

/** Binary search, and the three places it is usually got wrong. */
public final class Searching {

    private Searching() {}

    /**
     * Classic binary search over a SORTED array. O(log n).
     *
     * <p>"Sorted" is a precondition, not a suggestion: on unsorted input this returns a wrong
     * answer rather than failing, which is the worst kind of bug.
     */
    public static int binarySearch(int[] sorted, int target) {
        int low = 0;
        int high = sorted.length - 1;

        while (low <= high) {
            // NOT (low + high) / 2. On a large array that sum overflows int and goes negative,
            // and the negative index throws. Java's own Arrays.binarySearch carried this bug
            // until 2006. Subtracting first cannot overflow.
            int mid = low + (high - low) / 2;

            if (sorted[mid] == target) {
                return mid;
            }
            if (sorted[mid] < target) {
                low = mid + 1;   // mid + 1, not mid, or a two-element range loops forever
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }

    /** The same algorithm written recursively - identical O(log n), but O(log n) stack. */
    public static int binarySearchRecursive(int[] sorted, int target, int low, int high) {
        if (low > high) {
            return -1;
        }
        int mid = low + (high - low) / 2;
        if (sorted[mid] == target) {
            return mid;
        }
        return sorted[mid] < target
                ? binarySearchRecursive(sorted, target, mid + 1, high)
                : binarySearchRecursive(sorted, target, low, mid - 1);
    }

    /**
     * The variant that actually earns its keep: the FIRST index whose value is >= target.
     *
     * <p>Plain binary search answers "is it there". This answers "where does it belong", which is
     * what you need for insertion points, range queries and every "first element greater than x"
     * problem. Note the loop is {@code low < high} and the else branch keeps mid.
     */
    public static int lowerBound(int[] sorted, int target) {
        int low = 0;
        int high = sorted.length;   // one PAST the end, deliberately
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (sorted[mid] < target) {
                low = mid + 1;
            } else {
                high = mid;         // mid might be the answer, so do not exclude it
            }
        }
        return low;
    }

    public static int linearSearch(int[] values, int target) {
        for (int i = 0; i < values.length; i++) {
            if (values[i] == target) {
                return i;
            }
        }
        return -1;
    }

    static void check() {
        Check.section("Searching");

        int[] sorted = {1, 3, 5, 7, 9, 11};
        Check.eq(binarySearch(sorted, 1), 0, "first element");
        Check.eq(binarySearch(sorted, 11), 5, "last element");
        Check.eq(binarySearch(sorted, 7), 3, "middle element");
        Check.eq(binarySearch(sorted, 4), -1, "absent value");
        Check.eq(binarySearch(new int[0], 1), -1, "empty array");
        Check.eq(binarySearch(new int[] {42}, 42, 0, 0), 0, "single element hit");

        Check.eq(binarySearchRecursive(sorted, 9, 0, sorted.length - 1), 4, "recursive agrees");
        Check.eq(binarySearchRecursive(sorted, 2, 0, sorted.length - 1), -1, "recursive miss");

        Check.eq(lowerBound(sorted, 5), 2, "lowerBound on an exact match");
        Check.eq(lowerBound(sorted, 4), 2, "lowerBound between values");
        Check.eq(lowerBound(sorted, 0), 0, "lowerBound below everything");
        Check.eq(lowerBound(sorted, 99), 6, "lowerBound above everything");

        // The overflow case, stated as an arithmetic fact rather than by allocating 2bn ints.
        int low = 1_500_000_000;
        int high = 2_000_000_000;
        Check.isTrue(low + high < 0, "low + high really does overflow");
        Check.isTrue(low + (high - low) / 2 > 0, "the safe form does not");

        Check.eq(linearSearch(new int[] {4, 2, 9}, 9), 2, "linear search finds it");
        Check.eq(linearSearch(new int[] {4, 2, 9}, 5), -1, "linear search misses");
    }

    /** Overload so the single-element assertion above reads naturally. */
    private static int binarySearch(int[] sorted, int target, int low, int high) {
        return binarySearchRecursive(sorted, target, low, high);
    }
}
