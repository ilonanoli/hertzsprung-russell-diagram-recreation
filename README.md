# Stellar Population Analysis Using Gaia DR3

An independent computational astrophysics project using **real Gaia DR3 observations** to explore stellar populations through a physical Hertzsprung–Russell diagram and an observational colour–magnitude diagram (CMD).

![Gaia DR3 colour–magnitude diagram](figures/gaia_cmd_dark.png)

## Overview

The project uses Python, `astroquery`, `astropy`, `pandas`, `numpy`, and `matplotlib` to retrieve, filter, analyse and visualise stellar observations. The final CMD includes **11,303 sources** with positive parallaxes and formal parallax signal-to-noise ratio greater than 10. The physical HR analysis includes **8,322 sources** with usable temperature and radius estimates.

## Scientific approach

**Physical HR diagram:** calculate luminosity from Gaia estimates of radius and effective temperature:

\[L/L_\odot=(R/R_\odot)^2(T_{\rm eff}/5772\,\mathrm{K})^4.\]

**Colour–magnitude diagram:** calculate the Gaia colour index and absolute magnitude using parallax in milliarcseconds:

\[C=G_{\rm BP}-G_{\rm RP},\qquad M_G=G+5\log_{10}(\varpi)-10.\]

The CMD displays a clear main sequence, with smaller regions consistent with giant and white-dwarf candidates. These are **position-based interpretations, not verified classifications**. The colour scale represents the Gaia BP–RP index, not independently measured visual colours.

## Repository contents

- `scripts/gaia.py`: physical HR data retrieval, luminosity calculation and initial diagram
- `scripts/analysis.py`: effective-temperature histogram
- `scripts/gaia_cmd.py`: multi-region CMD data acquisition, filtering and initial plot
- `scripts/gaia_cmd_final.py`: dark-theme annotated CMD
- `data/gaia_hr_data.csv`: processed physical HR sample
- `data/gaia_cmd_clean.csv`: filtered CMD sample
- `figures/gaia_cmd.png`: initial CMD
- `figures/gaia_cmd_dark.png`: final CMD
- `report/report.tex`: scientific report source

## Reproduce the visualisations

Install dependencies:

```bash
python -m pip install astroquery astropy numpy pandas matplotlib
```

From the project root, run the plot scripts **inside the `data/` directory** or adjust the CSV paths in the scripts to point to `data/`. For example, from the project root:

```bash
cd data
python ../scripts/gaia_cmd_final.py
```

The code writes `gaia_cmd_dark.png` into the working directory. To retrieve data again, run the acquisition scripts from the same working directory; online VizieR access is required.

To compile the report in a local LaTeX installation:

```bash
cd report
pdflatex report.tex
pdflatex report.tex
```

## Data and limitations

Data: Gaia DR3 via CDS VizieR (`I/355/gaiadr3` and `I/355/paramp`). The physical HR sample was drawn from one two-degree cone; the CMD was assembled from four two-degree cones, each capped at 20,000 returned sources. The CMD filter requires non-missing photometry and parallax and `Plx/e_Plx > 10` with positive parallax and uncertainty. The sampling is **not representative of the whole Galaxy**. No extinction or Gaia parallax zero-point corrections were applied; formal parallax quality alone does not rule out problematic astrometric or photometric solutions.

## References

- [Gaia DR3 documentation (ESA)](https://gea.esac.esa.int/archive/documentation/GDR3/)
- [Gaia DR3 summary paper](https://doi.org/10.1051/0004-6361/202243940)
- [CDS VizieR](https://vizier.cds.unistra.fr/)
