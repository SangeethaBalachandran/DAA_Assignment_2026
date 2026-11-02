## 1. Problem Definition

An electric delivery truck must travel a distance of **350 km from Chennai to Bengaluru**. The truck starts with a fully charged battery, and a full charge allows it to travel a maximum distance of **120 km**. Fast-charging stations are available at fixed kilometre positions along the highway.

Each time the truck stops at a charging station, it takes 40 minutes to recharge. The objective is to determine the minimum number of charging stops required to complete the journey without running out of battery.

The problem is modelled as a **Greedy Optimization Problem**, where the truck selects the farthest reachable charging station at each step to minimize the total number of stops.

### 1.1 Input

- Total journey distance: 350 km.
- Maximum travel distance per full charge: 120 km.
- Initial battery condition: 100% (fully charged).
- Charging station positions (km from Chennai):  
  `40, 95, 130, 180, 210, 260, 300, 330`
- Time required for each charging stop: 40 minutes.

### 1.2 Output

The algorithm produces:

1. Minimum number of charging stops required.
2. Locations of the selected charging stations.
3. Total charging time incurred during the journey.
4. Whether the journey is feasible with the available charging stations.

**Expected Output for the Given Instance:**

- Selected charging stations: 95 km, 210 km, 330 km.
- Minimum number of stops: 3.
- Total charging time: 120 minutes.
- Journey feasibility: Feasible.

### 1.3 Constraints

1. The truck starts from Chennai at kilometre 0.
2. The destination is Bengaluru at kilometre 350.
3. The truck can travel at most 120 km on a full charge.
4. Charging stations are located at fixed positions along the route.
5. The truck can recharge only at the available charging stations.
6. The truck must not travel beyond its available battery range.
7. Each charging stop incurs a fixed time penalty of 40 minutes.
8. Charging stations must be visited in increasing order of their kilometre positions.
9. The destination is reachable only if the remaining distance is within the available battery range.

### 1.4 Assumptions

1. The truck begins its journey with a 100% charged battery.
2. Every charging station can provide a complete recharge to 100%.
3. A full charge always provides a driving range of exactly 120 km.
4. Battery consumption is uniform throughout the journey.
5. Road conditions, traffic, weather and elevation changes are ignored.
6. Charging stations are always operational and available.
7. The charging time is fixed at 40 minutes per stop, regardless of the remaining battery level.
8. The truck does not need to recharge after reaching Bengaluru.
9. The charging station positions are known in advance and can be sorted in ascending order.
10. The primary objective is to minimize the number of charging stops rather than minimize distance, energy consumption or charging cost.

**Problem Classification:** Optimization Problem  
**Design Technique:** Greedy Method  
**Objective Function:** Minimize the total number of charging stops.  
**Feasibility Condition:** The distance between any two consecutive charging points, including the starting point and destination, must not exceed 120 km.

## 2. Greedy Algorithm Design

The problem is solved using the **Greedy Method**, specifically the **Farthest-Reachable Charging Station Strategy**.

At every step, the truck selects the farthest charging station that can be reached using its current battery charge. This allows the truck to cover the maximum possible distance before making the next charging stop, thereby reducing the total number of stops.

### 2.1 Greedy Choice

At the current position, let the maximum reachable distance be:

`Current Position + 120 km`

Among all available charging stations within this range, the algorithm selects the station with the greatest kilometre position.

The selected station becomes the next charging point. The truck recharges fully at that station and repeats the same process until the destination is reachable.

**Greedy Strategy:** Always choose the farthest reachable charging station.

### 2.2 Algorithm Steps

1. Sort all charging station positions in ascending order.
2. Initialize the current position to 0 km (Chennai).
3. Check whether the destination is reachable directly from the current position.
4. If the destination is not reachable, identify all charging stations within 120 km of the current position.
5. Select the farthest reachable charging station.
6. If no charging station is reachable, declare the journey infeasible.
7. Otherwise, add the selected station to the list of charging stops.
8. Update the current position to the selected station.
9. Repeat until the destination is within the truck's maximum travel range.
10. Return the selected charging stations, total number of stops, total charging time, and journey feasibility.

### 2.3 Pseudocode

```text
GREEDY-CHARGING-STOPS(stations, destination, range)

    Sort stations in ascending order

    current_position = 0
    stops = empty list

    Add destination to stations

    while destination - current_position > range:

        farthest_station = current_position

        for each station in stations:

            if station > current_position
               and station - current_position <= range:

                farthest_station = station

            else if station - current_position > range:
                break

        if farthest_station == current_position:
            return "Journey Not Feasible"

        Add farthest_station to stops
        current_position = farthest_station

    total_stops = length(stops)
    total_charging_time = total_stops * 40

    return stops, total_stops, total_charging_time
```

### 2.4 Greedy Algorithm Execution for the Given Input

The truck starts at kilometre 0 with a maximum range of 120 km.

| Step | Current Position | Maximum Reach | Selected Station | Distance Travelled |
|---|---:|---:|---:|---:|
| 1 | 0 km | 120 km | 95 km | 95 km |
| 2 | 95 km | 215 km | 210 km | 115 km |
| 3 | 210 km | 330 km | 330 km | 120 km |
| 4 | 330 km | 450 km | Destination (350 km) | 20 km |

