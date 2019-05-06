import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from astral import Astral, AstralGeocoder, Location
import datetime

 
def calc_group_size(stops_df, groupby_cols, include_prop = True):
    """
    Calculates the size of the groups formed by grouping stops_df by groupby_cols.

    INPUTS
    =======
    stops_df: A pandas DataFrame that contains stops observations.
    groupby_cols: A list of the name of columns of stops_df to groupby
    include_prop: Whether to include the proportion of observations in each group in addition to the size.

    RETURNS
    ========
    A pandas DataFrame with column 'n' that indicates the size of the group and potentially 'prop' that indicates
    the proportion of observation in the group.
    """
    #groupby = stops_df.groupby(groupby_cols).size().to_frame().reset_index()
    #groupby.columns = list(groupby_cols) + ['n']
    #if include_prop:
        #groupby['prop'] = groupby['n'] / len(stops_df)
    #return groupby
    groupby_df = (stops_df
    .groupby(groupby_cols, as_index=False)[stops_df.columns.values[0]]
    .agg({'n': len}))
    if include_prop:
        groupby_df['prop'] = groupby_df['n'] / len(stops_df)
    return groupby_df


def calc_stop_rates(stops_df, population_df, groupby_cols, population_col='num_people'):
    """
    Calculates the stop rates of the groups formed by grouping stops_df by groupby_cols.

    INPUTS
    =======
    stops_df: A pandas DataFrame that contains stops observations.
    population_df: A pandas DataFrame that contains the population number of each group.
                   Function assumes the population number column is named 'num_people'
    groupby_cols: A list of the name of columns of stops_df and population_df.
    population_col: A string indicating the name of the population column in the population_df.
                     Function assumes that population column is named 'num_people' by default.

    RETURNS
    ========
    A pandas DataFrame with column 'n' that indicates the size of the groups and potentially 'prop' that indicates
    the proportion of observation in the groups.
    """
    #groupby_df = stops_df.groupby(groupby_cols).size().reset_index()
    #groupby_df.columns = list(groupby_cols) + ['n']
    #merged = groupby_df.merge(population_df, on = groupby_cols)
    #merged['stop_rate'] = merged['n'] / merged['num_people']
    #return merged[list(groupby_cols) + ['stop_rate']]
    groupby_df = calc_group_size(stops_df, groupby_cols)
    merged_df = groupby_df.merge(population_df, how='left', on=groupby_cols).dropna(axis=0)
    merged_df['stop_rate'] = merged_df['n'] / merged_df[population_col]
    merged_df['stop_rate'] = merged_df['stop_rate'].astype('float')
    return merged_df[list(groupby_cols) + ['stop_rate']]


def calc_search_rates(stops_df, groupby_cols, search_col = 'search_conducted'):
    """
    Calculates the search rates of the groups formed by grouping stops_df by groupby_cols.

    INPUTS
    =======
    stops_df: A pandas DataFrame that contains stops observations.
    groupby_cols: A list of the name of columns of stops_df to groupby
    search_col: A string indicating the name of the search column.
                     Function assumes that search column is named 'search_conducted' by default.

    RETURNS
    ========
    A pandas DataFrame with column 'search_rate' that indicates the search rates of the groups.
    """
    #groupby_df = stops_df.groupby(groupby_cols)[search_col].mean().reset_index()
    #groupby_df = groupby_df.dropna()
    #groupby_df = groupby_df.reset_index(drop = True)
    #groupby_df.columns = groupby_cols + ['search_rate']
    #return groupby_df
    groupby_df = (stops_df
    .groupby(groupby_cols, as_index=False)[search_col]
    .agg({'search_rate': lambda x: np.mean([float(i) for i in x])})
    .dropna(axis=0))
    return groupby_df


