import matplotlib.pyplot as plt
from io import StringIO

def plotStructure(nodes, members):
	fig = plt.figure()
	width = 0.8 # 80% of the figure's width
	height = 0.8 # 80% of the figure's height

	# Calculate 'left' and 'bottom' to center the axes
	left = (1 - width) / 2
	bottom = (1 - height) / 2

	axes = fig.add_axes([left, bottom, width, height])
	fig.gca().set_aspect('equal', adjustable='box')

	for mbr in members:
		node_i = mbr[0] #Node number for node i of this member
		node_j = mbr[1] #Node number for node j of this member

		ix = nodes[node_i-1,0] #x-coord of node i of this member
		iy = nodes[node_i-1,1] #y-coord of node i of this member
		jx = nodes[node_j-1,0] #x-coord of node j of this member
		jy = nodes[node_j-1,1] #y-coord of node j of this member
		axes.plot([ix,jx],[iy,jy],'b') #Member

	#Plot nodes
	for i, n in enumerate(nodes):
		axes.plot([n[0]],[n[1]],'bo', ms=4)
		label = str(i+1) #The node number label string
		offX = (nodes[:, 0].max() - nodes[:, 0].min()) / 70
		offY = (nodes[:, 1].max() - nodes[:, 1].min()) / 70
		axes.text(n[0]+offX, n[1]+offY, label, fontsize=12)

	axes.set_xlabel('Distance (m)')
	axes.set_ylabel('Distance (m)')
	axes.set_title('Structure')
	margin = (nodes[:, 0].max() - nodes[:, 0].min()) / 10
	axes.set_xlim([nodes[:, 0].min() - margin, nodes[:, 0].max() + margin])
	axes.set_ylim([nodes[:, 1].min() - margin, nodes[:, 1].max() + margin])
	axes.grid()

	svg_data = StringIO()
	fig.savefig(svg_data, format='svg')
	plt.close(fig)

	return svg_data

def plotResponse(nodes, members, nodal_disp, mbr_forces, xFac):
	fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all', figsize=(8, 10))
	fig.subplots_adjust(hspace=0.4)
	ax1.set_aspect('equal', adjustable='box')
	ax2.set_aspect('equal', adjustable='box')

	# Call separate functions for each subplot
	subplotForces(ax1, nodes, members, mbr_forces)
	subplotDeflection(ax2, nodes, members, nodal_disp, xFac)

	svg_data = StringIO()
	fig.savefig(svg_data, format='svg')
	plt.close(fig)

	return svg_data # Make sure to return the SVG data as a string

def subplotForces(ax, nodes, members, mbr_forces):
	# Plot tension/compression members
	for n, mbr in enumerate(members):
		node_i = mbr[0]
		node_j = mbr[1]

		ix = nodes[node_i-1,0]
		iy = nodes[node_i-1,1]
		jx = nodes[node_j-1,0]
		jy = nodes[node_j-1,1]

		if(abs(mbr_forces[n]) < 0.001):
			ax.plot([ix,jx],[iy,jy],'grey', linestyle='--') # Zero force in member
		elif(mbr_forces[n] > 0):
			ax.plot([ix,jx],[iy,jy],'b') # Member in tension
		else:
			ax.plot([ix,jx],[iy,jy],'r') # Member in compression

	ax.set_xlabel('Distance (m)')
	ax.set_ylabel('Distance (m)')
	ax.set_title('Tension/compression members')
	ax.grid()

def subplotDeflection(ax, nodes, members, nodal_disp, xFac):
	# Plot deformed members
	for i, mbr in enumerate(members):
		node_i = int(mbr[0])
		node_j = int(mbr[1])

		ix = nodes[node_i-1,0]
		iy = nodes[node_i-1,1]
		jx = nodes[node_j-1,0]
		jy = nodes[node_j-1,1]

		ax.plot([ix,jx],[iy,jy],'grey', lw=0.75) # Member

		ux_i = nodal_disp[i][0]
		uy_i = nodal_disp[i][1]
		ux_j = nodal_disp[i][2]
		uy_j = nodal_disp[i][3]

		ax.plot([ix + ux_i*xFac, jx + ux_j*xFac], [iy + uy_i*xFac, jy + uy_j*xFac],'r') # Deformed member

	ax.set_xlabel('Distance (m)')
	ax.set_ylabel('Distance (m)')
	ax.set_title('Deflected shape')
	ax.grid()
