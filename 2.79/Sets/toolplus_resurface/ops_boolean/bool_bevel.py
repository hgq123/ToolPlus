import time
import random

time_start = False
bl_info = {
    "name": "Boolean Bevel",
    "author": "Rodinkov Ilya",
    "version": (0, 1, 1),
    "blender": (2, 75, 0),
    "location": "View3D > Tools > Boolean Bevel > Bevel",
    "description": "Create bevel after boolean",
    "warning": "This add-on is still in development.",
    "wiki_url": "",
    "category": "Object",
}

import bpy
import bmesh
import addon_utils
from bpy.types import AddonPreferences


class BooleanBevelPreferences(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Instructions:")


# LOAD MODULE #
import bmesh

class ObjectBooleanBevelBridge(bpy.types.Operator):
    """Create the bridge on Object"""
    bl_idname = "object.boolean_bevel_bridge"
    bl_label = "Boolean Bevel Bridge"
    bl_options = {'REGISTER', 'UNDO'}

    number_cuts = bpy.props.IntProperty(name="Bridge Segments", default=5, min=4, max=1000)
    relax = bpy.props.EnumProperty(name="Relax",
                                   items=(("0", "Not Use", "Not Use"),
                                          ("1", "1", "One"),
                                          ("3", "3", "Three"),
                                          ("5", "5", "Five"),
                                          ("10", "10", "Ten"),
                                          ("25", "25", "Twenty-five")),
                                   description="Number of times the loop is relaxed",
                                   default="5")

    interpolation = bpy.props.EnumProperty(name="Interpolation",
                                           items=(("cubic", "Cubic", "Natural cubic spline, smooth results"),
                                                  ("linear", "Linear", "Vertices are projected on existing edges")),
                                           description="Algorithm used for interpolation",
                                           default='cubic')

    def execute(self, context):
        
        # check for needed addons
        loop_tools_addon = "mesh_looptools"
        state = addon_utils.check(loop_tools_addon)
        if not state[0]:
            bpy.ops.wm.addon_enable(module=loop_tools_addon)

        #check for edge selections in bmesh
        object = context.object
        object.update_from_editmode()
        mesh_bm = bmesh.from_edit_mesh(object.data)

        selected_edges = [e for e in mesh_bm.edges if e.select]

        # check wich select mode is active        
        if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, True, False): 
                                    
            # check edge selection value  
            if len(selected_edges) == 2:
 
                bpy.ops.mesh.bridge_edge_loops(type='PAIRS', number_cuts=self.number_cuts, interpolation='SURFACE')
                bpy.ops.mesh.select_less()
                bpy.ops.object.vertex_group_assign_new()
                bpy.ops.mesh.select_less()
                bpy.ops.mesh.delete(type='VERT')
                bpy.ops.object.vertex_group_select()
                bpy.ops.mesh.looptools_relax(iterations=self.relax, interpolation=self.interpolation)

                bpy.ops.mesh.bridge_edge_loops(type='PAIRS', number_cuts=self.number_cuts - 2, interpolation='SURFACE')
                bpy.ops.object.vertex_group_remove(all=False)

                print(self)
                self.report({'INFO'}, "Boolean Bevel Bridge")  

            else:
                self.report({'WARNING'}, "Need 2 selected Edges")
                return {'CANCELLED'}

        else:                
            print(self)
            self.report({'INFO'}, "Need EdgeMode") 
            return {'CANCELLED'}


        return {'FINISHED'}



class ObjectBooleanBevelRemovePipes(bpy.types.Operator):
    """Remove Pipes"""
    bl_idname = "object.boolean_bevel_remove_pipes"
    bl_label = "Remove Pipes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for i in bpy.data.objects:
            if i.name.find("_BB_PIPE") != -1:
                i.select = True
        bpy.ops.object.delete(use_global=False)
        return {'FINISHED'}


class ObjectBooleanBevelPipe(bpy.types.Operator):
    """Create the pipe on Object"""
    bl_idname = "object.boolean_bevel_make_pipe"
    bl_label = "Boolean Bevel Pipe"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}


    # DRAW REDO LAST [F6] #
    def draw(self, context):
        layout = self.layout

        layout = self.layout

        col = layout.column(align=True)

        box = col.box().column(align=True)
        
        row = box.row(align=True)   
        row.prop(self, "all_settings")

        box.separator()

        row = box.row(align=True)   
        row.prop(self, "value_radius", text="Radius")
        row.prop(self, "sides", text="Side")

        box.separator()
        
        row = box.row(align=True)   
        row.prop(self, "simplify")
        row.prop(self, "subdivide", text="Subdiv")

        box.separator()

        row = box.row(align=True)   
        row.prop(self, "repeat", text="Relax")
        row.prop(self, "relax", text="Factor")

        box.separator()

        if self.all_settings:

            box = col.box().column(1)
            
            row = box.row(align=True) 
            row.prop(self, "sharp")
            row.prop(self, "sharp_angle")

            box.separator()

            row = box.row(align=True) 
            row.prop(self, "fix_curve", text="Fix Twist")
            row.prop(self, "curve_tilt")
            box.separator()

            row = box.column(align=True) 
            row.prop(self, "twist_mode")
            row.prop(self, "interpolation")

            box.separator()

            row = box.row(align=True) 
            row.prop(self, "vertex_remove")
            row.prop(self, "smooth")
  
            box.separator()


    all_settings = bpy.props.BoolProperty(name="Show all settings", default=False)

    value_radius = bpy.props.FloatProperty(name="Pipe Radius", default=0.05, min=0.0001, max=30.0, step=1)
    sides = bpy.props.IntProperty(name="Pipe Sides", default=8, min=3, max=100)

    relax = bpy.props.EnumProperty(name="Relax Factor",
                                   items=(("0", "Not Use", "Not Use"),
                                          ("1", "1", "One"),
                                          ("3", "3", "Three"),
                                          ("5", "5", "Five"),
                                          ("10", "10", "Ten"),
                                          ("25", "25", "Twenty-five")),
                                   description="Number of times the loop is relaxed",
                                   default="5")

    repeat = bpy.props.IntProperty(name="Repeat relax", default=1, min=1, max=1000)

    simplify = bpy.props.FloatProperty(name="Simplify", default=0.0, min=0.0, max=1.0, unit="ROTATION", step=100)

    subdivide = bpy.props.IntProperty(name="Subdivide Patch", default=0, min=0, max=500)

    sharp = bpy.props.BoolProperty(name="Sharp Edge", default=False)
    sharp_angle = bpy.props.FloatProperty(name="Sharp angle", default=0.523599, min=0.0, max=3.0, unit="ROTATION",
                                          step=100)

    fix_curve = bpy.props.BoolProperty(name="Fix Curve Twist", default=True)
    curve_tilt = bpy.props.FloatProperty(name="Mean Tilt", default=45.0, min=-45.0, max=45.0)
    twist_mode = bpy.props.EnumProperty(name="Twist Mode",
                                        items=(("MINIMUM", "Minimum", "Use the least twist over the entire curve"),
                                               ("TANGENT", "Tangent", "Use the tangent to calculate twist")),
                                        description="The type of tilt calculation for 3D Curves",
                                        default="MINIMUM")

    smooth = bpy.props.IntProperty(name="Smooth", default=60, min=0, max=500)
    vertex_remove = bpy.props.FloatProperty(name="Remove Vertex", default=0.00001, min=0.0, max=5.0, step=0.1)

    interpolation = bpy.props.EnumProperty(name="Interpolation",
                                           items=(("cubic", "Cubic", "Natural cubic spline, smooth results"),
                                                  ("linear", "Linear", "Vertices are projected on existing edges")),
                                           description="Algorithm used for interpolation",
                                           default='cubic')


    def execute(self, context):
        custom = False
        loop_tools_addon = "mesh_looptools"
        state = addon_utils.check(loop_tools_addon)
        if not state[0]:
            bpy.ops.wm.addon_enable(module=loop_tools_addon)

        if bpy.data.objects.find('BOOLEAN_BEVEL_GUIDE_CUSTOM') != -1:
            custom = True

        scene = context.scene
        src_obj = scene.objects.active

        if not custom:
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'})
            duplicate = scene.objects.active
        # have_bool = prepare_object(scene, duplicate, False, None, None,
        #                            "False")



        if not custom:
            have_bool = prepare_object(scene, duplicate, False, None, None,
                                       "False")
        else:
            have_bool = [True, 0, "NoName"]

        if have_bool[0]:
            if not custom:
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=have_bool[1])
            scene.objects.active = src_obj
            if not custom:
                bpy.ops.object.modifier_remove(modifier=have_bool[1])
                scene.objects.active = duplicate

                guide = get_guide(scene, self.simplify, self.subdivide, self.relax, custom, self.sharp,
                                  self.sharp_angle,
                                  self.interpolation, self.vertex_remove, self.repeat, duplicate, have_bool[2])

            else:
                guide = get_guide(scene, self.simplify, self.subdivide, self.relax, custom, self.sharp,
                                  self.sharp_angle,
                                  self.interpolation, self.vertex_remove, self.repeat, src_obj, have_bool[2])
            if not custom:
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=have_bool[1])
            # bpy.ops.object.select_all(action='DESELECT')
            # scene.objects.active = src_obj
            if not guide:
                self.report({'ERROR'}, "Error on get_guide")
                return {'CANCELLED'}
            else:
                create_curve(self.value_radius, self.sides, self.fix_curve, self.curve_tilt, self.twist_mode, scene,
                             self.smooth)

            pipe = scene.objects.active
            pipe.name = src_obj.name + "_BB_PIPE"
            # bpy.ops.object.select_all(action='DESELECT')
            # pipe.select = True
            # bpy.ops.object.convert(target='MESH')
            bpy.data.objects["BOOLEAN_BEVEL_CURVE_PROFILE"].name = pipe.name + "_PROFILE"

        bpy.ops.object.select_all(action='DESELECT')

        if not custom:
            duplicate.select = True
            bpy.ops.object.delete(use_global=False)

        clear_objects(scene, pipe)
        return {'FINISHED'}


