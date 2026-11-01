import random
def generate_case(n, gap=60, seed=7):
    random.seed(seed)
    # Sorted charger positions, each gap is safely below 120 km.
    return [gap * (i + 1) for i in range(n)]
