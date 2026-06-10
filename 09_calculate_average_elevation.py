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

def elevation():  # Model

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    tza_adm2_1967_shp = os.path.join(input_dir, "tza_adm2_1967",  "tza_adm2_1967.shp")
    gt30e020n40_tif = os.path.join(input_dir, "elevation", "gt30e020n40.tif")
    gt30e020s10_tif = os.path.join(input_dir, "elevation", "gt30e020s10.tif")
    tza_border_dir = os.path.join(process_dir, "tza_border")
    tza_border_shp = os.path.join(tza_border_dir, "tza_border.shp")
    
    elevation_dir = os.path.join(process_dir, "elevation")
    elevation_tif = os.path.join(elevation_dir, "elevation.tif")

    elevation_Clip_dir = os.path.join(process_dir, "elevation_Clip")
    elevation_Clip_tif = os.path.join(elevation_Clip_dir, "elevation_Clip.tif")

    elevation_statis_dir = os.path.join(process_dir, "elevation_statis")
    elevation_statis = os.path.join(elevation_statis_dir, "elevation_statis.dbf")

    elevation_xlsx_dir = os.path.join(output_dir, "elevation")
    elevation_xlsx = os.path.join(elevation_xlsx_dir, "elevation.xlsx")


    # Create directories if they don't exist
    os.makedirs(elevation_dir, exist_ok=True)
    os.makedirs(elevation_Clip_dir, exist_ok=True)
    os.makedirs(elevation_statis_dir, exist_ok=True)
    os.makedirs(elevation_xlsx_dir, exist_ok=True)

    # Process: Mosaic To New Raster (Mosaic To New Raster) (management)
    elevation_tif = arcpy.management.MosaicToNewRaster(input_rasters=[gt30e020n40_tif, gt30e020s10_tif], output_location=elevation_dir, raster_dataset_name_with_extension="elevation.tif", coordinate_system_for_the_raster="PROJCS[\"WGS_1984_UTM_Zone_37S\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",10000000.0],PARAMETER[\"Central_Meridian\",39.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", pixel_type="16_BIT_SIGNED", number_of_bands=1)[0]
    elevation_tif = arcpy.Raster(elevation_tif)

    # Process: Clip Raster (Clip Raster) (management)
    arcpy.management.Clip(in_raster=elevation_tif, rectangle="29.5895292580001 -11.7623492139999 40.4447348230001 -0.983143016999922", out_raster=elevation_Clip_tif, in_template_dataset=tza_border_shp, clipping_geometry="ClippingGeometry")
    elevation_Clip_tif = arcpy.Raster(elevation_Clip_tif)

    # Process: Zonal Statistics as Table (Zonal Statistics as Table) (ia)
    Output_Join_Layer = ""
    arcpy.ia.ZonalStatisticsAsTable(tza_adm2_1967_shp, "distname19", elevation_Clip_tif, elevation_statis, "DATA", "ALL", "CURRENT_SLICE", [90], "AUTO_DETECT", "ARITHMETIC", 360, Output_Join_Layer)



    # Export DataFrame to Excel
    dbf = Dbf5(elevation_statis)
    df = dbf.to_dataframe()
    df.to_excel(elevation_xlsx, index=False)

    
# Run the function
elevation()
    
    

