# ##### BEGIN GPL LICENSE BLOCK #####
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

bl_info = {
    "name": "Modifier Shortcuts Panel",
    "author": "Scthe",
    "blender": (2, 72, 0),
    "location": "Properties -> Modifiers",
    "description": "New panel in modifiers tab for quicker access to favorite modifiers",
    "warning": "",
    "wiki_url": "",
    "category": "Object"}

import bpy
from bpy.utils import register_module, unregister_module
from bpy.props import IntProperty

class Modifier_shortcuts_panel(bpy.types.Operator):
    bl_label = "Modifier Shortcuts Panel"
    bl_idname = "object.modifier_shortcuts_panel"
    bl_description = "New panel in modifiers tab for quicker access to favorite modifiers"
    bl_options = {"REGISTER", "UNDO"}
    
    # mode - which button was pressed
    MODE_SHOW_RENDER = -1
    MODE_SHOW_VIEWPORT = -2
    MODE_SHOW_EDITMODE = -3
    MODE_SHOW_CAGE = -4
    MODE_APPLY = -5
    MODE_MANAGE = -6
    mode = IntProperty(name="mode", min = MODE_MANAGE, max = 20, default = 0)
    property_name = "common_used_modifiers"
    
    @classmethod
    def poll(cls, context):
        #print('poll')
        return True

    def invoke(self, context, event):
        print('invoke')
        print(bpy.context.scene.get(self.property_name, None))
        if not bpy.context.scene.get(self.property_name, None):
            bpy.context.scene[self.property_name] = []    
        return self.execute(context)

    def execute(self, context):
        print('execute')
        obj = bpy.context.object
        modifiers = list(bpy.context.scene.get(self.property_name, None))
        
        if not obj.modifiers: # TODO really ?
            # nothing to do
            return {"FINISHED"}
        
        # TODO use function toogle_all with setattr / getattr
        if self.mode == self.MODE_SHOW_RENDER:
            # show render
            opt = not obj.modifiers[0].show_render
            for mod in obj.modifiers:
                mod.show_render = opt
        
        elif self.mode == self.MODE_SHOW_VIEWPORT:
            # show viewport
            opt = not obj.modifiers[0].show_viewport
            for mod in obj.modifiers:
                mod.show_viewport = opt
        
        elif self.mode == self.MODE_SHOW_EDITMODE:
            # show edit mode
            opt = not obj.modifiers[0].show_in_editmode
            for mod in obj.modifiers:
                mod.show_in_editmode = opt
        
        elif self.mode == self.MODE_SHOW_CAGE:
            # show cage
            opt = not obj.modifiers[0].show_on_cage
            for mod in obj.modifiers:
                mod.show_on_cage = opt
        
        elif self.mode == self.MODE_APPLY:
            # apply
            while obj.modifiers:
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier = obj.modifiers[0].name)
        
        elif self.mode == self.MODE_MANAGE:
            # manage
            name = obj.modifiers[0].type
            if name in modifiers:
                modifiers.remove(name) # if already exist on the list -> remove from it !
            else:
                modifiers.append(name)
            bpy.context.scene[self.property_name] = modifiers
                    
        elif self.mode < len( modifiers):
            # add selected modifier
            bpy.ops.object.modifier_add( type = modifiers[self.mode])
        
        return {"FINISHED"}

def menu_draw (self, context):
    self.layout.operator_context = "INVOKE_DEFAULT"
    layout = self.layout
    row = layout.row(True)
    
    # TODO write some lambda to encapsulate
    # create_button = lambda _icon:     row.operator(Modifier_shortcuts_panel.bl_idname, icon =_icon
    row.operator(Modifier_shortcuts_panel.bl_idname, icon ='RESTRICT_RENDER_OFF').mode = Modifier_shortcuts_panel.MODE_SHOW_RENDER
    row.operator(Modifier_shortcuts_panel.bl_idname, icon ='RESTRICT_VIEW_OFF').mode = Modifier_shortcuts_panel.MODE_SHOW_VIEWPORT
    row.operator(Modifier_shortcuts_panel.bl_idname, icon ='EDITMODE_HLT').mode = Modifier_shortcuts_panel.MODE_SHOW_EDITMODE
    row.operator(Modifier_shortcuts_panel.bl_idname, icon ='OUTLINER_DATA_MESH').mode = Modifier_shortcuts_panel.MODE_SHOW_CAGE
    row.separator()
    row.operator(Modifier_shortcuts_panel.bl_idname, icon ='FILE_TICK', text=" Apply all").mode = Modifier_shortcuts_panel.MODE_APPLY
    row.operator(Modifier_shortcuts_panel.bl_idname, icon ='NLA', text=" Manage").mode = Modifier_shortcuts_panel.MODE_MANAGE
    row = layout.row(True)
    

    modifiers = bpy.context.scene.get( Modifier_shortcuts_panel.property_name, None)
    if modifiers:
        # TODO enumerate
        for i in range( len(modifiers)):
            if i & 1  == 0 and i != 0: # start new row
                row = layout.row(True)
            row.operator(Modifier_shortcuts_panel.bl_idname, icon ='SPACE2', text = modifiers[i] ).mode = i

    # TODO wtf ?
    row = layout.row(True)
    row = layout.row(True)
 
def register():
    unregister()
    register_module(__name__)
    bpy.types.DATA_PT_modifiers.prepend(menu_draw) # prepend / append !
    
def unregister():
    unregister_module(__name__)
    bpy.types.DATA_PT_modifiers.remove(menu_draw) 

if __name__ == "__main__":
    register()
