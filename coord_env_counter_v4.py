import argparseimport numpy as npparser = argparse.ArgumentParser(    description="Read a LAMMPS .data file and count for nearest neighbours.")parser.add_argument(    "--file",    type=str,    help="The .data file to read.",)parser.add_argument(    "--int",    type=float,    help="The sample interval.",)args = parser.parse_args()def retrieve_data(data_file, coordinates, boxsize):    with open(f"{data_file}", "r") as df:        lines = df.readlines()    natoms = int((lines[2].split())[0])    boxsize += (float((lines[5].split())[1]),                float((lines[6].split())[1]),                float((lines[7].split())[1]))    for i in range(1, natoms+1):        # atom_id = float((lines[i+14].split())[0])        xcoord = float((lines[i+14].split())[2])        ycoord = float((lines[i+14].split())[3])        zcoord = float((lines[i+14].split())[4])        fullcoord = ([xcoord, ycoord, zcoord])        coordinates.append(fullcoord)    return coordinates, boxsize, natoms# retrieve_data returns a list of ([x,y,z],...) coordinates# and the [xhi, yhi, zhi] box sizedef pythagoras(a, b, c):    distance = np.sqrt(a**2 + b**2 + c**2)    return distance# just squares and roots 3 1D distancesdef find_1D_distances(i, j, boxsize):    dx = i[0] - j[0]    dy = i[1] - j[1]    dz = i[2] - j[2]    dx = dx - boxsize[0]*int((dx * 2.0)/boxsize[0])    dy = dy - boxsize[1]*int((dy * 2.0)/boxsize[1])    dz = dz - boxsize[2]*int((dz * 2.0)/boxsize[2])    return dx, dy, dzdef reduce_coordinates(full_coordinates, boxsize, sampling_interval):    zdistances = []    segmented_coordinates = []    for i in range(1, int(boxsize[2]/sampling_interval) + 1):        zbounds = [(i-1) * sampling_interval, i * sampling_interval]        segment = []        for coord in full_coordinates:            if zbounds[0] < coord[2] < zbounds[1]:                segment.append(coord)        zdistances.append(i * sampling_interval)        segmented_coordinates.append(segment)    return zdistances, segmented_coordinatesdef distance_check(segment_coordinates, full_coordinates, cutoff, boxsize):    segment_data = []    for i, coord1 in enumerate(segment_coordinates):        count = 0        for coord2 in full_coordinates:            dx, dy, dz = find_1D_distances(coord1, coord2, boxsize)            distance = pythagoras(dx, dy, dz)            if coord1 == coord2:                continue            if distance < cutoff:                count = count + 1        segment_data.append([i, count])    return segment_datadef create_table_entry(zdistance, segment_data):    data_entry = [zdistance]    for i in [3, 4]:        proportion = 0        count = 0        for element in segment_data:            if element[1] == i:                count = count + 1        if len(segment_data) == 0:            proportion = proportion        else:            proportion = count/len(segment_data)        data_entry.append(proportion)    return data_entrydef create_full_table(results):    with open(f"{args.file[0:-5]}_{args.int}_coord_distr_fn.dat", "x") as cdf:        cdf.write("zdistance %3coord %4coord\n")        for item in results:            cdf.write("{:.1f} {:.2f} {:.2f}\n".format(*item))def write_lammpstrj(natoms, boxsize, full_coordinates):    with open(f"{args.file[0:-5]}.lammpstrj", "x") as fi:        fi.write("ITEM: TIMESTEP\n")        fi.write("0\n")        fi.write("ITEM: NUMBER OF ATOMS\n")        fi.write(f"{natoms}\n")        fi.write("ITEM: BOX BOUNDS pp pp pp\n")        fi.write(f"0.0 {boxsize[0]} \n")        fi.write(f"0.0 {boxsize[1]} \n")        fi.write(f"0.0 {boxsize[2]} \n")        fi.write("ITEM: ATOMS id type x y z\n")        for idx, row in enumerate(full_coordinates, 1):            fi.write(f"{idx} 1 {row[0]}  {row[1]}  {row[2]}\n")# Maincutoff = 1.6sampling_interval = args.intfull_coordinates = []boxsize = ()results = []full_coordinates, boxsize, natoms = retrieve_data(args.file,                                                  full_coordinates,                                                  boxsize)zdistances, segmented_coordinates = reduce_coordinates(full_coordinates,                                                       boxsize,                                                       sampling_interval)for zdistance, segment_coordinates in zip(zdistances, segmented_coordinates):    segment_data = distance_check(segment_coordinates,                                  full_coordinates,                                  cutoff,                                  boxsize)    data_entry = create_table_entry(zdistance,                                    segment_data)    results.append(data_entry)create_full_table(results)print("Successfully wrote results table to "      f"{args.file[0:-5]}_{args.int}_coord_distr_fn.dat")write_lammpstrj(natoms, boxsize, full_coordinates)print("Successfully wrote lammpstrj visualisation to "      f"{args.file[0:-5]}.lammpstrj")"""Add in function to make lammpstrj visualisation"""