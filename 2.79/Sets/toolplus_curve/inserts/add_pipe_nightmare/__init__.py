'''
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
'''

#bl_info = {
#	'name': 'Pipe Nightmare',
#	'author': 'Trentin Frederick (proxe)',
#	'version': (0, 2, 28),
#	'blender': (2, 78, 0),
#	'location': 'View 3D \N{Rightwards Arrow} Add \N{Rightwards Arrow} Curve \N{Rightwards Arrow} Pipes',
#	'description': 'Create random pipes.',
#	# 'warning': '',
#	# 'wiki_url': '',
#	# 'tracker_url': '',
#	'category': 'Object'
#}

import bpy
from bpy.utils import register_module, unregister_module

from toolplus_curve.inserts.add_pipe_nightmare import interface, operator


# REGISTRY #        
def register():    
    bpy.utils.register_module(__name__)

def unregister():   
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()