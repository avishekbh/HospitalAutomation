
# Importing modules for reading CSV files, running the OS command CURL and writing to XML file
import csv
import os
import sys
import logging
import glob # For reading only *.csv files in the directory
import xml.etree.cElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('update.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

# Changing the directory to the directory where the CSV file is kept
#os.chdir('/home/obhi/Documents')

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
    for filename in glob.glob('*.csv'):
        try:
            with open(filename, 'rb') as f:
                csvfile = csv.reader(f)
                for row in csvfile:
                    if flag == 0:
                    	for r in row :
                        	print r
                    elif flag == 1:
                    	for r in row :
                        	print r
                    elif row[4] == "Last_Update":
                        flag = 1
        except:
            e = sys.exc_info()[0]
            logger.debug("Error in reading files ::Message:: "+e)

        dataValueSet = ET.Element("dataValueSet")
        dataValueSet.set("xmlns", "http://dhis2.org/schema/dxf/2.0")
        dataValueSet.set("dataSet", "dataSetID")
        dataValueSet.set("completeDate", "date")
        dataValueSet.set("period", "period")
        dataValueSet.set("orgUnit", "orgUnitID")

        dataValue = ET.SubElement(dataValueSet, "dataValue")
        dataValue.set("dataElement", "dataElementID")
        dataValue.set("value", "1")

        dataValue = ET.SubElement(dataValueSet, "dataValue")
        dataValue.set("dataElement", "dataElementID")
        dataValue.set("value", "2")

        indent(dataValueSet)
        tree = ET.ElementTree(dataValueSet)
        filename = filename.rstrip(".csv")
        xml_file = filename+".xml"
        tree.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")

        #TODO Add the hospital name in the logfile

        os.system("curl -d @"+xml_file+" ""http://180.149.243.107:8080"" -H ""Content-Type:application/xml"" -u admin:district -v")


if __name__ == '__main__':
    reader_writer_sender()
