package dsa;

import java.util.ArrayList;
import java.util.List;

/**
 * A hash table with separate chaining - what HashMap is, simplified.
 *
 * <p>The idea in one line: turn the key into an array index, and go straight there. That is what
 * makes lookup O(1) on average rather than the O(n) of scanning a list.
 *
 * <p><b>Average</b> is doing real work in that sentence. Two keys can hash to the same bucket, and
 * then you are scanning a chain. With a good hash and a bounded load factor the chains stay
 * roughly one element long; with a terrible hash - {@code return 0;} is a legal hashCode - every
 * key lands in one bucket and the table degrades to a linked list at O(n).
 */
public class HashTable<K, V> {

    private static final double MAX_LOAD_FACTOR = 0.75;

    private static final class Entry<K, V> {
        final K key;
        V value;
        Entry<K, V> next;

        Entry(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }

    private Entry<K, V>[] buckets;
    private int size;

    public HashTable() {
        this(16);
    }

    // Java cannot create a generic array; every hash map implementation, including the JDK's,
    // suppresses this pair of warnings in exactly this way.
    @SuppressWarnings({"unchecked", "rawtypes"})
    public HashTable(int capacity) {
        this.buckets = new Entry[Math.max(1, capacity)];
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    /** Visible so the post can show the load factor doing its job. */
    public int bucketCount() {
        return buckets.length;
    }

    /**
     * Math.floorMod, not %.
     *
     * <p>A hashCode can be negative, and Java's % keeps the sign - so {@code -7 % 16} is -7, and
     * that is an ArrayIndexOutOfBoundsException. It is a real bug in a lot of hand-written hash
     * tables, and it only shows up for keys that happen to hash negative.
     */
    private int bucketFor(Object key, int length) {
        return key == null ? 0 : Math.floorMod(key.hashCode(), length);
    }

    public V put(K key, V value) {
        int index = bucketFor(key, buckets.length);
        for (Entry<K, V> e = buckets[index]; e != null; e = e.next) {
            if (equal(e.key, key)) {
                V previous = e.value;
                e.value = value; // a Map replaces, it does not duplicate
                return previous;
            }
        }
        Entry<K, V> head = new Entry<>(key, value);
        head.next = buckets[index];
        buckets[index] = head;
        size++;

        if ((double) size / buckets.length > MAX_LOAD_FACTOR) {
            resize();
        }
        return null;
    }

    public V get(K key) {
        int index = bucketFor(key, buckets.length);
        for (Entry<K, V> e = buckets[index]; e != null; e = e.next) {
            if (equal(e.key, key)) {
                return e.value;
            }
        }
        return null;
    }

    public boolean containsKey(K key) {
        int index = bucketFor(key, buckets.length);
        for (Entry<K, V> e = buckets[index]; e != null; e = e.next) {
            if (equal(e.key, key)) {
                return true;
            }
        }
        return false;
    }

    public V remove(K key) {
        int index = bucketFor(key, buckets.length);
        Entry<K, V> previous = null;
        for (Entry<K, V> e = buckets[index]; e != null; previous = e, e = e.next) {
            if (equal(e.key, key)) {
                if (previous == null) {
                    buckets[index] = e.next;
                } else {
                    previous.next = e.next;
                }
                size--;
                return e.value;
            }
        }
        return null;
    }

    public List<K> keys() {
        List<K> out = new ArrayList<>(size);
        for (Entry<K, V> bucket : buckets) {
            for (Entry<K, V> e = bucket; e != null; e = e.next) {
                out.add(e.key);
            }
        }
        return out;
    }

    /**
     * Every key has to be REHASHED, not merely moved: the bucket index depends on the table
     * length, so the same key belongs somewhere else in a bigger table. Copying buckets across
     * verbatim is a silent corruption - get() then looks in the right place and finds nothing.
     */
    @SuppressWarnings({"unchecked", "rawtypes"})
    private void resize() {
        Entry<K, V>[] old = buckets;
        Entry<K, V>[] bigger = new Entry[old.length * 2];
        for (Entry<K, V> bucket : old) {
            for (Entry<K, V> e = bucket; e != null; ) {
                Entry<K, V> next = e.next;
                int index = bucketFor(e.key, bigger.length);
                e.next = bigger[index];
                bigger[index] = e;
                e = next;
            }
        }
        buckets = bigger;
    }

    private static boolean equal(Object a, Object b) {
        return a == null ? b == null : a.equals(b);
    }

    static void check() {
        Check.section("HashTable");

        HashTable<String, Integer> map = new HashTable<>(4);
        Check.isTrue(map.isEmpty(), "starts empty");
        Check.eq(map.get("missing"), null, "get on a missing key is null");

        Check.eq(map.put("a", 1), null, "put returns null for a new key");
        map.put("b", 2);
        Check.eq(map.put("a", 10), 1, "put returns the previous value");
        Check.eq(map.get("a"), 10, "put replaces, does not duplicate");
        Check.eq(map.size(), 2, "size counts keys, not puts");

        Check.isTrue(map.containsKey("b"), "containsKey hit");
        Check.isTrue(!map.containsKey("z"), "containsKey miss");
        Check.eq(map.remove("b"), 2, "remove returns the value");
        Check.eq(map.remove("b"), null, "removing twice is null");
        Check.eq(map.size(), 1, "size after remove");

        // A negative hashCode - the floorMod case. "polygenelubricants" is the classic
        // String whose hashCode is Integer.MIN_VALUE.
        HashTable<Integer, String> negatives = new HashTable<>(8);
        negatives.put(-7, "neg");
        Check.eq(negatives.get(-7), "neg", "negative hashCode does not blow up");

        // Grow past the load factor and prove nothing was lost in the rehash.
        HashTable<Integer, Integer> big = new HashTable<>(2);
        for (int i = 0; i < 200; i++) {
            big.put(i, i * i);
        }
        Check.eq(big.size(), 200, "all keys present after resizing");
        Check.isTrue(big.bucketCount() > 2, "table actually grew");
        boolean allFound = true;
        for (int i = 0; i < 200; i++) {
            if (big.get(i) == null || big.get(i) != i * i) {
                allFound = false;
            }
        }
        Check.isTrue(allFound, "every key still resolves after rehashing");
        Check.eq(big.keys().size(), 200, "keys() sees them all");
    }
}
