"""
    python script by Youngbin LIM
    To inquire any queries, Contact: lyb0684@naver.com
    
    *************************************
    *Description on the input parameters*
    *************************************
    
    D: Dimensionality, if 
    D=0, 2D-wire, planar
      1, 2D-wire, axis
      2, 2D-shell, planar
      3, 2D-shell, axis
      4, 3D-shell  
      5, 3D-solid      
    
    G: Type of Random point Generator, if
    G=0, Random sampling from Gaussian distribution
    G=1, Random sampling from Weibull distribution
    G=2, Random sampling from Roughness PSD
    G=3, From profile data
    
    Lx, Ly : Length of x and y direction (Lx, Ly)
    
    Lz : Lz is the thickness of deformable solid. It is the distance between the bottom surface and the top (averaged) surface
    Input Lz=0 corresponds to 3D surface
    
    Le: Le is the approximate element length 
    
    Nx, Ny: Number of sampling points for x and y direction
    
    WB_a, WB_b: WB_a and WB_b is parameters for Weibull distribution, 
    where, Cummulative Distribution Function: F=1-exp[-(x/a)^b]

    Std: Std is standard deviation of Gaussian distribution. Mean value is 0
    
"""
# Numpy
import numpy as np
from numpy import random
from math import gamma
## Abaqus import
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

def PG2D(D,Ly,Points_top,PartName):
    Lx=abs(Points_top[0,0]-Points_top[-1,0]);
    if D==0: #2D wire, Planar
        mdb.Model(name='Rough_Surf_2D_Wire_Planar', modelType=STANDARD_EXPLICIT)
        s=mdb.models['Rough_Surf_2D_Wire_Planar'].ConstrainedSketch(name='__profile__', sheetSize=Lx*200)
        
        Points_Range = len(Points_top[:,0])-1;
        for i in range(Points_Range):
            s.Line(point1=(Points_top[i,0],Points_top[i,1]), point2=(Points_top[i+1,0],Points_top[i+1,1]))
#        s.Spline(points=Points_top)        

        p = mdb.models['Rough_Surf_2D_Wire_Planar'].Part(name=PartName, dimensionality=TWO_D_PLANAR, type=DISCRETE_RIGID_SURFACE)
        p.BaseWire(sketch=s)
        s.unsetPrimaryObject()
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Rough_Surf_2D_Wire_Planar'].sketches['__profile__']
    elif D==1: #2D wire, Axis
        mdb.Model(name='Rough_Surf_2D_Wire_Axis', modelType=STANDARD_EXPLICIT)
        s=mdb.models['Rough_Surf_2D_Wire_Axis'].ConstrainedSketch(name='__profile__', sheetSize=Lx*200)
        
        Points_Range = len(Points_top[:,0])-1;
        for i in range(Points_Range):
            s.Line(point1=(Points_top[i,0],Points_top[i,1]), point2=(Points_top[i+1,0],Points_top[i+1,1]))
#        s.Spline(points=Points_top)

        p = mdb.models['Rough_Surf_2D_Wire_Axis'].Part(name=PartName, dimensionality=AXISYMMETRIC, type=DISCRETE_RIGID_SURFACE)
        s.sketchOptions.setValues(viewStyle=AXISYM)
        s.setPrimaryObject(option=STANDALONE)
        s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
        p.BaseWire(sketch=s)
        s.unsetPrimaryObject()
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Rough_Surf_2D_Wire_Axis'].sketches['__profile__']
    elif D==2: #2D shell, Planar
        mdb.Model(name='Rough_Surf_2D_Shell_Planar', modelType=STANDARD_EXPLICIT)
        s=mdb.models['Rough_Surf_2D_Shell_Planar'].ConstrainedSketch(name='__profile__', sheetSize=Lx*200)
   
        Points_Range = len(Points_top[:,0])-1;
        for i in range(Points_Range):
            s.Line(point1=(Points_top[i,0],Points_top[i,1]), point2=(Points_top[i+1,0],Points_top[i+1,1]))
