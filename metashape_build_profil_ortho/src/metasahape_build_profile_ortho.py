"""
Script to generate orthomosaics for profiles and retain information for use in 2D drawing and reprojection into 3D.

Current alpha version 1. Script will take 2 input markers and generate 3 markers to define a plane
"""

from ast import Index
import Metashape
import os
import math

# Create a Metashape document object
doc = Metashape.app.document

# Get the active chunk
chunk = doc.chunk
crs = doc.chunk.crs

# Prompt the user for a baseline z to use in projections
baseline = Metashape.app.getString("PLease set a baseline")
file_contents=f"# 3-point definition of orthoprojection plane for vertical surface. {crs.wkt}\n"
file_contents+=f"# Label;Easting;Northing;Altitude;2D x;2D y\n"

# Get the list of all marker groups in the chunk
markergroups = chunk.marker_groups
print(markergroups)

first = True
second = False

for index, marker in enumerate(chunk.markers):
    if not second: #shim to stop after the second marker incase 3 are selected
        if marker.selected:
            print(first)
            print(second)
            if first:
                #set name for to group the new pins based on the label of the first pin selected
                new_group_name = "profil_" + marker.label
                print(new_group_name)

                first = False
                coord = marker.position
                T = chunk.transform.matrix
                crs = chunk.crs
                xyz  = crs.project(T.mulp(coord))

                print(marker.label)
                new_x = round(xyz[0], 2)
                new_y = round(xyz[1], 2)
                new_z = int(baseline)
                new_point1 = Metashape.Vector([new_x, new_y, new_z])

                # new_z = round(xyz[2] * 4) / 4.0  # rounds to the nearest quarter metre¨
                file_contents += f"1_{new_group_name};{new_x};{new_y};{new_z};{0};{1}\n"
                file_contents += f"3_{new_group_name};{new_x};{new_y};{(new_z + 1)};{0};{0}\n"
                print(file_contents  + "\n")
            else:
                
                second = True
                coord = marker.position
                T = chunk.transform.matrix
                crs = chunk.crs
                xyz  = crs.project(T.mulp(coord))
                print(marker.label)
                new_x = round(xyz[0], 2)
                new_y = round(xyz[1], 2)
                new_z = int(baseline)
                new_point2 = Metashape.Vector([new_x, new_y, new_z])
                dist = math.dist(new_point1, new_point2)

                print(dist)
                # new_z = round(xyz[2] * 4) / 4.0  # rounds to the nearest quarter metre¨
                file_contents += f"2_{new_group_name};{new_x};{new_y};{new_z};{dist};{0}\n"
                print(file_contents + "\n")

            # Get the path of the current project
            project_path = doc.path
            parent_dir = os.path.dirname(project_path)
 #           parent_dir = os.path.dirname(parent_dir)
            target_dir = parent_dir + "/profile_points/"
            # Check if the directory exists
            if not os.path.exists(target_dir):
                # Create the directory if it doesn't exist
                os.makedirs(target_dir)
                # Define the file name and content

            file_name = new_group_name + ".txt"

            # Write the contents to a file in the same directory as the project
            file_path = target_dir + file_name
            with open(file_path, "w") as f:
                f.write(file_contents)
    else:
        file_contents=""


