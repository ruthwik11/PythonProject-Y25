"""
Simple route optimization: Euclidean distance + nearest neighbor + capacity check.

This follows the same idea as the report's sample main.py, but kept in one module.
"""
from __future__ import annotations

import math
from typing import Any

from data.sample_data import Order, Vehicle


def calculate_distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Straight-line (Euclidean) distance between two points."""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def nearest_neighbor_route(
    start: tuple[float, float], orders: list[Order]
) -> list[Order]:
    """Order stops by always going to the nearest not-yet-visited location."""
    route: list[Order] = []
    current = start
    remaining = orders.copy()
    while remaining:
        next_order = min(remaining, key=lambda o: calculate_distance(current, o.location))
        route.append(next_order)
        current = next_order.location
        remaining.remove(next_order)
    return route


def optimize_routes(
    orders: list[Order], vehicles: list[Vehicle]
) -> tuple[dict[str, dict[str, Any]], float, list[Order]]:
    """
    Greedy assignment: sort orders by weight (heavy first), fill each vehicle,
    then apply nearest-neighbor sequencing for that vehicle's stops.

    Returns:
        routes dict per vehicle id,
        total distance,
        list of orders that could not be assigned (capacity overflow).
    """
    routes: dict[str, dict[str, Any]] = {}
    total_distance = 0.0

    # Copy so we can remove assigned orders without touching the caller's list
    pending = sorted(orders, key=lambda o: o.weight, reverse=True)
    unassigned: list[Order] = []

    for vehicle in vehicles:
        assigned_orders: list[Order] = []
        remaining_capacity = vehicle.capacity

        for order in pending[:]:
            if order.weight <= remaining_capacity:
                assigned_orders.append(order)
                remaining_capacity -= order.weight
                pending.remove(order)

        optimized_route = nearest_neighbor_route(vehicle.start_location, assigned_orders)

        distance = 0.0
        current = vehicle.start_location
        for order in optimized_route:
            distance += calculate_distance(current, order.location)
            current = order.location

        routes[vehicle.id] = {
            "orders": [o.id for o in optimized_route],
            "distance": round(distance, 2),
            "load_used": round(vehicle.capacity - remaining_capacity, 2),
        }
        total_distance += distance

    # Anything left did not fit — educational projects often report this clearly
    unassigned.extend(pending)

    return routes, round(total_distance, 2), unassigned
