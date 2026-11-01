def count_inversions_brute(arr):
    """Count all inversions by checking every pair: O(n^2) time."""
    count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                count += 1
    return count


def count_weighted_inversions_brute(rankings, top_k=10):
    """
    Brute-force reference for the weighted rule:
    weight 5 if either title is in the top-k of Engine A or Engine B;
    otherwise weight 1.
    """
    score = 0
    for i in range(len(rankings)):
        for j in range(i + 1, len(rankings)):
            if rankings[i] > rankings[j]:
                i_is_top = (i < top_k or rankings[i] <= top_k)
                j_is_top = (j < top_k or rankings[j] <= top_k)
                score += 5 if (i_is_top or j_is_top) else 1
    return score


if __name__ == "__main__":
    example = [3, 1, 6, 2, 8, 4, 7, 5]
    print("Disagreement score:", count_inversions_brute(example))
    print("Weighted disagreement score:",
          count_weighted_inversions_brute(example, top_k=10))
