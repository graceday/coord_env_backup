import argparseimport numpy as npparser = argparse.ArgumentParser(    description="Read a LAMMPS .data file and count for nearest neighbours.")parser.add_argument(    "--file",    type=str,    help="The .data file to read.",)args = parser.parse_args()def retrieve_data(data_file, coordinates, boxsize):    with open(f"{data_file}", "r") as df:        lines = df.readlines()    natoms = int((lines[2].split())[0])    boxsize += ([float((lines[5].split())[0]), float((lines[5].split())[1])],                [float((lines[6].split())[0]), float((lines[6].split())[1])],                [float((lines[7].split())[0]), float((lines[7].split())[1])])    for i in range(1, natoms+1):        # atom_id = float((lines[i+14].split())[0])        xcoord = float((lines[i+14].split())[2])        ycoord = float((lines[i+14].split())[3])        zcoord = float((lines[i+14].split())[4])        fullcoord = ([xcoord, ycoord, zcoord])        coordinates.append(fullcoord)    return coordinates, boxsize# retrieve_data returns a list of ([x,y,z],...) coordinates# and the [xhi, yhi, zhi] box sizedef pythagoras(a, b, c):    distance = np.sqrt(a**2 + b**2 + c**2)    return distance# just squares and roots 3 1D distancesdef find_1D_distances(i, j, boxsize):    dx = i[0] - j[0]    dy = i[1] - j[1]    dz = i[2] - j[2]    boxlenx = boxsize[0][1] - boxsize[0][0]    boxleny = boxsize[1][1] - boxsize[1][0]    boxlenz = boxsize[2][1] - boxsize[2][0]    dx = dx - boxlenx*int((dx * 2.0)/boxlenx)    dy = dy - boxleny*int((dy * 2.0)/boxleny)    dz = dz - boxlenz*int((dz * 2.0)/boxlenz)    return dx, dy, dzdef distance_check(full_coordinates, cutoff, boxsize):    data = []    for i, coord1 in enumerate(full_coordinates):        count = 0        for coord2 in full_coordinates:            dx, dy, dz = find_1D_distances(coord1, coord2, boxsize)            distance = pythagoras(dx, dy, dz)            if coord1 == coord2:                continue            if distance < cutoff:                count = count + 1        data.append([i, count])    return data# loops over coordinates data set and calculates distance between points,# adding 1 to the coordination environment count if there is an atom at less# than the cutoff distancedef create_histogram_table(data):    results_table = []    for i in [0, 1, 2, 3, 4, 5, 6]:        count = 0        for element in data:            if element[1] == i:                count = count + 1        results_table.append([i, count])    with open(f"{args.file[0:-5]}_coord_distr.dat", "x") as hist:        hist.write("coord_no frequency\n")        for item in results_table:            hist.write("{} {}\n".format(*item))# produces a coord_no / frequency data table# Maincutoff = 1.6full_coordinates = []boxsize = ()full_coordinates, boxsize = retrieve_data(args.file, full_coordinates, boxsize)print(boxsize)data = distance_check(full_coordinates, cutoff, boxsize)create_histogram_table(data)