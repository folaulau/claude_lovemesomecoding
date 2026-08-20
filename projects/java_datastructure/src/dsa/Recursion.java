package dsa;

import java.util.ArrayList;
import java.util.List;

/**
 * Recursion: a method that calls itself on a smaller version of the same problem.
 *
 * <p>Two parts, always. A <b>base case</b> that returns without recursing, and a <b>recursive
 * case</b> that must make progress towards it. Miss either and you get StackOverflowError - which
 * is not a mysterious failure, it is the runtime telling you the base case is never reached.
 *
 * <p>Java has no tail-call optimisation, so depth is bounded by the stack - a few thousand frames.
 * Any recursion whose depth scales with n over about 10,000 has to be rewritten as a loop.
 */
public final class Recursion {

    private Recursion() {}

    public static long factorial(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("factorial of a negative number");
        }
        if (n <= 1) {
            return 1;          // base case
        }
        return n * factorial(n - 1);
    }

    /**
     * The naive Fibonacci - deliberately kept, because it is the clearest example of a recursion
     * that is correct and useless. Each call spawns two more, so this is O(2^n): fib(50) would
     * take longer than a lunch break. {@link DynamicProgramming#fibonacci} is the fix.
     */
    public static long fibonacciNaive(int n) {
        if (n < 2) {
            return n;
        }
        return fibonacciNaive(n - 1) + fibonacciNaive(n - 2);
    }

    public static String reverse(String s) {
        if (s.length() <= 1) {
            return s;
        }
        return reverse(s.substring(1)) + s.charAt(0);
    }

    public static boolean isPalindrome(String s) {
        String cleaned = s.toLowerCase().replaceAll("[^a-z0-9]", "");
        return palindrome(cleaned, 0, cleaned.length() - 1);
    }

    private static boolean palindrome(String s, int low, int high) {
        if (low >= high) {
            return true;
        }
        if (s.charAt(low) != s.charAt(high)) {
            return false;
        }
        return palindrome(s, low + 1, high - 1);
    }

    /** The same job as a loop, to make the trade-off concrete: no stack, but less direct. */
    public static long factorialIterative(int n) {
        long result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    /**
     * Towers of Hanoi - the problem recursion is genuinely better at.
     *
     * <p>The iterative solution exists and nobody can read it. Three lines of recursion say the
     * whole thing: move n-1 out of the way, move the big one, move n-1 back.
     */
    public static List<String> hanoi(int discs) {
        List<String> moves = new ArrayList<>();
        hanoi(discs, 'A', 'C', 'B', moves);
        return moves;
    }

    private static void hanoi(int n, char from, char to, char via, List<String> moves) {
        if (n == 0) {
            return;
        }
        hanoi(n - 1, from, via, to, moves);
        moves.add(n + ":" + from + "->" + to);
        hanoi(n - 1, via, to, from, moves);
    }

    static void check() {
        Check.section("Recursion");

        Check.eq(factorial(0), 1L, "0! is 1");
        Check.eq(factorial(1), 1L, "1! is 1");
        Check.eq(factorial(5), 120L, "5!");
        Check.eq(factorial(20), 2432902008176640000L, "20! is the largest that fits in a long");
        Check.threw(() -> factorial(-1), IllegalArgumentException.class, "negative factorial");
        Check.eq(factorialIterative(10), factorial(10), "loop and recursion agree");

        Check.eq(fibonacciNaive(0), 0L, "fib(0)");
        Check.eq(fibonacciNaive(1), 1L, "fib(1)");
        Check.eq(fibonacciNaive(10), 55L, "fib(10)");
        Check.eq(fibonacciNaive(20), 6765L, "fib(20)");

        Check.eq(reverse(""), "", "reverse empty");
        Check.eq(reverse("a"), "a", "reverse single");
        Check.eq(reverse("abc"), "cba", "reverse");

        Check.isTrue(isPalindrome("racecar"), "palindrome");
        Check.isTrue(isPalindrome("A man, a plan, a canal: Panama"), "palindrome ignoring punctuation");
        Check.isTrue(isPalindrome(""), "empty is a palindrome");
        Check.isTrue(!isPalindrome("hello"), "not a palindrome");

        // 2^n - 1 moves, the closed form. Proving it holds for several n is the real check.
        Check.eq(hanoi(0).size(), 0, "no discs, no moves");
        Check.eq(hanoi(1).size(), 1, "one disc");
        Check.eq(hanoi(3).size(), 7, "three discs is 2^3 - 1");
        Check.eq(hanoi(10).size(), 1023, "ten discs is 2^10 - 1");
        Check.eq(hanoi(3).toString(),
                "[1:A->C, 2:A->B, 1:C->B, 3:A->C, 1:B->A, 2:B->C, 1:A->C]", "the actual moves");

        // The stack is finite, and that is a fact worth demonstrating rather than asserting.
        Check.threw(() -> deepRecursion(1_000_000), StackOverflowError.class,
                "a million frames overflows the stack");
    }

    private static void deepRecursion(int n) {
        if (n == 0) {
            return;
        }
        deepRecursion(n - 1);
    }
}
