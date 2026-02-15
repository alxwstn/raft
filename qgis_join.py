# path to project folder C:\Users\alexw\GIS\QGIS\SDPRF
# How to run windows:
# C:/Users/alexw/AppData/Local/Programs/OSGeo4W/apps/Python312/python.exe qgis_join.py
prefix_path = 'C:/Users/alexw/AppData/Local/Programs/OSGeo4W/apps/qgis'
# How to run on windows: C:/Users/alexw/AppData/Local/Programs/OSGeo4W/apps/Python312/python.exe qgis_join.py 
import os, sys
# Append QGIS Python library and plugins to python search path
sys.path.append(prefix_path + '/python')
sys.path.append(prefix_path + '/python/plugins')

# Try the import
from qgis.core import *
print('qgis bootstrap successful!')

# Supply path to qgis install location
QgsApplication.setPrefixPath(prefix_path, True)

# # Create a reference to the QgsApplication.  Setting the
# # second argument to False disables the GUI.
qgs = QgsApplication([], False)

# # Load providers
qgs.initQgis()

import processing
from processing.core.Processing import Processing
Processing.initialize()
print('processing bootstrap successful!')

parcel_uri = "C:/Users/alexw/GIS/QGIS/SDPRF/River Parcels/ParcelUpdate1124.shp"
mappler_csv_uri = "C:/Users/alexw/GIS/QGIS/SDPRF/Mappler CSVs/sandiegorivertrash_data(2025-12-19).csv"
if os.path.exists(parcel_uri):
    vlayer_parcels = QgsVectorLayer(parcel_uri, "SDRPF_Parcels", "ogr")
    QgsProject.instance().addMapLayer(vlayer_parcels)
else:
    print("Oh no. Parcel file path invalid. Please recheck and try again")
    
if os.path.exists(mappler_csv_uri):
    mappler_csv_uri = "file:///" + mappler_csv_uri + "?delimiter=%s&crs=epsg:4326&xField=%s&yField=%s" % (",", "Longitude", "Latitude")
    vlayer_pins = QgsVectorLayer(mappler_csv_uri, "Trash_Pins", "delimitedtext")
    QgsProject.instance().addMapLayer(vlayer_pins)
else:
    print("Oh no. Parcel file path invalid. Please recheck and try again")
# http://gis.stackexchange.com/questions/133537/loading-csv-data-table-as-vector-layer-using-pyqgis
output = processing.run("native:joinattributesbylocation",{
    'DISCARD_NONMATCHING' : False,
    'INPUT' : vlayer_parcels,
    'JOIN' : vlayer_pins,
    'JOIN_FIELDS' : ['#','Latitude','Longitude','Site Name','Category','Bags of Trash','Comments','Image','uid','mid','is_data_view_flag','reg_datetime','edit_datetime','Date','Time','aws_s3_images','login_route_type','data_view_count','User Info'], 'METHOD' : 0, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'PREDICATE' : [0], 'PREFIX' : '' 
    })
vlayer_join = output['OUTPUT']
output_uri = "C:/Users/alexw/GIS/QGIS/SDPRF/Trash Joins/mmdd_table_AW.csv"

QgsVectorFileWriter.writeAsVectorFormat(vlayer_join, output_uri ,'utf-8', driverName="CSV")
print("output saved to {}".format(output_uri))

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()