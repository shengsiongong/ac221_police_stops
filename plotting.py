import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from astral import Astral, AstralGeocoder, Location
import datetime


def plot_hit_rates_comparison(hit_rates_comparison, minority_col, marker_size_col, marker_size_scale = 500):
    """
    Plot hit rates comparison madde from the function compare_hit_rates() in calculations.py.
    
    INPUTS
    =======
    compare_hit_rates: A pandas DataFrame made from the function compare_hit_rates
    minority_col: A string indicating the column to make a seperate plot for each unique value in minority_col
    marker_size_col: If not None, compare_hit_rates should have an extra column merged into it indicating the size of each 
                     group such that the size of the dot in the plot is proportional of the size of the group.
    marker_size_scale: A numeric value controlling the marker sizes. One should experiment to get the right marker size.
    """
    g = sns.FacetGrid(hit_rates_comparison, col=minority_col, height = 5)
    g.map(plt.grid)
    g.map_dataframe(plt.plot, [0, 1], [0,1], 'r--', color = 'black')
    if marker_size_col is not None:
        g.map(plt.scatter, "white_hit_rate", "minority_hit_rate", color = 'black', facecolors = 'none', 
                            s = hit_rates_comparison[marker_size_col] / marker_size_scale).set(
                            xlim=(-0.05,1.05) , ylim=(-0.05,1.05), xlabel = 'White hit rate', ylabel = 'Minority hit rate')
    else:
        g.map(plt.scatter, "white_hit_rate", "minority_hit_rate", color = 'black').set(
                            xlim=(-0.05,1.05) , ylim=(-0.05,1.05), xlabel = 'White hit rate', ylabel = 'Minority hit rate')
    g.add_legend();
