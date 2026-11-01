#!/usr/bin/env python3
"""Affine gap costs (Question 5): three tables per cell.

Convention: a gap of length k costs OPEN + (k-1)*EXT  (first gap base costs 3, each further
base costs 1).  If your instructor means "3 + k", call affine_align(..., open_=4).

  M[i][j] best cost with the last column a match/substitution
  X[i][j] best cost with the last column a deletion (consumes a reference base)
  Y[i][j] best cost with the last column an insertion (consumes a read base)

Usage: python3 affine_gap.py REFERENCE READ
"""
import sys

INF = 10 ** 9


def affine_tables(ref, read, sub=1, open_=3, ext=1):
    m, n = len(ref), len(read)
    M = [[INF] * (n + 1) for _ in range(m + 1)]
    X = [[INF] * (n + 1) for _ in range(m + 1)]
    Y = [[INF] * (n + 1) for _ in range(m + 1)]
    M[0][0] = 0
    for i in range(m + 1):
        for j in range(n + 1):
            if i >= 1 and j >= 1:
                s = 0 if ref[i - 1] == read[j - 1] else sub
                M[i][j] = s + min(M[i - 1][j - 1], X[i - 1][j - 1], Y[i - 1][j - 1])
            if i >= 1:
                X[i][j] = min(M[i - 1][j] + open_, X[i - 1][j] + ext, Y[i - 1][j] + open_)
            if j >= 1:
                Y[i][j] = min(M[i][j - 1] + open_, Y[i][j - 1] + ext, X[i][j - 1] + open_)
    return M, X, Y


def affine_align(ref, read, sub=1, open_=3, ext=1):
    M, X, Y = affine_tables(ref, read, sub, open_, ext)
    i, j = len(ref), len(read)
    cands = [(M[i][j], "M"), (X[i][j], "X"), (Y[i][j], "Y")]
    cost, state = min(cands, key=lambda t: t[0])
    ops = []
    while i > 0 or j > 0:
        if state == "M":
            s = 0 if ref[i - 1] == read[j - 1] else sub
            ops.append(("M" if s == 0 else "S", ref[i - 1], read[j - 1]))
            target = M[i][j] - s
            i, j = i - 1, j - 1
            state = "M" if M[i][j] == target else ("X" if X[i][j] == target else "Y")
        elif state == "X":
            ops.append(("D", ref[i - 1], "-"))
            v = X[i][j]
            pi = i - 1
            if M[pi][j] + open_ == v:
                state = "M"
            elif X[pi][j] + ext == v:
                state = "X"
            else:
                state = "Y"
            i = pi
        else:
            ops.append(("I", "-", read[j - 1]))
            v = Y[i][j]
            pj = j - 1
            if M[i][pj] + open_ == v:
                state = "M"
            elif Y[i][pj] + ext == v:
                state = "Y"
            else:
                state = "X"
            j = pj
    ops.reverse()
    return cost, ops


def affine_cost_of(ops, sub=1, open_=3, ext=1):
    c, prev = 0, None
    for o, _, _ in ops:
        if o == "S":
            c += sub
        elif o in "DI":
            c += ext if prev == o else open_
        prev = o
    return c


def show(T, name, ref, read):
    print(name)
    print("      -  " + "  ".join(" " + c for c in read))
    for i, row in enumerate(T):
        print(("-" if i == 0 else ref[i - 1]) + "  " + " ".join("  ." if x >= INF else "%3d" % x for x in row))
    print()


if __name__ == "__main__":
    ref = sys.argv[1] if len(sys.argv) > 2 else "GATTACA"
    read = sys.argv[2] if len(sys.argv) > 2 else "GCATGCA"
    M, X, Y = affine_tables(ref, read)
    show(M, "M (match/substitution)", ref, read)
    show(X, "X (deletion)", ref, read)
    show(Y, "Y (insertion)", ref, read)
    cost, ops = affine_align(ref, read)
    print("Affine minimum cost:", cost, "(recomputed from ops: %d)" % affine_cost_of(ops))
    print("Ref : " + "".join(r for _, r, _ in ops))
    print("Read: " + "".join(q for _, _, q in ops))
    print("Ops :", " ".join(o for o, _, _ in ops))
