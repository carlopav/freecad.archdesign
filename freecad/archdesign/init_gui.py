import os
import FreeCADGui as Gui
import FreeCAD as App
from freecad.archdesign import ICONPATH


class ArchDesign(Gui.Workbench):
    """
    class which gets initiated at startup of the gui
    """

    MenuText = "ArchDesign workbench"
    ToolTip = "a simple template workbench"
    Icon = os.path.join(ICONPATH, "ArchDesign_Workbench.svg")
    toolbox = ['MakeWall', 'JoinWalls', 'ExtendWall',
               'MakeOpeningElement','MakeDoor', 'MakeWindow',
               'MakeView'
              ]

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """
        This function is called at the first activation of the workbench.
        here is the place to import all the commands
        """
        from freecad.archdesign.commands.wall import MakeWall
        from freecad.archdesign.commands.openings import MakeOpeningElement
        from freecad.archdesign.commands.openings import MakeDoor
        from freecad.archdesign.commands.openings import MakeWindow
        from freecad.archdesign.commands.joinwalls import JoinWalls
        from freecad.archdesign.commands.joinwalls import ExtendWall
        from freecad.archdesign.commands.view import MakeView
        
        App.Console.PrintMessage("switching to archdesign\n")

        self.appendToolbar("Tools", self.toolbox)
        self.appendMenu("Tools", self.toolbox)

        Gui.addCommand('MakeWall', MakeWall())
        Gui.addCommand('JoinWalls', JoinWalls())
        Gui.addCommand('ExtendWall', ExtendWall())
        Gui.addCommand('MakeOpeningElement', MakeOpeningElement())
        Gui.addCommand('MakeDoor', MakeDoor())
        Gui.addCommand('MakeWindow', MakeWindow())

        Gui.addCommand('MakeView', MakeView())

    def Activated(self):
        '''
        code which should be computed when a user switch to this workbench
        '''
        pass

    def Deactivated(self):
        '''
        code which should be computed when this workbench is deactivated
        '''
        pass


Gui.addWorkbench(ArchDesign())