class ObjectBooleanBevelSymmetrize(bpy.types.Operator):
    """Symmetrize Object"""
    bl_idname = "object.boolean_bevel_symmetrize"
    bl_label = "Boolean Bevel Symmetrize"
    bl_options = {'REGISTER', 'UNDO'}

    direction = bpy.props.EnumProperty(name="Direction",
                                       items=(("NEGATIVE_X", "-x to +x", "-x to +x"),
                                              ("POSITIVE_X", "+x to -x", "+x to -x"),
                                              ("NEGATIVE_Y", "-y to +y", "-y to +y"),
                                              ("POSITIVE_Y", "+y to -y", "+y to -y"),
                                              ("NEGATIVE_Z", "-z to +z", "-z to +z"),
                                              ("POSITIVE_Z", "+z to -z", "+z to -z")),
                                       description="",
                                       default="NEGATIVE_X")

    threshold = bpy.props.FloatProperty(name="Threshold", default=0.0001, min=0, max=1000, step=0.01)

    def execute(self, context):
        src_obj = bpy.context.active_object
        # bpy.ops.object.vertex_group_remove(all=True)
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'})
        normals_object = bpy.context.active_object
        normals_object.name = src_obj.name + "_Normals"

        if self.direction[-1] == "X":
            transform_value = (-1.0, 1.0, 1.0)
            axys = 0
        elif self.direction[-1] == "Y":
            axys = 1
            transform_value = (1.0, -1.0, 1.0)
        elif self.direction[-1] == "Z":
            axys = 2
            transform_value = (1.0, 1.0, -1.0)

        print(axys)
        bpy.context.scene.objects.active = src_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.symmetrize(direction=self.direction, threshold=self.threshold)
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(src_obj.data)

        if self.direction.find("NEGATIVE") != -1:
            for vert in bm.verts:
                if vert.co[axys] >= -0.0 or vert.co[axys] >= 0.0:
                    vert.select = True
                    # print(vert.co[0])
        else:
            for vert in bm.verts:
                if vert.co[axys] <= 0.0 or vert.co[axys] <= -0.0:
                    vert.select = True
                    # print(vert.co[0])
        bpy.ops.mesh.select_more(use_face_step=True)
        bpy.ops.mesh.select_less(use_face_step=True)
        # bpy.ops.mesh.split()
        src_obj.vertex_groups.new(name="symmetrize")
        bpy.ops.object.vertex_group_assign()
        symmetrize_group = src_obj.vertex_groups.active.name
        bpy.ops.object.mode_set(mode='OBJECT')

        data_transfer_modifier = src_obj.modifiers.new(name="Boolean Bevel Custom Normals", type="DATA_TRANSFER")
        data_transfer_modifier.object = normals_object
        data_transfer_modifier.use_vert_data = True
        data_transfer_modifier.vert_mapping = "NEAREST"
        data_transfer_modifier.use_loop_data = True
        data_transfer_modifier.loop_mapping = "POLYINTERP_NEAREST"
        # data_transfer_modifier.vertex_group = symmetrize_group
        data_transfer_modifier.data_types_verts = {'VGROUP_WEIGHTS'}
        data_transfer_modifier.data_types_loops = {"CUSTOM_NORMAL"}
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=data_transfer_modifier.name)

        bpy.context.scene.objects.active = normals_object
        bpy.ops.transform.resize(value=transform_value)

        bpy.context.scene.objects.active = src_obj
        data_transfer_modifier = src_obj.modifiers.new(name="Boolean Bevel Custom Normals", type="DATA_TRANSFER")
        data_transfer_modifier.object = normals_object
        data_transfer_modifier.use_vert_data = True
        data_transfer_modifier.vert_mapping = "NEAREST"
        data_transfer_modifier.use_loop_data = True
        data_transfer_modifier.loop_mapping = "POLYINTERP_NEAREST"
        data_transfer_modifier.vertex_group = symmetrize_group
        data_transfer_modifier.data_types_verts = {'VGROUP_WEIGHTS'}
        data_transfer_modifier.data_types_loops = {"CUSTOM_NORMAL"}
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=data_transfer_modifier.name)

        normals_object.select = True
        bpy.ops.object.delete(use_global=False)
        src_obj.select = True
        bpy.context.scene.objects.active = src_obj
        bpy.ops.object.vertex_group_remove(all=True)
        return {'FINISHED'}


class ObjectBooleanBevelApplyModifiers(bpy.types.Operator):
    """Apply all modifiers on selected Objects"""
    bl_idname = "object.boolean_bevel_apply_modifiers"
    bl_label = "Boolean Bevel Apply Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    all = bpy.props.BoolProperty(name="Apply All Modifiers", default=True)

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            for modifier in obj.modifiers:
                modifier.show_viewport = False

            context.scene.objects.active = obj
            for modifier in obj.modifiers:
                if self.all:
                    try:
                        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
                    except:
                        bpy.ops.object.modifier_remove(modifier=modifier.name)
                elif modifier.name.find("Boolean Bevel") != -1:
                    try:
                        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
                    except:
                        bpy.ops.object.modifier_remove(modifier=modifier.name)

            for modifier in obj.modifiers:
                modifier.show_viewport = True
        return {'FINISHED'}


