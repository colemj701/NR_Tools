# Import arcpy module
import arcpy, os, sys
arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True

arcpy.SetProgressor("default","Initiating Split by Attribute tool...")

# Script arguments

Split_Field = arcpy.GetParameterAsText(1)

# Process: Loop Split by attribute
FCS = arcpy.ListFeatureClasses()
cf_count = len(FCS)
arcpy.SetProgressor("step","Splitting features...")
for fc in FCS:
    desc = arcpy.Describe(fc)
    arcpy.SetProgressorLabel('Splitting "{0}" by "{1}"...'.format(desc.name,Split_Field))
    arcpy.analysis.SplitByAttributes(fc, arcpy.env.workspace, Split_Field)
    arcpy.SetProgressorPosition()