# UAV Strategic Deconfliction System

This project is a drone airspace safety checker designed for FlytBase's Robotics Engineer Technical Assessment. It simulates multiple drones operating in shared airspace and determines whether a new drone mission is safe to execute — checking for spatial and temporal conflicts with other drones.

## 🚀 Features

- Supports 3D space + time (4D) mission conflict detection
- Interpolates drone paths to check continuous movement, not just waypoints
- Identifies spatial conflicts (within minimum distance)
- Detects temporal overlaps using timestamps
- Visualizes drone trajectories and conflicts
- Scalable and modular architecture

## 📁 Project Structure
Overview
This system serves as a strategic deconfliction service for validating whether a drone's planned waypoint mission is safe to execute in shared airspace. It checks for conflicts in both space and time against the simulated flight paths of multiple other drones.

Key Features
Spatial Conflict Detection: Validates that the primary mission's path does not intersect with any other drone's trajectory within a defined safety buffer.
Temporal Conflict Detection: Ensures that, within the overall mission window, no other drone is present in the same spatial area during overlapping time segments.
Detailed Conflict Information: When conflicts are detected, the system provides detailed information about the location, time, and involved drones.
2D and 3D Visualization: Visually depicts the primary drone's mission, trajectories of other drones, and highlights conflicts.
How to Use
Define the primary mission by specifying waypoints and a time window.
Add other drone missions, each with waypoints and associated timestamps.
Click "Run Check" to analyze the mission for conflicts.
View the visualization and conflict details to understand any detected issues.
Use the "Load Test Case" button to explore predefined scenarios.
System Design
The deconfliction system employs a modular architecture with the following components:

Conflict Detection Engine: Performs spatial and temporal checks on mission data.
Visualization Module: Generates 2D and 3D representations of missions and conflicts.
Test Case Repository: Provides sample scenarios for exploring different conflict situations.
Web Interface: Allows intuitive interaction with the system.
Scalability Considerations
For a real-world deployment handling tens of thousands of commercial drones, the system would need significant enhancements:

Spatial Partitioning: Using structures like octrees or R-trees to optimize spatial queries.
Distributed Computing: Parallelizing conflict detection across multiple nodes.
Real-time Data Ingestion: Building pipelines for handling continuous drone position updates.
Caching and Indexing: Optimizing database access for trajectory information.
Advanced Algorithms: Implementing more sophisticated conflict prediction methods.

## ▶️ How to Run

1. Open `main.py`
2. Set a primary drone mission
3. Choose a test case (conflict / no conflict)
4. Run the script to:
   - Check for conflicts
   - Print results
   - Show a plot (optional)

## 📦 Requirements

- Python 3.8+
- `matplotlib`, `numpy`

Install using:
```bash
pip install -r requirements.txt


---

## 🧠 Reflection Document

```markdown
# UAV Deconfliction System – Reflection

## ✍️ Design Decisions

My goal was to create a modular, simulation-based safety system that evaluates whether drone missions are safe to run in busy airspace. I structured the project with a clean separation:
- `main.py` handles I/O and test case control
- `deconfliction_system.py` holds the core logic
- `visualization.py` helps to explain and debug
- `test_cases.py` helps verify against known conflict scenarios

I chose Python for flexibility and readability, and used `matplotlib` for rapid 2D/3D plotting.

## 🧠 Conflict Detection Logic

Instead of comparing waypoints directly, I used **interpolation** to simulate the drone's motion between points. Each trajectory is processed into many `(x, y, z, t)` samples.

Then, for each moment in time, I compare the **Euclidean distance** between drones:
- In 3D space
- At the same or close timestamps (±1 second)

If the distance drops below a threshold (2 meters), a conflict is logged.

## 🤖 How AI Helped

I used Replit AI and ChatGPT during the project to:
- Refactor logic and improve modularity
- Quickly build the interpolation algorithm
- Debug corner cases and incorrect results
- Generate base templates for README and reflection

AI accelerated development but I always reviewed the code line-by-line to ensure it met the specific requirements and handled edge cases like altitude-only overlaps.

## 🌍 Scaling to 10,000+ Drones

To scale this system:
- Replace nested loops with **spatial indexing** (like R-Trees or KD-Trees)
- Use **distributed computing** (Ray, Dask) to parallelize conflict checks
- Stream real-time data using Kafka or MQTT
- Use **zone-based caching** to ignore far-away drones
- Store missions in a spatial database (PostGIS or MongoDB with GeoJSON)

With these changes, the system could realistically manage tens of thousands of drones in real-time airspace.

