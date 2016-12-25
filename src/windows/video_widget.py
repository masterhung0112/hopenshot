from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPalette

from classes.app import get_app

import openshot

class VideoWidget(QWidget):
    
    def paintEvent(self, event, *args):
        
        # Paint custom frame image on QWidget
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fill background black
        painter.fillRect(event.rect(), self.palette().window())
        
        if self.current_image:
            # DRAW FRAME
            # Calculate new frame image size, maintaining aspect ratio
            pixSize = self.current_image.size()
            pixSize.scale(event.rect().size(), Qt.KeepAspectRatio)
            
            # Scale the image
            scaledPix = self.current_image.scaled(pixSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Calculate center of QWidget and draw image
            center = self.centeredViewport(self.width(), self.height())
            painter.drawImage(center, scaledPix)
    
    def SetAspectRatio(self, new_aspect_ratio, new_pixel_ratio):
        """ Set a new aspect ratio """
        self.aspect_ratio = new_aspect_ratio
        self.pixel_ratio = new_pixel_ratio
    
    def centeredViewport(self, width, height):
        """ Calculate size of viewport to maintain apsect ratio """
        aspectRatio = self.aspect_ratio.ToFloat() * self.pixel_ratio.ToFloat()
        heightFromWidth = width / aspectRatio
        widthFromHeight = height * aspectRatio
        
        if heightFromWidth <= height:
            return QRect(0, (height - heightFromWidth) / 2, width, heightFromWidth)
        else:
            return QRect((width - widthFromHeight) / 2, 0, widthFromHeight, height)
    
    def present(self, image, *args):
        
        # Get frame's QImage from libopenshot
        self.current_image = image
        # Force repaint on this widget
        self.repaint()
    
    def connectSignals(self, renderer):
        """ Connect signals to renderer """
        renderer.present.connect(self.present)
    
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        
        # Init aspect ratio settings (default values)
        self.aspect_ratio = openshot.Fraction()
        self.pixel_ratio = openshot.Fraction()
        self.aspect_ratio.num = 16
        self.aspect_ratio.den = 9
        self.pixel_ratio.num = 1
        self.pixel_ratio.den = 1
        
        p = QPalette()
        p.setColor(QPalette.Window, Qt.black)
        super().setPalette(p)
        
        # Init current frame's QImage
        self.current_image = None
        
        # Get a reference to the window object
        self.win = get_app().window
