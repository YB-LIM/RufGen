"""

******************************************************************
**  Python script by Youngbin LIM, Contact : lyb0684@naver.com  **
******************************************************************
    This sciprt converts the image to the text file in the csv format
    Pixel values are converted to XYZ Triplet type data which can be used for RufGen plug-in
    The script was written on python 3.9
*****************************************
** Description on the input parameters **
*****************************************
    Lx : length in x-direction
    Ly : length in y-direction
    Zmin : minimum value of z-coordinate
    Zmax : maximum value of z-coordinate
    Input_ImagePath : Path of the image file
    Output_TextPath : Path of the text file to be saved

"""

from PIL import Image, ImageOps
import numpy as np

#Input parameters
Lx=1.0; Ly=1.0; Zmin=-0.01; Zmax=0.01; 
Input_ImagePath="Height_Crop.jpg"
Output_TextPath='Profile_Data_XYZ_Triplet.txt'

#Open image
Im = Image.open(Input_ImagePath);
#To gray scale
ImGray = ImageOps.grayscale(Im);
#Get the pixel values
pix_val = np.array(ImGray.getdata());
pix_val = pix_val.astype(np.float)
#Resize the list to grid data
size = np.shape(Im); Ny=size[0]; Nx=size[1];
pix_val = np.reshape(pix_val,(Ny,Nx));
#Scale the pixel values to actual height values
z_coord = ((Zmax-Zmin)*pix_val/255)+Zmin;
# Create x,y array
x=np.linspace(0,Lx,Nx,endpoint=True); y=np.linspace(0,Ly,Ny,endpoint=True);
# Convert Grid-data to XYZ Triplet
z=np.reshape(z_coord,np.size(z_coord)); Profile_XYZ=np.zeros((np.size(z_coord),3));
for i in range(len(z)):
    Profile_XYZ[i,:]=[x[i%len(x)], y[i//len(x)], z[i]]
#Save as .txt file
np.savetxt(Output_TextPath, Profile_XYZ, delimiter=',')        


