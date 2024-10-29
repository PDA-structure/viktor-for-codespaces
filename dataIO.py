import numpy as np
import io
import os

def processGeometryFile(input):
    # Fill in function body later
    return

def computerRestraintArray(inputData):
    # Fill in function body later
    return

def computeForceArray(inputData):
    #fill in function body later
    return

def exportResults(mbr_forces, node_disp, reactions, members):
    # fill in function body later
    return

def exportDemo():
    file_path = os.path.join(os.path.dirname(__file__), 'demo-geometry.csv')

    with open(file_path, 'rb') as file:
        file_contents = file.read()
        demo = io.BytesIO(file_contents)

    demo.seek(0) # Reset the pointer to the beginning of the BytesIO object
    return demo
