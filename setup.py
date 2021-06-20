from setuptools import setup
from freecad.archdesign import __version__
import os
# from freecad.workbench_starterkit.version import __version__
# name: this is the name of the distribution.
# Packages using the same name here cannot be installed together

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                            "freecad", "archdesign", "version.py")
with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.archdesign',
      version=str(__version__),
      packages=['freecad',
                'freecad.archdesign'],
      maintainer="carlopav",
      maintainer_email="carlopav@gmail.com",
      url="https://github.com/carlopav/freecad.archdesign",
      description="Experimental rewrite of FreeCAD Arch based on Geofeature and Origin Group Assembly concepts ",
      install_requires=[], # should be satisfied by FreeCAD's system dependencies already
      include_package_data=True)
