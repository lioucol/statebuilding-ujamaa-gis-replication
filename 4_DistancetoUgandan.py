import arcpy
import os
import pandas as pd


# Set working directory
# Modify the paths as needed
base_dir = "/Users/YAWEN L/Dropbox/GIS_Yawen/gis_input"
    
input_dir = os.path.join(base_dir, "input")
output_dir = os.path.join(base_dir, "output")
process_dir = os.path.join(base_dir, "process")


def DistancetoUgandan():  # DistancetoUgandan

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Define input and output paths
    tza_adm2_1967_2_ = os.path.join(input_dir, "tza_adm2_1967",  "tza_adm2_1967.shp")
    adm0_lines = os.path.join(input_dir, "adm0_lines.gdb", "adm0_lines")
    tza_adm2_1967_FeatureToPoint = os.path.join(process_dir, "tza_adm2_points", "tza_adm2_points.shp")
    
    UgandanBorder_dir = os.path.join(process_dir, "UgandanBorder")
    UgandanBorder = os.path.join(UgandanBorder_dir,"UgandanBorder.shp")
    
    DistanceToUgandan_dir = os.path.join(output_dir, "DistanceToUgandan")
    DistanceToUgandan_xlsx = os.path.join(DistanceToUgandan_dir, "DistanceToUgandan.xlsx")
    

    # Create directories if they don't exist
    os.makedirs(UgandanBorder_dir, exist_ok=True)
    os.makedirs(DistanceToUgandan_dir, exist_ok=True)
                              
    # Process: Export Features (Export Features) (conversion)
    arcpy.conversion.ExportFeatures(in_features=adm0_lines, out_features=UgandanBorder, where_clause="country1 = 'TANZANIA' And country2 = 'UGANDA'", field_mapping="adm_id \"adm_id\" true true false 8 Double 0 0,First,#,adm0_lines,adm_id,-1,-1;cc1 \"cc1\" true true false 65536 Text 0 0,First,#,adm0_lines,cc1,0,65535;country1 \"country1\" true true false 65536 Text 0 0,First,#,adm0_lines,country1,0,65535;cc2 \"cc2\" true true false 65536 Text 0 0,First,#,adm0_lines,cc2,0,65535;country2 \"country2\" true true false 65536 Text 0 0,First,#,adm0_lines,country2,0,65535;rank \"rank\" true true false 8 Double 0 0,First,#,adm0_lines,rank,-1,-1;label \"label\" true true false 65536 Text 0 0,First,#,adm0_lines,label,0,65535;status \"status\" true true false 65536 Text 0 0,First,#,adm0_lines,status,0,65535;notes \"notes\" true true false 65536 Text 0 0,First,#,adm0_lines,notes,0,65535;wld_date \"wld_date\" true true false 8 Date 0 0,First,#,adm0_lines,wld_date,-1,-1;wld_update \"wld_update\" true true false 8 Date 0 0,First,#,adm0_lines,wld_update,-1,-1;wld_land \"wld_land\" true true false 65536 Text 0 0,First,#,adm0_lines,wld_land,0,65535;wld_view \"wld_view\" true true false 65536 Text 0 0,First,#,adm0_lines,wld_view,0,65535")

    # Process: Near (Near) (analysis)
    Updated_Input_Features = arcpy.analysis.Near(in_features=tza_adm2_1967_FeatureToPoint, near_features=[UgandanBorder])[0]

    # Process: Join Field (Join Field) (management)
    tza_adm2_1967 = arcpy.management.JoinField(in_data=tza_adm2_1967_2_, in_field="distname19", join_table=Updated_Input_Features, join_field="distname19", fields=["NEAR_DIST"])[0]

    # Convert feature class to pandas DataFrame
    fields = [f.name for f in arcpy.ListFields(tza_adm2_1967)]
    data = [row for row in arcpy.da.SearchCursor(tza_adm2_1967, fields)]
    df = pd.DataFrame(data, columns=fields)

    # Export DataFrame to Excel
    df.to_excel(DistanceToUgandan_xlsx, index=False)



# Run the function
DistancetoUgandan()
