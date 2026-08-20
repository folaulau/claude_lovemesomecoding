package dsa;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

/**
 * A binary search tree: every node's left subtree holds smaller keys, its right subtree larger.
 *
 * <p>That one invariant is what buys O(log n) search - each comparison discards half the
 * remaining tree. But only if the tree is BALANCED. Insert 1, 2, 3, 4, 5 in order and every node
 * hangs off the right of the last: a linked list wearing a tree costume, at O(n). Real
 * implementations (TreeMap is a red-black tree) rebalance on insert; this one does not, so the
 * degenerate case stays visible.
 */
public class BinarySearchTree {

    private static final class Node {
        int value;
        Node left;
        Node right;

        Node(int value) {
            this.value = value;
        }
    }

    private Node root;
    private int size;

    public int size() {
        return size;
    }

    public void insert(int value) {
        root = insert(root, value);
    }

    private Node insert(Node node, int value) {
        if (node == null) {
            size++;
            return new Node(value);
        }
        if (value < node.value) {
            node.left = insert(node.left, value);
        } else if (value > node.value) {
            node.right = insert(node.right, value);
        }
        // value == node.value: a SET, so duplicates are ignored rather than stored twice
        return node;
    }

    public boolean contains(int value) {
        Node current = root;
        while (current != null) {
            if (value == current.value) {
                return true;
            }
            current = value < current.value ? current.left : current.right;
        }
        return false;
    }

    /**
     * Deletion, the part everyone skips.
     *
     * <p>Three cases: no children (drop it), one child (promote it), two children (replace the
     * value with the smallest value in the right subtree - the in-order successor - then delete
     * that successor, which by construction has at most one child).
     */
    public void delete(int value) {
        root = delete(root, value);
    }

    private Node delete(Node node, int value) {
        if (node == null) {
            return null;
        }
        if (value < node.value) {
            node.left = delete(node.left, value);
        } else if (value > node.value) {
            node.right = delete(node.right, value);
        } else if (node.left == null) {
            size--;
            return node.right;
        } else if (node.right == null) {
            size--;
            return node.left;
        } else {
            // Two children. Replace this node's value with its in-order successor - the smallest
            // value in the right subtree - then delete that successor from the right subtree.
            // The successor has no left child by construction, so that second delete always hits
            // one of the easy cases above and decrements size exactly once.
            Node successor = node.right;
            while (successor.left != null) {
                successor = successor.left;
            }
            node.value = successor.value;
            node.right = delete(node.right, successor.value);
        }
        return node;
    }

    /** In-order: left, node, right. On a BST this comes out SORTED - that is the whole trick. */
    public List<Integer> inOrder() {
        List<Integer> out = new ArrayList<>();
        inOrder(root, out);
        return out;
    }

    private void inOrder(Node node, List<Integer> out) {
        if (node == null) {
            return;
        }
        inOrder(node.left, out);
        out.add(node.value);
        inOrder(node.right, out);
    }

    /** Pre-order: node, left, right. Used to copy or serialise a tree. */
    public List<Integer> preOrder() {
        List<Integer> out = new ArrayList<>();
        preOrder(root, out);
        return out;
    }

    private void preOrder(Node node, List<Integer> out) {
        if (node == null) {
            return;
        }
        out.add(node.value);
        preOrder(node.left, out);
        preOrder(node.right, out);
    }

    /** Post-order: left, right, node. Used to free or fold a tree bottom-up. */
    public List<Integer> postOrder() {
        List<Integer> out = new ArrayList<>();
        postOrder(root, out);
        return out;
    }

    private void postOrder(Node node, List<Integer> out) {
        if (node == null) {
            return;
        }
        postOrder(node.left, out);
        postOrder(node.right, out);
        out.add(node.value);
    }

    /**
     * Level order - breadth-first, using a queue.
     *
     * <p>The other three traversals are depth-first and recurse. This one cannot: there is no
     * recursive formulation of "visit everything one level down". Queue for breadth, stack (or
     * recursion, which is a stack) for depth - that pairing is the thing to remember.
     */
    public List<Integer> levelOrder() {
        List<Integer> out = new ArrayList<>();
        if (root == null) {
            return out;
        }
        Deque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            Node node = queue.remove();
            out.add(node.value);
            if (node.left != null) {
                queue.add(node.left);
            }
            if (node.right != null) {
                queue.add(node.right);
            }
        }
        return out;
    }

    /** Longest root-to-leaf path. An empty tree is 0, a single node is 1. */
    public int height() {
        return height(root);
    }

    private int height(Node node) {
        return node == null ? 0 : 1 + Math.max(height(node.left), height(node.right));
    }

    static void check() {
        Check.section("BinarySearchTree");

        BinarySearchTree tree = new BinarySearchTree();
        Check.eq(tree.inOrder().toString(), "[]", "empty tree");
        Check.eq(tree.height(), 0, "empty height");
        Check.isTrue(!tree.contains(1), "empty contains nothing");

        for (int v : new int[] {50, 30, 70, 20, 40, 60, 80}) {
            tree.insert(v);
        }
        Check.eq(tree.size(), 7, "size after inserts");
        Check.eq(tree.inOrder().toString(), "[20, 30, 40, 50, 60, 70, 80]", "in-order is sorted");
        Check.eq(tree.preOrder().toString(), "[50, 30, 20, 40, 70, 60, 80]", "pre-order");
        Check.eq(tree.postOrder().toString(), "[20, 40, 30, 60, 80, 70, 50]", "post-order");
        Check.eq(tree.levelOrder().toString(), "[50, 30, 70, 20, 40, 60, 80]", "level order");
        Check.eq(tree.height(), 3, "height of a balanced 7-node tree");

        tree.insert(50);
        Check.eq(tree.size(), 7, "duplicates are ignored");
        Check.isTrue(tree.contains(60), "contains hit");
        Check.isTrue(!tree.contains(55), "contains miss");

        tree.delete(20);                       // leaf
        Check.eq(tree.inOrder().toString(), "[30, 40, 50, 60, 70, 80]", "delete a leaf");
        tree.delete(30);                       // one child
        Check.eq(tree.inOrder().toString(), "[40, 50, 60, 70, 80]", "delete a node with one child");
        tree.delete(70);                       // two children
        Check.eq(tree.inOrder().toString(), "[40, 50, 60, 80]", "delete a node with two children");
        Check.eq(tree.size(), 4, "size tracks deletions");
        tree.delete(999);
        Check.eq(tree.size(), 4, "deleting an absent value changes nothing");

        // The degenerate case, stated as a measurement rather than a warning.
        BinarySearchTree degenerate = new BinarySearchTree();
        for (int i = 1; i <= 10; i++) {
            degenerate.insert(i);
        }
        Check.eq(degenerate.height(), 10, "sorted input degenerates to a linked list");
        Check.eq(degenerate.inOrder().toString(), "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", "still correct, just slow");
    }
}