**Final Selected Route:**

`0 → 95 → 210 → 330 → 350 km`

**Algorithm Result:**

- Selected charging stations: 95 km, 210 km, 330 km.
- Minimum charging stops: 3.
- Total charging time: 3 × 40 = 120 minutes.
- Journey status: Feasible.

### 2.5 Implementation Details

The algorithm is implemented in Python. The implementation accepts the route distance, maximum vehicle range, and available charging station positions as input.

The charging station positions are sorted before processing. The algorithm then scans the stations and selects the farthest station that is reachable from the current position.

If no charging station is reachable and the destination is outside the available range, the algorithm reports that the journey is infeasible.

The implementation returns the selected charging stops, the total number of stops, the total charging time, and the feasibility status.

The implementation follows the greedy strategy and avoids exploring unnecessary combinations of charging stations.


## 3. Correctness of the Greedy Algorithm

The greedy algorithm selects the farthest reachable charging station at every step. This section explains why this strategy produces a feasible route with the minimum number of charging stops.

### 3.1 Greedy Choice Property

At any current position, the truck can travel at most 120 km before requiring another charge.

The algorithm selects the farthest charging station within this reachable distance.

This is a locally optimal choice because it allows the truck to travel as far as possible before making the next charging stop. Selecting a station closer to the current position would use a charging stop without making as much progress along the route.

### 3.2 Exchange Argument

Consider an optimal solution that selects a charging station O as its first stop from the current position.

Let G be the farthest reachable charging station selected by the greedy algorithm.

Since G is the farthest reachable station, G must be at the same position as O or farther along the route.

We can replace O with G without increasing the number of charging stops.

Any later charging station that was reachable from O will also be reachable from G because G is farther along the route. Therefore, this replacement does not make the remaining journey more difficult.

Thus, there exists an optimal solution that begins with the same choice as the greedy algorithm.

### 3.3 Inductive Proof

The correctness of the algorithm can also be established using induction.

**Base Case:**

If the destination is within 120 km of the starting position, the truck can reach the destination without any charging stops. The greedy algorithm correctly returns zero stops, which is optimal.

**Inductive Hypothesis:**

Assume that the greedy algorithm produces an optimal solution for the remaining journey after a particular charging stop.

**Inductive Step:**

From the current position, the greedy algorithm selects the farthest reachable charging station.

By the exchange argument, this choice can be part of an optimal solution. After reaching this station, the remaining problem has the same structure as the original problem.

By the inductive hypothesis, the greedy algorithm also produces an optimal solution for the remaining journey.

Therefore, the complete route produced by the greedy algorithm uses the minimum possible number of charging stops.

**Conclusion:**

The greedy algorithm is correct because it always makes a farthest-reachable choice that can be included in an optimal solution.

## 4. Complexity Analysis

Let `n` represent the number of available charging stations and `k` represent the number of charging stops selected by the algorithm.

### 4.1 Time Complexity

The algorithm first sorts the charging stations in ascending order.

- Sorting the stations requires `O(n log n)` time.
- After sorting, the algorithm scans the stations to identify the farthest reachable station.
- Each station is processed at most once in an efficient forward-scan implementation, requiring `O(n)` time.

Therefore:

**Time Complexity:**

- If the stations are already sorted: `O(n)`.
- Including sorting: `O(n log n)`.

### 4.2 Space Complexity

The algorithm stores the selected charging stations in an output list.

If `k` charging stops are selected, the output list requires `O(k)` space.

The sorting operation may also require additional implementation-dependent memory.

**Auxiliary Space Complexity:** `O(1)` for the scan itself, excluding sorting and the output list.

**Output Space Complexity:** `O(k)`.

### 4.3 Complexity Summary

| Operation | Time Complexity |
|---|---|
| Sorting charging stations | O(n log n) |
| Greedy station selection | O(n) |
| Total time including sorting | O(n log n) |
| Total time if already sorted | O(n) |
| Output storage | O(k) |

The greedy method is efficient because it avoids checking every possible combination of charging stations. It processes the sorted stations in a single forward scan.
## 5. Experimental Evaluation

The greedy charging-stop algorithm was implemented in Python and tested using different input sizes to evaluate its performance.

The experiments compare the execution time of the selected greedy algorithm with an alternative approach. Different numbers of charging stations are generated to observe how the execution time changes as the input size increases.

### 5.1 Experimental Setup

The experiment uses the following setup:

- Programming language: Python.
- Input: Different sets of charging station positions.
- Input sizes: Multiple values of `n`, representing the number of charging stations.
- Selected algorithm: Greedy farthest-reachable charging station algorithm.
- Comparison algorithm: Alternative Dynamic Programming implementation.
- Performance metric: Execution time in milliseconds.

The charging station positions are sorted before applying the greedy algorithm. Both implementations are tested using generated inputs to compare their execution times.

### 5.2 Results

The measured execution times are recorded in the file:

`results/timing.csv`

The corresponding performance graph is available at:

`results/timing_plot.png`

