import os
import arcpy

outPath = "d:"
outName = "Vector5"
arcpy.env.workspace = "d:"
arcpy.CreateFeatureclass_management(outPath,outName,"POLYGON","","DISABLED","DISABLED","","","","","")
arcpy.AddField_management("d:Vector5.shp","bh","LONG","","","","","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management("d:Vector5.shp","height","SHORT","","","","","NULLABLE","NON_REQUIRED","")

f1 = file(r"D:\buildVector\buildings0","r")
h1 = file(r"D:\buildVector\attribute0","r")
while True:
	line = f1.readline()
	if not line:
		break
	eme = line.split()
	if len(eme) == 3:
		arr = arcpy.Array()
		nodeCount = int(eme[2])
		cursor = arcpy.InsertCursor("d:Vector5.shp")
		array = arcpy.Array()
		point = arcpy.Point()
		for i in range(nodeCount):
			line = f1.readline()
			sxy = line.split(" ")
			x = float(sxy[0])
			y = float(sxy[1])
			point.X = x
			point.Y = y
			array.add(point)
		heigth = int(h1.readline().split()[2])
		row = cursor.newRow()
		row.shape = array
		row.height = heigth
		cursor.insertRow(row)
		array.removeAll()
f1.close()
h1.close()