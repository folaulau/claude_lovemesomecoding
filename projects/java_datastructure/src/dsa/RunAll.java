package dsa;

/**
 * Runs every check in the track.
 *
 * <p>Every Java sample published under /data-structure-algorithm is copied out of these files, and
 * check_content.py fails if a snippet and its source have drifted apart. So this is not a nice
 * extra - it is what makes "the code in the post works" a measured claim rather than a hope.
 *
 * <pre>
 * javac -d out src/dsa/*.java &amp;&amp; java -cp out dsa.RunAll
 * </pre>
 */
public final class RunAll {

    public static void main(String[] args) {
        System.out.println("data structures and algorithms - Java " + Runtime.version().feature());
        System.out.println();

        DynamicArray.check();
        SinglyLinkedList.check();
        ArrayStack.check();
        ArrayQueue.check();
        HashTable.check();
        Searching.check();
        Sorting.check();
        BinarySearchTree.check();
        MinHeap.check();
        Trie.check();
        Graph.check();
        Recursion.check();
        DivideAndConquer.check();
        DynamicProgramming.check();
        Greedy.check();
        JdkCollections.check();

        System.exit(Check.report());
    }
}
