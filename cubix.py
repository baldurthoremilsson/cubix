#!/usr/bin/python
import sys, os

#py2exe openglfix
if sys.platform[:3] == 'win':
    sys.path.insert(
        0,
        os.path.join(
            os.path.dirname( sys.executable ),
            'PyOpenGL-3.0.0a6-py2.4.egg'
        )
    )
    sys.path.append("scripts/py2exe/");
    import py2exeeggs
    py2exeeggs.loadEggs()


from engine3d import Engine3d
from engine3d.games import Tetris3d

e = Engine3d()
game = Tetris3d()
e.run( game )
