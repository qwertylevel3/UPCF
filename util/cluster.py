import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import *
from sklearn.neighbors import kneighbors_graph
from sklearn.datasets import make_blobs


def run():
    plt.figure(figsize=(12, 12))

    n_samples = 1500
    random_state = 2
    X, yreal = make_blobs(n_samples=n_samples, random_state=random_state)
    bandwidth = estimate_bandwidth(X, quantile=0.3)
    # connectivity matrix for structured Ward
    connectivity = kneighbors_graph(X, n_neighbors=10, include_self=False)
    # make connectivity symmetric
    connectivity = 0.5 * (connectivity + connectivity.T)

    y_kmeans = KMeans(n_clusters=3, random_state=random_state).fit_predict(X)

    y_meanshift= MeanShift(bandwidth=bandwidth, bin_seeding=True).fit_predict(X)

    y_ward = AgglomerativeClustering(n_clusters=3, linkage='ward',
                                           connectivity=connectivity).fit_predict(X)
    y_spectral = SpectralClustering(n_clusters=3,
                                          eigen_solver='arpack',
                                          affinity="nearest_neighbors").fit_predict(X)
    y_dbscan = DBSCAN(eps=0.5).fit_predict(X)
    y_affinity_propagation = AffinityPropagation(damping=.9,
                                                       preference=-500).fit_predict(X)

    y_average_linkage = AgglomerativeClustering(
        linkage="average", affinity="cityblock", n_clusters=3,
        connectivity=connectivity).fit_predict(X)

    y_birch = Birch(n_clusters=3).fit_predict(X)

    plt.subplot(331)
    plt.scatter(X[:, 0], X[:, 1], c=yreal)
    plt.subplot(332)
    plt.scatter(X[:, 0], X[:, 1], c=y_kmeans)
    plt.subplot(333)
    plt.scatter(X[:, 0], X[:, 1], c=y_meanshift)
    plt.subplot(334)
    plt.scatter(X[:, 0], X[:, 1], c=y_ward)
    plt.subplot(335)
    plt.scatter(X[:, 0], X[:, 1], c=y_spectral)
    plt.subplot(336)
    plt.scatter(X[:, 0], X[:, 1], c=y_dbscan)
    plt.subplot(337)
    plt.scatter(X[:, 0], X[:, 1], c=y_affinity_propagation)
    plt.subplot(338)
    plt.scatter(X[:, 0], X[:, 1], c=y_average_linkage)
    plt.subplot(339)
    plt.scatter(X[:, 0], X[:, 1], c=y_birch)
    plt.show()

