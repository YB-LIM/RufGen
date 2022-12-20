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
import numpy as np
from numpy import random
from math import gamma

def Height(D,G,Nx,Ny,Lx,Ly,WB_a,WB_b,std):
    #2D case
    if D==0 or D==1 or D==2 or D==3:
        if G==0: #G=0, Gaussian distribution case
            x=np.linspace(0,Lx,Nx,endpoint=True);
            y=np.random.normal(0,std,size=(Nx));
            Profile_pts=np.zeros((Nx,2));
            
            for i in range(len(x)):
                Profile_pts[i,:]=[x[i],y[i]]
                    
        elif G==1: #G=1, Weibull distribution case
            x=np.linspace(0,Lx,Nx,endpoint=True);
            y=-WB_a*gamma(1+1/WB_b)+WB_a*np.power(-np.log(random.random(Nx)),1/WB_b);
            Profile_pts=np.zeros((Nx,2));
            
            for i in range(len(x)):
                Profile_pts[i,:]=[x[i],y[i]]            
        
    #3D case    
    elif D==4 or D==5:
        if G==0: #G=0, Gaussian distribution case
            x=np.linspace(0,Lx,Nx,endpoint=True); y=np.linspace(0,Ly,Ny,endpoint=True);
            z=np.random.normal(0,std,size=(Ny*Nx)); Profile_pts=np.zeros((Nx*Ny,3));
            
            for i in range(Nx*Ny):
                Profile_pts[i,:]=[x[i%len(x)], y[i//len(x)], z[i]]
            
        elif G==1: #G=1, Weibull distribution case
            x=np.linspace(0,Lx,Nx,endpoint=True); y=np.linspace(0,Ly,Ny,endpoint=True);
            z=-WB_a*gamma(1+1/WB_b)+WB_a*np.power(-np.log(random.random((Ny*Nx))),1/WB_b); Profile_pts=np.zeros((Nx*Ny,3));

            for i in range(Nx*Ny):
                Profile_pts[i,:]=[x[i%len(x)], y[i//len(x)], z[i]]            
             
    return Profile_pts

def PSD(D,Lx,Ly,Lambda_min,Lambda_max,Cut_off,Rq,H):
    #2D case
    if D==0 or D==1 or D==2 or D==3:
        #To wave vector
        q0=2*np.pi/Lambda_max;
        qr=2*np.pi/Cut_off;
        q1=2*np.pi/Lambda_min;
        
        #Get the number of sampling points N
        N=int(Lx/Lambda_min); 
        if N%2==1:
            N=N-1
            
        #Create x array
        x=np.linspace(0,Lx,N,endpoint=True);
        dx=x[1]-x[0];

        #Generate an wave vector array
        qx=np.linspace(q0,q1,N,endpoint=True);

        I_cut=(qr/qx[-1])*N;
        #Magnitude array of the Roughness PSD
        Cq=np.zeros(N);

        for i in range(N):    
            if i+1<=I_cut:
                Cq[i]=np.power(qr,-2*(H+1));
            elif I_cut<i+1:
                Cq[i]=np.power(qx[i],-2*(H+1))

        #Scale to fit Rq value
        dq=abs(qx[1]-qx[0]);
        RMS_Calc=np.sqrt(np.sum(Cq*dq));
        Cq=Cq*np.power(Rq/RMS_Calc,2);

        #PSD to FFT
        FFT_Mag=np.sqrt(2*np.pi*N*Cq/dx);

        #Random sampling of phase angle
        Phi=(-np.pi+2*np.pi*np.random.random(N));

        #To complex number
        Values=np.zeros(N,dtype=complex);

        for i in range(N):
            Values[i]=FFT_Mag[i]*(np.cos(Phi[i])+1j*np.sin(Phi[i]))

        #Inverse FFT
        s=np.fft.ifft(np.fft.fftshift(Values));
        y=abs(s); y_avg=np.average(y);
        y=y-y_avg;

        Rq_Calc=(1/Lx)*np.sqrt(sum(np.power(y,2)*dx));
        y=y*Rq/Rq_Calc;

        Profile_pts=np.zeros((N,2))
        for i in range(N):
            Profile_pts[i,:]=[x[i],y[i]]
        return Profile_pts
    #3D case
    elif D==4 or D==5:
        #To wave vector
        q0=2*np.pi/Lambda_max;
        qr=2*np.pi/Cut_off;
        q1=2*np.pi/Lambda_min;

        #Get the number of sampling points N
        Nx=int(Lx/(0.25*Lambda_min));
        Ny=int(Ly/(0.25*Lambda_min));
        if Nx%2==1:
            Nx=Nx-1
        if Ny%2==1:
            Ny=Ny-1

        #Create x array
        x=np.linspace(0,Lx,Nx,endpoint=True);
        y=np.linspace(0,Ly,Ny,endpoint=True);
        dx=x[1]-x[0];
        dy=y[1]-y[0]

        #Generate an wave vector array
        qx=np.linspace(q0,q1,Nx,endpoint=True);
        qy=np.linspace(q0,q1,Ny,endpoint=True);

        #Magnitude array of the Roughness PSD
        Cq=np.zeros((Ny,Nx));

        for j in range(Ny):
            for i in range(Nx):
                if np.sqrt(qx[i]*qx[i]+qy[j]*qy[j])<=qr:
                    Cq[j,i]=np.power(qr,-2*(H+1));
                elif qr<np.sqrt(qx[i]*qx[i]+qy[j]*qy[j]):
                    Cq[j,i]=np.power(np.sqrt(qx[i]*qx[i]+qy[j]*qy[j]),-2*(H+1));

        #Scale to fit Rq value
        dqx=abs(qx[1]-qx[0]);
        dqy=abs(qy[1]-qy[0]);
        RMS_Calc=np.sqrt(np.sum(Cq*dqx*dqy));
        Cq=Cq*np.power(Rq/RMS_Calc,2);

        #PSD to FFT
        FFT_Mag=np.sqrt(Cq/(dx*dy)/(Nx*Ny*4*np.pi*np.pi));    

        #Random sampling of phase angle
        Phi=(-np.pi+2*np.pi*np.random.random((Ny,Nx)));

        #To complex number
        Values=np.zeros((Ny,Nx),dtype=complex);

        for k in range(Ny):
            for i in range(Nx):
                Values[k,i]=FFT_Mag[k,i]*(np.cos(Phi[k,i])+1j*np.sin(Phi[k,i]))

        #Inverse FFT
        s=np.fft.ifft2(np.fft.fftshift(Values));
        z=abs(s); z_avg=np.average(z);
        z=z-z_avg;

        Rq_Calc=np.sqrt((1/Lx/Ly)*np.sum(np.power(z,2)*dx*dy));
        z=z*Rq/Rq_Calc;

        Profile_pts=np.zeros((Ny,Nx));

        # Convert Grid-data to XYZ Triplet
        z=np.reshape(z,np.size(Profile_pts)); Profile_XYZ=np.zeros((np.size(Profile_pts),3));

        for i in range(len(z)):
            Profile_XYZ[i,:]=[x[i%len(x)], y[i//len(x)], z[i]]
                    
        Profile_pts=Profile_XYZ;
        
        return Profile_pts

def Profile(D,T,Lx,Ly,Profile_pts):
    #2D case
    if D==0 or D==1 or D==2 or D==3:
        Profile_pts=np.array(Profile_pts);
        
        #Move points
        min_x=min(Profile_pts[:,0]);   
        
        Profile_pts[:,0]=Profile_pts[:,0]-min_x; 
        y_avg=np.average(Profile_pts[:,1]); Profile_pts[:,1]=Profile_pts[:,1]-y_avg;
        return Profile_pts
    #3D case
    elif D==4 or D==5:
        if T==0:
            Profile_pts=np.array(Profile_pts);
        
            #Move points
            min_x=min(Profile_pts[:,0]); min_y=min(Profile_pts[:,1]);
        
            Profile_pts[:,0]=Profile_pts[:,0]-min_x; Profile_pts[:,1]=Profile_pts[:,1]-min_y;
            z_avg=np.average(Profile_pts[:,2]); Profile_pts[:,2]=Profile_pts[:,2]-z_avg;
            return Profile_pts
        elif T==1:
            Profile_pts=np.array(Profile_pts);
            
            # Get number of rows and columns from Grid-data
            Ny,Nx=Profile_pts.shape;
            # Set average z-value to be 0
            z_avg=np.average(Profile_pts); Profile_pts=Profile_pts-z_avg;   
            # Create x,y array
            x=np.linspace(0,Lx,Nx,endpoint=True); y=np.linspace(0,Ly,Ny,endpoint=True); 
            # Convert Grid-data to XYZ Triplet
            z=np.reshape(Profile_pts,np.size(Profile_pts)); Profile_XYZ=np.zeros((np.size(Profile_pts),3));
            
            for i in range(len(z)):
                Profile_XYZ[i,:]=[x[i%len(x)], y[i//len(x)], z[i]]
            
            Profile_pts=Profile_XYZ;         
            return Profile_pts
        
        
        