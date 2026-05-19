# Building a Rule-Based AI System with Python project

## Part 1: Initial Project Ideas

### 1. Project Idea 1: Retro Video Game Finder
* **What it does:** It acts as a digital clerk at a 90s game store, asking the user a few targeted questions to recommend the perfect classic video game to play next.
* **How it works using rules:** It maps specific combinations of preferences (genre, platform, era, difficulty) directly to a database of titles.
    * **Example:** IF preferred_genre is "RPG" AND era is "16-bit" AND difficulty is "Hard," THEN recommend Chrono Trigger. IF preferred_genre is "Platformer" AND vibe is "Casual," THEN recommend Kirby's Adventure.

### 2. Project Idea 2: Automated Personal Finance Copilot
* **What it does:** A text-based assistant that takes a user's basic financial inputs (monthly income, rent, food expenses) and provides instant, rule-based budgeting critiques and tailored savings advice.
* **How it works using rules:** It calculates simple ratios and passes them through a heuristic threshold script.
    * **Example:** IF rent_expense is greater than 50% of monthly_income, THEN output a "High Housing Burden Warning" with a tip on finding roommates. IF savings_rate is less than 10%, THEN trigger the "Emergency Fund Alert" routine.

### 3. Project Idea 3: Tesla Supercharger V4 Thermal Balancing & Fleet Router

* **What it does:** Simulates an integrated edge-computing and fleet routing architecture. The system co-optimizes high-voltage charging station resource allocation (managing 400V legacy packs vs. newer 800V architectures) and real-time vehicle navigation across a coordinate map. By linking asset telemetry directly to pathfinding, it dynamically reroutes vehicles to protect battery health and prevent local grid overloads.
* **How it works using rules:** The system captures live vehicle metrics and station environmental data, processing them through a cascading sequence of if-elif-else conditional rules. Instead of simply throttling station power in a vacuum, these rules simultaneously calculate a dynamic "node cost multiplier." This multiplier feeds directly into the terrain traversal metrics (g-costs) of an integrated A* pathfinding algorithm. When station states are dangerous or congested, the rules spike the multiplier, mathematically forcing the A* engine to recalculate and guide the vehicle along a physical detour lane.
    * **Example:** IF battery_temp > 55°C, THEN throttle allocated charging power to a safe 50kW AND scale the A^* node cost multiplier to 5.0. ELIF voltage_arch == "800V" AND occupancy_rate < 50%, THEN allocate ultra-fast 350kW charging lanes AND drop the A^* node cost multiplier to 0.5. IF grid_demand > 85% OR occupancy_rate == 100%, THEN scale down calculated power output by 50% AND maximize the A^* node cost multiplier to 10.0. 

### Chosen Idea: 
**Justification:** I chose the Tesla Supercharger V4 Thermal Balancing & Fleet Router because it perfectly demonstrates how classic, deterministic rule engines are used in real-world autonomous systems to enforce hardware safety limits. By integrating a rule-based system with the A* pathfinding algorithm, this project explores how safety thresholds can dynamically alter routing decisions on a coordinate grid. This mimics the actual software architecture utilized by leading EV and autonomous driving companies like Tesla.

## Part 2: Rules/Logic for the Chosen System

The **Tesla Supercharger V4 Thermal Balancing & Fleet Router** will follow these rules:

### **RULE SET 1: THERMAL SAFETY GUARDRAILS (Highest Priority)**
IF battery_temp > 55°C THEN
allocated_ power = 50 kW
(Emergency Derate)
node _cost multiplier = 3.0
(Avoid
station due to long cooling delay)
ELIF battery_temp > 45°C THEN
allocated power = 150 km
(Throttled Charging)
node_cost multiplier = 1.5 (Minor
delay penalty)

### **RULE SET 2: ARCHITECTURE & POWER
CABINET ALLOCATION**
ELSE
IF voltage_arch == "800V" AND
occupancy_rate ‹ 50% THEN
allocated_ power = 350 kw
(Ultra-Fast Charging)
node_cost multiplier = 0.8
(Highly optimal path node)
ELIF voltage_arch == "400V" OR
occupancy rate ›= 50% THEN
allocated_power = 250 kw
(Standard Fast Charging)
node_cost_ multiplier = 1.0
(Neutral path node)

### **RULE SET 3: GRID CONGESTION OVERRIDES**
IF grid_demand > 85%
OR occupancy_rate
== 100% THEN
allocated_power = allocated_power
* 0.5 (Force Grid-Saving Throttling)
(Station cost multiplier = 5.0
congested; A* should steer
around it)

## Part 3: Code Inputs/Outputs

**Input 1**
vehicle battery temperature in Celsius: 25
vehicle architecture type: 800V
station occupancy percentage: 50
local grid stress/demand percentage: 50
**Output 1**
Power Allocated: 250kw
A* Cost Multiplier: 1.0

**Input 2**
vehicle battery temperature in Celsius: 80
vehicle architecture type: 400V 
station occupancy percentage: 25
local grid stress/demand percentage: 70
**Output 2**
Power Allocated: 50kw
A* Cost Multiplier: 5.0

**Input 3**
vehicle battery temperature in Celsius: 37
vehicle architecture type: 400V
station occupancy percentage: 90
local grid stress/demand percentage: 60
**Output 3**
Power Allocated: 250kw 
A* Cost Multiplier: 1.0

## Part 4: Reflection

### Project Overview:

The developed rule-based expert system operates as an intelligent telemetry layer that directly bridges physical vehicle states with a mathematical navigation algorithm (A*). Utilizing a cascading series of deterministic if-elif-else conditional logic blocks, the system evaluates four real-time sensor inputs: vehicle battery temperature, voltage architecture (400V vs. 800V), charging station occupancy, and local grid demand.
Instead of operating in isolation, the expert system outputs two crucial variables: a dynamic power allocation cap (in kW) and a "node cost multiplier." This multiplier acts as the operational language translation to the A* pathfinder. When conditions are optimal, a low multiplier (0.5) incentivizes the vehicle to route straight through the Supercharger node. However, when safety thresholds are crossed such as an extreme battery temperature spike to 80°C, the rule engine drastically inflates the node cost multiplier (to 5.0 or 10.0). Even though the physical coordinates remain identical, the pathfinder mathematically interprets the station as a massive traffic jam, forcing the vehicle to bypass the charger and divert along a longer, safer alternate detour lane to prioritize battery thermal health and infrastructure preservation.

### Challenges:

Collaborating with an AI to design and build this modular architecture was highly educational, though it introduced unique environment configuration challenges. As a first-time user of Linux tools on Windows, navigating the Ubuntu command line and Windows Subsystem for Linux (WSL) presented an initial learning curve. For instance, when first trying to open the project directory in the IDE using the terminal command code ., the subsystem threw an intimidating Exec format error due to a dropped interop boundary between Windows and Linux. The AI successfully troubleshot this by guiding me through a hard WSL shutdown and system reset to restore terminal communication.
Furthermore, a major technical hurdle occurred when establishing the development environment. I initially allowed the IDE to default to my local Windows environment, downloading python tools via uv on the host side, while the source code files lived entirely within the isolated Ubuntu filesystem. This resulted in broken extension paths, missing interpreter flags, and warning lines all over the clean script. The AI helped me untangle this environment confusion by demonstrating how to reopen the project folder explicitly inside the WSL container, install the Python extension directly into the Ubuntu sandbox, and map the path directly to the internal Linux binary (/usr/bin/python3). This cleared the environment blocks and allowed the modular multi-file system to run seamlessly.