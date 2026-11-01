import sys

def solve_greedy(cost_matrix):
    n = len(cost_matrix)
    assigned_tickets = [False] * n
    total_cost = 0
    path = []
    
    for i in range(n):
        min_cost = sys.maxsize
        best_ticket = -1
        
        for j in range(n):
            if not assigned_tickets[j] and cost_matrix[i][j] < min_cost:
                min_cost = cost_matrix[i][j]
                best_ticket = j
                
        if best_ticket != -1:
            assigned_tickets[best_ticket] = True
            total_cost += min_cost
            path.append((i, best_ticket))
            
    return total_cost, path

if __name__ == "__main__":
    # Official Batch 10 Assignment Matrix
    cost_matrix = [
        [11, 4, 9, 7],
        [8, 6, 5, 10],
        [7, 10, 3, 9],
        [9, 8, 11, 6]
    ]
    
    print("Executing Greedy Approach for Field Service Technician Assignment...")
    greedy_cost, greedy_assignment = solve_greedy(cost_matrix)
    
    print(f"Total Cost (Greedy): {greedy_cost}")
    print("Assignments (Technician ID, Ticket ID):", greedy_assignment)