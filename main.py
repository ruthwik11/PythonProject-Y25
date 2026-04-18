"""
DTL-RO — Dynamic Transport Logistics and Route Optimization Tool
Main program: load data, optimize routes, print results, analytics, optional map.
"""
from __future__ import annotations

from pathlib import Path

import folium

from data.file_handler import load_orders_csv, load_vehicles_json, save_summary_csv
from data.sample_data import default_orders, default_vehicles
from planner.metrics import (
    distances_summary,
    print_summary_table,
    routes_to_dataframe,
    save_vehicle_distance_line_chart,
)
from planner.route_optimizer import optimize_routes

# Set True to pop up the matplotlib window (like the report screenshot).
SHOW_MATPLOTLIB_WINDOW = True


def load_problem_data():
    """Try CSV/JSON under data/; fall back to built-in sample if files are missing."""
    data_dir = Path(__file__).resolve().parent / "data"
    try:
        orders = load_orders_csv(data_dir / "orders.csv")
        vehicles = load_vehicles_json(data_dir / "vehicles.json")
        print("Loaded orders from data/orders.csv and vehicles from data/vehicles.json")
    except (FileNotFoundError, ValueError) as e:
        print(f"Using built-in sample data ({e})")
        orders = default_orders()
        vehicles = default_vehicles()
    return orders, vehicles


def print_route_output(routes: dict, total_distance: float) -> None:
    """Console layout aligned with the project report / screenshot style."""
    print("\nROUTE OPTIMIZATION OUTPUT\n")
    for v_id, data in routes.items():
        # str(list) matches report style: ['O1', 'O2', 'O3']
        print(f"{v_id} -> {data['orders']} | Distance: {data['distance']}")
        print()
    print(f"Total Distance: {total_distance:.2f}")


def save_simple_map(orders, html_path: Path) -> Path | None:
    """Very small Folium demo: markers for each order (creates reports/map.html)."""
    if not orders:
        return None
    avg_x = sum(o.location[0] for o in orders) / len(orders)
    avg_y = sum(o.location[1] for o in orders) / len(orders)
    # Folium expects lat-lon; our model uses abstract x,y — treat as plot coordinates.
    fmap = folium.Map(location=[avg_y, avg_x], zoom_start=6)
    for o in orders:
        folium.Marker([o.location[1], o.location[0]], tooltip=o.id).add_to(fmap)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    fmap.save(str(html_path))
    return html_path


def main() -> None:
    orders, vehicles = load_problem_data()

    routes, total_distance, unassigned = optimize_routes(orders, vehicles)

    print_route_output(routes, total_distance)

    if unassigned:
        leftover = ", ".join(o.id for o in unassigned)
        print(f"\nNote: could not assign all orders (capacity limit): {leftover}\n")

    # --- Analytics (NumPy + pandas + Matplotlib) ---
    dist_list = [routes[v]["distance"] for v in routes]
    stats = distances_summary(dist_list)
    print("\n--- NUMPY STATS ---")
    print(f"Mean vehicle distance: {stats['mean_distance']:.2f}")
    print(f"Max vehicle distance:  {stats['max_distance']:.2f}")

    df = routes_to_dataframe(routes)
    print_summary_table(df)

    reports_dir = Path(__file__).resolve().parent / "reports"
    csv_path = reports_dir / "route_summary.csv"
    save_summary_csv(csv_path, df.to_dict(orient="records"))
    print(f"\nSaved summary CSV: {csv_path}")

    chart_path = save_vehicle_distance_line_chart(
        routes, show_window=SHOW_MATPLOTLIB_WINDOW
    )
    print(f"Saved chart image: {chart_path}")

    map_path = save_simple_map(orders, reports_dir / "map.html")
    if map_path:
        print(f"Saved map: {map_path}")


if __name__ == "__main__":
    main()
