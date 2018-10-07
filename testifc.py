# use 3d viewer

import ifcopenshell

import ifcopenshell.geom



settings = ifcopenshell.geom.settings()

settings.set(settings.USE_PYTHON_OPENCASCADE, True)

occ_display = ifcopenshell.geom.utils.initialize_display()

ifc_file = ifcopenshell.open("test3.ifc")


products = ifc_file.by_type("IfcProduct")

for product in products:
	if product.is_a("IfcOpeningElement"): continue
	if product.Representation:
		shape = ifcopenshell.geom.create_shape(settings, product).geometry
		display_shape = ifcopenshell.geom.utils.display_shape(shape)
		if product.is_a("IfcPlate"):
			ifcopenshell.geom.utils.set_shape_transparency(display_shape, 0.8)

import OCC
import OCC.BRepBndLib
import numpy

RED, BLUE, GREEN = (1, 0, 0, 1), (0, 0, 1, 1), (0, 1, 0, 1)


walls = ifc_file.by_type("Ifcwall")
wall_shapes = []
bbox = OCC.Bnd.Bnd_Box()
for wall in walls:

	print('wall info \n', wall.get_info(),'\n')
	print('ObjectPlacement : ', wall.get_info()['ObjectPlacement'])
	
	shape = ifcopenshell.geom.create_shape(settings, wall).geometry
	wall_shapes.append((wall, shape))
	OCC.BRepBndLib.brepbndlib_Add(shape, bbox)
	g= BLUE
	ifcopenshell.geom.utils.display_shape(shape, clr=g)

print(ifc_file.by_id(111))


# find center
bounding_box_center = ifcopenshell.geom.utils.get_bounding_box_center(bbox)

occ_display.DisplayMessage(bounding_box_center, "C", update=True)

