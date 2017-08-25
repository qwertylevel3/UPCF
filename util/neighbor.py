from sklearn.neighbors import NearestNeighbors

def run():
    samples = [[0., 0.], [0., 1.], [1., 1.], [2., 2.], [2., 0.]]
    neigh = NearestNeighbors(n_neighbors=4)
    neigh.fit(samples)
    result=neigh.kneighbors([[2., 1.]])

    for i in result[1][0]:
        print(i)



