# Add-on information
bl_info = {
    "name": "Reboot",
    "author": "himham, dogway, mkbreuer, meta-androcto, saidenka",
    "version": (1, 1),
    "blender": (3, 3, 0),
    "location": "File Menu",
    "description": "Reboot Blender without save",
    "warning": "",
    "wiki_url": "https://github.com/himham-jak/re-Boot-with-Keymap",
    "tracker_url": "",
    "category": "System",
}


import bpy
import os, sys
import subprocess


class BLENDER_OT_Restart(bpy.types.Operator):
    bl_idname = "wm.restart_blender"
    bl_label = "Reboot Blender"
    bl_description = "Blender Restart"
    bl_options = {"REGISTER"}

    def execute(self, context):
        py = os.path.join(os.path.dirname(__file__), "after_restart.py")
        filepath = bpy.data.filepath
        if filepath != "":
            subprocess.Popen([sys.argv[0], filepath, "-P", py])
        else:
            subprocess.Popen([sys.argv[0], "-P", py])
        bpy.ops.wm.quit_blender()

        return {"FINISHED"}


def menu_draw(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("wm.restart_blender", text="Restart", icon="PLUGIN")
    layout.separator()
    prefs = bpy.context.preferences
    view = prefs.view
    layout.prop(view, "use_save_prompt")


addon_keymaps = []


def register():
    bpy.utils.register_class(BLENDER_OT_Restart)
    bpy.types.TOPBAR_MT_file.append(menu_draw)

    # Add the hotkey
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            BLENDER_OT_Restart.bl_idname, type="F8", value="PRESS", ctrl=True
        )
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(BLENDER_OT_Restart)
    bpy.types.TOPBAR_MT_file.remove(menu_draw)


if __name__ == "__main__":
    register()
