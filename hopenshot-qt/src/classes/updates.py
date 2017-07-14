from classes.logger import log

try:
    import json
except ImportError:
    import simplejson as json

class UpdateWatcher:
    """ Interface for classes that listen for 'undo' and 'redo' events. """

    def updateStatusChanged(self, undo_status, redo_status):
        """ Easily be notified each time there are 'undo' or 'redo' actions available in the UpdateManager. """
        raise NotImplementedError("updateStatus() not implemented in UpdateWatcher implementer.")

class UpdateInterface:
    def changed(self, action):
        raise NotImplementedError("changed() not implemented in UpdateInterface implementer.")

class UpdateAction:
    """A data structure representing a single update manager action, including any necessary data to reverse the action."""
    
    def __init__(self, type=None, key=[], values=None, partial_update=False):
        self.type = type  # insert, update, or delete
        self.key = key  # list which contains the path to the item, for example: ["clips",{"id":"123"}]
        self.values = values
        self.old_values = None
        self.partial_update = partial_update
    
    def set_old_values(self, old_vals):
        self.old_values = old_vals
    
    def json(self, is_array=False, only_value=False):
        """ Get the JSON string representing this UpdateAction """
        
        # Build the dictionary to be serialized
        if only_value:
            data_dict = self.values
        else:
            data_dict = {"type": self.type,
                         "key": self.key,
                         "value": self.values,
                         "partial": self.partial_update}
        
        if not is_array:
            # Use a JSON Object as the root object
            update_action_dict = data_dict
        else:
            # Use a JSON Array as the root object
            update_action_dict = [data_dict]

        # Serialize as JSON
        return json.dumps(update_action_dict)
        
    def load_json(self, value):
        """ Load this UpdateAction from a JSON string """
        # Set the Update Action properties
        self.type = update_action_dict["type"]
        self.key = update_action_dict["key"]
        self.values = update_action_dict["value"]
        self.old_values = update_action_dict["old_value"]
        self.partial_update = update_action_dict["partial"]

class UpdateManager:
    """ This class is used to track and distribute changes to listeners. Typically, only 1 instance of this class is needed,
    and many different listeners are connected with the add_listener() method. """
    
    def __init__(self):
        self.statusWatchers = []  # List of watchers
        self.updateListeners = []
        self.redoHistory = []  # List of actions undone
        self.actionHistory = []  # List of actions performed to current state
        self.currentStatus = [None, None]  # Status of Undo and Redo buttons (true/false for should be enabled)
        self.ignore_history = False # Ignore saving actions to history, to prevent a huge undo/redo list
        self.last_action = None
        
    def add_listener(self, listener, index=-1):
        if not listener in self.updateListeners:
            if index <= -1:
                self.updateListeners.append(listener)
            else:
                self.updateListeners.insert(index, listeners)
        else:
            log.warn("Listener already added")
    
    def update_watchers(self):
        """ Notify all watchers if any 'undo' or 'redo' actions are available. """

        new_status = (len(self.actionHistory) >= 1, len(self.redoHistory) >= 1)
        if self.currentStatus[0] != new_status[0] or self.currentStatus[1] != new_status[1]:
            for watcher in self.statusWatchers:
                watcher.updateStatusChanged(*new_status)
    
    # Carry out an action on all listeners
    def dispatch_action(self, action):
        """ Distribute changes to all listeners (by calling their changed() method) """
        
        try:
            # Loop through all listeners
            for listener in self.updateListeners:
                # Invoke change method on listener
                listener.changed(action)

        except Exception as ex:
            log.error("Couldn't apply '{}' to update listener: {}\n{}".format(action.type, listener, ex))
        self.update_watchers()
    
    # Perform new actions, clearing redo history for taking a new path
    def insert(self, key, values):
        """ Insert a new UpdateAction into the UpdateManager (this action will then be distributed to all listeners) """
        
        self.last_action = UpdateAction('insert', key, values)
        self.redoHistory.clear()
        if not self.ignore_history:
            self.actionHistory.append(self.last_action)
        self.dispatch_action(self.last_action)