class ObjectBooleanBevelRemoveModifiers(bpy.types.Operator):
    """Remove all modifiers on selected Objects"""
    bl_idname = "object.boolean_bevel_remove_modifiers"
    bl_label = "Boolean Bevel Remove Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    all = bpy.props.BoolProperty(name="Remove  All Modifiers", default=True)

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            for modifier in obj.modifiers:
                modifier.show_viewport = False

            context.scene.objects.active = obj

            for modifier in obj.modifiers:
                if self.all:
                    bpy.ops.object.modifier_remove(modifier=modifier.name)
                elif modifier.name.find("Boolean Bevel") != -1:
                    bpy.ops.object.modifier_remove(modifier=modifier.name)

            for modifier in obj.modifiers:
                modifier.show_viewport = True
        return {'FINISHED'}


class ObjectBooleanBevelRemoveObjects(bpy.types.Operator):
    """Remove all created Guides and Curves"""
    bl_idname = "object.boolean_bevel_remove_objects"
    bl_label = "Boolean Bevel Remove Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for i in ['BOOLEAN_BEVEL_CURVE', 'BOOLEAN_BEVEL_GUIDE', 'BOOLEAN_BEVEL_CURVE_PROFILE',
                  'BOOLEAN_BEVEL_GUIDE_CUSTOM']:
            index = bpy.data.objects.find(i)
            if index != -1:
                bpy.data.objects[i].select = True
                bpy.ops.object.delete(use_global=False)
        return {'FINISHED'}


class ObjectBooleanBevel(bpy.types.Operator):
    """Create the bevel on Object"""
    bl_idname = "object.boolean_bevel"
    bl_label = "Boolean Bevel"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # DRAW REDO LAST [F6] #
    def draw(self, context):

        layout = self.layout
        box = layout.box()
      
        row = box.row(align=True)                
        row.label("Show/Hide:")
        row.prop(self, "wire")
        row.prop(self, "preview_curve")

        row = box.row(align=True)
        row.prop(self, "all_settings", text="Enable additional Settings")

        ###
        box = layout.box()      
        box.label("Basic Parameters:")
       
        box.prop(self, "change_operation")

        box.separator()

        row = box.row(align=True)
        row.prop(self, "value_radius", text="Radius")
        row.prop(self, "bevel_width", text="Width")
        
        row = box.row(align=True)
        row.prop(self, "fillet_profile", text="Profile")
        row.prop(self, "fillet_segments", text="Segments")  

        row = box.row(align=True)
        row.prop(self, "simplify")   
        row.prop(self, "sides", text="Sides")
 
   
        if self.all_settings:    
                
#            row = box.row(align=True)
#            row.prop(self, "change_subdivide", text="Sudivide")           

#            if self.change_subdivide:

