"""
Centralized constants for the PhD Data Analysis project.
"""

# Plotting colors
DARK_COLOR = "#464646"
MID_COLOR = "#969696"
LIGHT_COLOR = "#DCDCDC"

# Font sizes
LABEL_FONTSIZE = 20
TITLE_FONTSIZE = 15
LEGEND_FONTSIZE = 20
TICK_FONTSIZE = 20

# Experiments excluded from certain downstream analyses
SKIP_SAMPLES = ["SC", "CC", "RM", "BM"]

# Map measurement names (derived from axis labels) to output subfolders
MEASUREMENT_PLOT_DIRS = {
    "Sinking-Velocity": "01_Boxplots_Sinking-Velocity",
    "Zeta-Potential": "02_Boxplots_Zeta-Potential",
    "Recovery-Rate": "03_Boxplots_Recovery-Rate",
    "Sinking-Properties": "04_Radarplots_Sinking-Properties",
    "Particle-Size": "05_Boxplots_Particle-Size",
    "Suspended-Solids": "06_Barplots_Suspended-Solids",
}
