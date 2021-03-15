import xarray as xr
import pandas as pd

from temperature_data_functions import temp_days
from temperature_data_functions import new_climate
from temperature_data_functions import make_pandas


def load_dataset(file, var):
    '''
    Load a single dataset and rename the 'tas' variable

    Returns: a dataset loaded from the local server
    '''

    dataset = xr.open_dataset(file)
    # rename the variable to 'tas' to make it equal across datasets
    return dataset.rename({var: 'tas'}).tas


def get_map_data_temp(variable, years, temp_threshold, temp_threshold_2, slider):
    '''
    This function is called from map.py and preprocesses the data that will be
    displayed on the two maps

    Returns: a historic and a projection dataset in pandas data frame format
    '''

    index_to_month = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                      7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    start_month = index_to_month[slider[0]]
    end_month = index_to_month[slider[1]]

    min_temp = 0
    max_temp = 0
    if variable == 'Minimum temperature below':
        max_temp = temp_threshold
        min_temp = -1000
    elif variable == 'Maximum temperature above':
        min_temp = temp_threshold
        max_temp = 1000
    else:
        min_temp = temp_threshold
        max_temp = temp_threshold_2

    ds_map_hist, ds_map_proj = load_historic_and_projection_map_data(variable)

    future_climate = new_climate(ds_map_hist, ds_map_proj, years)
    tempdays_hist = temp_days('hist',
                              ds_map_hist, min_temp, max_temp, start_month, end_month, years)
    tempdays_proj = temp_days('proj',
                              future_climate, min_temp, max_temp, start_month, end_month, years)
    tempdays_hist = make_pandas(tempdays_hist)
    tempdays_proj = make_pandas(tempdays_proj)

    return tempdays_hist, tempdays_proj


def load_historic_and_projection_map_data(variable):
    '''
    Load temperature data for the two maps

    Returns:
    '''

    variable_short = 'tavg'
    tas = 'tasAdjust'
    if variable == 'Minimum temperature below':
        variable_short = 'tmin'
        tas = 'tasminAdjust'
    elif variable == 'Maximum temperature above':
        variable_short = 'tmax'
        tas = 'tasmaxAdjust'

    data_map_hist = load_dataset(
        "Data/temperature/hist_" + variable_short + "_sel.nc", 'tas')
    data_map_proj = load_dataset(
        "Data/temperature/proj_" + variable_short + "_sel.nc", tas)

    return data_map_hist, data_map_proj


def get_chart_data_temp(variable, lat, lon):
    '''
    This function is called from chart.py and loads and preprocesses the data
    for a selected gridcell on the map

    Returns: a list of four datasets:
        - era5 => historic data
        - upc => projection of the upcoming period climate
        - mid => projection of mid century climate
        - end => projection of the end century climate
    '''

    variable_short = 'avg'
    tas = 'tasAdjust'
    if variable == 'Minimum temperature below':
        variable_short = 'min'
        tas = 'tasminAdjust'
    elif variable == 'Maximum temperature above':
        variable_short = 'max'
        tas = 'tasmaxAdjust'

    datasets = {
        'era5': {'data': [], 'description': 'Historical'},
        'hist': {'data': [], 'description': 'Historical model'},
        'upc': {'data': [], 'description': 'Upcoming period (2011-2040)'},
        'mid': {'data': [], 'description': 'Mid century (2041-2070)'},
        'end': {'data': [], 'description': 'End century (2071-2100)'}
    }

    # this list will consist of these datasets: ['era5', 'upc', 'mid', 'end']
    dataset_list = []

    # load all 5 datasets
    for name, _ in datasets.items():
        if name == 'era5':
            datasets[name]['data'] = load_dataset(
                "Data/temperature/tmp_era5_" + variable_short + ".nc", 'tas')
        else:
            datasets[name]['data'] = load_dataset(
                "Data/temperature/tmp_" + name + "_" + variable_short + ".nc", tas)

        # retrieve the data of the selected grid cell and convert to degrees
        # celsius
        datasets[name]['data'] = datasets[name]['data'].sel(
            lon=lon, lat=lat, method='nearest') - 273

    # for every projection, calculate the difference between this projection
    # and the historic model, and add this to era5
    for name in ['upc', 'mid', 'end']:
        datasets[name]['data'] = datasets['era5']['data'] + \
            (datasets[name]['data'] - datasets['hist']['data'])

    # convert every dataset that will be shown to the user to a dataframe
    # and set the description
    for name in ['era5', 'upc', 'mid', 'end']:
        datasets[name]['data'] = datasets[name]['data'].to_dataframe().rename(
            columns={'tas': datasets[name]['description']})

        dataset_list.append(
            datasets[name]['data'][datasets[name]['description']])

    # [::-1] to reverse the order of the datasets to fit the chart better
    ds = pd.concat(dataset_list[::-1], axis=1).round(1)

    return ds
