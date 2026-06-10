
import arcpy
from arcpy.sa import *
import os


# Set working directory
# current_file_path = os.path.abspath(__file__)
current_file_path = os.getcwd()
base_dir = f"gis_input"

input_dir = os.path.join(current_file_path,base_dir, "input","rainfallstations")
output_dir = os.path.join(current_file_path,base_dir, "output","rainfall")
process_dir = os.path.join(current_file_path,base_dir, "process","rainfallstations")

# Create directories if they don't exist
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(process_dir, exist_ok=True)


def csv_to_points(input_folder, output_folder):
    arcpy.env.overwriteOutput = True

    # Iterate through each year from 1960 to 2010
    for year in range(1960, 2011):
        # Construct the CSV file path for the current year
        csv_filename = f"rainfall_{year}.csv"
        csv_path = os.path.join(input_folder, csv_filename)
        
        # Construct the output shapefile path for the current year
        output_shp_name = f"rainfall_{year}_XYTableToPoint.shp"
        output_shp_path = os.path.join(output_folder, output_shp_name)

        # Perform XY Table To Point conversion
        arcpy.management.XYTableToPoint(in_table=csv_path,
                                        out_feature_class=output_shp_path,
                                        x_field="longitude",
                                        y_field="latitude",
                                        coordinate_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

if __name__ == '__main__':

    # Call the function to convert CSV files to points
    csv_to_points(input_dir, process_dir)


# Define the shape file and its fields
tza_adm2_1967_shp = "gis_input/input/tza_adm2_1967/tza_adm2_1967.shp"

# Month names for iterating
months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

# Dictionary mapping month names to z_field names
z_fields = {
    "jan": "rainfall_j", "feb": "rainfall_f", "mar": "rainfall_m", "apr": "rainfall_a", "may": "rainfall_1", "jun": "rainfall_2", "jul": "rainfall_3", "aug": "rainfall_4", "sep": "rainfall_s", "oct": "rainfall_o", "nov": "rainfall_n", "dec": "rainfall_d" }

def rainfall(year, month_name):
    arcpy.env.overwriteOutput = True
    
    in_features = os.path.join(process_dir, f"rainfall_{year}_XYTableToPoint.shp")
    z_field = z_fields[month_name]
    out_tif = os.path.join(process_dir, f"rainfall_{month_name}_{year}.tif")
    out_table = os.path.join(process_dir, f"rainfall_{month_name}_{year}")

    # Kriging (Kriging) (3d)
    arcpy.ddd.Kriging(in_point_features=in_features, z_field=z_field, out_surface_raster=out_tif, semiVariogram_props="Gaussian 0.039320 # # #", out_variance_prediction_raster="")
    out_tif = arcpy.Raster(out_tif)

    # Zonal Statistics as Table
    arcpy.sa.ZonalStatisticsAsTable(tza_adm2_1967_shp, "distname19", out_tif, out_table, "DATA", "MEAN")

    # Table To dBASE
    output_dbf = os.path.join(output_dir, f"rainfall_{month_name}_{year}.dbf")
    arcpy.conversion.TableToDBASE(Input_Table=[out_table], Output_Folder=output_dir)

# Main loop to process all years and months
for year in range(1960, 2011):
    for month_name in months:
        rainfall(year, month_name)


