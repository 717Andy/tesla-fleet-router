# Tesla Supercharger V4 Fleet Router

A Python simulation of one Supercharger stop, where safety rules set the charging power and the cost of driving through the stall.

## About

This project is a rule-based expert system. A short list of `if` / `elif` checks stands in for the hard limits a charging site has to enforce: keep a hot battery off a high-power stall, give an open 800V cabinet the fast lane, and ease off when the station or the local grid is already loaded. Each rule sets a power cap and a cost for driving through the stall. When that cost climbs high enough, A* sends the vehicle around the site.

The scene is a single vehicle crossing a 5×5 grid from `(0, 2)` to `(4, 2)`. Column `x = 2` is a wall with two gaps: the stall at `(2, 2)` and a bypass lane at `(2, 1)`. `src/main.py` asks for four readings. `src/engine.py` turns them into a power cap and a node-cost multiplier:

- Battery temperature decides whether the pack can take a fast charge. Above 55°C the cap is 50 kW. From just above 45°C through 55°C the cap is 150 kW.
- Pack voltage (`400V` or `800V`) and station occupancy decide the cabinet. A cool 800V vehicle at a site below 50% full is offered 350 kW. A 400V pack, or a site at 50% full or more, stays at the 250 kW baseline.
- Grid demand above 85%, or a station at exactly 100% occupancy, halves whatever power the earlier rules chose and marks the stall as a place to avoid.

`src/router.py` plans the drive with A*. An ordinary step costs 1. The step onto the stall costs `1 × multiplier`. On a cool, uncrowded 800V stop the multiplier is 0.5, the straight line through `(2, 2)` is the cheap path, and the report sends the vehicle in to charge. Above 55°C the multiplier is 5.0. Under the grid rule it is 10.0. The stall stays on the same coordinate either way. A* reads the higher cost as a jam and returns the longer bypass through `(2, 1)`.

Thermal checks run first, and cabinet allocation runs only when the pack is 45°C or cooler. The grid rule runs last, so it can replace both the power and the multiplier. The same four numbers always produce the same cap, the same multiplier, and the same route. You type the readings at the keyboard, and the program prints which rules fired and which path it chose.

The later sections list every threshold, the sample sessions, and the path costs.

## Requirements

- Python 3
- No third-party packages. `requirements.txt` records that the standard library (`os`, `sys`, and `heapq`) is enough.

## Run

From the project root:

```bash
python3 src/main.py
```

The program asks for:

| Prompt | Expected value |
| --- | --- |
| Battery temperature | Degrees Celsius, such as `35`, `48`, or `58` |
| Architecture | `400V` or `800V` (letter case does not matter) |
| Station occupancy | A percentage from `0` to `100` |
| Grid demand | A percentage from `0` to `100` |

A non-numeric entry in a numeric field prints an error and exits.

### Sample session

Clear, cool 800V site:

```text
Enter vehicle battery temperature in Celsius (e.g., 35, 48, 58): 30
Enter vehicle architecture type ('400V' or '800V'): 800V
Enter station occupancy percentage (0 - 100): 20
Enter local grid stress/demand percentage (0 - 100): 40
```

```text
[RULE TRIGGERED] Ultra-Fast 800V Architecture Lane Allocated.
Final Status -> Power Allocated: 350kW | A* Cost Multiplier: 0.5

Origin Node:       (0, 2)
Destination Node:  (4, 2)
Generated Route:   [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]

Decision: The vehicle is routing THROUGH the Supercharger station.
Action: Vehicle will charge at full capacity of 350kW.
```

Hot pack (80°C) on a 400V vehicle, with the site at 25% occupancy and the grid at 70%:

```text
[RULE TRIGGERED] Emergency Thermal Derate: Battery temp critical!
Final Status -> Power Allocated: 50kW | A* Cost Multiplier: 5.0

Generated Route:   [(0, 2), (1, 2), (1, 1), (2, 1), (3, 1), (3, 2), (4, 2)]

Decision: A* DETOUR DETECTED!
Action: The router bypassed the Supercharger via the (2,1) lane due to rule penalties.
```

## Rules

`evaluate_supercharger_rules` in `src/engine.py` returns `(allocated_power_kw, node_cost_multiplier)`. It starts from a baseline of **250 kW** and a multiplier of **1.0**, then applies the sets below in order.

Thermal rules and cabinet rules are mutually exclusive: a pack warmer than 45°C never receives the 800V ultra-fast lane. The grid rule runs afterward and can rewrite both outputs.

### 1. Thermal safety

| Battery temperature | Power | Multiplier | What the router does |
| --- | --- | --- | --- |
| Above 55°C | 50 kW | 5.0 | Bypass lane |
| Above 45°C, up to 55°C | 150 kW | 2.0 | Still drives through the charger |

### 2. Architecture and cabinet allocation

Applied when temperature is 45°C or below.

