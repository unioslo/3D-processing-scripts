import os
import sys
import xml.etree.ElementTree as ET

# accept input and output files as command-line arguments
if len(sys.argv) != 3:
    print("Usage: python GOM-points_to_CSV.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# load the XML document
tree = ET.parse(input_file)
root = tree.getroot()

# extract all point elements and sort by id attribute value
points = sorted(root.findall(".//point"), key=lambda p: int(p.get('id')))

# create list of strings for each point element
point_data = []
point_data.append("Point ID;X;Y;Z")  # column headers

for point in points:
    point_id = point.get('id')
    x = point.get('x')
    y = point.get('y')
    z = point.get('z')
    point_str = f"{point_id};{x};{y};{z}"
    point_data.append(point_str)

# combine list of point strings into one value-separated string
result = "\n".join(point_data)  # separate each point onto a new line

# Get the path and filename of the output file
path, file = os.path.split(output_file)

# Write the result to a new text file specified by the output_file argument
with open(output_file, "w") as f:
    f.write(result)