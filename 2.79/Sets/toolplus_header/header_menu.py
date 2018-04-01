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

from . menus.menu_options import (VIEW3D_TP_Header_Options_Menu)
from . menus.menu_display import (VIEW3D_TP_Header_Display_Menu)
from . menus.menu_ruler   import (VIEW3D_TP_Header_Ruler_Menu)
from . menus.menu_shading import (VIEW3D_TP_Header_Shading_Menu)
from . menus.menu_station import (VIEW3D_TP_Header_Station_Menu)

from . menus.menu_snapset import (VIEW3D_TP_Header_SnapSet_Menu)
from . menus.menu_snapto  import (VIEW3D_TP_Header_CursorTo_Menu)
from . menus.menu_snapto  import (VIEW3D_TP_Header_SelectTo_Menu)

from . origin.origin_menu  import (VIEW3D_TP_Origin_Menu)
from . origin.origin_menu  import (VIEW3D_TP_Origin_Advanced_Menu)

EDIT = ["EDIT_MESH", "EDIT_CURVE", "EDIT_SURFACE", "EDIT_LATTICE", "EDIT_METABALL", "EDIT_ARMATURE"]

# UI: MAIN MENU # 
class VIEW3D_TP_Header_Menus(bpy.types.Header):
    bl_space_type = 'VIEW_3D'

    @classmethod
    def poll(self, context):
       return 
       
    def draw(self, context):
        layout = self.layout       
    
        #tp_props = context.window_manager.tp_props_header

        icons = load_icons()
        
        layout.operator_context = 'INVOKE_REGION_WIN'    

        view = context.space_data        
        obj = context.active_object        
        obj_type = obj.type

        is_geometry = (obj_type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'})        
        is_mesh = (obj_type in {'MESH'})   

        row = layout.row(1)


        # USE BUTTONS #
        display_buttons = context.user_preferences.addons[__package__].preferences.tab_display_buttons
        if display_buttons == 'on': 


            # OPTIONS #  
            row.menu("VIEW3D_TP_Header_Options_Menu", text="", icon= "SCRIPTWIN")     

            row.separator()


            # RULER #  
            display_ruler = context.user_preferences.addons[__package__].preferences.tab_display_ruler
            if display_ruler == 'on':

                button_ruler_triangle = icons.get("icon_ruler_triangle") 
                row.operator("view3d.ruler", text='', icon_value = button_ruler_triangle.icon_id)     

                row.separator()


            # SNAP SET #   
            display_snap_set = context.user_preferences.addons[__package__].preferences.tab_display_snapset
            if display_snap_set == 'on': 

                row.separator()

                #button_snap_active = icons.get("icon_snap_active")
                #row.operator("tp_ops.active_snap", text="", icon_value=button_snap_active.icon_id) 

                button_snap_active = icons.get("icon_snap_active")
                row.operator("tp_ops.closest_snap", text="", icon_value=button_snap_active.icon_id)

                button_snap_cursor = icons.get("icon_snap_cursor")           
                row.operator("tp_ops.active_3d", text="", icon_value=button_snap_cursor.icon_id) 
         
                button_snap_grid = icons.get("icon_snap_grid")
                row.operator("tp_ops.grid", text="", icon_value=button_snap_grid.icon_id)
                            
                if context.mode == 'OBJECT':
                    button_snap_place = icons.get("icon_snap_place")
                    row.operator("tp_ops.place", text="", icon_value=button_snap_place.icon_id)

                else:
                    button_snap_retopo = icons.get("icon_snap_retopo")
                    row.operator("tp_ops.retopo", text="", icon_value=button_snap_retopo.icon_id)    
            
           
            # SNAP TO #   
            display_snap = context.user_preferences.addons[__package__].preferences.tab_display_snap
            if display_snap == 'on':  

                row.separator()

                button_cursor_center = icons.get("icon_cursor_center")            
                row.operator("view3d.snap_cursor_to_center", text="", icon_value = button_cursor_center.icon_id)

                button_cursor_active_obm = icons.get("icon_cursor_active_obm")           
                row.operator("view3d.snap_cursor_to_selected", text="", icon_value = button_cursor_active_obm.icon_id)

                if context.mode == 'OBJECT':
                   
                    button_snap_set = icons.get("icon_snap_set")            
                    row.operator("tp_ops.header_set_cursor", text="", icon_value = button_snap_set.icon_id)  
  
                button_select_cursor = icons.get("icon_select_cursor")    
                row.operator("view3d.snap_selected_to_cursor", text="", icon_value = button_select_cursor.icon_id).use_offset=False


            # ORIGIN TO #   
            display_origin = context.user_preferences.addons[__package__].preferences.tab_display_origin
            if display_origin == 'on':  
                
                row.separator()

                row.menu("VIEW3D_TP_Origin_Menu", text= "", icon= "VERTEXSEL")


            # ALIGN TO #   
            display_advanced = context.user_preferences.addons[__package__].preferences.tab_display_advanced
            if display_advanced == 'on':  
               
                row.separator()                
                
                ob = context
                if ob.mode in EDIT:   

                    button_origin_mesh = icons.get("icon_origin_mesh")                
                    row.operator("tp_ops.origin_transform", "", icon_value=button_origin_mesh.icon_id)               
                else:
                    button_origin_distribute = icons.get("icon_origin_distribute")  
                    row.operator("object.distribute_osc", "", icon_value=button_origin_distribute.icon_id)

                    button_origin_align = icons.get("icon_origin_align")                
                    row.operator("tp_origin.align_tools", "", icon_value=button_origin_align.icon_id)  

                button_align_zero = icons.get("icon_align_zero")                
                row.operator("tp_ops.zero_axis", "", icon_value=button_align_zero.icon_id)      


            row.separator()
            
            # NP POINT DISTANCE #       
            display_point_distance = context.user_preferences.addons[__package__].preferences.tab_display_point_distance
            if display_point_distance == 'on':  

                button_snap_ruler = icons.get("icon_snap_ruler") 
                row.operator("tp_ops.np_020_point_distance", text='', icon_value = button_snap_ruler.icon_id)

            if context.mode == 'OBJECT':

                display_point_move = context.user_preferences.addons[__package__].preferences.tab_display_point_move
                if display_point_move == 'on':  

                    button_snap_grab = icons.get("icon_snap_grab") 
                    row.operator("tp_ops.np_020_point_move", text='', icon_value=button_snap_grab.icon_id)                   
            
            
            if is_mesh and context.mode == 'OBJECT':


                display_roto_move = context.user_preferences.addons[__package__].preferences.tab_display_roto_move
                if display_roto_move == 'on':  

                    button_snap_rotate = icons.get("icon_snap_rotate") 
                    row.operator("tp_ops.np_020_roto_move", text='', icon_value=button_snap_rotate.icon_id)

                display_point_scale = context.user_preferences.addons[__package__].preferences.tab_display_point_scale
                if display_point_scale == 'on':   
 
                    button_snap_scale = icons.get("icon_snap_scale") 
                    row.operator("tp_ops.np_020_point_scale", text='', icon_value=button_snap_scale.icon_id)


                display_point_align = context.user_preferences.addons[__package__].preferences.tab_display_point_align
                if display_point_align == 'on':  

                    button_snap_abc = icons.get("icon_snap_abc") 
                    row.operator("tp_ops.np_020_point_align", text='', icon_value=button_snap_abc.icon_id) 


            # SNAPLINE #   
            display_snapline = context.user_preferences.addons[__package__].preferences.tab_display_snapline
            if display_snapline == 'on':  

                if is_mesh:

                    button_snap_line = icons.get("icon_snap_line") 
                    row.operator("tp_ops.snapline", text='', icon_value=button_snap_line.icon_id)    


            # DISPLAY #  
            display_objects = context.user_preferences.addons[__package__].preferences.tab_display_objects
            if display_objects == 'on':  
                
                row.separator()
                

                if obj:

                    row.operator("tp_ops.header_display_set", text="",  icon="META_CUBE")

                    button_draw_wire = icons.get("icon_draw_wire") 
                    row.operator("tp_ops.header_set_wire", text="", icon_value = button_draw_wire.icon_id)


            # SHADING #  
            display_shading = context.user_preferences.addons[__package__].preferences.tab_display_shading
            if display_shading == 'on':  

               row.separator()
                
               if context.mode == 'OBJECT':
                   row.operator("object.shade_smooth", text="", icon="SMOOTH")
                   row.operator("object.shade_flat", text="", icon="MESH_CIRCLE")
               else:
                   row.operator("mesh.faces_shade_smooth", text="", icon="SMOOTH")
                   row.operator("mesh.faces_shade_flat", text="", icon="MESH_CIRCLE") 

               if is_mesh:
                   row.prop(context.active_object.data, "use_auto_smooth", text="", icon="AUTO") 
                   row.prop(context.active_object.data, "show_double_sided", text="", icon="GHOST")




            # VIEW #
            display_view = context.user_preferences.addons[__package__].preferences.tab_display_view
            if display_view == 'on':                  
                    
                row = layout.row(1)
                row.operator_context = 'INVOKE_REGION_WIN'                
                
                row.prop(view, "use_matcap", text="", icon ="MATCAP_01")
                row.prop(context.space_data.fx_settings, "use_ssao", text="", icon="GROUP")
                row.prop(view, "show_only_render", text="", icon ="SCENE")
                row.prop(view, "show_world", text="", icon ="WORLD")
                row.prop(view, "show_floor", text="", icon ="GRID")


            # WINDOWS #
            display_window = context.user_preferences.addons[__package__].preferences.tab_display_window
            if display_window == 'on':  

                row = layout.row(1)
                row.operator_context = 'INVOKE_REGION_WIN'                
                  
                row.operator("screen.screen_full_area", text = "", icon = "FULLSCREEN_ENTER")                
                row.operator("screen.region_quadview", text="", icon="SPLITSCREEN")

                if view.region_quadviews:
                    
                    region = view.region_quadviews[2]
                   
                    row = layout.row(align=True)
                    row.prop(region, "lock_rotation")
                   
                    row = layout.row(align=True)
                    row.enabled = region.lock_rotation               
                    row.prop(region, "show_sync_view")
                   
                    row = layout.row(align=True)
                    row.enabled = region.lock_rotation and region.show_sync_view
                    row.prop(region, "use_box_clip")         


            # HISTORY #               
            display_header_history = context.user_preferences.addons[__package__].preferences.tab_display_history
            if display_header_history == 'on': 

                row = layout.row(1)
                row.operator("ed.undo", text="", icon="FRAME_PREV")
                row.operator("ed.undo_history", text="", icon="COLLAPSEMENU")
                row.operator("ed.redo", text="", icon="FRAME_NEXT")


            # SAVE #           
            display_header_save = context.user_preferences.addons[__package__].preferences.tab_display_save
            if display_header_save == 'on': 

                row = layout.row(1)
                row.operator("wm.save_mainfile",text="",icon="FILE_TICK") 
                row.operator("wm.save_as_mainfile",text="",icon="SAVE_AS")     
            




        # USE MENUS #
        else:


#            # BOTTOM MENUS #       
#            display_bottom = context.user_preferences.addons[__package__].preferences.tab_display_bottom
#            if display_bottom == 'on': 

            # NAMES / ICONS #  
            display_name = context.user_preferences.addons[__package__].preferences.tab_display_name
            if display_name == 'both_id':  

                # RULER #                         
                ico_ruler = "NOCURVE"                               
                tx_ruler = " Ruler"
                       
                # DISPLAY #
                ico_display = "SNAP_FACE"                             
                tx_display = " Display"

                # SHADING #
                ico_shading = "SMOOTH"                               
                tx_shading = " Shading"

                 # CURSOR TO #
                ico_cursorto = "FORCE_FORCE"                               
                tx_cursorto = " CursorTo"    
  
                # SELECT TO #
                ico_selectto = "RESTRICT_SELECT_OFF"                               
                tx_selectto = " SelectTo"  
                
                # ORIGIN TO #
                ico_originto = "VERTEXSEL"                               
                tx_originto = " OriginTo" 
                
                # ADVANCED #
                ico_advanced = "ALIGN"                               
                tx_advanced = " AlignTo" 

                # SNAPSET #
                ico_snapset = "CURSOR"                               
                tx_snapset = " SnapSet"                  
                  
                # STATION #
                ico_station = "SNAP_ON"                               
                tx_station = " Station"  
 
 
            elif display_name == 'icon_id':  

                # RULER #            
                ico_ruler = "NOCURVE"         
                tx_ruler = ""
            
                # DISPLAY #
                ico_display = "SNAP_FACE"                              
                tx_display = ""
              
                # SHADING #
                ico_shading = "SMOOTH"                               
                tx_shading = "" 

                 # CURSOR TO #
                ico_cursorto = "FORCE_FORCE"                               
                tx_cursorto = ""    
  
                # SELECT TO #
                ico_selectto = "RESTRICT_SELECT_OFF"                               
                tx_selectto = ""  

                # ORIGIN TO #
                ico_originto = "VERTEXSEL"                               
                tx_originto = "" 
                
                # ADVANCED #
                ico_advanced = "ALIGN"                               
                tx_advanced = "" 

                # SNAPSET #
                ico_snapset = "CURSOR"                               
                tx_snapset = ""                  
                  
                # STATION #
                ico_station = "SNAP_ON"                               
                tx_station = ""  

            elif display_name == 'text_id': 

                # RULER #                    
                ico_ruler = "NONE"
                tx_ruler = "Ruler"

                # DISPLAY #
                ico_display = "NONE"                               
                tx_display = "Display"
                
                # SHADING #
                ico_shading = "NONE"                               
                tx_shading = "Shading"                
                
                # CURSOR TO #
                ico_cursorto = "NONE"                               
                tx_cursorto = "CursorTo"    
  
                # SELECT TO #
                ico_selectto = "NONE"                               
                tx_selectto = "SelectTo"  
                
                # ORIGIN TO #
                ico_originto = "NONE"                               
                tx_originto = " OriginTo"  
               
                # ADVANCED #
                ico_advanced = "NONE"                               
                tx_advanced = " AlignTo" 
 
                # SNAPSET #
                ico_snapset = "NONE"                               
                tx_snapset = "SnapSet"                  
                  
                # STATION #
                ico_station = "NONE"                               
                tx_station = "Station"                  




            # OPTIONS #  
            row.menu("VIEW3D_TP_Header_Options_Menu", text="", icon= "SCRIPTWIN")         
            
            row.separator()
           
  
            # RULER #  
            display_ruler = context.user_preferences.addons[__package__].preferences.tab_display_ruler
            if display_ruler == 'on':

                row.menu("VIEW3D_TP_Header_Ruler_Menu", text= tx_ruler, icon= ico_ruler)

                row.separator()
     

             # SNAPSET #   
            display_snapset = context.user_preferences.addons[__package__].preferences.tab_display_snapset
            if display_snapset == 'on': 
              
                row.menu("VIEW3D_TP_Header_SnapSet_Menu", text= tx_snapset, icon= ico_snapset)

                row.separator()               
                

            # SNAP TO #   
            display_snap = context.user_preferences.addons[__package__].preferences.tab_display_snap
            if display_snap == 'on':  

                row.menu("VIEW3D_TP_Header_CursorTo_Menu", text= tx_cursorto, icon= ico_cursorto)

                row.separator()
               
                row.menu("VIEW3D_TP_Header_SelectTo_Menu", text= tx_selectto, icon= ico_selectto)
               
                row.separator()
          
            
            # ORIGIN TO #   
            display_origin = context.user_preferences.addons[__package__].preferences.tab_display_origin
            if display_origin == 'on':  
                
                row.menu("VIEW3D_TP_Origin_Menu", text= tx_originto, icon= ico_originto)

                row.separator()

           
            # ALIGN TO #   
            display_advanced = context.user_preferences.addons[__package__].preferences.tab_display_advanced
            if display_advanced == 'on':  
                
                row.menu("VIEW3D_TP_Origin_Advanced_Menu", text= tx_advanced, icon= ico_advanced)

                row.separator()


            # NP STATION # 
            display_station = context.user_preferences.addons[__package__].preferences.tab_display_station
            if display_station == 'on':  
     
                row.menu("VIEW3D_TP_Header_Station_Menu", text= tx_station, icon= ico_station)

                row.separator()


            # DISPLAY #  
            display_objects = context.user_preferences.addons[__package__].preferences.tab_display_objects
            if display_objects == 'on':  
        
                if obj:
                    row.menu("VIEW3D_TP_Header_Display_Menu", text= tx_display, icon= ico_display)

                    row.separator()


            # SHADING #  
            display_shading = context.user_preferences.addons[__package__].preferences.tab_display_shading
            if display_shading == 'on':  
                
                row.menu("VIEW3D_TP_Header_Shading_Menu", text= tx_shading, icon= ico_shading)

                row.separator()