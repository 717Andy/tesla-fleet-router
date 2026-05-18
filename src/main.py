import sys
import os

# Append current directory to path so local imports resolve cleanly inside WSL execution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine import evaluate_supercharger_rules
from router import run_fleet_router

def main():
    print("=======================================================")
    print("TESLA V4 SUPERCHARGER COGNITIVE FLEET ROUTER INITIATED")
    print("=======================================================")
    
    # 1. Gather descriptive system state data via user input calls
    try:
        b_temp = float(input("Enter vehicle battery temperature in Celsius (e.g., 35, 48, 58): "))
        v_arch = input("Enter vehicle architecture type ('400V' or '800V'): ").strip().upper()
        occupancy = float(input("Enter station occupancy percentage (0 - 100): "))
        demand = float(input("Enter local grid stress/demand percentage (0 - 100): "))
    except ValueError:
        print("\n[Error] Invalid input detected. Please enter numeric figures where requested.")
        return

    # 2. Process data through the rule-based expert engine module
    power, multiplier = evaluate_supercharger_rules(b_temp, v_arch, occupancy, demand)
    
    # 3. Initialize routing context coordinates
    start_pos = (0, 2)
    destination_pos = (4, 2)
    
    # 4. Compute optimal routing via the A* pathfinding module
    optimal_route = run_fleet_router(start_pos, destination_pos, multiplier)
    
    # 5. Output programmatic summary report
    print("================ ROUTING REPORT ================")
    print(f"Origin Node:       {start_pos}")
    print(f"Destination Node:  {destination_pos}")
    print(f"Generated Route:   {optimal_route}")
    
    # Check if the generated routing path includes the Supercharger node (2, 2)
    if (2, 2) in optimal_route:
        print("\nDecision: The vehicle is routing THROUGH the Supercharger station.")
        print(f"Action: Vehicle will charge at full capacity of {power}kW.")
    else:
        print("\nDecision: A* DETOUR DETECTED!")
        print("Action: The router bypassed the Supercharger via the (2,1) lane due to rule penalties.")
    print("=================================================")

if __name__ == "__main__":
    main()