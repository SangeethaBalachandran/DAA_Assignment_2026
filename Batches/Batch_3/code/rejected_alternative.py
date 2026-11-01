def greedy_join_order(p):

    n = len(p) - 1

    # Initially, every relation is a separate group
    groups = [(i, i) for i in range(n)]

    total_cost = 0

    # Continue until only one group remains
    while len(groups) > 1:

        best_cost = float("inf")
        best_index = -1

        # Find the cheapest adjacent pair
        for i in range(len(groups) - 1):

            left = groups[i]
            right = groups[i + 1]

            cost = (
                p[left[0]]
                * p[left[1] + 1]
                * p[right[1] + 1]
            )

            if cost < best_cost:
                best_cost = cost
                best_index = i

        # Merge the selected adjacent pair
        left = groups[best_index]
        right = groups[best_index + 1]

        total_cost += best_cost

        merged = (left[0], right[1])

        groups[best_index:best_index + 2] = [merged]

    return total_cost


if __name__ == "__main__":

    p = [40, 20, 30, 10, 30, 15]

    result = greedy_join_order(p)

    print("Greedy Join Cost:", result)
