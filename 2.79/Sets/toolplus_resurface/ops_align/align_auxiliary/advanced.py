# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#
# ***** END GPL LICENCE BLOCK *****


#bl_info = {
#    "name": "Advanced Align Tools",
#    "author": "Lell, Anfeo",
#    "version": (0, 8, 0),
#    "blender": (2, 6, 3),
#    "location": "View3D > Specials (W)",
#    "description": "Tools to align object, pivots and cursor, align rotation and scale",
#    "warning": "some functions in development",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "User Changed"}

import bpy, mathutils
from mathutils import Vector, Matrix
from bpy.props import EnumProperty, BoolProperty, FloatVectorProperty 

#subject 0 per oggetto, 1 per pivot e 2 per cursor
def align_function(subject, active_too, consistent, self_or_active, loc_x, loc_y, loc_z, ref1, ref2, loc_offset, 
        rot_x, rot_y, rot_z, rot_offset, scale_x, scale_y, scale_z, scale_offset,
         fit_x, fit_y, fit_z):
               
    sel_obj = bpy.context.selected_objects
    act_obj = bpy.context.active_object
    
    global sel_max
    global sel_min
    global sel_center
    global ref2_co
    
    def get_reference_points(obj, space):
        
        me = obj.data
        co_list = []
        #let's get all the points coodinates
        if space == "global":
            ok = False
            obj_mtx = obj.matrix_world                                                           
            if obj.type == 'MESH' and len(me.vertices) > 0:                    
                ok = True                
                for p in me.vertices:
                    co_list.append((obj_mtx * p.co))    
#            elif obj.type == 'CURVE' and len(me.splines) > 0:
#                ok = True                
#                for s in me.splines:
#                    for p in s.bezier_points:
#                        co_list.append((obj_mtx * p.co))
            elif obj.type == 'SURFACE' and len(me.splines) > 0:
                ok = True                
                for s in me.splines:
                    for p in s.points:
                        co_list.append((obj_mtx * p.co))
            elif obj.type == 'FONT' and len(me.splines) > 0:
                ok = True                
                for s in me.splines:
                    for p in s.bezier_points:
                        co_list.append((obj_mtx * p.co))
         
        elif space == "local":            
            ok = False                                                           
            if obj.type == 'MESH' and len(me.vertices) > 0:                    
                ok = True                
                for p in me.vertices:
                    co_list.append(p.co)    
