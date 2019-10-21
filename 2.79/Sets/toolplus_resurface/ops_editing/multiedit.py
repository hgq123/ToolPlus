# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
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
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


#bl_info = {  
#     "name": "MultiEdit",  
#     "author": "Antonis Karvelas",  
#     "version": (0, 2),  
#     "blender": (2, 7, 0),  
#     "location": "VIEW 3D > Tools > Multiple Objects Editing ",  
#     "description": "Allows you to edit multiple objects together in edit mode without destroying data",  
#     "warning": "Alpha Version 0.2, needs testing...",  
#     "wiki_url": "",  
#     "tracker_url": "",  
#     "category": "Mesh"}  


import bpy

#Create a list to put the names of the selected objects:
name_list = []

#Create a list to put the names of the duplicated objects:
duplicated_list = [] 

special_vgroups_list = []

class MultiEdit_Enter(bpy.types.Operator):
    bl_label = "MultiEdit Enter"
    bl_idname = "tp_ops.multiedit_enter_operator"
    
    def execute(self, context):
        #Check the type and the number of the objects:
        object_list = bpy.context.selected_objects
        for obj in object_list:
          if obj.type != "MESH":
               obj.select = False
          else:
               pass
        new_object_list = bpy.context.selected_objects
        if len(new_object_list) >= 2:
            self.enter(new_object_list)
        else:
            bpy.ops.object.mode_set(mode = 'EDIT')    
        return {'FINISHED'}
    
    def enter(self, objects):
        #Create lists and vertex groups
        copied = 0
        for object in objects:
            #Duplicate Objects
            self.duplicateObject(bpy.context.scene, (object.name + "_dupl" + str(copied)),object)
            duplicated_list.append(object.name + "_dupl" + str(copied))
            copied += 1
            name_list.append(object.name)
            #Create Vertex Groups
            bpy.context.scene.objects.active = object
            for vert_group in object.vertex_groups:
             #  object.vertex_groups.remove(vert_group)
               special_vgroups_list.append(vert_group.name)
            object.vertex_groups.new(object.name)
            vertex_group = object.vertex_groups[-1]
            verts = []
            for vert in object.data.vertices:
                verts.append(vert.index)
                vertex_group.add(verts, 1.0, 'ADD')
        
            #Move duplicated to diferent layer
            bpy.ops.object.select_all(action = 'DESELECT')
            bpy.data.objects[(object.name + "_dupl" + str(copied - 1))].select = True
            bpy.ops.object.move_to_layer(layers=((False,)*19 +(True,))) 
            
            object.select = True
            for modifier in object.modifiers:
                object.modifiers.remove(modifier)
            for constraint in object.constraints:
                object.constraints.remove(constraint)    
                        
        for object in objects:
            bpy.data.objects[object.name].select = True
        bpy.ops.object.join()        
        bpy.context.active_object.name = "MultiEdit"
        bpy.ops.object.mode_set(mode = 'EDIT')            
        
    
    
    #DuplicateObject function
    def duplicateObject(self, scene, name, copyobj):
 
        # Create new mesh
        mesh = bpy.data.meshes.new(name)
 
        # Create new object associated with the mesh
        ob_new = bpy.data.objects.new(name, mesh)
 
        # Copy data block from the old object into the new object
        ob_new.data = copyobj.data.copy()
        ob_new.scale = copyobj.scale
        ob_new.location = copyobj.location
 
        # Link new object to the given scene and select it
        scene.objects.link(ob_new)
        for mod in copyobj.modifiers:
            mod_new = ob_new.modifiers.new(mod.name, mod.type)
            properties = [p.identifier for p in mod.bl_rna.properties
                          if not p.is_readonly]
            for prop in properties:
                setattr(mod_new, prop, getattr(mod, prop))
        for constr in copyobj.constraints:
            constr_new = ob_new.constraints.new(constr.type)
            properties = [p.identifier for p in constr.bl_rna.properties
                          if not p.is_readonly]
            for prop in properties:
                setattr(constr_new, prop, getattr(constr, prop))        
        for vertex_g in copyobj.vertex_groups:
          vert_g_new = ob_new.vertex_groups.new(vertex_g.name)
          properties = [p.identifier for p in vertex_g.bl_rna.properties
                          if not p.is_readonly]
          for prop in properties:
               setattr(vert_g_new, prop, getattr(vertex_g, prop))
        return ob_new
    
    
    
