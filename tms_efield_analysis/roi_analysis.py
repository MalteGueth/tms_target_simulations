import os
import numpy as np
import simnibs
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

## Set pre-loop variables and plot the ROI

# Set the base path to your simnibs installation
path = 'C:\\Users\\Malte\\SimNIBS-3.2'
# Set the name of the subject
subject = 'ernie'
# Set the folder within the simnibs path where you saved your simulation results
folder = 'simnibs_examples\\ernie\\simnibs_simulation'
# Set the coil name that you used in the simulation
coil = 'Magstim_70mm_Fig8'
# Create the name of the results .msh file
result_file = subject + '_TMS_1-0001_' + coil + '_scalar.msh'
# Create the complete directory including the results file you want to load
# In this case this directory is:
# 'C:\\Users\\Malte\\SimNIBS-3.2\\simnibs_examples\\ernie\\simnibs_simulation\\ernie_TMS_1-0001_Magstim_70mm_Fig8_scalar.msh'
results_dir = os.path.join(path, folder, result_file)

# Set the number of simulations you would like to compare (counter in the file name after "_TMS_")
# We have this at two for the comparison of 30 vs. 90 degrees
nrSim = 2

# Load in the simulation result from the .msh file
head_mesh = simnibs.read_msh(results_dir)

# Crop the mesh file, so you only have the gray matter left (which is at index 2)
gray_matter = head_mesh.crop_mesh(2)

## Define the ROI

# Use the coordinates for the targeted gyrus in native space
# This is normally supplied by the anatomical analysis
# In this case I provide the coordinates I have chosen from the example file
sub_coords = [28, -77.3, 66.4]

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

## Get the normE field statistics

# Set the field you would like to analyze (normE field)
field_name = 'normE'

# Create two empty pandas Data Frames to collect some statistics on the different coil angles
# as well as all the normE values contained in the ROI sphere
field_stats = pd.DataFrame(np.zeros(shape=(nrSim*3, 3)))
# Get the size of the ROI sphere
roi_size = len(roi[roi==True])
field_values = pd.DataFrame(np.zeros(shape=(nrSim*roi_size, 2)))

# Rename the columns of the empty Data Frames
field_stats = field_stats.rename(columns={0: 'angle', 1: 'measure', 2: 'value'})
field_values = field_values.rename(columns={0: 'angle', 1: 'value'})
# Create an angle dictionary that will assign degrees to loop iterations
angle_dict = {1: '30', 2: '90'}
# Set a counter for statistical measures (used for indexing)
counter = 0

# Start the loop (two iterations, one for each simulation result)
for angle in np.arange(1, nrSim+1, 1):

    # Load the simulation result just like before, but now you're specifying which simulation result to load
    # 1 = 30 degrees, 2 = 90 degrees
    result_file = subject + '_TMS_1-000' + str(angle) + '_' + coil + '_scalar.msh'
    results_dir = os.path.join(path, folder, result_file)

    head_mesh = simnibs.read_msh(results_dir)
    gray_matter = head_mesh.crop_mesh(2)
    field = gray_matter.field[field_name][:]

    # Collect all the values contained in the sphreical ROI for the current field
    # and assign the corresponding coil angle
    field_values.iloc[roi_size*(angle - 1):roi_size*(angle), 0] = angle_dict[angle]
    field_values.iloc[roi_size*(angle - 1):roi_size*(angle), 1] = field[roi]

    # Also assign the coil angle in the statistics Data Frame
    field_stats.iloc[counter, 0] = angle_dict[angle]
    field_stats.iloc[counter+1, 0] = angle_dict[angle]
    field_stats.iloc[counter+2, 0] = angle_dict[angle]

    # Add a label which measure is in which row
    field_stats.iloc[counter, 1] = 'mean'
    field_stats.iloc[counter+1, 1] = 'peak'
    field_stats.iloc[counter+2, 1] = 'sd'

    # Calculate the mean, peak, and standard deviations for the current angle
    field_stats.iloc[counter, 2] = np.average(field[roi], weights=elm_vols[roi])
    field_stats.iloc[counter+1, 2] = np.max(field[roi])
    field_stats.iloc[counter+2, 2] = np.std(field[roi])

    # Increase the counter by (for three measures), so it will skip to the correct row index in the next iteration
    counter = counter + 3

# Make sure each column in the Data Frame is set to have the correct data type
field_stats = field_stats.astype({'angle': str, 'measure': str, 'value': float})
field_values = field_values.astype({'angle': str, 'value': float})

# Plot the statistics as a bar plot
fig, ax = plt.subplots()
sns.barplot(x='measure', y='value', hue='angle', data=field_stats, ax=ax)
fig.savefig(os.path.join(path, folder, 'normE_stats_barplot.pdf'), bbox_inches='tight')

# Plot the field values in a violin plot
fig, ax = plt.subplots()
sns.violinplot(x='angle', y='value', data=field_values, ax=ax)
fig.savefig(os.path.join(path, folder, 'normE_values_violinplot.pdf'), bbox_inches='tight')
