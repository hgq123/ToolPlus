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

"""
bl_info = {
    "name": "Bevel/Taper Curve",
    "author": "Cmomoney",
    "version": (1, 1),
    "blender": (2, 69, 0),
    "location": "View3D > Object > Bevel/Taper",
    "description": "Adds bevel and/or taper curve to active curve",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Bevel_-Taper_Curve",
    "tracker_url": "https://projects.blender.org/tracker/index.php?func=detail&aid=37377&group_id=153&atid=467",
    "category": "Curve"}
""" 
 
import bpy
from bpy.types import Operator
from bpy.props import *
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

def add_taper(self, context):

    scale_ends1 = self.scale_ends1
    scale_ends2 = self.scale_ends2
    scale_mid = self.scale_mid
    verts = [(-2.0, 1.0 * scale_ends1, 0.0, 1.0), (-1.0, 0.75 * scale_mid, 0.0, 1.0), (0.0, 1.5 * scale_mid, 0.0, 1.0), (1.0, 0.75 * scale_mid, 0.0, 1.0), (2.0, 1.0 * scale_ends2, 0.0, 1.0)]
    make_path(self, context, verts)

def add_type5(self, context):
    
    scale_x = self.scale_x
    scale_y = self.scale_y
    verts = [[0.0 * scale_x, 0.049549 * scale_y, 0.0, 0.031603 * scale_x, 0.047013 * scale_y, 0.0, 0.05 * scale_x, 0.0 * scale_y, 0.0, 0.031603 * scale_x, -0.047013 * scale_y, 0.0, 0.0 * scale_x, -0.049549 * scale_y, 0.0, -0.031603 * scale_x, -0.047013 * scale_y, 0.0, -0.05 * scale_x, -0.0 * scale_y, 0.0, -0.031603 * scale_x, 0.047013 * scale_y, 0.0]]
    lhandles = [[(-0.008804 * scale_x, 0.049549 * scale_y, 0.0), (0.021304 * scale_x, 0.02119 * scale_y, 0.0), (0.05 * scale_x, 0.051228 * scale_y, 0.0), (0.036552 * scale_x, -0.059423 * scale_y, 0.0), (0.008804 * scale_x, -0.049549 * scale_y, 0.0), (-0.021304 * scale_x, -0.02119 * scale_y, 0.0), (-0.05 * scale_x, -0.051228 * scale_y, 0.0), (-0.036552 * scale_x, 0.059423 * scale_y, 0.0)]]
    rhandles = [[(0.008803 * scale_x, 0.049549 * scale_y, 0.0), (0.036552 * scale_x, 0.059423 * scale_y, 0.0), (0.05 * scale_x, -0.051228 * scale_y, 0.0), (0.021304 * scale_x, -0.02119 * scale_y, 0.0), (-0.008803 * scale_x, -0.049549 * scale_y, 0.0), (-0.036552 * scale_x, -0.059423 * scale_y, 0.0), (-0.05 * scale_x, 0.051228 * scale_y, 0.0), (-0.021304 * scale_x, 0.02119 * scale_y, 0.0)]]
    make_curve(self, context, verts, lhandles, rhandles)
    
def add_type4(self, context):
    
    scale_x = self.scale_x
    scale_y = self.scale_y
    verts = [[-0.0 * scale_x, 0.017183 * scale_y, 0.0, 0.05 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, -0.017183 * scale_y, 0.0, -0.05 * scale_x, -0.0 * scale_y, 0.0]]
    lhandles = [[(-0.017607 * scale_x, 0.017183 * scale_y, 0.0), (0.05 * scale_x, 0.102456 * scale_y, 0.0), (0.017607 * scale_x, -0.017183 * scale_y, 0.0), (-0.05 * scale_x, -0.102456 * scale_y, 0.0)]]
    rhandles = [[(0.017607 * scale_x, 0.017183 * scale_y, 0.0), (0.05 * scale_x, -0.102456 * scale_y, 0.0), (-0.017607 * scale_x, -0.017183 * scale_y, 0.0), (-0.05 * scale_x, 0.102456 * scale_y, 0.0)]]
    make_curve(self, context, verts, lhandles, rhandles)
    
