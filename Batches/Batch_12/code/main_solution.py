def count_inversions(arr):
    """Return (sorted_array, inversion_count) using merge-sort counting."""
    if len(arr) <= 1:
        return arr[:], 0

    mid = len(arr) // 2
    left, left_count = count_inversions(arr[:mid])
    right, right_count = count_inversions(arr[mid:])

    merged = []
    i = j = 0
    cross_count = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            cross_count += len(left) - i
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, left_count + right_count + cross_count


def count_weighted_inversions(rankings, top_k=10):
    """
    Return (ordinary_inversions, weighted_score).

    rankings[j] is the Engine A position of the title at Engine B position j.
    A title is considered top-k if it is in Engine A's top-k OR Engine B's
    top-k. Each inversion involving at least one such title has weight 5;
    every other inversion has weight 1.

    The weighted score is computed in O(n log n) using merge sort and
    suffix counts of top-k-marked elements.
    """
    items = [(value, (index < top_k or value <= top_k))
             for index, value in enumerate(rankings)]

    def sort_count(values):
        if len(values) <= 1:
            return values[:], 0, 0

        mid = len(values) // 2
        left, left_inv, left_weight = sort_count(values[:mid])
        right, right_inv, right_weight = sort_count(values[mid:])

        # suffix_top[i] = number of top-k items in left[i:]
        suffix_top = [0] * (len(left) + 1)
        for i in range(len(left) - 1, -1, -1):
            suffix_top[i] = suffix_top[i + 1] + int(left[i][1])

        merged = []
        i = j = 0
        cross_inv = 0
        cross_weight = 0

        while i < len(left) and j < len(right):
            if left[i][0] <= right[j][0]:
                merged.append(left[i])
                i += 1
            else:
                # right[j] is smaller than every remaining left element.
                remaining = len(left) - i
                top_pairs = remaining if right[j][1] else suffix_top[i]
                cross_inv += remaining
                cross_weight += remaining + 4 * top_pairs
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return (merged, left_inv + right_inv + cross_inv,
                left_weight + right_weight + cross_weight)

    _, inversions, weighted_score = sort_count(items)
    return inversions, weighted_score


if __name__ == "__main__":
    example = [3, 1, 6, 2, 8, 4, 7, 5]
    sorted_array, score = count_inversions(example)
    inversions, weighted = count_weighted_inversions(example, top_k=10)

    print("Original ranking:", example)
    print("Sorted ranking:", sorted_array)
    print("Disagreement score:", score)
    print("Weighted disagreement score:", weighted)
