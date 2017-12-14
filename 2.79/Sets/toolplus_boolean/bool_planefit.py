# ##### BEGIN GPL LICENSE BLOCK #####
#
#  PLaneFit, (c) 2017 Michel Anders (varkenvarken)
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
#    "name": "PlaneFit",
#    "author": "Michel Anders (varkenvarken)",
#    "version": (0, 0, 201712101438),
#    "blender": (2, 79, 0),
#    "location": "Edit mode 3d-view, Add-->PlaneFit",
#    "description": "Add a plane that best fits a collection of selected vertices",
#    "warning": "",
#    "wiki_url": "",
#    "category": "Mesh",
#}

# LOAD MODUL #
import bpy
import numpy as np

def planeFit(points):
    ctr = points.mean(axis=0)
    x = points - ctr
    M = np.cov(x.T)
    eigenvalues,eigenvectors = np.linalg.eig(M)
    normal = eigenvectors[:,eigenvalues.argmin()]
    return ctr,normal

def orthopoints(normal):
	m = np.argmax(normal)
	x = np.ones(3,dtype=np.float32)
	x[m] = 0
	x /= np.linalg.norm(x)
	x = np.cross(normal, x)
	y = np.cross(normal, x)
	return x,y

class VIEW3D_TP_PlaneFit(bpy.types.Operator):
	bl_idname = 'tp_ops.planefit'
	bl_label = 'PlaneFit'
	bl_options = {'REGISTER', 'UNDO'}

	size = bpy.props.FloatProperty(name="Size", description="Size of the plane", default=10, min=1, soft_max=100)

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH' and context.active_object.type == 'MESH')

	def execute(self, context):
		bpy.ops.object.editmode_toggle()
		me = context.active_object.data
		count = len(me.vertices)
		if count > 0:  # degenerate mesh, but better safe than sorry
			shape = (count, 3)
			verts = np.empty(count*3, dtype=np.float32)
			selected = np.empty(count, dtype=np.bool)
			me.vertices.foreach_get('co', verts)
			me.vertices.foreach_get('select', selected)
			verts.shape = shape
			ctr, normal = planeFit(verts[selected])  # actually we should check if there are at least 3 points selected
			dx, dy = orthopoints(normal)
			# can't use mesh.from_pydata here because that won't let us ADD to a mesh
			me.vertices.add(4)
			me.vertices[count  ].co = ctr+dx*self.size
			me.vertices[count+1].co = ctr+dy*self.size
			me.vertices[count+2].co = ctr-dx*self.size
			me.vertices[count+3].co = ctr-dy*self.size
			lcount = len(me.loops)
			me.loops.add(4)
			pcount = len(me.polygons)
			me.polygons.add(1)
			me.polygons[pcount].loop_total = 4
			me.polygons[pcount].loop_start = lcount
			me.polygons[pcount].vertices = [count,count+1,count+2,count+3]
			me.update(calc_edges=True)

		bpy.ops.object.editmode_toggle()
		return {'FINISHED'}



# REGISTRY #        
def register():    
    bpy.utils.register_module(__name__)

def unregister():   
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()