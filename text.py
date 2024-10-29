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