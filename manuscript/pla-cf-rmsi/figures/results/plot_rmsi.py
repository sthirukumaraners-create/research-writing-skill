"""
Figure 1 and Figure 2 for the PLA-CF RMSI screening article.
Data: nine measured strengths supplied with the manuscript record.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "figures" / "data"
OUT = Path(__file__).resolve().parent

COLORS = ["#0077BB", "#EE7733", "#009988"]
MAXIMIN_COLOR = "#CC3311"

ROWS = [
    (1, 0.1, 30, 0, 41.20, 53.20, 86.80),
    (2, 0.1, 45, 45, 30.75, 62.60, 78.70),
    (3, 0.1, 60, 90, 20.50, 55.60, 55.40),
    (4, 0.2, 30, 45, 23.50, 62.80, 69.60),
    (5, 0.2, 45, 90, 16.70, 55.10, 59.40),
    (6, 0.2, 60, 0, 31.00, 69.70, 56.20),
    (7, 0.3, 30, 90, 23.60, 63.30, 52.30),
    (8, 0.3, 45, 0, 18.10, 47.80, 44.00),
    (9, 0.3, 60, 45, 19.70, 45.90, 30.00),
]


def sample_std(values):
    values = np.asarray(values, dtype=float)
    mean = values.mean()
    return float(np.sqrt(np.sum((values - mean) ** 2) / (len(values) - 1)))


def build_tables():
    frame = pd.DataFrame(
        ROWS, columns=["run", "layer_mm", "speed_mm_s", "raster_deg", "tensile_MPa", "compressive_MPa", "flexural_MPa"]
    )
    responses = ["tensile_MPa", "compressive_MPa", "flexural_MPa"]
    limits = {}
    for column in responses:
        limits[column] = (float(frame[column].min()), float(frame[column].max()))
        span = limits[column][1] - limits[column][0]
        frame[column.replace("_MPa", "_norm")] = (frame[column] - limits[column][0]) / span

    norm_cols = ["tensile_norm", "compressive_norm", "flexural_norm"]
    frame["RMSI"] = 100.0 * frame[norm_cols].mean(axis=1)
    frame["maximin"] = frame[norm_cols].min(axis=1)
    frame["maximin_x100"] = 100.0 * frame["maximin"]

    summary_rows = []
    for column in responses:
        values = frame[column].to_numpy()
        summary_rows.append(
            {
                "response": column.replace("_MPa", ""),
                "min": values.min(),
                "max": values.max(),
                "range": values.max() - values.min(),
                "mean": values.mean(),
                "std_sample": sample_std(values),
                "n_runs": len(values),
            }
        )
    summary = pd.DataFrame(summary_rows)

    level_rows = []
    for factor, levels in (
        ("layer_mm", [0.1, 0.2, 0.3]),
        ("speed_mm_s", [30, 45, 60]),
        ("raster_deg", [0, 45, 90]),
    ):
        for level in levels:
            subset = frame[frame[factor] == level]
            level_rows.append(
                {
                    "factor": factor,
                    "level": level,
                    "n": len(subset),
                    "mean_tensile_MPa": subset["tensile_MPa"].mean(),
                    "mean_compressive_MPa": subset["compressive_MPa"].mean(),
                    "mean_flexural_MPa": subset["flexural_MPa"].mean(),
                    "mean_RMSI": subset["RMSI"].mean(),
                    "mean_maximin": subset["maximin"].mean(),
                }
            )
    levels = pd.DataFrame(level_rows)

    DATA.mkdir(parents=True, exist_ok=True)
    frame.to_csv(DATA / "rmsi_scores.csv", index=False, float_format="%.6f")
    summary.to_csv(DATA / "response_dispersion.csv", index=False, float_format="%.6f")
    levels.to_csv(DATA / "factor_level_means.csv", index=False, float_format="%.6f")
    return frame, summary, levels


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#D0D0D0", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=3.5, width=0.6)


def plot_scores(frame):
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.15), constrained_layout=True)
    x = np.arange(len(frame))
    width = 0.24
    labels = ["Tensile", "Compressive", "Flexural"]
    columns = ["tensile_norm", "compressive_norm", "flexural_norm"]
    ax = axes[0]
    for offset, column, label, color in zip((-width, 0, width), columns, labels, COLORS):
        ax.bar(x + offset, frame[column], width=width, color=color, label=label, edgecolor="white", linewidth=0.4)
    style_axes(ax)
    ax.set_xticks(x)
    ax.set_xticklabels([str(int(v)) for v in frame["run"]])
    ax.set_xlabel("Run")
    ax.set_ylabel("Min-max normalized strength")
    ax.set_ylim(0, 1.08)
    ax.legend(frameon=False, ncol=3, loc="upper right", bbox_to_anchor=(1.0, 1.18))
    ax.text(-0.12, 1.12, "a", transform=ax.transAxes, fontsize=11, fontweight="bold")

    ax = axes[1]
    layer_colors = {0.1: COLORS[0], 0.2: COLORS[1], 0.3: COLORS[2]}
    bar_colors = [layer_colors[v] for v in frame["layer_mm"]]
    ax.bar(x, frame["RMSI"], color=bar_colors, edgecolor="white", linewidth=0.4, label="RMSI")
    ax.plot(
        x,
        frame["maximin_x100"],
        color=MAXIMIN_COLOR,
        marker="o",
        markersize=4.5,
        linewidth=1.2,
        label="Maximin x 100",
    )
    style_axes(ax)
    ax.set_xticks(x)
    ax.set_xticklabels([str(int(v)) for v in frame["run"]])
    ax.set_xlabel("Run")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, loc="upper right")
    ax.text(-0.12, 1.12, "b", transform=ax.transAxes, fontsize=11, fontweight="bold")
    fig.savefig(OUT / "figure1_rmsi_scores.png", dpi=450)
    fig.savefig(OUT / "figure1_rmsi_scores.svg")
    plt.close(fig)


def plot_main_effects(levels):
    fig, axes = plt.subplots(1, 3, figsize=(6.9, 2.7), sharey=True, constrained_layout=True)
    specs = [
        ("layer_mm", "Layer thickness (mm)", [0.1, 0.2, 0.3], ["0.1", "0.2", "0.3"]),
        ("speed_mm_s", "Printing speed (mm/s)", [30, 45, 60], ["30", "45", "60"]),
        ("raster_deg", "Raster angle (deg)", [0, 45, 90], ["0", "45", "90"]),
    ]
    for ax, (factor, xlabel, level_values, ticklabels), panel in zip(axes, specs, ("a", "b", "c")):
        subset = levels[levels["factor"] == factor].set_index("level").loc[level_values]
        ax.plot(np.arange(len(level_values)), subset["mean_RMSI"], color=COLORS[0], marker="o", linewidth=1.4)
        style_axes(ax)
        ax.set_xticks(np.arange(len(level_values)))
        ax.set_xticklabels(ticklabels)
        ax.set_xlabel(xlabel)
        ax.set_ylim(0, 80)
        ax.text(-0.16, 1.08, panel, transform=ax.transAxes, fontsize=11, fontweight="bold")
    axes[0].set_ylabel("Mean RMSI")
    fig.savefig(OUT / "figure2_rmsi_main_effects.png", dpi=450)
    fig.savefig(OUT / "figure2_rmsi_main_effects.svg")
    plt.close(fig)


def main():
    frame, summary, levels = build_tables()
    plot_scores(frame)
    plot_main_effects(levels)
    print(frame[["run", "tensile_norm", "compressive_norm", "flexural_norm", "RMSI", "maximin"]].to_string(index=False))
    print(summary.to_string(index=False))
    print(levels.to_string(index=False))


if __name__ == "__main__":
    main()
