######################################################
#
#Run:
#   python setup.py py2exe
######################################################

import sys
from distutils.core import setup
import py2exe

sys.path.append("../../");

opts = {
    "py2exe":{
        "excludes":"OpenGL",
        "includes":"ctypes.*,weakref,logging",
    }
}

setup (
        options = opts,
	version="0.1.0",
	description="Cubix",
	name="Cubix",
	windows=[
        {
            "script": "../../cubix.py",     
            "icon_resources": [(1, "../../icon/48.ico")]
        }
    ],
        data_files=[("../../data.cbx"), ("PyOpenGL-3.0.0a6-py2.4.egg"),("glut32.dll")]
)