from PyQt5.QtWidgets import QApplication

from classes import languages, info, project_data, settings, updates
from classes.logger import log

def get_app():
    return QApplication.instance()

class OpenShotApp(QApplication):
    
    def __init__(self, *argv, mode=None):
        QApplication.__init__(self, *argv)
        
        # Setup the application
        self.setApplicationName('openshot')
        self.setApplicationVersion(info.SETUP['version'])
        
        # Init settings
        self.settings = settings.SettingStore()
        try:
            self.settings.load()
        except Exception as ex:
            log.error("Couldn't load user settings. Exiting. Msg: {}".format(ex))
            exit()
        
        # Init translation system
        languages.init_languages()
        
        # Tests of project data loading/sav
        self.project = project_data.ProjectDataStore()
        
        # Init Update Manager
        self.updates = updates.UpdateManager()
        
        # It is important that the project is the first listener if the key gets update
        self.updates.add_listener(self.project)
        
        from windows.main_window import MainWindow
        self.window = MainWindow(mode)
    
    def _tr(self, message):
        return self.translate('', message)
    
    def run(self):
        res = self.exec_()
        return res
