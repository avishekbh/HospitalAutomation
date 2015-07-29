__author__ = 'obhi'
# Importing modules for reading CSV files, running the OS command CURL and writing to XML file
import csv
import os
import sys
import logging
import glob  # For reading only *.csv files in the directory
import xml.etree.cElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('update.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


# Changing the directory to the directory where the CSV file is kept
# os.chdir('/home/obhi/Documents')

def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def reader_writer_sender():
    flag = 0
    hospitals =   {
        'peerless' : {'hosp_dets' : {'dataSet':"C6ciemRdZvd", 'orgUnit': "o3Fdcxep773"},
                      'ITU' : {'Total': "dToLU495hdD" , 'Reserved' : "WtlxTsYjvFO" , 'Occupied' : "HSSL9CQCEmu" ,'Available' : "rNdaHxXE13d"},
                      'ICCU' : {'Total': "SRYSn6KiUgs" , 'Reserved' : "ix8dVgFAqbv" , 'Occupied' : "z5PMfjPOeaU" ,'Available' : "jW487vss0PK"},
                      'NICU' : {'Total': "U97U38U2eBj" , 'Reserved' : "ys96ilizEcV" , 'Occupied' : "IAXlkWdrypq" ,'Available' : "MRCwMGNQOpg"},
                      },
        'bellevue' : {'hosp_dets' : {'dataSet':"L3NTA4t5LPS", 'orgUnit': "iNwzBcDqGsY"},
                      'CCU' : {'Total' : "G8RVMxO86Qc" , 'Reserved' : "GgULTaSUMBS" ,'Occupied' : "MhRIygQBvbx" , 'Available' : "brszB1hGZeG"},
                      'ITU' : {'Total': "dToLU495hdD" , 'Reserved' : "WtlxTsYjvFO" , 'Occupied' : "HSSL9CQCEmu" ,'Available' : "rNdaHxXE13d"},
                      'ICCU' : {'Total': "SRYSn6KiUgs" , 'Reserved' : "ix8dVgFAqbv" , 'Occupied' : "z5PMfjPOeaU" ,'Available' : "jW487vss0PK"},
                      'ICU-I' : {'Total' : "JXGDUZUxfC1" , 'Reserved' : "XJnDJzbnxIS" , 'Occupied' : "VEV5SQ3o4Cl" ,'Available' : "OJFT7dJ6UoL"},
                      'CTVS' : {'Total' : "B3zytjeLBkC" , 'Reserved' : "noOQUiGuYnC" , 'Occupied' : "dG9IYWemUNa" ,'Available' : "cZFZarClUkB"},
                      'NICU' : {'Total': "U97U38U2eBj" , 'Reserved' : "ys96ilizEcV" , 'Occupied' : "IAXlkWdrypq" ,'Available' : "MRCwMGNQOpg"},
                      'SCBU' : {'Total' : "zDEFJIDCUjb" ,'Reserved' : "XqBI7j0SNWg" ,'Occupied' : "oF9zVVtGBz9" ,'Available' : "dCGFxlOVlwg"}
                      }
    }
    bed_info = ['Total', 'Reserved', 'Occupied', 'Available']

    for filename in glob.glob('*.csv'):
        try:
            with open(filename, 'rb') as f:
                hos_name = "null"
                flag = 0
                csvfile = csv.reader(f)
                dataValueSet = ET.Element("dataValueSet")
                dataValueSet.set("xmlns", "http://dhis2.org/schema/dxf/2.0")

                for key in hospitals:
                    if key in filename:
                        hos_name=key
                        dataValueSet.set("dataSet", hospitals[hos_name]['hosp_dets']['dataSet'])
                        dataValueSet.set("orgUnit", hospitals[hos_name]['hosp_dets']['orgUnit'])
                    else:
                        logger.debug("The filename sent by hospital does not exist")
                        quit()

                for row in csvfile:
                    index = 1
                    if row[0] == "#":
                        flag = 1
                        continue
                    bed_type = row[0]
                    dataValueSet.set("completeDate", row[4])
                    dataValueSet.set("period", row[4][:8])
                    for b in bed_info:
                        dataValue = ET.SubElement(dataValueSet, "dataValue")
                        dataValue.set("dataElement", hospitals[hos_name][bed_type][b])
                        if index == 4:
                            dataValue.set("value", str(int(row[1]) - int(row[2]) - int(row[3])))
                            break
                        else:
                            dataValue.set("value", row[index])
                        index += 1
        except:
            e = sys.exc_info()[0]
            logger.debug("Error in reading files ::Message:: " + str(e))
        if flag == 1:
            indent(dataValueSet)
            tree = ET.ElementTree(dataValueSet)
            filename = filename[:-4]
            xml_file = filename + ".xml"
            tree.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")
            os.system("curl -d @" +xml_file+ " ""http://180.149.243.107:8080/api/dataValueSets"" -H ""Content-Type:application/xml"" -u admin:district -v")

            # TODO Add the hospital name in the logfile


if __name__ == '__main__':
    reader_writer_sender()
