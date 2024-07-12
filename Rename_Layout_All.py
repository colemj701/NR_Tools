import arcpy

arcpy.SetProgressor("default","Initiating Rename Layout tool...")

# open the project
aprx = arcpy.mp.ArcGISProject("CURRENT")

Figure_Num = arcpy.GetParameterAsText(0)
New_Num = arcpy.GetParameterAsText(1)
Map_Title = arcpy.GetParameterAsText(2)
New_Map_Title = arcpy.GetParameterAsText(3)

# get a list of all the layouts in the project
layouts = aprx.listLayouts()

# loop through the layouts and change the name
layout_count = len(layouts)
arcpy.SetProgressor("Step","Revising layout names...",0,layout_count,1)
for layout in layouts:
    layout.name = layout.name.replace(Figure_Num,New_Num).replace(Map_Title,New_Map_Title)
    arcpy.SetProgressorPosition()