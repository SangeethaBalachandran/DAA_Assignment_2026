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