def calc_arrest_rates(stops_df, groupby_cols, arrest_col = 'arrest_made'):
    """
    Calculates the arrest rates of the groups formed by grouping stops_df by groupby_cols.

    INPUTS
    =======
    stops_df: A pandas DataFrame that contains stops observations.
    groupby_cols: A list of the name of columns of stops_df to groupby
    arrest_col: A string indicating the name of the arrest column.
                     Function assumes that frisk column is named 'arrest_made' by default.

    RETURNS
    ========
    A pandas DataFrame with column 'arrest_rate' that indicates the arrest rates of the groups.
    """
    #groupby_df = stops_df.groupby(groupby_cols)[arrest_col].mean().reset_index()
    #groupby_df = groupby_df.dropna()
    #groupby_df = groupby_df.reset_index(drop = True)
    #groupby_df.columns = groupby_cols + ['arrest_rate']
    #return groupby_df
    groupby_df = (stops_df
    .groupby(groupby_cols, as_index=False)[arrest_col]
    .agg({'arrest_rate': 'mean'})
    .dropna(axis=0))
    return groupby_df

def calc_frisk_rates(stops_df, groupby_cols, frisk_col = 'frisk_performed'):
    """
    Calculates the frisk rates of the groups formed by grouping stops_df by groupby_cols.

    INPUTS
    =======
    stops_df: A pandas DataFrame that contains stops observations.
    groupby_cols: A list of the name of columns of stops_df to groupby
    frisk_column: A string indicating the name of the frisk column.
                     Function assumes that frisk column is named 'frisk_performed' by default.

    RETURNS
    ========
    A pandas DataFrame with column 'frisk_rate' that indicates the frisk rates of the groups.
    """
    #groupby_df = stops_df.groupby(groupby_cols)[frisk_col].mean().reset_index()
    #groupby_df = groupby_df.dropna()
    #groupby_df = groupby_df.reset_index(drop = True)
    #groupby_df.columns = groupby_cols + ['frisk_rate']
    #return groupby_df
    groupby_df = (stops_df
    .groupby(groupby_cols, as_index=False)[frisk_col]
    .agg({'frisk_rate': lambda x: np.mean([float(i) for i in x])})
    .dropna(axis=0))
    return groupby_df

def calc_hit_rates(stops_df, groupby_cols, search_col = 'search_conducted', contraband_col = 'contraband_found'):
    """
    Calculates the hit rates for contrabands of the groups formed by grouping stops_df by groupby_cols.

    INPUTS
    =======
    stops_df: A pandas DataFrame that contains stops observations.
    groupby_cols: A list of the name of columns of stops_df to groupby
    search_col: A string indicating the name of the search column.
                     Function assumes that search column is named 'search_conducted' by default.
    contraband_col: A string indicating the name of the contraband column.
                     Function assumes that contraband column is named 'contraband_found' by default.

    RETURNS
    ========
    A pandas DataFrame with column 'hit_rate' that indicates the hit rates of the groups.
    """
    #groupby_df = stops_df.groupby(groupby_cols)[contraband_col].mean().reset_index()
    #groupby_df = groupby_df.dropna()
    #groupby_df = groupby_df.reset_index(drop = True)
    #groupby_df.columns = groupby_cols + ['hit_rate']
    #return groupby_df
    groupby_df = (stops_df[stops_df[search_col]==True]
    .groupby(groupby_cols, as_index=False)[contraband_col]
    .agg({'hit_rate': lambda x: np.mean([float(i) for i in x])})
    .dropna(axis=0))
    return groupby_df