The graph illustrates how the execution time changes with increasing input size.

### 5.3 Analysis

The greedy algorithm scans the sorted charging stations and selects the farthest reachable station.

Its time complexity is `O(n)` when the stations are already sorted and `O(n log n)` when sorting is included.

The straightforward Dynamic Programming implementation considers possible previous stations when calculating the minimum number of stops. Its time complexity is `O(n²)`.

Therefore, the greedy approach is expected to scale more efficiently for larger input sizes under the assumptions of this problem.

Actual execution times may vary depending on the system configuration, Python environment, and input data.

## 6. Extensions and Real-World Applications

The implemented greedy algorithm solves the basic EV charging problem under fixed-range and equal-stop-cost assumptions. However, real-world EV charging scenarios may involve additional constraints such as variable charging prices, different charging speeds, and changing battery ranges.

### 6.1 Variable Driving Range

In a more complex scenario, the vehicle may have different driving ranges depending on the charging station, battery condition, or road conditions.

This can be modelled as a directed graph:

- Each charging station represents a vertex.
- A directed edge from station `i` to station `j` exists if the vehicle can travel from `i` to `j` using the available range after charging at `i`.
- The destination is represented as the final vertex.

Breadth-First Search (BFS) can be used to find a route with the minimum number of charging transitions when each transition has equal cost.

### 6.2 Variable Charging Costs

The farthest-reachable greedy strategy minimises the number of stops under the assumptions of the original problem. However, it may not minimise the total charging cost when electricity prices differ between stations.

Consider the following example:

- Maximum driving range: 120 km.
- Charging stations: 60 km, 110 km, and 180 km.
- Destination: 240 km.
- Electricity price at 60 km: ₹1 per unit.
- Electricity price at 110 km: ₹10 per unit.
- Electricity price at 180 km: ₹1 per unit.

The farthest-first strategy may choose the station at 110 km. It arrives with 10 units of range remaining and needs to purchase 70 units at ₹10 each. It then purchases another 60 units at ₹1 each at the 180 km station.

Total cost:

`(70 × ₹10) + (60 × ₹1) = ₹760`

A cheaper strategy is to stop at 60 km, purchase 60 units at ₹1 each, travel to 180 km, and purchase another 60 units at ₹1 each.

Total cost:

`(60 × ₹1) + (60 × ₹1) = ₹120`

This demonstrates that farthest-first is not always the best strategy when the objective is to minimise charging cost.

For variable prices and partial charging, a state-based shortest-path or Dynamic Programming approach can be used.

### 6.3 Real-World Application

The concepts used in this project are relevant to electric vehicle route-planning systems.

For example, **A Better Routeplanner (ABRP)** is a real-world EV trip-planning service that helps drivers plan charging stops based on vehicle and journey information.

Reference links:

- Website: https://abetterrouteplanner.com/home
- Charging stops help: https://abrp.featurebase.app/en/help/articles/4023913-charging-stops

Our project uses a simplified model to demonstrate how algorithm design can help optimise charging-stop decisions.

## 7. Conclusion

This project applies the Greedy Method to solve the EV charging-stop optimisation problem for a 350 km journey from Chennai to Bengaluru.

The vehicle has a maximum driving range of 120 km per full charge, and charging stations are available at predefined kilometre positions.

By selecting the farthest reachable charging station at every step, the algorithm identifies the route:

`0 → 95 → 210 → 330 → 350 km`

The final result is:

- Minimum charging stops: 3.
- Selected charging stations: 95 km, 210 km, and 330 km.
- Total charging-stop time: 120 minutes.
- Journey feasibility: Feasible.

The correctness of the greedy strategy is supported by an exchange argument and induction. Its time complexity is `O(n)` when the stations are already sorted and `O(n log n)` when sorting is included.

The experimental evaluation compares the greedy algorithm with a Dynamic Programming alternative. The results demonstrate the efficiency of the greedy approach for the given problem assumptions.

We also explored extensions for more realistic scenarios involving variable driving ranges and charging costs.

Overall, the project demonstrates that the Greedy Method provides an efficient and optimal solution for the given problem assumptions, while more complex optimisation techniques are required when additional real-world constraints are introduced.

## 8. Team Contributions and Presentation

### 8.1 Team Contributions

| Member | Contribution |
|---|---|
| 24I311 | Problem definition, input-output specification, constraints, assumptions, and introduction. |
| 24I324 | Greedy algorithm design, algorithm steps, pseudocode, and Python implementation. |
| 24I304 | Correctness proof, exchange argument, induction, and complexity analysis. |
| 24I322 | Alternative algorithm implementation, input generation, experimental testing, and performance evaluation. |
| 24I339 | README integration, experimental results presentation, extensions, real-world applications, conclusion, and final presentation coordination. |

### 8.2 Presentation

The team presentation explains the problem, selected algorithm, implementation, correctness, complexity, experimental evaluation, and possible extensions.

**Presentation recording:** [Watch Demo](https://drive.google.com/drive/folders/107jTMHhU_-85rzs5a_r1iK3KFEgyjNJ)

**Presentation slides:** `slides.pdf`
