
import arcpy
import os
import pandas as pd


# Set working directory
# Modify the paths as needed
base_dir = "/Users/YAWEN L/Dropbox/GIS_Yawen/gis_input"
    
input_dir = os.path.join(base_dir, "input")
output_dir = os.path.join(base_dir, "output")
process_dir = os.path.join(base_dir, "process")


def distancetocapital():  # distancetocapital function

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True
    

    # Define input and output paths
    tza_adm2_1967 = os.path.join(input_dir, "tza_adm2_1967",  "tza_adm2_1967.shp")
    tza_adm2_points_dir = os.path.join(process_dir, "tza_adm2_points")
    tza_adm2_points_shp = os.path.join(process_dir, "tza_adm2_points", "tza_adm2_points.shp")
    mizizima_dir = os.path.join(process_dir, "mizizima")
    mizizima_shp = os.path.join(process_dir, "mizizima", "mizizima.shp")
    DistanceToCapital_dir = os.path.join(output_dir, "DistanceToCapital")
    DistanceToCapital_xlsx = os.path.join(DistanceToCapital_dir, "DistanceToCapital.xlsx")

    # Create directories if they don't exist
    os.makedirs(tza_adm2_points_dir, exist_ok=True)
    os.makedirs(mizizima_dir, exist_ok=True)
    os.makedirs(DistanceToCapital_dir, exist_ok=True)

    # Process: Feature To Point (Feature To Point) (management)
    arcpy.management.FeatureToPoint(in_features=tza_adm2_1967, out_feature_class=tza_adm2_points_shp)

    # Process: Export Features (Export Features) (conversion)
    arcpy.conversion.ExportFeatures(
        in_features=tza_adm2_points_shp,
        out_features=mizizima_shp,
        where_clause="distname19 = 'Mzizima'",
        field_mapping=(
            f"distname19 \"distname19\" true true false 254 Text 0 0,First,#,"
            f"{tza_adm2_points_shp},distname19,0,253;ORIG_FID \"ORIG_FID\" true true false 0 Long 0 0,First,#,"
            f"{tza_adm2_points_shp},ORIG_FID,-1,-1"
        )
    )

    # Process: Near (Near) (analysis)
    tza_adm2_points_shp_2_ = arcpy.analysis.Near(in_features=tza_adm2_points_shp, near_features=[mizizima_shp])[0]


    # Process: Join Field (Join Field) (management)
    tza_adm2_1967_2_ = arcpy.management.JoinField(in_data=tza_adm2_1967, in_field="distname19", join_table=tza_adm2_points_shp_2_, join_field="distname19", fields=["NEAR_DIST"])[0]

    # Convert feature class to pandas DataFrame
    fields = [f.name for f in arcpy.ListFields(tza_adm2_points_shp_2_)]
    data = [row for row in arcpy.da.SearchCursor(tza_adm2_points_shp_2_, fields)]
    df = pd.DataFrame(data, columns=fields)

    # Export DataFrame to Excel
    df.to_excel(DistanceToCapital_xlsx, index=False)

   
# Run the function
distancetocapital()