def compare_rates(rate_name, rates, majority_group, minority_groups, group_col):
    """
    Compares the rates (such as hit rate) between a majority group in a column (i.e. race) and specificed minority groups
    accounting for other group information such as district.

    INPUTS
    =======
    rate_name: A string indicating the column name of the rate
    rates: A pandas DataFrame that contains information about the rate of each group.
               Should contain the column rate_name.
               The functions calc_xx_rates() makes a valid DataFrame for this function.
    majority_group: A string indicating the majority group.
    minority_groups: A list of strings indicating the minority groups.
    group_col: A string indicating the name of the column that indicates the group of the observation.

    RETURNS
    ========
    A pandas DataFrame in which each row compares the rate between the majority group and one of the minority
    groups accounting for the other columns not used in the rates columns.
    """
    #index_cols = set(rates.columns) - set([group_col])
    #index_cols.remove(rate_name)
    #index_cols = list(index_cols)
    #rates = rates.copy()
    #rates = rates[rates[group_col].isin([majority_group] + list(minority_groups))]
    #if len(index_cols) == 0:
        #rates = pd.DataFrame(rates.set_index([group_col])[rate_name]).T
    #else:
        #rates = rates.set_index(list(index_cols) + [group_col])[rate_name].unstack(fill_value = np.nan)
    #rates = rates.rename(columns = {majority_group: majority_group + '_' + rate_name}).reset_index()
    #rates = rates.melt(id_vars = list(index_cols) + [majority_group + '_' + rate_name])
    #rates = rates.rename(columns = {group_col: 'minority_group', 'value': 'minority_' + rate_name})
    #if len(index_cols) > 0:
        #rates = rates.sort_values(by = index_cols)
    #return rates.reset_index(drop = True)
    index_cols = set(rates.columns) - set([group_col])
    index_cols.remove(rate_name)
    index_cols = list(index_cols)
    rates_df = (pd
    .pivot_table(rates, index=index_cols, columns=group_col, values=rate_name, fill_value=0)
    .rename({majority_group: majority_group+ '_' + rate_name}, axis=1))
    if len(index_cols) > 0:
        rates_df.reset_index(inplace=True)
    rates_df = (rates_df
    .melt(id_vars=index_cols+[majority_group+ '_' + rate_name],
    value_vars=minority_groups,
    value_name='minority' + '_' + rate_name)
    .rename({group_col: 'minority_group'}, axis=1))
    if len(index_cols) > 0:
        rates_df = (rates_df
        .sort_values(index_cols)
        .reset_index(drop=True))
    return rates_df

def calc_sunset_times(stops_df, latitude, longitude, timezone, date_col = 'date'):
    """
    Calculates the sunset times for all unique dates in stops_df using the provided latitude and longitude using the given
    timezone.

    INPUTS
    =======
    stops_df: A pandas DataFrame that contains stops observations.
    latitude: An object that can be converted to a float that represents the latitude
    longitude: An object that can be converted to a float that represents the longitude
    timezone: A string indicating the timezone to calculate the times in.
              For a list of accepted arguments for timezone, use the follow code:

              from pytz import all_timezones
              for timezone in all_timezones:
                  print(timezone)
    date_col: A string indicating the date column on stops_df. By default assumes it is 'date'.

    RETURNS
    ========
    A pandas DataFrame in which each row contains information about a date, with column 'sunset' representing sunset
    time, 'dusk' representing dusk time, 'sunset_minutes' representing sunset time in minutes, and 'dusk_minutes' representing
    dusk time in minutes.
    """
    l = Location()
    l.solar_depression = 'civil'
    l.latitude = float(latitude)
    l.longitude = float(longitude)
    l.timezone = timezone
    l.elevation = 0
    unique_dates = list(stops_df[date_col].unique())
    sunset = [l.sun(pd.Timestamp(date), local = True)['sunset'].time() for date in unique_dates]
    dusk = [l.sun(pd.Timestamp(date), local = True)['dusk'].time() for date in unique_dates]
    sunset_minutes = [time.hour * 60 + time.minute for time in sunset]
    dusk_minutes = [time.hour * 60 + time.minute for time in dusk]
    sunset_times = pd.DataFrame(zip(unique_dates, sunset, dusk, sunset_minutes, dusk_minutes))
    sunset_times.columns = ['date', 'sunset', 'dusk', 'sunset_minute', 'dusk_minute']
    return sunset_times

