# path to project folder C:\Users\alexw\GIS\QGIS\SDPRF
import os
from qgis.core import *

QgsProject.instance().removeAllMapLayers()
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
# QgsProject.instance().addMapLayer(vlayer_join)
QgsVectorFileWriter.writeAsVectorFormat(vlayer_join, output_uri ,'utf-8', driverName="CSV")
print("output saved to {}".format(output_uri))

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()