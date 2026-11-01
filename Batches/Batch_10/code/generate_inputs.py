# Implementation by Purushothaman
import random
import time
import csv
import os
import matplotlib.pyplot as plt

from main_solution import solve_branch_and_bound
from rejected_alternative import solve_greedy

def generate_matrix(n):
    return [[random.randint(10, 100) for _ in range(n)] for _ in range(n)]

def main():
    sizes = [4, 6, 8, 10, 12]
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    csv_path = os.path.join(results_dir, 'timing.csv')
    plot_path = os.path.join(results_dir, 'timing_plot.png')
    
    timing_data = []
    print("Generating inputs and timing algorithms. This may take a few seconds...")
    
    for n in sizes:
        matrix = generate_matrix(n)
        
        start_bb = time.time()
        solve_branch_and_bound(matrix)
        time_bb = time.time() - start_bb
        
        start_gr = time.time()
        solve_greedy(matrix)
        time_gr = time.time() - start_gr
        
        timing_data.append((n, time_bb, time_gr))
        print(f"Size N={n:2} | Branch & Bound: {time_bb:.5f}s | Greedy: {time_gr:.5f}s")

    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['n', 'time_branch_and_bound', 'time_greedy'])
        for data in timing_data:
            writer.writerow(data)
            
    n_vals = [d[0] for d in timing_data]
    bb_times = [d[1] for d in timing_data]
    gr_times = [d[2] for d in timing_data]

    plt.figure(figsize=(8, 5))
    plt.plot(n_vals, bb_times, marker='o', label='Branch and Bound', color='red')
    plt.plot(n_vals, gr_times, marker='s', label='Greedy', color='blue')
    plt.title('Algorithm Running Time vs Input Size (N)')
    plt.xlabel('Number of Technicians / Tickets (N)')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_path)
    print(f"\nSuccess: Saved timing.csv and timing_plot.png to the results folder.")

if __name__ == "__main__":
    main()