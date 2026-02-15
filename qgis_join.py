# How to run windows:
# C:/Users/alexw/AppData/Local/Programs/OSGeo4W/apps/Python312/python.exe qgis_join.py
import os, sys, pathlib, logging
from config import get_current_raft_date, config

prefix_path = config['qgis_prefix_path']
# Append QGIS Python library and plugins to python search path
sys.path.append(config['qgis_python_path'])
sys.path.append(config['qgis_plugin_path'])

# import qgis
from qgis.core import *
logging.info('qgis bootstrap successful!')

# Supply path to qgis install location
QgsApplication.setPrefixPath(prefix_path, True)

# # Create a reference to the QgsApplication.  Setting the
# # second argument to False disables the GUI.
qgs = QgsApplication([], False)

# # Load providers
qgs.initQgis()

# load the processing plugins
import processing
from processing.core.Processing import Processing
Processing.initialize()
logging.info('processing plugin bootstrap successful!')

# Begin trash join
project_uri = pathlib.Path(__file__).parent.resolve()
parcel_uri = os.path.join(project_uri, "templates", "river_parcels","ParcelUpdate1124.shp")
mappler_csv_uri = os.path.join(project_uri, "output", "Mappler.csv")
output_uri = os.path.join(project_uri, "output", get_current_raft_date().strftime('%m%d_table_AW.csv'))

if os.path.exists(parcel_uri):
    vlayer_parcels = QgsVectorLayer(parcel_uri, "SDRPF_Parcels", "ogr")
    QgsProject.instance().addMapLayer(vlayer_parcels)
else:
    logging.error("Oh no. Parcel file path invalid. Please recheck and try again")
    sys.exit(1)
    
if os.path.exists(mappler_csv_uri):
    mappler_csv_uri = "file:///" + mappler_csv_uri + "?delimiter=%s&crs=epsg:4326&xField=%s&yField=%s" % (",", "Longitude", "Latitude")
    vlayer_pins = QgsVectorLayer(mappler_csv_uri, "Trash_Pins", "delimitedtext")
    QgsProject.instance().addMapLayer(vlayer_pins)
else:
    logging.error("Oh no. CSV file path invalid. Please recheck and try again")
    sys.exit(1)

# http://gis.stackexchange.com/questions/133537/loading-csv-data-table-as-vector-layer-using-pyqgis
output = processing.run("native:joinattributesbylocation",{
    'DISCARD_NONMATCHING' : False,
    'INPUT' : vlayer_parcels,
    'JOIN' : vlayer_pins,
    'JOIN_FIELDS' : ['#','Latitude','Longitude','Site Name','Category','Bags of Trash','Comments','Image','uid','mid','is_data_view_flag','reg_datetime','edit_datetime','Date','Time','aws_s3_images','login_route_type','data_view_count','User Info'], 'METHOD' : 0, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'PREDICATE' : [0], 'PREFIX' : '' 
    })
vlayer_join = output['OUTPUT']

QgsVectorFileWriter.writeAsVectorFormat(vlayer_join, output_uri ,'utf-8', driverName="CSV")
logging.info("output saved to {}".format(output_uri))
# End trash join

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()