#                row = box.row(align=True)
#                row.prop(self, "subdiv_a", text="SDiv A")
#                row.prop(self, "subdiv_b", text="SDiv B") 

                      
            box.prop(self, "do_bevel")
            box.prop(self, "stop_calc")
            box.prop(self, "custom_normals")


        ###
        box = layout.box()
        box.label("Curve Parameters:")
      
        row = box.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(self, "sharp")
        row.prop(self, "sharp_angle") 
  
        row = box.row(align=True)
        row.label("Relax:") 
        row.prop(self, "relax", text="")
     
        row = box.row(align=True) 
        row.label("Relax Repeat:") 
        row.prop(self, "repeat", text="")


        if self.all_settings:

            row = box.row(align=True)
            row.label("Interpolation:")        
            row.prop(self, "interpolation", text="")

            box.separator()
      
            row = box.row(align=True)  
            row.prop(self, "vertex_remove", text="Remove")
            row.prop(self, "subdivide", text="SDiv Patch")

            box.separator() 
            
            box.prop(self, "smooth_bevel")
            if self.smooth_bevel:

                row = box.row(align=True)
                row.prop(self, "smooth_bevel_value", text="Value")
                row.prop(self, "smooth_bevel_step", text="Steps")
                
        box.separator()     


        if self.all_settings:

            ###
            box = layout.box()
            box.label("Other Parameters:")
            box.prop(self, "fix_curve")
       
            row = box.row(align=True)
            row.prop(self, "curve_tilt", text="Tilt")
            row.prop(self, "smooth", text="Smooth")      

            row = box.row(align=True)
            row.label("Twist:") 
            row.prop(self, "twist_mode", text="")
           
            row = box.row(align=True)
            row.label("Path:")          
            row.prop(self, "union_path", text="")

            box.separator()

            box.prop(self, "triangulate", text="Triangulate Ngons")
            if self.triangulate:
                box.prop(self, "method")
           
            box.separator()

        ###
        box = layout.box()
        box.prop(self, "use_material", text="Random Material")       





    # PROPS #
    interpolation = bpy.props.EnumProperty(name="Interpolation",
                                           items=(("cubic", "Cubic", "Natural cubic spline, smooth results"),
                                                  ("linear", "Linear", "Vertices are projected on existing edges")),
                                           description="Algorithm used for interpolation",
                                           default='cubic')

    wire = bpy.props.BoolProperty(name="Wire", default=True)

    change_operation = bpy.props.EnumProperty(name="Operation",
                                              items=(("False", "Not change", "Not change"),
                                                     ("UNION", "Union", "Use Union"),
                                                     ("DIFFERENCE", "Difference", "Use Difference"),
                                                     ("INTERSECT", "Intersect", "Use Intersect"),
                                                     ("SLICE", "Slice", "Use Slice")),
                                              description="Change Boolean Operation",
                                              default="False")

    change_subdivide = bpy.props.BoolProperty(name="Change subdivide", default=False)
    subdiv_a = bpy.props.IntProperty(name="Subdivision A", default=1, min=0, max=6)
    subdiv_b = bpy.props.IntProperty(name="Subdivision B", default=1, min=0, max=6)

    sharp = bpy.props.BoolProperty(name="Sharp Edge", default=False)
    sharp_angle = bpy.props.FloatProperty(name="Sharp angle", default=0.523599, min=0.0, max=3.0, unit="ROTATION",
                                          step=100)
    simplify = bpy.props.FloatProperty(name="Simplify", default=0.0, min=0.0, max=1.0, unit="ROTATION", step=100)

    subdivide = bpy.props.IntProperty(name="Subdivide Patch", default=0, min=0, max=500)
    relax = bpy.props.EnumProperty(name="Relax factor",
                                   items=(("0", "Not Use", "Not Use"),
                                          ("1", "1", "One"),
                                          ("3", "3", "Three"),
                                          ("5", "5", "Five"),
                                          ("10", "10", "Ten"),
                                          ("25", "25", "Twenty-five")),
                                   description="Number of times the loop is relaxed",
                                   default="5")
    repeat = bpy.props.IntProperty(name="Repeat relax", default=1, min=1, max=1000)
    value_radius = bpy.props.FloatProperty(name="Cut Radius", default=0.07, min=0.0001, max=30.0, step=1)
    sides = bpy.props.IntProperty(name="Sides of circle", default=8, min=3, max=10)
    fix_curve = bpy.props.BoolProperty(name="Fix Curve Twist", default=True)
    curve_tilt = bpy.props.FloatProperty(name="Mean Tilt", default=45.0, min=-45.0, max=45.0)
    twist_mode = bpy.props.EnumProperty(name="Twist Mode",
                                        items=(("MINIMUM", "Minimum", "Use the least twist over the entire curve"),
                                               ("TANGENT", "Tangent", "Use the tangent to calculate twist")),
                                        description="The type of tilt calculation for 3D Curves",
                                        default="MINIMUM")
    smooth = bpy.props.IntProperty(name="Smooth", default=60, min=0, max=500)
    preview_curve = bpy.props.BoolProperty(name="Curve", default=False)

    union_path = bpy.props.EnumProperty(name="Path Operation",
                                        items=(("UNION", "Union", "Use Union"),
                                               ("DIFFERENCE", "Difference", "Use Difference")),
                                        description="Change Boolean Operation",
                                        default="UNION")

    fillet_profile = bpy.props.FloatProperty(name="Fillet Profile", default=0.7, min=-0.15, max=1.0)
    fillet_segments = bpy.props.IntProperty(name="Fillet Segments", default=5, min=0, max=30)

    triangulate = bpy.props.BoolProperty(name="Split NGon", default=False)
    method = bpy.props.EnumProperty(name="Method",
                                    items=(("BEAUTY", "BEAUTY", "Use BEAUTY"),
                                           ("CLIP", "CLIP", "Use CLIP")),
                                    description="Method for splitting the polygons into triangles",
                                    default="BEAUTY")
    smooth_bevel = bpy.props.BoolProperty(name="Smooth Bevel", default=False)
    smooth_bevel_value = bpy.props.IntProperty(name="Smooth Value", default=5, min=0, max=30)
    smooth_bevel_step = bpy.props.IntProperty(name="Smooth Step", default=3, min=0, max=1000)

    vertex_remove = bpy.props.FloatProperty(name="Remove Vertex", default=0.00001, min=0.0, max=5.0, step=0.1)

    use_material = bpy.props.BoolProperty(name="Use Materials", default=False)

    stop_calc = bpy.props.BoolProperty(name="Stop calculations", default=False)

    all_settings = bpy.props.BoolProperty(name="All settings", default=False)

    do_bevel = bpy.props.BoolProperty(name="Create Bevel", default=True)

    custom_normals = bpy.props.BoolProperty(name="Custom Normals", default=True)

    # flip_normals = bpy.props.BoolProperty(name="Flip Normals", default=True)

    bevel_width = bpy.props.IntProperty(name="Bevel_width", default=98, min=0, max=100)


    def execute(self, context):
        loop_tools_addon = "mesh_looptools"
        state = addon_utils.check(loop_tools_addon)
        if not state[0]:
            bpy.ops.wm.addon_enable(module=loop_tools_addon)
        global time_start
        if self.stop_calc:
            return {'FINISHED'}

        time_start = time.time()
        context.tool_settings.vertex_group_weight = 1.0
        custom = False
        scene = context.scene
        src_obj = scene.objects.active
        clear_objects(scene, src_obj)
        # bpy.ops.object.select_all(action='DESELECT')
        # scene.objects.active = src_obj
        if bpy.data.objects.find('BOOLEAN_BEVEL_GUIDE_CUSTOM') != -1:
            custom = True

        if not custom:
            have_bool = prepare_object(scene, src_obj, self.change_subdivide, self.subdiv_a, self.subdiv_b,
                                       self.change_operation)
        else:
            have_bool = [True, 0, "NoName"]
        print("Prepare: %.4f sec" % (time.time() - time_start))
        if have_bool[0]:
            src_obj.show_wire = self.wire
            src_obj.show_all_edges = self.wire
            if self.custom_normals:
                src_obj.select = True
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'})
                normals_object = scene.objects.active
                normals_object.name = src_obj.name + "_Normals"
                src_obj.select = False
                normals_object.select = True
                bpy.ops.object.shade_smooth()
                normals_object.hide_render = True
                normals_object.draw_type = 'BOUNDS'
                # normals_object.hide = True
                if not custom:
                    normals_object_bool = normals_object.modifiers[len(normals_object.modifiers) - 1].object
                    operation_name = normals_object.modifiers[len(normals_object.modifiers) - 1].operation
                    bpy.ops.object.modifier_remove(
                        modifier=normals_object.modifiers[len(normals_object.modifiers) - 1].name)

                    bpy.ops.object.select_all(action='DESELECT')

                    normals_object_bool.select = True
                    scene.objects.active = normals_object_bool
                    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'})
                    normals_object_bool = scene.objects.active
                    normals_object_bool.name = src_obj.name + "_Normals_bool"
                    # src_obj.select = False
                    bpy.ops.object.select_all(action='DESELECT')
                    normals_object_bool.select = True
                    bpy.ops.object.shade_smooth()
                    print(scene.objects.active.name)
                    if operation_name == "DIFFERENCE":
                        bpy.ops.object.mode_set(mode='EDIT')
                        bpy.ops.mesh.select_mode(type='VERT')
                        bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.mesh.flip_normals()
                        # bpy.ops.mesh.normals_make_consistent(inside=self.flip_normals)
                        bpy.ops.object.mode_set(mode='OBJECT')

                    normals_object_bool.hide_render = True
                    normals_object_bool.draw_type = 'BOUNDS'
                    # normals_object_bool.hide = True

                scene.objects.active = src_obj
                bpy.ops.object.select_all(action='DESELECT')
            if self.change_operation == "SLICE" and not custom:
                src_obj.select = True
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'})
                slice_object = scene.objects.active
                slice_object.name = src_obj.name + "_SLICE"
                slice_object.modifiers[len(slice_object.modifiers) - 1].operation = "INTERSECT"
                slice_name = slice_object.modifiers[len(slice_object.modifiers) - 1].object.name

                slice_object.vertex_groups.clear()
                # bpy.ops.object.mode_set(mode='EDIT')
                # bpy.ops.mesh.reveal()
                # bpy.ops.mesh.select_mode(type='FACE')
                # bpy.ops.mesh.select_all(action='SELECT')
                # slice_object.vertex_groups.new(name=src_obj.name)
                # bpy.ops.object.vertex_group_assign()
                # # bpy.ops.mesh.select_all(action='DESELECT')
                # # bpy.ops.mesh.hide(unselected=False)
                # bpy.ops.object.mode_set(mode='OBJECT')

                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=have_bool[1])
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='FACE')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.reveal()
                slice_object.vertex_groups.new(name=src_obj.name)
                bpy.ops.object.vertex_group_assign()
                bpy.ops.mesh.select_all(action='INVERT')
                slice_object.vertex_groups.new(name=slice_name)
                bpy.ops.object.vertex_group_assign()
                # return {'FINISHED'}
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.hide(unselected=False)

                bpy.ops.object.mode_set(mode='OBJECT')
                # return {'FINISHED'}
                #
                # if self.custom_normals:
                #     normals_object.select = True
                #     # scene.objects.active = normals_object
                #     bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'})
                #     normals_object = scene.objects.active
                #     normals_object.name = slice_object.name + "_Normals"
                #     slice_object.select = False
                #     normals_object.select = True
                #     bpy.ops.object.shade_smooth()
                #     normals_object.hide_render = True
                #     normals_object.hide = True
                #     # normals_object_bool = normals_object.modifiers[len(normals_object.modifiers) - 1].object
                #     # operation_name = normals_object.modifiers[len(normals_object.modifiers) - 1].operation
                #     # bpy.ops.object.modifier_remove(
                #     #     modifier=normals_object.modifiers[len(normals_object.modifiers) - 1].name)
                #
                #     bpy.ops.object.select_all(action='DESELECT')

                # normals_object_bool.select = True
                # scene.objects.active = normals_object_bool
                # bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'})
                # normals_object_bool = scene.objects.active
                # normals_object_bool.name = src_obj.name + "_Normals_bool"
                # src_obj.select = False
                # normals_object_bool.select = True
                # bpy.ops.object.shade_smooth()
                # # print(operation_name)
                # # if operation_name == "DIFFERENCE":
                # #     bpy.ops.object.mode_set(mode='EDIT')
                # #     bpy.ops.mesh.select_mode(type='VERT')
                # #     bpy.ops.mesh.flip_normals()
                # #     bpy.ops.object.mode_set(mode='OBJECT')
                # normals_object_bool.hide_render = True
                # normals_object_bool.hide = True

                scene.objects.active = src_obj
                bpy.ops.object.select_all(action='DESELECT')

            if not custom:
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=have_bool[1])

            guide = get_guide(scene, self.simplify, self.subdivide, self.relax, custom, self.sharp, self.sharp_angle,
                              self.interpolation, self.vertex_remove, self.repeat, src_obj, have_bool[2])

            print("Get Guide: %.4f sec" % (time.time() - time_start))
            if not guide:
                self.report({'ERROR'}, "Error on get_guide")
                return {'CANCELLED'}
            else:
                create_curve(self.value_radius, self.sides, self.fix_curve, self.curve_tilt, self.twist_mode, scene,
                             self.smooth)
                print("Create Curve: %.4f sec" % (time.time() - time_start))
                if self.preview_curve:
                    return {'FINISHED'}
                else:
                    do_boolean(scene, src_obj, self.union_path)
                    print("Do Boolean: %.4f sec" % (time.time() - time_start))
                    create_bevel(scene, src_obj, self.fillet_profile, self.fillet_segments, self.triangulate,
                                 self.smooth_bevel, self.method, self.smooth_bevel_value, self.smooth_bevel_step,
                                 have_bool[2], self.do_bevel, self.custom_normals, self.bevel_width)
                    if self.use_material:
                        set_material(self.smooth_bevel, src_obj, have_bool[2])
                    print("Create Bevel: %.4f sec" % (time.time() - time_start))

                    if self.custom_normals:
                        for modifier in src_obj.modifiers:
                            modifier.show_viewport = False

                        for modifier in src_obj.modifiers:
                            try:
                                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
                            except:
                                bpy.ops.object.modifier_remove(modifier=modifier.name)
                        src_obj.vertex_groups.clear()

                    if self.change_operation == "SLICE" and not custom:
                        scene.objects.active = slice_object
                        do_boolean(scene, slice_object, self.union_path)
                        create_bevel(scene, slice_object, self.fillet_profile, self.fillet_segments, self.triangulate,
                                     self.smooth_bevel, self.method, self.smooth_bevel_value, self.smooth_bevel_step,
                                     have_bool[2], self.do_bevel, self.custom_normals, self.bevel_width)
                        if self.use_material:
                            set_material(self.smooth_bevel, slice_object, have_bool[2])

                        if self.custom_normals:
                            for modifier in slice_object.modifiers:
                                modifier.show_viewport = False

                            for modifier in slice_object.modifiers:
                                try:
                                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
                                except:
                                    bpy.ops.object.modifier_remove(modifier=modifier.name)
                            slice_object.vertex_groups.clear()

                    clear_objects(scene, src_obj)

                    if self.custom_normals:
                        bpy.ops.object.select_all(action='DESELECT')
                        if not custom:
                            bpy.data.objects[src_obj.name + "_Normals_bool"].select = True
                        bpy.data.objects[src_obj.name + "_Normals"].select = True

                        bpy.ops.object.delete(use_global=False)
                        src_obj.select = True
                        scene.objects.active = src_obj
                    print("Finish: %.4f sec\n" % (time.time() - time_start))

                    return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Object does not have a Boolean modifier")
            return {'CANCELLED'}


