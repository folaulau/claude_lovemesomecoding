package dsa;

import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Deque;
import java.util.PriorityQueue;
import java.util.Queue;

/**
 * The standard-library counterparts of the structures in this track.
 *
 * <p>The posts show a hand-written implementation and then the JDK class you would actually use.
 * Those JDK snippets live here rather than only in the prose, so that they are compiled and
 * asserted like everything else - otherwise the "every sample is verified" claim would quietly
 * have a hole in it exactly where readers are most likely to copy and paste.
 *
 * <p>Several of the assertions below exist to pin down behaviour that surprises people: that a
 * PriorityQueue does not iterate in sorted order, that ArrayDeque.push adds to the front, and what
 * Arrays.binarySearch returns when it misses.
 */
public final class JdkCollections {

    private JdkCollections() {}

    /** A task with a priority, for the comparator example. */
    public record Task(int priority, String name) {}

    static void check() {
        Check.section("JdkCollections");

        // ---------------------------------------------------------------- ArrayDeque as a stack
        Deque<String> stack = new ArrayDeque<>();
        stack.push("a");
        stack.push("b");
        Check.eq(stack.pop(), "b", "ArrayDeque as a LIFO stack");

        // push() adds to the FRONT, so iteration runs top-to-bottom - the opposite of the
        // legacy java.util.Stack, which extends Vector and iterates bottom-to-top.
        stack.push("c");
        Check.eq(stack.toString(), "[c, a]", "ArrayDeque iterates top-first");

        // ---------------------------------------------------------------- ArrayDeque as a queue
        Queue<String> queue = new ArrayDeque<>();
        queue.add("first");
        queue.add("second");
        Check.eq(queue.remove(), "first", "ArrayDeque as a FIFO queue");

        // poll() returns null when empty; remove() throws. That is the whole difference.
        queue.clear();
        Check.eq(queue.poll(), null, "poll returns null when empty");
        Check.threw(queue::remove, java.util.NoSuchElementException.class, "remove throws when empty");

        // ---------------------------------------------------------------- PriorityQueue
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.add(5);
        pq.add(1);
        pq.add(3);
        Check.eq(pq.poll(), 1, "min-heap by default - smallest first, not first added");

        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
        maxHeap.add(5);
        maxHeap.add(1);
        maxHeap.add(3);
        Check.eq(maxHeap.poll(), 5, "the comparator is the only difference from a max-heap");

        PriorityQueue<Task> tasks = new PriorityQueue<>(
                Comparator.comparingInt(Task::priority).thenComparing(Task::name));
        tasks.add(new Task(2, "b"));
        tasks.add(new Task(1, "z"));
        tasks.add(new Task(1, "a"));
        Check.eq(tasks.poll().name(), "a", "ties broken by the second comparator");
        Check.eq(tasks.poll().name(), "z", "then the rest of priority 1");

        // ---------------------------------------------------------------- top k with a size-k heap
        // Min-heap for the k LARGEST: the root is the weakest of the current best k, so it is
        // the one to discard. Getting that inversion backwards is the usual mistake.
        int[] values = {9, 4, 7, 1, 8, 2, 6};
        int k = 3;
        PriorityQueue<Integer> topK = new PriorityQueue<>();
        for (int value : values) {
            topK.add(value);
            if (topK.size() > k) {
                topK.poll();          // drop the smallest of the k+1
            }
        }
        Check.eq(topK.size(), 3, "the heap never grows past k");
        Check.eq(topK.poll(), 7, "third largest");
        Check.eq(topK.poll(), 8, "second largest");
        Check.eq(topK.poll(), 9, "largest");

        // ---------------------------------------------------------------- Arrays.binarySearch
        int[] sorted = {1, 3, 5, 7, 9, 11};
        int target = 7;
        int index = Arrays.binarySearch(sorted, target);
        Check.eq(index, 3, "Arrays.binarySearch on a hit");

        // On a miss it returns -(insertionPoint) - 1. The -1 exists because insertion point 0
        // would otherwise be indistinguishable from a hit at index 0.
        int miss = Arrays.binarySearch(sorted, 4);
        Check.isTrue(miss < 0, "a miss is negative");
        Check.eq(-miss - 1, 2, "and decodes to the insertion point");
        Check.eq(-miss - 1, Searching.lowerBound(sorted, 4), "which is lowerBound by another name");
    }
}
