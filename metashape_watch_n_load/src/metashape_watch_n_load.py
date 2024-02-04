# small script to watch a folder and process.
# WARNING, current suggeset pipeline relies on in-camera jpg - this can cause issues with built in distortion profiles for some (especially mirrorless) cameras
#   can be mitigated by implementing image ocnversion pipleine further upstream

import Metashape
import PySide2
import time
import threading
import os

from PySide2 import QtGui, QtCore, QtWidgets


# define the dialogue
class watchDlg(QtWidgets.QDialog):

    # intercept close window event to stop the listen subroutine
    def reject(self):
        global isOn
        # change flag so monitor thread will come out of loop
        isOn = False
        print("\n\n==================================================")
        print("Watch mode closed.")
        print("Running processes will continue")
        print("==================================================\n\n")
        return super(watchDlg, self).reject()

    def __init__(self, parent):
        global isOn

        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle("Watch mode")

        self.btnStartReset = QtWidgets.QPushButton("Start/Reset")
        self.btnStartReset.setFixedSize(90, 50)
        self.btnStartReset.setToolTip("Detects markers and performs alignment on entire dataset")

        self.btnPause = QtWidgets.QPushButton("Watch/Pause")
        self.btnPause.setFixedSize(90, 50)
        self.btnPause.setToolTip("Stops the watch procedure. Background processes continue. use for restarting after manual editing")

        self.btnFocusGroup = QtWidgets.QPushButton("New Focus Group")
        self.btnFocusGroup.setFixedSize(90, 50)
        self.btnFocusGroup.setToolTip("Creates a new focus group for next image set")

        self.btnClose = QtWidgets.QPushButton("Close")
        self.btnClose.setFixedSize(90, 50)
        self.btnClose.setToolTip("Closes this window, running procceses continue")

        # findme todo: add entry field for lens calibration data https://www.agisoft.com/forum/index.php?topic=1748.0
            # also need routines to populate and clear as needed.

        layout = QtWidgets.QGridLayout()  # creating layout

        layout.addWidget(self.btnStartReset, 1, 1)
        layout.addWidget(self.btnPause, 1, 5)
        layout.addWidget(self.btnFocusGroup, 5, 1)
        layout.addWidget(self.btnClose, 5, 5)
  

        self.setLayout(layout)

        QtCore.QObject.connect(self.btnStartReset, QtCore.SIGNAL("clicked()"), self.start_reset)
        QtCore.QObject.connect(self.btnPause, QtCore.SIGNAL("clicked()"), self.watch_pause)
        QtCore.QObject.connect(self.btnFocusGroup, QtCore.SIGNAL("clicked()"), self.makeFocusGroup)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()"))

        self.setWindowModality(QtCore.Qt.NonModal)
        self.show()

        window = QtWidgets.QDialog(self)
        window.closeEvent = self.closeEvent



    # loads photos in the input folder
    # checks they don't already exist in thr project (assumes unique photo names)
    # and cleans up any that have been deleted during capture.
    def load_photos(self):
        print("loading photos")
        print(photos_path)
        global _photo_list

        #findme todo: add a characters check in file path to make sure there aren't any strange things
        #findme todo next:  get the chunk name to avoid any accidental loading into other chunks

        file_list = os.listdir(photos_path)