#        s.Spline(points=Points_top)
  
        s.Line(point1=(0,Points_top[0,1]), point2=(0,-Ly))
        s.Line(point1=(0,-Ly), point2=(Lx,-Ly))
        s.Line(point1=(Lx,-Ly), point2=(Lx,Points_top[-1,1]))
        p = mdb.models['Rough_Surf_2D_Shell_Planar'].Part(name=PartName, dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
        p.BaseShell(sketch=s)
        s.unsetPrimaryObject()
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Rough_Surf_2D_Shell_Planar'].sketches['__profile__']
    elif D==3: #2D shell, Axis
        mdb.Model(name='Rough_Surf_2D_Shell_Axis', modelType=STANDARD_EXPLICIT)
        s=mdb.models['Rough_Surf_2D_Shell_Axis'].ConstrainedSketch(name='__profile__', sheetSize=Lx*200)
        Points_Range = len(Points_top[:,0])-1;
        for i in range(Points_Range):
            s.Line(point1=(Points_top[i,0],Points_top[i,1]), point2=(Points_top[i+1,0],Points_top[i+1,1]))        
#        s.Spline(points=Points_top)

        s.Line(point1=(0,Points_top[0,1]), point2=(0,-Ly))
        s.Line(point1=(0,-Ly), point2=(Lx,-Ly))
        s.Line(point1=(Lx,-Ly), point2=(Lx,Points_top[-1,1]))
        p = mdb.models['Rough_Surf_2D_Shell_Axis'].Part(name=PartName, dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
        s.sketchOptions.setValues(viewStyle=AXISYM)
        s.setPrimaryObject(option=STANDALONE)
        s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
        p.BaseShell(sketch=s)
        s.unsetPrimaryObject()
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Rough_Surf_2D_Shell_Axis'].sketches['__profile__']
        return 0
        
def PG3D(D,Lz,x_elnum,y_elnum,Bot_layer_num,Nodes_top,PartName):
    if D==4: #3D shell
        El_total_N=x_elnum*y_elnum;
        #****************
        #Mesh Generation*
        #****************
        Elements=np.zeros((El_total_N,5));
        for k in range(y_elnum):
            for j in range(x_elnum):
                Elements[j+x_elnum*k,:]=[(j+1)+k*x_elnum, (j+1)+(x_elnum+1)*k+1, (j+1)+(x_elnum+1)*k+(x_elnum+2), (j+1)+(x_elnum+1)*k+(x_elnum+1), (j+1)+(x_elnum+1)*k]
        
        #************************************
        #Element sets for surface definition*
        #************************************

        elset_S1=[[1], [x_elnum*y_elnum], [1]]; elset_S1=np.transpose(elset_S1);

        #*****************
        #Write input file*
        #*****************
        PartName = PartName.upper()
        file=open('Rough_Surf_3D_Shell.inp','w')
        file.write("*Part, Name=")
        file.write(PartName)
        file.write("\n*Node\n")
        np.savetxt(file,Nodes_top,fmt='%d, %.6e, %.6e, %.6e',delimiter=",")
        file.write("*Element, type=R3D4\n")
        np.savetxt(file,Elements,fmt='%d, %d, %d, %d, %d',delimiter=",")
        file.write("*Elset, elset=elset_S1, generate\n")
        np.savetxt(file,elset_S1,fmt='%d',delimiter=",")
        file.write("*Surface, type=element, name=S1\nelset_S1, S1\n")
        file.write("*End Part")
        file.close()
        
        #**************************************************
        #Import part and convert to geometry in Abaqus/CAE*
        #**************************************************
                
        mdb.ModelFromInputFile(name='Rough_Surf_3D_Shell', inputFileName='Rough_Surf_3D_Shell.inp')
        a = mdb.models['Rough_Surf_3D_Shell'].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        PartName = PartName.upper()
        p1 = mdb.models['Rough_Surf_3D_Shell'].parts[PartName]
        session.viewports['Viewport: 1'].setValues(displayedObject=p1)
        
        #Geometry conversion is disabled for further release
        
        #p = mdb.models['Rough_Surf_3D_Shell'].Part(name='GEOMETRY', objectToCopy=mdb.models['Rough_Surf_3D_Shell'].parts['ORPHAN_MESH'])
        #p.FaceFromElementFaces(elementFaces=p.surfaces['S1'])
        #session.viewports['Viewport: 1'].setValues(displayedObject=p1)
        
    elif D==5: #3D solid
        Nodes_bot=np.zeros((len(Nodes_top)*Bot_layer_num,4));
        El_total_N=x_elnum*y_elnum*Bot_layer_num;
        
        for i in range(Bot_layer_num):
            for j in range(len(Nodes_top)):
                Nodes_bot[j+i*len(Nodes_top),:]=[j+1+(i+1)*len(Nodes_top), Nodes_top[j,1], Nodes_top[j,2], Nodes_top[j,3]-(i+1)*(Nodes_top[j,3]+Lz)/Bot_layer_num]
                
        Nodes=np.append(Nodes_top,Nodes_bot,axis=0);
        N_shift=(x_elnum+1)*(y_elnum+1);
        
        Elements=np.zeros((El_total_N,9));
        
        for i in range(Bot_layer_num):
            for k in range(y_elnum):
                for j in range(x_elnum):
                    Elements[j+x_elnum*k+i*x_elnum*y_elnum,:]=[(j+1)+k*x_elnum+i*x_elnum*y_elnum, (j+1)+(x_elnum+1)*k+(i+1)*N_shift,(j+1)+(x_elnum+1)*k+1+(i+1)*N_shift,(j+1)+(x_elnum+1)*k+(x_elnum+2)+(i+1)*N_shift,(j+1)+(x_elnum+1)*k+(x_elnum+1)+(i+1)*N_shift,(j+1)+(x_elnum+1)*k+i*N_shift,(j+1)+(x_elnum+1)*k+1+i*N_shift,(j+1)+(x_elnum+1)*k+(x_elnum+2)+i*N_shift,(j+1)+(x_elnum+1)*k+(x_elnum+1)+i*N_shift]

        #************************************
        #Element sets for surface definition*
        #************************************

        elset_S1=[[x_elnum*y_elnum*(Bot_layer_num-1)+1], [El_total_N], [1]]; elset_S1=np.transpose(elset_S1);
        elset_S2=[[1], [x_elnum*y_elnum], [1]]; elset_S2=np.transpose(elset_S2);
        elset_S3=np.zeros((Bot_layer_num,3)); elset_S4=np.zeros((Bot_layer_num,3)); 
        elset_S5=np.zeros((Bot_layer_num,3)); elset_S6=np.zeros((Bot_layer_num,3));

        #elset_S3
        for i in range(Bot_layer_num):
            elset_S3[i,:]=[1+(x_elnum*y_elnum)*i, x_elnum+(x_elnum*y_elnum)*i, 1]
        #elset_S4
        for i in range(Bot_layer_num):
            elset_S4[i,:]=[x_elnum+(x_elnum*y_elnum)*i, x_elnum*y_elnum+(x_elnum*y_elnum)*i, x_elnum]
        #elset_S5
        for i in range(Bot_layer_num):
            elset_S5[i,:]=[x_elnum*(y_elnum-1)+1+(x_elnum*y_elnum)*i, x_elnum*y_elnum+(x_elnum*y_elnum)*i, 1]
        #elset_S6
        for i in range(Bot_layer_num):
            elset_S6[i,:]=[1+(x_elnum*y_elnum)*i, x_elnum*(y_elnum-1)+1+(x_elnum*y_elnum)*i, x_elnum]

        #*****************
        #Write input file*
        #*****************
        PartName = PartName.upper()
        file=open('Rough_Surf_3D_Solid.inp','w')
        file.write("*Part, Name=")
        file.write(PartName)
        file.write("\n*Node\n")
        np.savetxt(file,Nodes,fmt='%d, %.6e, %.6e, %.6e',delimiter=",")
        file.write("*Element, type=C3D8R\n")
        np.savetxt(file,Elements,fmt='%d, %d, %d, %d, %d, %d, %d, %d, %d',delimiter=",")
        file.write("*Elset, elset=elset_S1, generate\n")
        np.savetxt(file,elset_S1,fmt='%d',delimiter=",")
        file.write("*Elset, elset=elset_S2, generate\n")
        np.savetxt(file,elset_S2,fmt='%d',delimiter=",")
        file.write("*Elset, elset=elset_S3, generate\n")
        np.savetxt(file,elset_S3,fmt='%d',delimiter=",")
        file.write("*Elset, elset=elset_S4, generate\n")
        np.savetxt(file,elset_S4,fmt='%d',delimiter=",")
        file.write("*Elset, elset=elset_S5, generate\n")
        np.savetxt(file,elset_S5,fmt='%d',delimiter=",")
        file.write("*Elset, elset=elset_S6, generate\n")
        np.savetxt(file,elset_S6,fmt='%d',delimiter=",")
        file.write("*Surface, type=element, name=S1\nelset_S1, S1\n")
        file.write("*Surface, type=element, name=S2\nelset_S2, S2\n")
        file.write("*Surface, type=element, name=S3\nelset_S3, S3\n")
        file.write("*Surface, type=element, name=S4\nelset_S4, S4\n")
        file.write("*Surface, type=element, name=S5\nelset_S5, S5\n")
        file.write("*Surface, type=element, name=S6\nelset_S6, S6\n")
        file.write("*End Part")
        file.close()
        
        #**************************************************
        #Import part and convert to geometry in Abaqus/CAE*
        #**************************************************
        mdb.ModelFromInputFile(name='Rough_Surf_3D_Solid', inputFileName='Rough_Surf_3D_Solid.inp')
        a = mdb.models['Rough_Surf_3D_Solid'].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        p1 = mdb.models['Rough_Surf_3D_Solid'].parts[PartName]
        session.viewports['Viewport: 1'].setValues(displayedObject=p1)
        
        #Geometry conversion is disabled for further release        
        #p = mdb.models['Rough_Surf_3D_Solid'].Part(name='GEOMETRY', objectToCopy=mdb.models['Rough_Surf_3D_Solid'].parts['ORPHAN_MESH'])
        #p.FaceFromElementFaces(elementFaces=p.surfaces['S1'])
        #p.FaceFromElementFaces(elementFaces=p.surfaces['S2'])
        #p.FaceFromElementFaces(elementFaces=p.surfaces['S3'])
        #p.FaceFromElementFaces(elementFaces=p.surfaces['S4'])
        #p.FaceFromElementFaces(elementFaces=p.surfaces['S5'])
        #p.FaceFromElementFaces(elementFaces=p.surfaces['S6'])
        #p = mdb.models['Rough_Surf_3D_Solid'].parts['GEOMETRY']
        #f = p.faces
        #p.AddCells(faceList = f[0:6])
        #del p.features['Orphan mesh-1']
        
        session.viewports['Viewport: 1'].setValues(displayedObject=p1)
        session.viewports['Viewport: 1'].setColor(globalTranslucency=True)
        session.viewports['Viewport: 1'].setColor(translucency=1)
    return 0
