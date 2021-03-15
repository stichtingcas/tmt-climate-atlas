import numpy as np
import pandas as pd


def temp_days(period, data_array, low_t, high_t, start_month, end_month, year):
    '''
    This function takes in a data array with average daily temperatures

    Returns: a grid with for every cell the number of days within the specified
    range
    '''

    def is_month(month_of_array, start_month, end_month):
        month_dict = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                      "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
        return (month_of_array >= month_dict[start_month]) & (month_of_array <= month_dict[end_month])

    trange = (low_t, high_t)
    datemp = []
    if period == 'proj':
        lowert = year[:4] + '-01-01'
        uppert = year[5:] + '-12-31'
        # Slice DataArray for given geographical extent, year
        data_array = data_array.sel(time=slice(lowert, uppert))

    datemp = data_array.sel(time=is_month(
        data_array['time.month'], start_month, end_month))

    zeros = datemp[0]
    zeros.values = np.zeros((datemp.sizes['lat'], datemp.sizes['lon']))

    # Calculate number of optimum temperature days per cell over the selected 30-year period and average (/30)
    zeros.values = ((datemp >= (
        273.15 + trange[0])) & (datemp <= (273.15 + trange[1]))).astype(int).sum(axis=0)

    optdays = zeros / 30
    optdays.values = np.flip(optdays.values, 0)
    return optdays


def new_climate(hist, proj, period):
    '''
    function that superimposes change of coarse resolution (e.g. GCM) on higher resolution gridded data (e.g. ERA5-Land)
    hist ~ historical data (ERA5/measurements etc.)
    proj ~ modelled data for historical period and future period to calculate difference
    period ~ future climate time window to calculate. Format: '2041-2070'

    Returns: xarray DataArray with daily values per grid cell for future period
    '''
    if (int(period[5:]) - int(period[:4])) != 29:
        raise ValueError(
            "Period is not 30 years. Please pick a 30-year period, e.g. 1981-2010.")

    start = period[:4] + '-01-01'
    if period[:4] != '2011':
        end = period[5:] + '-12-31'
    else:
        end = period[5:] + '-12-30'

    hist_model = proj.sel(time=slice('1981-01-01', '2010-12-31')).reindex(
        lat=hist['lat'].values, lon=hist['lon'].values, method='nearest')
    fut_model = proj.sel(time=slice(start, end)).reindex(
        lat=hist['lat'].values, lon=hist['lon'].values, method='nearest')
    change = fut_model.values - hist_model.values
    future_climate = fut_model
    future_climate.values = hist.values + change

    return future_climate


def make_pandas(data):
    '''
    This function converts the data to a pandas dataframe so it can be used by
    the choropleth map function by dash

    Returns: pandas dataframe
    '''
    data = data.to_dataframe()
    data = data['tas']
    data = pd.DataFrame(data)
    data = data.reset_index()
    data['lat_lon'] = data['lat'].round(1).astype(
        str) + '_' + data['lon'].round(1).astype(str)
    data['No. of days'] = data['tas']
    data.index = data['lat_lon']
    data = data.drop(columns=['lat', 'lon', 'tas'])
    return data
