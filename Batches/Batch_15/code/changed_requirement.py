
"""
Member 5 - Batch 15
Changed Requirement: 2D Bin Packing with Anti-Affinity

Objective:
Minimize the number of physical servers while satisfying:
1. CPU capacity
2. RAM capacity
3. Replicas of the same service cannot share a server
"""

import math
from collections import Counter


def estimate_lower_bound(vms, cpu_capacity, ram_capacity):
    """
    Estimate a lower bound on the number of servers required.

    The answer cannot be smaller than:
    - Total CPU / CPU capacity
    - Total RAM / RAM capacity
    - Maximum number of VMs belonging to one service
    """

    if not vms:
        return 0

    total_cpu = sum(vm["cpu"] for vm in vms)
    total_ram = sum(vm["ram"] for vm in vms)

    cpu_bound = math.ceil(total_cpu / cpu_capacity)
    ram_bound = math.ceil(total_ram / ram_capacity)

    service_counts = Counter(
        vm["service"] for vm in vms
    )
    anti_affinity_bound = max(service_counts.values())

    return max(
        cpu_bound,
        ram_bound,
        anti_affinity_bound
    )


def solve_changed_requirement(vms, cpu_capacity, ram_capacity):
    """
    Find an optimal VM placement using backtracking
    with branch-and-bound pruning.

    Each VM is a dictionary:
    {
        "name": "VM1",
        "cpu": 6,
        "ram": 8,
        "service": "A"
    }

    Returns:
        minimum number of servers, server placements
    """

    if cpu_capacity <= 0 or ram_capacity <= 0:
        raise ValueError("Server capacities must be positive.")

    # Validate VM data
    for vm in vms:
        if vm["cpu"] <= 0 or vm["ram"] <= 0:
            raise ValueError(
                f'{vm["name"]}: CPU and RAM must be positive.'
            )

        if vm["cpu"] > cpu_capacity:
            raise ValueError(
                f'{vm["name"]} exceeds server CPU capacity.'
            )

        if vm["ram"] > ram_capacity:
            raise ValueError(
                f'{vm["name"]} exceeds server RAM capacity.'
            )

    if not vms:
        return 0, []

    # Largest combined resource requirements first
    ordered_vms = sorted(
        vms,
        key=lambda vm: (
            vm["cpu"] / cpu_capacity
            + vm["ram"] / ram_capacity
        ),
        reverse=True
    )

    n = len(ordered_vms)

    lower_bound = estimate_lower_bound(
        ordered_vms, cpu_capacity, ram_capacity
    )

    # A valid initial solution: one VM per server
    best_count = n
    best_servers = [
        {
            "cpu_used": vm["cpu"],
            "ram_used": vm["ram"],
            "services": {vm["service"]},
            "vms": [vm["name"]]
        }
        for vm in ordered_vms
    ]

    servers = []

    def backtrack(i):
        nonlocal best_count, best_servers

        # All VMs have been placed
        if i == n:
            if len(servers) < best_count:
                best_count = len(servers)

                best_servers = [
                    {
                        "cpu_used": s["cpu_used"],
                        "ram_used": s["ram_used"],
                        "services": set(s["services"]),
                        "vms": s["vms"][:]
                    }
                    for s in servers
                ]
            return

        # Prune if this branch cannot improve the best solution
        if len(servers) >= best_count:
            return

        vm = ordered_vms[i]

        # Equivalent server states need only be tried once
        seen_states = set()

        for server in servers:
            state = (
                server["cpu_used"],
                server["ram_used"],
                frozenset(server["services"])
            )

            if state in seen_states:
                continue

            seen_states.add(state)

            # Check both resource capacities and anti-affinity
            if (
                server["cpu_used"] + vm["cpu"] <= cpu_capacity
                and server["ram_used"] + vm["ram"] <= ram_capacity
                and vm["service"] not in server["services"]
            ):
                # Place VM
                server["cpu_used"] += vm["cpu"]
                server["ram_used"] += vm["ram"]
                server["services"].add(vm["service"])
                server["vms"].append(vm["name"])

                backtrack(i + 1)

                # Undo placement
                server["vms"].pop()
                server["services"].remove(vm["service"])
                server["cpu_used"] -= vm["cpu"]
                server["ram_used"] -= vm["ram"]

        # Open a new server if it may improve the solution
        if len(servers) + 1 < best_count:
            servers.append({
                "cpu_used": vm["cpu"],
                "ram_used": vm["ram"],
                "services": {vm["service"]},
                "vms": [vm["name"]]
            })

            backtrack(i + 1)

            servers.pop()

    backtrack(0)

    return best_count, best_servers


