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
