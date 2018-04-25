# ##### BEGIN GPL LICENSE BLOCK #####
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
# based on display tools from Jordi Vall-llovera Medina and Jhon Wallace 


# LOAD MODUL #    
import bpy
from bpy import *
from bpy.props import *


class VIEW3D_TP_Remove_Modifier_Mirror(bpy.types.Operator):
    """remove modifier mirror"""
    bl_idname = "tp_ops.remove_mod_mirror"
    bl_label = "Remove Mirror Modifier"
    bl_options = {'REGISTER', 'UNDO'}
  
    def execute(self, context):
        scene = bpy.context.scene
        selected = bpy.context.selected_objects 
        
        if not(selected):    
            for obj in bpy.data.objects:        
                obj = bpy.context.scene.objects.active
                     
                for modifier in obj.modifiers: 
                    if (modifier.type == 'MIRROR'):
                        obj.modifiers.remove(modifier)

        else:
            for obj in selected:
                
                for modifier in obj.modifiers:    
                    if (modifier.type == 'MIRROR'):
                        obj.modifiers.remove(modifier)
                        
        return {'FINISHED'}


class VIEW3D_TP_Render_On_Off(bpy.types.Operator):
    '''render on / off'''
    bl_idname = "tp_ops.mods_render"
    bl_label = "Render"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        is_apply = True
        message_a = ""

        for mod in context.active_object.modifiers:
            if (mod.show_render):
                is_apply = False
                break
        for obj in context.selected_objects:
            for mod in obj.modifiers:
                mod.show_render = is_apply

        if is_apply:
            message_a = "All Render ON"
        else:
            message_a = "All Render OFF"

        self.report(type={"INFO"}, message=message_a)
                    
        return {'FINISHED'}
        
        

class VIEW3D_TP_Modifier_On_Off(bpy.types.Operator):
    '''view on / off'''
    bl_idname = "tp_ops.mods_view"
    bl_label = "View"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        is_apply = True
        message_a = ""

        for mod in context.active_object.modifiers:
            if (mod.show_viewport):
                is_apply = False
                break
        for obj in context.selected_objects:
            for mod in obj.modifiers:
                mod.show_viewport = is_apply

        if is_apply:
            message_a = "All View ON"
        else:
            message_a = "All View OFF"

        self.report(type={"INFO"}, message=message_a)

                    
        return {'FINISHED'}
    


class VIEW3D_TP_Edit_On_Off(bpy.types.Operator):
    '''edit on / off'''
    bl_idname = "tp_ops.mods_edit"
    bl_label = "Edit"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        is_apply = True
        message_a = ""

        for mod in context.active_object.modifiers:
            if (mod.show_in_editmode):
                is_apply = False
                break
        for obj in context.selected_objects:
            for mod in obj.modifiers:
                mod.show_in_editmode = is_apply

        if is_apply:
            message_a = "All Edit ON"
        else:
            message_a = "All Edit OFF"

        self.report(type={"INFO"}, message=message_a)

                    
        return {'FINISHED'}
        


class VIEW3D_TP_Cage_On_Off(bpy.types.Operator):
    '''cage  on / off'''
    bl_idname = "tp_ops.mods_cage"
    bl_label = "Cage"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        is_apply = True
        message_a = ""

        for mod in context.active_object.modifiers:
            if (mod.show_on_cage):
                is_apply = False
                break
        for obj in context.selected_objects:
            for mod in obj.modifiers:
                mod.show_on_cage = is_apply

        if is_apply:
            message_a = "All Cage ON"
        else:
            message_a = "All Cage OFF"

        self.report(type={"INFO"}, message=message_a)

                    
        return {'FINISHED'}
    
    
# REGISTRY #        
def register():    
    bpy.utils.register_module(__name__)

def unregister():   
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()