#!/usr/bin/env python

"""
This data was restructured using ChatGPT v1.0.0
Disse dataene ble omstrukturert ved bruk av ChatGPT v1.0.0

Usage: python GOM-scale_to_CSV.py input.xml output.csv
"""

import argparse
import os
import xml.etree.ElementTree as ET

# Create the argument parser
parser = argparse.ArgumentParser(description='Convert XML distances to CSV format')
parser.add_argument('input_file', help='XML input file path')
parser.add_argument('output_file', help='CSV output file path')

# Parse the arguments
args = parser.parse_args()

# Read the distances from the XML input file
tree = ET.parse(args.input_file)
root = tree.getroot()

# Create the header and data lists
header = ['start_point', 'end_point', 'length', 'accuracy (m)']
data = []

# Iterate over each distance element and extract the data
for distance in root.iter('distance'):
    name = distance.attrib['name']
    height = distance.attrib['height']
    length = distance.attrib['length']
    
    # Split the name into start and end points
    start_point, end_point = name.split('↔')
    
    # Append the extracted data to the data list
    data.append([start_point, end_point, length, '0.0000002'])

# Write the header and data to the CSV output file
output_file = os.path.join(os.path.dirname(args.input_file), args.output_file)
with open(output_file, 'w') as f:
    f.write('# This data was restructured using ChatGPT v1.0.0\n')
    f.write('# Disse dataene ble omstrukturert ved bruk av ChatGPT v1.0.0\n')
    f.write(';'.join(header) + '\n')
    for row in data:
        f.write(';'.join(row) + '\n')

print('Conversion complete.')
