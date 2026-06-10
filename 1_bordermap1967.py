
import arcpy
import os


# Set working directory
# Modify the paths as needed
base_dir = "/Users/YAWEN L/Dropbox/GIS_Yawen/gis_input"
    
input_dir = os.path.join(base_dir, "input")
output_dir = os.path.join(base_dir, "output")
process_dir = os.path.join(base_dir, "process")


def bordermap1967():  # Define bordermap1967 function

    # Allow overwriting output files
    arcpy.env.overwriteOutput = True

    # Define input and output paths
    tza_admbnda_adm2_20181019_2_ = os.path.join(input_dir, "tza_admbnda_adm2_20181019", "tza_admbnda_adm2_20181019.shp")
    directory_csv = os.path.join(input_dir, "directory.csv")

    admin_dissolve_projected_dir = os.path.join(process_dir, "admin_dissolve_projected")
    admin_dissolve_projected_shp = os.path.join(admin_dissolve_projected_dir, "admin_dissolve_projected.shp")
    
    tza_adm2_1967_dir = os.path.join(output_dir, "tza_adm2_1967")
    tza_adm2_1967_shp = os.path.join(tza_adm2_1967_dir, "tza_adm2_1967.shp")

    # Create output subdirectory if it doesn't exist
    os.makedirs(tza_adm2_1967_dir, exist_ok=True)

    # Process: Join Field
    tza_admbnda_adm2_20181019 = arcpy.management.JoinField(
        in_data=tza_admbnda_adm2_20181019_2_,
        in_field="ADM2_EN",
        join_table=directory_csv,
        join_field="id_dist_name_16_boundaries",
        fields=["distname1967"]
    )[0]

    # Process: Dissolve
    arcpy.management.Dissolve(in_features=tza_admbnda_adm2_20181019, out_feature_class=admin_dissolve_projected_shp, dissolve_field=["distname19"])

    # Process: Project (Project) (management)
    arcpy.management.Project(in_dataset=admin_dissolve_projected_shp, out_dataset=tza_adm2_1967_shp, out_coor_system="PROJCS[\"WGS_1984_UTM_Zone_37S\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",10000000.0],PARAMETER[\"Central_Meridian\",39.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]")

    
# Run the function
bordermap1967()

