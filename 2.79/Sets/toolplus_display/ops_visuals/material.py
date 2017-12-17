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



# LOAD MODUL #    
import bpy
from bpy import *
from bpy.props import *   
from bpy.types import WindowManager

    
class VIEW3D_TP_Visual_Object_Materials(bpy.types.Operator):
    """Add a new Material and enable Color Object"""
    bl_idname = "tp_ops.material_add"
    bl_label = "Object Material Color"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object
        
        bpy.ops.object.material_slot_remove() 
 
        bpy.ops.tp_ops.material_one()

        return {'FINISHED'}


bpy.types.WindowManager.col_mat_surface = bpy.props.FloatVectorProperty(name='', description='Surface Color', default=(0.92, 0.9, 0.84), min=0, max=1, step=1, precision=3, subtype='COLOR_GAMMA', size=3)

class VIEW3D_TP_Visual_One_Material(bpy.types.Operator):
    """Add Material"""
    bl_idname = "tp_ops.material_one"
    bl_label = "Add MAT"
    bl_options = {'REGISTER', 'UNDO'}  
 
    #replace = bpy.props.BoolProperty(name = "Replace", description = "replace existing material", default = False, options = {'SKIP_SAVE'})
    all = bpy.props.BoolProperty(name = "to all in Scene", description = "add material to all in scene or only to selected", default = False)
    obj_color = bpy.props.BoolProperty(name="Use Object Color", description="Value", default=False)

    def execute(self, context): 
        wm = bpy.context.window_manager
        scn = bpy.context.scene
        obj = bpy.context.active_object
        
        mat_name = ('MAT_'+ obj.name)
        mat = bpy.data.materials.new(mat_name)                    
        mat.diffuse_color = wm.col_mat_surface   
        #mat.specular_intensity = 0   

        if self.all == True:
            tp_obj = bpy.context.scene.objects
        else:
            tp_obj = bpy.context.selected_objects

        add_to_slot = [o for o in tp_obj if o.type == 'MESH' and o.is_visible(scn)]

        for obj in add_to_slot:  
            scn.objects.active = obj          

            obj.data.materials.append(mat)           
        
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.material_slot_assign()

        for  i in range(self.obj_color):
            bpy.context.object.active_material.use_object_color = True

        return {'FINISHED'}






class VIEW3D_TP_Visual_List_Materials(bpy.types.Menu): 
    """apply material to object or mesh"""
    bl_idname = "tp_ops.material_list"
    bl_label = "Material List"

    def draw(self, context):
        layout = self.layout

        for mat in bpy.data.materials:  
            name = mat.name
            try:
                icon_val = layout.icon(mat)
            except:
                icon_val = 1
                print ("WARNING [Mat Panel]: Could not get icon value for %s" % name)
            op = layout.operator("tp_ops.assign_material", text=name, icon_value=icon_val)
            op.mat_to_assign = name
            

        
class VIEW3D_TP_Visual_Assign_Materials(bpy.types.Operator):
    bl_idname = "tp_ops.assign_material"
    bl_label = "Assign Material"
 
    mat_to_assign = bpy.props.StringProperty(default="")
 
    def execute(self, context):

        if context.mode == 'EDIT_MESH':
            obj = context.object
            bm = bmesh.from_edit_mesh(obj.data)
 
            selected_face = [f for f in bm.faces if f.select]          
 
            mat_name = [mat.name for mat in bpy.context.object.material_slots if len(bpy.context.object.material_slots)]
 
            if self.mat_to_assign in mat_name:
                context.object.active_material_index = mat_name.index(self.mat_to_assign) 
                bpy.ops.object.material_slot_assign() 
            else: 
                bpy.ops.object.material_slot_add()
                bpy.context.object.active_material = bpy.data.materials[self.mat_to_assign] 
                bpy.ops.object.material_slot_assign() 
            return {'FINISHED'}

        elif context.object.mode == 'OBJECT':
 
            obj_list = [obj.name for obj in context.selected_objects]
 
            for obj in obj_list:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[obj].select = True                
                bpy.context.scene.objects.active = bpy.data.objects[obj]
                bpy.context.object.active_material_index = 0
 
                if self.mat_to_assign == bpy.data.materials:
                    bpy.context.active_object.active_material = bpy.data.materials[mat_name]
 
                else:
                    if not len(bpy.context.object.material_slots):
                        bpy.ops.object.material_slot_add()
 
                    bpy.context.active_object.active_material = bpy.data.materials[self.mat_to_assign]
 
            for obj in obj_list:
                bpy.data.objects[obj].select = True
 
            return {'FINISHED'}   
                                               
        elif context.mode == 'EDIT_CURVE': 
            obj = context.object        
            
            bpy.ops.object.material_slot_add()
            bpy.context.object.active_material = bpy.data.materials[self.mat_to_assign] 
            bpy.ops.object.material_slot_assign() 
            return {'FINISHED'}



