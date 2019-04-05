bl_info = {
    'name': 'Lighting Toolkit for Blender',
    'author': 'Jorge Sanchez Salcedo',
    'version': (1, 2, 5),
    'blender': (2, 79, 7),
    'category': 'Lighting'
}

import bpy
import os

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
        new_group = 'Light_Group'
        
        if new_group in bpy.data.groups:
            new_light = bpy.ops.object.lamp_add(type=bpy.context.scene.getLightTypeCombo.lamp_combo_box, location=(0,0,0), rotation=(0,0,0))
            bpy.ops.object.group_link(group=new_group)
        else:
            bpy.ops.group.create(name=new_group)
            new_light = bpy.ops.object.lamp_add(type=bpy.context.scene.getLightTypeCombo.lamp_combo_box, location=(0,0,0), rotation=(0,0,0))
            bpy.ops.object.group_link(group=new_group)
        
        for i in new_light:
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
        new_group = 'Light_Group'
        selected = bpy.context.selected_objects
        
        if new_group in bpy.data.groups:
            
            for i in selected:
                obj_name = i.name
                new_lamp_name = self.new_name + '_' + obj_name
                loc = i.location
                new_light = bpy.ops.object.lamp_add(type=bpy.context.scene.getLightTypeCombo.lamp_combo_box, location=loc)
                bpy.ops.object.group_link(group=new_group)
                
                for i in new_light:
                    bpy.context.object.name = new_lamp_name
                    bpy.context.object.data.name = new_lamp_name
                
        else:
            bpy.ops.group.create(name=new_group)
            
            for i in selected:
                obj_name = i.name
                new_lamp_name = self.new_name + '_' + obj_name
                loc = i.location
                new_light = bpy.ops.object.lamp_add(type=bpy.context.scene.getLightTypeCombo.lamp_combo_box, location=loc)
                bpy.ops.object.group_link(group=new_group)
                
                for i in new_light:
                    bpy.context.object.name = new_lamp_name
                    bpy.context.object.data.name = new_lamp_name
                
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
        new_group = 'Light_Group'
        
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                rv3d = area.spaces[0].region_3d
                if rv3d is not None:            
                    loc = area.spaces[0].region_3d.view_location
                    rot = (area.spaces[0].region_3d.view_rotation).to_euler()
                    dis = area.spaces[0].region_3d.view_distance 

                    if new_group in bpy.data.groups:
                        new_light = bpy.ops.object.lamp_add(type=bpy.context.scene.getLightTypeCombo.lamp_combo_box, location=loc, rotation=rot)
                        bpy.ops.object.group_link(group=new_group)                        
                        
                    else:
                        bpy.ops.group.create(name=new_group)
                        new_light = bpy.ops.object.lamp_add(type=bpy.context.scene.getLightTypeCombo.lamp_combo_box, location=loc, rotation=rot)
                        bpy.ops.object.group_link(group=new_group) 
                        
                    for i in new_light:
                        bpy.context.object.name = self.new_name
                        bpy.context.object.data.name = self.new_name
                    
                    bpy.ops.view3d.object_as_camera()
                    bpy.context.space_data.lock_camera = True
                    
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

