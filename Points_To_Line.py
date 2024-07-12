

# Import arcpy module
import arcpy, os, sys
arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True

arcpy.SetProgressor("default","Initiating Flag Points to Feature Line tool...")

# Script arguments

Split_Field = arcpy.GetParameterAsText(1)
Sort_Field = arcpy.GetParameterAsText(2)

# Process: Loop Split by attribute
Points = arcpy.ListFeatureClasses()
arcpy.SetProgressor("default","Splitting features...")
for fc in Points:
    desc1 = arcpy.Describe(fc)
    arcpy.SetProgressorLabel('Splitting "{0}" by "{1}"...'.format(desc1.name,Split_Field))
    arcpy.analysis.SplitByAttributes(fc, arcpy.env.workspace, Split_Field)
    arcpy.SetProgressorPosition()

arcpy.ResetProgressor()

# Process: Generate Lines from Split Points
Lines = arcpy.ListFeatureClasses()
line_count = len(Lines)
arcpy.SetProgressor("step","Generating feature lines from flag points",0,line_count,1)
for fc in Lines:
    desc2 = arcpy.Describe(fc)
    arcpy.SetProgressorLabel('Generating line "{0}"...'.format(desc2.name))
    arcpy.management.PointsToLine(fc,fc+"_Line",Split_Field,Sort_Field,"NO_CLOSE")
    arcpy.SetProgressorPosition()