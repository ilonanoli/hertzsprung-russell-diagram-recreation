from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

vizier = Vizier(
    columns=[
        "Source", "Plx", "e_Plx",
        "Gmag", "BPmag", "RPmag"
    ],
    row_limit=20000
)

regions = [
    (56.75, 24.11),
    (180.0, 30.0),
    (270.0, -30.0),
    (90.0, -45.0)
]

frames = []

for ra, dec in regions:
    coord = SkyCoord(
        ra=ra * u.deg,
        dec=dec * u.deg,
        frame="icrs"
    )

    result = vizier.query_region(
        coord,
        radius=2 * u.deg,
        catalog="I/355/gaiadr3"
    )

    if result:
        frame = result[0].to_pandas()
        frames.append(frame)
        print(f"Region ({ra}, {dec}): {len(frame)} stars")

df = pd.concat(frames, ignore_index=True)

df = df.drop_duplicates(subset="Source")
df.to_csv("gaia_cmd_raw.csv", index=False)

print("Total unique sources:", len(df))

df = df.dropna(
    subset=["Plx", "e_Plx", "Gmag", "BPmag", "RPmag"]
).copy()

df = df[
    (df["Plx"] > 0) &
    (df["e_Plx"] > 0) &
    (df["Plx"] / df["e_Plx"] > 10)
].copy()

df["BP_RP"] = df["BPmag"] - df["RPmag"]

df["M_G"] = (
    df["Gmag"]
    + 5 * np.log10(df["Plx"])
    - 10
)

df.to_csv("gaia_cmd_clean.csv", index=False)

print("Stars after filtering:", len(df))


#Display the cleaned data in a color-magnitude diagram

plt.figure(figsize=(11, 8))

plt.scatter(
    df["BP_RP"],
    df["M_G"],
    s=2,
    alpha=0.25,
    c=df["BP_RP"],
    cmap="coolwarm",
    rasterized=True
)

plt.gca().invert_yaxis()

plt.xlim(-0.5, 4)
plt.ylim(17, -6)

plt.xlabel(r"Colour index $G_{BP}-G_{RP}$", fontsize=12)
plt.ylabel(r"Absolute magnitude $M_G$", fontsize=12)

plt.title(
    "Stellar Populations in Gaia DR3",
    fontsize=15
)

plt.colorbar(label=r"Colour index $G_{BP}-G_{RP}$")
plt.grid(alpha=0.12)
plt.tight_layout()

plt.savefig("gaia_cmd.png", dpi=300)
plt.show()