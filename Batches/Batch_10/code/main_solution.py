import sys
import heapq

class Node:
    def __init__(self, cost, path, bound, level, assigned):
        self.cost = cost
        self.path = path
        self.bound = bound
        self.level = level
        self.assigned = assigned

    def __lt__(self, other):
        return self.bound < other.bound

def calculate_lower_bound(cost_matrix, assigned, level, current_cost):
    n = len(cost_matrix)
    bound = current_cost
    for i in range(level, n):
        min_val = sys.maxsize
        for j in range(n):
            if not assigned[j] and cost_matrix[i][j] < min_val:
                min_val = cost_matrix[i][j]
        if min_val != sys.maxsize:
            bound += min_val
    return bound

def solve_branch_and_bound(cost_matrix):
    n = len(cost_matrix)
    pq = []
    initial_bound = calculate_lower_bound(cost_matrix, [False]*n, 0, 0)
    start_node = Node(0, [], initial_bound, 0, [False]*n)
    heapq.heappush(pq, start_node)
    
    min_cost = sys.maxsize
    best_path = []
    
    while pq:
        current = heapq.heappop(pq)
        
        if current.bound >= min_cost:
            continue
            
        if current.level == n:
            if current.cost < min_cost:
                min_cost = current.cost
                best_path = current.path
            continue
            
        i = current.level
        for j in range(n):
            if not current.assigned[j]:
                new_cost = current.cost + cost_matrix[i][j]
                new_path = current.path + [(i, j)]
                new_assigned = list(current.assigned)
                new_assigned[j] = True
                
                new_bound = calculate_lower_bound(cost_matrix, new_assigned, i + 1, new_cost)
                
                if new_bound < min_cost:
                    heapq.heappush(pq, Node(new_cost, new_path, new_bound, i + 1, new_assigned))
                    
    return min_cost, best_path

if __name__ == "__main__":
    # Official Batch 10 Assignment Matrix
    cost_matrix = [
        [11, 4, 9, 7],
        [8, 6, 5, 10],
        [7, 10, 3, 9],
        [9, 8, 11, 6]
    ]
    
    print("Executing Branch and Bound for Field Service Technician Assignment...")
    min_cost, assignment = solve_branch_and_bound(cost_matrix)
    
    print(f"Minimum Total Cost (Travel Time / Skill Mismatch): {min_cost}")
    print("Assignments (Technician ID, Ticket ID):", assignment)