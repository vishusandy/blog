import bpy
from bpy.app.handlers import persistent
import sys
import os

"""
Put this in `<blender_path>/<version>/scripts/startup`

It will automatically add the directory of the current .blend file into the system path.
This allows python files in the same directory to be loaded by just `import <script>`

"""

last_dir = None


def unload_last():
    if last_dir:
        sys.path.remove(last_dir)


def add_dir():
    global last_dir
    if hasattr(bpy.data, 'filepath'):
        dir = os.path.dirname(bpy.data.filepath)
        last_dir = dir

        if dir and not dir in sys.path:
            sys.path.append(dir)
            print(f'changed directory to: {dir}')


@persistent
def append_new_dir(a, b):
    unload_last()
    add_dir()


def register():
    bpy.app.handlers.load_post.append(append_new_dir)
    bpy.app.handlers.save_post.append(append_new_dir)
    add_dir()


if __name__ == "__main__":
    register()