class ObjectBooleanCustomBevel(bpy.types.Operator):
    """Create variable bevel on Object"""
    bl_idname = "object.boolean_custom_bevel"
    bl_label = "Boolean Custom Bevel"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # DRAW REDO LAST [F6] #
    def draw(self, context):

        layout = self.layout

        box = layout.box()

        row = box.row(align=True)
        row.prop(self, "all_settings", text="Enable additional Settings")
    
        ###
        box = layout.box()      
     
        row = box.row(align=True)       
        row.label("BoolPath:")
        row.prop(self, "union_path", text="")

        box.separator()

        row = box.column(align=True)
        row.prop(self, "fillet_profile", text="Profile")
        row.prop(self, "fillet_segments", text="Segments")
        row.prop(self, "bevel_width", text="Width")

        box.separator()

        if self.all_settings:
            
            box = layout.box() 

            box.prop(self, "smooth_bevel")
          
            if self.smooth_bevel:
                
                row = box.column(align=True)            
                row.prop(self, "smooth_bevel_value")
                row.prop(self, "smooth_bevel_step")


            box = layout.box()
            
            box.prop(self, "triangulate")

            if self.triangulate:
                box.prop(self, "method")

            box.separator()
            
            box.prop(self, "stop_calc")
            box.prop(self, "do_bevel")
            box.prop(self, "custom_normals")
            box.prop(self, "remove")
           
            box.separator()
        
        ###
        box = layout.box()
        box.prop(self, "use_material", text="Random Material")


    # PROPS #
    all_settings = bpy.props.BoolProperty(name="All settings", default=False)

    union_path = bpy.props.EnumProperty(name="Path Operation",
                                        items=(("UNION", "Union", "Use Union"),
                                               ("DIFFERENCE", "Difference", "Use Difference")),
                                        description="Change Path Operation",
                                        default="UNION")

    fillet_profile = bpy.props.FloatProperty(name="Fillet Profile", default=0.7, min=-0.15, max=1.0)
    fillet_segments = bpy.props.IntProperty(name="Fillet Segments", default=20, min=0, max=30)
    remove = bpy.props.BoolProperty(name="Remove Curve and Guide", default=True)

    triangulate = bpy.props.BoolProperty(name="Triangulate", default=False)
    method = bpy.props.EnumProperty(name="Method",
                                    items=(("BEAUTY", "BEAUTY", "Use BEAUTY"),
                                           ("CLIP", "CLIP", "Use CLIP")),
                                    description="Method for splitting the polygons into triangles",
                                    default="BEAUTY")

    do_bevel = bpy.props.BoolProperty(name="Create Bevel", default=True)
    smooth_bevel = bpy.props.BoolProperty(name="Smooth Bevel", default=False)
    smooth_bevel_value = bpy.props.IntProperty(name="Smooth Value", default=1, min=0, max=30)
    smooth_bevel_step = bpy.props.IntProperty(name="Smooth Step", default=3, min=0, max=1000)

    use_material = bpy.props.BoolProperty(name="Use Materials", default=False)

    stop_calc = bpy.props.BoolProperty(name="Stop calculations", default=False)
    custom_normals = bpy.props.BoolProperty(name="Custom Normals", default=True)
    bevel_width = bpy.props.IntProperty(name="Bevel_width", default=98, min=0, max=100)
    

    def execute(self, context):
        try:
            state = addon_utils.check("mesh_looptools")
            print(state)
            if not state[0]:
                bpy.ops.wm.addon_enable(module="mesh_looptools")
        except:
            self.report({'ERROR'}, "Loop Tools not installed.")
            return {'CANCELLED'}

        if self.stop_calc:
            return {'FINISHED'}
        scene = context.scene
        src_obj = scene.objects.active
        try:
            do_boolean(scene, src_obj, self.union_path)
            create_bevel(scene, src_obj, self.fillet_profile, self.fillet_segments, self.triangulate, self.smooth_bevel,
                         self.method, self.smooth_bevel_value, self.smooth_bevel_step, "NoName", self.do_bevel,
                         self.custom_normals, self.bevel_width)
            if self.use_material:
                set_material(self.smooth_bevel, src_obj, "NoName_")
        except:
            pass

        if self.custom_normals:
            for modifier in src_obj.modifiers:
                modifier.show_viewport = False

            for modifier in src_obj.modifiers:
                try:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
                except:
                    bpy.ops.object.modifier_remove(modifier=modifier.name)
            src_obj.vertex_groups.clear()

            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[src_obj.name + "_Normals_bool"].select = True
            bpy.data.objects[src_obj.name + "_Normals"].select = True

            bpy.ops.object.delete(use_global=False)
            src_obj.select = True
            scene.objects.active = src_obj

        if self.remove:
            clear_objects(scene, src_obj)

        return {'FINISHED'}


