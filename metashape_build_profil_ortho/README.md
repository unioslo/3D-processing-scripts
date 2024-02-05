# metashape_build_profil_ortho
 Builds an orthomosaic from 2 points on a profile

# Work In Progress!

Current script will take 2 points as input, and generate 3 new points that can be used in the making a DEM or orthomosaic.

## Usage
 -1 Open project in metashape and make sure model is correctly georeferenced.

 -1 create 2 new points on the profile you want an orthomosaic of.
    the first point should be at the Left of the profile.
    Points should be on the surface of the profile, e.g. not on a stone that protudes
    Exact positioning is not important.

-1 Rename point 1 to the ID of your section - this is important.

-1 select this renamed point 1, and point 2 (select the names, not the tick box)

-1 Go to tools -> run script and run the script in the src folder
    when asked for a baseline - choose a sensible number for your site/section. This allows you to use the same elevation baseline for all sections in your site if you want to

-1 you can then delete the two points you made on the section
    NOTE: this will be automated later

-1 when complete, use the reference panel to import the new points created - these will be in a folder called profil_points in the same folder as your metashape project
    NOTE: THIS WILL BE CHANGED IN FUTURE VERSIONS

-1 choose workflow -> build DEM, or build Orthomosaic

-1 choose 'planar' projection and 'markers'.  If it is only one profile in that model the markers will be automatically selected for you.

-1 you can then export the DEM/orthomosaic and load into an arcgis map with an arbitrary metric coordinate system (this is available from T:\Bifrost-Lab\2-3Dutstyr\8-GIS_utstyr\Coordinate Reference Systems), arcgis templates are WIP.


## TO DO
Lots