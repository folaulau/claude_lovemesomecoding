"""The Data Structures & Algorithms track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend with
the track and post 25 is the newest.

All 24 pre-existing slugs were published between 2018 and 2019 and are indexed. They are being
rewritten in place, NOT replaced: changing one of those slugs changes a live URL, and three of them
(`binary-search`, `quick-sort`, `recursion`) are linked to from the `fundamental-problem` LeetCode
track. Only `data-structure-algorithm-get-started` is new.

Because the old posts carry 2018/2019 dates and `upsert_post` never overwrites an existing date,
seeding this track needs `seed.py --force-dates` for the reading order to come out right.

The 10:00 stamps are deliberate: `/spring-boot` dates its posts at 09:00 and
`/spring-study-guide` at 14:00, and an exact tie leaves archive order to sort stability.

`source` names the class in `src/dsa/` every Java snippet in that post is copied from.
`check_content.py` verifies the two have not drifted apart.
"""

CATEGORY = {
    "slug": "data-structure-algorithm",
    "name": "Data Structures & Algorithms",
    "description": (
        "Data structures and algorithms in Java 25 — arrays and lists, stacks and queues, hash "
        "tables, trees, heaps, tries and graphs, with recursion, sorting, searching, dynamic "
        "programming and greedy algorithms. Every implementation is a real compiled file with "
        "assertions behind it, not a snippet."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts.
NAV_GROUP = "Software Engineering"

# Java sources under src/dsa/. `tests/run.sh` compiles these with -Werror and runs
# every assertion; the posts quote from them.
SOURCE_DIR = "src/dsa"

VERSIONS = {
    "java": "25",
    "jdk": "Amazon Corretto 25.0.0 (LTS, September 2025)",
    "build": "none — javac and java, no dependencies",
}

POSTS = [
    # ------------------------------------------------------------ foundations
    {
        "slug": "data-structure-algorithm-get-started",
        "title": "Data Structures & Algorithms – Get Started",
        "file": "01-get-started.html",
        "date": "2026-07-01T10:00:00",
        "tags": ["data-structures", "algorithms", "java"],
        "source": None,
        "excerpt": (
            "Start here. What this track covers and in what order, why it is written in Java 25, "
            "and how to run every example yourself with nothing but a JDK — no build tool and no "
            "dependencies. Also the one habit that separates people who can answer these "
            "questions from people who have only read about them."
        ),
    },
    {
        "slug": "data-structure-algorithm-introduction",
        "title": "What a Data Structure Actually Is",
        "file": "02-introduction.html",
        "date": "2026-07-03T10:00:00",
        "tags": ["data-structures", "algorithms", "java"],
        "source": None,
        "excerpt": (
            "A data structure is a decision about how to lay data out in memory, and an algorithm "
            "is a decision about how to walk it. Why there is no best structure, the four "
            "questions that pick one, and the Java collection each choice maps onto."
        ),
    },
    {
        "slug": "data-structure-algorithm-memory",
        "title": "Memory — Why Structures Have Different Speeds",
        "file": "03-memory.html",
        "date": "2026-07-05T10:00:00",
        "tags": ["memory", "data-structures", "java", "cache"],
        "source": None,
        "excerpt": (
            "The stack, the heap, and why an array of a million ints can be faster to scan than a "
            "linked list of a million ints even though both are O(n). Contiguous memory, cache "
            "lines, pointer chasing, and what a Java object reference really costs."
        ),
    },
    {
        "slug": "data-structure-algorithm-big-o-notation",
        "title": "Big O Notation",
        "file": "04-big-o-notation.html",
        "date": "2026-07-07T10:00:00",
        "tags": ["big-o", "complexity", "algorithms"],
        "source": None,
        "excerpt": (
            "How an algorithm's cost grows as the input grows — the only performance question "
            "that survives a change of hardware. The common classes from O(1) to O(2^n), how to "
            "read a complexity off a loop, why constants are dropped, and the difference between "
            "time and space complexity."
        ),
    },
    {
        "slug": "data-structure-algorithm-omega",
        "title": "Omega, Theta and the Rest of the Notation",
        "file": "05-omega.html",
        "date": "2026-07-09T10:00:00",
        "tags": ["big-o", "omega", "theta", "complexity"],
        "source": None,
        "excerpt": (
            "Big O is an upper bound, Omega is a lower bound and Theta is both at once. What each "
            "one actually claims, why saying an algorithm is O(n^2) does not mean it is slow, and "
            "the difference between a bound and a case that people conflate constantly."
        ),
    },
    # ------------------------------------------------------ linear structures
    {
        "slug": "data-structure-algorithm-array",
        "title": "Arrays",
        "file": "06-array.html",
        "date": "2026-07-11T10:00:00",
        "tags": ["array", "data-structures", "java"],
        "source": "DynamicArray",
        # Generic one-liners that illustrate a point rather than quote an implementation.
        # Listed explicitly so check_content.py can stay strict about everything else.
        "illustrative": [
            "int[] values = new int[1000];",
        ],
        "excerpt": (
            "The structure everything else is built on: a fixed-length block of memory where "
            "index arithmetic makes any element reachable in one step. What that buys you, what "
            "it costs on insert and delete, and why the fixed length is the whole problem."
        ),
    },
    {
        "slug": "data-structure-algorithm-arraylist",
        "title": "ArrayList — Building a Growable Array",
        "file": "07-arraylist.html",
        "date": "2026-07-13T10:00:00",
        "tags": ["arraylist", "array", "java", "amortized"],
        "source": "DynamicArray",
        "excerpt": (
            "ArrayList with the lid off — an array, a size, and a resize when it fills up. Why "
            "doubling makes add() amortised O(1) while growing by one makes n adds O(n^2), what "
            "the resize actually costs, and the null that stops a removed element leaking."
        ),
    },
    {
        "slug": "data-structure-algorithm-linked-list",
        "title": "Linked Lists",
        "file": "08-linked-list.html",
        "date": "2026-07-15T10:00:00",
        "tags": ["linked-list", "data-structures", "java"],
        "source": "SinglyLinkedList",
        "excerpt": (
            "Nodes joined by references. O(1) at the front where an array is O(n), O(n) for "
            "random access where an array is O(1) — the trade in both directions. Reversing a "
            "list in one pass, Floyd's cycle detection, and why the tail reference matters."
        ),
    },
    {
        "slug": "data-structure-algorithm-stack",
        "title": "Stacks",
        "file": "09-stack.html",
        "date": "2026-07-17T10:00:00",
        "tags": ["stack", "lifo", "data-structures", "java"],
        "source": "ArrayStack",
                "excerpt": (
            "Last in, first out — everything happens at one end, so everything is O(1). Building "
            "one on an array, the balanced-brackets problem that is the reason interviewers ask "
            "about stacks, why the call stack is one, and why you should never use java.util.Stack."
        ),
    },
    {
        "slug": "data-structure-algorithm-queue",
        "title": "Queues",
        "file": "10-queue.html",
        "date": "2026-07-19T10:00:00",
        "tags": ["queue", "fifo", "circular-buffer", "java"],
        "source": "ArrayQueue",
                "excerpt": (
            "First in, first out. Written as a circular buffer, because the obvious version — "
            "shift everything down on dequeue — is O(n) and is the standard way a hand-rolled "
            "queue goes wrong. Plus the growth bug that only appears after the buffer has wrapped."
        ),
    },
    {
        "slug": "data-structure-algorithm-hashtable",
        "title": "Hash Tables",
        "file": "11-hashtable.html",
        "date": "2026-07-21T10:00:00",
        "tags": ["hashtable", "hashmap", "hashing", "java"],
        "source": "HashTable",
        "excerpt": (
            "Turn the key into an array index and go straight there. Separate chaining, the load "
            "factor, why resizing has to rehash rather than copy, what a bad hashCode does to "
            "your O(1), and the equals/hashCode contract that breaks lookups when you get it wrong."
        ),
    },
    # ------------------------------------------------------------- paradigms
    {
        "slug": "data-structure-algorithm-recursion",
        "title": "Recursion",
        "file": "12-recursion.html",
        "date": "2026-07-23T10:00:00",
        "tags": ["recursion", "algorithms", "java", "stack"],
        "source": "Recursion",
        "excerpt": (
            "A method that calls itself on a smaller version of the same problem. The base case "
            "and the progress towards it, what the call stack is really doing, why "
            "StackOverflowError is a message rather than a mystery, and when a loop is the better "
            "answer."
        ),
    },
    {
        "slug": "data-structure-algorithm-divide-and-conquer",
        "title": "Divide and Conquer",
        "file": "13-divide-and-conquer.html",
        "date": "2026-07-25T10:00:00",
        "tags": ["divide-and-conquer", "algorithms", "recursion"],
        "source": "DivideAndConquer",
        "excerpt": (
            "Split the problem into independent subproblems, solve each, combine. The word doing "
            "the work is independent — that is exactly what separates this from dynamic "
            "programming. Fast exponentiation, and counting inversions for free inside a merge."
        ),
    },
    {
        "slug": "data-structure-algorithm-dynamic-programming",
        "title": "Dynamic Programming",
        "file": "14-dynamic-programming.html",
        "date": "2026-07-27T10:00:00",
        "tags": ["dynamic-programming", "memoization", "algorithms"],
        "source": "DynamicProgramming",
        "excerpt": (
            "Solve each subproblem once and remember the answer. The two conditions that have to "
            "hold, top-down memoisation versus bottom-up tables, and the jump from O(2^n) to O(n) "
            "on Fibonacci. Plus coin change, knapsack, LCS and Kadane's algorithm."
        ),
    },
    {
        "slug": "data-structure-algorithm-greedy-algorithms",
        "title": "Greedy Algorithms",
        "file": "15-greedy-algorithms.html",
        "date": "2026-07-29T10:00:00",
        "tags": ["greedy", "algorithms", "optimization"],
        "source": "Greedy",
        "excerpt": (
            "Take the best-looking option at each step and never reconsider. Fast, simple, and "
            "correct only when the greedy choice property holds — with a worked case where greedy "
            "returns three coins and dynamic programming returns two, so you can see it fail."
        ),
    },
    # --------------------------------------------------- searching & sorting
    {
        "slug": "data-structure-algorithm-binary-search",
        "title": "Binary Search",
        "file": "16-binary-search.html",
        "date": "2026-07-31T10:00:00",
        "tags": ["binary-search", "searching", "algorithms", "java"],
        "source": "Searching",
                "excerpt": (
            "Halve the search space every comparison: O(log n), a billion elements in thirty "
            "steps. Also the three ways it is habitually got wrong — the midpoint overflow that "
            "was in the JDK for nine years, the infinite loop, and the boundary — plus lowerBound, "
            "the variant that is actually useful."
        ),
    },
    {
        "slug": "data-structure-algorithm-merge-sort",
        "title": "Merge Sort",
        "file": "17-merge-sort.html",
        "date": "2026-08-02T10:00:00",
        "tags": ["merge-sort", "sorting", "divide-and-conquer", "java"],
        "source": "Sorting",
        "excerpt": (
            "Split in half, sort each half, merge. O(n log n) in every case and stable, at the "
            "cost of O(n) extra space. Why stability is decided by a single <= in the merge, why "
            "the buffer should be allocated once, and why Java sorts objects this way."
        ),
    },
    {
        "slug": "data-structure-algorithm-quick-sort",
        "title": "Quick Sort",
        "file": "18-quick-sort.html",
        "date": "2026-08-04T10:00:00",
        "tags": ["quick-sort", "sorting", "partition", "java"],
        "source": "Sorting",
        "excerpt": (
            "Partition around a pivot and recurse. Sorts in place and is usually the fastest in "
            "practice, but has an O(n^2) worst case — and the input that triggers it is the "
            "already-sorted array you are most likely to be handed. Median-of-three, and the "
            "recursion trick that caps the stack at O(log n)."
        ),
    },
    # -------------------------------------------------------- trees & heaps
    {
        "slug": "data-structure-algorithm-trees",
        "title": "Trees and Binary Search Trees",
        "file": "19-trees.html",
        "date": "2026-08-06T10:00:00",
        "tags": ["tree", "binary-search-tree", "traversal", "java"],
        "source": "BinarySearchTree",
        "excerpt": (
            "The BST invariant and the O(log n) it buys — but only while the tree stays balanced, "
            "and inserting sorted data makes it a linked list in disguise. All four traversals, "
            "why in-order comes out sorted, and deletion with two children, the case everyone skips."
        ),
    },
    {
        "slug": "data-structure-algorithm-heap",
        "title": "Heaps",
        "file": "20-heap.html",
        "date": "2026-08-08T10:00:00",
        "tags": ["heap", "binary-heap", "heapify", "java"],
        "source": "MinHeap",
        "excerpt": (
            "A tree stored in a flat array with no references at all, kept ordered just enough "
            "that the minimum is always at index 0. Sift up, sift down, and why building a heap "
            "from an array is O(n) rather than O(n log n) — a genuinely counter-intuitive result."
        ),
    },
    {
        "slug": "data-structure-algorithm-priority-queue",
        "title": "Priority Queues",
        "file": "21-priority-queue.html",
        "date": "2026-08-10T10:00:00",
        "tags": ["priority-queue", "heap", "java"],
        "source": "MinHeap",
        "excerpt": (
            "A queue that serves by priority rather than by arrival. What Java's PriorityQueue is "
            "underneath, the comparator that decides min-heap or max-heap, the k-largest pattern "
            "that beats sorting, and the iteration order that is not sorted and surprises everyone."
        ),
    },
    {
        "slug": "data-structure-algorithm-trie",
        "title": "Tries",
        "file": "22-trie.html",
        "date": "2026-08-12T10:00:00",
        "tags": ["trie", "prefix-tree", "autocomplete", "java"],
        "source": "Trie",
        "excerpt": (
            "A prefix tree: one node per character, words spelled out along the paths. Why it is "
            "the wrong choice for exact lookup — a HashSet is simpler and faster — and the right "
            "one for autocomplete and every other prefix question a set cannot answer."
        ),
    },
    # -------------------------------------------------------------- graphs
    {
        "slug": "data-structure-algorithm-graph",
        "title": "Graphs",
        "file": "23-graph.html",
        "date": "2026-08-14T10:00:00",
        "tags": ["graph", "adjacency-list", "data-structures", "java"],
        "source": "Graph",
        "excerpt": (
            "Vertices and edges — the structure behind social networks, maps, dependencies and "
            "package managers. Directed against undirected, weighted against unweighted, and why "
            "an adjacency list beats an adjacency matrix on almost every real graph."
        ),
    },
    {
        "slug": "data-structure-algorithm-breadth-first-search",
        "title": "Breadth-First Search",
        "file": "24-breadth-first-search.html",
        "date": "2026-08-16T10:00:00",
        "tags": ["bfs", "graph", "queue", "shortest-path"],
        "source": "Graph",
        "excerpt": (
            "Explore level by level using a queue — and get the shortest path in an unweighted "
            "graph for free, which no other traversal does. Reconstructing the path, why you mark "
            "visited on enqueue rather than dequeue, and where BFS stops being the right tool."
        ),
    },
    {
        "slug": "data-structure-algorithm-depth-first-search",
        "title": "Depth-First Search",
        "file": "25-depth-first-search.html",
        "date": "2026-08-18T10:00:00",
        "tags": ["dfs", "graph", "stack", "recursion"],
        "source": "Graph",
        "excerpt": (
            "Follow one path to its end, then back up and try the next. The same code as BFS with "
            "the queue swapped for a stack — the traversal strategy IS the container. Recursive "
            "and iterative forms, cycle detection, and how to choose between DFS and BFS."
        ),
    },
]
