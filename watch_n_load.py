# small script to watch a folder and process.


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
       print("Watch mode closed. Running processes will continue")
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



    # loads photos in the input folder and checks they don't already exist in thr project (assumes unique photo names)
    
    def load_photos(self):
        print("loading photos")
        global isProcessing
        isProcessing = True


        print(photos_path)

        file_list = os.listdir(photos_path)

        photo_list = list()

        camera_list = list()
        for camera in chunk.cameras:
            camera_list.append(camera.label)


        # iterate through the file list to check for valid file types and uniqueness
        for file in file_list:

            ext = file.rsplit(".",1)[1].lower()
            basename = file.rsplit(".",1)[0]
            # only includes valid image files
            # findme todo: refine this. currently restricted to smaller sized images for speedier loading, "tif", "tiff", "dng"
            # excludes temporary files that have ~ in the name
            if ext in ["jpg", "jpeg", "jxl", "heic", "heif"]:
                if basename not in camera_list and '~' not in basename:
                    photo_list.append("/".join([photos_path, file]))


        if photo_list:

            chunk.addPhotos(photo_list)
            # continue to next processing stage

            print (str(len(photo_list)) + "new photos added")
            return True

        else:
            print ('no photos to add.')
            return False
        

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

        print("isProcessing = " + str(isProcessing))
        print("isReset = " + str(isReset))
        print("isFirst = " + str(isFirst))


        isProcessing = True
        
        #findme todo:  add a merge markers step to have only one detect markers event on iterative captures
            # see https://www.agisoft.com/forum/index.php?topic=10112.0
            # detectMarkers(target_type=CircularTarget12bit, tolerance=25, filter_mask=False, inverted=False, noparity=False, maximum_residual=5, minimum_size=0, minimum_dist=5, cameras=photo_list)
        
        p = self.load_photos()        

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
            print ("resetting alignment and markers")
            # reset alignment and realign using some of the existing information
            # findme debug next: something fishy with the behaviour sometimes breaks or left unfinished

            # findme todo: add a merge markers step to have only one detect markers on photo-import
            # findme todo: expose or preset the tolerance. set low due to DoF issues with 
            
            isReset = False
            chunk.remove(chunk.markers)
            chunk.point_cloud.removeKeypoints()
            Metashape.app.update()

            # findme todo: allow for reduction of markers to avoid clusters and redetect more after final final alignment (?)
            chunk.detectMarkers(target_type=Metashape.CircularTarget12bit, tolerance=20, filter_mask=False, inverted=False, noparity=False, maximum_residual=5, minimum_size=0, minimum_dist=5)

            Metashape.app.update()
            for frame in chunk.frames:
                frame.matchPhotos(downscale=4, reset_matches=True, keep_keypoints=True, generic_preselection=False, reference_preselection=True, reference_preselection_mode=Metashape.ReferencePreselectionEstimated, mask_tiepoints=False)
                # findme todo: add some nuances for dealing with different masks and failed alignments at later stages of processing?
                Metashape.app.update()

            chunk.alignCameras(reset_alignment=True)
            Metashape.app.update()


        elif isWatching:
            print ("adding images if they exist")
            if p:
                # add new images to existing alignment
                for frame in chunk.frames:
                    frame.matchPhotos(downscale=4, reset_matches=False, keep_keypoints=True, generic_preselection=True, reference_preselection=True, reference_preselection_mode=Metashape.ReferencePreselectionSource, mask_tiepoints=True)
                    Metashape.app.update()
                chunk.alignCameras(reset_alignment=False)
                Metashape.app.update()

        isProcessing = False
        print ("Stopped processing... waiting and watching")

    # async loop handler. Will run in the background checking if there is anything to process every
    def monitor(self):
        global timer
        global m


        print ("folder watch started")
        ##### findme todo: consider watchdog package for filesystem response ####

        if isWatching:
            print("watching")
            self.watcher()

        else:
            print("not watching stopped")

        app.processEvents()

        # uses a flag to stop the script when the window is closed
        # but allows active processing events to carry on in the background if theyæve started
        # findme todo: restructure with signals to put processing in main thread
        if isOn:
            time.sleep(3)
            # findme todo: bypass the recurrance limit in python in a nice way
            print("timeout = " + str(timer))
            timer = timer - 1
            self.monitor()
        else:
            print("end of watch process deleting the monitor")
            del m
            # findme todo next: something might be getting stuck in a loop and the thread isn't being deleted.
            

#------------------  button actions -----------

    # changes the status flag to stop the watching next time the timer loops out
    def watch_pause(self):
        global isWatching
        global isFirst

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
    global isReset
    global isNewFocus
    global isOn
    global m

    # set global variables
    chunk = doc.chunk
    isWatching = False      # always start without the watch enabled, even if processing stages were left running
    isNewFocus = False      # flag so the next bactch of photos added are placed in a new calibration 
    isOn = True

    
    # reset the monitor thread
    if 'm' in globals():
        # STILL WORKING ON THE LAST PROCESS
        isOn=True
        print("thread liveth")
        print(m)
    else:
        print("the thread is dead, long live the thread")
        isProcessing = False
    isReset = False
    isFirst = True
    # checks for existing alignment to choose appropriate alignment settings
    for camera in chunk.cameras:
        if camera.transform:
            isFirst=False
            isReset = True         # flag that rejiggers whole alignment from the beginning

    

    # Get the folder to watch 
    # Metashape now uses slash (/) not backslash (\).
    # findme todo: make relative to current project rather than rely on choosing each launch
    photos_path = Metashape.app.getExistingDirectory("Select root folder for projects.")


    # launch the dialogue box. Script runs til dialogue closes.
    dlg = watchDlg(parent)



    
label = "Scripts/Watch and Capture" 
Metashape.app.addMenuItem(label, watch_capture)
print("To execute this script press {}".format(label))


