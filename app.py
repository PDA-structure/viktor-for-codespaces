import viktor as vkt
# Utility fucntions and text blocks
from analysis import *
from visualisation import *
from dataIO import *
from text import *

class Parametrization(vkt.Parametrization):
    # Tab 1
    tab_1 = vkt.Tab('HELLO THERE!')
    tab_1.text = vkt.Text("THIS IS MY FIRST VIKTOR APP - LEARNING FROM ENGINEERING SKILLS WEBSITE")

    # TAB 2 - SECTION 1 - ANALYSIS CONSTANTS
    tab_2 = vkt.Tab("Data Input")
    tab_2.section_1 = vkt.Section("Define Analysis Constants")
    tab_2.section_1.info = vkt.Text(info_constants)
    tab_2.section_1.E = vkt.NumberField("Young's Modulus (GPa)", min=0, default=200)
    tab_2.section_1.lb = vkt.LineBreak()
    tab_2.section_1.A = vkt.NumberField('Cross-sectional Area (m^2)', min=0, default=0.005)
    tab_2.section_1.lb1 = vkt.LineBreak()
    tab_2.section_1.xFac = vkt.NumberField('Deflection scale slider', variant='slider', min=1, max=1000, default=500)

    # TAB 2 - SECTION 2 - STRUCTURE GEOMETRY (DOWNLOAD GEOMETRY AND UPLOAD GEOMETRY FILE)
    tab_2.section_2 = vkt.Section("Define Structure Geometry")
    tab_2.section_2.info = vkt.Text(info_geometry1)
    tab_2.section_2.download_demo = vkt.DownloadButton('Download Demo Geometry', method='download_demo_file')
    tab_2.section_2.info2 = vkt.Text(info_geometry2)
    tab_2.section_2.info3 = vkt.Text(info_geometry3)
    tab_2.section_2.geometry_file = vkt.FileField('Upload CSV')
    
    # TAB 2 - SECTION 3 - RESTRAINTS
    tab_2.section_3 = vkt.Section("Define Restraints")
    tab_2.section_3.info = vkt.Text("Hello World")

    tab_2.section_4 = vkt.Section("Define Applied Loads")
    tab_2.section_4.info = vkt.Text("Hello World")

    # Tab 3
    tab_3 = vkt.Tab("Results Export")
    tab_3.section_1 = vkt.Section("Export Results")
    tab_3.section_1.info = vkt.Text("hello world")


class Controller(vkt.Controller):
    label = 'OpenSeesPy 2D Truss Analysis - from EngineeringSkills.com'
    parametrization = Parametrization

    def download_demo_file(self,params, **kwargs):
        file = exportDemo()
        return vkt.DownloadResult(file_content=file, file_name='demo-geometry.csv')