class VIEW3D_TP_Visual_Delete_Materials(bpy.types.Operator):
    """Remove all materials slots / Value Slider"""
    bl_idname = "tp_ops.remove_all_material"
    bl_label = "Delete all Material"
    bl_options = {'REGISTER', 'UNDO'}

    deleteMat = bpy.props.IntProperty(name="Delete Material-Slots", description="Value", default=1, min=1, soft_max=500, step=1)
    
    def draw(self, context):
        layout = self.layout

        box = layout.box().column(1)   

        row = box.row(1)                
        row.prop(self,'deleteMat', text="Delete Material-Slots")         

        
    def execute(self, context):                

        if context.object.mode == 'EDIT':
                bpy.ops.object.editmode_toggle()      
                bpy.ops.object.material_slot_remove()
                bpy.ops.object.editmode_toggle()
        else:
            for i in range(self.deleteMat):
                bpy.ops.object.material_slot_remove()

        return {'FINISHED'}




#http://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Materials/Multiple_Materials
bpy.types.WindowManager.col_material_wire = bpy.props.FloatVectorProperty(name='', description='Wire Color idx1', default=(0.0 ,0.0 ,0.1), min=0, max=1, step=1, precision=3, subtype='COLOR_GAMMA', size=3)
bpy.types.WindowManager.col_material_surface = bpy.props.FloatVectorProperty(name='', description='Surface Color idx0', default=(0.92, 0.9, 0.84), min=0, max=1, step=1, precision=3, subtype='COLOR_GAMMA', size=3)

class VIEW3D_TP_Visual_Wire_Material(bpy.types.Operator):
    """Add Wire Material"""
    bl_idname = "tp_ops.material_wire"
    bl_label = "WireMat"
    bl_options = {'REGISTER', 'UNDO'}  

    all = bpy.props.BoolProperty(name = "to all in Scene", description = "add material to all in scene or only to selected", default = False)

    def execute(self, context): 
        wm = bpy.context.window_manager
        scn = bpy.context.scene

        if 'material_surface' not in bpy.data.materials:
            mat = bpy.data.materials.new('material_surface')
            mat.specular_intensity = 0
        else: mat = bpy.data.materials.get('material_surface')
        mat.diffuse_color = wm.col_material_surface

        if 'material_wire' not in bpy.data.materials:
            mat = bpy.data.materials.new('material_wire')
            mat.specular_intensity = 0
            mat.use_transparency = True
            mat.type = 'WIRE'
            mat.offset_z = 0.05
        else: mat = bpy.data.materials.get('material_wire')
        mat.diffuse_color = wm.col_material_wire

        if self.all == True:
            tp_obj = bpy.context.scene.objects
        else:
            tp_obj = bpy.context.selected_objects

        add_to_slot = [o for o in tp_obj if o.type == 'MESH' and o.is_visible(scn)]

        for obj in add_to_slot:
            scn.objects.active = obj

            for mat in obj.material_slots:
                bpy.ops.object.material_slot_remove()

            obj.data.materials.append(bpy.data.materials.get('material_wire'))
            obj.data.materials.append(bpy.data.materials.get('material_surface'))
            obj.material_slots.data.active_material_index = 1

            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.material_slot_assign()
            bpy.ops.object.mode_set()

        return {'FINISHED'}




class VIEW3D_TP_Visual_Purge_Materials(bpy.types.Operator):
    '''Purge orphaned materials'''
    bl_idname="tp_ops.purge_unused_material"
    bl_label="Purge Materials"
    
    def execute(self, context):

        target_coll = eval("bpy.data.materials")

        for item in target_coll:
            if item.users == 0:
                target_coll.remove(item)

        return {'FINISHED'}


class VIEW3D_TP_Visual_Quad_Toggle(bpy.types.Operator):
    """Quad View"""
    bl_idname = "tp_ops.quad_toggle"
    bl_label = "Quad View"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.screen.region_quadview()
        return {'FINISHED'}
    


class VIEW3D_TP_Visual_OBJECT_OT_hide_select_clear(bpy.types.Operator):
    """Unlocks all visible objects"""
    bl_idname = "object.hide_select_clear"
    bl_label = "Clear All Restrict Select"

    def execute(self, context):
        scn = context.scene
        active_layers = [i for i, l in enumerate(scn.layers) if l]
        for obj in scn.objects:
            for i in active_layers:
                if obj.layers[i] and not obj.hide and obj.hide_select:
                    #unlock them
                    obj.hide_select = False
        
        return {'FINISHED'}



class VIEW3D_TP_Visual_FAKE_OPS(bpy.types.Operator):
    """do nothing"""
    bl_idname = "tp_ops.fake_ops"
    bl_label = "Do Nothing"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        print
        return {'FINISHED'}



# SPECIAL MENU #
def menu_func(self, context):
    self.layout.separator()
    self.layout.operator("tp_ops.remove_all_material", text="Del. MAT-Slots", icon='DISCLOSURE_TRI_DOWN')
    self.layout.operator("tp_ops.purge_unused_material", text="Purge Unused", icon="PANEL_CLOSE")   
   

# REGISTRY #        
def register():    
    bpy.utils.register_module(__name__)
    bpy.types.MATERIAL_MT_specials.append(menu_func)

def unregister():   
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()