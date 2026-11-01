"""
Rejected alternative for this special case: O(n^2) dynamic programming.
dp[i] = minimum number of charging stops needed to reach charger i.
The source (position 0) has cost 0; destination is treated as the final node.
"""
def dp_min_stops(chargers, destination, range_km):
    points = [0] + sorted(chargers) + [destination]
    n = len(points)
    inf = 10**9
    dp = [inf] * n
    parent = [-1] * n
    dp[0] = 0
    for j in range(1, n):
        for i in range(j):
            if points[j] - points[i] <= range_km and dp[i] + (0 if j == n-1 else 1) < dp[j]:
                dp[j] = dp[i] + (0 if j == n-1 else 1)
                parent[j] = i
    if dp[-1] == inf:
        return None
    path = []
    cur = n - 1
    while parent[cur] != -1:
        cur = parent[cur]
        if cur != 0:
            path.append(points[cur])
    return list(reversed(path))

if __name__ == "__main__":
    print(dp_min_stops([40,95,130,180,210,260,300,330], 350, 120))
