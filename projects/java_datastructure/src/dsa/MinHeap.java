package dsa;

import java.util.NoSuchElementException;

/**
 * A binary min-heap - the data structure a PriorityQueue actually is.
 *
 * <p>Two things make it work. The <b>heap property</b>: every node is <= its children, so the
 * minimum is always at the root. And the <b>array layout</b>: the tree is stored in a flat array
 * with no node objects and no references at all, because a complete binary tree has a closed-form
 * index for every relationship.
 *
 * <pre>
 * parent(i) = (i - 1) / 2      left(i) = 2i + 1      right(i) = 2i + 2
 * </pre>
 *
 * <p>Note what a heap is NOT: sorted. Only the root is guaranteed. Iterating a PriorityQueue gives
 * you the array order, not ascending order, and that surprises people constantly - to get sorted
 * output you have to poll() repeatedly.
 */
public class MinHeap {

    private int[] items;
    private int size;

    public MinHeap() {
        this(16);
    }

    public MinHeap(int capacity) {
        this.items = new int[Math.max(1, capacity)];
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    /** O(log n) - the new element bubbles up at most the height of the tree. */
    public void add(int value) {
        if (size == items.length) {
            items = java.util.Arrays.copyOf(items, items.length * 2);
        }
        items[size] = value;
        siftUp(size);
        size++;
    }

    /** The minimum, without removing it. O(1) - it is just items[0]. */
    public int peek() {
        if (size == 0) {
            throw new NoSuchElementException("heap is empty");
        }
        return items[0];
    }

    /**
     * Remove and return the minimum. O(log n).
     *
     * <p>The move: promote the LAST element to the root, then sift it down. Promoting a child
     * instead would leave a hole in the middle of the array and break the complete-tree layout
     * every index calculation depends on.
     */
    public int poll() {
        if (size == 0) {
            throw new NoSuchElementException("heap is empty");
        }
        int min = items[0];
        items[0] = items[--size];
        siftDown(0);
        return min;
    }

    private void siftUp(int index) {
        while (index > 0) {
            int parent = (index - 1) / 2;
            if (items[index] >= items[parent]) {
                break;
            }
            swap(index, parent);
            index = parent;
        }
    }

    private void siftDown(int index) {
        while (true) {
            int left = 2 * index + 1;
            int right = 2 * index + 2;
            int smallest = index;

            if (left < size && items[left] < items[smallest]) {
                smallest = left;
            }
            if (right < size && items[right] < items[smallest]) {
                smallest = right;
            }
            if (smallest == index) {
                return;
            }
            swap(index, smallest);
            index = smallest;
        }
    }

    private void swap(int i, int j) {
        int tmp = items[i];
        items[i] = items[j];
        items[j] = tmp;
    }

    /**
     * Build a heap from an array in O(n), not O(n log n).
     *
     * <p>Adding n elements one at a time is n * O(log n). Sifting down from the last parent
     * backwards is O(n) - most nodes are near the bottom and barely move. A genuinely
     * counter-intuitive result, and the reason heapify exists as a separate operation.
     */
    public static MinHeap heapify(int[] values) {
        MinHeap heap = new MinHeap(Math.max(1, values.length));
        System.arraycopy(values, 0, heap.items, 0, values.length);
        heap.size = values.length;
        for (int i = values.length / 2 - 1; i >= 0; i--) {
            heap.siftDown(i);
        }
        return heap;
    }

    /**
     * The k smallest elements, using a heap of size k.
     *
     * <p>O(n log k) and O(k) space, where sorting the whole array to take k is O(n log n) and
     * O(n). When k is small and n is huge - "top 10 of a billion" - that is the difference
     * between fitting in memory and not.
     */
    public static int[] smallest(int[] values, int k) {
        if (k <= 0) {
            return new int[0];
        }
        MinHeap heap = heapify(values);
        int n = Math.min(k, values.length);
        int[] out = new int[n];
        for (int i = 0; i < n; i++) {
            out[i] = heap.poll();
        }
        return out;
    }

    static void check() {
        Check.section("MinHeap");

        MinHeap heap = new MinHeap(2);
        Check.threw(heap::poll, NoSuchElementException.class, "poll when empty");
        Check.threw(heap::peek, NoSuchElementException.class, "peek when empty");

        for (int v : new int[] {5, 3, 8, 1, 9, 2}) {
            heap.add(v);
        }
        Check.eq(heap.size(), 6, "size");
        Check.eq(heap.peek(), 1, "minimum at the root");
        Check.eq(heap.peek(), 1, "peek does not remove");

        StringBuilder drained = new StringBuilder();
        while (!heap.isEmpty()) {
            drained.append(heap.poll()).append(' ');
        }
        Check.eq(drained.toString().trim(), "1 2 3 5 8 9", "polling repeatedly yields sorted order");

        MinHeap built = MinHeap.heapify(new int[] {9, 4, 7, 1, 8, 2});
        Check.eq(built.size(), 6, "heapify keeps every element");
        Check.eq(built.poll(), 1, "heapify establishes the heap property");
        Check.eq(built.poll(), 2, "and holds it");

        Check.eq(java.util.Arrays.toString(smallest(new int[] {9, 4, 7, 1, 8, 2}, 3)),
                "[1, 2, 4]", "three smallest");
        Check.eq(java.util.Arrays.toString(smallest(new int[] {1}, 5)),
                "[1]", "k larger than the input");
        Check.eq(java.util.Arrays.toString(smallest(new int[] {1, 2}, 0)),
                "[]", "k of zero");

        // Duplicates must survive - a heap is a multiset, unlike the BST above.
        MinHeap dupes = new MinHeap();
        dupes.add(4);
        dupes.add(4);
        dupes.add(4);
        Check.eq(dupes.size(), 3, "duplicates are kept");
        Check.eq(dupes.poll(), 4, "and come back out");
    }
}
