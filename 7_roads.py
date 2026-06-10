import arcpy
import os
import pandas as pd


# Set working directory
base_dir = "/Users/YAWEN L/Dropbox/GIS_Yawen/gis_input"

input_dir = os.path.join(base_dir, "input")
output_dir = os.path.join(base_dir, "output")
process_dir = os.path.join(base_dir, "process")


def roads():  # roads

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    tza_adm2_1967 = os.path.join(input_dir, "tza_adm2_1967", "tza_adm2_1967.shp")
    roads_1968_projected = os.path.join(input_dir, "roads", "roads_1968_projected.shp")

    roads_districts_intersect_dir = os.path.join(process_dir, "roads_districts_intersect")
    roads_districts_intersect_shp = os.path.join(roads_districts_intersect_dir, "roads_districts_intersect.shp")

    roads_totallength_dir = os.path.join(process_dir, "roads_totallength")
    roads_totallength_dbf = os.path.join(roads_totallength_dir, "roads_totallength.dbf")

    length_of_road_dir = os.path.join(output_dir, "length_of_roads")
    length_of_road_xlsx =  os.path.join(length_of_road_dir, "length of roads.xlsx")


    # Create directories if they don't exist
    os.makedirs(roads_districts_intersect_dir, exist_ok=True)
    os.makedirs(roads_totallength_dir, exist_ok=True)
    os.makedirs(length_of_road_dir, exist_ok=True)
    

    # Process: Intersect (Intersect) (analysis)
    arcpy.analysis.Intersect(in_features=[[tza_adm2_1967, ""], [roads_1968_projected, ""]], out_feature_class=roads_districts_intersect_shp, join_attributes="ALL", output_type="LINE")

    # Process: Add Field (Add Field) (management)
    roads_districts_intersect_shp_4_ = arcpy.management.AddField(in_table=roads_districts_intersect_shp, field_name="lth_divi", field_type="FLOAT")[0]

    # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
    roads_districts_intersect_shp_2_ = arcpy.management.CalculateGeometryAttributes(in_features=roads_districts_intersect_shp_4_, geometry_property=[["lth_divi", "LENGTH_GEODESIC"]], length_unit="KILOMETERS")[0]

    # Process: Summary Statistics (Summary Statistics) (analysis)
    arcpy.analysis.Statistics(in_table=roads_districts_intersect_shp_2_, out_table=roads_totallength_dbf, statistics_fields=[["lth_divi", "SUM"]], case_field=["distname19"])

    # Read the Zonal Statistics table into a pandas DataFrame
   
    fields = ["distname19", "SUM_lth_divi"]
    data = []
    with arcpy.da.SearchCursor(roads_totallength, fields) as cursor:
        for row in cursor:
            data.append(row)

    # Create a DataFrame
    df = pd.DataFrame(data, columns=fields)

    # Export DataFrame to Excel
    df.to_excel(length_of_road_xlsx, index=False)

# Run the function
roads()


    
