import os
import openshot

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QListView, QAbstractItemView, QMessageBox

from classes.app import get_app
from classes.logger import log
from classes.query import File
from windows.models.files_model import FilesModel

try:
    import json
except ImportError:
    import simplejson as json

class FilesListView(QListView):
    """ A ListView QWidget used on the main window """
    drag_item_size = 48
    
    def refresh_view(self):
        self.files_model.update_model()
    
    def __init__(self, *args):
        super(QListView, self).__init__(*args)
        
        app = get_app()
        self.win = app.window
        
        # Get Model data
        self.files_model = FilesModel()
        self.setAcceptDrops(True)
        self.setDragEnabled(False)
        self.setDropIndicatorShown(True)
        self.selected = []
        self.ignore_image_sequence_paths = []
        
        # Setup header columns
        self.setModel(self.files_model.model)
        self.setIconSize(QSize(131, 108))
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setUniformItemSizes(True)
        self.setWordWrap(True)
        self.setStyleSheet("QListView::item { padding-top: 2px; }")
        
        # Refresh view
        self.refresh_view()
    
    def is_image(self, file):
        path = file["path"].lower()

        if path.endswith((".jpg", ".jpeg", ".png", ".bmp", ".svg", ".thm", ".gif", ".bmp", ".pgm", ".tif", ".tiff")):
            return True
        else:
            return False
    
    def add_file(self, filepath):
        path, filename = os.path.split(filepath)
        
        # Add file into project
        app = get_app()
        _ = app._tr
        
        file = File.get(path=filepath)
        
        if file:
            return
        
        clip = openshot.Clip(filepath)
        
        #try:
        reader = clip.Reader()
        file_data = json.loads(reader.Json())
        if file_data["has_video"] and not self.is_image(file_data):
            file_data["media_type"] = "video"
        elif file_data["has_video"] and self.is_image(file_data):
            file_data["media_type"] = "image"
        elif file_data["has_audio"] and not file_data["has_video"]:
            file_data["media_type"] = "audio"
                
        file = File()
        file.data = file_data
            
        file.save()
        return True
            
        #except Exception as e:
        #    # Handle exception
        #    msg = QMessageBox()
        #    msg.setText(_("{} is not a valid video, audio, or image file.\n{}".format(filename, e)))
        #    msg.exec_()
        #    return False
            
