# CC_transform_to_metashape
 Reads the transform matrix from Cloud Compare into a script that transforms the model space in metashape

This is done through regex pattern matching identifying each 4x4 matrix so a complete copy of the Cloud Compare Console should* be parsable.

## note on units
Includes selection of units used during the transform process.

If you exported models in mm and performed alignment in cloud compare (common when aligning to structured light scans),
then it is necessary to compensate for this in metashape where the local reference continues to function in metres.

This appears to be true even when using a CRS set to mm units.

Use of imperial measurements has not been tested.