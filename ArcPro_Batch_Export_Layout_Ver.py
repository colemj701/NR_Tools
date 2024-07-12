#-------------------------------------------------------------------------------
# Name:        AEI_Rename_Separate_Map_Layouts.py
# Purpose:     Batch renames map layout exports and separate in equipment types
#                                              
# Author:      veronica.enierga
#
# Created:     5/9/2023
# Copyright:   (c) veronica.enierga 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy,os

arcpy.SetProgressor("default","Initiating batch layout export tool...")

arcpy.env.overwriteOutput = True

folder_path = arcpy.GetParameterAsText(0)

Project = arcpy.GetParameterAsText(1)

eqp_type = arcpy.GetParameterAsText(2)

aprx = arcpy.mp.ArcGISProject(Project)

lyts = aprx.listLayouts()
lyt_list = len(lyts)
arcpy.SetProgressor("step","Exporting project layouts",0,lyt_list,1)
for layout in lyts:
  arcpy.SetProgressorLabel('Exporting "{0}" to PDF...'.format(f"{layout.name}"))
  layout_name = layout.name.replace("\\"," ") + "_" + eqp_type
  layout.exportToPDF(os.path.join(folder_path, f"{layout_name}"), 300, "BEST", True, "ADAPTIVE", True, "LAYERS_ONLY", True, 80, False, False, True, False)
  arcpy.SetProgressorPosition()


# Function to rename map layouts
def renameMaps(dir):

    # Variables
    pdfNames = [file for file in os.listdir(dir) if file.endswith(".pdf")]
    root_path = dir
    equipment = ["ECU", "TNK", "ICE", "RCE", "MISC"]
    letter = ["B", "F", "D", "J", "H"]
    equip = []
    index = 0

    # Make equipment folders
    for item in equipment:
        path = os.path.join(root_path, item)
        if os.path.exists(path) is False:
            os.mkdir(path)

    # Move files into folders
    for pdfs in pdfNames:
        index = pdfNames.index(pdfs)
        equip = pdfNames[index].split("_")

        # Creates new PDF name
        for items in equipment:
            equipIndex = equipment.index(items)
            if equip[0] == equipment[equipIndex]:
                newName = equip[0] + " " + letter[equipIndex] + "-" + equip[1]
        
        os.rename(dir + "\\" + pdfNames[index], dir + "\\" + equip[0] + "\\" + newName)  

def main():

    renameMaps(folder_path)

if __name__ == '__main__':
    main()
