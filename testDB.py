from abaqusGui import *
import testForm
from abaqusConstants import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

###########################################################################
# Class definition                                                        #
###########################################################################

class TestDB(AFXDataDialog):
    [
        ID_CLICKED_TUTORIAL,
    ] = range(AFXDataDialog.ID_LAST, AFXDataDialog.ID_LAST+1)

    #----------------------------------------------------------------------
    def __init__(self, form):

        Main_DB = AFXDataDialog.__init__(self, form, 'Rough Surface Generator plug-in',
            self.OK|self.APPLY|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)            
        
        self.TutorialDB = None
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_TUTORIAL, TestDB.onCmdSelect)
        
        ###################
        ### First page  ###
        ###################
        tabBook1 = FXTabBook(self, None, 0, LAYOUT_FILL_X)
        FXTabItem(tabBook1, ' Geometry ')
        tab1Frame = FXHorizontalFrame(tabBook1,FRAME_RAISED|FRAME_SUNKEN)
                     
        #For modeling dimensionality
        #                                  x  y  w  h  pl  pr  pt  pb        
        vf = FXVerticalFrame(tab1Frame, 0, 0, 0, 0, 0, 12, 10, 10, 10)
        #                                                                                        x  y  w  h  pl pr pt pb
        Top_title = FXLabel(vf,' 01. Input geometric information ',None, LABEL_NORMAL, 0, 0, 0, 0, 5, 0, 5, 10)
        Top_title.setFont( getAFXFont(FONT_BOLD) )
                
        #For Part Name
        #                                                               x  y  w  h  pl pr pt pb
        hf_part = FXHorizontalFrame(vf)
        #gb0 = FXGroupBox(hf_part,'Part Name',FRAME_GROOVE|LAYOUT_FILL_X, 0, 0, 0, 0, 4, 205, 3, 7)
        #                                                                     x  y  w  h  pl pr pt pb
        Name_Field = AFXTextField(hf_part, 23, ' Part Name: ', form.PartNameKw, 0, AFXTEXTFIELD_STRING)
        
        
        hf = FXHorizontalFrame(vf)
        sw = FXSwitcher(vf)
        #                                                               x  y  w  h  pl pr pt pb
        gb = FXGroupBox(hf,'Modeling Space',FRAME_GROOVE|LAYOUT_FILL_X, 0, 0, 0, 0, 4, 13, 3, 7)

        #                                                                                         x  y  w  h  pl pr pt pb
        FXRadioButton(gb,'3D', sw, FXSwitcher.ID_OPEN_FIRST, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 6, 26, 10, 5)
        FXRadioButton(gb,'2D-Planar', sw,FXSwitcher.ID_OPEN_FIRST+1, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 100, 9, 10, 5)
        FXRadioButton(gb,'2D-Axisymmetric', sw, FXSwitcher.ID_OPEN_FIRST+2, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 85, 5, 10, 5)
        
        #Choose the shape of surface                                  x  y  w  h  pl pr pt pb 
        gb1 = FXGroupBox(sw, 'Shape', FRAME_GROOVE|LAYOUT_SIDE_RIGHT, 0, 0, 0, 0, 4, 249, 3, 0)

        #                                                                           x  y  w  h  pl pr pt pb
        Shell_3D_btn=FXRadioButton(gb1, 'Shell', form.D, 5, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 6, 14, 10, 5)
        Solid_3D_btn=FXRadioButton(gb1, 'Solid', form.D, 6, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 101, 6, 10, 5)      
  
        gb2 = FXGroupBox(sw, 'Shape', FRAME_GROOVE|LAYOUT_SIDE_RIGHT, 0, 0, 0, 0, 4, 162, 3, 0)

        #                                                                          x  y  w  h  pl pr pt pb
        Wire_2DPlanar_btn=FXRadioButton(gb2, 'Wire', form.D, 1, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 6, 15, 10, 5)
        Shell_2DPlanar_btn=FXRadioButton(gb2, 'Shell', form.D, 3, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 102, 5, 10, 5) 
        
        gb3 = FXGroupBox(sw, 'Shape', FRAME_GROOVE|LAYOUT_SIDE_RIGHT, 0, 0, 0, 0, 4, 162, 3, 5)

        Wire_2DAxis_btn=FXRadioButton(gb3, 'Wire', form.D, 2, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 6, 15, 10, 5)
        Shell_2DAxis_btn=FXRadioButton(gb3, 'Shell', form.D, 4, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 102, 5, 10, 5)

        #
        #Option for windowing function        
        
        hf_window = FXHorizontalFrame(vf)
        #                                                                                                      x  y  w  h  pl pr pt pb
        gb_window = FXGroupBox(hf_window,'Rectangular side wall (optional for 3D)',FRAME_GROOVE|LAYOUT_FILL_X, 0, 0, 0, 0, 6, 59, 3, 7)
        hf = FXHorizontalFrame(gb_window)       
        #                                                                                                                                                    x  y  w  h  pl pr pt pb
        XP_btn = FXCheckButton(hf, '+X side\tSide wall normal to the positive X-direction is generated in rectangular shape',form.XP, 0, CHECKBUTTON_NORMAL, 0, 0, 0, 0, 1, 50, 10, 5)
        XN_btn = FXCheckButton(hf, '-X side\tSide wall normal to the negative X-direction is generated in rectangular shape',form.XN, 0, CHECKBUTTON_NORMAL, 0, 0, 0, 0, 0, 50, 10, 5)
        YP_btn = FXCheckButton(hf, '+Y side\tSide wall normal to the positive Y-direction is generated in rectangular shape',form.YP, 0, CHECKBUTTON_NORMAL, 0, 0, 0, 0, 0, 50, 10, 5)
        YN_btn = FXCheckButton(hf, '-Y side\tSide wall normal to the negative Y-direction is generated in rectangular shape',form.YN, 0, CHECKBUTTON_NORMAL, 0, 0, 0, 0, 0, 5, 10, 5)        
        

        hf_space = FXHorizontalFrame(vf)
        space = FXLabel(hf,'\n')
        space.setFont( getAFXFont(FONT_SMALL) )        
        hf3 = FXHorizontalFrame(vf)
        Signature = FXLabel(hf3,'Developed by Youngbin LIM')
        Signature.setFont( getAFXFont(FONT_MONOSPACE) )
        sp = FXLabel(hf3,'                                                   ')
        sp.setFont( getAFXFont(FONT_SMALL) )
        Tips_btn_1st = FXButton(hf3, ' Tutorial ', None, self, self.ID_CLICKED_TUTORIAL)
        
        ###################
        ### Second page ###
        ###################
        FXTabItem(tabBook1, ' Surface Generator ')
        #                                                               x  y  w  h  pl pr pt pb
        tab2Frame = FXVerticalFrame(tabBook1,FRAME_RAISED|FRAME_SUNKEN, 0, 0, 0, 0, 4, 10,  -7, 5)
        tabBook2 = FXTabBook(tab2Frame, None, 0, LAYOUT_FILL_X)

        vf_top = FXVerticalFrame(tab2Frame, 0, 0, 0, 0, 0, 12, 10, 10, 10)
        #                                                                                      x  y  w  h  pl pr pt pb
        Top_title = FXLabel(vf_top,' 02. Select type of surface generator',None, LABEL_NORMAL, 0, 0, 0, 0, 5, 0, 5, 12)
        Top_title.setFont( getAFXFont(FONT_BOLD) )        
        
        hf_top = FXHorizontalFrame(vf_top)
        sw2 = FXSwitcher(vf_top)
        
        #Surface Generator type
        #                                                                    x  y  w  h  pl pr pt pb
        gb4 = FXGroupBox(hf_top,'Surface Generation Algorithm',FRAME_GROOVE, 0, 0, 0, 0, 4, 13, 3, 7)
        #                                                                                                            x  y  w  h  pl pr pt pb
        FXRadioButton(gb4,'Height Distribution\tRandom points are sampled from height distribution\nSampling points are positioned in uniform grid and spline interpolated', sw2, FXSwitcher.ID_OPEN_FIRST, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 6, 15, 10,5)
        FXRadioButton(gb4,'PSD\tPoints on rough surface are generated from Power Spectral Density function', sw2, FXSwitcher.ID_OPEN_FIRST+1, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 65, 8, 10, 5)
        FXRadioButton(gb4,'Import Profile Data\tImport measured profile data', sw2, FXSwitcher.ID_OPEN_FIRST+2, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 70, 1, 10, 5)
        
        
        #Page for Height Distribution
        #                                                         x  y  w  h  pl pr pt pb
        gb_HD = FXGroupBox(sw2,'Distribution type', FRAME_GROOVE, 0, 0, 0, 0, 4, 100, 3, 5)
        #                              x  y  w  h  pl pr pt pb
        vf = FXVerticalFrame(gb_HD, 0, 0, 0, 0, 0, 0, 0, 3, 0)
        hf = FXHorizontalFrame(vf, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        #                                                                            x  y  w  h  pl pr pt pb
        Gaussian_btn = FXRadioButton(hf,'Gaussian', form.G, 1, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 6, 20, 5, 0)
        Weibull_btn = FXRadioButton(hf,'Weibull', form.G, 2, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 115, 0, 5, 0)
        
        #Page for PSD
        #                                        x  y  w  h  pl pr pt pb
        gb_PSD = FXGroupBox(sw2,'', FRAME_GROOVE, 0, 0, 0, 0, 4, 277, 3, 3)
        
        vf = FXVerticalFrame(gb_PSD, 0, 0, 0, -10, 0, 0, 0)
        hf = FXHorizontalFrame(vf, 0, 0, 0, 0, -10, 0, 0, 0)
        #                                                                                                               x  y  w  h  pl pr pt pb
        PSD_Select = FXRadioButton(hf,'Automatically selected for PSD', form.G, 3, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 6, 0, 20, 0)

        #Page for Profile Data
        #                                          x  y  w  h  pl pr pt pb
        gb_Prof = FXGroupBox(sw2,'Data type', FRAME_GROOVE, 0, 0, 0, 0, 4, 108, 3, 3)
        
        vf = FXVerticalFrame(gb_Prof, 0, 0, 0, -10, 0, 0, 0)
        hf = FXHorizontalFrame(vf, 0, 0, 0, 0, -10, 0, 0, 0)
        #                                                                               x  y  w  h  pl pr pt pb
        XYZ_Triplet_btn = FXRadioButton(hf,'XYZ Triplet\tFor 3D case, data points are listed in x,y,z format (m by 3 matrix)\nShould be in the ascending order of x and y\nFor 2D case, simply XY-data (m by 2 matrix)\n Also need to be in the ascending order of x', form.G, 4, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 6, 20, 5, 0)
        Uniform_Grid_btn = FXRadioButton(hf,'Uniform Grid\tData includes z coordiate data positioned in uniform grid (m by n matrix)\nLength in x and y needs to be specified', form.G, 5, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 104, 0, 5, 0)
               
        ##Bottom line for page 2
        #hf3 = FXHorizontalFrame(vf_top)
        #space = FXLabel(hf3,'\n\n\n\n\n')
        #space.setFont( getAFXFont(FONT_SMALL) )
        #hf4 = FXHorizontalFrame(vf_top)
        #Contact = FXLabel(hf4,'Contact: Youngbin.LIM@3ds.com')
        #Contact.setFont( getAFXFont(FONT_MONOSPACE) ) 
                
        ###################
        ###  Third page ###
        ###################
                                       
        FXTabItem_3 = FXTabItem(tabBook1, ' Parameter ')
        tab3Frame_3 = FXHorizontalFrame(tabBook1,FRAME_RAISED|FRAME_SUNKEN)
        #                                                x  y  w  h  pl  pr  pt pb
        vf_top_2 = FXVerticalFrame(tab3Frame_3, 0, 0, 0, 0, 0, 15, 10, 7, 10)
        hf_top_2 = FXHorizontalFrame(vf_top_2)
        
        #Shows nothing when dimensionality and surface generator is not selected        
        Show_nothing = FXLabel(hf_top_2,'               Please select dimensionality and type of surface generator',None, LABEL_NORMAL, 0, 0, 0, 0, 2, 0, 5, 10)        
        Show_nothing.setFont( getAFXFont(FONT_BOLD) )
        
        #GroupBox for size parameters
        #                                                   x  y  w  h  pl pr pt pb
        gb_size = FXGroupBox(vf_top_2,'Size', FRAME_GROOVE, 0, 0, 0, 0, 4, 12, 3, 3, 3)
        
        vf = FXVerticalFrame(gb_size, 0, 0, 0, -10, 0, 0, 0)
        hf = FXHorizontalFrame(vf, 0, 0, 0, 0, -10, 0, 0, 0)
        #                                                                     x  y  w  h  pl pr pt pb
        Lx_input = AFXTextField(hf, 8, ' Lx:\tLength in x-direction', form.Lx, 0, AFXTEXTFIELD_FLOAT)
        Ly_input = AFXTextField(hf, 8, '         Ly\tLength in y-direction:', form.Ly, 0, AFXTEXTFIELD_FLOAT)
        Lz_input = AFXTextField(hf, 8, '         Lz\tLength in z-direction:', form.Lz, 0, AFXTEXTFIELD_FLOAT)
        Le_input = AFXTextField(hf, 8, '         Le:\tApproximate element size\nNeeds to be defined for 3D case\n as direct geometry generation is not supported', form.Le, 0, AFXTEXTFIELD_FLOAT)
        
        space = FXLabel(vf_top_2,'')
        space.setFont( getAFXFont(FONT_SMALL) )
        
        #GroupBox for Roughness parameters for Height Distribution
        #                                                    x  y  w  h  pl pr pt pb
        gb_rough = FXGroupBox(vf_top_2,'Height Distribution', FRAME_GROOVE, 0, 0, 0, 0, 4, 10, 3, 3)

        vf1 = FXVerticalFrame(gb_rough, 0, 0, 0, -10, 0, 0, 0)
        hf = FXHorizontalFrame(vf1, 0, 0, 0, 0, -10, 0, 0, 0)     
        #                                                                          x  y  w  h  pl pr pt pb
        Nx_input = AFXTextField(hf, 6, ' Nx:   \tNumber of sampling points in x-direction', form.Nx, 0, AFXTEXTFIELD_INTEGER)
        Ny_input = AFXTextField(hf, 6, '  Ny:   \tNumber of sampling points in y-direction', form.Ny, 0, AFXTEXTFIELD_INTEGER)
        Std_input = AFXTextField(hf, 6, '   std: \tStandard deviation for Gaussian distribution\nThe average is automatically set to z=0', form.std, 0, AFXTEXTFIELD_FLOAT)
        a_input = AFXTextField(hf, 6, '    a:\tWeibull distribution parameter a,\n where cumulative distribution function, F\n is defined as F = 1 - exp[-(x/a)^b]', form.a, 0, AFXTEXTFIELD_FLOAT)
        b_input = AFXTextField(hf, 6, '     b:\tWeibull distribution parameter b,\n where cumulative distribution function, F\n is defined as F = 1 - exp[-(x/a)^b]', form.b, 0, AFXTEXTFIELD_FLOAT)
        
        
        space2 = FXLabel(vf_top_2,'')
        space2.setFont( getAFXFont(FONT_SMALL) )        
        
        #GroupBox for Roughness parameters for PSD
        gb_PSD_input = FXGroupBox(vf_top_2,'Roughness PSD', FRAME_GROOVE, 0, 0, 0, 0, 4, 10, 3, 3)   

        vf2 = FXVerticalFrame(gb_PSD_input, 0, 0, 0, -10, 0, 0, 0)
        hf = FXHorizontalFrame(vf2, 0, 0, 0, 0, -10, 0, 0, 0)
       
        Lmin_input = AFXTextField(hf, 6, ' Lmin:\tMinimum wave length scale of rough surface', form.Lmin, 0, AFXTEXTFIELD_FLOAT)
        Lmax_input = AFXTextField(hf, 6, '  Lmax:\tMaximum wave length scale of rough surface', form.Lmax, 0, AFXTEXTFIELD_FLOAT)
        Lcut_input = AFXTextField(hf, 6, '  Lcut:\tCut-off wave length', form.Lcut, 0, AFXTEXTFIELD_FLOAT)
        H_input = AFXTextField(hf, 6, '   H:\tHurst exponent, 0 < = H < = 1\n It defines the slope of PSD in Log-Log scale', form.H, 0, AFXTEXTFIELD_FLOAT)
        Rq_input = AFXTextField(hf, 6, '   Rq:\tStandard deviation of height\nThe average is automatically set to z=0', form.Rq, 0, AFXTEXTFIELD_FLOAT)
 
        #space3 = FXLabel(vf_top_2,'')
        #space3.setFont( getAFXFont(FONT_SMALL) )
        #space4 = FXLabel(vf_top_2,'')
        #space4.setFont( getAFXFont(FONT_SMALL) )
                        
        ###################
        ###  Forth page ###
        ###################        
        
        FXTabItem_4 = FXTabItem(tabBook1, ' Profile Data ')
        tab4Frame = FXHorizontalFrame(tabBook1,FRAME_RAISED|FRAME_SUNKEN)
        #                                        x  y  w  h  pl  pr  pt pb
        vf_top_3 = FXVerticalFrame(tab4Frame, 0, 0, 0, 0, 0, 15, 10, 7, 10)
        hf_top_3 = FXHorizontalFrame(vf_top_3)

        Show_nothing_2 = FXLabel(hf_top_3,'               Please select dimensionality and type of surface generator',None, LABEL_NORMAL, 0, 0, 0, 0, 2, 0, 5, 10)        
        Show_nothing_2.setFont( getAFXFont(FONT_BOLD) )
        
        #GroupBox for txt data
        #                                                              x  y  w  h  pl pr pt pb
        gb_csv = FXGroupBox(vf_top_3,'Import .txt file', FRAME_GROOVE, 0, 0, 0, 0, 4, 47, 3, 3)
        
        vf_csv = FXVerticalFrame(gb_csv, 0, 0, 0, -10, 0, 0, 0)
        #                                     x  y  w  h  pl pr pt pb
        hf_csv = FXHorizontalFrame(vf_csv, 0, 0, 0, 0, 0, 0, 0, 15, 10)
        hf2_csv = FXHorizontalFrame(vf_csv, 0, 0, 0, 0, 0, 0, 0, 0, 10)
                
        #File Selector
        fileHandler = FileDBFileHandler(form, 'fileName', 'Text file (seperated by "," or "tab") (*.txt)')
        fileTextHf = FXHorizontalFrame(p=hf_csv, opts=0, x=0, y=0, w=0, h=0, pl=4, pr=0, pt=0, pb=5)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        fileTextHf.setSelector(99)
        File_Text = AFXTextField(p=fileTextHf, ncols=46, labelText='File name:', tgt=form.fileNameKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=fileTextHf, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
                
        Lx_input_2 = AFXTextField(hf2_csv, 8, ' Lx:\tLength in x-direction', form.Lx, 0, AFXTEXTFIELD_FLOAT)
        Ly_input_2 = AFXTextField(hf2_csv, 8, '   Ly:\tLength in y-direction:', form.Ly, 0, AFXTEXTFIELD_FLOAT)
        Lz_input_2 = AFXTextField(hf2_csv, 8, '    Lz:\tLength in z-direction:', form.Lz, 0, AFXTEXTFIELD_FLOAT)
        Le_input_2 = AFXTextField(hf2_csv, 8, '   Le:\tApproximate element size\nNeeds to be defined for 3D case\n as direct geometry generation is not supported', form.Le, 0, AFXTEXTFIELD_FLOAT)


        ##Bottom Note
        #
        Note_Profile = AFXNote(vf_top_3,'Profile data should contain numbers only (no title, column name, etc.)')
        #space3.setFont( getAFXFont(FONT_SMALL) )
        #space4 = FXLabel(vf_top_3,'')
        #space4.setFont( getAFXFont(FONT_SMALL) )
        
        #For processUpdates
        self.form = form
        self.gb_PSD = gb_PSD
        self.sw = sw
        self.sw2 = sw2
        self.PSD_Select = PSD_Select
        self.Gaussian_btn = Gaussian_btn
        self.Weibull_btn  = Weibull_btn 
        self.Show_nothing = Show_nothing
        self.Show_nothing_2 = Show_nothing_2
        self.gb_size = gb_size
        self.Lx_input = Lx_input
        self.Ly_input = Ly_input
        self.Lz_input = Lz_input
        self.Le_input = Le_input
        self.Lx_input_2 = Lx_input_2
        self.Ly_input_2 = Ly_input_2
        self.Lz_input_2 = Lz_input_2
        self.Le_input_2 = Le_input_2
        self.Shell_3D_btn = Shell_3D_btn
        self.Solid_3D_btn = Solid_3D_btn
        self.Wire_2DPlanar_btn =Wire_2DPlanar_btn
        self.Shell_2DPlanar_btn=Shell_2DPlanar_btn
        self.Wire_2DAxis_btn= Wire_2DAxis_btn
        self.Shell_2DAxis_btn=Shell_2DAxis_btn 
        
        self.Nx_input = Nx_input
        self.Ny_input = Ny_input
        self.Std_input = Std_input
        self.a_input = a_input
        self.b_input = b_input
        
        self.Lmin_input = Lmin_input
        self.Lmax_input = Lmax_input
        self.Lcut_input = Lcut_input
        self.H_input =  H_input 
        self.Rq_input = Rq_input
        
        self.gb_window = gb_window
        self.XP_btn = XP_btn
        self.XN_btn = XN_btn
        self.YP_btn = YP_btn
        self.YN_btn = YN_btn
        self.gb_rough = gb_rough
        self.gb_PSD_input = gb_PSD_input
        self.gb_csv = gb_csv
        self.Note_Profile = Note_Profile
        
        self.Uniform_Grid_btn = Uniform_Grid_btn
        self.XYZ_Triplet_btn = XYZ_Triplet_btn
        self.File_Text = File_Text
        
#    #----------------------------------------------------------------------

    def processUpdates(self):
        #Automatically select Surface generator if Surface Generation Alogrithm is changed
        if self.sw2.getCurrent() == 1:
            self.PSD_Select.setCheck()
            self.form.G.setValue(3)
        elif self.sw2.getCurrent() == 0 and self.Gaussian_btn.getCheck() == False and self.Weibull_btn.getCheck() == False:
            self.Gaussian_btn.setCheck()
            self.form.G.setValue(1)
        elif self.sw2.getCurrent() == 2 and self.Uniform_Grid_btn.getCheck() == False and self.XYZ_Triplet_btn.getCheck() == False:
            self.XYZ_Triplet_btn.setCheck()
            self.form.G.setValue(4)            
        
        #Automatically select Dimensionality if Modeling Space is changed
        if self.sw.getCurrent() == 0 and self.Shell_3D_btn.getCheck() == False and self.Solid_3D_btn.getCheck() == False:
            self.Shell_3D_btn.setCheck()
            self.form.D.setValue(5)            
        elif self.sw.getCurrent() == 1 and self.Wire_2DPlanar_btn.getCheck() == False and self.Shell_2DPlanar_btn.getCheck() == False:
            self.Wire_2DPlanar_btn.setCheck()
            self.form.D.setValue(1)
        elif self.sw.getCurrent() == 2 and self.Wire_2DAxis_btn.getCheck() == False and self.Shell_2DAxis_btn.getCheck() == False:
            self.Wire_2DAxis_btn.setCheck()
            self.form.D.setValue(2)
                       
        #Activate windowing for 3D case
        if self.sw.getCurrent() == 0:
            self.gb_window.show()            
            self.XP_btn.show()
            self.XN_btn.show()
            self.YP_btn.show()
            self.YN_btn.show()
            self.gb_window.enable()
            self.XP_btn.enable()
            self.XN_btn.enable()
            self.YP_btn.enable()
            self.YN_btn.enable()
            self.Uniform_Grid_btn.enable()
            self.XYZ_Triplet_btn.setText('XYZ Triplet')
        elif self.sw.getCurrent() == 1 or self.sw.getCurrent() == 2:
           self.gb_window.show()            
           self.XP_btn.show()
           self.XN_btn.show()
           self.YP_btn.show()
           self.YN_btn.show()
           self.gb_window.disable()
           self.XP_btn.disable()
           self.XN_btn.disable()
           self.YP_btn.disable()
           self.YN_btn.disable()
           self.Uniform_Grid_btn.disable()
           self.XYZ_Triplet_btn.setText('XY-Data    ')
        #Shows nothing when dimensionality and surface generator is not selected
        if self.form.D.getValue() == 0 or self.form.G.getValue() == 0:            
            self.Show_nothing.show()
            self.Show_nothing_2.show()
            self.gb_size.hide()
            self.gb_rough.hide()
            self.gb_PSD_input.hide()
            self.gb_csv.hide()
                        
        #2D-wire
        elif self.form.D.getValue() == 1 or self.form.D.getValue() == 2:
            #Input tab for Gaussian distribution, G = 1
            if self.form.G.getValue() == 1:
                #Size tab
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()
                self.Lx_input.enable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()  
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.enable()
                self.Nx_input.enable()
                self.Ny_input.disable()
                self.Std_input.enable()
                self.a_input.disable()
                self.b_input.disable()
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')
                self.gb_csv.show()
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()                
                #Tips button
                #self.Tips_btn_3rd.show()
                #self.Tips_btn_4th.hide()
            #Input tab for Weibull distribution, G = 2    
            elif self.form.G.getValue() == 2:
                #Size tab
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.enable()
                self.Nx_input.enable()
                self.Ny_input.disable()                
                self.Std_input.disable()
                self.a_input.enable()
                self.b_input.enable()                
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')                
                self.gb_csv.show()
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()                
                #Tips button
                #self.Tips_btn_3rd.show() 
                #self.Tips_btn_4th.hide()                
            #Input tab for PSD, G = 3
            elif self.form.G.getValue() == 3:
                #Size tab
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab                
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable()
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable() 
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.enable()
                self.Lmin_input.enable()
                self.Lmax_input.enable()
                self.Lcut_input.enable()
                self.H_input.enable() 
                self.Rq_input.enable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')
                self.gb_csv.show()
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()                
                #Tips button
                #self.Tips_btn_3rd.show()
                #self.Tips_btn_4th.hide()                
            #Input tab for Profile Data - XYZ Triplet, G = 4
            elif self.form.G.getValue() == 4:
                #Size tab
                self.Show_nothing.setText('                                       Please go to Profile Data tab')
                self.gb_size.show()               
                self.gb_size.disable()
                self.Lx_input.disable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab                
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable()
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable() 
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('03. Import text file to generate rough surface')
                self.gb_csv.show()
                self.gb_csv.enable()
                self.File_Text.show()
                self.File_Text.enable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.enable()                
                #Tips button
                #self.Tips_btn_3rd.hide()
                #self.Tips_btn_4th.show()                
            #Input tab for Profile Data - Uniform Grid, G = 5
            elif self.form.G.getValue() == 5:
                #Size tab
                self.Show_nothing.setText('                                       Please go to Profile Data tab')
                self.gb_size.show()
                self.gb_size.disable()
                self.Lx_input.disable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab                
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable()
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable() 
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('03. Import text file to generate rough surface')
                self.gb_csv.show()
                self.gb_csv.enable()
                self.File_Text.show()
                self.File_Text.enable()
                self.Lx_input_2.enable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()   
                self.Note_Profile.enable()                
                #Tips button
                #self.Tips_btn_3rd.hide()
                #self.Tips_btn_4th.show()                
        #2D-shell
        elif self.form.D.getValue() == 3 or self.form.D.getValue() == 4: 
            #Input tab for Gaussian distribution, G = 1
            if self.form.G.getValue() == 1:
                #Size tab
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.enable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.enable()
                self.Nx_input.enable()
                self.Ny_input.disable()
                self.Std_input.enable()
                self.a_input.disable()
                self.b_input.disable()                
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')
                self.gb_csv.show()
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()                
                #Tips button
                #self.Tips_btn_3rd.show()
                #self.Tips_btn_4th.hide()                
            #Input tab for Weibull distribution, G = 2    
            elif self.form.G.getValue() == 2:
                #Size tab
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.enable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.enable()
                self.Nx_input.enable()
                self.Ny_input.disable() 
                self.Std_input.disable()
                self.a_input.enable()
                self.b_input.enable()   
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')
                self.gb_csv.hide() 
                #Tips button
                #self.Tips_btn_3rd.show()
                self.gb_csv.show()
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()  
                self.Note_Profile.disable()                
            #Input tab for PSD, G = 3
            elif self.form.G.getValue() == 3:
                #Size tab
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.enable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable() 
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable()   
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.enable()
                self.Lmin_input.enable()
                self.Lmax_input.enable()
                self.Lcut_input.enable()
                self.H_input.enable() 
                self.Rq_input.enable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')                
                self.gb_csv.show()
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()                
                #Tips button
                #self.Tips_btn_3rd.show()
                #self.Tips_btn_4th.hide()
            #Input tab for Profile Data - XYZ Triplet, G = 4
            elif self.form.G.getValue() == 4:
                #Size tab
                self.Show_nothing.setText('                                       Please go to Profile Data tab')
                self.gb_size.show()
                self.gb_size.disable()
                self.Lx_input.disable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab                
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable()
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable() 
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('03. Import text file to generate rough surface')
                self.gb_csv.show()
                self.gb_csv.enable()
                self.File_Text.show()
                self.File_Text.enable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.enable()
                self.Lz_input_2.disable()                
                self.Le_input_2.disable()
                self.Note_Profile.enable()                
                #Tips button
                #self.Tips_btn_3rd.hide()
                #self.Tips_btn_4th.show()                
            #Input tab for Profile Data - Uniform Grid, G = 5
            elif self.form.G.getValue() == 5:
                #Size tab
                self.Show_nothing.setText('                                       Please go to Profile Data tab')
                self.gb_size.show()
                self.gb_size.disable()
                self.Lx_input.disable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab                
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable()
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable() 
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('03. Import text file to generate rough surface')
                self.gb_csv.show()
                self.gb_csv.enable()
                self.File_Text.show()
                self.File_Text.enable()                
                self.Lx_input_2.enable()                
                self.Ly_input_2.enable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.enable()                
                #Tips button
                #self.Tips_btn_3rd.hide()
                #self.Tips_btn_4th.show()                
        #3D-shell
        elif self.form.D.getValue() == 5:          
            #Input tab for Gaussian distribution, G = 1
            if self.form.G.getValue() == 1:
                #Size tab
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.enable()
                self.Lz_input.disable()
                self.Le_input.enable()
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.enable()
                self.Nx_input.enable()
                self.Ny_input.enable()
                self.Std_input.enable()
                self.a_input.disable()
                self.b_input.disable()                
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')                
                self.gb_csv.show()
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()                
                #Tips button
                #self.Tips_btn_3rd.show()
                #self.Tips_btn_4th.hide()                
            #Input tab for Weibull distribution, G = 2    
            elif self.form.G.getValue() == 2:
                #Size tab
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.enable()
                self.Lz_input.disable()
                self.Le_input.enable()
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.enable()
                self.Nx_input.enable()
                self.Ny_input.enable() 
                self.Std_input.disable()
                self.a_input.enable()
                self.b_input.enable()   
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')                
                self.gb_csv.show()
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()                
                #Tips button
                #self.Tips_btn_3rd.show()
                #self.Tips_btn_4th.hide()                
            #Input tab for PSD, G = 3
            elif self.form.G.getValue() == 3:
                #Size tab
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.enable()
                self.Lz_input.disable()
                self.Le_input.enable()
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable() 
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable()   
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.enable()
                self.Lmin_input.enable()
                self.Lmax_input.enable()
                self.Lcut_input.enable()
                self.H_input.enable() 
                self.Rq_input.enable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')                
                self.gb_csv.show()
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()
                #Tips button
                #self.Tips_btn_3rd.show()
                #self.Tips_btn_4th.hide()                
            #Input tab for Profile Data - XYZ Triplet, G = 4
            elif self.form.G.getValue() == 4:
                #Size tab
                self.Show_nothing.setText('                                       Please go to Profile Data tab')
                self.gb_size.show()
                self.gb_size.disable()
                self.Lx_input.disable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab                
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable()
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable() 
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('03. Import text file to generate rough surface')
                self.gb_csv.show()
                self.gb_csv.enable()
                self.File_Text.show()
                self.File_Text.enable()                
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()                
                self.Le_input_2.enable()
                self.Note_Profile.enable()
                #Tips button
                #self.Tips_btn_3rd.hide()
                #self.Tips_btn_4th.show()
            #Input tab for Profile Data - Uniform Grid, G = 5
            elif self.form.G.getValue() == 5:
                #Size tab
                self.Show_nothing.setText('                                       Please go to Profile Data tab')
                self.gb_size.show()
                self.gb_size.disable()
                self.Lx_input.disable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab                
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable()
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable() 
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('03. Import text file to generate rough surface')
                self.gb_csv.show()
                self.gb_csv.enable()
                self.File_Text.show()
                self.File_Text.enable()                
                self.Lx_input_2.enable()                
                self.Ly_input_2.enable()
                self.Lz_input_2.disable()
                self.Le_input_2.enable()
                self.Note_Profile.enable() 
                #Tips button
                #self.Tips_btn_3rd.hide()
                #self.Tips_btn_4th.show()                
        #3D-solid
        elif self.form.D.getValue() == 6:                
            #Input tab for Gaussian distribution, G = 1
            if self.form.G.getValue() == 1:
                #Size tab
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.enable()
                self.Lz_input.enable()
                self.Le_input.enable()
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.enable()
                self.Nx_input.enable()
                self.Ny_input.enable()
                self.Std_input.enable()
                self.a_input.disable()
                self.b_input.disable()                
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')                
                self.gb_csv.show()                
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()
                #Tips button
                #self.Tips_btn_3rd.show()
                #self.Tips_btn_4th.hide()                
            #Input tab for Weibull distribution, G = 2    
            elif self.form.G.getValue() == 2:
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.enable()
                self.Lz_input.enable()
                self.Le_input.enable()
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.enable()
                self.Nx_input.enable()
                self.Ny_input.enable() 
                self.Std_input.disable()
                self.a_input.enable()
                self.b_input.enable()   
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')                
                self.gb_csv.show()                
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()
                #Tips button
                #self.Tips_btn_3rd.show()
                #self.Tips_btn_4th.hide()                
            #Input tab for PSD, G = 3
            elif self.form.G.getValue() == 3:
                self.Show_nothing.setText('03. Define parameters to generate rough surface')
                self.gb_size.show()
                self.gb_size.enable()                
                self.Lx_input.enable()
                self.Ly_input.enable()
                self.Lz_input.enable()
                self.Le_input.enable()
                #Height distrinution tab
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable() 
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable()   
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.enable()
                self.Lmin_input.enable()
                self.Lmax_input.enable()
                self.Lcut_input.enable()
                self.H_input.enable() 
                self.Rq_input.enable()
                #Profile Data tab
                self.Show_nothing_2.setText('                                       Please go to Parameter tab')                
                self.gb_csv.show()                
                self.gb_csv.disable()
                self.File_Text.show()
                self.File_Text.disable()
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.disable()
                self.Le_input_2.disable()
                self.Note_Profile.disable()
                #Tips button
                #self.Tips_btn_3rd.show()
                #self.Tips_btn_4th.hide()                          
            #Input tab for Profile Data - XYZ Triplet, G = 4
            elif self.form.G.getValue() == 4:
                #Size tab
                self.Show_nothing.setText('                                       Please go to Profile Data tab')
                self.gb_size.show()
                self.gb_size.disable()
                self.Lx_input.disable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab                
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable()
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable() 
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('03. Import text file to generate rough surface')
                self.gb_csv.show()
                self.gb_csv.enable()
                self.File_Text.show()
                self.File_Text.enable()                
                self.Lx_input_2.disable()                
                self.Ly_input_2.disable()
                self.Lz_input_2.enable()                
                self.Le_input_2.enable()
                self.Note_Profile.enable()
                #Tips button
                #self.Tips_btn_3rd.hide()
                #self.Tips_btn_4th.show()                
            #Input tab for Profile Data - Uniform Grid, G = 5
            elif self.form.G.getValue() == 5:
                #Size tab
                self.Show_nothing.setText('                                       Please go to Profile Data tab')
                self.gb_size.show()
                self.gb_size.disable()
                self.Lx_input.disable()
                self.Ly_input.disable()
                self.Lz_input.disable()
                self.Le_input.disable()
                #Height distrinution tab                
                self.gb_rough.show()
                self.gb_rough.disable()
                self.Nx_input.disable()
                self.Ny_input.disable()
                self.Std_input.disable()
                self.a_input.disable()
                self.b_input.disable() 
                #PSD tab
                self.gb_PSD_input.show()
                self.gb_PSD_input.disable()
                self.Lmin_input.disable()
                self.Lmax_input.disable()
                self.Lcut_input.disable()
                self.H_input.disable() 
                self.Rq_input.disable()
                #Profile Data tab
                self.Show_nothing_2.setText('03. Import text file to generate rough surface')
                self.gb_csv.show()
                self.gb_csv.enable()
                self.File_Text.show()
                self.File_Text.enable()                
                self.Lx_input_2.enable()                
                self.Ly_input_2.enable()
                self.Lz_input_2.enable()
                self.Le_input_2.enable()
                self.Note_Profile.enable()
                #Tips button
                #self.Tips_btn_3rd.hide()
                #self.Tips_btn_4th.show()                
                
##    #----------------------------------------------------------------------
#    def onTutrl(self, sender, sel, ptr):
#        index = self.lst.getSingleSelection()
#        self.sw.setCurrent(index)
#        self.form.Tutrl.setValue(index)
#        return 1

    def onCmdSelect(self, sender, sel, ptr):
        
        if not self.TutorialDB:
           self.TutorialDB = AFXDialog('Tutorial', self.DISMISS, DIALOG_ACTIONS_SEPARATOR, x=0, y=0, w=0, h=0)
           #################################
           ### First page - Introduction ###
           #################################
           tabBook1 = FXTabBook(self.TutorialDB, None, 0, LAYOUT_FILL_X)
           FXTabItem(tabBook1, 'Introduction', None)
           tab1Frame = FXHorizontalFrame(tabBook1, FRAME_RAISED|FRAME_SUNKEN)

           Introduction = os.path.join(thisDir, 'Tutorial\Introduction.png')
           Icon_Introduction = afxCreatePNGIcon(Introduction)
           FXLabel(p=tab1Frame, text='', ic=Icon_Introduction)

           #############################
           ### Second page - Geometry ##
           #############################            
           FXTabItem(tabBook1, 'Geometry')
           tab2Frame = FXHorizontalFrame(tabBook1, FRAME_RAISED|FRAME_SUNKEN)
           
           tabBook2 = FXTabBook(tab2Frame, None, 0, TABBOOK_LEFTTABS|LAYOUT_FILL_X)
           #PAGE 1
           FXTabItem(tabBook2, '1', None, TAB_LEFT)
           subTab2Frame_p1 = FXHorizontalFrame(tabBook2, FRAME_RAISED|FRAME_SUNKEN)
           Geo_P1 = os.path.join(thisDir, 'Tutorial\Geo_P1.png')
           Icon_Geo_P1 = afxCreatePNGIcon(Geo_P1)
           FXLabel(p=subTab2Frame_p1, text='', ic=Icon_Geo_P1)
           
           #PAGE 2
           FXTabItem(tabBook2, '2', None, TAB_LEFT)
           subTab2Frame_p2 = FXHorizontalFrame(tabBook2, FRAME_RAISED|FRAME_SUNKEN) 
           Geo_P2 = os.path.join(thisDir, 'Tutorial\Geo_P2.png')
           Icon_Geo_P2 = afxCreatePNGIcon(Geo_P2)
           FXLabel(p=subTab2Frame_p2, text='', ic=Icon_Geo_P2)          
          
           #PAGE 3
           FXTabItem(tabBook2, '3', None, TAB_LEFT)
           subTab2Frame_p3 = FXHorizontalFrame(tabBook2, FRAME_RAISED|FRAME_SUNKEN)
           Geo_P3 = os.path.join(thisDir, 'Tutorial\Geo_P3.png')
           Icon_Geo_P3 = afxCreatePNGIcon(Geo_P3)
           FXLabel(p=subTab2Frame_p3, text='', ic=Icon_Geo_P3) 

           #PAGE 4
           FXTabItem(tabBook2, '4', None, TAB_LEFT)
           subTab2Frame_p4 = FXHorizontalFrame(tabBook2, FRAME_RAISED|FRAME_SUNKEN)           
           Geo_P4 = os.path.join(thisDir, 'Tutorial\Geo_P4.png')
           Icon_Geo_P4 = afxCreatePNGIcon(Geo_P4)
           FXLabel(p=subTab2Frame_p4, text='', ic=Icon_Geo_P4)
           
           #PAGE 5
           FXTabItem(tabBook2, '5', None, TAB_LEFT)
           subTab2Frame_p5 = FXHorizontalFrame(tabBook2, FRAME_RAISED|FRAME_SUNKEN)           
           Geo_P5 = os.path.join(thisDir, 'Tutorial\Geo_P5.png')
           Icon_Geo_P5 = afxCreatePNGIcon(Geo_P5)
           FXLabel(p=subTab2Frame_p5, text='', ic=Icon_Geo_P5)

           
           #####################################
           ### Third page - Suface generator ###
           #####################################
           FXTabItem(tabBook1, 'Suface generator')
           tab3Frame = FXHorizontalFrame(tabBook1, FRAME_RAISED|FRAME_SUNKEN)
           
           tabBook3 = FXTabBook(tab3Frame, None, 0, TABBOOK_LEFTTABS|LAYOUT_FILL_X)
           #PAGE 1           
           FXTabItem(tabBook3, '1', None, TAB_LEFT)
           subTab3Frame_p1 = FXHorizontalFrame(tabBook3, FRAME_RAISED|FRAME_SUNKEN)
           Sur_P1 = os.path.join(thisDir, 'Tutorial\Sur_P1.png')
           Icon_Sur_P1 = afxCreatePNGIcon(Sur_P1)
           FXLabel(p=subTab3Frame_p1, text='', ic=Icon_Sur_P1)
           
           #PAGE 2            
           FXTabItem(tabBook3, '2', None, TAB_LEFT)
           subTab3Frame_p2 = FXHorizontalFrame(tabBook3, FRAME_RAISED|FRAME_SUNKEN)
           Sur_P2 = os.path.join(thisDir, 'Tutorial\Sur_P2.png')
           Icon_Sur_P2 = afxCreatePNGIcon(Sur_P2)
           FXLabel(p=subTab3Frame_p2, text='', ic=Icon_Sur_P2)
           
           #PAGE 3            
           FXTabItem(tabBook3, '3', None, TAB_LEFT)
           subTab3Frame_p3 = FXHorizontalFrame(tabBook3, FRAME_RAISED|FRAME_SUNKEN)
           Sur_P3 = os.path.join(thisDir, 'Tutorial\Sur_P3.png')
           Icon_Sur_P3 = afxCreatePNGIcon(Sur_P3)
           FXLabel(p=subTab3Frame_p3, text='', ic=Icon_Sur_P3)  

           #PAGE 4            
           FXTabItem(tabBook3, '4', None, TAB_LEFT)
           subTab3Frame_p4 = FXHorizontalFrame(tabBook3, FRAME_RAISED|FRAME_SUNKEN)
           Sur_P4 = os.path.join(thisDir, 'Tutorial\Sur_P4.png')
           Icon_Sur_P4 = afxCreatePNGIcon(Sur_P4)
           FXLabel(p=subTab3Frame_p4, text='', ic=Icon_Sur_P4)
           
           #PAGE 5
           FXTabItem(tabBook3, '5', None, TAB_LEFT)
           subTab3Frame_p5 = FXHorizontalFrame(tabBook3, FRAME_RAISED|FRAME_SUNKEN)
           Sur_P5 = os.path.join(thisDir, 'Tutorial\Sur_P5.png')
           Icon_Sur_P5 = afxCreatePNGIcon(Sur_P5)
           FXLabel(p=subTab3Frame_p5, text='', ic=Icon_Sur_P5)

           #PAGE 6
           FXTabItem(tabBook3, '6', None, TAB_LEFT)
           subTab3Frame_p6 = FXHorizontalFrame(tabBook3, FRAME_RAISED|FRAME_SUNKEN)
           Sur_P6 = os.path.join(thisDir, 'Tutorial\Sur_P6.png')
           Icon_Sur_P6 = afxCreatePNGIcon(Sur_P6)
           FXLabel(p=subTab3Frame_p6, text='', ic=Icon_Sur_P6)      

           #PAGE 7
           FXTabItem(tabBook3, '7', None, TAB_LEFT)
           subTab3Frame_p7 = FXHorizontalFrame(tabBook3, FRAME_RAISED|FRAME_SUNKEN)
           Sur_P7 = os.path.join(thisDir, 'Tutorial\Sur_P7.png')
           Icon_Sur_P7 = afxCreatePNGIcon(Sur_P7)
           FXLabel(p=subTab3Frame_p7, text='', ic=Icon_Sur_P7) 

           #PAGE 8
           FXTabItem(tabBook3, '8', None, TAB_LEFT)
           subTab3Frame_p8 = FXHorizontalFrame(tabBook3, FRAME_RAISED|FRAME_SUNKEN)
           Sur_P8 = os.path.join(thisDir, 'Tutorial\Sur_P8.png')
           Icon_Sur_P8 = afxCreatePNGIcon(Sur_P8)
           FXLabel(p=subTab3Frame_p8, text='', ic=Icon_Sur_P8)            
           
           ########################################
           ### Forth page - Roughness parameter ###
           ########################################
           FXTabItem(tabBook1, 'Roughness parameter')
           tab4Frame = FXHorizontalFrame(tabBook1, FRAME_RAISED|FRAME_SUNKEN)           
           tabBook4 = FXTabBook(tab4Frame, None, 0, TABBOOK_LEFTTABS|LAYOUT_FILL_X)
           #PAGE 1           
           FXTabItem(tabBook4, '1', None, TAB_LEFT)
           subTab4Frame_p1 = FXHorizontalFrame(tabBook4, FRAME_RAISED|FRAME_SUNKEN)
           Rough_P1 = os.path.join(thisDir, 'Tutorial\Rough_P1.png')
           Icon_Rough_P1 = afxCreatePNGIcon(Rough_P1)
           FXLabel(p=subTab4Frame_p1, text='', ic=Icon_Rough_P1)

           #PAGE 2            
           FXTabItem(tabBook4, '2', None, TAB_LEFT)
           subTab4Frame_p2 = FXHorizontalFrame(tabBook4, FRAME_RAISED|FRAME_SUNKEN)
           Rough_P2 = os.path.join(thisDir, 'Tutorial\Rough_P2.png')
           Icon_Rough_P2 = afxCreatePNGIcon(Rough_P2)
           FXLabel(p=subTab4Frame_p2, text='', ic=Icon_Rough_P2)                     
           
           ####################################
           ### Fifth page - Acknowledgement ###
           ####################################           
           #FXTabItem(tabBook1, 'Acknowledgement')
           #tab5Frame = FXHorizontalFrame(tabBook1, FRAME_RAISED|FRAME_SUNKEN)
           #tabBook5 = FXTabBook(tab5Frame)
           #Acknowledgement = os.path.join(thisDir, 'Tutorial\Acknowledgement.png')
           #Icon_Acknowledgement = afxCreatePNGIcon(Acknowledgement)
           #FXLabel(p=tab5Frame, text='', ic=Icon_Acknowledgement)

           
           self.TutorialDB.create()
        
        self.TutorialDB.show()       
      
        return 1


class FileDBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.fileNameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, FileDBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):

       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
           self.fileNameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
       fileDb.setReadOnlyPatterns('*.txt')
       fileDb.create()
       fileDb.showModal()
