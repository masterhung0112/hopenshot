""" 
 @file
 @brief This file loads and saves settings 
"""

import os

from PyQt5.QtCore import QStandardPaths, QCoreApplication

from classes import info
from classes.logger import log
from classes.json_data import JsonDataStore

def get_settings():
    return QCoreApplication.instance().settings

class SettingStore(JsonDataStore):
    def __init__(self):
        super(JsonDataStore, self).__init__()
        self.data_type = "user settings"
        self.settings_filename = "openshot.settings"
        self.default_settings_filename = os.path.join(info.PATH, 'settings', '_default.settings')
    
    def get_all_settings(self):
        """ Get the entire list of settings (with all metadata) """
        return self._data
        
    def set(self, key, value):
        """ Store setting, but adding isn't allowed. All possible settings must be in default settings file. """
        key = key.lower()

        # Load user setting's values (for easy merging)
        user_values = {}
        for item in self._data:
            if "setting" in item and "value" in item:
                user_values[item["setting"].lower()] = item

        # Save setting
        if key in user_values:
            user_values[key]["value"] = value
        else:
            log.warn("{} key '{}' not valid. The following are valid: {}".format(self.data_type, key,
                                                                                 list(self._data.keys())))
    
    def load(self):
        """ Load user settings file from disk, merging with allowed settings in default settings file.
        Creates user settings if missing. """
        # Default and user settings objects
        default_settings, user_settings = {}, {}

        # try to load default settings, on failure will raise exception to caller
        default_settings = self.read_from_file(self.default_settings_filename)

        # Try to find user settings file
        file_path = os.path.join(info.USER_PATH, self.settings_filename)

        # Load user settings (if found)
        if os.path.exists(file_path.encode('UTF-8')):

            # Will raise exception to caller on failure to read
            user_settings = self.read_from_file(file_path)

        # Merge default and user settings, excluding settings not in default, Save settings
        self._data = self.merge_settings(default_settings, user_settings)

        # Return success of saving user settings file back after merge
        return self.write_to_file(file_path, self._data)
        
    def save(self):
        """ Save user settings file to disk """

        # Try to find user settings file
        file_path = os.path.join(info.USER_PATH, self.settings_filename)

        # try to save data to file, will raise exception on failure
        self.write_to_file(file_path, self._data)
    
