welcomeText = '''
This is a multi-line comment
We'll use this somewhere in our app

## Markdown headers can also be used
We can also use markdown math formatting (eg. N/mm^2) and have it render correctly
'''

info_constants= """
## Analysis Constants
Here we define the constants used in our analysis:
- Young's Modulus $(GPa)$
- Cross-sectional area of our bar elements $(m^2)$

We could easily adapt this to provide values on a member-by-member basis by, for example, uploading a csv file (as you'll see below), but a single value for each will be sufficient for now.
"""

info_geometry1="""
## Structure Geometry
Now we upload a csv file containing the nodal positions and member definitions for the truss.

You can download a demo geometry file below. *Modify as needed for your own structure.*
"""

info_geometry2="""
#### CSV file format
The data in geometry csv file is structured as follows:

```
NODES,
0,6
4,6
8,6
...
MEMBERS,
1,2
2,3
3,4
...
```
Nodes are defined by their **x** and **y** position and numbered sequentially. The members are defined by the **node numbers** at either end.
"""

info_geometry3="""
### Upload Geometry File
"""

info_restraints="""
## Structure Restraints
Next, we'll define the restraints. This will give us a good opportunity to demonstrate how to accept and process tabular data.

At any node (identified by its node number), we can specify:
- A pin support which provides translational restraint in the x and y direction
- A horizontal roller which provides translational restraint in the y direction only
- A vertical roller which provides translational restraint in the x direction only
"""

info_loads="""
## Applied Loads
Finally, we define any nodal loads applied to the structure. Again, we accept user input in a tabular format here. We could just as easily accept a csv file, in fact, we could combine all structure and loading information into a single cvs file upload if we wanted.

At any node (again identified by its node number), we can specify:
- A horizontal force magnitude, $F_x (N)$
- A vertical force magnitude, $F_y (N)$
"""

info_export="""
## Exporting Results to CSV

The results of our analysis are reported in the graphical and tabular results panes, to the right. However, it may also be useful to export all results in a single csv file. So, we demonstrate that here. Note that we could also build a PDF report - but I'll leave that as an exercise for you!
"""