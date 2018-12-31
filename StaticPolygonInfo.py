
import arcpy
#输入要素
featureClass = arcpy.GetParameterAsText(0)
#存储多部件数
multPartCount = arcpy.GetParameterAsText(1)
#存储环数，如果没有环则为0
multRingCount = arcpy.GetParameterAsText(2)
#存储多边形节点数
nodeCout = arcpy.GetParameterAsText(3)
fc = featureClass
arcpy.AddField_management(fc,multPartCount,"SHORT")
arcpy.AddField_management(fc,multRingCount,"SHORT")
arcpy.AddField_management(fc,nodeCout,"SHORT")
listField = ["OID@","SHAPE@",multPartCount,multRingCount,nodeCout]
cursor = arcpy.da.UpdateCursor(fc,listField)
for row in cursor:
	partNum = 0
	ringNum = 0
	NodeNum = 0
	#每个部件
	for part in row[1]:
		## 每个节点
		for point in part:
			if point :
				NodeNum += 1
			else:
				ringNum +=1
		partNum += 1
	row[2] = partNum
	row[3] = ringNum
	row[4] = NodeNum
	cursor.updateRow(row)
del cursor