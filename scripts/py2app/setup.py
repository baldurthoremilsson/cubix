'''
Usage:
   python setup.py py2app
'''

import sys
sys.path.append('../../')
from setuptools import setup

PATH = "../../"

setup (
	version="1.0",
	description="Cubix",
	name="Cubix",
    	setup_requires=['py2app'],
	app=[PATH + 'cubix.py'],
	data_files=[(PATH + "data.cbx")],
	options={'py2app': {'argv_emulation':True}}
)
