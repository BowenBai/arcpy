import arcpyimport os
txtPath = arcpy.GetParameterAsText(0)
outPath = arcpy.GetParameterAsText(1)
outName = arcpy.GetParameterAsText(2)
arcpy.env.workspace = outPath
arcpy.CreateFeatureclass_management(outPath,outName,"POLYGON","","DISABLED","DISABLED","","","","","")
#添加字段
outShp = os.path.join(outPath,outName)+".shp"
arcpy.AddField_management(outShp,"界址点数","SHORT","","","","jzds","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"地块面积","DOUBLE",12,2,"","dkmj","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"地块编号","TEXT","","","","dkbh","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"地块名称","TEXT","","","","dkmc","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"几何类型","TEXT","","","","jhlx","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"图幅编号","TEXT","","","","tfbh","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"地块用途","TEXT","","","","dkyt","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management(outShp,"地类编码","TEXT","","","","dlbm","NULLABLE","NON_REQUIRED","")
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
        #存储几何对象信息
        parts = arcpy.Array() #多部件
        rings = arcpy.Array() #多环对象

        #标识是否含有洞信息
        flag = "1"
        ring = arcpy.Array()
        point = arcpy.Point()        
        #坐标解析
        for i in range(jzds):
            xyline = f.readline()
            namedkbhyx = xyline.split(",")            
            if len(namedkbhyx) == 4:                
                name = namedkbhyx[0]
                bh = namedkbhyx[1].strip()                
                if bh == flag:                    
                    #如果flag没有发生变化则增加内环    
                    y = float(namedkbhyx[2])
                    x = float(namedkbhyx[3])
                    point.X = x
                    point.Y = y
                    ring.add(point)                
                else:                    
                    #开始一个新环.坐标为None
                    rings.add(ring)
                    ring.removeAll()

                    flag = bh        
        #加上最后一环
        rings.add(ring)        
        ##rings.remove(0)
        ring.removeAll()        
        # 如果只有一个环，移除其他
        if len(rings) == 1:
            rings = rings.getObject(0)
        parts.add(rings)
        rings.removeAll()        
        #如果是单部件要素
        if len(parts) == 1:
            parts = parts.getObject(0)        
        #endfor
        #属性赋值
        row = cursor.newRow()

        row.shape = arcpy.Polygon(parts)
        row.setValue("界址点数",jzds)
        row.setValue("地块面积",dkmj)
        row.setValue("地块名称",dkmc)
        row.setValue("地块编号",dkbh)
        row.setValue("几何类型",jhlx)
        row.setValue("图幅编号",tf)
        row.setValue("地块用途",dkyt)
        row.setValue("地类编码",dlbm)
        cursor.insertRow(row)
f.close()
del cursor
print "----Done----"