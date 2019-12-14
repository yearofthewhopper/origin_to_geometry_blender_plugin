# ***** BEGIN GPL LICENSE BLOCK *****
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
# ***** END GPL LICENSE BLOCK *****

# <pep8-80 compliant>

bl_info = {
    "name": "Orgin_to_geometry",
    "description": "Set object origin to geometry in edit-mode, by a selection",
    "author": "Noland Chaliha",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D Viewport > Edit Mode > Ctrl + Shift + P",
    "category": "Object"
    }

import bpy

def main(context):
    bcs = bpy.context.scene
    cursorLoc_X = bcs.cursor.location[0]
    cursorLoc_Y = bcs.cursor.location[1]
    cursorLoc_Z = bcs.cursor.location[2]
    bpy.ops.view3d.snap_cursor_to_selected()
    bpy.ops.object.mode_set()
    bpy.ops.object.origin_set(
        type = 'ORIGIN_GEOMETRY',
        center = 'MEDIAN'
        )
    bpy.ops.object.mode_set(mode = 'EDIT')
    bcs.cursor.location[0] = cursorLoc_X
    bcs.cursor.location[1] = cursorLoc_Y
    bcs.cursor.location[2] = cursorLoc_Z

class OBJ_OT_set_origin(bpy.types.Operator):
    '''Tooltip'''
    bl_idname = "obj.ori_to_there"
    bl_label = "Set Origin to Selected"

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and (
                context.object.type == 'MESH'
                or
                context.object.type == 'CURVE'
                or
                context.object.type == 'ARMATURE'
                )
            )

    def execute(self, context):
        main(context)
        return {'FINISHED'}


addon_keymaps = []

def register():
    bpy.utils.register_class(OBJ_OT_set_origin)
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(
        name = '3D View',
        space_type = 'VIEW_3D',
        modal = False,
        )
    kmi = km.keymap_items.new(
        'obj.ori_to_there','P','PRESS',
        ctrl = True,
        shift = True
        )
    addon_keymaps.append((km,kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(OBJ_OT_set_origin)

if __name__ == "__main__":
    register()
