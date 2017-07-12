import xml.etree.ElementTree as ET

def xmlToArray(xml):
    array_data = {}
    root = ET.fromstring(xml)
    for child in root:
        value = child.text
        array_data[child.tag] = value
    return array_data


def arrayToXml(arr):
    """array转xml"""
    xml = ["<xml>"]
    a = dict()
    for k, v in arr.items():
        xml.append("<{0}>{1}</{0}>".format(k, v))
        # if v.isdigit():
        #     xml.append("<{0}>{1}</{0}>".format(k, v))
        # else:
        #     xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
    xml.append("</xml>")
    return "".join(xml)