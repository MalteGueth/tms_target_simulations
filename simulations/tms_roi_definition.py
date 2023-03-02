import os
import numpy as np
import simnibs

## Set pre-loop variables and plot the ROI

# Set the base path to your simnibs installation
path = 'D:\\lab_meetings\\simnibs_workshop\\simnibs_examples\\'
# Set the name of the subject
subject = 'ernie'
# Set the folder within the simnibs path where you saved your simulation results
folder = 'simulation'
# Set the coil name that you used in the simulation
coil = 'Magstim_70mm_Fig8'
# Create the name of the results .msh file
result_file = subject + '_TMS_1-0001_' + coil + '_nii_scalar.msh'
# Create the complete directory including the results file you want to load
# In this case this directory is:
# 'C:\\Users\\Malte\\SimNIBS-3.2\\simnibs_examples\\ernie\\simnibs_simulation\\ernie_TMS_1-0001_Magstim_70mm_Fig8_scalar.msh'
results_dir = os.path.join(path, folder, result_file)

# Load in the simulation result from the .msh file
head_mesh = simnibs.read_msh(results_dir)

# Crop the mesh file, so you only have the gray matter left (which is at index 2)
gray_matter = head_mesh.crop_mesh(2)

## Define the ROI

# Use the coordinates for the targeted gyrus in native space
# This is normally supplied by the anatomical analysis
# In this case I provide the coordinates I have chosen from the example subject
sub_coords = [36, -76, 50]

# Set the radius of the ROI sphere in mm
r = 5.

# Electric fields are defined in the center of the elements
# get element centers
elm_centers = gray_matter.elements_baricenters()[:]
# Determine the elements in the ROI that are within the ROI sphere's radius
roi = np.linalg.norm(elm_centers - sub_coords, axis=1) < r
# Get the element volumes, we will use those for extracting field statistics
elm_vols = gray_matter.elements_volumes_and_areas()[:]

# Plot the ROI sphere on top of the gray matter in Gmsh
gray_matter.add_element_field(roi, 'roi')
gray_matter.view(visible_fields='roi').show()
