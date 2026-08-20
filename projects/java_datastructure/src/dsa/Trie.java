package dsa;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * A trie (prefix tree): one node per character, words spelled out along the paths.
 *
 * <p>Lookup is O(m) in the length of the WORD, with no dependence on how many words the trie
 * holds. A HashSet is also roughly O(m) - it has to hash the string, which reads every character.
 * So a trie is not the answer to "does this word exist"; a HashSet is simpler and faster there.
 *
 * <p>The trie earns its place on <b>prefix</b> questions: every word starting with "car",
 * autocomplete, longest common prefix. A HashSet cannot answer those without scanning everything.
 * Choosing a trie for exact lookup is the classic case of picking the clever structure over the
 * right one.
 */
public class Trie {

    private static final class Node {
        // A HashMap, not a 26-slot array. The array version is faster and is what interview
        // answers usually show, but it silently assumes lowercase ASCII - it breaks on digits,
        // apostrophes and every non-English alphabet.
        final Map<Character, Node> children = new HashMap<>();
        boolean endOfWord;
    }

    private final Node root = new Node();
    private int size;

    public int size() {
        return size;
    }

    /** O(m) in the length of the word. */
    public void insert(String word) {
        Node node = root;
        for (char c : word.toCharArray()) {
            node = node.children.computeIfAbsent(c, k -> new Node());
        }
        if (!node.endOfWord) {
            node.endOfWord = true;
            size++;
        }
    }

    /**
     * Note this is NOT the same question as startsWith. "car" can be a path through the trie
     * without being a word - if only "cargo" was inserted. The endOfWord flag is what
     * distinguishes them, and leaving it out is the standard trie bug.
     */
    public boolean contains(String word) {
        Node node = find(word);
        return node != null && node.endOfWord;
    }

    public boolean startsWith(String prefix) {
        return find(prefix) != null;
    }

    private Node find(String s) {
        Node node = root;
        for (char c : s.toCharArray()) {
            node = node.children.get(c);
            if (node == null) {
                return null;
            }
        }
        return node;
    }

    /** Autocomplete: every word under a prefix. This is what a trie is actually for. */
    public List<String> wordsWithPrefix(String prefix) {
        List<String> out = new ArrayList<>();
        Node start = find(prefix);
        if (start != null) {
            collect(start, new StringBuilder(prefix), out);
        }
        out.sort(String::compareTo);   // deterministic, since HashMap iteration order is not
        return out;
    }

    private void collect(Node node, StringBuilder path, List<String> out) {
        if (node.endOfWord) {
            out.add(path.toString());
        }
        for (Map.Entry<Character, Node> e : node.children.entrySet()) {
            path.append(e.getKey());
            collect(e.getValue(), path, out);
            path.deleteCharAt(path.length() - 1);   // backtrack, or the paths concatenate
        }
    }

    static void check() {
        Check.section("Trie");

        Trie trie = new Trie();
        Check.isTrue(!trie.contains("anything"), "empty trie contains nothing");
        Check.isTrue(!trie.startsWith("a"), "empty trie has no prefixes");

        for (String w : new String[] {"car", "cargo", "care", "dog", "do"}) {
            trie.insert(w);
        }
        Check.eq(trie.size(), 5, "size counts words");

        Check.isTrue(trie.contains("car"), "exact word");
        Check.isTrue(trie.contains("do"), "a word that is a prefix of another");
        Check.isTrue(!trie.contains("ca"), "a prefix that was never inserted is not a word");
        Check.isTrue(trie.startsWith("ca"), "but it IS a prefix");
        Check.isTrue(!trie.startsWith("z"), "absent prefix");

        Check.eq(trie.wordsWithPrefix("car").toString(), "[car, care, cargo]", "autocomplete");
        Check.eq(trie.wordsWithPrefix("do").toString(), "[do, dog]", "prefix that is also a word");
        Check.eq(trie.wordsWithPrefix("").toString(), "[car, care, cargo, do, dog]", "empty prefix is everything");
        Check.eq(trie.wordsWithPrefix("zzz").toString(), "[]", "no matches");

        trie.insert("car");
        Check.eq(trie.size(), 5, "inserting a duplicate does not grow it");

        // Non-alphabetic characters - the case a 26-slot array cannot represent.
        Trie mixed = new Trie();
        mixed.insert("a1");
        mixed.insert("don't");
        Check.isTrue(mixed.contains("a1"), "digits work");
        Check.isTrue(mixed.contains("don't"), "punctuation works");
    }
}
