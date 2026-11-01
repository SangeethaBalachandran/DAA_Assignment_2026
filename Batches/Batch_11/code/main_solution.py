"""Chosen algorithm: minimum-penalty paragraph layout using dynamic programming."""

def word_wrap(words, width):
    n = len(words)
    if width <= 0:
        raise ValueError("width must be positive")
    if any(len(w) > width for w in words):
        raise ValueError("A word exceeds the line width; use the hyphenation extension.")

    prefix = [0] * (n + 1)
    for k, word in enumerate(words, 1):
        prefix[k] = prefix[k - 1] + len(word)

    dp = [float("inf")] * (n + 1)
    parent = [-1] * (n + 1)
    dp[0] = 0

    for j in range(1, n + 1):
        for i in range(j, 0, -1):
            used = prefix[j] - prefix[i - 1] + (j - i)
            if used > width:
                break
            line_cost = 0 if j == n else (width - used) ** 3
            candidate = dp[i - 1] + line_cost
            if candidate < dp[j]:
                dp[j] = candidate
                parent[j] = i

    lines = []
    j = n
    while j:
        i = parent[j]
        if i < 1:
            raise RuntimeError("No valid layout")
        lines.append(" ".join(words[i - 1:j]))
        j = i - 1
    lines.reverse()
    return lines, int(dp[n])


if __name__ == "__main__":
    text = "A clear model of the problem is half of the final answer"
    words = text.split()
    lines, penalty = word_wrap(words, 16)
    print("Optimal layout:")
    for line in lines:
        print(line)
    print("Minimum penalty:", penalty)
