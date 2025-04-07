# CC_transform_to_metashape
 Reads the transform matrix from Cloud Compare into a script that transforms the model space in metashape

This is done through regex pattern matching identifying each 4x4 matrix so a complete copy of the Cloud Compare Console should* be parsable.

## note on units
Includes selection of units used during the transform process.

If your reference model is in mm (common with CT or structured light data) you need to apply a 1000 x scale in cloud compare before performing the alignment.
See screenshot (edit - mulitply scale)

when importing the transform in metashape, you must select the 'mm' button.



Use of imperial measurements has not been tested.