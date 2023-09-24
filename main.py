import system_of_cities as sc
import linked_census as lc
import network_utils as nu
import pandas as pd
import numpy as np

if __name__ == '__main__':
    parent = sc.get_system_of_cities(year=lc.CensusYear.y1850, alpha=1)
    collection = parent.identify_subsystems_via_community_detection(algorithm=nu.CommunityDetectionAlgorithm.LEIDEN, resolution=0.005, n_iterations=100)
    from Plotting.CommunityQuality import community_block_matrix_heatmap
    fig = community_block_matrix_heatmap(collection=collection, min_n_cities=20, log_scale=True)


