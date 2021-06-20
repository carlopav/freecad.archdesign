#***************************************************************************
#*   Copyright (c) 2020 Carlo Pavan                                        *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************
"""Provide the object code for Arch objects.
This module was added during 0.19 dev cycle to offer some base classes
to the new arch objects.
Old objects were derived from ArchComponent, and strictly related to IFC
implementation, new objects are more lightweight related to IFC.
"""
## @package base
# \ingroup ARCH
# \brief Provide the object code for Arch base objects.

import FreeCAD as App
from PySide.QtCore import QT_TRANSLATE_NOOP

import ArchIFC

class ShapeGroup(object):
    """
    The ShapeGroup object is the base object for Arch Walls.
    It provides the possibility to display the object own shape and also 
    the grouped objects shape at the same time.
    The object was designed by realthunder.

    ref: Python object with OriginGroupExtension
         https://forum.freecadweb.org/viewtopic.php?f=22&t=44701
         https://gist.github.com/realthunder/40cd71a3085be666c3e2d718171de133
    """
    def __init__(self, obj=None):
        self.Object = obj
        if obj:
            self.attach(obj)

    def __getstate__(self):
        return

    def __setstate__(self,_state):
        return

    def attach(self,obj):
        obj.addExtension('App::GeoFeatureGroupExtensionPython')

    def onDocumentRestored(self, obj):
        self.Object = obj



class Component(ShapeGroup, ArchIFC.IfcProduct):

    def __init__(self, obj=None):
        super(Component, self).__init__(obj)
        # print("running wall object init method\n")
        if obj:
            print("running obj init method")

            obj.Proxy = self
            self.Object = obj
            self.attach(obj)
            self.execute(obj)

        # self.Type = 'ArchDesign_Product' TO BE SET IN DERIVED OBJECT

    def attach(self, obj):
        ShapeGroup.attach(self, obj)
        ArchIFC.IfcProduct.setProperties(self, obj)
        Component.set_properties(self, obj)


    def set_properties(self, obj):
        """Give the component its component specific properties, such as material.

        You can learn more about properties here:
        https://wiki.freecadweb.org/property
        """

        existing_properties = obj.PropertiesList

        # BASE Properties ---------------------------------------------------
        _tip = 'Link to the material object.'
        obj.addProperty('App::PropertyLink', 'Material',
                        'Base', _tip)

        # COMPONENTS Properties (partially implemented at the moment) ---------
        if not "Additions" in existing_properties:
            _tip = 'List of objects to include in a compound with the base component shape'
            obj.addProperty('App::PropertyLinkListChild', 'Additions',
                            'Components', _tip) # TODO: better PropertyLinkListGlobal or PropertyLinkListChild?

        if not "Subtractions" in existing_properties:
            _tip = 'List of objects to subtract from the component shape'
            obj.addProperty('App::PropertyLinkListGlobal', 'Subtractions',
                            'Components', _tip)

        if not "BaseGeometry" in existing_properties:
            _tip = 'Optional objects to use as base geometry for the wall shape'
            obj.addProperty('App::PropertyLinkListChild', 'BaseGeometry',
                            'Components', _tip) # TODO: better PropertyLinkListGlobal or PropertyLinkListChild?

        # COMPONENTS Properties (partially implemented at the moment) ---------
        if not "StandardCode" in existing_properties:
            obj.addProperty("App::PropertyString","StandardCode","Component",QT_TRANSLATE_NOOP("App::Property","An optional standard (OmniClass, etc...) code for this component"))



