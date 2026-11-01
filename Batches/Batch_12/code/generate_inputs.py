import random


def generate_permutation(n, seed=None, order="random"):
    """Generate a random, sorted, or reverse-sorted permutation of 1..n."""
    values = list(range(1, n + 1))
    if order == "reverse":
        values.reverse()
    elif order == "random":
        random.Random(seed).shuffle(values)
    elif order != "sorted":
        raise ValueError("order must be random, sorted, or reverse")
    return values


if __name__ == "__main__":
    for size in [100, 500, 1000, 2000, 5000]:
        print(size, generate_permutation(size, seed=42)[:10])
