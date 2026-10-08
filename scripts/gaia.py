from astroquery.vizier import Vizier
import astropy.units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt

# MAX NUMBER OF STARS
Vizier.ROW_LIMIT = 20000

# COLUMNS WE NEED
Vizier.columns = [
    'Source',
    'RA_ICRS',
    'DE_ICRS',
    'Teff',
    'Rad',
    'logg',
    'Dist',
    'A0'
]

# DEFINE COORDINATES OF THE REGION OF THE SKY
coord = SkyCoord(
    ra=56.75 * u.deg,
    dec=24.11 * u.deg,
    frame='icrs'
)

# QUERY GAIA DR3 ASTROPHYSICAL PARAMETERS
result = Vizier.query_region(
    coord,
    radius=2.0 * u.deg,
    catalog="I/355/paramp"
)

if result:
    df = result[0].to_pandas()

    print("Downloaded rows:", len(df))
    print(df.head())

    # WE REMOVE STARS WITHOUT TEMPERATURE OR RADIUS
    df = df.dropna(subset=['Teff', 'Rad'])

    # DEFINE SOLAR EFFECTIVE TEMPERATURE
    T_sun = 5772

    # WE CALCULATE LUMINOSITY IN SOLAR UNITS
    df['Lum'] = (df['Rad'] ** 2) * (df['Teff'] / T_sun) ** 4

    print("\nStars with usable parameters:", len(df))
    print(df[['Teff', 'Rad', 'Lum', 'logg']].head())

    # FINALLY WE SAVE LOCALLY
    df.to_csv("gaia_hr_data.csv", index=False)

    
# FIGURE 1: HERTZSPRUNG–RUSSELL DIAGRAM FROM GAIA DR3

plt.figure(figsize=(10, 7))

plt.scatter(
    df['Teff'],
    df['Lum'],
    s=2,
    alpha=0.4
)

plt.yscale('log')
plt.gca().invert_xaxis()

plt.xlabel(r'Effective temperature $T_{\rm eff}$ (K)')
plt.ylabel(r'Luminosity $L/L_\odot$')
plt.title('Hertzsprung–Russell Diagram from Gaia DR3')

plt.grid(True, alpha=0.2)
plt.tight_layout()

plt.show()
