# ##### BEGIN GPL LICENSE BLOCK #####
#
# (C) 2017 MKB
#
#  This program is free software; you can redistribute it and / or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#


# LOAD MODUL #    
import bpy
from bpy import *
from bpy.props import *
from . icons.icons import load_icons  

EDIT = ["EDIT_MESH", "EDIT_CURVE", "EDIT_SURFACE", "EDIT_LATTICE", "EDIT_METABALL", "EDIT_ARMATURE"]

EDIT_REST = ["EDIT_CURVE", "EDIT_SURFACE", "EDIT_LATTICE", "EDIT_METABALL", "EDIT_ARMATURE"]

# UI: HOTKEY MENU PIE # 
class VIEW3D_MT_originset_menu_pie(bpy.types.Menu):
    bl_label = "OriginSet"
    bl_idname = "VIEW3D_MT_originset_menu_pie"

    def draw(self, context):
        layout = self.layout
       
        menu_prefs = context.preferences.addons[__package__].preferences

        icons = load_icons()  

        layout.operator_context = 'INVOKE_REGION_WIN'

        pie = layout.menu_pie()            

        #Box 1 L
        layout = pie.split().column()
        layout.label (text="WIP")
      
        #Box 2 R
        layout = pie.split().column()
        layout.label (text="WIP")
       
        #Box 3 B
        layout = pie.split().column()
        layout.label (text="WIP")

        #Box 4 T 
        layout = pie.split().column()
        layout.label (text="WIP")

        #Box 5 LT
        layout = pie.split().column()
        layout.label (text="WIP")

        #Box 6 RT 
        layout = pie.split().column()
        layout.label (text="WIP")

        #Box 7 LB 
        layout = pie.split().column()
        layout.label (text="WIP")
      
        #Box 8 RB
        layout = pie.split().column()
        layout.label (text="WIP")       

