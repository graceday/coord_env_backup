# Coord environment analysis tool
- Reads in a LAMMPS .data file and analysis carbon coordination environment
- coord_env produces table of coord no vs frequency having excluded any atoms within 1.6Å of the box boundary
- v2 improves on this to count all atoms within the box
- v3 takes slices and makes a distr fn
- v4 makes a lammpstrj file to visualise
- v5 is modified to deal with a box which does not have one vertex at the origin
- cumulative_v2 is similarly a modified version, which works for a box located anywhere on the cartesian axes and sweeps across this in slices to generate a profile of proportions of 3 and 4 coordinate C atoms
