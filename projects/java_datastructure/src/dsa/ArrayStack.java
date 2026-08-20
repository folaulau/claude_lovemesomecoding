package dsa;

import java.util.EmptyStackException;

/**
 * A stack: last in, first out. Every operation happens at one end.
 *
 * <p>Backed by an array rather than a linked list, because a stack only ever touches the top and
 * an array's end is exactly where appends are cheap. All three operations are O(1) - push is
 * amortised, for the same doubling reason as {@link DynamicArray}.
 *
 * <p><b>Do not use java.util.Stack.</b> It extends Vector, so every method is synchronised whether
 * or not you are sharing it, and - worse - inheriting from Vector means it also exposes get(int),
 * so callers can reach into the middle of a "stack". Use ArrayDeque instead.
 */
public class ArrayStack<E> {

    private Object[] items;
    private int size;

    public ArrayStack() {
        this(10);
    }

    public ArrayStack(int initialCapacity) {
        this.items = new Object[Math.max(1, initialCapacity)];
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public void push(E item) {
        if (size == items.length) {
            items = java.util.Arrays.copyOf(items, items.length * 2);
        }
        items[size++] = item;
    }

    @SuppressWarnings("unchecked")
    public E pop() {
        if (size == 0) {
            throw new EmptyStackException();
        }
        E item = (E) items[--size];
        items[size] = null; // let it be collected
        return item;
    }

    @SuppressWarnings("unchecked")
    public E peek() {
        if (size == 0) {
            throw new EmptyStackException();
        }
        return (E) items[size - 1];
    }

    /**
     * The canonical stack problem, and the reason interviewers ask it: it is the smallest problem
     * where a stack is obviously the right answer. Each closing bracket must match the most
     * recently opened one - which is the definition of LIFO.
     */
    public static boolean balanced(String input) {
        ArrayStack<Character> stack = new ArrayStack<>();
        for (char c : input.toCharArray()) {
            switch (c) {
                case '(', '[', '{' -> stack.push(c);
                case ')' -> {
                    if (stack.isEmpty() || stack.pop() != '(') {
                        return false;
                    }
                }
                case ']' -> {
                    if (stack.isEmpty() || stack.pop() != '[') {
                        return false;
                    }
                }
                case '}' -> {
                    if (stack.isEmpty() || stack.pop() != '{') {
                        return false;
                    }
                }
                default -> { }
            }
        }
        // Anything still open is unbalanced - the check people forget.
        return stack.isEmpty();
    }

    static void check() {
        Check.section("ArrayStack");

        ArrayStack<String> stack = new ArrayStack<>(1);
        Check.threw(stack::pop, EmptyStackException.class, "pop when empty");

        stack.push("a");
        stack.push("b");
        Check.eq(stack.peek(), "b", "peek does not remove");
        Check.eq(stack.size(), 2, "size after peek");
        Check.eq(stack.pop(), "b", "LIFO");
        Check.eq(stack.pop(), "a", "LIFO again");
        Check.isTrue(stack.isEmpty(), "empty after popping both");

        Check.isTrue(balanced("()"), "simple pair");
        Check.isTrue(balanced("{[()]}"), "nested");
        Check.isTrue(balanced("a(b)[c]{d}"), "with other characters");
        Check.isTrue(!balanced("(]"), "mismatched pair");
        Check.isTrue(!balanced("("), "never closed");
        Check.isTrue(!balanced(")("), "closed before opened");
        Check.isTrue(balanced(""), "empty string is balanced");
    }
}
