# -*- coding: utf-8 -*-
#
#     This file is part of BgeZocpNode. Copyright 2013 Stichting z25.org
#
#     BgeZocpNode is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     BgeZocpNode is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with PartyTechApp.  If not, see <http://www.gnu.org/licenses/>.
#
#
# adaptation from example script of using threads in Blender 2.55 game engine
# thread(!) in ba: http://blenderartists.org/forum/showthread.php?t=204802
# Example of terminating thread is from here:
# http://bytes.com/topic/python/answers/45247-terminating-thread-parent
#
# make sure you keep the python script active through the logic bricks!!!!!
# (always activate TRUE, Level TRUE)

try:
    import bge
except Exception as e:
    print("This module needs to be run inside the Blender Game Engine!")
    raise(e)
import queue

import time

# class that is responsible for stopping thread (thanks to moguri@blenderartists)
class object_ptr():
    def __init__(self, obj, cleanup_method):
        print("creating object_ptr")
        self.object = obj
        self.cleanup = cleanup_method
        
    def __del__(self):
        print("deleting object_ptr")
        try:
            self.cleanup()
            # give a second to cleanup
            time.sleep(1)
        except Exception as e:
            print("Threadobject's 'cleanup' method is missing, this should not happen", e)
        # self.thread.terminate() # not in Threads

# run this script only once
ob = bge.logic.getCurrentController().owner

def init():
    if not ob.get('init'):
        print("ZOCP INITIALISING")
        from z25 import BgeZOCP
        import socket
        znode = BgeZOCP.BgeZOCP()
        znode.set_node_name("BGE@"+ socket.gethostname())
        bge.logic.cleanup_object = object_ptr(znode, znode.stop)
        ob['ZOCP'] = znode
        ob['init'] = 1
        
        
def process_zocp():
    if ob.get('init'):
        znode = ob.get('ZOCP')
        if znode:
            znode.run_once(0)
