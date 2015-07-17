
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
    for filename in glob.glob('*.csv'):
        print filename
        if "peerless" in filename:
            try:
                with open(filename, 'rb') as f:
                    i=0
                    csvfile = csv.reader(f)
                    dataValueSet = ET.Element("dataValueSet")
                    dataValueSet.set("xmlns", "http://dhis2.org/schema/dxf/2.0")
                    dataValueSet.set("dataSet", "C6ciemRdZvd")
                    dataValueSet.set("orgUnit", "o3Fdcxep773")
                    for row in csvfile:
                        dataValueSet.set("completeDate", row[3])
                        dataValueSet.set("period", row[3][:8])
                        if i==1:
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "SRYSn6KiUgs")
                            dataValue.set("value", row[1])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "z5PMfjPOeaU")
                            dataValue.set("value", row[2])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "jW487vss0PK")
                            dataValue.set("value", str(int(row[1]) - int(row[2])))
                        elif i==2:
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "U97U38U2eBj")
                            dataValue.set("value", row[1])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "IAXlkWdrypq")
                            dataValue.set("value", row[2])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "MRCwMGNQOpg")
                            dataValue.set("value", str(int(row[1]) - int(row[2])))
                        elif i==0:
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "dToLU495hdD")
                            dataValue.set("value", row[1])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "HSSL9CQCEmu")
                            dataValue.set("value", row[2])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "rNdaHxXE13d")
                            dataValue.set("value", str(int(row[1]) - int(row[2])))
                        i=i+1
            except:
                e = sys.exc_info()[0]
                logger.debug("Error in reading files ::Message:: " + str(e))
        elif "belle" in filename:
            try:
                with open(filename, 'rb') as f:
                    i=0    
                    csvfile = csv.reader(f)
                    dataValueSet = ET.Element("dataValueSet")
                    dataValueSet.set("xmlns", "http://dhis2.org/schema/dxf/2.0")
                    dataValueSet.set("dataSet", "L3NTA4t5LPS")
                    dataValueSet.set("orgUnit", "iNwzBcDqGsY")
                    for row in csvfile:
                        dataValueSet.set("completeDate", row[3])
                        dataValueSet.set("period", row[3][:8])
                        if i==1:
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "SRYSn6KiUgs")
                            dataValue.set("value", row[1])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "z5PMfjPOeaU")
                            dataValue.set("value", row[2])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "jW487vss0PK")
                            dataValue.set("value", str(int(row[1]) - int(row[2])))
                        elif i==2:
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "U97U38U2eBj")
                            dataValue.set("value", row[1])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "IAXlkWdrypq")
                            dataValue.set("value", row[2])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "MRCwMGNQOpg")
                            dataValue.set("value", str(int(row[1]) - int(row[2])))
                        elif i==0:
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "dToLU495hdD")
                            dataValue.set("value", row[1])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "HSSL9CQCEmu")
                            dataValue.set("value", row[2])
                            dataValue = ET.SubElement(dataValueSet, "dataValue")
                            dataValue.set("dataElement", "rNdaHxXE13d")
                            dataValue.set("value", str(int(row[1]) - int(row[2])))
                        i=i+1
            except:
                e = sys.exc_info()[0]
                logger.debug("Error in reading files ::Message:: " + str(e))
        indent(dataValueSet)
        tree = ET.ElementTree(dataValueSet)
        filename = filename[:-4]
        xml_file = filename + ".xml"
        tree.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")


        #TODO Add the hospital name in the logfile

        os.system("curl -d @"+xml_file+" ""http://180.149.243.107:8080"" -H ""Content-Type:application/xml"" -u admin:district -v")


if __name__ == '__main__':
    reader_writer_sender()
