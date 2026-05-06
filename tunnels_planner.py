import csv
import geopy.distance
from scipy.sparse.csgraph import minimum_spanning_tree
import matplotlib.pyplot as plt

def main():
    cities = load_cities_dataset()
    visualize_points(cities)
    mat = compute_direct_distances(cities)
    mst = get_mst(mat)
    print_mst(mst, cities)
    visualize_mst(mst, cities)

# Loads dataset from https://simplemaps.com/data/us-cities
# List of dicts with keys 'lat', 'lng' and 'name'
def load_cities_dataset():
    cities = []
    with open('uscities.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city = {}
            if int(row["population"]) > 150000: # Filter out smaller cities
                city['lat'] = float(row['lat'])
                city['lng'] = float(row['lng'])
                city['name'] = row['city']
                cities.append(city)
    return cities

# Returns adjacency matrix of direct distances
def compute_direct_distances(cities):
    # Create adjacency mat of -1
    mat = [[-1] * len(cities) for _ in range(len(cities))]

    # Fill mat with direct distances
    for i in range(len(cities)):
        for j in range(len(cities)):
            # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
            add_edge(
                mat, i, j,
                geopy.distance.geodesic(
                    (cities[i]['lat'], cities[i]['lng']),
                    (cities[j]['lat'], cities[j]['lng'])
                ).km
            )

    return mat

# https://www.geeksforgeeks.org/python/introduction-to-graphs-in-python/
def add_edge(mat, i, j, km):
    mat[i][j] = km
    mat[j][i] = km

# Computes minimum spanning tree
def get_mst(mat):
    Tcsr = minimum_spanning_tree(mat)
    return Tcsr.toarray().astype(int)

# Print which city to city connections
def print_mst(mst, cities):
    for i in range(len(mst)):
        for j in range(len(mst[i])):
            if mst[i][j] != 0:
                print (cities[i]['name'], ' to ', cities[j]['name'], ': ', mst[i][j], 'kms')

########## Visualization ##########
def visualize_points(cities):
    # FIXME this doesn't correctly scale lat/long
    for city in cities:
        plt.plot(city['lat'], city['lng'], 'bo')
    plt.show()

def visualize_mst(mst, cities):
    # Display points
    # FIXME this doesn't correctly scale lat/long
    for city in cities:
        plt.plot(city['lat'], city['lng'], 'bo')
    
    # Display lines
    for i in range(len(mst)):
        for j in range(len(mst[i])):
            cityi = cities[i]
            cityj = cities[j]
            if mst[i][j] != 0:
                plt.plot(
                    [cityi['lat'], cityj['lat']],
                    [cityi['lng'], cityj['lng']],
                    'g-'
                )
    plt.show()

########### Main ##########
main()