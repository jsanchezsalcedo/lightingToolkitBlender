bl_info = {
    'name': 'Lighting Toolkit for Blender',
    'author': 'Jorge Sanchez Salcedo <jorgesanchez.da@gmail.com>',
    'version': (2, 1, 0),
    'blender': (4, 3, 0),
    'category': 'Lighting'
}

import bpy

from bpy.props import (EnumProperty,
                       StringProperty,
                       PointerProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup)

# Utility Functions
def ensure_collection(name):
    """Ensure a collection exists, create it if not."""
    if name not in bpy.data.collections:
        bpy.data.collections.new(name)
    return bpy.data.collections[name]

# Property Group
class GetLightType(PropertyGroup):
    bl_idname = 'lt.getLightType'
    bl_label = 'Get Light Type'

    lamp_combo_box : EnumProperty(
        name='Lights',
        items=[
            ('SUN', 'Sun', ''),
            ('AREA', 'Area', ''),
            ('POINT', 'Point', ''),
            ('SPOT', 'Spot', '')
        ])
    
# Panel
class VIEW3D_PT_LightingToolkit(Panel):
    bl_label = 'Lighting Toolkit'
    bl_idname = 'VIEW3D_PT_lightingToolkit'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lighting Toolkit'

    def draw(self, context):
        layout = self.layout     
        wm = context.window_manager

        row = layout.row()
        layout.label(text='Scenes:')

        row = layout.row()
        row.operator("ob.undo", text="Undo")
        row.operator("ob.redo", text="Redo")

        row = layout.row()
        layout.separator()

        row = layout.row()
        row.prop(context.scene.lamp_combo_box, 'lamp_combo_box')

        row = layout.row()
        row.operator("lt.create_light", text="Create Light")
        
        row = layout.row()
        row.operator("lt.create_light_objects", text="Create light to objects")
        
        row = layout.row()
        row.operator("lt.create_light_view", text="Create light from view")
        
        row = layout.row()
        row.operator("lt.view_from_selected", text="View from selected")

        row = layout.row()
        row.separator()

        row = layout.row()
        row.label(text='Objects:')

        row = layout.row()
        row.operator("ob.rename_object", text="Rename")

        row = layout.row()
        row.operator("ob.center_origin_object", text="Center origin to object")

        row = layout.row()
        row.operator("ob.add_subdivisions", text="Subdivide")
        
        row = layout.row()
        row.operator("ob.duplicate", text="Duplicate")
        
        row = layout.row()
        row.operator("ob.delete", text="Delete")

        row = layout.row()
        row.operator("ob.hide_object", text="Isolate")
        row.operator("ob.unhide_object", text="Show all")

# Operator  
class EDIT_OT_Undo(Operator):
    bl_idname = 'ob.undo'
    bl_label = 'Undo'
        
    def execute(self, context):
        bpy.ops.ed.undo()
                        
        return{'FINISHED'}
    
class EDIT_OT_Redo(Operator):
    bl_idname = 'ob.redo'
    bl_label = 'Redo'
        
    def execute(self, context):
        bpy.ops.ed.redo()
                        
        return{'FINISHED'}
    
