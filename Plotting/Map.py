from typing import List

import plotly.graph_objects as go
import system_of_cities as sc
import pandas as pd
import numpy as np

from Plotting.Layout import MapPlotLayout


def system_of_cities_map(collection: sc.SystemOfCitiesCollection, min_n_cities: int, layout: MapPlotLayout):
    n_cities_systems = collection.get_systems_n_cities()
    large_systems_ids = n_cities_systems.loc[n_cities_systems['n_cities'] >= min_n_cities].index
    traces = get_traces_large_systems(collection=collection, layout=layout, large_systems_ids=large_systems_ids)
    other_cities_scatter = get_traces_cities_not_in_large_systems(collection=collection, layout=layout, large_systems_ids=large_systems_ids)
    traces.append(other_cities_scatter)
    fig = go.Figure(data=traces)
    fig.update_layout(template='plotly_white', title=f'Map systems with at least {min_n_cities} cities in {collection.year.value}', font=dict(size=18))
    fig.update_xaxes(title_text='Longitude')
    fig.update_yaxes(title_text='Latitude')
    return fig


def get_traces_large_systems(collection: sc.SystemOfCitiesCollection, layout: MapPlotLayout, large_systems_ids: List[int]):
    large_systems = collection.get_systems(systems=large_systems_ids)
    traces = []
    for s in large_systems:
        names_coords_pop = pd.concat([s.get_city_coordinates(), s.get_city_name(), s.get_city_population()], axis=1)
        names_coords_pop.dropna(subset=['lon', 'lat'], inplace=True)
        sizes = _scale_to_interval(x=np.power(names_coords_pop['population'].values, layout.marker_size_exponent), min_val=layout.marker_size_min, max_val=layout.marker_size_max)
        scatter = go.Scatter(x=names_coords_pop['lon'].values, y=names_coords_pop['lat'].values, mode='markers', text=names_coords_pop['city_name'].values, marker=dict(size=sizes),
                             name=s.get_largest_city_name(),
                             hoverinfo='text')
        traces.append(scatter)
    return traces


def get_traces_cities_not_in_large_systems(collection: sc.SystemOfCitiesCollection, layout: MapPlotLayout, large_systems_ids: List[int]):
    other_cities = []
    for s in collection.get_systems():
        if s.sid not in large_systems_ids:
            names_coords_pop = pd.concat([s.get_city_coordinates(), s.get_city_name(), s.get_city_population()], axis=1)
            names_coords_pop.dropna(subset=['lon', 'lat'], inplace=True)
            other_cities.append(names_coords_pop)

    other_cities = pd.concat(other_cities, axis=0)
    other_cities_scatter = go.Scatter(x=other_cities['lon'].values, y=other_cities['lat'].values, mode='markers', text=other_cities['city_name'].values,
                                      marker=dict(size=layout.marker_size_min / 2, color='black'), name='Other cities')

    return other_cities_scatter


def _scale_to_interval(x: np.ndarray, min_val: float, max_val: float):
    return (x - np.min(x)) / (np.max(x) - np.min(x)) * (max_val - min_val) + min_val