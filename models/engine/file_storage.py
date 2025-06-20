#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import json
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    Serializes instances to a JSON file and
    deserializes JSON file to instances.

    Attributes:
        __file_path (str): path to the JSON file
        __objects (dict): stores all instantiated objects
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns all objects, or only those of a specific class.

        Args:
            cls (type, optional): Class type to filter objects

        Returns:
            dict: all objects or filtered by class
        """
        if cls is not None:
            filtered_objects = {
                key: obj for key, obj in self.__objects.items()
                if isinstance(obj, cls)
            }
            return filtered_objects
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to __objects

        Args:
            obj (BaseModel): the object to store
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file
        """
        json_dict = {
            key: obj.to_dict() for key, obj in self.__objects.items()
        }
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(json_dict, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if file exists)
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = value["__class__"]
                    self.__objects[key] = eval(class_name)(**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it exists.

        Args:
            obj (BaseModel, optional): the object to delete
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(key, None)  # safe delete

    def close(self):
        """
        Calls reload() to deserialize the JSON file
        """
        self.reload()
