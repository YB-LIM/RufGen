"""
    python script by Youngbin LIM
    To inquire any queries, Contact: lyb0684@naver.com
    
    *************************************
    *Description on the input parameters*
    *************************************
    
    D: Dimensionality (-1 from plug-in) , if 
    D=0, 2D-wire, planar
      1, 2D-wire, axis
      2, 2D-shell, planar
      3, 2D-shell, axis
      4, 3D-shell  
      5, 3D-solid      
    
    G: Type of Random point Generator (-1 from plug-in), if
    G=0, Random sampling from Gaussian distribution
    G=1, Random sampling from Weibull distribution
    G=2, Random sampling from Roughness PSD
    G=3, XYZ Point cloud
    G=4, Uniform grid

    
    Lx, Ly : Length of x and y direction (Lx, Ly)
    
    Lz : Lz is the thickness of deformable solid. It is the distance between the bottom surface and the top (averaged) surface
    Input Lz=0 corresponds to 3D surface
    
    Le: Le is the approximate element length 
    
    Nx, Ny: Number of sampling points for x and y direction
    
    WB_a, WB_b: WB_a and WB_b is parameters for Weibull distribution, 
    where, Cummulative Distribution Function: F=1-exp[-(x/a)^b]

    Std: Std is standard deviation of Gaussian distribution. Mean value is 0
    
    Rq: Roughness parameter Rq, or standard deviation of height
    
    H (0~1): Hurst exponent. Smaller the value, Rougher the surface
    
    Lambda_min: minimum length scale of spatial wave
    Lambda_max: maximum length scale of spatial wave
    Cut_off_wave_length: Cut off wave length
    
"""
# Library import
import numpy as np
from numpy import random
from math import gamma
# Abaqus import
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
#RSGen Module import
import RPG
import TopGen
import PartGen