class ObjectBooleanBevelCustomEdge(bpy.types.Operator):
    """Create bevel on selected edges"""
    bl_idname = "object.boolean_bevel_custom_edge"
    bl_label = "Boolean Bevel Custom Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        loop_tools_addon = "mesh_looptools"
        state = addon_utils.check(loop_tools_addon)
        if not state[0]:
            bpy.ops.wm.addon_enable(module=loop_tools_addon)

        scene = context.scene
        src_obj = scene.objects.active
        try:
            bpy.ops.mesh.duplicate_move()
            bpy.ops.mesh.separate(type='SELECTED')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.hide(unselected=False)
            bpy.ops.object.mode_set(mode='OBJECT')
            guide = bpy.context.selected_objects[0]
            guide.name = "BOOLEAN_BEVEL_GUIDE_CUSTOM"
        except:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.ed.undo()
            return False
        src_obj.select = True
        scene.objects.active = src_obj
        # bpy.ops.object.boolean_bevel('INVOKE_DEFAULT')
        return {'FINISHED'}


#class BooleanBevelPanel(bpy.types.Panel):
#    bl_label = "Boolean Bevel"
#    bl_space_type = 'VIEW_3D'
#    bl_region_type = 'TOOLS'
#    bl_category = "Tools"

#    def draw(self, context):
#        layout = self.layout
#        split = layout.split()
#        col = split.column(align=True)
#        if bpy.context.object:
#            if 0 < len(bpy.context.selected_objects) < 2 and bpy.context.object.mode == "OBJECT":
#                col.operator("object.boolean_bevel", text="Bevel", icon='MOD_BEVEL')
#                col.operator("object.boolean_bevel_symmetrize", text="Symmetrize", icon='MOD_MIRROR')
#                col.operator("object.boolean_bevel_make_pipe", text="Make Pipe", icon="MOD_CURVE")

#                if bpy.data.objects.find('BOOLEAN_BEVEL_CURVE') != -1 and bpy.data.objects.find(
#                        'BOOLEAN_BEVEL_GUIDE') != -1:
#                    col.operator("object.boolean_custom_bevel", text="Custom Bevel", icon='MOD_BEVEL')
#            if bpy.context.object.mode == "EDIT":
#                col.operator("object.boolean_bevel_custom_edge", text="Custom Edge", icon='EDGESEL')
#                # col.operator("object.boolean_bevel_bridge", text="Bridge Edge", icon='EDGESEL')
#        col.separator()
#        col.operator("object.boolean_bevel_remove_objects", text="Remove Objects", icon='X')
#        if len(bpy.context.selected_objects) > 0 and bpy.context.object.mode == "OBJECT":
#            col.operator("object.boolean_bevel_apply_modifiers", text="Apply Modifiers", icon='IMPORT')
#            col.operator("object.boolean_bevel_remove_modifiers", text="Remove Modifiers", icon='X')
#        col.operator("object.boolean_bevel_remove_pipes", text="Remove Pipes", icon='X')


def prepare_object(scene, src_obj, change_subdivide, subdiv_a, subdiv_b, change_operation):
    print("Prepare start: %.4f sec" % (time.time() - time_start))
    modifiers = src_obj.modifiers
    boolean = False
    bool_object = False
    subsurf_boolean = False
    subsurf_object = False

    for modifier in modifiers:
        modifier.show_viewport = False
    if len(modifiers) > 0:
        # проверка на наличие булена
        for modifier in modifiers:
            if modifier.type == "BOOLEAN":
                boolean = modifier
                bool_object = modifier.object
                break
    print("Prepare Modifiers: %.4f sec" % (time.time() - time_start))
    if boolean and (bool_object != False):
        # смена операции

        if change_operation != "False":
            if change_operation == "SLICE":
                boolean.operation = "DIFFERENCE"
            else:
                boolean.operation = change_operation
        # ищем последние модификаторы подразделения
        for modifier in bool_object.modifiers:
            if modifier.type == "SUBSURF":
                subsurf_object = modifier
        for modifier in modifiers:
            if modifier.type == "SUBSURF":
                subsurf_boolean = modifier
        # меняем подразделение
        if change_subdivide:
            if subsurf_boolean != False:
                subsurf_boolean.levels = subdiv_a
            if subsurf_object != False:
                subsurf_object.levels = subdiv_b
        print("Prepare Other: %.4f sec" % (time.time() - time_start))
        for modifier in modifiers:
            # пропускаем фаски
            if modifier.name.find("Boolean Bevel") == -1:
                # если булен
                if modifier.type == "BOOLEAN":
                    print("Prepare Boolean: %.4f sec" % (time.time() - time_start))
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(type='VERT')
                    bpy.ops.mesh.select_all(action='SELECT')

                    if len(src_obj.vertex_groups) == 0:
                        src_obj.vertex_groups.new(name=src_obj.name)
                        bpy.ops.object.vertex_group_assign()
                    # elif src_obj.vertex_groups[0] != src_obj.name:
                    #     src_obj.vertex_groups.new(name=src_obj.name)
                    #     bpy.ops.object.vertex_group_assign()

                    bpy.ops.mesh.hide(unselected=False)
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    scene.objects.active = modifier.object
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(type='VERT')
                    bpy.ops.mesh.reveal()
                    bpy.ops.object.mode_set(mode='OBJECT')
                    modifier.object.draw_type = 'BOUNDS'
                    scene.objects.active = src_obj
                    bpy.ops.object.select_all(action='DESELECT')
                    print("Prepare Other: %.4f sec" % (time.time() - time_start))
                    print(bool_object.name)
                    return [True, modifier.name, bool_object.name]
                else:
                    # если нет то применяем модификаторы
                    try:
                        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
                    except:
                        pass
                        # bpy.ops.object.modifier_remove(modifier=modifier.name)
    return [False]