#        print("file list:")
#        print(file_list)
        photo_list = list()     # temporary list of photo paths to be added
        label_list = list()     # temporay list of photos (without paths) to be added
        camera_list = list()    # cameras in the chunk

        # get current camera list and remove any that have been deleted at source.
        
        for camera in chunk.cameras:
            exist = os.path.isfile(camera.photo.path)
            if exist:
                camera_list.append(camera.label)
            else:
                chunk.remove(camera)


        # findme todo: refine this. currently restricted to compressed images to use incamera jpgs for simplicity
        # only includes valid image files
        ext = ["jpg", "jpeg", "jxl", "heic", "heif"]
        # iterate through the file list to check for valid file types and uniqueness
        for file in file_list:

            # excludes temporary files that have ~ in the name
            if file.lower().endswith(tuple(ext)):
                basename = file.rsplit(".",1)[0]
                if basename not in camera_list and '~' not in basename:
                    label_list.append(basename) # shim to pass camera names for selecting
                    photo_list.append("/".join([photos_path, file]))

        if photo_list:
            try:
                chunk.addPhotos(photo_list)
                print (str(len(photo_list)) + " new photos added")
            except: # findme todo: find the correct error exception
                print("Unexpected item in the photo area")
                label_list.clear()

            return label_list
        else:
            print ('no photos to add.')
            return label_list
        


        # findme todo: allow camera grouping for then applying different callibration
        #   see https://www.agisoft.com/forum/index.php?topic=6383.0




        # findme todo next: tidy up the logic here! a shim to induce a leading delay in the script to reduce the chance of 'file access error'.
        # see sketch on remarlable
    #    if _photo_list:        
      #      chunk.addPhotos(_photo_list)
            # continue to next processing stage

     #       print (str(len(photo_list)) + " new photos added")

     #       if photo_list:
       #         _photo_list = photo_list[:]
      #      else:
       #         _photo_list.clear()
        #    return True
     #   else:
      #      if photo_list: # findme debug: unclear if you can set a list to an empty list may not need this if
       #         _photo_list = photo_list[:]
        #    print ('no photos to add.')
         #   return False

        

    # findme todo: add a tidyup button?
    # structures folders by cameras and groups (or seperate script?)
                
        

    def reprocess():
        print("something for the future")
        #   findme todo:
        #   swap out the jpgs for dngs and reprocess on high
        #   include some managment for merging chunks first (?)

        #   findme todo later:
        #   adapt to process low file sizes and swap in with large to reduce process time?
        #       e.g.export camera positions
        #       add photos new and import positions (do sizes need changing?)


    # adds new photos and adds them to the alignment
    def watcher(self):
        global isProcessing
        global isFirst
        global isReset

        print("----------------------")
        print("process loop")
        print("isProcessing = " + str(isProcessing))
        print("isReset = " + str(isReset))
        print("isFirst = " + str(isFirst))
        print("isWatching = " + str(isWatching))



        isProcessing = True
        
        #findme todo:  add a merge markers step to have only one detect markers event on iterative captures
            # see https://www.agisoft.com/forum/index.php?topic=10112.0
            # detectMarkers(target_type=CircularTarget12bit, tolerance=25, filter_mask=False, inverted=False, noparity=False, maximum_residual=5, minimum_size=0, minimum_dist=5, cameras=photo_list)
        
        label_list = self.load_photos()        
        print (" photos added. Trying alignment")
        
        try:    # inelegant solution to handle error thrown when files aren't fully transferred
            print ("trying...")
            if isFirst:
                print ("first run")

                # findme todo: allow for reduction of markers to avoid clusters and redetect more after final final alignment (?)
                chunk.detectMarkers(target_type=Metashape.CircularTarget12bit, tolerance=10, filter_mask=False, inverted=False, noparity=False, maximum_residual=5, minimum_size=0, minimum_dist=5)

                # align all images from scratch
                isFirst = False
                for frame in chunk.frames:
                    frame.matchPhotos(downscale=4, generic_preselection=True, keep_keypoints=True, reference_preselection=False, mask_tiepoints=False)
                    Metashape.app.update()

                chunk.alignCameras(reset_alignment=True)
                Metashape.app.update()

            elif isReset:
                print("--------------------------------")
                print ("resetting alignment and markers. using keypoint masks)")
                # reset alignment and realign using some of the existing information
                # resetting will use masks
                # findme debug next: something fishy with the behaviour sometimes breaks or left unfinished

                # findme todo: add a merge markers step to have detect markers on photo-import
                # see https://www.agisoft.com/forum/index.php?topic=10112.0
                # findme todo: expose or make presets for tolerance and invertedness. set low due to DoF issues with 
                
                isReset = False
                chunk.remove(chunk.markers)
                chunk.point_cloud.removeKeypoints()
                Metashape.app.update()

                # findme todo: allow for reduction of markers to avoid clusters and redetect more after final final alignment (?)
                chunk.detectMarkers(target_type=Metashape.CircularTarget12bit, tolerance=20, filter_mask=False, inverted=False, noparity=False, maximum_residual=5, minimum_size=0, minimum_dist=5)

                Metashape.app.update()
                for frame in chunk.frames:
                    frame.matchPhotos(downscale=4, reset_matches=True, keep_keypoints=True, generic_preselection=False, reference_preselection=True, reference_preselection_mode=Metashape.ReferencePreselectionEstimated, mask_tiepoints=False, filter_mask = True)
                    # findme todo: add some nuances for dealing with different masks and failed alignments at later stages of processing?
                    Metashape.app.update()

                chunk.alignCameras(reset_alignment=True)
                Metashape.app.update()

            elif isWatching:
                print ("adding images if they exist and realigning")
                if label_list:
                    # add new images to existing alignment
                    for frame in chunk.frames:
                        frame.matchPhotos(downscale=4, reset_matches=False, keep_keypoints=True, generic_preselection=True, reference_preselection=True, reference_preselection_mode=Metashape.ReferencePreselectionSource, mask_tiepoints=False)
                        Metashape.app.update()
                    chunk.alignCameras(reset_alignment=False)

                    # selects the aligned cameras, useful for seeing result of last import.
                    for camera in chunk.cameras:
                        if (camera.label in label_list):
                                camera.selected = True
                        else:
                                camera.selected = False

                    Metashape.app.update()



        except: # findme todo: find the correct error exception
            print("Some sort of error (probably waiting for a file. Will try again next loop")


        isProcessing = False
        print("\n\n===========================================")
        print ("Finished processing... waiting and watching")
        print("===========================================\n\n")


    # async loop handler. Will run in the background checking if there is anything to process every
    def monitor(self):
        global timer
        global m

        ##### findme todo: consider watchdog package for filesystem response ####

        if isWatching:
            print("watching")
            self.watcher()
        elif isProcessing:
            print("not watching, doing")
        else:
            print("idling")

        app.processEvents()

        # uses a flag to stop the script when the window is closed
        # but allows active processing events to carry on in the background if theyæve started
        # findme todo: restructure with signals to put processing in main thread
        if isOn:
            time.sleep(10)
            # findme todo: bypass the recurrance limit in python in a nice way
            print("timeout = " + str(timer))
            timer = timer - 1
            self.monitor()
        else:
            print("\n\n\n*********************************************************************")
            print("end of watch process, deleting the monitor")
            del m
            print("THE THREAD IS DEAD")
            print("Safe to do other things")
            print("*********************************************************************\n\n\n")
            # findme debug next: something might be getting stuck in a loop and the thread isn't being deleted.
            



