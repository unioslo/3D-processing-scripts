# watch_n_load
metashape script to watch a folder and auto align any new images
Developed by A. Pantos - Museum of Cultural History, University of Oslo

How to use: 
- run script from Agisoft Metashape
- select root folder which contains the images to be aligned
- Start/Reset: detects markers and performs alignment on entire dataset from the designated folder
- Watch/Pause: stops the watch procedure. Background processes continue. Use for restarting after manual editing
- New focus group: currently nothing, not connected yet but will create a new focus group for nthe following images
- Close: closes the window, running processes continue

Aligning using the script is done on low



## To Do  Restructure to avoid global vars. Move into different class out of the dialogue?

## TO DO restructure to use signals so processing events occur off main thread, and only the wmonitor is on a seperate thread
