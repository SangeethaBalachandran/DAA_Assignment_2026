
"""Rejected alternative: next-fit greedy line packing.

This is a useful baseline, but it does not guarantee the minimum cubic
whitespace penalty because it never revisits earlier line-break decisions.
"""

def greedy_layout(words, width):
    lines = []
    current = []
    used = 0
    for word in words:
        extra = len(word) if not current else len(word) + 1
        if used + extra <= width:
            current.append(word)
            used += extra
        else:
            if not current:
                raise ValueError("A word exceeds the line width")
            lines.append(" ".join(current))
            current = [word]
            used = len(word)
    if current:
        lines.append(" ".join(current))

    penalty = 0
    for line in lines[:-1]:  # final line is free
        penalty += (width - len(line)) ** 3
    return lines, penalty


if __name__ == "__main__":
    words = "A clear model of the problem is half of the final answer".split()
    lines, penalty = greedy_layout(words, 16)
    print("Greedy layout:")
    for line in lines:
        print(line)
    print("Greedy penalty:", penalty)