def add_type3(self, context):
    
    scale_x = self.scale_x
    scale_y = self.scale_y
    verts = [[-0.017183 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, 0.05 * scale_y, 0.0, 0.017183 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, -0.05 * scale_y, 0.0]]
    lhandles = [[(-0.017183 * scale_x, -0.017607 * scale_y, 0.0), (-0.102456 * scale_x, 0.05 * scale_y, 0.0), (0.017183 * scale_x, 0.017607 * scale_y, 0.0), (0.102456 * scale_x, -0.05 * scale_y, 0.0)]]
    rhandles = [[(-0.017183 * scale_x, 0.017607 * scale_y, 0.0), (0.102456 * scale_x, 0.05 * scale_y, 0.0), (0.017183 * scale_x, -0.017607 * scale_y, 0.0), (-0.102456 * scale_x, -0.05 * scale_y, 0.0)]]
    make_curve(self, context, verts, lhandles, rhandles)
    
def add_type2(self, context):
    
    scale_x = self.scale_x
    scale_y = self.scale_y
    verts = [[-0.05 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, 0.05 * scale_y, 0.0, 0.05 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, -0.05 * scale_y, 0.0]]
    lhandles = [[(-0.05 * scale_x, -0.047606 * scale_y, 0.0), (-0.047606 * scale_x, 0.05 * scale_y, 0.0), (0.05 * scale_x, 0.047607 * scale_y, 0.0), (0.047606 * scale_x, -0.05 * scale_y, 0.0)]]
    rhandles = [[(-0.05 * scale_x, 0.047607 * scale_y, 0.0), (0.047607 * scale_x, 0.05 * scale_y, 0.0), (0.05 * scale_x, -0.047607 * scale_y, 0.0), (-0.047607 * scale_x, -0.05 * scale_y, 0.0)]]
    make_curve(self, context, verts, lhandles, rhandles)
    
def add_type1(self, context):
    
    scale_x = self.scale_x
    scale_y = self.scale_y
    verts = [[-0.05 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, 0.05 * scale_y, 0.0, 0.05 * scale_x, 0.0 * scale_y, 0.0, 0.0 * scale_x, -0.05 * scale_y, 0.0]]
    lhandles = [[(-0.05 * scale_x, -0.027606 * scale_y, 0.0), (-0.027606 * scale_x, 0.05 * scale_y, 0.0), (0.05 * scale_x, 0.027606 * scale_y, 0.0), (0.027606 * scale_x, -0.05 * scale_y, 0.0)]]
    rhandles = [[(-0.05 * scale_x, 0.027607 * scale_y, 0.0), (0.027607 * scale_x, 0.05 * scale_y, 0.0), (0.05 * scale_x, -0.027607 * scale_y, 0.0), (-0.027607 * scale_x, -0.05 * scale_y, 0.0)]]
    make_curve(self, context, verts, lhandles, rhandles)

def make_path(self, context, verts):
    
    target = bpy.context.scene.objects.active
    bpy.ops.curve.primitive_nurbs_path_add(view_align=False, enter_editmode=False, location=(0, 0, 0))
    target.data.taper_object = bpy.context.scene.objects.active
    taper = bpy.context.scene.objects.active
    taper.name = target.name + '_Taper'
    bpy.context.scene.objects.active = target
    points = taper.data.splines[0].points
    for i in range(len(verts)):
        points[i].co = verts[i]