class CREATE_OT_CreateLight(Operator):
    bl_idname = 'lt.create_light'
    bl_label = 'Create Light'
    light_name: StringProperty(name="Name:")

    def execute(self, context):
        light_type = bpy.context.scene.lamp_combo_box.lamp_combo_box
        new_light = bpy.ops.object.light_add(type=light_type, location=(0, 0, 0), rotation=(0,0,0))
        
        for i in new_light:
            bpy.context.object.name = self.light_name
            bpy.context.object.data.name = self.light_name + "Shape"

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class CREATE_OT_CreateLightIntoObjects(Operator):
    bl_idname = 'lt.create_light_objects'
    bl_label = 'Create Light Into Objects'

    def execute(self, context):
        selected = bpy.context.selected_objects
        light_type = bpy.context.scene.lamp_combo_box.lamp_combo_box
        light_name = light_type

        for i in selected:
            obj_name = i.name
            obj_loc = i.location
            new_light_name = obj_name + '_' + light_name.casefold() + 'Light'

            new_light = bpy.ops.object.light_add(type=light_type, location=obj_loc)
        
            for i in new_light:
                bpy.context.object.name = new_light_name
                bpy.context.object.data.name = new_light_name + 'Shape'

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class CREATE_OT_CreateLightFromView(Operator):
    bl_idname = 'lt.create_light_view'
    bl_label = 'Create Light From View'
    light_name: StringProperty(name="Name:")

    def execute(self, context):
        light_type = bpy.context.scene.lamp_combo_box.lamp_combo_box

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                rv3d = area.spaces[0].region_3d
                if rv3d is not None:            
                    loc = area.spaces[0].region_3d.view_location
                    rot = (area.spaces[0].region_3d.view_rotation).to_euler()
                    dis = area.spaces[0].region_3d.view_distance
                    
                    new_light = bpy.ops.object.light_add(type=light_type, location=loc, rotation=rot)

                    for i in new_light:
                        bpy.context.object.name = self.light_name
                        bpy.context.object.data.name = self.light_name + "Shape"

                    bpy.ops.view3d.object_as_camera()
                    bpy.context.space_data.lock_camera = True
                    
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        
class VIEW_OT_ViewFromSelected(Operator):
    bl_idname = 'lt.view_from_selected'
    bl_label = 'View from selected'
    
    def execute(self, context):
        bpy.ops.view3d.object_as_camera()
        bpy.context.space_data.lock_camera = False
        
        return {'FINISHED'}
    
class EDIT_OT_Rename(Operator):
    bl_idname = 'ob.rename_object'
    bl_label = 'Rename'
    new_name: StringProperty(name="Name:")
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        #self.report({'INFO'}, self.new_name)

        for i in selected:
            obj_name = i.name
            object = bpy.data.objects[obj_name]

            bpy.context.view_layer.objects.active = object
            obj = bpy.context.object
            obj.name = self.new_name + ".000"
            obj.data.name = obj.name + "Shape"

        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)    

class EDIT_OT_CenterOrigin(Operator):
    bl_idname = 'ob.center_origin_object'
    bl_label = 'Hide'
    
    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

        return{'FINISHED'}

class EDIT_OT_add_subdivions(Operator):
    bl_idname = "ob.add_subdivisions"
    bl_label = "Subdivide"

    def execute(self, context):
        selected = bpy.context.selected_objects
        
        for i in selected:
            obj_name = i.name
            object = bpy.ops.object
            objects = bpy.data.objects

            bpy.context.view_layer.objects.active = objects[obj_name]

            object.modifier_add(type='SUBSURF')
            object.modifier_apply(modifier="Subdivision")
            object.shade_smooth()

        return{'FINISHED'}
    
class EDIT_OT_Duplicate(Operator):
    bl_idname = 'ob.duplicate'
    bl_label = 'Duplicate'
        
    def execute(self, context):
        bpy.ops.object.duplicate()
                        
        return{'FINISHED'}
        
class EDIT_OT_Delete(Operator):
    bl_idname = 'ob.delete'
    bl_label = 'Delete'
        
    def execute(self, context):
        bpy.ops.object.delete()
            
        return{'FINISHED'}
    
class EDIT_OT_Hide(Operator):
    bl_idname = 'ob.hide_object'
    bl_label = 'Hide'
    
    def execute(self, context):
        bpy.ops.object.hide_view_set(unselected=True)

        return{'FINISHED'}

class EDIT_OT_Unhide(Operator):
    bl_idname = 'ob.unhide_object'
    bl_label = 'Hide'
    
    def execute(self, context):
        bpy.ops.object.hide_view_clear()

        return{'FINISHED'}

# Registration
classes = (GetLightType,
           VIEW3D_PT_LightingToolkit,
           EDIT_OT_Undo,
           EDIT_OT_Redo,
           CREATE_OT_CreateLight,
           CREATE_OT_CreateLightIntoObjects,
           CREATE_OT_CreateLightFromView,
           VIEW_OT_ViewFromSelected,
           EDIT_OT_Rename,
           EDIT_OT_CenterOrigin,
           EDIT_OT_add_subdivions,
           EDIT_OT_Delete,
           EDIT_OT_Duplicate,
           EDIT_OT_Hide,
           EDIT_OT_Unhide)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.lamp_combo_box = bpy.props.PointerProperty(type=GetLightType)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.lamp_combo_box

if __name__ == '__main__':
    register()
