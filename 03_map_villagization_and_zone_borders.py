
import arcpy
import os

# Set working directory
# Modify the paths as needed
base_dir = "/Users/YAWEN L/Dropbox/GIS_Yawen/gis_input"
    
input_dir = os.path.join(base_dir, "input")
output_dir = os.path.join(base_dir, "output")
process_dir = os.path.join(base_dir, "process")


def villagization():  # villagization

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True



    #1 vlllagization figure
    
    # Define input and output paths
    tza_adm2_1967_2_ = os.path.join(input_dir, "tza_adm2_1967",  "tza_adm2_1967.shp")
    treatment_formap_clean_csv = os.path.join(input_dir, "treatment_formap_clean.csv")
    tza_admbnda_adm2_20181019_shp_2_ = os.path.join(input_dir, "tza_admbnda_adm2_20181019", "tza_admbnda_adm2_20181019.shp")
    directory_csv = os.path.join(input_dir, "directory.csv")
    tza_zoneborder_dir = os.path.join(output_dir, "tza_zoneborder")

    # Process: Join Field (Join Field) (management)
    tza_adm2_1967 = arcpy.management.JoinField(in_data=tza_adm2_1967_2_, in_field="distname19", join_table=treatment_formap_clean_csv, join_field="id_dist_name_67", fields=["c78_treatment_dist67"])[0]

    

    #2 zone border

    # Define input and output paths
    tza_admbnda_adm2_20181019_shp_2_ = os.path.join(input_dir, "tza_admbnda_adm2_20181019", "tza_admbnda_adm2_20181019.shp")
    directory_csv = os.path.join(input_dir, "directory.csv")
    tza_zoneborder_dir = os.path.join(output_dir, "tza_zoneborder")
    tza_zoneborder_shp = os.path.join(tza_zoneborder_dir, "tza_zoneborder.shp")

    # Create directories if they don't exist
    os.makedirs(tza_zoneborder_dir, exist_ok=True)

    # Process: Join Field (2) (Join Field) (management)
    tza_admbnda_adm2_20181019_shp = arcpy.management.JoinField(in_data=tza_admbnda_adm2_20181019_shp_2_, in_field="ADM2_EN", join_table=directory_csv, join_field="id_dist_name_16_boundaries", fields=["zonename"])[0]

    # Process: Dissolve (Dissolve) (management)
    arcpy.management.Dissolve(in_features=tza_admbnda_adm2_20181019_shp, out_feature_class=tza_zoneborder_shp, dissolve_field=["zonename"])

    
    

# Run the function
villagization()





# Make the graphic map

# Get the current project
#aprx = arcpy.mp.ArcGISProject("CURRENT")

# Create a new layout
#layout = aprx.createLayout(page_width=21, page_height=29.7, page_units="CENTIMETER", name="villagization_map")

# Define input and output paths
#tza_adm2_1967 = os.path.join(input_dir, "tza_adm2_1967",  "tza_adm2_1967.shp")

# Add layers 
#map_frame = layout.listElements('MAPFRAME_ELEMENT')[0]
#layers = map_frame.map.listLayers()


# Save the project
#aprx.save()

