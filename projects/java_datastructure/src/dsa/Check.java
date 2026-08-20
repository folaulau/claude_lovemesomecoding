package dsa;

/**
 * A three-line test harness.
 *
 * <p>Deliberately not JUnit: this project has no build tool and no dependencies, so the whole
 * thing compiles with a bare {@code javac} and runs with a bare {@code java}. That matters because
 * every sample in the track is copied out of these files, and a reader has to be able to run them
 * the same way.
 */
public final class Check {

    private static int passed = 0;
    private static int failed = 0;

    private Check() {}

    public static void eq(Object actual, Object expected, String label) {
        if (String.valueOf(actual).equals(String.valueOf(expected))) {
            passed++;
        } else {
            failed++;
            System.out.printf("  FAIL %s%n    expected: %s%n    actual:   %s%n", label, expected, actual);
        }
    }

    public static void isTrue(boolean condition, String label) {
        eq(condition, true, label);
    }

    public static void threw(Runnable body, Class<? extends Throwable> expected, String label) {
        try {
            body.run();
            eq("no exception", expected.getSimpleName(), label);
        } catch (Throwable actual) {
            eq(actual.getClass().getSimpleName(), expected.getSimpleName(), label);
        }
    }

    public static void section(String name) {
        System.out.println("  " + name);
    }

    public static int report() {
        System.out.printf("%n%d passed, %d failed%n", passed, failed);
        return failed == 0 ? 0 : 1;
    }
}
