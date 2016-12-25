import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QToolBar, QLineEdit, QActionGroup, 
    QWidget, QSizePolicy, QFileDialog)
from PyQt5.QtGui import QKeySequence 

from classes import info, ui_utils, settings 
from classes.app import get_app
from classes.logger import log

from windows.video_widget import VideoWidget
from windows.views.file_listview import FilesListView

class MainWindow(QMainWindow):
    
    # Path to ui file
    ui_path = os.path.join(info.PATH, 'windows', 'ui', 'main-window.ui')
        
    def getShortcutByName(self, setting_name):
        """ Get the key sequence back from the setting name"""
        s = settings.get_settings()
        shortcut = QKeySequence(s.get(setting_name))
        return shortcut
        
    def SetWindowTitle(self):
        """ Set the window title based on a variety of factors """
        
        _ = get_app()._tr  # Get translation function
        
        self.setWindowTitle(_("OpenShot Video Editor"))
    
    def setup_toolbars(self):
        _ = get_app()._tr  # Get translation function
        
        # Start undo and redo actions disabled
        self.actionUndo.setEnabled(False)
        self.actionRedo.setEnabled(False)
        
        # Add files toolbar =================================================================================
        self.filesToolbar = QToolBar("Files Toolbar")
        self.filesActionGroup = QActionGroup(self)
        self.filesActionGroup.setExclusive(True)
        self.filesActionGroup.addAction(self.actionFilesShowAll)
        self.filesActionGroup.addAction(self.actionFilesShowVideo)
        self.filesActionGroup.addAction(self.actionFilesShowAudio)
        self.filesActionGroup.addAction(self.actionFilesShowImage)
        self.actionFilesShowAll.setChecked(True)
        self.filesToolbar.addAction(self.actionFilesShowAll)
        self.filesToolbar.addAction(self.actionFilesShowVideo)
        self.filesToolbar.addAction(self.actionFilesShowAudio)
        self.filesToolbar.addAction(self.actionFilesShowImage)
        self.filesFilter = QLineEdit()
        self.filesFilter.setObjectName("fileFilter")
        self.filesFilter.setPlaceholderText(_("Filter"))
        self.filesToolbar.addWidget(self.filesFilter)
        self.actionFilesClear.setChecked(False)
        self.filesToolbar.addAction(self.actionFilesClear)
        self.tabFiles.layout().addWidget(self.filesToolbar)
        
        # Add transitions toolbar =================================================================================
        
        # Add effects toolbar =================================================================================
        
        # Add Video Preview toolbar ==========================================================================
        self.videoToolbar = QToolBar("Video Toolbar")
        
        # Add left spacer
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.videoToolbar.addWidget(spacer)
        
        # Playback controls
        self.videoToolbar.addAction(self.actionJumpStart)
        self.videoToolbar.addAction(self.actionRewind)
        self.videoToolbar.addAction(self.actionPlay)
        self.videoToolbar.addAction(self.actionFastForward)
        self.videoToolbar.addAction(self.actionJumpEnd)
        self.actionPlay.setCheckable(True)
        
        # Add right spacer
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.videoToolbar.addWidget(spacer)

        self.tabVideo.layout().addWidget(self.videoToolbar)
        
        # Add Timeline toolbar ================================================================================
    
    
    def actionImportFiles_trigger(self, event):
        app = get_app()
        _ = app._tr
        recommended_path = app.project.current_filepath
        if not recommended_path:
            recommended_path = os.path.join(info.HOME_PATH)
        files = QFileDialog.getOpenFileNames(self, _("Import File..."), recommended_path)[0]
        for file_path in files:
            self.filesTreeView.add_file(file_path)
            self.filesTreeView.refresh_view()
            log.info("Imported media file {}".format(file_path))
        
    
    def keyPressEvent(self, event):
        """Receive key press events for the widget."""
        
        # Detect the current KeySequence pressed (including modifier keys)
        key_value = event.key()
        modifiers = int(event.modifiers())
        
        if (key_value > 0 and key_value != Qt.Key_Shift and key_value != Qt.Key_Alt and
            key_value != Qt.Key_Control and key_value != Qt.Key_Meta):
                # A valid key sequence
                key = QKeySequence(modifiers + key_value)
        else:
            # No valid key sequence detected
            return
        
        # Get the video player object
        
        # Get framerate
        
        # Basic shortcuts i.e just a letter
        
        # Boiler plate key mappings (mostly for menu support on Ubuntu/Unity)
        if key.matches(self.getShortcutByName("actionImportFiles")) == QKeySequence.ExactMatch:
            self.actionImportFiles.trigger()
        
        # Debug
        log.info("keyPressEvent: %s" % (key.toString()))
        
                
    def __init__(self, mode=None):
        QMainWindow.__init__(self)
        self.mode = mode    # None or unittest (None is normal usage)
        
        _ = get_app()._tr
        # set window on app for reference during initialization of children
        get_app().window = self
        
        # Load UI from designer
        ui_utils.load_ui(self, self.ui_path)
        
        # Load user settings for window
        s = settings.get_settings()
        self.recent_menu = None
        
        # Setup the toolbars
        self.setup_toolbars()
        
        # Set Window title
        self.SetWindowTitle()
        
        # Setup files tree
        if s.get("file_view") == "details":
            self.filesTreeView = FilesTreeView(self)
        else:
            self.filesTreeView = FilesListView(self)
        self.tabFiles.layout().addWidget(self.filesTreeView)
        
        # Setup the video preview
        self.videoPreview = VideoWidget(self)
        self.tabVideo.layout().insertWidget(0, self.videoPreview)
        
        # Init UI
        ui_utils.init_ui(self)
        
        # Show window
        if not self.mode == "unittest":
            self.show()
