def matrix_chain_order(p):
    n = len(p) - 1

    # Create DP cost table and split table
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    # Calculate minimum cost for increasing subchain lengths
    for length in range(2, n + 1):

        for i in range(n - length + 1):

            j = i + length - 1
            cost[i][j] = float("inf")

            # Try every possible splitting position
            for k in range(i, j):

                current_cost = (
                    cost[i][k]
                    + cost[k + 1][j]
                    + p[i] * p[k + 1] * p[j + 1]
                )

                if current_cost < cost[i][j]:
                    cost[i][j] = current_cost
                    split[i][j] = k

    return cost[0][n - 1], split, cost


# Reconstruct the optimal join order
def get_order(split, i, j):

    if i == j:
        return f"R{i + 1}"

    k = split[i][j]

    left = get_order(split, i, k)
    right = get_order(split, k + 1, j)

    return f"({left} JOIN {right})"


# Main program
if __name__ == "__main__":

    # Given input
    p = [40, 20, 30, 10, 30, 15]

    # Execute Dynamic Programming algorithm
    minimum_cost, split, dp = matrix_chain_order(p)

    # Display minimum cost
    print("Minimum Join Cost:", minimum_cost)

    # Display optimal join order
    print("Optimal Join Order:",
          get_order(split, 0, len(p) - 2))

    # Display DP cost table
    print("\nDP Cost Table:")

    for row in dp:
        print(row)