'''
class Product(ShapeGroup, ArchIFC.IfcProduct):
    """The Arch Component object.

    Acts as a base for all other Arch objects, such as Arch walls and Arch
    structures. Its properties and behaviours are common to all Arch objects.

    You can learn more about Arch Components, and the purpose of Arch
    Components here: https://wiki.freecadweb.org/Arch_Component

    Parameters
    ----------
    obj: <App::FeaturePython>
        The object to turn into an Arch Component
    """


    def __init__(self, obj):
        obj.Proxy = self
        if obj:
            # print("running obj init method")

            obj.Proxy = self
            self.Object = obj
            self.attach(obj)
            self.execute(obj)
        self.Type = "Product"

    def attach(self, obj):
        ShapeGroup.attach(self, obj)
        self.setProperties(obj)


    def setProperties(self, obj):
        """Give the component its component specific properties, such as material.

        You can learn more about properties here:
        https://wiki.freecadweb.org/property
        """

        ArchIFC.IfcProduct.setProperties(self, obj)

        pl = obj.PropertiesList

        # COMPONENTS Properties (partially implemented at the moment) ---------

        if not "Additions" in pl:
            _tip = 'List of objects to include in a compound with the base product shape'
            obj.addProperty('App::PropertyLinkListChild', 'Additions',
                            'Components', _tip) # TODO: better PropertyLinkListGlobal or PropertyLinkListChild?

        if not "Subtractions" in pl:
            _tip = 'List of objects to subtract from the product shape'
            obj.addProperty('App::PropertyLinkListGlobal', 'Subtractions',
                            'Components', _tip)

        if not "BaseGeometry" in pl:
            _tip = 'Optional objects to use as base geometry for the wall shape'
            obj.addProperty('App::PropertyLinkListChild', 'BaseGeometry',
                            'Components', _tip) # TODO: better PropertyLinkListGlobal or PropertyLinkListChild?

        # COMPONENTS Properties (partially implemented at the moment) ---------

        if not "Description" in pl:
            obj.addProperty("App::PropertyString","Description","Component",QT_TRANSLATE_NOOP("App::Property","An optional description for this component"))
        if not "Tag" in pl:
            obj.addProperty("App::PropertyString","Tag","Component",QT_TRANSLATE_NOOP("App::Property","An optional tag for this component"))
        if not "StandardCode" in pl:
            obj.addProperty("App::PropertyString","StandardCode","Component",QT_TRANSLATE_NOOP("App::Property","An optional standard (OmniClass, etc...) code for this component"))
        if not "Material" in pl:
            obj.addProperty("App::PropertyLink","Material","Component",QT_TRANSLATE_NOOP("App::Property","A material for this object"))

        self.Subvolume = None
        #self.MoveWithHost = False
        self.Type = "Component"


    def onDocumentRestored(self, obj):
        """Method run when the document is restored. Re-add the Arch component properties.

        Parameters
        ----------
        obj: <App::FeaturePython>
            The component object.
        """
        self.setProperties(self, obj)


    def execute(self,obj):
        """Method run when the object is recomputed. (to be overrided)

        If the object is a clone, just copy the shape it's cloned from.

        Process subshapes of the object to add additions, and subtract
        subtractions from the object's shape.

        Parameters
        ----------
        obj: <App::FeaturePython>
            The component object.
        """
        if obj.Base:
            shape = self.spread(obj,obj.Base.Shape)
            if obj.Additions or obj.Subtractions:
                shape = self.processSubShapes(obj,shape)
            obj.Shape = shape

        return


    def __getstate__(self):
        # for compatibility with 0.17
        if hasattr(self,"Type"):
            return self.Type
        return "ArchDesign_Product"


    def __setstate__(self,state):
        return None


    def onBeforeChange(self, obj, prop):
        """Method called before the object has a property changed.

        Specifically, this method is called before the value changes.

        Parameters
        ----------
        obj: <App::FeaturePython>
            The component object.
        prop: string
            The name of the property that has changed.
        """
        return


    def onChanged(self, obj, prop):
        """Method called when the object has a property changed.

        call ArchIFC.IfcProduct.onChanged().

        Parameters
        ----------
        obj: <App::FeaturePython>
            The component object.
        prop: string
            The name of the property that has changed.
        """

        ArchIFC.IfcProduct.onChanged(self, obj, prop)

        return


    def getParentHeight(self,obj):
        """Get a height value from hosts.

        Recursively crawl hosts until a Floor or BuildingPart is found, then
        return the value of its Height property.

        Parameters
        ---------
        obj: <App::FeaturePython>
            The component object.

        Returns
        -------
        <App::PropertyLength>
            The Height value of the found Floor or BuildingPart.
        """

        for parent in obj.InList:
            if Draft.getType(parent) in ["Floor","BuildingPart"]:
                if obj in parent.Group:
                    if parent.HeightPropagate:
                        if parent.Height.Value:
                            return parent.Height.Value
        # not found? get one level higher
        for parent in obj.InList:
            if hasattr(parent,"Group"):
                if obj in parent.Group:
                    return self.getParentHeight(parent)
        return 0


    def getExtrusionData(self,obj):
        """Get the object's extrusion data.

        Recursively scrape the Bases of the object, until a Base that is
        derived from a <Part::Extrusion> is found. From there, copy the
        extrusion to the (0,0,0) origin.

        With this copy, get the <Part.Face> the shape was originally
        extruded from, the <Base.Vector> of the extrusion, and the
        <Base.Placement> needed to move the copy back to its original
        location/orientation. Return this data as a tuple.

        If an object derived from a <Part::Multifuse> is encountered, return
        this data as a tuple containing lists. The lists will contain the same
        data as above, from each of the objects within the multifuse.

        Parameters
        ----------
        obj: <App::FeaturePython>
            The component object.

        Returns
        -------
        tuple
            Tuple containing:

            1) The <Part.Face> the object was extruded from.
            2) The <Base.Vector> of the extrusion.
            3) The <Base.Placement> of the extrusion.
        """

        if hasattr(obj,"CloneOf"):
            if obj.CloneOf:
                if hasattr(obj.CloneOf,"Proxy"):
                    if hasattr(obj.CloneOf.Proxy,"getExtrusionData"):
                        data = obj.CloneOf.Proxy.getExtrusionData(obj.CloneOf)
                        if data:
                            return data

        if obj.Base:
            # the base is another arch object which can provide extrusion data
            if hasattr(obj.Base,"Proxy") and hasattr(obj.Base.Proxy,"getExtrusionData") and (not obj.Additions) and (not obj.Subtractions):
                if obj.Base.Base:
                    if obj.Placement.Rotation.Angle < 0.0001:
                        # if the final obj is rotated, this will screw all our IFC orientation. Better leave it like that then...
                        data = obj.Base.Proxy.getExtrusionData(obj.Base)
                        if data:
                            return data
                            # TODO above doesn't work if underlying shape is not at (0,0,0). But code below doesn't work well yet
                            # add the displacement of the final object
                            disp = obj.Shape.CenterOfMass.sub(obj.Base.Shape.CenterOfMass)
                            if isinstance(data[2],(list,tuple)):
                                ndata2 = []
                                for p in data[2]:
                                    p.move(disp)
                                    ndata2.append(p)
                                return (data[0],data[1],ndata2)
                            else:
                                ndata2 = data[2]
                                ndata2.move(disp)
                                return (data[0],data[1],ndata2)

            # the base is a Part Extrusion
            elif obj.Base.isDerivedFrom("Part::Extrusion"):
                if obj.Base.Base:
                    base,placement = self.rebase(obj.Base.Base.Shape)
                    extrusion = FreeCAD.Vector(obj.Base.Dir).normalize()
                    if extrusion.Length == 0:
                        extrusion = FreeCAD.Vector(0,0,1)
                    else:
                        extrusion = placement.inverse().Rotation.multVec(extrusion)
                    if hasattr(obj.Base,"LengthFwd"):
                        if obj.Base.LengthFwd.Value:
                            extrusion = extrusion.multiply(obj.Base.LengthFwd.Value)
                    if not self.isIdentity(obj.Base.Placement):
                        placement = placement.multiply(obj.Base.Placement)
                    return (base,extrusion,placement)

            elif obj.Base.isDerivedFrom("Part::MultiFuse"):
                rshapes = []
                revs = []
                rpls = []
                for sub in obj.Base.Shapes:
                    if sub.isDerivedFrom("Part::Extrusion"):
                        if sub.Base:
                            base,placement = self.rebase(sub.Base.Shape)
                            extrusion = FreeCAD.Vector(sub.Dir).normalize()
                            if extrusion.Length == 0:
                                extrusion = FreeCAD.Vector(0,0,1)
                            else:
                                extrusion = placement.inverse().Rotation.multVec(extrusion)
                            if hasattr(sub,"LengthFwd"):
                                if sub.LengthFwd.Value:
                                    extrusion = extrusion.multiply(sub.LengthFwd.Value)
                            placement = obj.Placement.multiply(placement)
                            rshapes.append(base)
                            revs.append(extrusion)
                            rpls.append(placement)
                    else:
                        exdata = ArchCommands.getExtrusionData(sub.Shape)
                        if exdata:
                            base,placement = self.rebase(exdata[0])
                            extrusion = placement.inverse().Rotation.multVec(exdata[1])
                            placement = obj.Placement.multiply(placement)
                            rshapes.append(base)
                            revs.append(extrusion)
                            rpls.append(placement)
                if rshapes and revs and rpls:
                    return (rshapes,revs,rpls)
        return None


    def hideSubobjects(self,obj,prop):
        """Hides Additions and Subtractions of this Component when that list changes.

        Intended to be used in conjunction with the .onChanged() method, to
        access the property that has changed.

        When an object loses or gains an Addition, this method hides all
        Additions.  When it gains or loses a Subtraction, this method hides all
        Subtractions.

        Does not effect objects of type Window, or clones of Windows.

        Parameters
        ----------
        obj: <App::FeaturePython>
            The component object.
        prop: string
            The name of the property that has changed.
        """

        if FreeCAD.GuiUp:
            if prop in ["Additions","Subtractions"]:
                if hasattr(obj,prop):
                    for o in getattr(obj,prop):
                        if (Draft.getType(o) != "Window") and (not Draft.isClone(o,"Window",True)):
                            if (Draft.getType(obj) == "Wall"):
                                if (Draft.getType(o) == "Roof"):
                                    continue
                            o.ViewObject.hide()
            elif prop in ["Mesh"]:
                if hasattr(obj,prop):
                    o = getattr(obj,prop)
                    if o:
                        o.ViewObject.hide()


    def processSubShapes(self,obj,base,placement=None):
        """Add Additions and Subtractions to a base shape.

        If Additions exist, fuse them to the base shape. If no base is
        provided, just fuse other additions to the first addition.

        If Subtractions exist, cut them from the base shape. Roofs and Windows
        are treated uniquely, as they define their own Shape to subtract from
        parent shapes using their .getSubVolume() methods.

        TODO determine what the purpose of the placement argument is.

        Parameters
        ----------
        obj: <App::FeaturePython>
            The component object.
        base: <Part.Shape>, optional
            The base shape to add Additions and Subtractions to.
        placement: <Base.Placement>, optional
            Prior to adding or subtracting subshapes, the <Base.Placement> of
            the subshapes are multiplied by the inverse of this parameter.

        Returns
        -------
        <Part.Shape>
            The base shape, with the additions and subtractions performed.
        """

        import Draft,Part
        #print("Processing subshapes of ",obj.Label, " : ",obj.Additions)

        if placement:
            if self.isIdentity(placement):
                placement = None
            else:
                placement = FreeCAD.Placement(placement)
                placement = placement.inverse()

        # treat additions
        for o in obj.Additions:

            if not base:
                if hasattr(o,'Shape'):
                    base = o.Shape
            else:
                if base.isNull():
                    if hasattr(o,'Shape'):
                        base = o.Shape
                else:
                    # special case, both walls with coinciding endpoints
                    import ArchWall
                    js = ArchWall.mergeShapes(o,obj)
                    if js:
                        add = js.cut(base)
                        if placement:
                            add.Placement = add.Placement.multiply(placement)
                        base = base.fuse(add)

                    elif hasattr(o,'Shape'):
                        if o.Shape and not o.Shape.isNull() and o.Shape.Solids:
                            s = o.Shape.copy()
                            if placement:
                                s.Placement = s.Placement.multiply(placement)
                            if base:
                                if base.Solids:
                                    try:
                                        base = base.fuse(s)
                                    except Part.OCCError:
                                        print("Arch: unable to fuse object ", obj.Name, " with ", o.Name)
                            else:
                                base = s

        # treat subtractions
        subs = obj.Subtractions
        for link in obj.InListRecursive:
            if hasattr(link,"Hosts"):
                if link.Hosts:
                    if obj in link.Hosts:
                        subs.append(link)
            elif hasattr(link,"Host") and Draft.getType(link) != "Rebar":
                if link.Host == obj:
                    subs.append(link)
        for o in subs:
            if base:
                if base.isNull():
                    base = None

            if base:
                subvolume = None

                if (Draft.getType(o.getLinkedObject()) == "Window") or (Draft.isClone(o,"Window",True)):
                    # windows can be additions or subtractions, treated the same way
                    subvolume = o.getLinkedObject().Proxy.getSubVolume(o)
                elif (Draft.getType(o) == "Roof") or (Draft.isClone(o,"Roof")):
                    # roofs define their own special subtraction volume
                    subvolume = o.Proxy.getSubVolume(o)
                elif hasattr(o,"Subvolume") and hasattr(o.Subvolume,"Shape"):
                    # Any other object with a Subvolume property
                    subvolume = o.Subvolume.Shape.copy()
                    if hasattr(o,"Placement"):
                        subvolume.Placement = subvolume.Placement.multiply(o.Placement)

                if subvolume:
                    if base.Solids and subvolume.Solids:
                        if placement:
                            subvolume.Placement = subvolume.Placement.multiply(placement)
                        if len(base.Solids) > 1:
                            base = Part.makeCompound([sol.cut(subvolume) for sol in base.Solids])
                        else:
                            base = base.cut(subvolume)

                elif hasattr(o,'Shape'):
                    # no subvolume, we subtract the whole shape
                    if o.Shape:
                        if not o.Shape.isNull():
                            if o.Shape.Solids and base.Solids:
                                    s = o.Shape.copy()
                                    if placement:
                                        s.Placement = s.Placement.multiply(placement)
                                    try:
                                        if len(base.Solids) > 1:
                                            base = Part.makeCompound([sol.cut(s) for sol in base.Solids])
                                        else:
                                            base = base.cut(s)
                                    except Part.OCCError:
                                        print("Arch: unable to cut object ",o.Name, " from ", obj.Name)
        return base

    def isIdentity(self,placement):
        """Check if a placement is *almost* zero.

        Check if a <Base.Placement>'s displacement from (0,0,0) is almost zero,
        and if the angle of its rotation about its axis is almost zero.

        Parameters
        ----------
        placement: <Base.Placement>
            The placement to examine.

        Returns
        -------
        bool
            Returns true if angle and displacement are almost zero, false it
            otherwise.
        """

        if (placement.Base.Length < 0.000001) and (placement.Rotation.Angle < 0.000001):
            return True
        return False

    def applyShape(self,obj,shape,placement,allowinvalid=False,allownosolid=False):
        """Check the given shape, then assign it to the object.

        Finally, run .computeAreas() method, to calculate the horizontal and
        vertical area of the shape.

        Parameters
        ----------
        obj: <App::FeaturePython>
            The component object.
        shape: <Part.Shape>
            The shape to check and apply to the object.
        placement: <Base.Placement>
            The placement to apply to the object.
        allowinvalid: bool, optional
            Whether to allow invalid shapes, or to throw an error.
        allownosolid: bool, optional
            Whether to allow non-solid shapes, or to throw an error.
        """
        if not shape:
            App.Console.PrintWarning(obj.Label + " " + translate("ArchDesign","has an invalid shape")+"\n")
            return
        if not shape.isNull():
            App.Console.PrintWarning(obj.Label + " " + translate("ArchDesign","has a null shape")+"\n")
            return

        if not shape.isValid():
            if allowinvalid:
                obj.Shape = self.spread(obj,shape,placement)
                if not self.isIdentity(placement):
                    obj.Placement = placement
            else:
                FreeCAD.Console.PrintWarning(obj.Label + " " + translate("Arch","has an invalid shape")+"\n")
            return

        if shape.Solids:
            if shape.Volume < 0:
                shape.reverse()
            if shape.Volume < 0:
                FreeCAD.Console.PrintError(translate("Arch","Error computing the shape of this object")+"\n")
                return
            import Part
            try:
                r = shape.removeSplitter()
            except Part.OCCError:
                pass
            else:
                shape = r
            p = self.spread(obj,shape,placement).Placement.copy() # for some reason this gets zeroed in next line
            obj.Shape = self.spread(obj,shape,placement)
            if not self.isIdentity(placement):
                obj.Placement = placement
            else:
                obj.Placement = p
        else:
            if allownosolid:
                obj.Shape = self.spread(obj,shape,placement)
                if not self.isIdentity(placement):
                    obj.Placement = placement
            else:
                App.Console.PrintWarning(obj.Label + " " + translate("Arch","has no solid")+"\n")

        self.computeAreas(obj)

    def isStandardCase(self,obj):
        """Determine if the component is a standard case of its IFC type.

        Not all IFC types have a standard case.

        If an object is a standard case or not varies between the different
        types. Each type has its own rules to define what is a standard case.

        Rotated objects, or objects with Additions or Subtractions are not
        standard cases.

        All objects whose IfcType is suffixed with the string " Sandard Case"
        are automatically a standard case.

        Parameters
        ----------
        obj: <App::FeaturePython>
            The component object.

        Returns
        -------
        bool
            Whether the object is a standard case or not.
        """

        # Standard Case has been set manually by the user
        if obj.IfcType.endswith("Standard Case"):
            return True
        # Try to guess
        import ArchIFC
        if obj.IfcType + " Standard Case" in ArchIFC.IfcTypes:
            # this type has a standard case
            if obj.Additions or obj.Subtractions:
                return False
            if obj.Placement.Rotation.Axis.getAngle(FreeCAD.Vector(0,0,1)) > 0.01:
                # reject rotated objects
                return False
            if obj.CloneOf:
                return obj.CloneOf.Proxy.isStandardCase(obj.CloneOf)
            if obj.IfcType == "Wall":
                # rules:
                # - vertically extruded
                # - single baseline or no baseline
                if (not obj.Base) or (len(obj.Base.Shape.Edges) == 1):
                    if hasattr(obj,"Normal"):
                        if obj.Normal in [FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1)]:
                            return True
            elif obj.IfcType in ["Beam","Column","Slab"]:
                # rules:
                # - have a single-wire profile or no profile
                # - extrusion direction is perpendicular to the profile
                if obj.Base and (len(obj.Base.Shape.Wires) != 1):
                    return False
                if not hasattr(obj,"Normal"):
                    return False
                if hasattr(obj,"Tool") and obj.Tool:
                    return False
                if obj.Normal == FreeCAD.Vector(0,0,0):
                    return True
                elif len(obj.Base.Shape.Wires) == 1:
                    import DraftGeomUtils
                    n = DraftGeomUtils.getNormal(obj.Base.Shape)
                    if n:
                        if (n.getAngle(obj.Normal) < 0.01) or (abs(n.getAngle(obj.Normal)-3.14159) < 0.01):
                            return True
            # TODO: Support windows and doors
            # rules:
            # - must have a rectangular shape
            # - must have a host
            # - must be parallel to the host plane
            # - must have an IfcWindowType and IfcRelFillsElement (to be implemented in IFC exporter)
            return False

'''
