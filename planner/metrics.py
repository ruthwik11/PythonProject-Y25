"""
Analytics: NumPy statistics, pandas summary table, Matplotlib chart (saved under reports/).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def distances_summary(distances: list[float]) -> dict[str, float]:
    """Use NumPy for simple aggregate stats (mean and max distance)."""
    arr = np.array(distances, dtype=float)
    return {
        "mean_distance": float(np.mean(arr)),
        "max_distance": float(np.max(arr)),
    }


def routes_to_dataframe(routes: dict) -> pd.DataFrame:
    """Build a readable pandas table for console / export."""
    rows = []
    for vid, data in routes.items():
        rows.append(
            {
                "vehicle_id": vid,
                "order_ids": ",".join(data["orders"]),
                "distance": data["distance"],
                "load_used": data["load_used"],
            }
        )
    return pd.DataFrame(rows)


def save_vehicle_distance_line_chart(
    routes: dict,
    outfile: str | Path | None = None,
    title: str = "Vehicle Distance - Line Chart",
    show_window: bool = False,
) -> Path:
    """
    Green line chart with markers — similar to the project report screenshot.
    Saves PNG into reports/ and returns the path.
    """
    base = Path(__file__).resolve().parent.parent / "reports"
    base.mkdir(parents=True, exist_ok=True)
    path = Path(outfile) if outfile else base / "vehicle_distance_chart.png"

    vehicles = list(routes.keys())
    distances = [routes[v]["distance"] for v in vehicles]

    plt.figure(figsize=(8, 5))
    plt.plot(vehicles, distances, color="green", marker="o", linewidth=2)
    plt.title(title)
    plt.xlabel("Vehicles")
    plt.ylabel("Distance")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    if show_window:
        plt.show()
    plt.close()
    return path


def print_summary_table(df: pd.DataFrame) -> None:
    """Pretty-print the pandas summary (good for demos / reports)."""
    print("\n--- SUMMARY TABLE (pandas) ---")
    print(df.to_string(index=False))
