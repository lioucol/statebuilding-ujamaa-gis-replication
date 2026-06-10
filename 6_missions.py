import arcpy
import os
import pandas as pd
from simpledbf import Dbf5


# Set working directory
# Modify the paths as needed
base_dir = "/Users/YAWEN L/Dropbox/GIS_Yawen/gis_input"
    
input_dir = os.path.join(base_dir, "input")
output_dir = os.path.join(base_dir, "output")
process_dir = os.path.join(base_dir, "process")


def missions():  # missions

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True
   
    # Define input and output feature classes with relative paths
    bj_missions = os.path.join(input_dir, "bj_missions", "bj_missions.shp")
    tza_adm2_1967 = os.path.join(input_dir, "tza_adm2_1967", "tza_adm2_1967.shp")
    
    tza_adm2_1967_SpatialJoin_dir = os.path.join(process_dir, "tza_adm2_1967_SpatialJoin")
    tza_adm2_1967_SpatialJoin = os.path.join(tza_adm2_1967_SpatialJoin_dir, "tza_adm2_1967_SpatialJoin.shp")
    tza_adm2_1967_Spa_Statistics_dir = os.path.join(process_dir, "tza_adm2_1967_Spa_Statistics")
    tza_adm2_1967_Spa_Statistics = os.path.join(tza_adm2_1967_Spa_Statistics_dir, "tza_adm2_1967_Spa_Statistics.shp")
    Number_of_Missions_dir = os.path.join(output_dir, "Number of Missions")
    Number_of_Missions_xlsx = os.path.join(Number_of_Missions_dir, "Number of Missions.xlsx")

     # Create directories if they don't exist
    os.makedirs(tza_adm2_1967_SpatialJoin_dir, exist_ok=True)
    os.makedirs(tza_adm2_1967_Spa_Statistics_dir, exist_ok=True)
    os.makedirs(Number_of_Missions_dir, exist_ok=True)
    

    # Process: Select Layer By Location (Select Layer By Location) (management)
    bj_missions_2_, Output_Layer_Names, Count = arcpy.management.SelectLayerByLocation(in_layer=[bj_missions], select_features=tza_adm2_1967)

    # Process: Spatial Join (Spatial Join) (analysis)
    arcpy.analysis.SpatialJoin(target_features=tza_adm2_1967, join_features=bj_missions_2_, out_feature_class=tza_adm2_1967_SpatialJoin, join_operation="JOIN_ONE_TO_MANY", field_mapping="distname19 \"distname19\" true true false 254 Text 0 0,First,#,tza_adm2_1967,distname19,0,253;NEAR_DIST \"DistToCapital\" true true false 19 Double 0 0,First,#,tza_adm2_1967,NEAR_DIST,-1,-1;c78_treatm \"villagization\" true true false 19 Double 0 0,First,#,tza_adm2_1967,c78_treatm,-1,-1;NEAR_DIS_1 \"DistToUgandan\" true true false 19 Double 0 0,First,#,tza_adm2_1967,NEAR_DIS_1,-1,-1;xcoord \"xcoord\" true true false 24 Double 15 23,First,#,bj_missions,xcoord,-1,-1;ycoord \"ycoord\" true true false 24 Double 15 23,First,#,bj_missions,ycoord,-1,-1;denom \"denom\" true true false 80 Text 0 0,First,#,bj_missions,denom,0,79;vacated \"vacated\" true true false 80 Text 0 0,First,#,bj_missions,vacated,0,79")

    # Process: Summary Statistics (Summary Statistics) (analysis)
    arcpy.analysis.Statistics(in_table=tza_adm2_1967_SpatialJoin, out_table=tza_adm2_1967_Spa_Statistics, statistics_fields=[["Join_Count", "COUNT"]], case_field=["distname19"])

    # Read the Zonal Statistics table into a pandas DataFrame
    fields = ["distname19", "FREQUENCY"]
    data = []
    with arcpy.da.SearchCursor(tza_adm2_1967_Spa_Statistics, fields) as cursor:
        for row in cursor:
            data.append(row)

    # Create a DataFrame
    df = pd.DataFrame(data, columns=fields)

    # Export DataFrame to Excel
    df.to_excel(Number_of_Missions_xlsx, index=False)


# Run the function
missions()

