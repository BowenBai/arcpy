
import arcpy
#����Ҫ��
featureClass = arcpy.GetParameterAsText(0)
#�洢�ಿ����
multPartCount = arcpy.GetParameterAsText(1)
#�洢���������û�л���Ϊ0
multRingCount = arcpy.GetParameterAsText(2)
#�洢����νڵ���
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
	#ÿ������
	for part in row[1]:
		## ÿ���ڵ�
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