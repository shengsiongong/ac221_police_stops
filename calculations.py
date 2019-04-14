import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from astral import Astral, AstralGeocoder, Location
import datetime


def calc_group_size(stops_df, groupby_cols, include_prop = True):
    groupby = stops_df.groupby(groupby_cols).size().to_frame().reset_index()
    groupby.columns = list(groupby_cols) + ['n']
    if include_prop:
        groupby['prop'] = groupby['n'] / len(stops_df)
    return groupby

def calc_stop_rates(stops_df, population_df, groupby_cols):
    groupby_df = stops_df.groupby(groupby_cols).size().reset_index()
    groupby_df.columns = list(groupby_cols) + ['n']
    merged = groupby_df.merge(population_df, on = groupby_cols)
    merged['stop_rate'] = merged['n'] / merged['num_people']
    return merged[list(groupby_cols) + ['stop_rate']]

def calc_search_rates(stops_df, groupby_cols):
    groupby_df = stops_df.groupby(groupby_cols)['search_conducted'].mean().reset_index()
    groupby_df.columns = groupby_cols + ['search_rate']
    return groupby_df

def calc_frisk_rates(stops_df, groupby_cols):
    groupby_df = stops_df.groupby(groupby_cols)['frisk_performed'].mean().reset_index()
    groupby_df.columns = groupby_cols + ['frisk_rate']
    return groupby_df

def calc_hit_rates(stops_df, groupby_cols):
    groupby_df = stops_df.groupby(groupby_cols)['contraband_found'].mean().reset_index()
    groupby_df = groupby_df.dropna()
    groupby_df = groupby_df.reset_index(drop = True)
    groupby_df.columns = groupby_cols + ['hit_rate']
    return groupby_df

def compare_hit_rates(hit_rates, minority_races, index_cols):
    hit_rates = hit_rates[hit_rates['subject_race'].isin(['white'] + minority_races)]
    hit_rates = hit_rates.set_index(list(index_cols) + ['subject_race'])['hit_rate'].unstack(fill_value = 0)
    hit_rates = hit_rates.rename(columns = {'white': 'white_hit_rate'}).reset_index()
    hit_rates = hit_rates.melt(id_vars = list(index_cols) + ['white_hit_rate'])
    hit_rates = hit_rates.rename(columns = {'subject_race': 'minority_race', 'value': 'minority_hit_rate'})
    hit_rates = hit_rates.sort_values(by = index_cols)
    return hit_rates.reset_index(drop = True)

def plot_hit_rates_comparison(hit_rates_comparison, marker_size_col, marker_size_scale = 500):
    g = sns.FacetGrid(hit_rates_comparison, col="minority_race", height = 5)
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

def calc_sunset_times(stops_df, latitude, longitude, timezone):
    l = Location()
    l.solar_depression = 'civil'
    l.latitude = latitude
    l.longitude = longitude
    l.timezone = timezone
    l.elevation = 0   
    unique_dates = list(stops_df['date'].unique())
    sunset = [l.sun(pd.Timestamp(date), local = True)['sunset'].time() for date in unique_dates]
    dusk = [l.sun(pd.Timestamp(date), local = True)['dusk'].time() for date in unique_dates]
    sunset_minutes = [time.hour * 60 + time.minute for time in sunset]
    dusk_minutes = [time.hour * 60 + time.minute for time in dusk]
    sunset_times = pd.DataFrame(zip(unique_dates, sunset, dusk, sunset_minutes, dusk_minutes))
    sunset_times.columns = ['date', 'sunset', 'dusk', 'sunset_minute', 'dusk_minute']
    return sunset_times

def get_veil_of_darkness_observations(stops_df, sunset_times):
    stops_df = stops_df.copy()
    merged = stops_df.merge(sunset_times, on = 'date')
    times = merged['time'].apply(lambda time: datetime.datetime.strptime(time, '%H:%M:%S').time())
    merged['minute'] = times.apply(lambda time: time.hour * 60 + time.minute)
    merged['minutes_after_dark'] = merged['minute'] - merged['dusk_minute']
    merged['is_dark'] = (merged['minute'] > merged['dusk_minute']).astype(int)
    min_dusk_minute = merged['dusk_minute'].min()
    max_dusk_minute = merged['dusk_minute'].max()
    # Filter to get only the intertwilight period
    merged = merged[(merged['minute'] > min_dusk_minute) & (merged['minute'] < max_dusk_minute)] 
    # Remove ambigous period between sunset and dusk
    merged = merged[~((merged['minute'] > merged['sunset_minute']) &\
                        (merged['minute'] < merged['dusk_minute']))]
    return merged

def calc_vod_rate_of_minority(vod_stops, start_time, end_time, minority_race):
    vod_stops = vod_stops.copy()
    vod_stops = vod_stops[(vod_stops['time'] > start_time) & (vod_stops['time'] < end_time)]
#     vod_stops = vod_stops[vod_stops['subject_race'].isin(['white', minority_race])]
    vod_stops['is_{}'.format(minority_race)] = (vod_stops['subject_race'] == minority_race).astype(int)
    groupby = vod_stops.groupby(['is_dark'])['is_{}'.format(minority_race)].mean()
    return groupby




