"""
Sample domain classes for DTL-RO.

Uses simple inheritance: a base class holds a common id field;
Order and Vehicle extend it with their own fields.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LogisticsEntity:
    """Base class for things that appear in routing (orders, vehicles, etc.)."""

    id: str


@dataclass
class Order(LogisticsEntity):
    """A delivery order with a 2D location and weight."""

    location: tuple[float, float]  # (x, y) for Euclidean distance
    weight: float


@dataclass
class Vehicle(LogisticsEntity):
    """A vehicle with capacity and a starting point for routes."""

    capacity: float
    start_location: tuple[float, float]


def default_orders() -> list[Order]:
    """Same demo data as the academic report / main example."""
    return [
        Order("O1", (2.0, 3.0), 2.0),
        Order("O2", (5.0, 7.0), 3.0),
        Order("O3", (1.0, 8.0), 1.0),
        Order("O4", (6.0, 2.0), 4.0),
        Order("O5", (3.0, 6.0), 2.0),
    ]


def default_vehicles() -> list[Vehicle]:
    """Two vehicles starting at origin — matches the sample in the report."""
    return [
        Vehicle("V1", 6.0, (0.0, 0.0)),
        Vehicle("V2", 6.0, (0.0, 0.0)),
    ]
