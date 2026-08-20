package dsa;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * A graph as an adjacency list - a map from each vertex to its neighbours.
 *
 * <p><b>Adjacency list vs adjacency matrix.</b> A matrix is a V x V grid: O(1) to ask "is there an
 * edge a-b", but O(V^2) memory whether or not the edges exist. A list is O(V + E) memory and O(1)
 * to iterate a vertex's neighbours, which is what traversal actually does. Real graphs are sparse
 * - a social network has millions of users and nowhere near millions of friends each - so the
 * list wins almost always.
 */
public class Graph {

    private final Map<String, Set<String>> adjacency = new HashMap<>();
    private final boolean directed;

    public Graph() {
        this(false);
    }

    public Graph(boolean directed) {
        this.directed = directed;
    }

    public void addVertex(String v) {
        adjacency.computeIfAbsent(v, k -> new LinkedHashSet<>());
    }

    /** LinkedHashSet, so traversal order is insertion order and the tests are deterministic. */
    public void addEdge(String a, String b) {
        addVertex(a);
        addVertex(b);
        adjacency.get(a).add(b);
        if (!directed) {
            adjacency.get(b).add(a);
        }
    }

    public Set<String> neighbours(String v) {
        return adjacency.getOrDefault(v, Set.of());
    }

    public int vertexCount() {
        return adjacency.size();
    }

    /**
     * Breadth-first search: a QUEUE, level by level.
     *
     * <p>Visits everything one step away, then everything two steps away, and so on. That is what
     * makes it - and only it - find the shortest path in an unweighted graph.
     *
     * <p>Mark visited when ENQUEUEING, not when dequeuing. Marking on dequeue lets a vertex be
     * queued several times before it is first processed, which on a dense graph is an exponential
     * blow-up rather than a slight inefficiency.
     */
    public List<String> breadthFirst(String start) {
        List<String> order = new ArrayList<>();
        if (!adjacency.containsKey(start)) {
            return order;
        }
        Set<String> visited = new HashSet<>();
        Deque<String> queue = new ArrayDeque<>();

        visited.add(start);
        queue.add(start);

        while (!queue.isEmpty()) {
            String current = queue.remove();
            order.add(current);
            for (String next : neighbours(current)) {
                if (visited.add(next)) {   // add() returns false if it was already there
                    queue.add(next);
                }
            }
        }
        return order;
    }

    /**
     * Depth-first search: a STACK, following one path to its end before backtracking.
     *
     * <p>Same code as BFS with the queue swapped for a stack - which is the point worth making.
     * The traversal strategy IS the choice of container.
     */
    public List<String> depthFirst(String start) {
        List<String> order = new ArrayList<>();
        if (!adjacency.containsKey(start)) {
            return order;
        }
        Set<String> visited = new HashSet<>();
        Deque<String> stack = new ArrayDeque<>();
        stack.push(start);

        while (!stack.isEmpty()) {
            String current = stack.pop();
            // Checked on POP here, not on push: a vertex can be pushed by several neighbours
            // before it is ever popped, so the pop is the only place it is certainly first.
            if (!visited.add(current)) {
                continue;
            }
            order.add(current);
            List<String> next = new ArrayList<>(neighbours(current));
            // Reversed so the first neighbour is explored first, matching the recursive version.
            for (int i = next.size() - 1; i >= 0; i--) {
                if (!visited.contains(next.get(i))) {
                    stack.push(next.get(i));
                }
            }
        }
        return order;
    }

    /** The recursive DFS, for comparison. The call stack replaces the explicit one. */
    public List<String> depthFirstRecursive(String start) {
        List<String> order = new ArrayList<>();
        if (adjacency.containsKey(start)) {
            depthFirstRecursive(start, new HashSet<>(), order);
        }
        return order;
    }

    private void depthFirstRecursive(String current, Set<String> visited, List<String> order) {
        if (!visited.add(current)) {
            return;
        }
        order.add(current);
        for (String next : neighbours(current)) {
            depthFirstRecursive(next, visited, order);
        }
    }

    /**
     * Shortest path in an UNWEIGHTED graph, via BFS.
     *
     * <p>Weighted graphs need Dijkstra instead - BFS assumes every edge costs the same, and on a
     * weighted graph it confidently returns the path with the fewest hops rather than the cheapest.
     */
    public List<String> shortestPath(String from, String to) {
        if (!adjacency.containsKey(from) || !adjacency.containsKey(to)) {
            return List.of();
        }
        Map<String, String> cameFrom = new HashMap<>();
        Set<String> visited = new HashSet<>();
        Deque<String> queue = new ArrayDeque<>();
        visited.add(from);
        queue.add(from);

        while (!queue.isEmpty()) {
            String current = queue.remove();
            if (current.equals(to)) {
                List<String> path = new ArrayList<>();
                for (String at = to; at != null; at = cameFrom.get(at)) {
                    path.add(at);
                }
                java.util.Collections.reverse(path);
                return path;
            }
            for (String next : neighbours(current)) {
                if (visited.add(next)) {
                    cameFrom.put(next, current);
                    queue.add(next);
                }
            }
        }
        return List.of();   // unreachable
    }

    /** Whether a path exists at all - the connectivity question. */
    public boolean connected(String from, String to) {
        return !shortestPath(from, to).isEmpty();
    }

    static void check() {
        Check.section("Graph");

        //   a - b - d
        //   |   |
        //   c   e     and an isolated f
        Graph g = new Graph();
        g.addEdge("a", "b");
        g.addEdge("a", "c");
        g.addEdge("b", "d");
        g.addEdge("b", "e");
        g.addVertex("f");

        Check.eq(g.vertexCount(), 6, "vertex count");
        Check.eq(g.breadthFirst("a").toString(), "[a, b, c, d, e]", "BFS visits by level");
        Check.eq(g.depthFirst("a").toString(), "[a, b, d, e, c]", "DFS follows one path down");
        Check.eq(g.depthFirstRecursive("a").toString(), "[a, b, d, e, c]", "recursive DFS agrees");
        Check.eq(g.breadthFirst("nope").toString(), "[]", "traversing from an absent vertex");
        Check.eq(g.breadthFirst("f").toString(), "[f]", "isolated vertex");

        Check.eq(g.shortestPath("a", "e").toString(), "[a, b, e]", "shortest path");
        Check.eq(g.shortestPath("a", "a").toString(), "[a]", "path to self");
        Check.eq(g.shortestPath("a", "f").toString(), "[]", "no path to an isolated vertex");
        Check.isTrue(g.connected("c", "d"), "connected across the graph");
        Check.isTrue(!g.connected("a", "f"), "not connected");

        // Undirected edges go both ways; directed ones do not.
        Check.isTrue(g.neighbours("b").contains("a"), "undirected edge is symmetric");
        Graph directed = new Graph(true);
        directed.addEdge("x", "y");
        Check.isTrue(directed.neighbours("x").contains("y"), "directed edge forwards");
        Check.isTrue(!directed.neighbours("y").contains("x"), "but not backwards");

        // A cycle must not loop forever - that is what the visited set is for.
        Graph cyclic = new Graph();
        cyclic.addEdge("p", "q");
        cyclic.addEdge("q", "r");
        cyclic.addEdge("r", "p");
        Check.eq(cyclic.breadthFirst("p").toString(), "[p, q, r]", "BFS terminates on a cycle");
        Check.eq(cyclic.depthFirst("p").toString(), "[p, q, r]", "DFS terminates on a cycle");
    }
}
