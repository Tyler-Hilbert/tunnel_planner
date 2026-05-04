import csv
import geopy.distance
from scipy.sparse import csr_array
from scipy.sparse.csgraph import minimum_spanning_tree
import matplotlib.pyplot as plt

def main():
    coords, cities = load_cities_dataset()
    visualize_points(coords)
    mat = get_empty_mat(coords)
    comput_distances(coords, mat)
    mst = get_mst(mat)
    display_mst(mst, cities)
    visualize_mst(coords, mst)


########## Data loading functions ##########

# https://simplemaps.com/data/us-cities
def load_cities_dataset():
    with open('uscities.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        coords = []
        cities = []
        for row in reader:
            if check_if_add_coord(row):
                #print (row["population"], ' \t', row["city"])
                coords.append((row['lat'], row['lng']))
                cities.append(row["city"])
    return coords, cities

def check_if_add_coord(row):
    #return 'Texas' in row["state_name"] and int(row["population"]) > 150000
    return int(row["population"]) > 150000

########## Graph / edge functions ##########

def get_empty_mat(coords):
    V = len(coords)  # Number of vertices
    #print (V)
    mat = [[-1] * V for _ in range(V)]
    return mat

# https://www.geeksforgeeks.org/python/introduction-to-graphs-in-python/
def add_edge(mat, i, j, km):
    mat[i][j] = km
    mat[j][i] = km

def comput_distances(coords, mat):
    for i in range(len(coords)):
        for j in range(len(coords)):
            # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
            add_edge(mat, i, j, int(geopy.distance.geodesic(coords[i], coords[j]).km))


########## MST functions ##########

def get_mst(mat):
    Tcsr = minimum_spanning_tree(mat)
    return Tcsr.toarray().astype(int)

def display_mst(mst, cities):
    for i in range(len(mst)):
        for j in range(len(mst[i])):
            if mst[i][j] != 0:
                print (cities[i], ' to ', cities[j], ': ', mst[i][j], 'kms')

########## Visualization ##########
def visualize_points(coords):
    # FIXME this doesn't correctly scale lat/long
    for coord in coords:
        plt.plot(float(coord[0]), float(coord[1]), 'bo')
    plt.show()

def visualize_mst(coords, mst):
    # Display points
    # FIXME this doesn't correctly scale lat/long
    for coord in coords:
        plt.plot(float(coord[0]), float(coord[1]), 'bo')
    
    # Display lines
    for i in range(len(mst)):
        for j in range(len(mst[i])):
            coord_i = coords[i]
            coord_j = coords[j]
            if mst[i][j] != 0:
                plt.plot(
                    [float(coord_i[0]),float(coord_j[0])],
                    [float(coord_i[1]), float(coord_j[1])], 
                    'g-'
                )
    
    plt.show()

########### Main ##########
main()