def get_guide(scene, simplify, subdivide, relax, custom, sharp, sharp_angle, interpolation, vertex_remove, repeat,
              src_obj, name):
    print("get_guide Start: %.4f sec" % (time.time() - time_start))
    if not custom:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.select_mode(type='FACE')
        src_obj.vertex_groups.new(name=name + "_")
        bpy.ops.object.vertex_group_assign()

        bpy.ops.mesh.region_to_loop()
        if sharp:
            bpy.ops.mesh.hide(unselected=True)
            if relax != '0':
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.edges_select_sharp(sharpness=sharp_angle)
                bpy.ops.mesh.select_all(action='INVERT')
                bpy.ops.mesh.looptools_relax(iterations=relax, interpolation=interpolation)
                bpy.ops.mesh.select_all(action='SELECT')

        try:
            bpy.ops.mesh.duplicate_move()
            bpy.ops.mesh.separate(type='SELECTED')
            print("Separate")
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.hide(unselected=False)
            bpy.ops.object.mode_set(mode='OBJECT')
            guide = bpy.context.selected_objects[0]
            guide.name = "BOOLEAN_BEVEL_GUIDE"
            print("get_guide отделили Guide: %.4f sec" % (time.time() - time_start))
        except:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.ed.undo()
            return False
    else:
        guide = bpy.data.objects['BOOLEAN_BEVEL_GUIDE_CUSTOM']
        guide.name = "BOOLEAN_BEVEL_GUIDE"

    scene.objects.active = guide
    src_obj.select = False
    guide.select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.remove_doubles()
    print("get_guide Зашли в режим редактирования: %.4f sec" % (time.time() - time_start))
    # return {'FINISHED'}
    if simplify > 0:
        bpy.ops.mesh.dissolve_limited(angle_limit=simplify)
        print("get_guide упростили: %.4f sec" % (time.time() - time_start))
    if subdivide > 0:
        bpy.ops.mesh.subdivide(number_cuts=subdivide)
        print("get_guide подразделили: %.4f sec" % (time.time() - time_start))
    for i in range(repeat):
        if relax != '0' and not sharp:
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.looptools_relax(iterations=relax, interpolation=interpolation)
            # bpy.ops.mesh.select_mode(type='FACE')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.looptools_relax(iterations=relax, interpolation=interpolation)
            print("get_guide сглаживание: %.4f sec" % (time.time() - time_start))
    bpy.ops.mesh.remove_doubles(threshold=vertex_remove, use_unselected=False)

    bpy.ops.object.mode_set(mode='OBJECT')
    return guide


def create_curve(value_radius, sides, fix_curve, curve_tilt, twist_mode, scene, smooth):
    bpy.ops.object.convert(target='CURVE', keep_original=True)

    curve_cut = bpy.context.object
    curve_cut.name = "BOOLEAN_BEVEL_CURVE"
    curve_cut.data.fill_mode = 'FULL'
    curve_cut.data.bevel_depth = value_radius
    curve_cut.data.bevel_resolution = sides
    if fix_curve:
        curve_cut.data.resolution_u = 1
        curve_cut.data.twist_mode = twist_mode
        curve_cut.data.twist_smooth = smooth
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.spline_type_set(type='BEZIER')
        bpy.ops.curve.handle_type_set(type='FREE_ALIGN')
        bpy.ops.curve.normals_make_consistent()
        bpy.ops.transform.tilt(value=curve_tilt)
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.transform.tilt(value=curve_tilt)
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_circle_add(vertices=sides, radius=value_radius)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.convert(target='CURVE', keep_original=False)
    circle = scene.objects.active
    circle.name = "BOOLEAN_BEVEL_CURVE_PROFILE"
    scene.objects.active = curve_cut
    curve_cut.data.bevel_object = circle

    return curve_cut


def do_boolean(scene, src_obj, union_path):
    curve_cut = bpy.data.objects['BOOLEAN_BEVEL_CURVE']
    scene.objects.active = curve_cut
    curve_cut.select = True
    try:
        bpy.ops.object.convert(target='MESH', keep_original=False)
    except:
        pass
    # curve_cut = bpy.data.objects['BOOLEAN_BEVEL_CURVE']
    curve_cut.draw_type = 'BOUNDS'
    boolean_modifier = src_obj.modifiers.new(name="BooleanBevel", type='BOOLEAN')
    boolean_modifier.show_viewport = False
    boolean_modifier.object = curve_cut
    boolean_modifier.operation = union_path
    # boolean_modifier.double_threshold = 0.0
    bpy.ops.object.select_all(action='DESELECT')
    scene.objects.active = src_obj
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=boolean_modifier.name)

    bpy.ops.object.select_all(action='DESELECT')
    scene.objects.active = src_obj


