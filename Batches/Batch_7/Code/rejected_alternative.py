r"""Rejected techniques, kept for comparison.
 1. DYNAMIC PROGRAMMING over subsets (exact, O(3^n)):  f[S] = 1 + min f[S \ I] over independent I in S.
 2. GREEDY (Welsh-Powell: descending degree, lowest free slot) - fast but not exact (see trap)."""
from generate_inputs import greedy_trap, instance7, COURSES

def chromatic_dp(adj):
    n = len(adj)
    nb = [sum(1 << u for u in adj[v]) for v in range(n)]
    N = 1 << n
    indep = [True] * N
    for S in range(1, N):
        low = (S & -S).bit_length() - 1
        indep[S] = indep[S & (S - 1)] and not (nb[low] & S)
    f = [0] * N
    for S in range(1, N):
        low = S & -S
        rest = S ^ low
        best = n
        sub = rest
        while True:                      # all submasks of rest, each joined with 'low'
            I = sub | low
            if indep[I]:
                c = f[S ^ I] + 1
                if c < best: best = c
            if sub == 0: break
            sub = (sub - 1) & rest
        f[S] = best
    return f[N - 1]

def welsh_powell(adj):
    n = len(adj)
    order = sorted(range(n), key=lambda v: (-len(adj[v]), v))
    col = {}
    for v in order:
        used = {col[u] for u in adj[v] if u in col}
        c = 1
        while c in used: c += 1
        col[v] = c
    return col

if __name__ == "__main__":
    print("DP chromatic number of instance:", chromatic_dp(instance7()))
    names, g = greedy_trap()
    col = welsh_powell(g)
    print("greedy trap -> slots used:", max(col.values()), {names[v]: c for v, c in sorted(col.items())})
    print("DP (optimal) on the same graph:", chromatic_dp(g))