| Condition | Power | Multiplier |
| --- | --- | --- |
| `800V` and occupancy below 50% | 350 kW | 0.5 |
| `400V`, or occupancy of 50% or higher | 250 kW | 1.0 |

An architecture string other than `400V` or `800V`, combined with occupancy below 50%, leaves the 250 kW / 1.0 baseline in place.

### 3. Grid congestion

If grid demand is **above 85%**, or occupancy is **exactly 100%**, the engine halves the power chosen so far and sets the multiplier to **10.0**. Demand of exactly 85% does not trip this rule. Occupancy of 99% does not either, unless demand is already above 85%.

Halving applies on top of a thermal derate. A 50 kW emergency cap becomes 25 kW, and a 350 kW ultra-fast cap becomes 175 kW. The multiplier becomes 10.0 either way, so the vehicle takes the bypass. After this rule, power is a float (`175.0`, `125.0`, `75.0`, `25.0`).

## Worked examples

| °C | Pack | Occupancy | Grid | Power | Multiplier | Path |
| --- | --- | --- | --- | --- | --- | --- |
| 25 | 800V | 50% | 50% | 250 kW | 1.0 | Through `(2, 2)` |
| 30 | 800V | 20% | 40% | 350 kW | 0.5 | Through `(2, 2)` |
| 37 | 400V | 90% | 60% | 250 kW | 1.0 | Through `(2, 2)` |
| 48 | 800V | 20% | 40% | 150 kW | 2.0 | Through `(2, 2)` |
| 80 | 400V | 25% | 70% | 50 kW | 5.0 | Bypass `(2, 1)` |
| 30 | 800V | 20% | 90% | 175 kW | 10.0 | Bypass `(2, 1)` |
| 50 | 400V | 100% | 40% | 75 kW | 10.0 | Bypass `(2, 1)` |

The 48°C row is the warm-pack case: power is cut to 150 kW, and the multiplier of 2.0 is still cheap enough that A* drives through the stall. The last two rows show the grid rule cutting an earlier allocation in half and forcing the detour.

## Map and pathfinding

`run_fleet_router` in `src/router.py` searches a 5×5 grid. Coordinates run from `(0, 0)` to `(4, 4)`. Every launch of `src/main.py` starts at `(0, 2)` and heads for `(4, 2)`.

Column `x = 2` is a wall except for two openings: the Supercharger at `(2, 2)` and the bypass at `(2, 1)`.

```text
        x=0   x=1   x=2   x=3   x=4
y=4      .     .    wall   .     .
y=3      .     .    wall   .     .
y=2      S     .     C     .     G
y=1      .     .     B     .     .
y=0      .     .    wall   .     .
```

`S` is the start, `C` is the charger, `B` is the bypass, and `G` is the goal.

Movement is up, down, left, or right. A normal step costs `1.0`. Stepping onto `(2, 2)` costs `1.0 × multiplier`. The heuristic is Manhattan distance, and the open set is a min-heap of `f = g + h`.

The straight path visits the charger and costs `3 + multiplier`:

```text
(0, 2) → (1, 2) → (2, 2) → (3, 2) → (4, 2)
```

The bypass is six steps and costs `6`:

```text
(0, 2) → (1, 2) → (1, 1) → (2, 1) → (3, 1) → (3, 2) → (4, 2)
```

With the multipliers this engine actually emits:

| Multiplier | Path cost through the charger | Chosen path |
| --- | --- | --- |
| 0.5 | 3.5 | Through the charger |
| 1.0 | 4.0 | Through the charger |
| 2.0 | 5.0 | Through the charger |
| 5.0 | 8.0 | Bypass |
| 10.0 | 13.0 | Bypass |

If no path exists, `run_fleet_router` returns `None`. On this map the bypass is always open, so a route is always found.

When the charger is on the path, the report prints `Vehicle will charge at full capacity of {power}kW` using the kilowatts the rules returned, including a thermal cap such as 150 kW. When the charger is off the path, the report names the `(2, 1)` bypass.

## Calling the modules

`src/main.py` puts its own directory on `sys.path`, so launching that file is enough for the prompts. To call the functions from another script, add `src` yourself:

```python
import sys
sys.path.insert(0, "src")

from engine import evaluate_supercharger_rules
from router import run_fleet_router

power_kw, multiplier = evaluate_supercharger_rules(30, "800V", 20, 40)
route = run_fleet_router((0, 2), (4, 2), multiplier)
```

`evaluate_supercharger_rules` also prints each rule that fires. Pass the architecture as the uppercase string `"400V"` or `"800V"`; the function does not normalize case. `main` does that before the call.

## Project layout

```text
src/main.py        Prompts, runs the rules, prints the routing report
src/engine.py      Thermal, cabinet, and grid rules
src/router.py      A* search with a weighted Supercharger tile
tests/test_rules.py  Placeholder for rule tests (empty)
requirements.txt   Notes that the standard library is sufficient
```
