from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import testDB
from testForm import TestForm
 
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
                              buttonText='Rough Surface Generator',
                              object=TestForm(toolset),
                              messageId=AFXMode.ID_ACTIVATE,
                              icon=None,
                              kernelInitString='import RSGen_Master',
                              applicableModules=ALL,
                              version='N/A',
                              author='Youngbin LIM',
                              description='Generate rough surface in Abaqus/CAE with this plug-in' ,
                              helpUrl='N/A'
                              )