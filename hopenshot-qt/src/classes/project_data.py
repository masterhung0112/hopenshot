import os
import random
import copy
import shutil
import glob

from classes.json_data import JsonDataStore
from classes.updates import UpdateInterface
from classes import info, settings
from classes.logger import log

class ProjectDataStore(JsonDataStore):

    def __init__(self):
        JsonDataStore.__init__(self)
        self.data_type = "project data"  # Used in error messages
        self.default_project_filepath = os.path.join(info.PATH, 'settings', '_default.project')
        
        # Set default filepath to user's home folder
        self.current_filepath = None
        
        # Track changes after save
        self.has_unsaved_changes = False
        
        # Load default project data on creation
        self.new()
    
    # Load default project data
    def new(self):
        """ Try to load default project settings file, will raise error on failure """
        import openshot
        
        self._data = self.read_from_file(self.default_project_filepath)
        self.current_filepath = None
        self.has_unsaved_changes = False

        # Get default profile
        s = settings.get_settings()
        default_profile = s.get("default-profile")
        
        # Loop through profiles
        for profile_folder in [info.USER_PROFILES_PATH, info.PROFILES_PATH]:
            for file in os.listdir(profile_folder):
                # Load Profile and append description
                profile_path = os.path.join(profile_folder, file)
                profile = openshot.Profile(profile_path)

                if default_profile == profile.info.description:
                    log.info("Setting default profile to %s" % profile.info.description)

                    # Update default profile
                    self._data["profile"] = profile.info.description
                    self._data["width"] = profile.info.width
                    self._data["height"] = profile.info.height
                    self._data["fps"] = {"num" : profile.info.fps.num, "den" : profile.info.fps.den}
        
        # Get the default audio settings for the timeline (and preview playback)
        default_sample_rate = int(s.get("default-samplerate"))
        default_channel_ayout = s.get("default-channellayout")

        channels = 2
        channel_layout = openshot.LAYOUT_STEREO
        if default_channel_ayout == "LAYOUT_MONO":
            channels = 1
            channel_layout = openshot.LAYOUT_MONO
        elif default_channel_ayout == "LAYOUT_STEREO":
            channels = 2
            channel_layout = openshot.LAYOUT_STEREO
        elif default_channel_ayout == "LAYOUT_SURROUND":
            channels = 3
            channel_layout = openshot.LAYOUT_SURROUND
        elif default_channel_ayout == "LAYOUT_5POINT1":
            channels = 6
            channel_layout = openshot.LAYOUT_5POINT1
        elif default_channel_ayout == "LAYOUT_7POINT1":
            channels = 8
            channel_layout = openshot.LAYOUT_7POINT1

        # Set default samplerate and channels
        self._data["sample_rate"] = default_sample_rate
        self._data["channels"] = channels
        self._data["channel_layout"] = channel_layout
        
    
    def get(self, key):
        """ Get copied value of a given key in data store """
        
        # Verify key is valid type
        if not isinstance(key, list):
            log.warning("get() key must be a list. key: {}".format(key))
            return None
        if not key:
            log.warning("Cannot get empty key.")
            return None
        
        # Get reference to internal data structure
        obj = self._data
        
        # Iterate through key list finding sub-objects either by name or by an object match criteria such as {"id":"ADB34"}.
        for key_index in range(len(key)):
            key_part = key[key_index]
            
            # Key_part must be a string or dictionary
            if not isinstance(key_part, dict) and not isinstance(key_part, str):
                log.error("Unexpected key part type: {}".format(type(key_part).__name__))
                return None
            
            # If key_part is a dictionary and obj is a list or dict, each key is tested as a property of the items in the current object
            # in the project data structure, and the first match is returned.
            if isinstance(key_part, dict) and isinstance(obj, list):
                # Overall status of finding a matching sub-object
                found = False
                
                # Loop through each item in object to find match
                for item_index in range(len(obj)):
                    item = obj[item_index]
                    # True until something disqualifies this as a match
                    match = True
                    # Check each key in key_part dictionary and if not found to be equal as a property in item, move on to next item in list
                    for subkey in key_part.keys():
                        # Get each key in dictionary (i.e. "id", "layer", etc...)
                        subkey = subkey.lower()
                        # If object is missing the key or the values differ, then it doesn't match.
                        if not (subkey in item and item[subkey] == key_part[subkey]):
                            match = False
                            break
                    # If matched, set key_part to index of list or dict and stop loop
                    if match:
                        found = True
                        obj = item
                        break
                # No match found, return None
                if not found:
                    return None
            
            # If key_part is a string, homogenize to lower case for comparisons
            if isinstance(key_part, str):
                key_part = key_part.lower()
                
                # Check current obj type (should be dictionary)
                if not isinstance(obj, dict):
                    log.warn(
                        "Invalid project data structure. Trying to use a key on a non-dictionary object. Key part: {} (\"{}\").\nKey: {}".format(
                            (key_index), key_part, key))
                    return None
                
                
                # If next part of path isn't in current dictionary, return failure
                if not key_part in obj:
                    log.warn("Key not found in project. Mismatch on key part {} (\"{}\").\nKey: {}".format((key_index),
                                                                                                           key_part,
                                                                                                           key))
                    return None

                # Get the matching item
                obj = obj[key_part]
        
        # After processing each key, we've found object, return copy of it
        return copy.deepcopy(obj)
        
    def _set(self, key, values=None, add=False, partial_update=False, remove=False):
        """ Store setting, but adding isn't allowed. All possible settings must be in default settings file. """
        
        log.info(
            "_set key: {} values: {} add: {} partial: {} remove: {}".format(key, values, add, partial_update, remove))
        parent, my_key = None, ""
        
        # Verify key is valid type
        if not isinstance(key, list):
            log.warning("_set() key must be a list. key: {}".format(key))
            return None
        if not key:
            log.warning("Cannot set empty key.")
            return None
        
        # Get reference to internal data structure
        obj = self._data
        
        # Iterate through key list finding sub-objects either by name or by an object match criteria such as {"id":"ADB34"}.
        for key_index in range(len(key)):
            key_part = key[key_index]
            
            # Key_part must be a string or dictionary
            if not isinstance(key_part, dict) and not isinstance(key_part, str):
                log.error("Unexpected key part type: {}".format(type(key_part).__name__))
                return None
            
            # If key_part is a dictionary and obj is a list or dict, each key is tested as a property of the items in the current object
            # in the project data structure, and the first match is returned.
            if isinstance(key_part, dict) and isinstance(obj, list):
                # Overall status of finding a matching sub-object
                found = False
                
                # Loop through each item in object to find match
                for item_index in range(len(obj)):
                    item = obj[item_index]
                    # True until something disqualifies this as a match
                    match = True
                    
                    # Check each key in key_part dictionary and if not found to be equal as a property in item, move on to next item in list
                    for subkey in key_part.keys():
                        # Get each key in dictionary (i.e. "id", "layer", etc...)
                        subkey = subkey.lower()
                        # If object is missing the key or the values differ, then it doesn't match.
                        if not (subkey in item and item[subkey] == key_part[subkey]):
                            match = False
                            break
                    # If matched, set key_part to index of list or dict and stop loop
                    if match:
                        found = True
                        obj = item
                        my_key = item_index
                        break
                
                # No match found, return None
                if not found:
                    return None
                    
            # If key_part is a string, homogenize to lower case for comparisons
            if isinstance(key_part, str):
                key_part = key_part.lower()

                # Check current obj type (should be dictionary)
                if not isinstance(obj, dict):
                    return None

                # If next part of path isn't in current dictionary, return failure
                if not key_part in obj:
                    log.warn("Key not found in project. Mismatch on key part {} (\"{}\").\nKey: {}".format((key_index),
                                                                                                           key_part,
                                                                                                           key))
                    return None

                # Get sub-object based on part key as new object, continue to next part
                obj = obj[key_part]
                my_key = key_part
                
            # Set parent to the last set obj (if not final iteration)
            if key_index < (len(key) - 1) or key_index == 0:
                parent = obj
                
        # After processing each key, we've found object and parent, return former value/s on update
        ret = copy.deepcopy(obj)
        
        # Apply the correct action to the found item
        if remove:
            del parent[my_key]

        else:

            # Add or Full Update
            # For adds to list perform an insert to index or the end if not specified
            if add and isinstance(parent, list):
                # log.info("adding to list")
                parent.append(values)

            # Otherwise, set the given index
            elif isinstance(values, dict):
                # Update existing dictionary value
                obj.update(values)

            else:

                # Update root string
                self._data[my_key] = values

        # Return the previous value to the matching item (used for history tracking)
        return ret
        
    def changed(self, action):
        """ This method is invoked by the UpdateManager each time a change happens (i.e UpdateInterface) """
        # Track unsaved changes
        self.has_unsaved_changes = True
        
        if action.type == "insert":
            # Insert new item
            old_vals = self._set(action.key, action.values, add=True)
            action.set_old_values(old_vals)  # Save previous values to reverse this action

        elif action.type == "update":
            # Update existing item
            old_vals = self._set(action.key, action.values, partial_update=action.partial_update)
            action.set_old_values(old_vals)  # Save previous values to reverse this action

        elif action.type == "delete":
            # Delete existing item
            old_vals = self._set(action.key, remove=True)
            action.set_old_values(old_vals)  # Save previous values to reverse this action
    
    # Utility methods
    def generate_id(self, digits=10):
        """ Generate random alphanumeric ids """

        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        id = ""
        for i in range(digits):
            c_index = random.randint(0, len(chars) - 1)
            id += (chars[c_index])
        return id
