bl_info = {
    'name': 'Lighting Toolkit for Blender',
    'author': 'Jorge Sanchez Salcedo',
    'version': (1, 2, 2),
    'blender': (2, 79, 7),
    'category': 'Lighting'
}

import bpy

from bpy.props import (IntProperty,
                       BoolProperty,
                       EnumProperty,
                       StringProperty,
                       CollectionProperty,
                       PointerProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)

class GetLightType(PropertyGroup):
    bl_idname = 'lamp.getLightType'
    bl_label = 'Get Light Type'
    bl_option = {"REGISTER", "UNDO"}
    
    lightTypes = [('SUN', 'Sun', ''),    
                ('AREA', 'Area', ''),    
                ('POINT', 'Point', ''),    
                ('SPOT', 'Spot', '')]

    lamp_combo_box = EnumProperty(name = '', items = lightTypes, default='SUN') 

class CREATE_OT_CreateLight(Operator):
    bl_idname = 'lamp.create_light'
    bl_label = 'Create Light'
    new_name = bpy.props.StringProperty(name="Name:")
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        newLight = bpy.ops.object.lamp_add(type=bpy.context.scene.getLightTypeCombo.lamp_combo_box, location=(0,0,0), rotation=(0,0,0))
        for i in newLight:
            bpy.context.object.name = self.new_name
            bpy.context.object.data.name = self.new_name
        
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
class CREATE_OT_CreateLightIntoObjects(Operator):
    bl_idname = 'lamp.create_light_objects'
    bl_label = 'Create Light Into Objects'
    new_name = bpy.props.StringProperty(name="Name:")
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected = bpy.context.selected_objects

        for i in selected:
            objName = i.name
            newLampName = self.new_name + '_' + objName
            loc = i.location
            newLight = bpy.ops.object.lamp_add(type=bpy.context.scene.getLightTypeCombo.lamp_combo_box, location=loc)
            
            for i in newLight:
                bpy.context.object.name = newLampName
                bpy.context.object.data.name = newLampName
                
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class CREATE_OT_CreateLightFromView(Operator):
    bl_idname = 'lamp.create_light_view'
    bl_label = 'Create Light From View'
    new_name = bpy.props.StringProperty(name="Name:")
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                rv3d = area.spaces[0].region_3d
                if rv3d is not None:            
                    loc = area.spaces[0].region_3d.view_location
                    rot = (area.spaces[0].region_3d.view_rotation).to_euler()
                    dis = area.spaces[0].region_3d.view_distance 
                    newLight = bpy.ops.object.lamp_add(type=bpy.context.scene.getLightTypeCombo.lamp_combo_box, location=loc, rotation=rot)
                    bpy.ops.view3d.object_as_camera()
                    bpy.context.space_data.lock_camera = True
                    
                    for i in newLight:
                        bpy.context.object.name = self.new_name
                        bpy.context.object.data.name = self.new_name
                    
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class CREATE_PT_LightingToolkit(Panel):
    bl_idname = "panel.createToolkit"
    bl_label = "Create"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Lighting Toolkit"

    def draw(self, context):
        self.layout.prop(context.scene.getLightTypeCombo, "lamp_combo_box")
        self.layout.separator()
        self.layout.operator("lamp.create_light", text="New lamp")
        self.layout.operator("lamp.create_light_objects", text="New lamp into objects")
        self.layout.operator("lamp.create_light_view", text="New lamp from view")
        
class EDIT_OT_DeleteLight(Operator):
    bl_idname = 'lamp.delete_light'
    bl_label = 'Delete Light'
    bl_options = {"REGISTER", "UNDO"}
        
    def execute(self, context):
        bpy.ops.object.delete()
            
        return{'FINISHED'}
    
class EDIT_OT_DuplicateLight(Operator):
    bl_idname = 'lamp.duplicate_light'
    bl_label = 'Duplicate Light'
    bl_options = {"REGISTER", "UNDO"}
        
    def execute(self, context):
        bpy.ops.object.duplicate()
                        
        return{'FINISHED'}
        
class EDIT_PT_LightingToolkit(Panel):
    bl_idname = "panel.editToolkit"
    bl_label = "Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Lighting Toolkit"
    
    def draw(self, context):
        self.layout.operator("lamp.delete_light", text="Delete")
        self.layout.operator("lamp.duplicate_light", text="Duplicate")

class VIEW_OT_ViewFromSelected(Operator):
    bl_idname = 'lamp.view_from_selected'
    bl_label = 'View from selected'
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        bpy.ops.view3d.object_as_camera()
        bpy.context.space_data.lock_camera = True
        
        return {"FINISHED"}
    
class VIEW_OT_IsolateLamps(Operator):
    bl_idname = 'lamp.isolate_lamps'
    bl_label = 'Isolate Lamps'
    
    def getSceneLamps(self):
        sceneLamps = []        
        for obj in bpy.data.objects:
            if obj.type == 'LAMP':
                sceneLamps.append(obj)
            else:
                pass
        
        sceneLampsOn = []        
        for lamp in sceneLamps:
            if lamp.hide == False:
                sceneLampsOn.append(lamp)
            else:
                pass
            
        return sceneLamps
    
    def modal(self, context, event):
        sceneLamps = self.getSceneLamps()
        wm = context.window_manager
        
        if wm.isolate_toggle_button == True:
            for lamp in sceneLamps:
                selected = bpy.context.selected_objects
                if lamp not in selected:
                    lamp.hide = True
                else:
                    lamp.hide = False
                    
        elif wm.isolate_toggle_button == False:
            context.window_manager.event_timer_remove(self._timer)
            for lamp in sceneLamps:
                lamp.hide = False
            
            return {'FINISHED'}
        
        return {'PASS_THROUGH'}
    
    def invoke(self, context, event):
        self._timer = context.window_manager.event_timer_add(0.01, context.window)
        context.window_manager.modal_handler_add(self)
        return{'RUNNING_MODAL'}    
        
class VIEW_PT_LightingToolkit(Panel):
    bl_idname = "panel.viewToolkit"
    bl_label = "View"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Lighting Toolkit"
    
    def draw(self, context):
        wm = context.window_manager
        label = 'Isolated' if wm.isolate_toggle_button else 'Isolate'
        self.layout.operator("lamp.view_from_selected", text="View from selected")
        self.layout.prop(wm, "isolate_toggle_button", text=label, toggle=True)

def update_function(self, context):
    if self.isolate_toggle_button:
        bpy.ops.lamp.isolate_lamps('INVOKE_DEFAULT')
    return
        
def register():
    bpy.utils.register_module(__name__)
    
    bpy.types.WindowManager.isolate_toggle_button = BoolProperty(default=False, update=update_function)
    bpy.types.Scene.getLightTypeCombo = PointerProperty(type=GetLightType)

def unregister():
    bpy.utils.unregister_module(__name__)
    
    del bpy.types.WindowManager.isolate_toggle_button
    del bpy.types.Scene.getLightTypeCombo

if __name__ == "__main__":
    register()