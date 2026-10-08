import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("gaia_hr_data.csv")

plt.figure(figsize=(9, 5))

plt.hist(
    df["Teff"].dropna(),
    bins=60,
    edgecolor="black",
    alpha=0.7
)

plt.xlabel("Effective temperature (K)")
plt.ylabel("Number of stars")
plt.title("Temperature Distribution — Gaia DR3")
plt.grid(alpha=0.2)

plt.tight_layout()
plt.show()
