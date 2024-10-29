import numpy as np
import io
import os

def processGeometryFile(input):
	#Initialise containers
	nodes = []
	members = []

	#Initialise flags to indicate which type of line we're reading
	reading_nodes = False
	reading_members = False
      
	#Open file
	with input.file.open(encoding='utf-8') as file:
		#Process line-by-line
		for line in file:
			line = line.strip()
                  
			#Check what type of line we're parsing and update flags
			if "NODES" in line:
				reading_nodes = True
				reading_members = False
				continue
                  
			elif "MEMBERS" in line:
				reading_nodes = False
				reading_members = True
				continue

			# Create node if line is a node definition and append to nodes list
			if reading_nodes and line:
				parts = line.split(',')
				if len(parts) == 2: # Ensure there are exactly two elements
					x, y = map(int, parts)
					nodes.append([x, y])
					
			# Create member if line is a member definition and append to members list
			if reading_members and line:
				parts = line.split(',')
				if len(parts) == 2: # Ensure there are exactly two elements
					node_i, node_j = map(int, parts)
					members.append([node_i, node_j])

	return np.array(nodes), np.array(members)


def computerRestraintArray(inputData):
	restraints = [] #Initialise the list
	
	for row in inputData:
		node = row["col_1"] # Access col_1 from this row
		support = row["col_2"] # Access col_1 from this row

		"""
		Note that we specified the names col_1 and col_2 when we defined the
		table in our Parametrization() class in app.py
		"""
		restraint = []
		restraint.append(node) # Add the node number to the current restraint list

		#Convert strings to numbers and add to current restraint list
		if support == "Pin":
			restraint.extend([1,1])
		elif support == "X-Roller":
			restraint.extend([0,1])
		elif restraint == "Y-Roller":
			restraint.extend([1,0])

		restraints.append(restraint)

	return np.array(restraints)

def computeForceArray(inputData):
	forces = []
	for row in inputData:
		node = row["col_1"]
		if node != None:
			fx = 0 if row["col_2"]==None else row["col_2"]
			fy = 0 if row["col_3"]==None else row["col_3"]
			force = [node, fx, fy]
			forces.append(force)

	return np.array(forces)

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
