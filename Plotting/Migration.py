import system_of_cities as sc
import numpy as np
import graph_tool.all as gt


def plot_migration_distributions(system_collection: sc.SystemOfCitiesCollection):
    migrations = gt.adjacency(system_collection.parent.g, weight=system_collection.parent.g.ep['weight']).toarray()
