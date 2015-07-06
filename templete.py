from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml.etree import ElementTree
from xml.dom import minidom
import os
import sys

z_list=['CPU Load Average', 'Memory Usage', 'IOStat xvda Util-IO', 'Eth0 Network Traffic', 'Eth1 Network Traffic']
	
help='''python template.py $text_file $xml_file
$text_file formart
#######################################
~Customer - test
srv-test-lb1
srv-test-web1
srv-test-db1
######################################'''

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def check_arg():
	if len(sys.argv) != 3:
		print help
		sys.exit()
	
def check_xml(file):
	if os.path.isfile(file):
		print 'The xml file is already there'
		sys.exit()
def check_text(file):
	try:
		os.path.isfile(file)
	except IOError:
		print 'The text file is not found'
		sys.exit()
		pass

def get_ioformart(z_list):
        answer=raw_input('please defind the io graph(default for aliyun):')
        if answer == '':
                io_graph='IOStat hda-xvdb %util'
        else:
                io_graph=answer
        z_list=['CPU Load Average', 'Memory Usage', io_graph, 'Eth0 Network Traffic', 'Eth1 Network Traffic']

def get_server(X, Y, NAME, HOST):
	item = SubElement(items, 'screen_item')
	resourcetype=SubElement(item, 'resourcetype')
	resourcetype.text='0'
	width=SubElement(item, 'width')
	width.text='200'
	height=SubElement(item, 'height')
	height.text='100'
	x=SubElement(item, 'x')
	x.text=str(X)
	y=SubElement(item, 'y')
	y.text=str(Y)
	colspan=SubElement(item, 'colspan')
	colspan.text='1'
	rowspan=SubElement(item, 'rowspan')
	rowspan.text='1'
	elements=SubElement(item, 'elements')
	elements.text='0'
	valign=SubElement(item, 'valign')
	valign.text='0'
	halign=SubElement(item, 'halign')
	halign.text='0'
	style=SubElement(item, 'style')
	style.text='0'
	url=SubElement(item, 'url')
	dynamic=SubElement(item, 'dynamic')
	dynamic.text='0'
	sort_triggers=SubElement(item, 'sort_triggers')
	sort_triggers.text='0'
	resource=SubElement(item, 'resource')
	name=SubElement(resource, 'name')
	name.text=HOST
	host=SubElement(resource, 'host')
	host.text=NAME
	max_columns=SubElement(item, 'max_columns')
	max_columns.text='1'
	application=SubElement(item, 'application')

check_arg()
t_file = sys.argv[1]
x_file = sys.argv[2]
s_list=[ ]
f_list=[ ]
check_text(t_file)
check_xml(x_file)
get_ioformart(z_list)
f = open(t_file, 'r')
for f_line in f.readlines():
	f_line=f_line.strip('\n')
	f_list.append(f_line)

f.close()
Vsize = len(f_list) - 1
cus_name = f_list[0]
cus=f_list[0]
del f_list[0]
zabbix_import = Element('zabbix_export')
version = SubElement(zabbix_import, 'version')
version.text = '2.0'
date = SubElement(zabbix_import, 'date')
date.text = '11:53'
screens = SubElement(zabbix_import, 'screens')
screen = SubElement(screens, 'screen')
name = SubElement(screen, 'name')
name.text = cus_name
hsize = SubElement(screen, 'hsize')
hsize.text = '5'
vsize = SubElement(screen, 'vsize')
vsize.text=str(Vsize)
items = SubElement(screen, 'screen_items')

for Host in f_list:
	Y=f_list.index(Host)
	for Zabbix in z_list:
		X=z_list.index(Zabbix)
		get_server(X, Y, Host, Zabbix)
xml_output = prettify(zabbix_import)
f=open(x_file, 'w')
f.write(xml_output)
f.close()
