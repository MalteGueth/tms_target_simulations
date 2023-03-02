from simnibs import sim_struct, run_simnibs

# Coding SimNIBS simulations in python relies on session objects (here called s)
# Think of them like complex variables that contain many lists, tables, and other information in one place
# In this case you can index the session object (with a dot) to access or change information 
# like the name of the file you want to run simulations on, the coil you would like to use, 
# or the position of the coil.

# Set your root directory
path = 'C:\\Users\\Malte\\SimNIBS-3.2\\simnibs_examples\\ernie\\'
# Initialize a session
s = sim_struct.SESSION()
# Index the mesh file you would like to use for the simulation
s.fnamehead = path + 'ernie.msh'
# Set the output folder for the simulation results
s.pathfem = path + 'simulation'

# Initialize a list of TMS simulations
tmslist = s.add_tmslist()
# Select the coil file
tmslist.fnamecoil = 'Magstim_70mm_Fig8.nii.gz'

# Initialize a coil position
# You can add as many as you like
# Just repeat the code from line 26 to 37 with a different name (line 29)
pos = tmslist.add_position()
# Set a name for the simulation
pos.name = 'P4_45'
# The position center will set the target position of the TMS coil
# By specifying a standard electrode name, it will be set to that position
pos.centre = 'P4'
# pos_ydir is the orientation of the y-axis, which is the prolongation of the handle (green axis)
# Therefore, this parameter will set the orientation of the coil
# Specifying an electrode name will point the coil at this particular electrode
pos.pos_ydir = 'C2'
# Set the distance between the coil and the head surface to be 10 mm
pos.distance = 10

# Run the simulation(s)
run_simnibs(s)
