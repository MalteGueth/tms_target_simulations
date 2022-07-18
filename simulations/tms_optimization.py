from simnibs import opt_struct

# Just like with the previous scripted simulations, coding SimNIBS optimization in Python relies on session structures (tms_opt)
# You add new parameters to the object by indexing them with a dot and then specifying the parameter

# This analysis will take a target location and give you the optimal coil location and orientation
# to maximize the electric field strength at this target by running a series of simulations

# Set your root directory
path = 'C:\\Users\\Malte\\SimNIBS-3.2\\'

# Initialize the optimization structure
tms_opt = opt_struct.TMSoptimize()
# Index the mesh file you would like to use for the optimization
tms_opt.fnamehead = path + 'simnibs_examples\\ernie\\ernie.msh'
# Select the folder you would like to store the results in
# This needs to be an empty folder
tms_opt.pathfem = path + 'optimization'
# Set the coil name that you would like to use for the optimization
tms_opt.fnamecoil = 'Magstim_70mm_Fig8.nii.gz'
# Select a target for the optimization
tms_opt.target = [28, -77.3, 66.4]
# If you set the solver to 'pardiso',
# you run a more memory efficient version of the optimization
tms_opt.solver_options = 'pardiso'
# Set the maximum of the range of angles to include into the optimization search
tms_opt.search_angle = 360
# Set the size of angle increments
tms_opt.angle_resolution = 15
# Set the radius drawn around the target in mm
tms_opt.target_size = 5
# Set the distance of the coil to the head surface in mm
tms_opt.distance = 10

# Run the optimization
tms_opt.run()