class CYCLES_RENDER_PT_sampling(Panel):
    bl_idname = "panels.cycles_sampling"
    bl_label = "Sampling"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Lighting Toolkit"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        cscene = scene.cycles

        row = layout.row(align=True)
        row.menu("CYCLES_MT_sampling_presets", text=bpy.types.CYCLES_MT_sampling_presets.bl_label)

        row = layout.row()
        sub = row.row()
        sub.prop(cscene, "progressive", text="")
        row.prop(cscene, "use_square_samples")

        split = layout.split()

        col = split.column()
        sub = col.column(align=True)
        sub.label("Settings:")

        seed_sub = sub.row(align=True)
        seed_sub.prop(cscene, "seed")
        seed_sub.prop(cscene, "use_animated_seed", text="", icon="TIME")

        sub.prop(cscene, "sample_clamp_direct")
        sub.prop(cscene, "sample_clamp_indirect")
        sub.prop(cscene, "light_sampling_threshold")

        if cscene.progressive == 'PATH' or use_branched_path(context) is False:
            col = split.column()
            sub = col.column(align=True)
            sub.label(text="Samples:")
            sub.prop(cscene, "samples", text="Render")
            sub.prop(cscene, "preview_samples", text="Preview")
        else:
            sub.label(text="AA Samples:")
            sub.prop(cscene, "aa_samples", text="Render")
            sub.prop(cscene, "preview_aa_samples", text="Preview")

            col = split.column()
            sub = col.column(align=True)
            sub.label(text="Samples:")
            sub.prop(cscene, "diffuse_samples", text="Diffuse")
            sub.prop(cscene, "glossy_samples", text="Glossy")
            sub.prop(cscene, "transmission_samples", text="Transmission")
            sub.prop(cscene, "ao_samples", text="AO")

            subsub = sub.row(align=True)
            subsub.active = use_sample_all_lights(context)
            subsub.prop(cscene, "mesh_light_samples", text="Mesh Light")

            sub.prop(cscene, "subsurface_samples", text="Subsurface")
            sub.prop(cscene, "volume_samples", text="Volume")

            col = layout.column(align=True)
            col.prop(cscene, "sample_all_lights_direct")
            col.prop(cscene, "sample_all_lights_indirect")

        layout.row().prop(cscene, "sampling_pattern", text="Pattern")

        for rl in scene.render.layers:
            if rl.samples > 0:
                layout.separator()
                layout.row().prop(cscene, "use_layer_samples")
                break

        draw_samples_info(layout, context)


class CYCLES_RENDER_PT_light_paths(Panel):
    bl_idname = "panels.cycles_lightpaths"
    bl_label = "Light paths"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Lighting Toolkit"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        cscene = scene.cycles

        row = layout.row(align=True)
        row.menu("CYCLES_MT_integrator_presets", text=bpy.types.CYCLES_MT_integrator_presets.bl_label)

        split = layout.split()

        col = split.column()

        sub = col.column(align=True)
        sub.label("Transparency:")
        sub.prop(cscene, "transparent_max_bounces", text="Max")

        col.separator()

        col.prop(cscene, "caustics_reflective")
        col.prop(cscene, "caustics_refractive")
        col.prop(cscene, "blur_glossy")

        col = split.column()

        sub = col.column(align=True)
        sub.label(text="Bounces:")
        sub.prop(cscene, "max_bounces", text="Max")

        sub = col.column(align=True)
        sub.prop(cscene, "diffuse_bounces", text="Diffuse")
        sub.prop(cscene, "glossy_bounces", text="Glossy")
        sub.prop(cscene, "transmission_bounces", text="Transmission")
        sub.prop(cscene, "volume_bounces", text="Volume")

class RENDER_OT_RenderSettings(Operator):
    bl_idname = "render.render_settings"
    bl_label = "Render settings"
    
    def execute(self, context):
        fr_start = str(bpy.context.scene.frame_start)
        fr_end = str(bpy.context.scene.frame_end)
        fr_step = str(bpy.context.scene.frame_step)
        getPath = bpy.app.binary_path
        blenderPath = getPath.split('blender.exe')[0]
        blenderPath = blenderPath.replace('\\','/')

        blenderLine = 'cd ' + blenderPath

        getPath = bpy.data.filepath
        filePath = getPath.replace('\\','/')

        getPath = bpy.path.abspath('//')
        renderFilePath = getPath.replace('\\','/')
        renderFileName = os.path.join(renderFilePath, 'batch_render.bat')
        renderPath = os.path.join(renderFilePath, 'render_test/')

        commandLine = 'blender -b "' + filePath + '" -o "' + renderPath + '" -F MULTILAYER -t=0'

        renderfile = open(renderFileName, 'w')

        renderfile.write(blenderLine)
        renderfile.write('\n')
        renderfile.write('blender -b "' + filePath + '" -o "' + renderPath + '" -F MULTILAYER ')
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

        row = col.row()
        row.prop(rd, "use_border", text="Border")
        sub = row.row()
        sub.active = rd.use_border
        sub.prop(rd, "use_crop_to_border", text="Crop")

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Frame Range:")
        row = col.row(align=True)
        row.prop(scene, "frame_start", text="")
        row.prop(scene, "frame_end", text="")
        col.prop(scene, "frame_step", text="Step")
        
class RENDER_PT_RenderSettings(Panel):
    bl_idname = "panel.renderSettings"
    bl_label = "Render"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Lighting Toolkit"
    
    def draw(self, context):
        self.layout.operator("render.render_settings", text="Batch Render")     

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