def execute(D,G,Lx,Ly,Lz,Nx,Ny,a,b,std,Lmin,Lmax,Lcut,Le,H,Rq,XP,XN,YP,YN,FileName,PartName):
    #Initialize variables for Kernel script
    D=D-1; G=G-1; T=-1;
    D=int(D); G=int(G); Lx=float(Lx); Ly=float(Ly); Nx=int(Nx); Ny=int(Ny); a=float(a); b=float(b); std=float(std);
    Lmin=float(Lmin); Lmax=float(Lmax); Lcut=float(Lcut); Le=float(Le); H=float(H); Rq=float(Rq);
    #Show stop button
    showStopButtonInGui()
    
    
    #2D case
    if D==0 or D==1 or D==2 or D==3:
        #Height Distribution
        if G==0 or G==1:
            Profile_pts=RPG.Height(D,G,Nx,Ny,Lx,Ly,a,b,std)
            Ra,Rq,Points_top=TopGen.TG2D(Profile_pts)
            PartGen.PG2D(D,Ly,Points_top,PartName)
            print('**************************')
            print('** Roughness parameters **')
            print('**************************')            
            print('Ra:',Ra,', Rq:',Rq)
        #PSD
        elif G==2:
            Profile_pts=RPG.PSD(D,Lx,Ly,Lmin,Lmax,Lcut,Rq,H)
            Ra,Rq,Points_top=TopGen.TG2D(Profile_pts)
            PartGen.PG2D(D,Ly,Points_top,PartName)
            print('**************************')
            print('** Roughness parameters **')
            print('**************************')        
            print('Ra:',Ra,', Rq:',Rq)            
        #Profile Data - XY Data
        elif G==3:
            T=0
            try:
                file=open(FileName)
                Profile_pts=np.loadtxt(file);
                file.close()                            
            except:
                file=open(FileName)
                Profile_pts=np.loadtxt(file, delimiter=",");
                file.close()
                
            Profile_pts = Profile_pts.astype(float)
            
            Profile_pts=RPG.Profile(D,T,Lx,Ly,Profile_pts)
            Ra,Rq,Points_top=TopGen.TG2D(Profile_pts)
            PartGen.PG2D(D,Ly,Points_top,PartName)
            print('**************************')
            print('** Roughness parameters **')
            print('**************************')        
            print('Ra:',Ra,', Rq:',Rq)
    #3D case
    elif D==4 or D==5:
        #Height Distribution
        if G==0 or G==1:
            Profile_pts=RPG.Height(D,G,Nx,Ny,Lx,Ly,a,b,std)
            Sa,Sq,N_total,El_total,x_elnum,y_elnum,Bot_layer_num,Nodes_top=TopGen.TG3D(D,Le,Lz,Profile_pts,XP,XN,YP,YN)
            PartGen.PG3D(D,Lz,x_elnum,y_elnum,Bot_layer_num,Nodes_top,PartName)
            print('**********************')           
            print('** Mesh information **')
            print('**********************')             
            print('Number of nodes:',N_total,', Number of elements:',El_total)
            print('**************************')
            print('** Roughness parameters **')
            print('**************************')        
            print('Sa:',Sa,', Sq:',Sq)   
        #PSD
        elif G==2:
            Profile_pts=RPG.PSD(D,Lx,Ly,Lmin,Lmax,Lcut,Rq,H)
            Sa,Sq,N_total,El_total,x_elnum,y_elnum,Bot_layer_num,Nodes_top=TopGen.TG3D(D,Le,Lz,Profile_pts,XP,XN,YP,YN)
            PartGen.PG3D(D,Lz,x_elnum,y_elnum,Bot_layer_num,Nodes_top,PartName)   
            print('**********************')           
            print('** Mesh information **')
            print('**********************')             
            print('Number of nodes:',N_total,', Number of elements:',El_total)
            print('**************************')
            print('** Roughness parameters **')
            print('**************************')        
            print('Sa:',Sa,', Sq:',Sq)               
        #Profile Data - XYZ Triplet
        elif G==3:
            T=0
            try:
                file=open(FileName)
                Profile_pts=np.loadtxt(file);
                file.close()                            
            except:
                file=open(FileName)
                Profile_pts=np.loadtxt(file, delimiter=",");
                file.close()                  
                               
            Profile_pts = Profile_pts.astype(float)
            x=Profile_pts[:,0]; y=Profile_pts[:,1]; z=Profile_pts[:,2];        
            Lx=abs(x[0]-x[-1]); Ly=abs(y[0]-y[-1]);    
            Profile_pts=RPG.Profile(D,T,Lx,Ly,Profile_pts)
            Sa,Sq,N_total,El_total,x_elnum,y_elnum,Bot_layer_num,Nodes_top=TopGen.TG3D(D,Le,Lz,Profile_pts,XP,XN,YP,YN)
            PartGen.PG3D(D,Lz,x_elnum,y_elnum,Bot_layer_num,Nodes_top,PartName)
            print('**********************')           
            print('** Mesh information **')
            print('**********************')             
            print('Number of nodes:',N_total,', Number of elements:',El_total)
            print('**************************')
            print('** Roughness parameters **')
            print('**************************')        
            print('Sa:',Sa,', Sq:',Sq)               

        elif G==4: 
            T=1
            try:
                file=open(FileName)
                Profile_pts=np.loadtxt(file);
                file.close()                            
            except:
                file=open(FileName)
                Profile_pts=np.loadtxt(file, delimiter=",");
                file.close()                  
                               
            Profile_pts = Profile_pts.astype(float)
            
            Profile_pts=RPG.Profile(D,T,Lx,Ly,Profile_pts)
            Sa,Sq,N_total,El_total,x_elnum,y_elnum,Bot_layer_num,Nodes_top=TopGen.TG3D(D,Le,Lz,Profile_pts,XP,XN,YP,YN)
            PartGen.PG3D(D,Lz,x_elnum,y_elnum,Bot_layer_num,Nodes_top,PartName)
            print('**********************')           
            print('** Mesh information **')
            print('**********************')             
            print('Number of nodes:',N_total,', Number of elements:',El_total)
            print('**************************')
            print('** Roughness parameters **')
            print('**************************')        
            print('Sa:',Sa,', Sq:',Sq)