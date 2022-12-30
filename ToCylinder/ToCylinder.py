"""
This script transforms flat rough surface to cylindrical shape

*********************************************************************
*** The flat rough surface should be generated with RSGen plug-in ***
*********************************************************************
Usage
1. Put this script and Rough_Surf_3D_Shell.inp in the working directory 
2. Run the script, and a new input file for the cylindrical shape is generated


Python script by Youngbin LIM. Contact : lyb0684@naver.com
"""

import numpy as np
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

N_offset = 0
El_offset = 0

#Read input file generated with RSGen plug-in
file=open("Rough_Surf_3D_Shell.inp","r").readlines()

#Find lines for Node definition
Node_Start = 0; Node_End = 0;

#Find Start line
for i in range(len(file)):
    Node_search = file[i].split(",")
    if Node_search[0] != '1':
       Node_Start = Node_Start + 1
    elif Node_search[0] == '1':
        break

#Find End line
for i in range(len(file)):
    Node_search = file[i+Node_Start+1].split(",")
    if Node_search[0] != '1':
       Node_End = Node_End + 1
    elif Node_search[0] == '1':
        break

Node_End = Node_End + Node_Start - 1
Node_list_size = Node_End - (Node_Start - 1)

#Get X,Y,Z coordinate data
XYZ_data = np.zeros((Node_list_size,3))

for i in range(Node_list_size):
    Node_line = file[i+Node_Start].split(",")
    XYZ_data[i,:] = [float(Node_line[1]), float(Node_line[2]), float(Node_line[3])]

#Match Nodes in First line and the last line
Nodes_Num = 0

for i in range(len(XYZ_data)):
    if XYZ_data[i,1] == 0:
        Nodes_Num = Nodes_Num + 1 
    elif XYZ_data[i,1] != 0:
        break

for i in range(Nodes_Num):
    XYZ_data[-(i+1),2] = XYZ_data[Nodes_Num-(i+1),2] = 0

#Transform to Cylindrical shape
X0 = XYZ_data[:,0]; Y0 = XYZ_data[:,1]; Z0 = XYZ_data[:,2]
R0 = max(Y0)/(2*np.pi)
L = XYZ_data[:,1];
Y_cyl = np.zeros(len(Y0))
Z_cyl = np.zeros(len(Z0))

for i in range(len(Y0)):
    Y_cyl[i] = (R0 + Z0[i])*(np.cos(np.pi - L[i]/R0))
    Z_cyl[i] =  (R0 + Z0[i])*np.sin(np.pi - L[i]/R0)

Nodes_cyl = np.zeros((len(Y0),4))

for i in range(len(Y0)):
    Nodes_cyl[i,:] = [int(i+1)+N_offset, X0[i], Y_cyl[i], Z_cyl[i]]

#Write new input file for cylindrical rough surface
#Read element definition
Element_Start = Node_End + 2; Element_End = 0;

#Find Element End line
for i in range(len(file)):
    Element_search = file[i+Element_Start+1].split(",")
    if Element_search[0] != '*Elset':
       Element_End = Element_End + 1
    elif Element_search[0] == '*Elset':
        break

Element_End = Element_End + Element_Start
Element_list_size = Element_End - (Element_Start - 1)

Elements = np.zeros((Element_list_size,5))

for i in range(Element_list_size):
    Element_line = file[i+Element_Start].split(",")
    Elements[i,:] = [int(Element_line[0])+El_offset, int(Element_line[1])+N_offset, int(Element_line[2])+N_offset, int(Element_line[3])+N_offset, int(Element_line[4])+N_offset]

file=open('Rough_Surf_3D_Shell_Cyl.inp','w')
file.write("*Node\n")
np.savetxt(file,Nodes_cyl,fmt='%d, %f, %f, %f',delimiter=",")
file.write("*Element, type=R3D4\n")
np.savetxt(file,Elements,fmt='%d, %d, %d, %d, %d',delimiter=",")
file.close()

#********************************
#Import input file in Abaqus/CAE*
#********************************
                
mdb.ModelFromInputFile(name='Rough_Surf_3D_Shell_Cyl', inputFileName='Rough_Surf_3D_Shell_Cyl.inp')
a = mdb.models['Rough_Surf_3D_Shell_Cyl'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
p1 = mdb.models['Rough_Surf_3D_Shell_Cyl'].parts['PART-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)