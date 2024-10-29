import viktor as vkt
# Utility functions and text blocks
from analysis import *
from visualisation import *
from dataIO import *
from text import *
from pathlib import Path

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
    tab_2.section_3.info = vkt.Text(info_restraints)
    tab_2.section_3.table_restraints = vkt.Table('Restraint Definition')
    tab_2.section_3.table_restraints.col_1 = vkt.IntegerField('Node number')
    tab_2.section_3.table_restraints.col_2 = vkt.OptionField('Restraint Type', options=['Pin', 'X-Roller', 'Y-Roller'])

    # TAB 2 - APPLIED LOADS
    tab_2.section_4 = vkt.Section("Define Applied Loads")
    tab_2.section_4.info = vkt.Text(info_loads)
    tab_2.section_4.table_loads = vkt.Table('Load Definition')
    tab_2.section_4.table_loads.col_1 = vkt.IntegerField('Node number')
    tab_2.section_4.table_loads.col_2 = vkt.NumberField('Fx (N)')
    tab_2.section_4.table_loads.col_3 = vkt.NumberField('Fy (N)')

    # Tab 3
    tab_3 = vkt.Tab("Results Export")
    tab_3.section_1 = vkt.Section("Export Results")
    tab_3.section_1.info = vkt.Text("hello world")


class Controller(vkt.Controller):
    label = 'OpenSeesPy 2D Truss Analysis - from EngineeringSkills.com'
    parametrization = Parametrization
    @vkt.ImageView("Structure", duration_guess=1)
    def createStructurePlot(self, params, **kwargs):
        if params.tab_2.section_2.geometry_file:
            nodes, members = processGeometryFile(params.tab_2.section_2.geometry_file)
            svg_data = plotStructure(nodes, members)
            return vkt.ImageResult(svg_data)
        
        else:
            image_path = Path(__file__).parent /'assets' / 'jpeg-file.jpg'
            return vkt.ImageResult.from_path(image_path)

    @vkt.ImageView("Graphical Results", duration_guess=1)
    def createResultsPlot(self, params, **kwargs):

        image_path = Path(__file__).parent /'assets' / 'jpeg-file.jpg'

        #Only attempt workflow if geometry uploaded and at least two supports defined
        if params.tab_2.section_2.geometry_file and len(params.tab_2.section_3.table_restraints)>1:
          
          #Make sure there are no 'None' restraint values
          if all(item.col_2 is not None for item in params.tab_2.section_3.table_restraints):
            nodes, members = processGeometryFile(params.tab_2.section_2.geometry_file)
            restraints = computerRestraintArray(params.tab_2.section_3.table_restraints)
            forces = computeForceArray(params.tab_2.section_4.table_loads)
            mbr_disp, mbr_forces, node_disp, reactions = analyseStructure(params.tab_2.section_1.E, params.tab_2.section_1.A, nodes, members, restraints, forces)
            svg_data = plotResponse(nodes, members, mbr_disp, mbr_forces, params.tab_2.section_1.xFac)
            return vkt.ImageResult(svg_data)
          
          #Else plot placeholder image
          else: 
            return vkt.ImageResult.from_path(image_path)
          

        #Else plot placeholder image
        else:
            return vkt.ImageResult.from_path(image_path)

    @vkt.DataView("Results Data", duration_guess=1)
    def createResultsData(self, params, **kwargs):
        data_items_disp = []
        data_items_force = []
        data_items_reactions = []
         
	    # Only attempt workflow if geometry uploaded and at least two supports defined
        if params.tab_2.section_2.geometry_file and len(params.tab_2.section_3.table_restraints)>1:

		# Make sure there are no 'None' restraint values
            if all(item.col_2 is not None for item in params.tab_2.section_3.table_restraints):
                
                nodes, members = processGeometryFile(params.tab_2.section_2.geometry_file)
                restraints = computerRestraintArray(params.tab_2.section_3.table_restraints)
                forces = computeForceArray(params.tab_2.section_4.table_loads)
                mbr_disp, mbr_forces, node_disp, reactions = analyseStructure(params.tab_2.section_1.E, params.tab_2.section_1.A, nodes, members, restraints, forces)
                
                for i, d in enumerate(node_disp):
                    resultString = f"Ux: {d[0]} mm, Uy: {d[1]} mm"
                    data_items_disp.append(vkt.DataItem(f'Node {i+1}', resultString))
                    
                for i, mbr in enumerate(members):
                    resultString = f'{mbr_forces[i]} kN'
                    data_items_force.append(vkt.DataItem(f'Member {i+1} (nodes {mbr[0]} to {mbr[1]})', resultString))
                    
                for i, r in enumerate(reactions):
                    resultString = f'Rx: {r[1]} kN, Ry: {r[2]} kN'
                    data_items_reactions.append(vkt.DataItem(f'Node {r[0]}', resultString))
                    
        data_group = vkt.DataGroup(
            vkt.DataItem('Displacement','', subgroup=vkt.DataGroup(*data_items_disp)),
            vkt.DataItem('Member Forces','', subgroup=vkt.DataGroup(*data_items_force)),
            vkt.DataItem('Reactions','', subgroup=vkt.DataGroup(*data_items_reactions))
        )

        return vkt.DataResult(data_group)

    def download_demo_file(self,params, **kwargs):
        file = exportDemo()
        return vkt.DownloadResult(file_content=file, file_name='demo-geometry.csv')