#------------------  button actions -----------


    # findme todo:  add focus masks
        # https://www.agisoft.com/forum/index.php?topic=14057.0

    # changes the status flag to stop the watching next time the timer loops out
    def watch_pause(self):
        global isWatching
        global isFirst
        global isReset

        Reset = False # stops it ressetting everytime you restart the scrip and want to watch

        if not 'm' in globals():
            self.startMonitor()
        
        isFirst = False # disables the first alignment paramters to so you can come back from manual edit

        if isWatching: # pause the watch
            isWatching = False
            self.setWindowTitle("Watch mode: stopped. Press start to reset alignment")
        else: # continue the watch
            isWatching = True
            self.setWindowTitle("Watch mode: running...")
            # starts a new monitor function on a new thread

        print("-----watch/pause pressed")
        print ("isFirst")
        print (isFirst)
        print ("isWatching")
        print (isWatching)
        print ("isProcessing")
        print (isProcessing)
        print ("isReset")
        print (isReset)


    # starts a monitoring deamon on a new thread
    def startMonitor(self):
        global timer
        global isOn
        global m

        timer = 1000            # defualt reciprocator limit for python
        m = threading.Thread(target=self.monitor)
        m.start()
        isOn = True

    # begins the processing from the beginning
    def start_reset(self):
        global isWatching
        global isReset


        # initializes the monitor function if not already running
        if not 'm' in globals():
            self.startMonitor()
        else:
            print ("process still running")

        # only does stuff when nothings already in process
        # findme todo: handle better with button enable etc.
        if not isProcessing:
            if not isWatching:
                isWatching = True
                self.setWindowTitle("Watch mode: running...")
                # starts a new watch function on a new thread

            # switch flag for reset command
            if not isFirst:
                print("isReset " + str(isReset))
                isReset = True




    def makeFocusGroup(self):
        # do creates a new focus group.  Opptionally moves files into subfolder or do on packdown?
        print("make new focus group")



def watch_capture():
    global app
    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()
    doc = Metashape.app.document

    # findme todo: must be a smarter way than all these globals? Need
    # initialize global flags and variables    
    global chunk
    global isFirst
    global isWatching
    global isProcessing
    global photos_path
    global _photo_list # a cached photolist as shim for file transfer issues
    global isReset
    global isNewFocus
    global isOn
    global m

    # set global variables
    chunk = doc.chunk
    isWatching = False      # always start without the watch enabled, even if processing stages were left running
    isNewFocus = False      # flag so the next bactch of photos added are placed in a new calibration 
    isOn = True
    _photo_list = list()

    
    # reset the monitor thread
    if 'm' in globals():
        # STILL WORKING ON THE LAST PROCESS
        isOn=True
        print("thread liveth, wait for processing to end then restart metashape")
        print(m)
    else:
        print("the thread is dead, long live the thread")
        isProcessing = False
    isReset = False
    isFirst = True  
    # checks for existing alignment so reset is used if an alignment already exists
    for camera in chunk.cameras:
        if camera.transform:
            isFirst=False
    #        isReset = True         # flag that rejiggers whole alignment from the beginning

    

    # Get the folder to watch 
    # Metashape now uses slash (/) not backslash (\).
    # findme todo: make relative to current project rather than rely on choosing each launch
    photos_path = Metashape.app.getExistingDirectory("Select root folder for projects.")


    # launch the dialogue box. Script runs til dialogue closes.
    dlg = watchDlg(parent)



    
label = "Scripts/Watch and Capture" 
Metashape.app.addMenuItem(label, watch_capture)
print("To execute this script press {}".format(label))