def make_curve(self, context, verts, lh, rh):

    scale_x = self.scale_x
    scale_y = self.scale_y
    type = self.type
    target = bpy.context.scene.objects.active
    curve_data = bpy.data.curves.new(name=target.name +'_Bevel', type='CURVE')
    curve_data.dimensions = '3D'
    for p in range(len(verts)):
        c = 0
        spline = curve_data.splines.new(type='BEZIER')
        spline.use_cyclic_u = True
        spline.bezier_points.add( len(verts[p])/3-1 )
        spline.bezier_points.foreach_set('co', verts[p])
        for bp in spline.bezier_points:
            bp.handle_left_type = 'ALIGNED'
            bp.handle_right_type = 'ALIGNED'
            bp.handle_left.xyz = lh[p][c]
            bp.handle_right.xyz = rh[p][c]
            c += 1
    object_data_add(context, curve_data, operator=self)
    target.data.bevel_object = bpy.context.scene.objects.active
    bpy.context.scene.objects.active = target

class add_tapercurve(Operator, AddObjectHelper):
    """Add taper curve to active curve"""
    bl_idname = "curve.tapercurve"
    bl_label = "Add Curve as Taper"
    bl_options = {'REGISTER', 'UNDO'}


    scale_ends1 = FloatProperty(name="End Width Left", description="Adjust left end taper", default=0.0, min=0.0)
    scale_ends2 = FloatProperty(name="End Width Right", description="Adjust right end taper", default=0.0, min=0.0)
    scale_mid = FloatProperty(name="Center Width", description="Adjust taper at center", default=1.0, min=0.0)
    link1 = BoolProperty(name='link ends', default=True)
    link2 = BoolProperty(name='link ends/center', default=False)
    if link2:
        diff = FloatProperty(name='Difference', default=1, description='Difference between ends and center while linked')

    def execute(self, context):
        if self.link1:
            self.scale_ends2 = self.scale_ends1
        if self.link2:
            self.scale_ends2 = self.scale_ends1 = self.scale_mid-self.diff
        add_taper(self, context)
        return {'FINISHED'}
    
class add_bevelcurve(Operator, AddObjectHelper):
    """Add bevel curve to active curve"""
    bl_idname = "curve.bevelcurve"
    bl_label = "Add Curve as Bevel"
    bl_options = {'REGISTER', 'UNDO'}

    type = IntProperty(name='Type', description='Type of bevel curve', default=1, min=1, max=5)
    scale_x = FloatProperty(name="scale x", description="scale on x axis", default=1.0)
    scale_y = FloatProperty(name="scale y", description="scale on y axis", default=1.0)
    link = BoolProperty(name='link xy', default=True)

    def execute(self, context):
        if self.link:
            self.scale_y = self.scale_x
        if self.type == 1:
            add_type1(self, context)
        if self.type == 2:
            add_type2(self, context)
        if self.type == 3:
            add_type3(self, context)
        if self.type == 4:
            add_type4(self, context)
        if self.type == 5:
            add_type5(self, context)
            
        return {'FINISHED'}

class Bevel_Taper_Curve_Menu(bpy.types.Menu):
    bl_label = "Bevel & Taper"
    bl_idname = "OBJECT_MT_bevel_taper_curve_menu"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("curve.bevelcurve")
        layout.operator("curve.tapercurve")


def menu_funcs(self, context):
    if bpy.context.scene.objects.active.type == "CURVE":
        
        self.layout.separator()
        self.layout.menu("OBJECT_MT_bevel_taper_curve_menu")



def register():
    bpy.utils.register_class(add_tapercurve)
    bpy.utils.register_class(add_bevelcurve)
    bpy.utils.register_class(Bevel_Taper_Curve_Menu)
    #bpy.types.INFO_MT_curve_add.append(menu_funcs)

def unregister():
    bpy.utils.unregister_class(add_tapercurve)
    bpy.utils.unregister_class(add_bevelcurve)
    bpy.utils.unregister_class(Bevel_Taper_Curve_Menu)
    #bpy.types.INFO_MT_curve_add.remove(menu_funcs)


if __name__ == "__main__":
    register()