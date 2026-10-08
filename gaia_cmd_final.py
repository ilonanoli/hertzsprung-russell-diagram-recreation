import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.colors import LinearSegmentedColormap, Normalize

stellar_cmap = LinearSegmentedColormap.from_list(
    "stellar",
    [
        (0.00, "#1748FF"),  # Electric blue
        (0.18, "#00BFFF"),  # Bright cyan
        (0.38, "#D9F7FF"),  # Icy white
        (0.52, "#FFF6B0"),  # Pale yellow
        (0.68, "#FFD000"),  # Gold
        (0.82, "#FF7300"),  # Orange
        (1.00, "#FF2020")   # Intense red
    ]
)

# Load real Gaia DR3 data
df = pd.read_csv("gaia_cmd_clean.csv")

df = df.dropna(subset=["BP_RP", "M_G"])
df = df[np.isfinite(df["BP_RP"]) & np.isfinite(df["M_G"])]

plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(13, 9))
fig.patch.set_facecolor("#000000")
ax.set_facecolor("#000000")

# Subtle glow
ax.scatter(
    df["BP_RP"],
    df["M_G"],
    c=df["BP_RP"],
    cmap=stellar_cmap,
    norm=Normalize(vmin=-0.5, vmax=4),
    s=5,
    alpha=0.06,
    linewidths=0,
    rasterized=True
)

# Individual stars
scatter = ax.scatter(
    df["BP_RP"],
    df["M_G"],
    c=df["BP_RP"],
    cmap=stellar_cmap,
    norm=Normalize(vmin=-0.5, vmax=4),
    s=0.8,
    alpha=0.75,
    linewidths=0,
    rasterized=True
)

# Astronomy convention: brightest stars at the top
ax.set_xlim(-0.5, 4.2)
ax.set_ylim(17, -6)

ax.set_xlabel(
    r"Colour index $G_{\rm BP}-G_{\rm RP}$",
    fontsize=14,
    labelpad=12
)
ax.set_ylabel(
    r"Absolute magnitude $M_G$",
    fontsize=14,
    labelpad=12
)
fig.text(
    0.5, 0.935,
    "Hertzsprung–Russell Diagram",
    ha="center",
    va="center",
    fontsize=23,
    fontweight="bold",
    color="white"
)

fig.text(
    0.5, 0.895,
    "Gaia DR3 | Stellar Colour–Magnitude Diagram",
    ha="center",
    va="center",
    fontsize=12,
    color="#AAAAAA"
)

ax.grid(color="white", alpha=0.05, linewidth=0.5)
ax.tick_params(colors="white", labelsize=11)

for spine in ax.spines.values():
    spine.set_color("#aaaaaa")

cbar = fig.colorbar(scatter, ax=ax, pad=0.025)
cbar.set_label(
    r"Colour index $G_{\rm BP}-G_{\rm RP}$",
    fontsize=12
)

# Labels for regions that are visible in the current sample
ax.annotate(
    "Main sequence",
    xy=(2.1, 8.0),
    xytext=(2.5, 5.4),
    fontsize=13,
    color="white",
    arrowprops=dict(arrowstyle="->", color="white")
)

ax.annotate(
    "Giant candidates",
    xy=(1.25, 0.5),
    xytext=(1.8, -2),
    fontsize=12,
    color="#ffbd94",
    arrowprops=dict(arrowstyle="->", color="#ffbd94")
)

ax.annotate(
    "White dwarf candidates",
    xy=(0.25, 12.0),
    xytext=(-0.25, 15.5),
    fontsize=12,
    color="#a9caff",
    arrowprops=dict(arrowstyle="->", color="#a9caff")
)

ax.text(
    0.97, 0.04,
    f"N = {len(df):,} stars",
    transform=ax.transAxes,
    ha="right",
    fontsize=11,
    color="white",
    bbox=dict(
        facecolor="#101018",
        edgecolor="#888888",
        boxstyle="round,pad=0.5"
    )
)

# Adjust the plot size to leave room for the titles
fig.subplots_adjust(
    top=0.79,
    bottom=0.12,
    left=0.15,
    right=0.90
)

plt.savefig(
    "gaia_cmd_dark.png",
    dpi=300,
    facecolor=fig.get_facecolor(),
    bbox_inches="tight"
)

plt.show()