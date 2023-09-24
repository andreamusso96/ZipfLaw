import system_of_cities as sc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, leaves_list


def clustered_adjacency_matrix_heatmap(collection: sc.SystemOfCitiesCollection, min_n_cities: int):
    clustered_adjacency_largest_systems = collection.community_detection_result.get_clustered_adjacency(threshold_community_size=min_n_cities - 1)
    clustered_adjacency_largest_systems = pd.DataFrame(np.where(clustered_adjacency_largest_systems > 0, 1, 0),
                                                       index=clustered_adjacency_largest_systems.index,
                                                       columns=clustered_adjacency_largest_systems.columns)

    labels = collection.parent.get_city_name(city=clustered_adjacency_largest_systems.index)['city_name'].fillna('---').values
    labels = np.where(labels != '---', labels, clustered_adjacency_largest_systems.index.astype(str))
    fig = go.Figure(data=go.Heatmap(z=clustered_adjacency_largest_systems.values, x=labels, y=labels, colorscale='Greys'))
    fig.update_layout(template='plotly_white', title=f'Clustered adjacency matrix for systems with at least {min_n_cities} cities in {collection.year.value}', font=dict(size=18))
    fig.update_xaxes(title_text='City')
    fig.update_yaxes(title_text='City')
    return fig


def community_block_matrix_heatmap(collection: sc.SystemOfCitiesCollection, min_n_cities: int, log_scale: bool = False):
    n_cities_systems = collection.get_systems_n_cities()
    large_systems_ids = n_cities_systems.loc[n_cities_systems['n_cities'] >= min_n_cities].index
    block_matrix = collection.community_detection_result.get_block_matrix()
    block_matrix_largest_systems = block_matrix.loc[large_systems_ids, large_systems_ids]
    block_matrix_largest_systems = np.log(block_matrix_largest_systems + 1) if log_scale else block_matrix_largest_systems
    block_matrix_largest_systems = hierarchical_cluster_block_matrix(matrix=block_matrix_largest_systems) if len(block_matrix_largest_systems) > 2 else block_matrix_largest_systems

    labels = collection.get_systems_name(systems=block_matrix_largest_systems.index)['name'].fillna('---').values
    labels = np.where(labels != '---', labels, large_systems_ids.astype(str))

    fig = go.Figure(data=go.Heatmap(z=block_matrix_largest_systems.values, x=labels, y=labels))
    fig.update_layout(template='plotly_white', title=f'Community block matrix for systems with a least {min_n_cities} cities in {collection.year.value}', font=dict(size=18))
    fig.update_xaxes(title_text='System')
    fig.update_yaxes(title_text='System')
    return fig


def hierarchical_cluster_block_matrix(matrix: pd.DataFrame):
    # Convert the distance matrix into a condensed form
    symmetric_matrix = (matrix.values + matrix.values.T)/2
    distance_matrix = np.divide(1, symmetric_matrix, out=np.inf * np.ones_like(symmetric_matrix), where=symmetric_matrix != 0)
    max_distance_matrix = distance_matrix[distance_matrix != np.inf].max()
    distance_matrix = np.where(distance_matrix == np.inf, 10*max_distance_matrix, distance_matrix)
    np.fill_diagonal(distance_matrix, 0)
    condensed_matrix = squareform(distance_matrix)

    # Compute the hierarchical clustering
    linked = linkage(condensed_matrix, method='single')

    # Get the order of rows (or columns) from the hierarchy
    order = leaves_list(linked)

    # Reorder the matrix
    ordered_matrix = matrix.iloc[order,order]
    return ordered_matrix