#            elif obj.type == 'CURVE' and len(me.splines) > 0:
#                ok = True                
#                for s in me.splines:
#                    for p in s.bezier_points:
#                        co_list.append(p.co)
            elif o.type == 'SURFACE' and len(me.splines) > 0:
                ok = True                
                for s in me.splines:
                    for p in s.points:
                        co_list.append(p.co)
            elif o.type == 'FONT' and len(o.data.splines) > 0:
                ok = True                
                for s in me.splines:
                    for p in s.bezier_points:
                        co_list.append(p.co)                 
        
        #se è stato trovato un punto valido
        #procedo a calcolare gli estremi
        if ok:            
            max_x = co_list[0][0]
            min_x = co_list[0][0]
            max_y = co_list[0][1]
            min_y = co_list[0][1]
            max_z = co_list[0][2]
            min_z = co_list[0][2]
            
            for v in co_list:                                
                
                #confronto le coord della lista con le minori e maggiori trovate
                #in modo da trovare le minori e maggiori per ogni asse
                act_x = v[0]
                if act_x > max_x:    max_x = act_x
                if act_x < min_x:    min_x = act_x
                    
                act_y = v[1]
                if act_y > max_y:    max_y = act_y
                if act_y < min_y:    min_y = act_y 
                    
                act_z = v[2]
                if act_z > max_z:    max_z = act_z
                if act_z < min_z:    min_z = act_z
                                
        else:
            #altrimenti uso il pivot dell'oggetto
            a = obj.location
            min_x = a[0]
            max_x = a[0] 
            min_y = a[1]
            max_y = a[1]
            min_z = a[2]
            max_z = a[2]
        
        center_x = min_x + ((max_x - min_x) / 2)
        center_y = min_y + ((max_y - min_y) / 2)
        center_z = min_z + ((max_z - min_z) / 2)               
        
        reference_points = [min_x, center_x, max_x, min_y, center_y, max_y, min_z, center_z, max_z]    
        return reference_points
    
    def get_sel_ref(ref_co, sel_obj): #cerco i punti estremi della selezione
        
        sel_min = ref_co.copy()
        sel_max = ref_co.copy() 
        
        for obj in sel_obj:
            if obj != act_obj or (active_too and obj == act_obj):
                
                ref_points = get_reference_points(obj, "global")
                ref_min = Vector([ref_points[0], ref_points[3], ref_points[6]])
                ref_max = Vector([ref_points[2], ref_points[5], ref_points[8]])


                if ref_min[0] < sel_min[0]:
                    sel_min[0] = ref_min[0]
                if ref_max[0] > sel_max[0]:
                    sel_max[0] = ref_max[0]
                if ref_min[1] < sel_min[1]:
                    sel_min[1] = ref_min[1]
                if ref_max[1] > sel_max[1]:
                    sel_max[1] = ref_max[1]
                if ref_min[2] < sel_min[2]:
                    sel_min[2] = ref_min[2]
                if ref_max[2] > sel_max[2]:
                    sel_max[2] = ref_max[2]
                    
        return sel_min, sel_max;
                    
                    
    def find_ref2_co(act_obj):
        #contiene le coordinate del punto di riferimento per il posizionamento
        if ref2 == "0":        
            ref_points = get_reference_points(act_obj, "global")
            ref2_co = [ref_points[0], ref_points[3], ref_points[6]]           
            ref2_co = Vector(ref2_co)
        elif ref2 == "1":
            ref_points = get_reference_points(act_obj, "global")
            ref2_co = [ref_points[1], ref_points[4], ref_points[7]]     
            ref2_co = Vector(ref2_co)
        elif ref2 == "2":
            ref2_co = act_obj.location
            ref2_co = Vector(ref2_co)
        elif ref2 == "3":    
            ref_points = get_reference_points(act_obj, "global")
            ref2_co = [ref_points[2], ref_points[5], ref_points[8]]                 
            ref2_co = Vector(ref2_co)
        elif ref2 == "4":
            ref2_co = bpy.context.scene.cursor_location                    

        return ref2_co
    
    def find_new_coord(obj):
                
        ref_points = get_reference_points(obj, "global") 

        if loc_x == True:
            if ref1 == "0":                           
                min_x = ref_points[0]
                new_x = ref2_co[0] + (obj.location[0] - min_x) + loc_offset[0]
            elif ref1 == "1":
                center_x = ref_points[1]
                new_x = ref2_co[0] + (obj.location[0] - center_x) + loc_offset[0]
            elif ref1 == "2":
                new_x = ref2_co[0] + loc_offset[0]
            elif ref1 == "3":                
                max_x = ref_points[2]   
                new_x = ref2_co[0] - (max_x - obj.location[0]) + loc_offset[0] 
            obj.location[0] = new_x
        if loc_y == True:
            if ref1 == "0":            
                min_y = ref_points[3]
                new_y = ref2_co[1] + (obj.location[1] - min_y) + loc_offset[1]
            elif ref1 == "1":
                center_y = ref_points[4]
                new_y = ref2_co[1] + (obj.location[1] - center_y) + loc_offset[1]
            elif ref1 == "2":
                new_y = ref2_co[1] + loc_offset[1]
            elif ref1 == "3":                
                max_y = ref_points[5]   
                new_y = ref2_co[1] - (max_y - obj.location[1]) + loc_offset[1]        
            obj.location[1] = new_y
        if loc_z == True:
            if ref1 == "0":           
                min_z = ref_points[6]
                new_z = ref2_co[2] + (obj.location[2] - min_z) + loc_offset[2]
            elif ref1 == "1":
                center_z = ref_points[7]
                new_z = ref2_co[2] + (obj.location[2] - center_z) + loc_offset[2]
            elif ref1 == "2":
                new_z = ref2_co[2] + loc_offset[2]
            elif ref1 == "3":                
                max_z = ref_points[8]
                new_z = ref2_co[2] - (max_z - obj.location[2]) + loc_offset[2]
            obj.location[2] = new_z
    
    def find_new_rotation(obj):
        if rot_x == True:
            obj.rotation_euler[0] = act_obj.rotation_euler[0] + rot_offset[0]
        if rot_y == True:    
            obj.rotation_euler[1] = act_obj.rotation_euler[1] + rot_offset[1]
        if rot_z == True:    
            obj.rotation_euler[2] = act_obj.rotation_euler[2] + rot_offset[2]
    
    def find_new_scale(obj):
        if scale_x == True:
            obj.scale[0] = act_obj.scale[0] + scale_offset[0]
        if scale_y == True:    
            obj.scale[1] = act_obj.scale[1] + scale_offset[1]
        if scale_z == True:    
            obj.scale[2] = act_obj.scale[2] + scale_offset[2]
                    
    def find_new_dimensions(obj, ref_dim):
        ref_points = get_reference_points(obj, "local")
        if fit_x:
            dim = ref_points[2] - ref_points[0]
            obj.scale[0] = (ref_dim[0] / dim) * act_obj.scale[0] 
        if fit_y:
            dim = ref_points[5] - ref_points[3]
            obj.scale[1] = (ref_dim[1] / dim) * act_obj.scale[1] 
        if fit_z:
            dim = ref_points[8] - ref_points[6]
            obj.scale[2] = (ref_dim[2] / dim) * act_obj.scale[2]         
            
        
    def move_pivot(obj):
        me = obj.data                
        vec_ref2_co = Vector(ref2_co)       
        offset = vec_ref2_co - obj.location  
        offset_x = [offset[0] + loc_offset[0], 0, 0]
        offset_y = [0, offset[1] + loc_offset[1], 0]
        offset_z = [0, 0, offset[2] + loc_offset[2]]   
        
        def movement(vec):
            obj_mtx = obj.matrix_world.copy()
            # What's the displacement vector for the pivot?
            move_pivot = Vector(vec)
             
            # Move the pivot point (which is the object's location)
            pivot = obj.location
            pivot += move_pivot         
            
            nm = obj_mtx.inverted() * Matrix.Translation(-move_pivot) * obj_mtx

            # Transform the mesh now
            me.transform(nm) 
            
        if loc_x: 
            movement(offset_x)
        if loc_y:
            movement(offset_y)   
        if loc_z:
            movement(offset_z)
               
    def point_in_selection(act_obj, sel_obj):
        ok = False
        for o in sel_obj:
            if o != act_obj:
                ref_ob = o
                obj_mtx = o.matrix_world                   
                if o.type == 'MESH' and len(o.data.vertices) > 0:
                    ref_co = o.data.vertices[0].co.copy()
                    ref_co = obj_mtx * ref_co
                    ok = True                        
                    break
                elif o.type == 'CURVE' and len(o.data.splines) > 0:
                    ref_co = o.data.splines[0].bezier_point[0].co.copy()
                    ref_co = obj_mtx * ref_co
                    ok = True
                    break
                elif o.type == 'SURFACE' and len(o.data.splines) > 0:
                    ref_co = o.data.splines[0].points[0].co.copy()
                    ref_co = obj_mtx * ref_co
                    ok = True
                    break
                elif o.type == 'FONT' and len(o.data.splines) > 0:
                    ref_co = o.data.splines[0].bezier_points[0].co.copy()
                    ref_co = obj_mtx * ref_co
                    ok = True
                    break                   
        #se nessun oggetto aveva dati, uso la posizione di un oggetto che non fosse quello attivo
        # come punto interno della selezione        
        if ok == False:
            ref_co = ref_ob.location
        
        return ref_co    
                
    if subject == "0":
        #if act_obj.type == ('MESH' or 'FONT' or 'CURVE' or 'SURFACE'):
        if act_obj.type == 'MESH' or act_obj.type == 'FONT' or act_obj.type == 'SURFACE': #or act_obj.type == 'CURVE' 
            ref2_co = find_ref2_co(act_obj)            
        else:
            if ref2 == "4":
                ref2_co = bpy.context.scene.cursor_location
            else:    
                ref2_co = act_obj.location
   
        #nel caso di selezione consistente
        if consistent: 
            #cerco un punto che sia nello spazio della selezione           
            ref_co = point_in_selection(act_obj, sel_obj)                                

            sel_min, sel_max = get_sel_ref(ref_co, sel_obj)
                    
            sel_center = sel_min + ((sel_max - sel_min) / 2)        
            translate = [0, 0, 0]
            
            #calcolo di quanto spostare la selezione
            if ref1 == "0":                                               
                translate = ref2_co - sel_min + loc_offset
            elif ref1 == "1":
                translate = ref2_co - sel_center + loc_offset                              
            elif ref1 == "3": 
                translate = ref2_co - sel_max + loc_offset                                           
                       
            #sposto i vari oggetti    
            for obj in sel_obj:
                
                if obj != act_obj or (active_too and obj == act_obj):

                    if loc_x:
                        obj.location[0] += translate[0]
                    if loc_y:
                        obj.location[1] += translate[1]
                    if loc_z:        
                        obj.location[2] += translate[2]
        else:    #not consistent 
            for obj in sel_obj:
                if obj != act_obj:
                    if rot_x or rot_y or rot_z:
                        find_new_rotation(obj)
                
                    if fit_x or fit_y or fit_z:
                        dim = [0, 0, 0]
                        ref_points = get_reference_points(act_obj, "local")                    
                        dim[0] = ref_points[2]-ref_points[0]
                        dim[1] = ref_points[5]-ref_points[3]
                        dim[2] = ref_points[8]-ref_points[6]
                        find_new_dimensions(obj, dim)
                    
                    if scale_x or scale_y or scale_z:
                        find_new_scale(obj)    
                       
                    if loc_x or loc_y or loc_z:
                        #print("ehy", ref2_co)                             
                        find_new_coord(obj)
                    
            if active_too == True:
                if loc_x or loc_y or loc_z:
                    find_new_coord(act_obj)
                if rot_x or rot_y or rot_z:
                    find_new_rotation(act_obj)
                if scale_x or scale_y or scale_z:
                    find_new_scale(act_obj)
                #add dimensions if dim offset will be added               
            
    elif subject == "1":
        if self_or_active == "1":
            if act_obj.type == 'MESH':
                ref2_co = find_ref2_co(act_obj)
        for obj in sel_obj:
            if self_or_active == "0":
                ref2_co = find_ref2_co(obj)
            if loc_x or loc_y or loc_z:
                if obj != act_obj and obj.type == 'MESH':
                    move_pivot(obj)
        
        if active_too == True:
            if act_obj.type == 'MESH':
                if loc_x or loc_y or loc_z:
                    if self_or_active == "0":
                        ref2_co = find_ref2_co(act_obj)
                    move_pivot(act_obj)
                            
    elif subject == "2":
        if self_or_active == "1":
            if act_obj.type == 'MESH' or act_obj.type == 'FONT' or act_obj.type == 'SURFACE': #or act_obj.type == 'CURVE' 
                ref2_co = find_ref2_co(act_obj)
                ref_points = get_reference_points(act_obj, "global")
            else: 
                ref2_co = act_obj.location
                ref_points = [act_obj.location[0], act_obj.location[0], act_obj.location[0], act_obj.location[1], act_obj.location[1], act_obj.location[1], act_obj.location[2], act_obj.location[2], act_obj.location[2]]        
            
            if ref2 == "0":            
                if loc_x == True:
                    bpy.context.scene.cursor_location[0] = ref_points[0] + loc_offset[0]
                if loc_y == True:
                    bpy.context.scene.cursor_location[1] = ref_points[3] + loc_offset[1]
                if loc_z == True:
                    bpy.context.scene.cursor_location[2] = ref_points[6] + loc_offset[2]
            elif ref2 == "1":
                if loc_x == True:
                    bpy.context.scene.cursor_location[0] = ref_points[1] + loc_offset[0]
                if loc_y == True:
                    bpy.context.scene.cursor_location[1] = ref_points[4] + loc_offset[1]
                if loc_z == True:
                    bpy.context.scene.cursor_location[2] = ref_points[7] + loc_offset[2]
            elif ref2 == "2":
                if loc_x == True: bpy.context.scene.cursor_location[0] = act_obj.location[0] + loc_offset[0]
                if loc_y == True: bpy.context.scene.cursor_location[1] = act_obj.location[1] + loc_offset[1]
                if loc_z == True: bpy.context.scene.cursor_location[2] = act_obj.location[2] + loc_offset[2]
            elif ref2 == "3":
                if loc_x == True:
                    bpy.context.scene.cursor_location[0] = ref_points[2] + loc_offset[0]
                if loc_y == True:
                    bpy.context.scene.cursor_location[1] = ref_points[5] + loc_offset[1]
                if loc_z == True:
                    bpy.context.scene.cursor_location[2] = ref_points[8] + loc_offset[2]
        elif self_or_active == "2":
            ref_co = point_in_selection(act_obj, sel_obj)
            
            sel_min, sel_max = get_sel_ref(ref_co, sel_obj)
            sel_center = sel_min + ((sel_max - sel_min) / 2)
            
            if ref2 == "0":            
                if loc_x == True:
                    bpy.context.scene.cursor_location[0] = sel_min[0] + loc_offset[0]
                if loc_y == True:
                    bpy.context.scene.cursor_location[1] = sel_min[1] + loc_offset[1]
                if loc_z == True:
                    bpy.context.scene.cursor_location[2] = sel_min[2] + loc_offset[2]
            elif ref2 == "1":
                if loc_x == True:
                    bpy.context.scene.cursor_location[0] = sel_center[0] + loc_offset[0]
                if loc_y == True:
                    bpy.context.scene.cursor_location[1] = sel_center[1] + loc_offset[1]
                if loc_z == True:
                    bpy.context.scene.cursor_location[2] = sel_center[2] + loc_offset[2]
            elif ref2 == "3":
                if loc_x == True:
                    bpy.context.scene.cursor_location[0] = sel_max[0] + loc_offset[0]
                if loc_y == True:
                    bpy.context.scene.cursor_location[1] = sel_max[1] + loc_offset[1]
                if loc_z == True:
                    bpy.context.scene.cursor_location[2] = sel_max[2] + loc_offset[2]
            
         


