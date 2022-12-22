from abaqusGui import *
import Rough_DB
from abaqusConstants import ALL
import osutils, os

###########################################################################
# Class definition
###########################################################################

class RoughForm(AFXForm):
    [
        ID_WARNING,
    ] = range(AFXForm.ID_LAST, AFXForm.ID_LAST+1)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):

        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_WARNING,
        RoughForm.onCmdWarning)
        
        # Create the command and keywords.
        #
        self.cmd = AFXGuiCommand(self, method='execute', objectName='RSGen_Master', registerQuery=False)
        self.D = AFXIntKeyword(self.cmd, 'D', TRUE, 0)
        self.G = AFXIntKeyword(self.cmd, 'G', TRUE, 0)
        self.Lx = AFXFloatKeyword(self.cmd, 'Lx', TRUE, 1.0, 8)
        self.Ly = AFXFloatKeyword(self.cmd, 'Ly', TRUE, 1.0, 8)
        self.Lz = AFXFloatKeyword(self.cmd, 'Lz', TRUE, 0.05, 8)
        self.Nx = AFXIntKeyword(self.cmd, 'Nx', TRUE, 50)
        self.Ny = AFXIntKeyword(self.cmd, 'Ny', TRUE, 50)
        self.a = AFXFloatKeyword(self.cmd, 'a', TRUE, 0.01, 8)
        self.b = AFXFloatKeyword(self.cmd, 'b', TRUE, 2.0, 8)
        self.std = AFXFloatKeyword(self.cmd, 'std', TRUE, 0.005, 8)
        self.Lmin = AFXFloatKeyword(self.cmd, 'Lmin', TRUE, 0.05, 8)
        self.Lmax = AFXFloatKeyword(self.cmd, 'Lmax', TRUE, 1.0, 8)
        self.Lcut = AFXFloatKeyword(self.cmd, 'Lcut', TRUE, 0.2, 8)
        self.Le = AFXFloatKeyword(self.cmd, 'Le', TRUE, 0.01, 8)
        self.H = AFXFloatKeyword(self.cmd, 'H', TRUE, 0.7, 8)
        self.Rq = AFXFloatKeyword(self.cmd, 'Rq', TRUE, 0.002, 8)
        self.XP = AFXBoolKeyword(self.cmd, 'XP', AFXBoolKeyword.TRUE_FALSE, TRUE, FALSE)
        self.XN = AFXBoolKeyword(self.cmd, 'XN', AFXBoolKeyword.TRUE_FALSE, TRUE, FALSE)
        self.YP = AFXBoolKeyword(self.cmd, 'YP', AFXBoolKeyword.TRUE_FALSE, TRUE, FALSE)
        self.YN = AFXBoolKeyword(self.cmd, 'YN', AFXBoolKeyword.TRUE_FALSE, TRUE, FALSE)
        self.fileNameKw = AFXStringKeyword(self.cmd, 'FileName', TRUE, '')
        self.PartNameKw = AFXStringKeyword(self.cmd, 'PartName', TRUE, 'Part_Rough')
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        self.cmd.setKeywordValuesToDefaults()
        self.D.setValue(5)
        self.G.setValue(1)
        import Rough_DB
        return Rough_DB.RoughDB(self)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):
        ##############################################################
        # Show Error message when the Length input is smaller than 0 #
        ############################################################## 
        # 2D wire case
        if self.D.getValue() == 1 or self.D.getValue() == 2:
            if self.Lx.getValue()<= 0:
                showAFXErrorDialog(self.getCurrentDialog(),
                '\nThe length should be greater than zero\n')
                return False
        # 2D shell case
        elif self.D.getValue() == 3 or self.D.getValue() == 4:
            if self.Lx.getValue() <= 0 or self.Ly.getValue()<= 0:
                showAFXErrorDialog(self.getCurrentDialog(),
                '\nThe length should be greater than zero\n')
                return False
                
        # 3D shell case
        elif self.D.getValue() == 5:
            if self.Lx.getValue() <= 0 or self.Ly.getValue() <= 0 or self.Le.getValue() <= 0:
                showAFXErrorDialog(self.getCurrentDialog(),
                '\nThe length should be greater than zero\n')                  
                return False                               
        
        # 3D solid case
        elif self.D.getValue() == 6:
            if self.Lx.getValue() <= 0 or self.Ly.getValue() <= 0 or self.Lz.getValue() <= 0 or self.Le.getValue() <= 0:
                showAFXErrorDialog(self.getCurrentDialog(),
                '\nThe length should be greater than zero\n')                
                return False                                                        
                
        #############################################################
        # Show Error message when Lcut is not between Lmin and Lmax #
        #############################################################
        if self.G.getValue() == 3:
            if self.Lcut.getValue() > self.Lmax.getValue() or self.Lcut.getValue() < self.Lmin.getValue():
                showAFXErrorDialog(self.getCurrentDialog(),
                '\nThe value of Lcut should be set between Lmin and Lmax\n')                
                return False

        ##################################################################
        # Show Error message when the data type does not match the input #
        ##################################################################
        #XYZ Triplet or XY Data
        if self.G.getValue() == 4:
            #2D case
            if self.D.getValue() == 1 or self.D.getValue() == 2 or self.D.getValue() == 3 or self.D.getValue() == 4:
                import numpy as np
                file=open(self.fileNameKw.getValue())
                try:
                    Profile_pts_check=np.loadtxt(file, delimiter=",");
                    file.close()
                except:
                    Profile_pts_check=np.loadtxt(file);
                    file.close()
                    
                Profile_pts_check = np.array(Profile_pts_check)
                col_num=len(Profile_pts_check[0])
                
                if col_num !=2:
                    showAFXErrorDialog(self.getCurrentDialog(),
                    '\nCheck the input data. XY-Data should be m by 2 matrix\n')
                    return False
            #3D case
            elif self.D.getValue() == 5 or self.D.getValue() == 6:
                import numpy as np
                file=open(self.fileNameKw.getValue())
                try:
                    Profile_pts_check=np.loadtxt(file, delimiter=",");
                    file.close()
                except:
                    Profile_pts_check=np.loadtxt(file);
                    file.close()               
                Profile_pts_check = np.array(Profile_pts_check)
                col_num=len(Profile_pts_check[0])
                
                if col_num !=3:
                    showAFXErrorDialog(self.getCurrentDialog(),
                    '\nCheck the input data. XYZ Triplet data should be m by 3 matrix\n')
                    return False                    
        #Uniform Grid Data
        elif self.G.getValue() == 5:
                import numpy as np
                file=open(self.fileNameKw.getValue())
                try:
                    Profile_pts_check=np.loadtxt(file, delimiter=",");
                    file.close()
                except:
                    Profile_pts_check=np.loadtxt(file);
                    file.close()                
                Profile_pts_check = np.array(Profile_pts_check)
                col_num=len(Profile_pts_check[0])
                
                if col_num ==3:
                    showAFXErrorDialog(self.getCurrentDialog(),
                    '\nCheck the input data. Uniform grid data should be m by n matrix\n')            
                    return False
        ################################################################################
        # Show Warning message when the top surface intersects with the bottom surface #
        ################################################################################
        #2D shell case
        if self.D.getValue() == 3 or self.D.getValue() == 4:
            #Height - Gaussian            
            if self.G.getValue() == 1:
                Intersect_Gaussian = 3*self.std.getValue() - self.Ly.getValue()
                if 0 <= Intersect_Gaussian:
                    showAFXWarningDialog(self.getCurrentDialog(),
                    '\nThe top surface is likely to intersect with the bottom surface.\n\n   (1) Increase the thickness, Ly or (2) Click Yes to ignore.\n',
                    AFXDialog.YES | AFXDialog.NO,
                    self, self.ID_WARNING)
                    return False
            #Height - Weibull                     
            elif self.G.getValue() == 2:
                import numpy as np
                from math import gamma
                mean = self.a.getValue()*gamma(1+1/self.b.getValue())
                Intersect_Weibull = 2.0*mean - self.Ly.getValue()
                if 0 <= Intersect_Weibull:
                    showAFXWarningDialog(self.getCurrentDialog(),
                    '\nThe top surface is likely to intersect with the bottom surface.\n\n   (1) Increase the thickness, Ly or (2) Click Yes to ignore.\n',
                    AFXDialog.YES | AFXDialog.NO,
                    self, self.ID_WARNING)
                    return False
            #PSD             
            elif self.G.getValue() == 3:
                Intersect_PSD = 3*self.Rq.getValue() - self.Ly.getValue() 
                if 0 <= Intersect_PSD:
                    showAFXWarningDialog(self.getCurrentDialog(),
                    '\nThe top surface is likely to intersect with the bottom surface.\n\n   (1) Increase the thickness, Ly or (2) Click Yes to ignore.\n',
                    AFXDialog.YES | AFXDialog.NO,
                    self, self.ID_WARNING)
                    return False                
        #3D solid case
        elif self.D.getValue() == 6:
            #Height - Gaussian            
            if self.G.getValue() == 1:
                Intersect_Gaussian = 3*self.std.getValue() - self.Lz.getValue()
                if 0 <= Intersect_Gaussian:
                    showAFXWarningDialog(self.getCurrentDialog(),
                    '\nThe top surface is likely to intersect with the bottom surface.\n\n   (1) Increase the thickness, Lz or (2) Click Yes to ignore.\n',
                    AFXDialog.YES | AFXDialog.NO,
                    self, self.ID_WARNING)
                    return False
            #Height - Weibull                     
            elif self.G.getValue() == 2:
                import numpy as np
                from math import gamma
                mean = self.a.getValue()*gamma(1+1/self.b.getValue())
                Intersect_Weibull = 2.0*mean - self.Lz.getValue()
                if 0 <= Intersect_Weibull:
                    showAFXWarningDialog(self.getCurrentDialog(),
                    '\nThe top surface is likely to intersect with the bottom surface.\n\n   (1) Increase the thickness, Lz or (2) Click Yes to ignore.\n',
                    AFXDialog.YES | AFXDialog.NO,
                    self, self.ID_WARNING)
                    return False
            #PSD             
            elif self.G.getValue() == 3:
                Intersect_PSD = 3*self.Rq.getValue() - self.Lz.getValue() 
                if 0 <= Intersect_PSD:
                    showAFXWarningDialog(self.getCurrentDialog(),
                    '\nThe top surface is likely to intersect with the bottom surface.\n\n   (1) Increase the thickness, Lz or (2) Click Yes to ignore.\n',
                    AFXDialog.YES | AFXDialog.NO,
                    self, self.ID_WARNING)
                    return False                            

        ############################################################################
        # Show Warning message when number of element exceed 1 million for 3D case #
        ############################################################################          
        # For 3D shell case 
        if self.D.getValue() == 5:
            if self.G.getValue() == 4:
                import numpy as np
                file=open(self.fileNameKw.getValue())
                try:
                    Profile_pts_check=np.loadtxt(file, delimiter=",");
                    file.close()
                except:
                    Profile_pts_check=np.loadtxt(file);
                    file.close()                    
                Profile_pts_check = np.array(Profile_pts_check)
                Profile_pts_check.astype(float)
                x=Profile_pts_check[:,0]; y=Profile_pts_check[:,1]; z=Profile_pts_check[:,2];        
                self.Lx.setValue(abs(x[0]-x[-1])); self.Ly.setValue(abs(y[0]-y[-1]));                            
            
            X_Elnum = int(self.Lx.getValue()/self.Le.getValue())
            Y_Elnum = int(self.Ly.getValue()/self.Le.getValue())
            Total_Elnum = X_Elnum*Y_Elnum
            Message = '\nThe total number of element exceeds 1 million '+'('+str(Total_Elnum)+')' + '\n                   Are you okay to proceed?\n'
            
            if Total_Elnum >= 1000000:
                showAFXWarningDialog(self.getCurrentDialog(),
                Message,
                AFXDialog.YES | AFXDialog.NO,
                self, self.ID_WARNING)
                return False
                
        # For 3D solid case 
        elif self.D.getValue() == 6:
            if self.G.getValue() == 4:
                import numpy as np
                file=open(self.fileNameKw.getValue())
                try:
                    Profile_pts_check=np.loadtxt(file, delimiter=",");
                    file.close()
                except:
                    Profile_pts_check=np.loadtxt(file);
                    file.close()
                    
                Profile_pts_check = np.array(Profile_pts_check)
                x=Profile_pts_check[:,0]; y=Profile_pts_check[:,1]; z=Profile_pts_check[:,2];
                Profile_pts_check.astype(float)                
                self.Lx.setValue(abs(x[0]-x[-1])); self.Ly.setValue(abs(y[0]-y[-1]));
                
            X_Elnum = int(self.Lx.getValue()/self.Le.getValue())
            Y_Elnum = int(self.Ly.getValue()/self.Le.getValue())
            Z_Elnum = int(self.Lz.getValue()/self.Le.getValue())
            Total_Elnum = X_Elnum*Y_Elnum*Z_Elnum
            Message = '\nThe total number of element exceeds 1 million '+'('+str(Total_Elnum)+')' + '\n                   Are you okay to proceed?\n'
            
            if Total_Elnum >= 1000000:
                showAFXWarningDialog(self.getCurrentDialog(),
                Message,
                AFXDialog.YES | AFXDialog.NO,
                self, self.ID_WARNING)
                return False
        
        return TRUE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    def onCmdWarning(self, sender, sel, ptr):

        if sender.getPressedButtonId() == \
            AFXDialog.ID_CLICKED_YES:
                self.issueCommands()