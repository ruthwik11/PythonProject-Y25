"""
Minimal FastAPI demo for the academic project.

Run from the `dtl-ro` folder:
    uvicorn api.simple_api:app --reload
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from data.file_handler import load_orders_csv, load_vehicles_json
from data.sample_data import default_orders, default_vehicles
from planner.route_optimizer import optimize_routes

app = FastAPI(title="DTL-RO Demo API", version="1.0")


def _load_and_solve():
    data_dir = Path(__file__).resolve().parent.parent / "data"
    try:
        orders = load_orders_csv(data_dir / "orders.csv")
        vehicles = load_vehicles_json(data_dir / "vehicles.json")
    except (FileNotFoundError, ValueError):
        orders = default_orders()
        vehicles = default_vehicles()
    routes, total_distance, unassigned = optimize_routes(orders, vehicles)
    return {
        "orders": [{"id": o.id, "x": o.location[0], "y": o.location[1], "weight": o.weight} for o in orders],
        "vehicles": [
            {"id": v.id, "capacity": v.capacity, "start": v.start_location} for v in vehicles
        ],
        "routes": routes,
        "total_distance": total_distance,
        "unassigned_order_ids": [o.id for o in unassigned],
    }


_CACHE = _load_and_solve()


@app.get("/orders")
def get_orders():
    return {"orders": _CACHE["orders"]}


@app.get("/vehicles")
def get_vehicles():
    return {"vehicles": _CACHE["vehicles"]}


@app.get("/routes")
def get_routes():
    return {
        "routes": _CACHE["routes"],
        "total_distance": _CACHE["total_distance"],
        "unassigned_order_ids": _CACHE["unassigned_order_ids"],
    }
