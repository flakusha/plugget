import plugget.actions._copy_files
import plugget.actions._maya_utils


class _Action(plugget.actions._copy_files.CopyFiles):
    target_dir = plugget.actions._maya_utils.get_plugin_path()


install = _Action.install
uninstall = _Action.uninstall
__all__ = ["install", "uninstall"]
