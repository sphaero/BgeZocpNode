import bpy
import sys
import time
import json
import socket
import zmq

from zocp import ZOCP
from mathutils import Vector

try:
    import bge
except Exception as e:
    print("This module needs to be run inside the Blender Game Engine!")
    raise(e)

class BgeZOCP(ZOCP):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_node_name("BGE@" + socket.gethostname())
        self._register_game_objects()
        self._register_light_objects()
        
    def _register_game_objects(self):
        print(bge.logic.getCurrentScene().objects)
        for object in bge.logic.getCurrentScene().objects:
           print(object.name, object.attrDict)
           self.set_object(object.name, "KX_GameObject")
           #self.register_vec3f("worldPosition",      object.worldPosition)
           #self.register_mat3f("worldOrientation",   object.worldOrientation)
           #self.register_vec3f("worldScale",         object.worldScale)
           self.register_bool ("visible",            object.visible)
           #self.register_vec3f("color",              object.color)
           self.register_int  ("state",              object.state)
           self.register_float("mass",               object.mass)

    def _register_light_objects(self):
        for object in bge.logic.getCurrentScene().lights:
           print(object.name)
           if object.type == "SPOT":
               self.set_object(object.name, "SPOT_KX_LightObject")
           elif object.type == "SUN":
               self.set_object(object.name, "SUN_KX_LightObject")
           else:
               self.set_object(object.name, "NORMAL_KX_LightObject")
           self.register_vec3f("worldPosition",      object.worldPosition[:])
           #self.register_mat3f("worldOrientation",   object.worldOrientation)
           #self.register_vec3f("worldScale",         object.worldScale)
           self.register_bool ("visible",            object.visible)
           #self.register_vec3f("color",              object.color)
           self.register_int  ("state",              object.state)
           self.register_float("mass",               object.mass)
           self.register_float("energy",             object.energy)
           self.register_float("distance",           object.distance)

    #########################################
    # ZOCP Event methods
    #########################################
    def on_peer_modified(self, peer, data, *args, **kwargs):
        print("ZOCP MODIFIED: %s modified %s" %(peer.hex, args))
        for key, val in data.items():
            if key == "objects":
                for objname, newvals in val:
                    self.update_game_objects(objname, newvals)
        
    def update_game_object(self, object, data):
        obj = bge.logic.getCurrentScene().objects.get(object)
        if obj:
            for key, val in data.items():
                setattr(obj, key, val) 
