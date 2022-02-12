import os
from .version import __version__
import FreeCAD as App

#import freecad.archdesign.import_ifc
#import freecad.archdesign.export_ifc

ICONPATH = os.path.join(os.path.dirname(__file__), "resources", "icons")

#App.addImportType("ArchDesign Industry Foundation Classes (*.ifc)","freecad.archdesign.import_ifc")
#App.addExportType("ArchDesign Industry Foundation Classes (*.ifc)","freecad.archdesign.export_ifc")
