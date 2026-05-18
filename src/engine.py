def evaluate_supercharger_rules(battery_temp, voltage_arch, occupancy_rate, grid_demand):
    """
    Evaluates the status of the Supercharger using deterministic logic thresholds.
    Returns: (allocated_power_kw, node_cost_multiplier)
    """
    allocated_power = 250  # Default baseline charging power in kW
    node_cost_multiplier = 1.0  # Default neutral cost multiplier for A*

    print("\n--- Running Rule-Based Expert System Logic ---")

    # RULE SET 1: THERMAL SAFETY GUARDRAILS (Highest Priority Override)
    if battery_temp > 55:
        allocated_power = 50
        node_cost_multiplier = 5.0
        print("[RULE TRIGGERED] Emergency Thermal Derate: Battery temp critical!")
    elif battery_temp > 45:
        allocated_power = 150
        node_cost_multiplier = 2.0
        print("[RULE TRIGGERED] Thermal Throttling: Battery running warm.")

    # RULE SET 2: VEHICLE ARCHITECTURE & POWER CABINET ALLOCATION
    else:
        if voltage_arch == "800V" and occupancy_rate < 50:
            allocated_power = 350
            node_cost_multiplier = 0.5  # Highly optimal node; clear and fast!
            print("[RULE TRIGGERED] Ultra-Fast 800V Architecture Lane Allocated.")
        elif voltage_arch == "400V" or occupancy_rate >= 50:
            allocated_power = 250
            node_cost_multiplier = 1.0
            print("[RULE TRIGGERED] Standard Fast-Charging Mode Engaged.")

    # RULE SET 3: GRID CONGESTION OVERRIDES
    if grid_demand > 85 or occupancy_rate == 100:
        allocated_power = allocated_power * 0.5
        node_cost_multiplier = 10.0  # Extreme penalty; A* should steer clear
        print("[RULE TRIGGERED] Grid Saving Override: Station overloaded/congested.")

    print(f"Final Status -> Power Allocated: {allocated_power}kW | A* Cost Multiplier: {node_cost_multiplier}")
    print("-----------------------------------------------\n")
    
    return allocated_power, node_cost_multiplier