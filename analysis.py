import openseespy.opensees as ops

def analyseStructure(E, A, nodes, members, restraints, forces):

	E = E*10**9 #Convert from GPa (supplied nby user) to N/m^2

	## INITIALISATION====================
	ops.wipe() # Remove any existing model
	ops.model('basic', '-ndm', 2, '-ndf', 2) # Set the modelbuilder - 2 dimensions and 2 degrees of freedom per node

	## STRUCTURE DEFINITION==============
	# Define nodes
	for i, n in enumerate(nodes):
		ops.node(i+1, float(n[0]), float(n[1]))

	# Define uniaxial material (Elastic matID E)
	ops.uniaxialMaterial("Elastic", 1, E)

	# Define elements
	for i, mbr in enumerate(members):
		ops.element("Truss", i+1, int(mbr[0]), int(mbr[1]), A, 1)

	# Define boundary conditions
	for r in restraints:
		ops.fix(int(r[0]),int(r[1]),int(r[2]))

	## LOAD DEFINITION====================
	ops.timeSeries("Constant", 1) # Create TimeSeries with a tag of 1
	ops.pattern("Plain", 1, 1) # Create a plain load pattern associated with the TimeSeries (pattern, patterTag, timeseriesTag)

	# Create the nodal load - command: load nodeID xForce yForce
	for f in forces:
		ops.load(int(f[0]), float(f[1]), float(f[2]))

	## ANALYSIS============================
	ops.system("BandSPD") # create SOE
	ops.numberer("RCM") # create DOF number
	ops.constraints("Plain") # create constraint handler
	ops.integrator("LoadControl", 1.0) # create integrator
	ops.algorithm("Linear") # create algorithm
	ops.analysis("Static") # create analysis object
	ops.analyze(1) # perform the analysis

	## EXTRACT RESULTS=====================
	#...
	#...
	#...
	# Member displacements
	mbr_disp = []
	for mbr in members:
		node_i = int(mbr[0]) # Node number for node i of this member
		node_j = int(mbr[1]) # Node number for node j of this member

		ux_i = ops.nodeDisp(node_i, 1) # Horizontal nodal displacement
		uy_i = ops.nodeDisp(node_i, 2) # Vertical nodal displacement
		ux_j = ops.nodeDisp(node_j, 1) # Horizontal nodal displacement
		uy_j = ops.nodeDisp(node_j, 2) # Vertical nodal displacement

		# Append the displacements for this member to the list
		mbr_disp.append([ux_i, uy_i, ux_j, uy_j])
	#...
	#...
	#...
	# Member forces
	mbr_forces = []
	for i, mbr in enumerate(members):
		mbr_forces.append(round(ops.basicForce(i+1)[0]/1000,2))
	#...
	#...
	#...
	#Nodal displacements
	node_disp = []
	for i, n in enumerate(nodes):
		ux = round(ops.nodeDisp(i+1, 1),5) # Horizontal nodal displacement
		uy = round(ops.nodeDisp(i+1, 2),5) # Vertical nodal displacement
		node_disp.append([ux, uy])	
	#...
	#...
	#...
	#Reactions
	reactions = []
	ops.reactions() # Calculate reactions
	for i, r in enumerate(restraints):
		R = ops.nodeReaction(int(r[0]))
		Rx = round(R[0]/1000,2)
		Ry = round(R[1]/1000,2)
		reactions.append([r[0], Rx, Ry])

	return mbr_disp, mbr_forces, node_disp, reactions