package dsa;

import java.util.NoSuchElementException;

/**
 * A singly linked list: nodes holding a value and a reference to the next node.
 *
 * <p>The contrast with {@link DynamicArray} is the entire reason both exist. A list wins at the
 * front - {@code addFirst} is O(1) where an array's insert-at-0 is O(n). An array wins at random
 * access - {@code get(i)} is O(1) where this has to walk i links. Neither is "faster"; they are
 * fast at different things.
 *
 * <p>A tail reference is what keeps {@code addLast} O(1). Without it, appending walks the whole
 * list every time and building an n-element list costs O(n^2).
 */
public class SinglyLinkedList<E> {

    /** A record cannot be used here: next has to be reassigned as the list changes. */
    private static final class Node<E> {
        E value;
        Node<E> next;

        Node(E value) {
            this.value = value;
        }
    }

    private Node<E> head;
    private Node<E> tail;
    private int size;

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    /** O(1) - the whole point of a linked list. */
    public void addFirst(E value) {
        Node<E> node = new Node<>(value);
        if (head == null) {
            head = tail = node;
        } else {
            node.next = head;
            head = node;
        }
        size++;
    }

    /** O(1) only because of the tail reference. */
    public void addLast(E value) {
        Node<E> node = new Node<>(value);
        if (tail == null) {
            head = tail = node;
        } else {
            tail.next = node;
            tail = node;
        }
        size++;
    }

    public E removeFirst() {
        if (head == null) {
            throw new NoSuchElementException("list is empty");
        }
        E value = head.value;
        head = head.next;
        if (head == null) {
            tail = null; // the list just became empty - a dangling tail would leak the old node
        }
        size--;
        return value;
    }

    /**
     * O(n), and that asymmetry is worth noticing: removing the LAST element needs the node before
     * it, and a singly linked list has no way back. This is the argument for a doubly linked list,
     * which is what java.util.LinkedList actually is.
     */
    public E removeLast() {
        if (head == null) {
            throw new NoSuchElementException("list is empty");
        }
        if (head == tail) {
            E value = head.value;
            head = tail = null;
            size--;
            return value;
        }
        Node<E> current = head;
        while (current.next != tail) {
            current = current.next;
        }
        E value = tail.value;
        current.next = null;
        tail = current;
        size--;
        return value;
    }

    /** O(n) - there is no index arithmetic to jump with. */
    public E get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("index " + index + " for size " + size);
        }
        Node<E> current = head;
        for (int i = 0; i < index; i++) {
            current = current.next;
        }
        return current.value;
    }

    public boolean contains(E value) {
        for (Node<E> n = head; n != null; n = n.next) {
            if (n.value == null ? value == null : n.value.equals(value)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Reverses the list in place, in one pass and with no extra allocation.
     *
     * <p>Three references, and the order of the four lines is the whole exercise: stash next
     * before overwriting the link, or the rest of the list becomes unreachable.
     */
    public void reverse() {
        Node<E> previous = null;
        Node<E> current = head;
        tail = head;
        while (current != null) {
            Node<E> next = current.next;
            current.next = previous;
            previous = current;
            current = next;
        }
        head = previous;
    }

    /**
     * Floyd's cycle detection - the "tortoise and hare".
     *
     * <p>One pointer moves one step, the other two. If there is a cycle the fast one laps the slow
     * one and they meet; if there is not, the fast one runs off the end. O(n) time and O(1) space,
     * where the obvious solution (a HashSet of visited nodes) costs O(n) space.
     */
    public boolean hasCycle() {
        Node<E> slow = head;
        Node<E> fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                return true;
            }
        }
        return false;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        for (Node<E> n = head; n != null; n = n.next) {
            sb.append(n != head ? ", " : "").append(n.value);
        }
        return sb.append(']').toString();
    }

    static void check() {
        Check.section("SinglyLinkedList");

        SinglyLinkedList<Integer> list = new SinglyLinkedList<>();
        Check.isTrue(list.isEmpty(), "starts empty");
        Check.threw(list::removeFirst, NoSuchElementException.class, "removeFirst when empty");

        list.addLast(2);
        list.addLast(3);
        list.addFirst(1);
        Check.eq(list.toString(), "[1, 2, 3]", "addFirst and addLast");
        Check.eq(list.size(), 3, "size");
        Check.eq(list.get(1), 2, "get walks");
        Check.isTrue(list.contains(3), "contains hit");
        Check.isTrue(!list.contains(9), "contains miss");

        list.reverse();
        Check.eq(list.toString(), "[3, 2, 1]", "reverse in place");
        // The tail must have moved too, or a later addLast appends to the wrong end.
        list.addLast(0);
        Check.eq(list.toString(), "[3, 2, 1, 0]", "tail is correct after reverse");

        Check.eq(list.removeFirst(), 3, "removeFirst returns the value");
        Check.eq(list.removeLast(), 0, "removeLast returns the value");
        Check.eq(list.toString(), "[2, 1]", "after both removals");

        SinglyLinkedList<Integer> single = new SinglyLinkedList<>();
        single.addFirst(42);
        Check.eq(single.removeLast(), 42, "removeLast on a one-element list");
        Check.isTrue(single.isEmpty(), "empty again");

        Check.isTrue(!list.hasCycle(), "no cycle in a normal list");
    }
}
