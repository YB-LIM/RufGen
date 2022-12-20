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
import numpy as np
from scipy.interpolate import CubicSpline
from window import tukey 
              
def TG2D(Profile_pts):
        Lx=abs(Profile_pts[0,0]-Profile_pts[-1,0])
        
        x_s=np.linspace(0,Lx,len(Profile_pts)*3,endpoint=True);
        CS=CubicSpline(Profile_pts[:,0],Profile_pts[:,1]); 
        R=CS(x_s);
        y_avg=np.average(R); dx=Lx/(len(Profile_pts)*3-1);
        
        Points_top=np.zeros((len(R),2))
        
        for i in range(len(R)):
            Points_top[i,:]=[x_s[i], R[i]]
        
        Ra=(1/Lx)*sum(abs(R-y_avg)*dx);
        Rq=np.sqrt((1/Lx)*sum(np.power(R-y_avg,2)*dx));   
              
        return Ra,Rq,Points_top

def TG3D(D,Le,Lz,Profile_pts,XP,XN,YP,YN):
    if D==4: #3D shell case
        x=Profile_pts[:,0]; y=Profile_pts[:,1]; z=Profile_pts[:,2];
        
        Lx=abs(x[0]-x[-1]); Ly=abs(y[0]-y[-1]);
        x_s=np.linspace(0,Lx,int(Lx/Le)+1,endpoint=True); y_s=np.linspace(0,Ly,int(Ly/Le)+1,endpoint=True);
        
        Num_x=1;
        for i in range(len(x)-1):
            if (x[i+1]-x[i])>0:
                Num_x=Num_x+1;
            elif (x[i+1]-x[i])<0:
                break        
        Num_y=int(len(Profile_pts)/Num_x);       

        x_elnum=len(x_s)-1; y_elnum=len(y_s)-1;
        Bot_layer_num=0;
        dx=x_s[1]-x_s[0]; dy=y_s[1]-y_s[0]               
        N_total=len(x_s)*len(x_s);
        El_total=x_elnum*y_elnum;
                                  
        #****************************
        #Apply Tukey window function*
        #****************************
        
        #Reshape x,y,z to grid-data
        z_grid=np.reshape(z,(Num_y,Num_x));
        x_grid=np.zeros(Num_x); y_grid=np.zeros(Num_y);
        
        for i in range(Num_x):
            x_grid[i]=x[i]
        
        for i in range(Num_y):
            y_grid[i]=y[i*Num_x] 
        
        window_X = np.ones(Num_x);
        window_Y = np.ones(Num_y);
        window_XP = np.ones(Num_x); 
        window_XN = np.ones(Num_x); 
        window_YP = np.ones(Num_y); 
        window_YN = np.ones(Num_y); 
        
        #*********************
        #Apply directionality*
        #*********************
        if XP==True:
            window_XP = tukey(Num_x);
            for i in range(Num_x):
                if i<int(Num_x/2):
                    window_XP[i]=1
                elif i>=int(Num_x/2):
                    window_XP[i]=window_XP[i]
        
        if XN==True:
            window_XN = tukey(Num_x);            
            for i in range(Num_x):
                if i<int(Num_x/2):
                    window_XN[i]=window_XN[i]
                elif i>=int(Num_x/2):
                    window_XN[i]=1
            
        if YP==True:
            window_YP = tukey(Num_y);            
            for i in range(Num_y):
                if i<int(Num_y/2):
                    window_YP[i]=1
                elif i>=int(Num_y/2):
                    window_YP[i]=window_YP[i]   
        
        if YN==True:
            window_YN = tukey(Num_y);            
            for i in range(Num_y):
                if i<int(Num_y/2):
                    window_YN[i]=window_YN[i]
                elif i>=int(Num_y/2):
                    window_YN[i]=1             
        
        window_X=window_XP*window_XN;
        window_Y=window_YP*window_YN;
        
        for i in range(Num_y):
            z_grid[i,:]=window_X*z_grid[i,:]
        for i in range(Num_x):
            z_grid[:,i]=window_Y*z_grid[:,i]
        
        
        #*********************
        #Spline interpolation*
        #*********************
        Rx=np.zeros((Num_y,len(x_s))); R=np.zeros((len(y_s),len(x_s)));
        
        for i in range(Num_y):
            #Rx[i,:]=QuadSpline(x_s,x_grid,z_grid[i,:])
            CS=CubicSpline(x_grid,z_grid[i,:])
            Rx[i,:]=CS(x_s)
        for i in range(len(x_s)):
            #R[:,i]=QuadSpline(y_s,y_grid,Rx[:,i])
            CS=CubicSpline(y_grid,Rx[:,i])
            R[:,i]=CS(y_s)            
            
        
        #*********************************
        #Nodes list for top rough surface*
        #*********************************
        z_avg=np.average(R);    
        z=np.reshape(R,np.size(R))-z_avg; Nodes_top=np.zeros((np.size(R),4));

        for i in range(np.size(R)):
            Nodes_top[i,:]=[i+1, x_s[i%len(x_s)], y_s[i//len(x_s)], z[i]]
        
        #**********************
        #Roughness calculation*
        #**********************
        Nx_r=int(len(x_s)*0.8); Ny_r=int(len(y_s)*0.8);
        R_r=np.zeros((Ny_r,Nx_r));
        
        for j in range(Ny_r):
            for i in range(Nx_r):
                R_r[j,i]=R[j+int(len(y_s)*0.1),i+int(len(x_s)*0.1)];
           
        Sa=(1/(0.8*Lx)/(0.8*Ly))*np.sum(abs(R_r)*(dx)*(dy));
        Sq=np.sqrt((1/(0.8*Lx)/(0.8*Ly))*np.sum(np.power(R_r,2))*(dx)*(dy));            
        
        return Sa,Sq,N_total,El_total,x_elnum,y_elnum,Bot_layer_num,Nodes_top
        
    elif D==5: #3D solid case
        x=Profile_pts[:,0]; y=Profile_pts[:,1]; z=Profile_pts[:,2];      
       
        Lx=abs(x[0]-x[-1]); Ly=abs(y[0]-y[-1]);
        x_s=np.linspace(0,Lx,int(Lx/Le)+1,endpoint=True); y_s=np.linspace(0,Ly,int(Ly/Le)+1,endpoint=True);
        
        Num_x=1;
        for i in range(len(x)-1):
            if (x[i+1]-x[i])>0:
                Num_x=Num_x+1;
            elif (x[i+1]-x[i])<0:
                break        
        Num_y=int(len(Profile_pts)/Num_x);

        x_elnum=len(x_s)-1; y_elnum=len(y_s)-1;
        dx=x_s[1]-x_s[0]; dy=y_s[1]-y_s[0]
        avg_mesh_size=(dx+dy)/2;
        Bot_layer_num=int(Lz//avg_mesh_size);
        N_total=len(x_s)*len(x_s)*Bot_layer_num;
        El_total=x_elnum*y_elnum*Bot_layer_num;
        
        #****************************
        #Apply Tukey window function*
        #****************************
        
        #Reshape x,y,z to grid-data
        z_grid=np.reshape(z,(Num_y,Num_x));
        x_grid=np.zeros(Num_x); y_grid=np.zeros(Num_y);
        
        for i in range(Num_x):
            x_grid[i]=x[i]
        
        for i in range(Num_y):
            y_grid[i]=y[i*Num_x] 
        
        window_X = np.ones(Num_x);
        window_Y = np.ones(Num_y);
        window_XP =np.ones(Num_x); 
        window_XN =np.ones(Num_x); 
        window_YP =np.ones(Num_y); 
        window_YN =np.ones(Num_y); 
        
        #*********************
        #Apply directionality*
        #*********************
        if XP==True:
            window_XP = tukey(Num_x);
            for i in range(Num_x):
                if i<int(Num_x/2):
                    window_XP[i]=1
                elif i>=int(Num_x/2):
                    window_XP[i]=window_XP[i]
        
        if XN==True:
            window_XN = tukey(Num_x);            
            for i in range(Num_x):
                if i<int(Num_x/2):
                    window_XN[i]=window_XN[i]
                elif i>=int(Num_x/2):
                    window_XN[i]=1
            
        if YP==True:
            window_YP = tukey(Num_y);            
            for i in range(Num_y):
                if i<int(Num_y/2):
                    window_YP[i]=1
                elif i>=int(Num_y/2):
                    window_YP[i]=window_YP[i]   
        
        if YN==True:
            window_YN = tukey(Num_y);            
            for i in range(Num_y):
                if i<int(Num_y/2):
                    window_YN[i]=window_YN[i]
                elif i>=int(Num_y/2):
                    window_YN[i]=1             
        
        window_X=window_XP*window_XN;
        window_Y=window_YP*window_YN;
        
        for i in range(Num_y):
            z_grid[i,:]=window_X*z_grid[i,:]
        for i in range(Num_x):
            z_grid[:,i]=window_Y*z_grid[:,i]
        
        
        #*********************
        #Spline interpolation*
        #*********************
        Rx=np.zeros((Num_y,len(x_s))); R=np.zeros((len(y_s),len(x_s)));
        
        for i in range(Num_y):
            CS=CubicSpline(x_grid,z_grid[i,:])
            Rx[i,:]=CS(x_s)
        for i in range(len(x_s)):
            CS=CubicSpline(y_grid,Rx[:,i])
            R[:,i]=CS(y_s)            
            
        #*********************************
        #Nodes list for top rough surface*
        #*********************************
        z_avg=np.average(R);    
        z=np.reshape(R,np.size(R))-z_avg; Nodes_top=np.zeros((np.size(R),4));        

        for i in range(np.size(R)):
            Nodes_top[i,:]=[i+1, x_s[i%len(x_s)], y_s[i//len(x_s)], z[i]]
        
        #**********************
        #Roughness calculation*
        #**********************
        Nx_r=int(len(x_s)*0.8); Ny_r=int(len(y_s)*0.8);
        R_r=np.zeros((Ny_r,Nx_r));
        
        for j in range(Ny_r):
            for i in range(Nx_r):
                R_r[j,i]=R[j+int(len(y_s)*0.1),i+int(len(x_s)*0.1)];
           
        Sa=(1/(0.8*Lx)/(0.8*Ly))*np.sum(abs(R_r)*(dx)*(dy));
        Sq=np.sqrt((1/(0.8*Lx)/(0.8*Ly))*np.sum(np.power(R_r,2))*(dx)*(dy));       
               
        return Sa,Sq,N_total,El_total,x_elnum,y_elnum,Bot_layer_num,Nodes_top