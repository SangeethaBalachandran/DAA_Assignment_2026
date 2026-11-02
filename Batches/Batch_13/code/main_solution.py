"""
Batch 13 - EV logistics: minimum charging stops
Greedy farthest-reachable charger algorithm for equal full-charge range.
Input positions are sorted and lie strictly between 0 and destination.
"""
def min_charging_stops(chargers, destination, range_km):
    points = sorted(chargers)
    if destination < 0 or range_km <= 0:
        raise ValueError("destination must be non-negative and range positive")
    if any(x <= 0 or x >= destination for x in points):
        raise ValueError("chargers must lie strictly between start and destination")

    stops = []
    current = 0
    i = 0
    while destination - current > range_km:
        farthest = current
        while i < len(points) and points[i] - current <= range_km:
            farthest = points[i]
            i += 1
        if farthest == current:
            return None  
        stops.append(farthest)
        current = farthest
    return stops


def main():
    chargers = [40, 95, 130, 180, 210, 260, 300, 330]
    route = min_charging_stops(chargers, 350, 120)
    if route is None:
        print("Trip infeasible")
    else:
        print("Minimum stops:", len(route))
        print("Stop locations (km):", route)
        print("Legs:", [0] + route + [350])

if __name__ == "__main__":
    main()
