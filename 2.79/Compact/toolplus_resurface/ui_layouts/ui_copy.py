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
from .. icons.icons import load_icons


def draw_copy_ui(self, context, layout):
        tot_props = context.window_manager.totarget_props          
        dpl_props = context.window_manager.dupliset_props          
        toc_props = context.window_manager.tocursor_props              
        tp_props = context.window_manager.tp_props_resurface        
        mft_props = context.window_manager.mifth_clone_props        
       
        icons = load_icons()

        layout.operator_context = 'INVOKE_REGION_WIN'
       
        icons = load_icons()     

        col = layout.column(align=True)

        if not tp_props.display_copy: 
          
            box = col.box().column(1)
            
            row = box.row(1)   
            row.prop(tp_props, "display_copy", text="", icon="TRIA_RIGHT", emboss = False)                
            row.label("CopyShop")     

            row.operator("tp_ops.copy_to_meshtarget_pl", text="", icon='PASTEFLIPDOWN')  
            
            button_switch = icons.get("icon_switch")
            row.operator("tp_ops.mft_radialclone_popup", text="", icon_value=button_switch.icon_id)

            button_copy_tocursor = icons.get("icon_copy_tocursor")
            row.menu("VIEW3D_MT_copypopup", text="", icon='MOD_ARRAY')
  

        else:
           
            box = col.box().column(1)
            
            row = box.row(1)  
            row.prop(tp_props, "display_copy", text="", icon="TRIA_DOWN", emboss = False)            
            row.label("CopyShop")  

            if context.mode == 'OBJECT':

                box.separator()  
                 
                row = box.row(1)
                row.operator("object.duplicate_move", text="Dupli Move")
                row.operator("object.duplicate_move_linked", text="Dupli Link")            
                          
                box.separator()  
                box.separator()  

                row = box.row(1)            
                row.operator("tp_ops.mft_radialclone", text="Radial Clone")
                row.prop(mft_props, "mft_clonez", text='')       
               
                row = box.row(1)
                row.prop(mft_props, "mft_radialClonesAxisType", text='')                
                row.prop(mft_props, "mft_radialClonesAxis", text='')

                box.separator()
                box.separator()
             
                
                row = box.row(1)
                if tp_props.display_copy_to_cursor:
                    row.prop(tp_props, "display_copy_to_cursor", text="", icon='TRIA_DOWN')                                                  
                    row.operator("tp_ops.copy_to_cursor_panel", text="2 Cursor")     
                    row.prop(toc_props, "total", text="")  
                else:
                    row.prop(tp_props, "display_copy_to_cursor", text="", icon='TRIA_RIGHT')                                                    
                    row.operator("tp_ops.copy_to_cursor_panel", text="2 Cursor")     
                    row.prop(toc_props, "total", text="")  
     
                if tp_props.display_copy_to_cursor:
                    scene = bpy.context.scene

                    box = col.box().column(1) 
                     
                    row = box.row(1)                              
                    row.prop(toc_props, "join", text = "Join")                 
                    row.prop(toc_props, "unlink", text = "Unlink")                 
                    
                    box.separator()
                
                    box = col.box().column(1) 
                     
                    row = box.row(1)                   
                    row.operator("object.simplearewo", text="ARewO Replicator")                                        
                   
                box.separator() 
                box.separator() 

                 
                row = box.row(1)            
                if tp_props.display_copy_to_faces:
                    row.prop(tp_props, "display_copy_to_faces", text="", icon='TRIA_DOWN')
                    row.operator("tp_ops.copy_to_meshtarget_pl", text="      Copy to Mesh Target") 
                else:
                    row.prop(tp_props, "display_copy_to_faces", text="", icon='TRIA_RIGHT')
                    row.operator("tp_ops.copy_to_meshtarget_pl", text="      Copy to Mesh Target") 
     
                if tp_props.display_copy_to_faces:
                    scene = bpy.context.scene
                                                       
                    box = col.box().column(1)

                    row = box.row(1)            
                    row.label("Source:")             
                    row.prop(tot_props, "copyfromobject", text="")  

                    box.separator()                     
                   
                    row = box.row(1)            
                    row.label("Target:") 
     
                    sub = row.row(1)
                    sub.scale_x = 1.55               
                    sub.prop(tot_props, 'copytype', expand=True)
                    
                    box.separator() 
                    
                    row = box.row(1)                
                    row.label("1st Axis:")
                   
                    sub1 = row.row(1)
                    sub1.scale_x = 1                    
                    sub1.prop(tot_props, 'priaxes', expand=True)
                    
                    box.separator() 
                               
                    row = box.row(1)                
                    row.label("2nd Axis:") 
      
                    sub2 = row.row(1)
                    sub2.scale_x = 1     
                    sub2.prop(tot_props, 'secaxes', expand=True)
              
                    box.separator()     
              
                    row = box.row(1)                 
                    if tot_props.copytype == 'E':
                        row.prop(tot_props, 'edgescale')
                        
                        if tot_props.edgescale:
                           row = box.row(1) 
                           row.prop(tot_props, 'scale')           


                    if len(bpy.context.selected_objects) == 2:

                        box = col.box().column(1)
                       
                        row = box.column(1)                                
                        row.label("! Source & Target Mesh !")                      
                     
                        box.separator() 
                                     
                        row = box.row(1)            
                        row.label("Origin to:")       
                        
                        row = box.row(1) 
                        row.prop(tot_props, "set_plus_z")       
                        row.prop(tot_props, "set_minus_z")  
                        
                        box.separator() 
                        
                        row = box.row(1)            
                        row.label("Relations:")

                        row = box.row(1)                                           
                        row.prop(tot_props, "dupli_unlinked", text = "Unlinked")
                        row.prop(tot_props, "join", text = "Join")

                        box.separator() 
                        
                        row = box.row(1)            
                        row.label("Editmode:")     
                        
                        row = box.row(1) 
                        row.prop(tot_props, "set_edit_target", text = "Target")                           
                        row.prop(tot_props, "set_edit_source", text = "Source")
                    
                    else:
                        pass                       
                
                box.separator()            
                box.separator()            
           

                obj = context.active_object     
                if obj:
                    obj_type = obj.type
                                                                          
                    if obj_type in {'MESH'}:

                        row = box.row(1)
                        
                        if tp_props.display_dupli:
                            row.prop(tp_props, "display_dupli", text="", icon='TRIA_DOWN')
                            row.operator("tp_ops.dupli_set_panel", "      Duplication to Active") 
                        else:
                            row.prop(tp_props, "display_dupli", text="", icon='TRIA_RIGHT')
                            row.operator("tp_ops.dupli_set_panel", "      Duplication to Active") 

                        if tp_props.display_dupli:

                            box = col.box().column(1)
                              
                            row = box.row(1)
                            row.prop(context.object, "dupli_type", expand=True)            

                            box.separator()
                                       
                            if context.object.dupli_type == 'FRAMES':
                                row = box.row(1)   
                                row.prop(context.object, "dupli_frames_start", text="Start")
                                row.prop(context.object, "dupli_frames_end", text="End")

                                row = box.row(1)                           
                                row.prop(context.object, "dupli_frames_on", text="On")
                                row.prop(context.object, "dupli_frames_off", text="Off")

                                row = box.row(1)   
                                row.prop(context.object, "use_dupli_frames_speed", text="Speed")

                            elif context.object.dupli_type == 'VERTS':
                                row = box.row(1)   
                                row.prop(context.object, "use_dupli_vertices_rotation", text="Rotation")

                            elif context.object.dupli_type == 'FACES':
                                row = box.row(1)                       
                                row.prop(context.object, "use_dupli_faces_scale", text="Scale")
                               
                                sub = row.row()
                                sub.active = context.object.use_dupli_faces_scale
                                sub.prop(context.object, "dupli_faces_scale", text="Inherit Scale")

                            elif context.object.dupli_type == 'GROUP':
                                row = box.row(1)
                                row.prop(context.object, "dupli_group", text="Group")

                            row = box.row(1)
                            row.prop(dpl_props, "dupli_align", text="Align")
                            row.prop(dpl_props, "dupli_single", text="Single")
                            
                            if dpl_props.dupli_single == True:
                                
                                row = box.row(1)            
                                row.prop(dpl_props, "dupli_separate", text="Separate")
                                row.prop(dpl_props, "dupli_link", text="As Instance")


                        box.separator()  
                        box.separator()  


                 
                row = box.row(1)
                
                if tp_props.display_toall:
                    row.prop(tp_props, "display_toall", text="", icon='TRIA_DOWN')
                    row.menu("VIEW3D_MT_copypopup", text="Copy Activ Attributes", icon='BLANK1') 
                else:
                    row.prop(tp_props, "display_toall", text="", icon='TRIA_RIGHT')
                    row.menu("VIEW3D_MT_copypopup", text="Copy Activ Attributes", icon='BLANK1') 
                    
                if tp_props.display_toall:
                    scene = context.scene
                  
                    box = col.box().column(1)

                    row = box.row(1) 
                    row.alignment = 'CENTER'                
                    row.label("Material", icon='MATERIAL') 

                    row = box.row(1) 
                    row.label("copy to:") 
                                      
                    row = box.row(1)   
                    row.operator("scene.to_all", text="Selected").mode = "material, selected"
                    row.operator("scene.to_all", text="Children").mode = "material, children"

                    box.separator()
                                    
                    row = box.row(1) 
                    row.label("append to:") 
                                      
                    row = box.row(1)   
                    row.operator("scene.to_all", text="Selected").mode = "material, selected, append"
                    row.operator("scene.to_all", text="Children").mode = "material, children, append"

                    box.separator()
                 
                    box = col.box().column(1)
                        
                    row = box.row(1) 
                    row.alignment = 'CENTER'                
                    row.label("Modifier", icon='MODIFIER') 
     
                    row = box.row(1) 
                    row.label("copy to:") 
                                      
                    row = box.row(1)   
                    row.operator("scene.to_all", text="Selected").mode = "modifier, selected"
                    row.operator("scene.to_all", text="Children").mode = "modifier, children"

                    box.separator()                

                    row = box.row(1) 
                    row.label("append to:") 
                                      
                    row = box.row(1)   
                    row.operator("scene.to_all", text="Selected").mode = "modifier, selected, append"
                    row.operator("scene.to_all", text="Children").mode = "modifier, children, append"
                    
                    box.separator()  

                    row = box.row(1)
                    row.prop(context.scene, "excludeMod")              
                    

                
                box.separator()      
                box.separator()      

                row = box.row(1)  
                if not tp_props.display_optimize_tools:
                    row.prop(tp_props, "display_optimize_tools", text="", icon='TRIA_RIGHT')

                    row.operator("object.select_linked", text="L-Select")  
                    row.operator_menu_enum("object.make_links_data", "type", text="Links ")
                    row.menu("VIEW3D_MT_make_single_user", text="Unlinks")

                else:
                    row.prop(tp_props, "display_optimize_tools", text="", icon='TRIA_DOWN')  
                    row.operator("object.select_linked", text="L-Select")  
                    row.operator_menu_enum("object.make_links_data", "type", text="Links ")
                    row.menu("VIEW3D_MT_make_single_user", text="Unlinks")

             
                    box = col.box().column(1) 
                   
                    row = box.row(1)                 
                    row.operator("object.multi_duplicate", text="Multi Linked", icon="LINKED")   
                    row.operator("object.join", text="Join", icon="AUTOMERGE_ON")             

                    box.separator() 
                   
                    row = box.row(1)  
                    row.label("Origin to:")
                    
                    sub = row.row(1)
                    sub.scale_x = 0.3333            
                    sub.operator("tp_ops.origin_plus_z", text="T", icon="LAYER_USED")  
                    props = sub.operator("object.origin_set", text="M", icon="LAYER_USED")
                    props.type = 'ORIGIN_GEOMETRY'
                    props.center = 'BOUNDS'
                    sub.operator("tp_ops.origin_minus_z", text="B", icon="LAYER_USED")


                box.separator()
                box.separator()

                 
                row = box.row(1)  
                
                if tp_props.display_array_tools:
                    row.prop(tp_props, "display_array_tools", text="", icon='TRIA_DOWN')
                    row.label("Modifier & Constraint")
                
                else:                                  
                    row.prop(tp_props, "display_array_tools", text="", icon='TRIA_RIGHT')  
                    row.operator("tp_ops.x_array", text="X Array")    
                    row.operator("tp_ops.y_array", text="Y Array")    
                    row.operator("tp_ops.z_array", text="Z Array")          

                if tp_props.display_array_tools:
                   
                    box = col.box().column(1) 

                    row = box.row(1) 
                    if tp_props.display_axis_array:
                        row.prop(tp_props, "display_axis_array", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_axis_array", text="", icon='TRIA_RIGHT')   
                    
                    row.operator("tp_ops.x_array", text="X Array")    
                    row.operator("tp_ops.y_array", text="Y Array")    
                    row.operator("tp_ops.z_array", text="Z Array")  

                    if tp_props.display_axis_array:
                                            
                        mod_types = []
                        append = mod_types.append

                        obj = context.active_object     
                        if obj:
                            if obj.modifiers:
                                  
                                box = col.box().column(1)                 
                                
                                row = box.row(1)
                                row.operator("object.transform_apply", text="Applied Scale?", icon="OUTLINER_DATA_EMPTY").scale=True
                                
                                row = box.row(1)
                                row.operator("tp_ops.expand_mod"," " ,icon = 'TRIA_DOWN')  
                                row.operator("tp_ops.collapse_mod", " " ,icon = 'TRIA_UP') 
                                row.operator("tp_ops.mods_view", " " ,icon = 'RESTRICT_VIEW_OFF') 
                                row.operator("tp_ops.remove_mod", text=" " , icon='X') 
                                row.operator("tp_ops.apply_mod", text=" " , icon='FILE_TICK') 
                   
                                box.separator()
                                
                                for mod in context.active_object.modifiers:

                                    row = box.row(1)

                                    if mod.show_expanded == True:
                                        if mod.type == 'ARRAY':
                                            append(mod.type)                                       
                                            
                                            box = col.box().column(1)
                                            
                                            row = box.row(1)                                        
                                            row.label(mod.name)
                                            
                                            if mod.fit_type == 'FIXED_COUNT':
                                                row.prop(mod, "count", text = "")                    

                                            box.separator()
                                            
                                            row = box.row(1)
                                            row.prop(mod, "relative_offset_displace", text="")

                                            box.separator()
                                            
                                            row = box.row(1)
                                            row.prop(mod, "use_merge_vertices", text="Merge")
                                            row.prop(mod, "use_merge_vertices_cap", text="First Last")
                                            
                                            row = box.row(1)
                                            row.prop(mod, "merge_threshold", text="Distance")

                                    else:
                                        box.separator()  
                            
                            else:
                                box = col.box().column(1) 
                                
                                row = box.row(1)
                                row.operator("tp_help.axis_array", text = "! no array active !", icon ="INFO")  
                                    
                        else:
                            box = col.box().column(1) 
                            
                            row = box.row(1)
                            row.operator("tp_help.axis_array", text = "! no array active !", icon ="INFO") 
                            ###                           

                                      
                    box.separator()
                                      
                    box = col.box().column(1) 

                    row = box.row(1) 
                    if tp_props.display_empty:
                        row.prop(tp_props, "display_empty", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_empty", text="", icon='TRIA_RIGHT')                  
                    
                    row.operator("tp_ops.add_empty_array_mods", text="Empty Plane", icon="MOD_ARRAY")
                    row.operator("tp_ops.add_empty_array", text="", icon="OUTLINER_DATA_EMPTY")

                    row = box.row(1) 
                    if tp_props.display_empty:
                        row.prop(tp_props, "display_empty", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_empty", text="", icon='TRIA_RIGHT')                  
                    
                    row.operator("tp_ops.add_empty_curve_mods", text="Empty Array", icon="MOD_ARRAY")
                    row.operator("tp_ops.add_empty_curve", text="", icon="OUTLINER_DATA_CURVE")
                    

                    if tp_props.display_empty:  

                        mod_types = []
                        append = mod_types.append
                                              
                        obj = context.active_object       
                        if obj:

                            if obj.modifiers:
                        
                                box = col.box().column(1)                 
                                
                                row = box.row(1)
                                row.operator("object.transform_apply", text="Applied Scale?", icon="OUTLINER_DATA_EMPTY").scale=True
                                
                                row = box.row(1)
                                row.operator("tp_ops.expand_mod"," " ,icon = 'TRIA_DOWN')  
                                row.operator("tp_ops.collapse_mod", " " ,icon = 'TRIA_UP')   
                                row.operator("tp_ops.mods_view", " " ,icon = 'RESTRICT_VIEW_OFF') 
                                row.operator("tp_ops.remove_mod", text=" " , icon='X') 
                                row.operator("tp_ops.apply_mod", text=" " , icon='FILE_TICK') 

                                box.separator()

                                for mod in context.active_object.modifiers:
                                      
                                    if mod.show_expanded == True:
                                        if mod.type == 'ARRAY':
                                            append(mod.type)
                                            
                                            box = col.box().column(1) 
                                            
                                            if mod.fit_type == 'FIXED_COUNT':
                                                
                                                row = box.row(1)                                        
                                                row.label("Mesh Array")
                                                
                                                if mod.fit_type == 'FIXED_COUNT':
                                                    row.prop(mod, "count", text = "")                    

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "relative_offset_displace", text="")

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "use_merge_vertices", text="Merge")
                                                row.prop(mod, "use_merge_vertices_cap", text="First Last")
                                                
                                                row = box.row(1)
                                                row.prop(mod, "merge_threshold", text="Distance")

                                                box.separator()   
                                                
                                                row = box.column(1)
                                                row.prop(mod, "offset_object", text="")   
                                                
                                                box.separator()

                                            elif mod.fit_type == 'FIT_CURVE':
                                               
                                                box.separator()
                                            
                                                row = box.row(1)
                                                row.label(text="Mesh Offset")                                                                                      
                                               
                                                row = box.row(1)
                                                row.prop(mod, "relative_offset_displace", text = "")

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "use_merge_vertices", text="Merge")
                                                row.prop(mod, "use_merge_vertices_cap", text="First Last")
                                                
                                                row = box.row(1)
                                                row.prop(mod, "merge_threshold", text="Distance")
                                                
                                                box.separator()   
                                                
                                                row = box.row(1)                                          
                                                row.prop(mod, "curve", text = "")    

                                                box.separator()                      
                                       
                                        elif mod.type == 'CURVE':
                                            append(mod.type)                         
                                            
                                            box = col.box().column(1) 
                                            
                                            row = box.column(1)
                                            row.label(text="Curve Deformation Axis")
                                            
                                            row = box.column(1)                                        
                                            row.row().prop(mod, "deform_axis", expand=True)
                                            
                                            box.separator()
                                            
                                            row = box.column(1) 
                                            row.prop(mod, "object", text="")
                                                                                    
                                            box.separator()
                                
                                    else:
                                        box.separator()  
                            
                            else:
                                box = col.box().column(1) 
                                
                                row = box.row(1)
                                row.operator("tp_help.empty_array", text = "! nothing selected !", icon ="INFO")   
                            
                                box = col.box().column(1) 
                                    
                        else:
                            box = col.box().column(1) 
                            
                            row = box.row(1)
                            row.operator("tp_help.empty_array", text = "! nothing selected !", icon ="INFO")             
                            
                            box = col.box().column(1) 
                          
                          
                    box.separator() 

                    row = box.row(1) 
                    if tp_props.display_array:
                        row.prop(tp_props, "display_array", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_array", text="", icon='TRIA_RIGHT')                  

                    row.operator("tp_ops.add_curve_array_mods", text="Curve Array", icon="MOD_ARRAY")     
                    row.operator("tp_ops.add_curve_array", text="", icon="CURVE_BEZCURVE")    
                          
                    row = box.row(1) 
                    if tp_props.display_array:
                        row.prop(tp_props, "display_array", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_array", text="", icon='TRIA_RIGHT')                           

                    row.operator("tp_ops.add_circle_array_mods", text="Circle Array", icon="MOD_ARRAY")
                    row.operator("tp_ops.add_circle_array", text="", icon="CURVE_BEZCIRCLE")
                    
                    if tp_props.display_array:

                        mod_types = []
                        append = mod_types.append
                        
                        obj = context.active_object       
                        if obj:

                            if obj.modifiers:
                         
                                box = col.box().column(1)                 
                                
                                row = box.row(1)
                                row.operator("object.transform_apply", text="Applied Scale?", icon="OUTLINER_DATA_EMPTY").scale=True
                                
                                row = box.row(1)
                                row.operator("tp_ops.expand_mod"," " ,icon = 'TRIA_DOWN')  
                                row.operator("tp_ops.collapse_mod", " " ,icon = 'TRIA_UP')  
                                row.operator("tp_ops.mods_view", " " ,icon = 'RESTRICT_VIEW_OFF') 
                                row.operator("tp_ops.remove_mod", text=" " , icon='X') 
                                row.operator("tp_ops.apply_mod", text=" " , icon='FILE_TICK') 

                                box.separator() 
                        
                                for mod in context.active_object.modifiers:
                                      
                                    if mod.show_expanded == True:
                                        if mod.type == 'ARRAY':
                                            append(mod.type)
                                            
                                            box = col.box().column(1) 
                                            
                                            if mod.fit_type == 'FIXED_COUNT':
                                                
                                                row = box.row(1)                                        
                                                row.label("Mesh Array")
                                                
                                                if mod.fit_type == 'FIXED_COUNT':
                                                    row.prop(mod, "count", text = "")                    

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "relative_offset_displace", text="")

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "use_merge_vertices", text="Merge")
                                                row.prop(mod, "use_merge_vertices_cap", text="First Last")
                                                
                                                row = box.row(1)
                                                row.prop(mod, "merge_threshold", text="Distance")

                                                box.separator()   
                                                
                                                row = box.column(1)
                                                row.prop(mod, "offset_object", text="")   
                                                
                                                box.separator()

                                            elif mod.fit_type == 'FIT_CURVE':
                                               
                                                box.separator()
                                            
                                                row = box.row(1)
                                                row.label(text="Mesh Offset")                                                                                      
                                               
                                                row = box.row(1)
                                                row.prop(mod, "relative_offset_displace", text = "")

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "use_merge_vertices", text="Merge")
                                                row.prop(mod, "use_merge_vertices_cap", text="First Last")
                                                
                                                row = box.row(1)
                                                row.prop(mod, "merge_threshold", text="Distance")
                                                
                                                box.separator()   
                                                
                                                row = box.row(1)                                          
                                                row.prop(mod, "curve", text = "")    

                                                box.separator()                      
                                       
                                        elif mod.type == 'CURVE':
                                            append(mod.type)                         
                                            
                                            box = col.box().column(1) 
                                            
                                            row = box.column(1)
                                            row.label(text="Curve Deformation Axis")
                                            
                                            row = box.column(1)                                        
                                            row.row().prop(mod, "deform_axis", expand=True)
                                            
                                            box.separator()
                                            
                                            row = box.column(1) 
                                            row.prop(mod, "object", text="")
                                                                                    
                                            box.separator()
                                
                                    else:
                                        box.separator()  
                            
                            else:
                                box = col.box().column(1) 
                                
                                row = box.row(1)
                                row.operator("tp_help.curve_array", text = "! nothing selected !", icon ="INFO")   
                            
                                box = col.box().column(1) 
                                    
                        else:
                            box = col.box().column(1) 
                            
                            row = box.row(1)
                            row.operator("tp_help.curve_array", text = "! nothing selected !", icon ="INFO")             
                            
                            box = col.box().column(1) 
                          
                      
                    box.separator()                        
                     
                    row = box.row(1) 
                    if tp_props.display_pfath:
                        row.prop(tp_props, "display_pfath", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_pfath", text="", icon='TRIA_RIGHT')            
                
                    row.operator("tp_ops.add_fpath_con", text="Add Follow Path", icon="CONSTRAINT_DATA")          
                    row.operator("tp_ops.add_fpath_curve", text="", icon="CURVE_BEZCIRCLE")
                   
                    box.separator() 
                    
                    if tp_props.display_pfath:
                        
                        con_types = []
                        append = con_types.append
                        
                        obj = context.active_object     
                        if obj:                                            
                            if obj.constraints:
                                                                                            
                                for con in context.active_object.constraints:

                                    box = col.box().column(1)
                            
                                    row = box.row(1)
                                    row.operator("object.fpath_array_panel", text="Set FPath Array", icon ="MOD_ARRAY")  
                                    
                                    box.separator()
                                    
                                    row = box.row(1)
                                    row.prop(context.scene, "type", )    
                                    
                                    row = box.row(1)                            
                                    row.prop(context.scene, "count")

                                                                     
                                    box.separator() 

                                    row = box.row(1)
                                    layout.operator_context = 'INVOKE_REGION_WIN'                    
                                    row.prop(context.scene, "frame_current", text="Frame")
                                    row.operator("object.select_grouped", text="Select Group").type='GROUP'
                                        
                                    row = box.row(1)      
                                    row.operator("tp_ops.linked_fpath",text="Set Linked")                  
                                    row.operator("tp_ops.single_fpath",text="Set Unlinked")  

                                    box.separator() 
                                    
                                    box = col.box().column(1)                 
                                    
                                    row = box.row(1)                                      
                                    row.operator("object.transform_apply", text="Applied Scale?", icon="OUTLINER_DATA_EMPTY").scale=True
                                   
                                    row = box.row(1)
                                    row.operator("tp_ops.expand_con","" ,icon = 'TRIA_DOWN')  
                                    row.operator("tp_ops.collapse_con", "" ,icon = 'TRIA_UP') 
                                    row.operator("tp_ops.constraint_off","off" ,icon = 'VISIBLE_IPO_OFF')  
                                    row.operator("tp_ops.constraint_on", "on" ,icon = 'RESTRICT_VIEW_OFF') 
                                    row.operator("object.constraints_clear", text="clear" , icon='X') 

                                    box.separator()                                     

                                    if con.show_expanded == True:  
                                                                                
                                        box = col.box().column(1) 
                                
                                        row = box.row(1)  
                                        
                                        if con.type == 'FOLLOW_PATH':
                                           
                                            append(con.type)

                                            box.label(con.name)
                                            
                                            box.prop(con, "target")

                                            box.separator() 
                                            
                                            row = box.column(1)                                                      
                                            row.operator("constraint.followpath_path_animate", text="Animate Path", icon='ANIM_DATA')
                                            row.label("!need activation in properties!")  
                                            
                                            box.separator()
                                            
                                            if context.scene.type == "OFFSET":
                                                row.prop(context.scene,"offset")
                                       
                                            elif context.scene.type == "FIXED_POSITION":
                                                row.prop(context.scene,"factor", "Offset")
                                                                                         
                                            box.separator() 
                                            
                                            row.prop(con, "use_curve_follow")
                                            
                                            row = box.row(1)
                                            row.label("Axis")
                                            row.prop(con, "forward_axis", expand=True)

                                            box.separator() 
                                            
                                            row = box.row(1)                            
                                            row.prop(con, "up_axis", text="Up")
                                            row.label()

                                            ###
                                            box.separator()   
                                    
                            else:
                                box = col.box().column(1) 
                                
                                row = box.row(1)
                                row.operator("tp_help.follow_path", text ="! no constraint active !", icon ="INFO")  
                                    
                        else:
                            box = col.box().column(1) 
                            
                            row = box.row(1)
                            row.operator("tp_help.follow_path", text = "! nothing selected !", icon ="INFO")             


                box.separator() 
             



            if context.mode == 'EDIT_MESH':

                box = col.box().column(1)
                 
                row = box.column(1)
                row.operator("mesh.duplicate_move", text="Dupli Move", icon='BLANK1')
                
                box = col.box().column(1) 
                 
                row = box.row(1)  
                row.operator("tp_ops.copy_to_cursor_panel", text="Copy 2 Cursor")     
                row.prop(toc_props, "total", text="")
                     
                box.separator()   




