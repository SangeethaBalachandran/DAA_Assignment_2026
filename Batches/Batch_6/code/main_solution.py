#!/usr/bin/env python3
"""Minimum-cost global alignment of a read against a reference region.

Usage:  python3 main_solution.py REFERENCE READ
Costs:  match 0, substitution 1, insertion 1, deletion 1.

Operation codes
  M  match         (ref base == read base)
  S  substitution  (ref base != read base)
  I  insertion     (read base that is not in the reference)
  D  deletion      (reference base that is missing from the read)

D[i][j] = minimum cost of aligning the first i reference bases with the first j read bases.
"""
import sys

SUB, INS, DEL = 1, 1, 1


def fill_table(ref, read):
    m, n = len(ref), len(read)
    D = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        D[i][0] = i * DEL
    for j in range(1, n + 1):
        D[0][j] = j * INS
    for i in range(1, m + 1):
        ri = ref[i - 1]
        row, prev = D[i], D[i - 1]
        for j in range(1, n + 1):
            v = prev[j - 1] + (0 if ri == read[j - 1] else SUB)  # diagonal
            up = prev[j] + DEL                                    # deletion
            if up < v:
                v = up
            left = row[j - 1] + INS                               # insertion
            if left < v:
                v = left
            row[j] = v
    return D


def traceback(D, ref, read):
    """Walk from (m,n) to (0,0); tie-break order: diagonal, deletion, insertion."""
    i, j = len(ref), len(read)
    ops = []
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            s = 0 if ref[i - 1] == read[j - 1] else SUB
            if D[i][j] == D[i - 1][j - 1] + s:
                ops.append(("M" if s == 0 else "S", ref[i - 1], read[j - 1]))
                i -= 1
                j -= 1
                continue
        if i > 0 and D[i][j] == D[i - 1][j] + DEL:
            ops.append(("D", ref[i - 1], "-"))
            i -= 1
            continue
        ops.append(("I", "-", read[j - 1]))
        j -= 1
    ops.reverse()
    return ops


def align(ref, read):
    D = fill_table(ref, read)
    return D[len(ref)][len(read)], traceback(D, ref, read)


def ops_cost(ops):
    return sum(0 if o == "M" else 1 for o, _, _ in ops)


def format_alignment(ops):
    top = "".join(r for _, r, _ in ops)
    mid = "".join("|" if o == "M" else " " for o, _, _ in ops)
    bot = "".join(q for _, _, q in ops)
    return "Ref : %s\n      %s\nRead: %s" % (top, mid, bot)


def variants(ops):
    """List variants with 1-based reference positions."""
    out, pos = [], 0
    for o, r, q in ops:
        if o in "MSD":
            pos += 1
        if o == "S":
            out.append("ref pos %d: substitution %s>%s" % (pos, r, q))
        elif o == "D":
            out.append("ref pos %d: deletion of %s" % (pos, r))
        elif o == "I":
            out.append("after ref pos %d: insertion of %s" % (pos, q))
    return out


def all_optimal(D, ref, read, limit=1000):
    """Enumerate every optimal alignment (all tie-breaks) by DFS over the table."""
    res = []

    def go(i, j, acc):
        if len(res) >= limit:
            return
        if i == 0 and j == 0:
            res.append(list(reversed(acc)))
            return
        if i > 0 and j > 0:
            s = 0 if ref[i - 1] == read[j - 1] else SUB
            if D[i][j] == D[i - 1][j - 1] + s:
                acc.append(("M" if s == 0 else "S", ref[i - 1], read[j - 1]))
                go(i - 1, j - 1, acc)
                acc.pop()
        if i > 0 and D[i][j] == D[i - 1][j] + DEL:
            acc.append(("D", ref[i - 1], "-"))
            go(i - 1, j, acc)
            acc.pop()
        if j > 0 and D[i][j] == D[i][j - 1] + INS:
            acc.append(("I", "-", read[j - 1]))
            go(i, j - 1, acc)
            acc.pop()

    go(len(ref), len(read), [])
    return res


def print_table(D, ref, read):
    print("      -  " + "  ".join(read))
    for i, row in enumerate(D):
        print(("-" if i == 0 else ref[i - 1]) + "  " + " ".join("%2d" % x for x in row))


if __name__ == "__main__":
    ref = sys.argv[1] if len(sys.argv) > 2 else "GATTACA"
    read = sys.argv[2] if len(sys.argv) > 2 else "GCATGCA"
    D = fill_table(ref, read)
    print_table(D, ref, read)
    ops = traceback(D, ref, read)
    print("\nMinimum cost:", D[-1][-1])
    print(format_alignment(ops))
    print("Edit operations:", " ".join(o for o, _, _ in ops))
    for v in variants(ops):
        print("  -", v)
    allo = all_optimal(D, ref, read)
    print("\nNumber of co-optimal alignments:", len(allo))
    for a in allo:
        print(" ", "".join(o for o, _, _ in a))
