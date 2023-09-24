from typing import List

import plotly.graph_objects as go
import system_of_cities as sc
import pandas as pd


def zipf_exponents_barchart(collection: sc.SystemOfCitiesCollection, min_n_cities: int, cutoff_thresholds: List[float], r2_threshold: float):
    n_cities_systems = collection.get_systems_n_cities()
    large_systems_ids = n_cities_systems.loc[n_cities_systems['n_cities'] >= min_n_cities].index
    large_systems = collection.get_systems(systems=large_systems_ids)
    zipf_exponents = _get_zipf_exponents(large_systems=large_systems, cutoff_thresholds=cutoff_thresholds)
    selected_zipf_exponents = _select_zipf_exponents_with_highest_nobs_above_r2_threshold(zipf_exponents=zipf_exponents, r2_threshold=r2_threshold)
    trace = go.Histogram(x=selected_zipf_exponents['exponent'].values, histnorm='probability', nbinsx=min(len(selected_zipf_exponents), 10))
    fig = go.Figure(data=[trace])
    fig.update_layout(template='plotly_white', title=f'Zipf exponents for systems with at least {min_n_cities} cities in {collection.year.value}', font=dict(size=18))
    fig.update_xaxes(title_text='Exponent')
    fig.update_yaxes(title_text='Probability')
    return fig


def _get_zipf_exponents(large_systems: List[sc.SystemOfCities], cutoff_thresholds: List[float]) -> pd.DataFrame:
    zipf_exponents = []
    for s in large_systems:
        for cutoff_threshold in cutoff_thresholds:
            zipf_reg_res = s.get_zipf_regression(cutoff_threshold=cutoff_threshold)
            zipf_exponents.append([s.sid, zipf_reg_res.slope, zipf_reg_res.r2, zipf_reg_res.n_obs, cutoff_threshold])

    zipf_exponents = pd.DataFrame(zipf_exponents, columns=['sid', 'exponent', 'r2', 'n_obs', 'cutoff_threshold'])
    return zipf_exponents


def _select_zipf_exponents_with_highest_nobs_above_r2_threshold(zipf_exponents: pd.DataFrame, r2_threshold: float) -> pd.DataFrame:
    sids = zipf_exponents['sid'].unique()
    exponents = []
    for sid in sids:
        ze_sid = zipf_exponents[zipf_exponents['sid'] == sid]
        ze_sid = ze_sid[ze_sid['r2'] > r2_threshold]
        if len(ze_sid) == 0:
            continue
        ze_sid = ze_sid.sort_values(by='n_obs')
        exponent = ze_sid.loc[ze_sid['n_obs'].idxmax()]['exponent']
        exponents.append([sid, exponent])

    exponents = pd.DataFrame(exponents, columns=['sid', 'exponent'])
    return exponents


def zipf_plots(collection: sc.SystemOfCitiesCollection, min_n_cities: int, cutoff_threshold: float):
    n_cities_systems = collection.get_systems_n_cities()
    large_systems_ids = n_cities_systems.loc[n_cities_systems['n_cities'] >= min_n_cities].index
    large_systems = collection.get_systems(systems=large_systems_ids)
    plots = []
    for s in large_systems:
        zipf_reg = s.get_zipf_regression(cutoff_threshold=cutoff_threshold)
        plots.append(zipf_reg.plot(show=False, text=s.get_city_name()['city_name'].values, title=f'Zipf plot for {s.get_largest_city_name()} in {s.year.value}'))
    return plots
