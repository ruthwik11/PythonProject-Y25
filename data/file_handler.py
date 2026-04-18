"""
Load and save orders/vehicles using CSV and JSON (file handling + exceptions).
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from data.sample_data import Order, Vehicle


def _project_root() -> Path:
    return Path(__file__).resolve().parent


def load_orders_csv(path: str | Path | None = None) -> list[Order]:
    """
    Read orders from CSV: columns id, x, y, weight
    """
    csv_path = Path(path) if path else _project_root() / "orders.csv"
    try:
        df = pd.read_csv(csv_path)
        df.columns = [str(c).lower().strip() for c in df.columns]
        required = {"id", "x", "y", "weight"}
        if not required.issubset(df.columns):
            raise ValueError(f"orders.csv must have columns: {required}")
        orders = []
        for _, row in df.iterrows():
            oid = str(row["id"]).strip()
            orders.append(
                Order(oid, (float(row["x"]), float(row["y"])), float(row["weight"]))
            )
        return orders
    except FileNotFoundError:
        raise FileNotFoundError(f"Orders file not found: {csv_path}") from None
    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"Could not parse orders CSV: {e}") from e


def load_vehicles_json(path: str | Path | None = None) -> list[Vehicle]:
    """
    Read vehicles from JSON list:
    [{"id": "V1", "capacity": 6, "start_x": 0, "start_y": 0}, ...]
    """
    json_path = Path(path) if path else _project_root() / "vehicles.json"
    try:
        text = json_path.read_text(encoding="utf-8")
        raw = json.loads(text)
        if not isinstance(raw, list):
            raise ValueError("vehicles.json must contain a JSON list")
        vehicles = []
        for item in raw:
            vid = str(item["id"])
            cap = float(item["capacity"])
            sx = float(item["start_x"])
            sy = float(item["start_y"])
            vehicles.append(Vehicle(vid, cap, (sx, sy)))
        return vehicles
    except FileNotFoundError:
        raise FileNotFoundError(f"Vehicles file not found: {json_path}") from None
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        raise ValueError(f"Could not parse vehicles JSON: {e}") from e


def save_summary_csv(filepath: Path, rows: list[dict]) -> None:
    """Optional: save a small pandas summary table for the report folder."""
    df = pd.DataFrame(rows)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
