#   Python3 script to parse Jeep Gladiator Infotainment Locations

# This data set was collected from a Jeep Gladiator infotainment system that underwent a chipoff extraction.
# The file system on the chip was QNX6.  Linux was used to convert the filesystem resulting in multiple partitions 
# becoming available. Relevant logs were found in 'loop13p13/archivedata/M_3588_20230424_062538_STOP_1957C005277B01F4F92156DB76B299A1.tar.gz' type paths
#
# Folder contents:
# pas_bootmicro_log.1		
# pas_sloginfo.log
# pas_debug.log.1			*this has the geo data
# pas_system.1.1.0.csv
# pas_performance.1.0.0.log

# This script will iterate through the folder and subfolders to find responsive log files.  It will find latitude and longitude values and add them to a CSV formatted report that provides the 
# date and time, latitude, and longitude.

#   Sample data for testing
# 04/02/2023 19:25:07.008/14023/30/nv_location/LocProxyWorker_1/fstoreGPS/712/=Some GPS data are discarded. storeGPS = 0x20
# 04/05/2023 19:25:07.008/14024/30/nv_location/LocProxyWorker_1/getDataPosllh/1061/=GPS Data->Long:90.217232,Latt:32.284225,NavDataStore->Long:-93.217232,Latt:22.284225,data->bStatus:1
# 04/05/2023 19:25:07.008/14025/30/nv_location/LocProxyWorker_1/getDataAlt/1108/=GPSData[latestGPS].status.geoid:89.599998, GPSData[latestGPS].status.WGS:-27.000000, data->iEllipsoidAltitude:62600, data->iAltitude:89600
# 04/15/2023 19:25:07.695/20046/30/nv_navigation/NaviWorkerHighest_2/void SI_GPSData::convertLocationData(const NV_tLocation&)/1014/=INF: f_locaction_info : Altitude.iAltitude:[89500], Altitude.iEllipsoidAltitude:[62600], Position.dLatitude:[-43.284261], Position.dLongitude:[-91.217197], eFix_Type:[7], Heading.iHeading:[80000], GPS_Health.ui16Hdop:[200], GPS_Health.ui16Vdop:[200], GPS_Health.ui16Pdop:[200], Position.uiAccuracy:[3540], GPS_Health.ui8NumberOfSatellitesUsedInFix:[8], GPS_Health.ui8NumberOfSatellitesInView:[11], Speed.uiSpeed:[500], ui8SyncCounter:[231]
# 04/30/2023 19:25:07.698/20054/28/nv_navigation/main/CI->SI Log/312/=[19:25:07.698         panaAPI notice -                               ] Map match result for data [231]: lat: 22.284260, lon: -93.217258, heading: 359.693749




import os
import re
import datetime

now = datetime.datetime.now()
now = now.strftime("%Y%m%d_%H%M%S")

folder = ###    PUT TARGET FOLDER HERE  ###
report = folder + "/report_" + now + ".csv"

dateregex = re.compile("(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2}):(\d{2})\.(\d{3})")
latituderegex = re.compile("(lat: (|-)(\d{2}).(\d{6}))|(dLatitude:\[((|-)\d{2}).(\d{6})\])|Latt:(|-)(\d{2}).(\d{6})|(Latitude = (|-)(\d{2}).(\d{6}))")
longituderegex = re.compile("lon: (|-)(\d{2}).(\d{6})|(dLongitude:\[(|-)(\d{2}).(\d{6})\])|Long:(|-)(\d{2}).(\d{6})|(Longitude = (|-)(\d{2}).(\d{6}))")
headingregex = re.compile("heading: (\d{2}).(\d{6})")

lines_w_lat_long = []

#   walks target folder and finds the debug logs containing lat and longs
def walk_directories(input_folder):
    for root, dirs, files in os.walk(input_folder):      # walks folders and subfolders
        # print(files)
        for filename in files:
            if filename == "pas_debug.log.1":
                print(os.path.join(root,filename))
                with open(os.path.join(root,filename), 'r',errors='ignore') as log2parse:
                    lines = log2parse.readlines()
                    for line in lines:          
                        if "lat:" in line:
                            lines_w_lat_long.append(line)

# regex search and formatting result to add to csv
def parse_lines_w_lat_long(list_of_lines):
    for t in (list_of_lines):
        founddate = (re.search(dateregex,t))
        foundlat = re.search(latituderegex,t)
        foundlong = re.search(longituderegex,t)
        date = founddate.group(0)
        lat = (foundlat.group(0)).split(" ")
        # print(lat[1])
        long = (foundlong.group(0)).split(" ")
        # print(long[1])
        report.write("'" + date + "'" + "," + lat[1] + "," + long[1] + "\n")
       
####### Run the thing! ######

with open(report, 'a') as report:
    report.write("Date," + "LATITUDE," + "LONGITUDE\n")

    walk_directories(folder)
    
    parse_lines_w_lat_long(lines_w_lat_long)
