bl_info = {
    'name': 'Lighting Toolkit for Blender',
    'author': 'Jorge Sanchez Salcedo <jorgesanchez.da@gmail.com>',
    'version': (2, 0, 0),
    'blender': (4, 3, 2),
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
    bl_idname = 'lt.getLightType'
    bl_label = 'Get Light Type'
    
    lamp_combo_box : EnumProperty(name='Lights', items=[
        ('SUN', 'Sun', ''),    
        ('AREA', 'Area', ''),    
        ('POINT', 'Point', ''),    
        ('SPOT', 'Spot', '')
        ])

class VIEW3D_PT_lightingToolkit(Panel):
    bl_label = 'Lighting Toolkit'
    bl_idname = 'VIEW3D_PT_lightingToolkit'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lighting Toolkit'
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.label(text='Scenes:')

        row = layout.row()
        row.operator('sc.sync_scenes', text='Sync scene')
        
        row = layout.row()
        row.operator('sc.optimize_file', text='Optimize scene')

        row = layout.row()
        row.separator()

        row = layout.row()
        row.prop(context.scene.lamp_combo_box, 'lamp_combo_box')
        
        row = layout.row()
        row.operator("lt.create_light", text="Create light")
        
        row = layout.row()
        row.operator("lt.create_light_objects", text="Create light to objects")
        
        row = layout.row()
        row.operator("lt.create_light_view", text="Create light from view")
        
        row = layout.row()
        row.operator("lamp.view_from_selected", text="View from selected")

        row = layout.row()
        row.separator()

        row = layout.row()
        row.label(text='Objects:')
        
        row = layout.row()
        row.operator("lt.rename_object", text="Rename")
        
        row = layout.row()
        row.operator("lamp.delete_light", text="Delete")
        
        row = layout.row()
        row.operator("lamp.duplicate_light", text="Duplicate")

class SYNC_OT_Sync_Scenes(Operator):
    bl_idname = 'sc.sync_scenes'
    bl_label = 'Sync lighting scene'
    
    def execute(self, context):
        lightObs = bpy.data.scenes['Lighting'].objects
        sceneObs = bpy.data.scenes['Scene'].objects
        
        for i in sceneObs:
            if i.name not in lightObs:
                bpy.data.objects[i.name].select=True
                bpy.ops.object.make_links_scene(scene='Lighting')
        
        bpy.ops.object.select_all()
        
        return{'FINISHED'}                    
		
class EDIT_OT_OptimizeBlendFile(Operator):
    bl_idname = 'sc.optimize_file'
    bl_label = 'Optimize scene file'
        
    def execute(self, context):
        for camera in bpy.data.cameras:
            if not camera.users:
                bpy.data.cameras.remove(camera)
            else:
                pass
        
        for lamp in bpy.data.lamps:
            if not lamp.users:
                bpy.data.lamps.remove(lamp)
            else:
                pass
        
        for material in bpy.data.materials:
            if not material.users:
                bpy.data.materials.remove(material)
            else:
                pass
        
        for image in bpy.data.images:
            if not image.users:
                bpy.data.images.remove(image)
            else:
                pass
        
        for texture in bpy.data.textures:
            if not texture.users:
                bpy.data.textures.remove(texture)
            else:
                pass
        
        for object in bpy.data.objects:
            if not object.users:
                bpy.data.objects.remove(object)
            else:
                pass
        
        for node in bpy.data.node_groups:
            if not node.users:
                bpy.data.node_groups.remove(node)
            else:
                pass	
            
        for group in bpy.data.groups:
            if not group.users:
                bpy.data.groups.remove(node)
            else:
                pass			
            
        return{'FINISHED'}

class CREATE_OT_CreateLight(Operator):
    bl_idname = 'lt.create_light'
    bl_label = 'Create Light'
    new_name: StringProperty(name="Name:")

    def execute(self, context):
        new_collection = 'Light_Group'
        lightType = bpy.context.scene.lamp_combo_box.lamp_combo_box
        
        if new_collection in bpy.data.collections:
            new_light = bpy.ops.object.light_add(type=lightType, location=(0,0,0), rotation=(0,0,0))
            bpy.ops.object.collection_link(collection=new_collection)
        else:
            bpy.ops.collection.create(name=new_collection)
            new_light = bpy.ops.object.light_add(type=lightType, location=(0,0,0), rotation=(0,0,0))
            bpy.ops.object.collection_link(collection=new_collection)
        
        for i in new_light:
            bpy.context.object.name = self.new_name
            bpy.context.object.data.name = self.new_name + 'Shape'
        
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
class CREATE_OT_CreateLightIntoObjects(Operator):
    bl_idname = 'lt.create_light_objects'
    bl_label = 'Create Light Into Objects'
    new_name: StringProperty(name="Name:")

    def execute(self, context):
        new_collection = 'Lighting'
        selected = bpy.context.selected_objects 
        lightType = bpy.context.scene.lamp_combo_box.lamp_combo_box
        
        if new_collection in bpy.data.collections:
            
            for i in selected:
                obj_name = i.name
                new_light_name = self.new_name + '_' + obj_name
                loc = i.location
                new_light = bpy.ops.object.light_add(type=lightType, location=loc)
                bpy.ops.object.collection_link(collection=new_collection)
                
                for i in new_light:
                    bpy.context.object.name = new_light_name
                    bpy.context.object.data.name = new_light_name + 'Shape'
                
        else:
            bpy.ops.collection.create(name=new_collection)
            
            for i in selected:
                obj_name = i.name
                new_light_name = self.new_name + '_' + obj_name
                loc = i.location
                new_light = bpy.ops.object.light_add(type=lightType, location=loc)
                bpy.ops.object.collection_link(collection=new_collection)
                
                for i in new_light:
                    bpy.context.object.name = new_light_name
                    bpy.context.object.data.name = new_light_name + 'Shape'
                
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class CREATE_OT_CreateLightFromView(Operator):
    bl_idname = 'lt.create_light_view'
    bl_label = 'Create Light From View'
    new_name = bpy.props.StringProperty(name="Name:")

    def execute(self, context):
        new_collection = 'Lighting'
        lightType = bpy.context.scene.lamp_combo_box.lamp_combo_box
        
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                rv3d = area.spaces[0].region_3d
                if rv3d is not None:            
                    loc = area.spaces[0].region_3d.view_location
                    rot = (area.spaces[0].region_3d.view_rotation).to_euler()
                    dis = area.spaces[0].region_3d.view_distance 

                    if new_collection in bpy.data.collections:
                        new_light = bpy.ops.object.light_add(type=lightType, location=loc, rotation=rot)
                        bpy.ops.object.collection_link(collection=new_collection)                      
                        
                    else:
                        bpy.ops.collection.create(name=new_collection)
                        new_light = bpy.ops.object.light_add(type=lightType, location=loc, rotation=rot)
                        bpy.ops.object.collection_link(collection=new_collection)
                        
                    for i in new_light:
                        bpy.context.object.name = self.new_name
                        bpy.context.object.data.name = self.new_name + 'Shape'
                    
                    bpy.ops.view3d.object_as_camera()
                    bpy.context.space_data.lock_camera = True
                    
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
class EDIT_OT_Rename(Operator):
    bl_idname = 'lt.rename_object'
    bl_label = 'Rename'
    new_name: StringProperty(name="Name:")
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        message = "{:s}".format(self.new_name)
        self.report({'INFO'}, message)

        for obj in selected:
            obj = obj.name
            object = bpy.data.objects[obj]
            bpy.context.view_layer.objects.active = object
            bpy.context.object.name = message
            bpy.context.object.data.name = message + 'Shape'

        return{'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
        
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
        
class VIEW_OT_ViewFromSelected(Operator):
    bl_idname = 'lamp.view_from_selected'
    bl_label = 'View from selected'
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        bpy.ops.view3d.object_as_camera()
        bpy.context.space_data.lock_camera = False
        
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
        
class RENDER_OT_RenderSettings(Operator):
    bl_idname = "render.render_settings"
    bl_label = "Render settings"
    
    def execute(self, context):
        fr_start = str(bpy.context.scene.frame_start)
        fr_end = str(bpy.context.scene.frame_end)
        fr_step = str(bpy.context.scene.frame_step)
        fl_format = str(bpy.context.scene.render.image_settings.file_format)
        getPath = bpy.app.binary_path
        blenderPath = getPath.split('blender.exe')[0]
        blenderPath = blenderPath.replace('\\','/')

        blenderLine = 'cd ' + blenderPath

        getPath = bpy.data.filepath
        filePath = getPath.replace('\\','/')

        getPath = bpy.path.abspath('//')
        renderFilePath = getPath.replace('\\','/')
        renderFileName = os.path.join(renderFilePath, 'batch_render.bat')
        renderPath = os.path.join(renderFilePath, 'render/')

        commandLine = 'blender -b "' + filePath + '" -o "' + renderPath + '" -F ' + fl_format + ' -t 6'

        renderfile = open(renderFileName, 'w')

        renderfile.write(blenderLine)
        renderfile.write('\n')
        renderfile.write('blender -b "' + filePath + '" -o "' + renderPath + '" -F ' + fl_format + ' -t 6 ')
        
        if fr_start == fr_end:
            renderfile.write('-f ' + fr_start)
        else:
            if fr_step == '1':
                renderfile.write('-s ' + fr_start + ' -e ' + fr_end + ' -a')
            else:
                renderfile.write('-s ' + fr_start + ' -e ' + fr_end + ' -a -j ' + fr_step)

        renderfile.close()
        
        bpy.ops.wm.save_mainfile()
        
        os.startfile(renderFilePath)
                        
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 350)

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render
        image_settings = rd.image_settings

        row = layout.row(align=True)
        row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
        row.menu("CYCLES_MT_sampling_presets", text=bpy.types.CYCLES_MT_sampling_presets.bl_label)

        split = layout.split()

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Resolution:")
        row = col.row(align=True)
        row.prop(rd, "resolution_x", text="")
        row.prop(rd, "resolution_y", text="")
        col.prop(rd, "resolution_percentage", text="")

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Frame Range:")
        row = col.row(align=True)
        row.prop(scene, "frame_start", text="")
        row.prop(scene, "frame_end", text="")
        col.prop(scene, "frame_step", text="Step")
        
        layout.separator()
        layout.template_image_settings(image_settings, color_management=False)
        if rd.use_multiview:
            layout.template_image_views(image_settings)
        layout.separator()
        
classes = (GetLightType,
           VIEW3D_PT_lightingToolkit,
           SYNC_OT_Sync_Scenes,
           EDIT_OT_OptimizeBlendFile,
           CREATE_OT_CreateLight,
           CREATE_OT_CreateLightIntoObjects,
           CREATE_OT_CreateLightFromView,
           EDIT_OT_Rename,
           EDIT_OT_DeleteLight,
           EDIT_OT_DuplicateLight,
           VIEW_OT_ViewFromSelected,
           VIEW_OT_IsolateLamps,
           RENDER_OT_RenderSettings,
)
        
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
