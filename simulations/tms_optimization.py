from simnibs import opt_struct

# Just like with the previous scripted simulations, coding SimNIBS optimization in Python relies on session structures (tms_opt)
# You add new parameters to the object by indexing them with a dot and then specifying the parameter

# This analysis will take a target location and give you the optimal coil location and orientation
# to maximize the electric field strength at this target by running a series of simulations

# Set your root directory
path = 'D:\\lab_meetings\\simnibs_workshop\\simnibs_examples\\ernie\\'

# Initialize the optimization structure
tms_opt = opt_struct.TMSoptimize()

# Supply the input file paths and output directory
# Index the mesh file you would like to use for the optimization
tms_opt.fnamehead = path + 'ernie.msh'
# Select the folder you would like to store the results in
# This needs to be an empty folder
tms_opt.pathfem = path + 'optimization'
# Set the coil name that you would like to use for the optimization
tms_opt.fnamecoil = 'Magstim_70mm_Fig8.nii.gz'

# Determine the initial coil placement
# Select a target for the optimization
tms_opt.target = [36, -76, 50]
# For selecting the initial coil angle before iterating through different positions
# set the orientation of the y-axis like before (pointing at CPz)
tms_opt.pos_ydir = [-5, -29, 68]
# Set distance
tms_opt.distance = 10.0

# Set the search parameters
# Set the maximum angle to include into the analysis
tms_opt.search_angle = 140
# Set the size of angle increments
tms_opt.angle_resolution = 15
# Set the a search radius in mm allowing the center of the coil to move in
tms_opt.search_radius = 10
# Set the radius drawn around the target in mm
tms_opt.target_size = 5

# The default is to first show this ROI and search parameters in gmsh
# before running the simulation
# Change this parameters to False if you would like to skip this visualization 
tms_opt.open_in_gmsh = True

# Choose a solver algorithm
# If you set the solver to 'pardiso',
# you run a more memory efficient version of the optimization
tms_opt.solver_options = 'pardiso'

# Run the optimization
tms_opt.run()
