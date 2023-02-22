import bpy
import addon_utils
from pathlib import Path
import shutil


# TODO uninstal/remove vs deactivate/disable


def enabled_plugins():
    """return list of installed plugins"""
    # TODO get list of installed plugins
    return bpy.context.preferences.addons.keys()


def installed_plugins():
    return [mod.bl_info.get("name") for mod in addon_utils.modules()]


def disable_plugin(name):
    bpy.ops.preferences.addon_disable(module=name)

def enable_plugin(name):
    bpy.ops.preferences.addon_enable(module=name)

def install_plugin(plugin_path: Path, force=False, enable=True):
    # If the “overwrite” parameter is True, the add-on will be reinstalled, even if it has not been previously removed.

    # manifest is named io_xray
    # but subdir is io_scene_xray
    # resulting in clashes. we cant just rename the subdir, might break code inside.
    # so we need to track the "name"


    local_script_dir = bpy.utils.script_path_user()
    local_addons_dir = Path(local_script_dir) / "addons"
    new_plugin_path = local_addons_dir / plugin_path.name
    shutil.move(str(plugin_path), str(new_plugin_path.parent))  # copy plugin_path to local_addons_dir

    # get user path from bpy



    # bpy.ops.preferences.addon_install(filepath=path, overwrite=force)
    # if enable:
    #     enable_plugin(name)

def uninstall_plugin(name):
    bpy.ops.preferences.addon_remove(module=name)

