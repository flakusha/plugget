import os
import sys
import subprocess


import os
import sys
import subprocess
import logging
from pathlib import Path
import importlib
import unreal


# def project_plugins_dir():
#     project_path = unreal.Paths.project_plugins_dir()
#     project_path = unreal.Paths.convert_relative_path_to_full(project_path)
#     return Path(project_path)

def project_site_dir():
    content_path = unreal.Paths.project_content_dir()  # '../../../Users/USER/MyProject/Content/'
    content_path = unreal.Paths.convert_relative_path_to_full(content_path)  # 'C:/Users/USER/MyProject/Content/'
    return Path(content_path) / r"Python\Lib\site-packages"  # 'C:/Users/USER/MyProject/Content/Python/Lib/site-packages'


# todo unify, copied from krita_pip


project_site_dir = project_site_dir()


python_version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)


def get_requirements(package: "plugget.data.Package", **kwargs) -> "list[Path]":
    # if requirements.txt exists in self.repo_paths, install requirements
    requirements_paths = []
    if (package.clone_dir / "requirements.txt").exists():
        requirements_paths.append(package.clone_dir / "requirements.txt")
    if package.repo_paths:
        for p in package.repo_paths:
            if p.endswith("requirements.txt"):
                requirements_paths.append(package.clone_dir / p)
    return requirements_paths


# def get_python():
#     python_exe = os.environ.get("PLUGGET_KRITA_PYTHON")  # set to same version as python in krita!
#
#     # Verify that the provided Python executable matches the current Python version
#     if not os.path.isfile(python_exe):
#         raise ValueError("Python executable not found at {}".format(python_exe))
#     if subprocess.check_output(
#             [python_exe, "-c", "import sys; print(sys.version_info[:2])"]).decode().strip() != python_version:
#         raise ValueError(
#             "Python executable {} does not match current Python version {}".format(python_exe, python_version))
#     return python_exe


def install(package: "plugget.data.Package", **kwargs):
    print("check for requirements")

    for p in get_requirements(package):
        if p.exists():
            print("requirements.txt found, installing requirements")
            subprocess.run(["pip", "install", "-r", package.clone_dir / p, '-t', project_site_dir])
        else:
            logging.warning(f"expected requirements.txt not found: '{p}'")
    importlib.invalidate_caches()


# def install(package: "plugget.data.Package", **kwargs):
#     # Use the Python executable to run the pip install command
#     args = [get_python(), "-m", "pip", "install", name, "-t", path]
#     subprocess.check_call(args)
#
#
# def uninstall(package: "plugget.data.Package", dependencies=False, **kwargs):
#     # Use the Python executable to run the pip uninstall command
#     if not dependencies:
#         return
#     args = [get_python(), "-m", "pip", "uninstall", name, "-t", path]
#     subprocess.check_call(args)


def uninstall(package: "plugget.data.Package", dependencies=False, **kwargs):
    # this method runs on uninstall, then the manifest is removed from installed packages
    # ideally uninstall removes files from a folder,

    if not dependencies:
        return

    for p in get_requirements(package):
        if p.exists():
            print("requirements.txt found, uninstalling requirements")
            print("package.clone_dir / p", package.clone_dir / p)
            subprocess.run(["pip", "uninstall", "-r", package.clone_dir / p, "-y"])
        else:
            logging.warning(f"expected requirements.txt not found: '{p}'")
    importlib.invalidate_caches()
