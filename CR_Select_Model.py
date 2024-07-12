
# Import arcpy module
import arcpy, os, sys

arcpy.SetProgressor("default","Initiating CR Selection tool...")

workspace1 = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True

# Script Arguments 1 Project Area 2 Target Output 3 workspace 4 output coordinate system
Project_Area = arcpy.GetParameterAsText(1)


Output_gdb = arcpy.GetParameterAsText(2)

OTL = arcpy.GetParameterAsText(3)

Output_Coordinate_System = arcpy.GetParameterAsText(4)

APE_Buf = arcpy.GetParameterAsText(5)

# Local Variables
default_gdb = arcpy.env.scratchGDB
APE = arcpy.analysis.PairwiseBuffer(Project_Area,Output_gdb+"\\CR_APE",APE_Buf,"NONE","","PLANAR")
Output_Feature_Layer = "feature_layer"


# Process: Batch Project CR Data
arcpy.env.workspace = workspace1
FCs = arcpy.ListFeatureClasses()
fc_count1 = len(FCs)
arcpy.SetProgressor("step","Projecting CR shapefiles...",0,fc_count1,1)
for fc in FCs:
    desc = arcpy.Describe(fc)
    arcpy.SetProgressorLabel('Projecting "{0}"...'.format(desc.name))
    arcpy.management.Project(fc, default_gdb+"\\"+desc.name.rstrip(".shp"),Output_Coordinate_System)
    arcpy.SetProgressorPosition()

arcpy.ResetProgressor()

arcpy.env.workspace = default_gdb
FCselect = arcpy.ListFeatureClasses()
fc_count2 = len(FCselect)
arcpy.SetProgressor("default","Executing Selection Process")
for fc in FCselect:
    desc1 = arcpy.Describe(fc)
    arcpy.SetProgressorLabel('Selecting "{0}" with "{1}" APE...'.format(desc1.name,APE_Buf))
    arcpy.management.MakeFeatureLayer(fc, Output_Feature_Layer)
    arcpy.management. SelectLayerByLocation(Output_Feature_Layer,"INTERSECT",APE,"","NEW_SELECTION","NOT_INVERT")
    arcpy.management.CopyFeatures(Output_Feature_Layer,Output_gdb+"\\"+desc1.name)
    arcpy.SetProgressorPosition()
    arcpy.SetProgressorLabel('Exporting "{0}" attribute table...'.format(desc1.name))
    arcpy.conversion.TableToTable(Output_Feature_Layer,OTL,fc+".csv")
    arcpy.SetProgressorPosition()
    arcpy.management.DeleteFeatures(fc)
                        
