import os
import copy

from classes import info
from classes.app import get_app

# Get project data reference
app = get_app()
project = app.project

class QueryObject:
    """ This class allows one or more project data objects to be queried """
    def __init__(self):
        self.id = None  # Unique ID of object
        self.key = None  # Key path to object in project data
        self.data = None  # Data dictionary of object
        self.parent = None  # Only used with effects (who belong to clips)
        self.type = "insert"  # Type of operation needed to save
    
    def save(self, OBJECT_TYPE):
        if not self.id and self.type == "insert":
            
            self.id = project.generate_id()
            
            self.data["id"] = copy.deepcopy(self.id)
            
            if not self.key:
                self.key = copy.deepcopy(OBJECT_TYPE.object_key)
                self.key.append({"id": self.id})
            
            # Insert into project data
            app.updates.insert(copy.deepcopy(OBJECT_TYPE.object_key), copy.deepcopy(self.data))
            
            self.type = "update"
        elif self.id and self.type == "update":

            # Update existing project data
            app.updates.update(self.key, self.data)
    
    def delete(self, OBJECT_TYPE):
        if self.id and self.type == "update":
            app.updates.delete(self.key)
            self.type = "delete"
            
    def title(self):
        return None
    
    def filter(OBJECT_TYPE, **kwargs):
        """ Take any arguments given as filters, and find a list of matching objects """
        
        # Get a list of all objects of this type
        parent = project.get(OBJECT_TYPE.object_key)
        matching_objects = []
        
        if parent:
            for child in parent:
                match = True
                for key, value in kwargs.items():
                    if key in child and not child[key] == value:
                        match = False
                        break;
                    elif key == 'intersect':
                        if (child.get("position", 0) > value or 
                            child.get("position", 0) + (child.get("end", 0) - child.get("start", 0)) < value):
                            match = False
                
                if match:
                    object = OBJECT_TYPE()
                    object.id = child["id"]
                    object.key = [OBJECT_TYPE.object_name, {"id": object.id }]
                    object.data = child
                    object.type = "update"
                    matching_objects.append(object)
                    
        return matching_objects
    
    def get(OBJECT_TYPE, **kwargs):
        """ Take any arguments given as filters, and find the first matching object """
        
        # Look for matching objects
        matching_objects = QueryObject.filter(OBJECT_TYPE, **kwargs)
        
        if matching_objects:
            return matching_objects[0]
        else:
            return None
            

class File(QueryObject):
    """ This class allows Files to be queried, updated, and deleted from the project data. """
    object_name = "files"  # Derived classes should define this
    object_key = [object_name]  # Derived classes should define this also
    
    def save(self):
        super().save(File)
    
    def delete(self):
        """ Delete the object from the project data store """
        super().delete(File)
        
    def filter(**kwargs):
        return QueryObject.filter(File, **kwargs)
        
    def get(**kwargs):
        return QueryObject.get(File, **kwargs)
