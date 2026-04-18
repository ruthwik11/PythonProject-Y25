DTL-RO — Dynamic Transport Logistics and Route Optimization Tool

Team Details

****2500030291 → B. JYOTHI SRI**

**2500030037 → P. SAI RUTHWIK**

**2500010002 → B. PRAVEEN VIJAY****

Project Brief 

DTL-RO is a university mini project developed to improve transportation and delivery planning.
The system assigns customer orders to available vehicles based on carrying capacity.
It calculates optimized routes using Euclidean distance and nearest neighbor logic.
The project helps reduce travel distance, delivery time, and transport cost.
It generates route summaries, charts, and map outputs for analysis.
The system also includes a simple API to access orders, vehicles, and routes.
It demonstrates practical use of Python for real-world logistics problems.

Modules Used in Project
1. Main Module (main.py)

This is the starting point of the project execution.
It loads all order and vehicle data from files.
It calls planner functions to optimize routes.
It displays output in console format as per report.
It also triggers chart and report generation.

2. API Module (api/simple_api.py)

This module provides a basic FastAPI web interface.
It allows users to view orders through API endpoints.
It provides vehicle data using browser requests.
It can display optimized route results in JSON format.
It shows how backend APIs work in Python projects.

3. Planner Module (planner/route_optimizer.py)

This is the core logic module of the project.
It assigns orders to vehicles using capacity limits.
It uses nearest neighbor for route generation.
It calculates travel distance between locations.
It returns optimized route plans for all vehicles.

4. Metrics Module (planner/metrics.py)

This module analyzes generated route results.
It calculates total distance and average values.
It creates summary tables using pandas.
It generates charts using matplotlib.
It saves reports for future reference.

5. Data Module (data/sample_data.py)

This module stores sample order and vehicle classes.
It demonstrates classes and inheritance concepts.
It creates reusable logistics objects.
It organizes order and vehicle information neatly.
It improves code structure and readability.

6. File Handling Module (data/file_handler.py)

This module reads CSV and JSON files.
It loads orders and vehicles into the system.
It handles missing file errors safely.
It saves generated outputs when required.
It demonstrates exception handling concepts.

Python Libraries Installed
NumPy

Used for mathematical calculations and statistics.
Helps find mean distance and max values.
Useful for numerical operations in analytics.
Fast and efficient for arrays.
Widely used in data science.

Pandas

Used to create tables and summary reports.
Converts route results into DataFrame format.
Exports output to CSV files.
Makes data easy to analyze.
Useful for structured datasets.

Matplotlib

Used to generate graphs and charts.
Creates vehicle distance line chart.
Helps visualize performance clearly.
Saves charts as PNG files.
Useful for project output screenshots.

FastAPI

Used to create simple web APIs.
Provides routes like /orders and /vehicles.
Returns JSON responses quickly.
Easy to learn and lightweight.
Modern Python backend framework.

Folium

Used to generate route map output.
Creates interactive HTML maps.
Marks order locations visually.
Useful for logistics route display.
Easy integration with Python.

JSON / CSV Modules

Used for file storage and reading.
Stores vehicle and order records.
Simple format for mini projects.
Easy to edit manually.
Useful for persistence.

Final Note

This project is designed at  balanced logic, practical concepts, modular coding structure, and real-world application in transport optimization.
