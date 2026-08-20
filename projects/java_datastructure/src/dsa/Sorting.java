package dsa;

import java.util.Arrays;

/**
 * Merge sort and quick sort - the two O(n log n) sorts worth knowing by heart, and the reason
 * there are two of them.
 *
 * <p>Merge sort is O(n log n) always, and stable, but needs O(n) extra space. Quick sort sorts in
 * place with O(log n) stack, is usually faster in practice because of cache behaviour, and has an
 * O(n^2) worst case. Neither dominates, which is why Java ships both: Arrays.sort on primitives is
 * a dual-pivot quicksort, and on objects it is a merge sort (TimSort) - precisely because objects
 * need stability and primitives cannot tell equal elements apart.
 */
public final class Sorting {

    private Sorting() {}

    // ---------------------------------------------------------------- merge sort

    /** Divide in half, sort each half, merge. O(n log n) time, O(n) space, stable. */
    public static void mergeSort(int[] a) {
        if (a.length < 2) {
            return;
        }
        // Allocated ONCE, here, and reused by every level of the recursion. Allocating inside
        // merge() instead is the usual version and it churns O(n log n) arrays for no reason.
        int[] buffer = new int[a.length];
        mergeSort(a, buffer, 0, a.length - 1);
    }

    private static void mergeSort(int[] a, int[] buffer, int low, int high) {
        if (low >= high) {
            return;
        }
        int mid = low + (high - low) / 2;
        mergeSort(a, buffer, low, mid);
        mergeSort(a, buffer, mid + 1, high);

        // Already in order - skip the merge entirely. Cheap to check, and it makes an
        // already-sorted array O(n log n) with no data movement at all.
        if (a[mid] <= a[mid + 1]) {
            return;
        }
        merge(a, buffer, low, mid, high);
    }

    private static void merge(int[] a, int[] buffer, int low, int mid, int high) {
        System.arraycopy(a, low, buffer, low, high - low + 1);

        int left = low;
        int right = mid + 1;
        for (int i = low; i <= high; i++) {
            if (left > mid) {
                a[i] = buffer[right++];
            } else if (right > high) {
                a[i] = buffer[left++];
            } else if (buffer[right] < buffer[left]) {
                a[i] = buffer[right++];
            } else {
                // <= keeps the LEFT element when they are equal. That single choice is what
                // makes this sort stable; flipping it to < silently breaks stability.
                a[i] = buffer[left++];
            }
        }
    }

    // ---------------------------------------------------------------- quick sort

    /** Partition around a pivot, recurse on both sides. In place, O(log n) stack. */
    public static void quickSort(int[] a) {
        quickSort(a, 0, a.length - 1);
    }

    private static void quickSort(int[] a, int low, int high) {
        while (low < high) {
            int p = partition(a, low, high);
            // Recurse into the SMALLER side and loop on the larger. This caps stack depth at
            // O(log n) even on input that would otherwise degrade - without it, a sorted array
            // plus a bad pivot is a StackOverflowError, not merely a slow sort.
            if (p - low < high - p) {
                quickSort(a, low, p - 1);
                low = p + 1;
            } else {
                quickSort(a, p + 1, high);
                high = p - 1;
            }
        }
    }

    /** Lomuto partition, with a median-of-three pivot. */
    private static int partition(int[] a, int low, int high) {
        // A fixed pivot (always a[high]) makes ALREADY-SORTED input the O(n^2) worst case -
        // which is the input you are most likely to be handed. Median-of-three costs three
        // comparisons and removes that.
        int mid = low + (high - low) / 2;
        if (a[mid] < a[low]) {
            swap(a, low, mid);
        }
        if (a[high] < a[low]) {
            swap(a, low, high);
        }
        if (a[high] < a[mid]) {
            swap(a, mid, high);
        }
        swap(a, mid, high);

        int pivot = a[high];
        int boundary = low;
        for (int i = low; i < high; i++) {
            if (a[i] < pivot) {
                swap(a, i, boundary++);
            }
        }
        swap(a, boundary, high);
        return boundary;
    }

    private static void swap(int[] a, int i, int j) {
        int tmp = a[i];
        a[i] = a[j];
        a[j] = tmp;
    }

    // ---------------------------------------------------------------- for contrast

    /** O(n^2). Here only so the post can measure it against the two above. */
    public static void bubbleSort(int[] a) {
        for (int pass = 0; pass < a.length - 1; pass++) {
            boolean swapped = false;
            for (int i = 0; i < a.length - 1 - pass; i++) {
                if (a[i] > a[i + 1]) {
                    swap(a, i, i + 1);
                    swapped = true;
                }
            }
            if (!swapped) {
                return; // already sorted - this is what makes best case O(n)
            }
        }
    }

    static void check() {
        Check.section("Sorting");

        int[][] cases = {
            {},
            {1},
            {2, 1},
            {5, 3, 8, 1, 9, 2, 7},
            {1, 2, 3, 4, 5},          // already sorted - quicksort's classic worst case
            {5, 4, 3, 2, 1},          // reversed
            {7, 7, 7, 7},             // all equal
            {3, -1, 0, -9, 4},        // negatives
        };

        for (int[] original : cases) {
            int[] expected = original.clone();
            Arrays.sort(expected);

            int[] m = original.clone();
            mergeSort(m);
            Check.eq(Arrays.toString(m), Arrays.toString(expected), "mergeSort " + Arrays.toString(original));

            int[] q = original.clone();
            quickSort(q);
            Check.eq(Arrays.toString(q), Arrays.toString(expected), "quickSort " + Arrays.toString(original));

            int[] b = original.clone();
            bubbleSort(b);
            Check.eq(Arrays.toString(b), Arrays.toString(expected), "bubbleSort " + Arrays.toString(original));
        }

        // A big, deterministic, pseudo-random array - the case small fixtures never cover.
        int[] big = new int[5000];
        long seed = 42;
        for (int i = 0; i < big.length; i++) {
            seed = seed * 6364136223846793005L + 1442695040888963407L;
            big[i] = (int) (seed >>> 33);
        }
        int[] expected = big.clone();
        Arrays.sort(expected);

        int[] m = big.clone();
        mergeSort(m);
        Check.isTrue(Arrays.equals(m, expected), "mergeSort on 5000 elements");

        int[] q = big.clone();
        quickSort(q);
        Check.isTrue(Arrays.equals(q, expected), "quickSort on 5000 elements");

        // Sorted input used to blow the stack with a fixed pivot. 100k elements proves it does not.
        int[] ascending = new int[100_000];
        for (int i = 0; i < ascending.length; i++) {
            ascending[i] = i;
        }
        quickSort(ascending);
        Check.eq(ascending[0], 0, "100k sorted input does not overflow the stack");
        Check.eq(ascending[99_999], 99_999, "and is still sorted");
    }
}
