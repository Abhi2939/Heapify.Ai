# Heap Sort: Study Notes (MIT 6.006 Fall 2011, Lecture 4)

These notes summarise Lecture 4 (Heaps and Heap Sort). Like the lecture, they use 1-indexed arrays: the root is A[1].

## Priority queue

A priority queue is a data structure that maintains a set S of elements, each associated with a key. A max-priority queue supports these operations:

- insert(S, x): insert element x into set S.
- max(S): return the element of S with the largest key.
- extract_max(S): return the element of S with the largest key and remove it from S.
- increase_key(S, x, k): increase the value of element x's key to the new value k (k must be at least the current key).

A min-priority queue is defined analogously, using the smallest key. A heap is one way to implement a priority queue.

## Heap

A heap is an array visualized as a nearly complete binary tree. The root of the tree is the first element, A[1]. For a node at index i:

- parent(i) = floor(i/2)
- left(i) = 2i
- right(i) = 2i + 1

Max-heap property: the key of a node is greater than or equal to the keys of its children, so A[parent(i)] >= A[i]. The min-heap property is defined analogously. A heap with n nodes has height floor(log2 n), which is Theta(lg n). The leaves are the nodes with indices floor(n/2)+1 through n. (If an implementation uses 0-indexed arrays, then parent(i) = (i-1)//2, left(i) = 2i+1 and right(i) = 2i+2.)

## max_heapify

max_heapify(A, i) fixes a single violation of the max-heap property at node i. It assumes the binary trees rooted at left(i) and right(i) are already max-heaps, but A[i] might be smaller than its children.

Steps: find the largest of A[i], A[left(i)] and A[right(i)]. If the largest is not A[i], swap A[i] with that child and call max_heapify on the child's index, because the swap may have broken the heap property one level down. Stop when the node is at least as large as both children or is a leaf.

Running time: the element can move down at most the height of the heap, so max_heapify takes O(lg n) time.

## build_max_heap

build_max_heap produces a max-heap from an arbitrary, unordered array. Steps: for i from floor(n/2) down to 1, call max_heapify(A, i).

Why start at floor(n/2): the nodes after that index are leaves, and a leaf is already a max-heap by itself. Going from the bottom up guarantees that when max_heapify runs on node i, both of its subtrees are already max-heaps.

Running time: build_max_heap takes O(n), not O(n lg n). A node at height h costs only O(h) to heapify, and there are at most ceil(n / 2^(h+1)) nodes at height h. Summing h * n / 2^h over all heights gives O(n). The simple bound of n calls times O(lg n) per call is correct but not tight.

## Heap sort algorithm

Sorting strategy:

1. Build a max-heap from the unordered array.
2. The maximum element is at A[1].
3. Swap A[1] with A[n]. The maximum element is now at its final position at the end of the array.
4. Discard node n from the heap by decreasing the heap size by one.
5. The new root may violate the max-heap property, but its children are still max-heaps. Run max_heapify on the root to fix it.
6. Repeat from step 2 until the heap is empty. The array is then sorted in increasing order.

Running time: build_max_heap takes O(n). Then there are n - 1 iterations, each doing one swap and one max_heapify at O(lg n). The total is O(n lg n) in the worst case.

## Properties of heap sort

- In place: yes. Heap sort rearranges elements inside the input array using only swaps and O(1) extra memory. Merge sort, by contrast, needs O(n) extra space.
- Time: O(n lg n) worst case.
- Stable: no. Elements with equal keys can change their relative order. Example: sort [2a, 2b, 1], where 2a and 2b are equal keys. The heap built from it is [2a, 2b, 1], and after the heap sort steps the result is [1, 2b, 2a], so 2a and 2b have swapped places.
- Comparison-based: heap sort only compares keys with each other.

## Quick answers

What is a heap? An array viewed as a nearly complete binary tree that satisfies the max-heap property (or the min-heap property), commonly used to implement a priority queue.

How do I find the parent and children of index i? With 1-indexed arrays, parent(i) = floor(i/2), left(i) = 2i, right(i) = 2i + 1.

What is the time complexity of heap sort? O(n lg n) in the worst case: O(n) to build the heap, then n - 1 extractions of O(lg n) each.

Is heap sort in place? Yes. It sorts within the input array with O(1) extra space.

Is heap sort stable? No. Equal keys may be reordered.

Why is build_max_heap O(n) and not O(n lg n)? Most nodes are near the bottom of the tree and need very little work in max_heapify, so the total work sums to O(n).

What operations does a priority queue support? insert, max, extract_max and increase_key.