def get_veil_of_darkness_observations(stops_df, sunset_times, date_col = 'date', time_col = 'time'):
    """
    Gets all observations in stops_df that occur after sunset times, removing the observations in the
    ambiguious period between sunset and dusk. Based on the tutorial's definition.

    INPUTS
    =======
    stops_df: A pandas DataFrame that contains stops observations.
    sunset_times. A pandas DataFrame that contains sunset information for each unique date in stops_df.
                  The function calc_sunset_times() makes such DataFrame.
    date_col: A string indicating the date column on stops_df and sunset_times. Should be the same for both.
          By default assumes it is 'date'.
    time_col: A string indicating the name of the time column. By default assumes it is 'time'.

    RETURNS
    ========
    A subset of stops_df that contains all observations that occur after sunset time, merged with sunset_times.
    """
    stops_df = stops_df.copy()
    merged = stops_df.merge(sunset_times, how='left', on = date_col)
    #Convert to datetime if needed.
    try:
        times = merged[time_col].apply(lambda time: datetime.datetime.strptime(time, '%H:%M:%S').time())
    except:
        times = merged[time_col]
    merged['minute'] = times.apply(lambda time: time.hour * 60 + time.minute)
    merged['minutes_after_dark'] = merged['minute'] - merged['dusk_minute']
    merged['is_dark'] = (merged['minute'] > merged['dusk_minute']).astype(int)
    min_dusk_minute = merged['dusk_minute'].min()
    max_dusk_minute = merged['dusk_minute'].max()
    # Filter to get only the intertwilight period
    merged = merged[(merged['minute'] >= min_dusk_minute) & (merged['minute'] <= max_dusk_minute)]
    # Remove ambigous period between sunset and dusk
    merged = merged[~((merged['minute'] > merged['sunset_minute']) &\
                        (merged['minute'] < merged['dusk_minute']))]
    return merged

def calc_vod_rate(vod_stops, start_time, end_time, group_col = 'subject_race', time_col = 'time'):
    """
    Calculate the rate based on observations in stops between start time and end time based on Veil-of-Darkness
    for a group.

    INPUTS
    =======
    vod_stops: A DataFrame that came from the function get_veil_of_darkness_observations().
    start_time: A string indicating the start time in the format "hh:mm".
    end_time: A string indicating the end time in the format "hh:mm".
    group_col: A string indicating the name of the group column. By default assume it is 'subject_race'
    time_col: A string indicating the name of the time column. By default assumes it is 'time'.

    RETURNS
    ========
    Calculate the Veil of Darkness rate based on observations in vod_stops between start time and end time
    for a minority group compared to a majority group.
    """
    vod_stops = vod_stops.copy()
    # convert input to datetime object
    start_time_dt = datetime.datetime.strptime(start_time, '%H:%M').time()
    end_time_dt = datetime.datetime.strptime(end_time, '%H:%M').time()

    # inclusive of start and end time
    
    vod_stops = vod_stops[(vod_stops[time_col] >= start_time_dt) & (vod_stops[time_col] <= end_time_dt)]

    vod_count = vod_stops.groupby('is_dark')[vod_stops.columns.values[0]].agg({'total_count': 'count'})
    vod_stops =(vod_stops
    .groupby(['is_dark', group_col], as_index=False)[vod_stops.columns.values[0]]
    .agg({'race_count': 'count'})
    .merge(vod_count, how='left', on='is_dark'))
    vod_stops['prop'] = vod_stops['race_count'] / vod_stops['total_count']
    vod_stops.drop(['race_count', 'total_count'], axis=1, inplace=True)
    vod_prop = vod_stops.pivot_table(values='prop', index='is_dark', columns=group_col)

    #vod_stops['is_{}'.format(group)] = (vod_stops[group_col] == group).astype(int)
    #groupby = vod_stops.groupby(['is_dark'])['is_{}'.format(group)].mean()
    return vod_prop
