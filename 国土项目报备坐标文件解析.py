import arcpyimport os
txtPath = arcpy.GetParameterAsText(0)
outPath = arcpy.GetParameterAsText(1)
outName = arcpy.GetParameterAsText(2)
arcpy.env.workspace = outPath
arcpy.CreateFeatureclass_management(outPath,outName,"POLYGON","","DISABLED","DISABLED","","","","","")
#����ֶ�
outShp = os.path.join(outPath,outName)+".shp"
arcpy.AddField_management(outShp,"��ַ����","SHORT","","","","jzds","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"�ؿ����","DOUBLE",12,2,"","dkmj","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"�ؿ���","TEXT","","","","dkbh","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"�ؿ�����","TEXT","","","","dkmc","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"��������","TEXT","","","","jhlx","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"ͼ�����","TEXT","","","","tfbh","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"�ؿ���;","TEXT","","","","dkyt","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"�������","TEXT","","","","dlbm","NULLABLE","NON_REQUIRED","")
f = open(txtPath,"r")
while True:
    line = f.readline()    
    if not line:        
        break
    #print line
    em = line.split(",")    
    if len(em) == 9:
        jzds = int(em[0])
        dkmj = float(em[1])
        dkmc = em[2]
        dkbh = em[3]
        jhlx = em[4]
        tf   = em[5]
        dkyt = em[6]
        dlbm = em[7]
        cursor = arcpy.InsertCursor(outShp)        
        #�洢���ζ�����Ϣ
        parts = arcpy.Array() #�ಿ��
        rings = arcpy.Array() #�໷����

        #��ʶ�Ƿ��ж���Ϣ
        flag = "1"
        ring = arcpy.Array()
        point = arcpy.Point()        
        #�������
        for i in range(jzds):
            xyline = f.readline()
            namedkbhyx = xyline.split(",")            
            if len(namedkbhyx) == 4:                
                name = namedkbhyx[0]
                bh = namedkbhyx[1].strip()                
                if bh == flag:                    
                    #���flagû�з����仯�������ڻ�    
                    y = float(namedkbhyx[2])
                    x = float(namedkbhyx[3])
                    point.X = x
                    point.Y = y
                    ring.add(point)                
                else:                    
                    #��ʼһ���»�.����ΪNone
                    rings.add(ring)
                    ring.removeAll()

                    flag = bh        
        #�������һ��
        rings.add(ring)        
        ##rings.remove(0)
        ring.removeAll()        
        # ���ֻ��һ�������Ƴ�����
        if len(rings) == 1:
            rings = rings.getObject(0)
        parts.add(rings)
        rings.removeAll()        
        #����ǵ�����Ҫ��
        if len(parts) == 1:
            parts = parts.getObject(0)        
        #endfor
        #���Ը�ֵ
        row = cursor.newRow()

        row.shape = arcpy.Polygon(parts)
        row.setValue("��ַ����",jzds)
        row.setValue("�ؿ����",dkmj)
        row.setValue("�ؿ�����",dkmc)
        row.setValue("�ؿ���",dkbh)
        row.setValue("��������",jhlx)
        row.setValue("ͼ�����",tf)
        row.setValue("�ؿ���;",dkyt)
        row.setValue("�������",dlbm)
        cursor.insertRow(row)
f.close()
del cursor
print "----Done----"