def validate_solution(servers, vms, cpu_capacity, ram_capacity):
    """Check that every VM is assigned exactly once and all constraints hold."""

    vm_by_name = {vm["name"]: vm for vm in vms}
    assigned = []

    for server in servers:
        cpu_total = 0
        ram_total = 0
        services = set()

        for name in server["vms"]:
            if name not in vm_by_name:
                return False

            vm = vm_by_name[name]
            assigned.append(name)

            cpu_total += vm["cpu"]
            ram_total += vm["ram"]

            # Anti-affinity: same service cannot occur twice
            if vm["service"] in services:
                return False

            services.add(vm["service"])

        if cpu_total > cpu_capacity:
            return False

        if ram_total > ram_capacity:
            return False

        if cpu_total != server["cpu_used"]:
            return False

        if ram_total != server["ram_used"]:
            return False

    expected = [vm["name"] for vm in vms]

    return (
        len(assigned) == len(expected)
        and len(set(assigned)) == len(expected)
        and set(assigned) == set(expected)
    )


def print_solution(servers, cpu_capacity, ram_capacity):
    """Display the final placement and resource utilization."""

    print("\nOptimal Placement")
    print("=" * 45)

    for i, server in enumerate(servers, start=1):
        print(f"\nServer {i}")
        print("  VMs:", ", ".join(server["vms"]))
        print(
            f'  CPU: {server["cpu_used"]}/{cpu_capacity} vCPUs'
        )
        print(
            f'  RAM: {server["ram_used"]}/{ram_capacity} GB'
        )


if __name__ == "__main__":

    CPU_CAPACITY = 10
    RAM_CAPACITY = 16

    # Sample input
    vms = [
        {"name": "VM1", "cpu": 6, "ram": 8, "service": "A"},
        {"name": "VM2", "cpu": 4, "ram": 6, "service": "B"},
        {"name": "VM3", "cpu": 5, "ram": 4, "service": "A"},
        {"name": "VM4", "cpu": 2, "ram": 4, "service": "C"}
    ]

    print("Changed Requirement: 2D Bin Packing")
    print("=" * 45)
    print(f"CPU capacity per server: {CPU_CAPACITY} vCPUs")
    print(f"RAM capacity per server: {RAM_CAPACITY} GB")
    print(f"Number of VMs: {len(vms)}")

    lower_bound = estimate_lower_bound(
        vms, CPU_CAPACITY, RAM_CAPACITY
    )

    print(f"Estimated lower bound: {lower_bound}")

    minimum_servers, placement = solve_changed_requirement(
        vms, CPU_CAPACITY, RAM_CAPACITY
    )

    print(f"Minimum servers required: {minimum_servers}")

    valid = validate_solution(
        placement, vms, CPU_CAPACITY, RAM_CAPACITY
    )

    print("Placement valid:", valid)

    print_solution(
        placement, CPU_CAPACITY, RAM_CAPACITY
    )

    if minimum_servers == lower_bound:
        print("\nOptimality verified: solution matches lower bound.")
    else:
        print(
            "\nSolution is valid; lower bound alone does not "
            "prove optimality for this input."
        )