def create_bevel(scene, src_obj, fillet_profile, fillet_segments, triangulate, smooth_bevel, method, smooth_bevel_value,
                 smooth_bevel_step, name, do_bevel, custom_normals, bevel_width):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.region_to_loop()
    bpy.ops.mesh.select_all(action='INVERT')
    # bpy.ops.object.vertex_group_add()
    src_obj.vertex_groups.new(name="Bevel_" + name + "_")
    bpy.ops.object.vertex_group_assign()
    bevel_group = src_obj.vertex_groups.active.name

    bpy.ops.object.mode_set(mode='OBJECT')

    guide = bpy.data.objects['BOOLEAN_BEVEL_GUIDE']

    print("Start shrinkwrap: %.4f sec" % (time.time() - time_start))
    shrinkwrap_modifier = src_obj.modifiers.new(name="shrinkwrap", type='SHRINKWRAP')
    shrinkwrap_modifier.wrap_method = 'NEAREST_VERTEX'
    shrinkwrap_modifier.vertex_group = bevel_group
    shrinkwrap_modifier.target = guide
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=shrinkwrap_modifier.name)
    print("End shrinkwrap: %.4f sec" % (time.time() - time_start))
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.remove_doubles()
    print("Remove Double: %.4f sec" % (time.time() - time_start))

    print("Split NGon: %.4f sec" % (time.time() - time_start))

    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.select_more(use_face_step=False)
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.edge_collapse()
    bpy.ops.mesh.dissolve_verts(use_face_split=True, use_boundary_tear=False)

    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type='EDGE')
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.select_more(use_face_step=True)
    bpy.ops.mesh.hide(unselected=True)
    bpy.ops.mesh.select_face_by_sides(number=3, type='EQUAL', extend=False)
    bpy.ops.object.vertex_group_deselect()
    bpy.ops.mesh.edge_collapse()

    bpy.ops.mesh.reveal()

    if triangulate:
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.select_more(use_face_step=True)
        bpy.ops.mesh.select_more(use_face_step=True)
        bpy.ops.mesh.hide(unselected=True)
        bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER', extend=False)
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method=method)
        bpy.ops.mesh.reveal()

    bpy.ops.mesh.select_all(action='DESELECT')
    if smooth_bevel:
        bpy.ops.object.vertex_group_select()
        src_obj.vertex_groups.new(name="Smooth_" + name + "_")
        bpy.ops.object.vertex_group_assign()
        for i in range(smooth_bevel_step):
            bpy.context.tool_settings.vertex_group_weight = bpy.context.tool_settings.vertex_group_weight - 1 / smooth_bevel_step
            bpy.ops.mesh.select_more(use_face_step=True)
            bpy.ops.object.vertex_group_deselect()
            bpy.ops.object.vertex_group_assign()
        smooth_group = src_obj.vertex_groups.active.name

    bpy.context.tool_settings.vertex_group_weight = 1.0

    if do_bevel:
        print("Start Bevel Modifier: %.4f sec" % (time.time() - time_start))
        fillet_modifier = src_obj.modifiers.new(name="Boolean Bevel", type='BEVEL')
        fillet_modifier.show_viewport = False
        fillet_modifier.offset_type = 'PERCENT'
        fillet_modifier.profile = fillet_profile
        fillet_modifier.segments = fillet_segments
        fillet_modifier.use_clamp_overlap = False
        # fillet_modifier.use_clamp_overlap = True
        fillet_modifier.limit_method = 'VGROUP'
        fillet_modifier.vertex_group = bevel_group
        fillet_modifier.width = bevel_width
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')
    # bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    if smooth_bevel:
        smooth_modifier = src_obj.modifiers.new(name="Boolean Bevel Smooth", type='SMOOTH')
        smooth_modifier.iterations = smooth_bevel_value
        smooth_modifier.vertex_group = smooth_group

    for modifier in src_obj.modifiers:
        modifier.show_viewport = True

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')

    if len(src_obj.vertex_groups) <= 4:
        if src_obj.vertex_groups[0].name == src_obj.name:
            bpy.ops.mesh.select_all(action='DESELECT')
            src_obj.vertex_groups.active_index = 0
            bpy.ops.object.vertex_group_select()
            bpy.ops.mesh.select_more(use_face_step=True)
            bpy.ops.object.vertex_group_assign()

    bpy.ops.mesh.select_all(action='DESELECT')
    src_obj.vertex_groups.active_index = len(src_obj.vertex_groups) - 2 - smooth_bevel
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.select_more(use_face_step=True)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    if custom_normals:

        data_transfer_modifier = src_obj.modifiers.new(name="Boolean Bevel Custom Normals", type="DATA_TRANSFER")
        if bpy.data.objects.find(src_obj.name + "_Normals") != -1:
            data_transfer_modifier.object = bpy.data.objects[src_obj.name + "_Normals"]
        else:
            data_transfer_modifier.object = bpy.data.objects[src_obj.vertex_groups[0].name + "_Normals"]
        data_transfer_modifier.use_vert_data = True
        data_transfer_modifier.vert_mapping = "NEAREST"
        data_transfer_modifier.use_loop_data = True
        data_transfer_modifier.loop_mapping = "POLYINTERP_NEAREST"
        if bpy.data.objects.find(src_obj.name + "_Normals") != -1:
            data_transfer_modifier.vertex_group = src_obj.name
        else:
            data_transfer_modifier.vertex_group = src_obj.vertex_groups[0].name
            print("hello world")
        data_transfer_modifier.data_types_verts = {'VGROUP_WEIGHTS'}
        data_transfer_modifier.data_types_loops = {"CUSTOM_NORMAL"}

        if bpy.data.objects.find(src_obj.name + "_Normals_bool") != -1:
            data_transfer_modifier = src_obj.modifiers.new(name="Boolean Bevel Custom Normals", type="DATA_TRANSFER")
            data_transfer_modifier.object = bpy.data.objects[src_obj.name + "_Normals_bool"]
            data_transfer_modifier.use_vert_data = True
            data_transfer_modifier.vert_mapping = "NEAREST"
            data_transfer_modifier.use_loop_data = True
            data_transfer_modifier.loop_mapping = "POLYINTERP_NEAREST"
            data_transfer_modifier.vertex_group = src_obj.vertex_groups[
                len(src_obj.vertex_groups) - 2 - smooth_bevel].name
            data_transfer_modifier.data_types_verts = {'VGROUP_WEIGHTS'}
            data_transfer_modifier.data_types_loops = {"CUSTOM_NORMAL"}
        else:
            data_transfer_modifier.vertex_group = bevel_group
            data_transfer_modifier.invert_vertex_group = True
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = 3.14159
    src_obj.select = True
    bpy.ops.object.shade_smooth()
    bpy.ops.object.select_all(action='DESELECT')
    print("End Bevel Modifier: %.4f sec" % (time.time() - time_start))


def set_material(smooth_bevel, src_obj, name):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')

    if len(src_obj.vertex_groups) <= 4:
        if src_obj.vertex_groups[0].name == src_obj.name:
            bpy.ops.mesh.select_all(action='DESELECT')
            src_obj.vertex_groups.active_index = 0
            bpy.ops.object.vertex_group_select()
            mat = bpy.data.materials.new(src_obj.name + "_")
            mat.diffuse_color = (random.random(), random.random(), random.random())
            src_obj.data.materials.append(mat)
            src_obj.active_material_index = len(src_obj.data.materials) - 1
            bpy.ops.object.material_slot_assign()

    bpy.ops.mesh.select_all(action='DESELECT')
    src_obj.vertex_groups.active_index = len(src_obj.vertex_groups) - 2 - smooth_bevel
    bpy.ops.object.vertex_group_select()

    mat = bpy.data.materials.new(name + "_")
    mat.diffuse_color = (random.random(), random.random(), random.random())
    src_obj.data.materials.append(mat)
    src_obj.active_material_index = len(src_obj.data.materials) - 1
    bpy.ops.object.material_slot_assign()

    bpy.ops.mesh.select_all(action='DESELECT')
    src_obj.vertex_groups.active_index = len(src_obj.vertex_groups) - 1 - smooth_bevel
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.select_more(use_face_step=True)

    mat = bpy.data.materials.new("Bevel_" + name + "_")
    mat.diffuse_color = (random.random(), random.random(), random.random())
    src_obj.data.materials.append(mat)
    src_obj.active_material_index = len(src_obj.data.materials) - 1
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')


def clear_objects(scene, src_obj):
    bpy.ops.object.select_all(action='DESELECT')
    for i in ['BOOLEAN_BEVEL_CURVE', 'BOOLEAN_BEVEL_GUIDE', 'BOOLEAN_BEVEL_CURVE_PROFILE']:
        index = bpy.data.objects.find(i)
        if index != -1:
            bpy.data.objects[i].select = True
            bpy.ops.object.delete(use_global=False)
    src_obj.select = True
    scene.objects.active = src_obj


def register():
#    bpy.utils.register_class(BooleanBevelPanel)
    bpy.utils.register_class(ObjectBooleanBevel)
    bpy.utils.register_class(ObjectBooleanCustomBevel)
    bpy.utils.register_class(ObjectBooleanBevelCustomEdge)
    bpy.utils.register_class(BooleanBevelPreferences)
    bpy.utils.register_class(ObjectBooleanBevelApplyModifiers)
    bpy.utils.register_class(ObjectBooleanBevelRemoveModifiers)
    bpy.utils.register_class(ObjectBooleanBevelRemoveObjects)
    bpy.utils.register_class(ObjectBooleanBevelSymmetrize)
    bpy.utils.register_class(ObjectBooleanBevelPipe)
    bpy.utils.register_class(ObjectBooleanBevelRemovePipes)
    # bpy.utils.register_class(ObjectBooleanBevelBridge)


def unregister():
#    bpy.utils.unregister_class(BooleanBevelPanel)
    bpy.utils.unregister_class(ObjectBooleanBevel)
    bpy.utils.unregister_class(ObjectBooleanCustomBevel)
    bpy.utils.unregister_class(ObjectBooleanBevelCustomEdge)
    bpy.utils.unregister_class(BooleanBevelPreferences)
    bpy.utils.unregister_class(ObjectBooleanBevelApplyModifiers)
    bpy.utils.unregister_class(ObjectBooleanBevelRemoveModifiers)
    bpy.utils.unregister_class(ObjectBooleanBevelRemoveObjects)
    bpy.utils.unregister_class(ObjectBooleanBevelSymmetrize)
    bpy.utils.unregister_class(ObjectBooleanBevelPipe)
    bpy.utils.unregister_class(ObjectBooleanBevelRemovePipes)
    # bpy.utils.unregister_class(ObjectBooleanBevelBridge)


if __name__ == "__main__":
    register()