class AlignTools(bpy.types.Operator):
    """Advanced Align Tools"""
    bl_idname = "tp_origin.align_tools"
    bl_label = "Advanced Align Tools"
    bl_description = "Align Object Tools"
    bl_options = {'REGISTER', 'UNDO'}

   
    #property definition

    #Object-Pivot-Cursor:
    subject = EnumProperty (items=(("0", "Object", "Align Objects"), ("1", "Origin", "Align Objects Origin"), ("2", "Cursor", "Align Cursor To Active")), 
                        name = "Align To", description = "What will be moved")
    # Move active Too:                               
    active_too = BoolProperty (name = "Active too", default= False, description= "Move the active object too")
    
    #advanced options
    advanced = BoolProperty (name = "Advanced Options", default =False, description = "Show advanced options")
    
    consistent = BoolProperty (name = "Consistent Selection", default = False, description = "Use consistent selection")
   
    #Align Location:
    loc_x = BoolProperty (name = "Align to X axis", default= False, description= "Enable X axis alignment")
    loc_y = BoolProperty (name = "Align to Y axis", default= False, description= "Enable Y axis alignment")                               
    loc_z = BoolProperty (name = "Align to Z axis", default= False, description= "Enable Z axis alignment")
   
    #Selection Option:
    ref1 = EnumProperty (items=(("3", "Max", "Align the maximum point"), ("1", "Center", "Align the center point"), ("2", "Origin", "Align the Origin"), 
                                    ("0", "Min", "Align the minimum point")),
                                    name = "Selection reference", description = "Moved objects reference point")   
    #Active Oject Option:
    ref2 = EnumProperty (items=(("3", "Max", "Align to the maximum point"), ("1", "Center", "Align to the center point"), ("2", "Origin", "Align to the Origin"),
                                 ("0", "Min", "Align to the minimum point"), ("4", "Cursor", "Description")),
                                    name = "Active reference", description = "Destination point")
    
    self_or_active = EnumProperty (items = (("0", "Self", "In relation of itself"), ("1", "Active", "In relation of the active object"), ("2", "Selection", "In relation of the entire selection")), 
                                    name = "Relation", default = "1", description = "To what the Origin will be aligned")
    #Location Offset
    loc_offset = FloatVectorProperty(name="Location Offset", description="Offset for location align position", default=(0.0, 0.0, 0.0),
                subtype='XYZ', size=3)
    #Rotation Offset
    rot_offset = FloatVectorProperty(name="Rotation Offset", description="Offset for rotation alignment", default=(0.0, 0.0, 0.0),
                subtype='EULER', size=3) 
    #Scale Offset
    scale_offset = FloatVectorProperty(name="Scale Offset", description="Offset for scale match", default=(0.0, 0.0, 0.0),
                subtype='XYZ', size=3)                                               
               
    #Fit Dimension Prop:
    fit_x = BoolProperty (name = "Fit Dimension to X axis", default= False, description= "")
    fit_y = BoolProperty (name = "Fit Dimension to Y axis", default= False, description= "")
    fit_z = BoolProperty (name = "Fit Dimension to Z axis", default= False, description= "")
    #Apply Fit Dimension:
    apply_dim = BoolProperty (name = "Apply  Dimension", default= False, description= "")
   
    #Align Rot Prop:
    rot_x = BoolProperty (name = "Align Rotation to X axis", default= False, description= "")
    rot_y = BoolProperty (name = "Align Rotation to Y axis", default= False, description= "")
    rot_z = BoolProperty (name = "Align Rotation to Z axis", default= False, description= "")
    
    #Apply Rot:
    apply_rot = BoolProperty (name = "Apply Rotation", default= False, description= "")
   
    #Align Scale:
    scale_x = BoolProperty (name = "Match Scale to X axis", default= False, description= "")
    scale_y = BoolProperty (name = "Match Scale to Y axis", default= False, description= "")
    scale_z = BoolProperty (name = "match Scale to Z axis", default= False, description= "")
    
    #Apply Scale:
    apply_scale = BoolProperty (name = "Apply Scale", default= False, description= "")
   
    def draw(self, context):
        layout = self.layout
       
        #Object-Pivot-Cursor:
        row0 = layout.row()
        row0.prop(self, 'subject', expand =True)
       
        # Move active Too:
        row1 = layout.row()
        row1.prop(self,'active_too')
        row1.prop(self, 'advanced')
        if self.advanced:
            row1b = layout.row()
            row1b.prop(self, 'consistent')
       
        row2 = layout.row()
        row2.label(icon='MAN_TRANS', text="Align Location:")
       
        #Align Location:
        row3 = layout.row()
        row3.prop(self, "loc_x", text="X")       
        row3.prop(self, "loc_y", text="Y") 
        row3.prop(self, "loc_z", text="Z")
        
        #Offset:                
        if self.advanced == True:
            #row8 = col.row()
            #row8.label(text='Location Offset')
            row9 = layout.row()
            row9.prop(self, 'loc_offset', text='')     
                                 
        #Selection Options
        if self.advanced == True:
            sel = bpy.context.selected_objects
            sel_obs = len(sel)
            if sel_obs != 0:
                row4 = layout.row()
                row4.label(text="Selected: "+str(sel_obs)+" Objects", icon ='OBJECT_DATA')
        #if self.subject == "1" or self.subject == "2":
        row5b = layout.row()
        row5b.prop(self, 'self_or_active', expand = True)
        #else:    
        row5 = layout.row()
        row5.prop(self, 'ref1', expand=True)
           
        #Active Object Options: Number of select objects
        act = bpy.context.active_object
        
        if self.advanced == True:
            if act:
                row6 = layout.row()           
                row6.label(text="Active: "+act.name, icon ='OBJECT_DATA')
        row7 = layout.row()
        row7.prop (self, 'ref2', expand=True)
                         
        if self.subject == "0":
            row12 = layout.row()
            row12.label(icon='MAN_ROT', text='Align Rotation:')       
            row13 = layout.row(align=True)
            row13.prop (self, 'rot_x', text='X')
            row13.prop (self, 'rot_y', text='Y')
            row13.prop (self, 'rot_z', text='Z')
            row13.prop (self, 'apply_rot', text='Apply')
            if self.advanced == True:
                row13b = layout.row()
                row13b.prop (self, 'rot_offset', text = '')
           
            row14 = layout.row()
            row14.label(icon='MAN_SCALE', text='Match Scale:')
            row15 = layout.row(align=True)
            row15.prop (self, 'scale_x', text='X')
            row15.prop (self, 'scale_y', text='Y')
            row15.prop (self, 'scale_z', text='Z')
            row15.prop (self, 'apply_scale', text='Apply')
            if self.advanced == True:
                row15b = layout.row()
                row15b.prop (self, 'scale_offset', text = '')
            
            row10 = layout.row()
            row10.label(icon='MAN_SCALE', text='Fit Dimensions:')
            row11 = layout.row(align=True)
            row11.prop (self, 'fit_x', text='X')
            row11.prop (self, 'fit_y', text='Y')
            row11.prop (self, 'fit_z', text='Z')
            row11.prop (self, 'apply_dim', text='Apply')


    def execute(self, context):
        align_function(self.subject, self.active_too, self.consistent, self.self_or_active, self.loc_x, self.loc_y, self.loc_z, 
        self.ref1, self.ref2, self.loc_offset,
         self.rot_x, self.rot_y, self.rot_z, self.rot_offset,
         self.scale_x, self.scale_y, self.scale_z, self.scale_offset, self.fit_x, self.fit_y, self.fit_z) 
                               
        return {'FINISHED'} 
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)  

"""    
#def menu_func(self, context):

    #self.layout.operator("tp_origin.align_tools", text="Align Objects")

def register():
    bpy.utils.register_class(AlignTools)
	#bpy.types.VIEW3D_MT_object_specials.prepend(menu_func)


def unregister():
    bpy.utils.unregister_class(AlignTools)
    #bpy.types.VIEW3D_MT_object_specials.remove(menu_func)

"""
    
    
    



