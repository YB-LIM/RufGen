from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import Rough_DB
from Rough_Form import RoughForm
 
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
                              buttonText='Rough Surface Generator',
                              object=RoughForm(toolset),
                              messageId=AFXMode.ID_ACTIVATE,
                              icon=None,
                              kernelInitString='import RSGen_Master',
                              applicableModules=ALL,
                              version='N/A',
                              author='Youngbin LIM',
                              description='Generate rough surface in Abaqus/CAE with this plug-in' ,
                              helpUrl='N/A'
                              )