package dsa;

import java.util.Arrays;

/**
 * What {@code ArrayList} is, with the lid off: an ordinary array plus a size, that replaces itself
 * with a bigger array when it runs out of room.
 *
 * <p>The only interesting decision is the growth factor. Doubling is what makes {@code add}
 * <b>amortised</b> O(1): the copies get more expensive as the array grows, but they also get
 * rarer, at exactly the rate that cancels out. Growing by a fixed +1 instead would make n adds
 * cost O(n^2) - the single most instructive mistake in this file.
 */
public class DynamicArray<E> {

    private Object[] items;
    private int size;

    public DynamicArray() {
        this(10);
    }

    public DynamicArray(int initialCapacity) {
        if (initialCapacity < 1) {
            throw new IllegalArgumentException("capacity must be positive");
        }
        this.items = new Object[initialCapacity];
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    /** Visible for the growth demonstration in the post - a real List does not expose this. */
    public int capacity() {
        return items.length;
    }

    /** Amortised O(1). The resize is O(n) but happens on a vanishing fraction of calls. */
    public void add(E item) {
        if (size == items.length) {
            grow();
        }
        items[size++] = item;
    }

    /** O(n) - every element from index onwards shifts up one slot. */
    public void add(int index, E item) {
        checkIndexForAdd(index);
        if (size == items.length) {
            grow();
        }
        System.arraycopy(items, index, items, index + 1, size - index);
        items[index] = item;
        size++;
    }

    @SuppressWarnings("unchecked")
    public E get(int index) {
        checkIndex(index);
        return (E) items[index];
    }

    @SuppressWarnings("unchecked")
    public E set(int index, E item) {
        checkIndex(index);
        E previous = (E) items[index];
        items[index] = item;
        return previous;
    }

    /** O(n) for the same reason as insert: the tail closes the gap. */
    @SuppressWarnings("unchecked")
    public E remove(int index) {
        checkIndex(index);
        E removed = (E) items[index];
        System.arraycopy(items, index + 1, items, index, size - index - 1);
        // Null the vacated slot. Without this the array keeps a reference to an object nobody
        // can reach any more, and it never becomes garbage - a real leak in a long-lived list.
        items[--size] = null;
        return removed;
    }

    public int indexOf(Object target) {
        for (int i = 0; i < size; i++) {
            if (items[i] == null ? target == null : items[i].equals(target)) {
                return i;
            }
        }
        return -1;
    }

    private void grow() {
        // Doubling is the whole trick. See the class comment.
        items = Arrays.copyOf(items, items.length * 2);
    }

    private void checkIndex(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("index " + index + " for size " + size);
        }
    }

    private void checkIndexForAdd(int index) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException("index " + index + " for size " + size);
        }
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < size; i++) {
            sb.append(i > 0 ? ", " : "").append(items[i]);
        }
        return sb.append(']').toString();
    }

    static void check() {
        Check.section("DynamicArray");

        DynamicArray<String> list = new DynamicArray<>(2);
        list.add("a");
        list.add("b");
        Check.eq(list.capacity(), 2, "capacity before growth");
        list.add("c");
        Check.eq(list.capacity(), 4, "capacity doubles, not +1");
        Check.eq(list.size(), 3, "size tracks adds, not capacity");
        Check.eq(list.toString(), "[a, b, c]", "append order");

        list.add(1, "x");
        Check.eq(list.toString(), "[a, x, b, c]", "insert shifts right");
        Check.eq(list.remove(0), "a", "remove returns the old value");
        Check.eq(list.toString(), "[x, b, c]", "remove closes the gap");
        Check.eq(list.indexOf("c"), 2, "indexOf scans");
        Check.eq(list.indexOf("nope"), -1, "indexOf misses");
        Check.eq(list.set(0, "y"), "x", "set returns the previous value");

        Check.threw(() -> list.get(99), IndexOutOfBoundsException.class, "get past the end");
        Check.threw(() -> new DynamicArray<>(0), IllegalArgumentException.class, "zero capacity");

        DynamicArray<Integer> counted = new DynamicArray<>(1);
        for (int i = 0; i < 1024; i++) {
            counted.add(i);
        }
        Check.eq(counted.capacity(), 1024, "1 doubled ten times");
        Check.eq(counted.size(), 1024, "all 1024 present");
    }
}
