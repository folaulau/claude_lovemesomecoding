package dsa;

import java.util.NoSuchElementException;

/**
 * A queue: first in, first out. Adds at one end, removes at the other.
 *
 * <p>This is a <b>circular buffer</b>, and that is the whole lesson. The naive version - an array
 * where dequeue shifts every remaining element down one - makes dequeue O(n) and is the single
 * most common way a hand-rolled queue goes wrong.
 *
 * <p>Instead, nothing moves. Two indices chase each other around the array and wrap with a modulo.
 * Both operations are O(1).
 */
public class ArrayQueue<E> {

    private Object[] items;
    private int head;  // index of the next element to come out
    private int size;

    public ArrayQueue() {
        this(10);
    }

    public ArrayQueue(int initialCapacity) {
        this.items = new Object[Math.max(1, initialCapacity)];
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    /** O(1) amortised. */
    public void enqueue(E item) {
        if (size == items.length) {
            grow();
        }
        items[(head + size) % items.length] = item;
        size++;
    }

    /** O(1) - nothing shifts, the head simply moves on. */
    @SuppressWarnings("unchecked")
    public E dequeue() {
        if (size == 0) {
            throw new NoSuchElementException("queue is empty");
        }
        E item = (E) items[head];
        items[head] = null;
        head = (head + 1) % items.length;
        size--;
        return item;
    }

    @SuppressWarnings("unchecked")
    public E peek() {
        if (size == 0) {
            throw new NoSuchElementException("queue is empty");
        }
        return (E) items[head];
    }

    /**
     * Growing has to UNROLL the wrap, not just copy the array.
     *
     * <p>Arrays.copyOf would preserve the physical layout, and a queue whose contents wrap past the
     * end would come out reordered. Copying element by element in logical order is the fix, and
     * forgetting it produces a bug that only appears once the buffer has wrapped at least once -
     * so it survives every small test.
     */
    private void grow() {
        Object[] bigger = new Object[items.length * 2];
        for (int i = 0; i < size; i++) {
            bigger[i] = items[(head + i) % items.length];
        }
        items = bigger;
        head = 0;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < size; i++) {
            sb.append(i > 0 ? ", " : "").append(items[(head + i) % items.length]);
        }
        return sb.append(']').toString();
    }

    static void check() {
        Check.section("ArrayQueue");

        ArrayQueue<Integer> q = new ArrayQueue<>(3);
        Check.threw(q::dequeue, NoSuchElementException.class, "dequeue when empty");

        q.enqueue(1);
        q.enqueue(2);
        q.enqueue(3);
        Check.eq(q.toString(), "[1, 2, 3]", "FIFO order");
        Check.eq(q.dequeue(), 1, "first in, first out");
        Check.eq(q.peek(), 2, "peek does not remove");

        // Now head is 1 and the next enqueue wraps to index 0.
        q.enqueue(4);
        Check.eq(q.toString(), "[2, 3, 4]", "enqueue wraps around");
        Check.eq(q.size(), 3, "size after wrap");

        // Force a grow while the contents are wrapped - the case the naive copy breaks.
        q.enqueue(5);
        Check.eq(q.toString(), "[2, 3, 4, 5]", "grow unrolls the wrap in order");
        Check.eq(q.dequeue(), 2, "still FIFO after growing");
        Check.eq(q.dequeue(), 3, "and again");
        Check.eq(q.dequeue(), 4, "and again");
        Check.eq(q.dequeue(), 5, "and again");
        Check.isTrue(q.isEmpty(), "drained");
    }
}
