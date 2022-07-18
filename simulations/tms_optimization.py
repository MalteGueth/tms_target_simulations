from simnibs import opt_struct

# Just like with the simulations, coding SimNIBS optimization in Python relies on session structures (tms_opt)
# You add new parameters to the object by indexing them with a dot and then specifying the parameter

# This analysis will take the target location and give you the optimal coil location and orientation
# to maximize the electric field strength at this target

# Set your root directory
path = 'C:\\Users\\Malte\\SimNIBS-3.2\\'

# Initialize the optimization structure
tms_opt = opt_struct.TMSoptimize()
# Index the mesh file you would like to use for the optimization
tms_opt.fnamehead = path + 'simnibs_examples\\ernie\\ernie.msh'
# Select the folder you would like to store the results in
tms_opt.pathfem = path + 'optimization'
# Set the coil name that you used in the optimization
tms_opt.fnamecoil = 'Magstim_70mm_Fig8.nii.gz'
# Select a target for the optimization
tms_opt.target = [28, -77.3, 66.4]
# If you set the solver to 'pardiso',
# you run a more memory efficient version of the optimization
tms_opt.solver_options = 'pardiso'
# Set the maximum angle to include into the analysis
tms_opt.search_angle = 180
# Set the size of angle increments
tms_opt.angle_resolution = 15

# Run the optimization
tms_opt.run()
