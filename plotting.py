import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from astral import Astral, AstralGeocoder, Location
import datetime



def plot_rates_comparison(rate_name, hit_rates_comparison, majority_group, minority_col, marker_size_col, marker_size_scale = 1,
                         min_lim = -0.1, max_lim = 1.1):
    """
    Plot hit rates comparison madde from the function compare_rates() in calculations.py.

    INPUTS
    =======
    rate_name: A string indicating the column of the rate
    compare_hit_rates: A pandas DataFrame made from the function compare_xx_rates
    majority_group: A string indicating the majority group (i.e. white)
    minority_col: A string indicating the column to make a seperate plot for each unique value in minority_col
    marker_size_col: If not None, compare_hit_rates should have an extra column merged into it indicating the size of each
                     group such that the size of the dot in the plot is proportional of the size of the group.
    marker_size_scale: A numeric value controlling the marker sizes. One should experiment to get the right marker size.
    min_lim: min limit of graph for both x and y.
    max_lim: max limit of graph for both x and y.
    """

    plt.style.use('ggplot')
    g = sns.FacetGrid(hit_rates_comparison, col=minority_col, height = 5)
    #g.map(plt.grid)

    g.map_dataframe(plt.plot, [min_lim, max_lim], [min_lim, max_lim], 'r--', color = 'black')
    if marker_size_col is not None:
#         hit_rates_comparison = hit_rates_comparison[hit_rates_comparison[marker_size_col] > 5000]
        g = (g.map(plt.scatter,
        majority_group + "_" + rate_name,
        "minority_" + rate_name,
        edgecolors = 'black',
        facecolors = 'none',
        s = hit_rates_comparison[marker_size_col].astype(int)/marker_size_scale) # test, attenuates differences
        .set_titles("{col_name}")
        .set(xlim=(min_lim,max_lim) , ylim=(min_lim,max_lim)))

        # add legend
        plt.scatter([], [], s=50, edgecolors='black', facecolors='none', label=marker_size_col)
        h, l = plt.gca().get_legend_handles_labels()
        legend = {labels: handles for handles, labels in zip(h,l)}
        g.add_legend(legend, title=r'$size \propto magnitude$',labelspacing=2);
    else:
        g = (g.map(plt.scatter,
        majority_group + "_" + rate_name, "minority_" + rate_name,
        edgecolors = 'black',
        facecolors = 'none')
        .set_titles("{col_name}")
        .set(xlim=(min_lim,max_lim) , ylim=(min_lim,max_lim)))
        g.add_legend();

# make a legend
# bins = np.linspace(hit_rates_search['num_searches'].min(), hit_rates_search['num_searches'].max(), 5)
# hit_rates_search['bins'] = np.digitize(hit_rates_search['num_searches'], bins)
#for i,b in enumerate(bins,1):
#    plt.scatter([], [], s=np.array([(i*5)**2]), edgecolors='black', facecolors='none', label=str(int(b)))