class MultiEdit_Exit(bpy.types.Operator):
    bl_label = "MultiEdit Exit"
    bl_idname = "tp_ops.multiedit_exit_operator"
    bl_context = "editmode"
    
    def execute(self,context):
        obj = bpy.context.active_object
        name = obj.name
        vgroup_index = 0 
               
        #SEPARATES OBJECTS
        
        for vertex_group in obj.vertex_groups:
            bpy.ops.object.mode_set(mode = 'EDIT') 
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.mesh.select_mode(type="VERT")
            bpy.ops.object.mode_set(mode = 'OBJECT')
            #obj.vertex_groups.active_index = (obj.vertex_groups).index(vertex_group)
            for vert in obj.data.vertices:
                for vertGroup in vert.groups:
                    if vertGroup.group == vgroup_index:
                        if vertex_group.name in special_vgroups_list:
                            break 
                        else:
                            vert.select = True  
                    else:
                         pass
                         
            bpy.ops.object.mode_set(mode = 'EDIT') 
            try:
                bpy.ops.mesh.separate(type="SELECTED")
            except:
               pass
            vgroup_index += 1
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        #REMOVES VERTEX GROUPS
        
        existing_vg = []
        object_layer = bpy.context.scene.active_layer
        for object in bpy.context.selected_objects:
            del existing_vg[:]
            vgroup_index = 0 
            for vg in object.vertex_groups:
                bpy.ops.object.mode_set(mode = 'EDIT') 
                bpy.ops.mesh.select_all(action = 'DESELECT')
                bpy.ops.object.mode_set(mode = 'OBJECT')
                #finding which vertex group has verts
                for vert in object.data.vertices:
                    for vertGroup in vert.groups:
                         if vertGroup.group == vgroup_index:
                              vert.select = True  
                              if object.vertex_groups[vgroup_index].name in special_vgroups_list:
                                   pass
                              elif object.vertex_groups[vgroup_index].name in existing_vg:
                                   pass
                              else:
                                   existing_vg.append(object.vertex_groups[vgroup_index].name)
                               
                    vgroup_index += 1                           
                #object.vertex_groups.remove(vg)
                    
            #RENAMES OBJECTS, ORGANIZES MATERIALS
            
            print(existing_vg)     
            if len(existing_vg) < 2:
                try:
                    object.name = existing_vg[0]
                    wanted_object_name = duplicated_list[(name_list.index(object.name))]
                    #print(existing_vg[-1])
                    #print(name_list)
                    #print(duplicated_list)
                    mats = []
                      
                    for slot in object.material_slots:
                        for slot_dupl in bpy.data.objects[wanted_object_name].material_slots:
                            if slot_dupl.name == slot.name:
                                mats.append(slot_dupl.name)
                            else:
                                pass
                              
                        
                    for mat_index in range(len(object.material_slots)):
                        try:
                         if object.material_slots[mat_index].name in mats:
                            pass
                           
                         else:    
                            bpy.context.scene.objects.active = object
                            #mat_index = object.material_slots[slot_dupl].index
                            object.active_material_index = mat_index
                            bpy.ops.object.material_slot_remove()
                        except:
                         pass
                    #All those things copy modifiers, constraints etc. with all properties. Cool...                    
                    for mod in bpy.data.objects[wanted_object_name].modifiers:
                        mod_new = object.modifiers.new(mod.name, mod.type)
                        properties = [p.identifier for p in mod.bl_rna.properties
                                        if not p.is_readonly]
                        for prop in properties:
                            setattr(mod_new, prop, getattr(mod, prop))
                                
                    for constr in bpy.data.objects[wanted_object_name].constraints:
                        constr_new = object.constraints.new(constr.type)
                        properties = [p.identifier for p in constr.bl_rna.properties
                                      if not p.is_readonly]
                        for prop in properties:
                            setattr(constr_new, prop, getattr(constr, prop))        
                    
                    #for vertex_g in bpy.data.objects[wanted_object_name].vertex_groups:
                    #     vert_g_new = object.vertex_groups.new(vertex_g.name)
                     #    properties = [p.identifier for p in vertex_g.bl_rna.properties
                      #             if not p.is_readonly]
                       #  for prop in properties:
                        #      setattr(vert_g_new, prop, getattr(vertex_g, prop))
                    for vgroup in object.vertex_groups:
                         if vgroup.name in bpy.data.objects[(duplicated_list[(name_list.index(object.name))])].vertex_groups:
                              pass
                         else:
                              object.vertex_groups.remove(vgroup)
                    for shape_key in object.data.shape_keys.key_blocks:
                         try:
                              bpy.context.scene.objects.active = object
                              if shape_key.name in bpy.data.objects[(duplicated_list[(name_list.index(object.name))])].data.shape_keys.key_blocks:
                                  print(object.name)#pass
                              else:
                                  print("here as well")
                                  idx = object.data.shape_keys.key_blocks.keys().index(shape_key.name)
                                  object.active_shape_key_index = idx
                                  bpy.ops.object.shape_key_remove()
                         except:
                              idx = object.data.shape_keys.key_blocks.keys().index(shape_key.name)
                              object.active_shape_key_index = idx
                              bpy.ops.object.shape_key_remove()
                        
                except:
                    pass                                           
            else:
                object.name = "New Geometry"
                
        
        #Deleting objects
        bpy.ops.object.select_all(action="DESELECT")
        try:
            bpy.data.objects["MultiEdit"].select = True
            vert_check = bpy.data.objects["MultiEdit"]
            if len(vert_check.data.vertices) > 0:
                pass#name_list.append(vert_check.name)
            else:
                bpy.ops.object.delete()   
        except:
            pass
                      
        #Check if checkbox is true and keep or not the original origin point(pun intended)
        if bpy.context.scene.Keep_Origin_Point:
            for obj in bpy.data.objects:
                for nam in name_list:
                    if nam == obj.name:
                        obj.select = True
                        bpy.context.scene.cursor_location = bpy.data.objects[duplicated_list[name_list.index(nam)]].location
                        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
                        obj.select = False 
                    else:
                        pass
        else:
            for obj in bpy.data.objects:
                for nam in name_list:
                    if nam in obj.name:
                        obj.select = True
                        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
                    
                    else:
                        pass  
        
        
        #Delete duplicated objects 
        self.selectLayer(20)
        bpy.ops.object.select_all(action="SELECT")
        for obj in bpy.context.selected_objects:
            if "dupl" not in obj.name:
                obj.select = False
        bpy.ops.object.delete()
        
        #Return to original layer
        self.selectLayer(object_layer + 1)
        
        #Empty lists for future use
        del name_list[:]
        del duplicated_list[:]
        del special_vgroups_list[:]
        return {'FINISHED'}
    
    def selectLayer(self, layer):
        layers = [False] * 20
        layers[layer - 1] = True
        bpy.context.scene.layers = layers    
    
   
    
#class MultiEdit_Panel(bpy.types.Panel):
#    bl_label = "Multiple Objects Editing"
#    bl_idname = "MultiEdit"
#    bl_space_type = "VIEW_3D"
#    bl_region_type = "TOOLS"
#    bl_category = "Tools"
#    
#    def draw(self, context):
#         layout = self.layout
#         sce = bpy.context.scene  
#         
#         layout.operator(MultiEdit_Enter.bl_idname)  #icon = something
#         layout.operator(MultiEdit_Exit.bl_idname)
#         layout.prop(sce, "Keep_Origin_Point")
#        


    
def register():
    bpy.utils.register_class(MultiEdit_Enter)
    bpy.utils.register_class(MultiEdit_Exit)
#    bpy.utils.register_class(MultiEdit_Panel)
    bpy.types.Scene.Keep_Origin_Point = bpy.props.BoolProperty ( name = "Keep Origin Point", description = "Keep the origin points of the objects, else reset origin to geometry.", default = True )
if __name__ == "__main__":
    register()            
            
