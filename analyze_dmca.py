#!/usr/bin/env python3
"""
Baseline analyzer for DMCA / Lumen-style notice CSV exports.

Part of an exploratory research toolkit for studying abusive or false
DMCA complaint patterns. This script is intentionally simple: load CSV,
summarize, and plot a few charts.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


REQUIRED_HINTS = ("date_received", "sender")


def load_notices(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    missing = [c for c in REQUIRED_HINTS if c not in df.columns]
    if missing:
        raise SystemExit(
            f"CSV is missing required columns: {', '.join(missing)}\n"
            f"Found columns: {', '.join(df.columns)}"
        )

    df["date_received"] = pd.to_datetime(df["date_received"], errors="coerce")
    df = df.dropna(subset=["date_received"]).copy()
    df["sender"] = df["sender"].fillna("[unknown]").astype(str)
    if "sender_country" in df.columns:
        df["sender_country"] = df["sender_country"].fillna("??").astype(str)
    if "role" in df.columns:
        df["role"] = df["role"].fillna("unspecified").astype(str)
    return df


def print_summary(df: pd.DataFrame) -> None:
    print("=== DMCA notice summary ===")
    print(f"Rows:              {len(df)}")
    print(f"Date range:        {df['date_received'].min().date()} → {df['date_received'].max().date()}")
    print(f"Unique senders:    {df['sender'].nunique()}")
    if "sender_country" in df.columns:
        print(f"Unique countries:  {df['sender_country'].nunique()}")
    if "target_domain" in df.columns:
        print(f"Unique domains:    {df['target_domain'].nunique()}")
    if "role" in df.columns:
        print("\nRole breakdown:")
        print(df["role"].value_counts().to_string())
    print("\nTop senders:")
    print(df["sender"].value_counts().head(10).to_string())


def plot_notices_over_time(df: pd.DataFrame, outdir: Path) -> Path:
    daily = df.set_index("date_received").resample("D").size()
    fig, ax = plt.subplots(figsize=(10, 4))
    daily.plot(ax=ax, color="#1f4e79", linewidth=1.8)
    ax.set_title("DMCA notices over time")
    ax.set_xlabel("Date received")
    ax.set_ylabel("Notices per day")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = outdir / "notices_over_time.png"
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_top_senders(df: pd.DataFrame, outdir: Path, top_n: int = 10) -> Path:
    counts = df["sender"].value_counts().head(top_n).sort_values()
    fig, ax = plt.subplots(figsize=(9, 5))
    counts.plot(kind="barh", ax=ax, color="#c45c26")
    ax.set_title(f"Top {top_n} notice senders")
    ax.set_xlabel("Number of notices")
    ax.set_ylabel("Sender")
    fig.tight_layout()
    path = outdir / "top_senders.png"
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_countries(df: pd.DataFrame, outdir: Path, top_n: int = 10) -> Path | None:
    if "sender_country" not in df.columns:
        return None
    counts = df["sender_country"].value_counts().head(top_n)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    counts.plot(kind="bar", ax=ax, color="#2f6f4e", rot=0)
    ax.set_title(f"Top {top_n} sender countries")
    ax.set_xlabel("Country code")
    ax.set_ylabel("Number of notices")
    fig.tight_layout()
    path = outdir / "sender_countries.png"
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze a CSV of DMCA/Lumen notices and write baseline charts."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("sample_data/dmca_notices_sample.csv"),
        help="Path to notices CSV",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("output"),
        help="Directory for generated charts",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input CSV not found: {args.input}")

    args.outdir.mkdir(parents=True, exist_ok=True)
    df = load_notices(args.input)
    print_summary(df)

    written = [
        plot_notices_over_time(df, args.outdir),
        plot_top_senders(df, args.outdir),
    ]
    country_chart = plot_countries(df, args.outdir)
    if country_chart:
        written.append(country_chart)

    print("\nCharts written:")
    for path in written:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
