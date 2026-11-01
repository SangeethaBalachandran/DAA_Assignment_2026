
import random


def generate_input(n, seed=42):
    """
    Generate a dimension array for n relations.
    Each dimension is a positive integer.
    """
    rng = random.Random(seed + n)

    dimensions = [rng.randint(10, 100)]

    for _ in range(n):
        dimensions.append(rng.randint(10, 100))

    return dimensions


def generate_all_inputs():
    """
    Generate test inputs for at least five input sizes.
    """
    input_sizes = [5, 10, 15, 20, 25]

    test_inputs = {}

    for n in input_sizes:
        test_inputs[n] = generate_input(n)

    return test_inputs


if __name__ == "__main__":
    inputs = generate_all_inputs()

    print("Generated Test Inputs")
    print("---------------------")

    for n, dimensions in inputs.items():
        print(f"\nNumber of relations: {n}")
        print(f"Dimensions: {dimensions}")
