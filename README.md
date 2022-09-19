# Self-Assembling Container
Self-Assembling Container is a Python script that calculates and edits dimensions in SolidWorks files to create containers for Testing Lab equipment at Velcro Research & Development.

## Background
During my Summer 2022 internship at Velcro in Manchester, New Hampshire, one of my projects was to design storage containers for different equipment in the R&D Testing Lab.

Each fixture was a combination of heavy, weirdly shaped, super tiny, or prone to falling over, so I had to design unique containers to house each fixture from scratch. Container pieces (sides, base, and lid) were fashioned from acrylic sheets, which I cut using the in-house CO~2~ laser cutter. 

All 11 containers were fully modeled in SolidWorks, including 3D printed pieces and necessary hardware. (Renderings can be viewed [here](https://lancefeig.github.io/#velcro-summer-2022---solidworks-renderings-for-testing-lab-fixture-containers).)

Every container design shares the same basic parts: two short walls, two longer walls, a base, and a lid. In addition, all container designs required a 2D part layout for laser cutting.

### Fig. 1. SolidWorks container assembly.
![mainassembly](https://github.com/lancefeig/velcro-self-assembling-container/blob/main/img/mainassembly.PNG?raw=true)

### Fig. 2. SolidWorks acrylic laser cutting layout.
![mainlayout](https://github.com/lancefeig/velcro-self-assembling-container/blob/main/img/mainlayout.PNG?raw=true)

The main difference between fixture container designs is the dimensions of the SolidWorks parts since the assemblies generally contain six components mated in the exact same manner.

Within each container assembly, the measurements are repeated multiple times in different parts (e.g., the length of the base is also the length of the long side and the lid; the height of the short side is also the height of the long side).

To calculate the dimensions for each container, I repeatedly performed the same computations (e.g., the width of the short side is always the base length minus twice the width of the acrylic; the height of the sides is always the maximum height of the fixture, plus a gap, plus the thickness of the acrylic to account for the interlocking lid).

Thus, I developed a Python script to remove the monotonous calculations and dimension editing from the container design process. Furthermore, the script enables my coworkers to speedily design new containers for new equipment after the conclusion of my internship.

## Functionality
The user is prompted to enter information specific to a certain fixture through a Tkinter GUI.

The *Acrylic Thickness* corresponds to the thickness of the acrylic used to cut the parts.

The *Maximum Length*, *Maximum Width*, and *Maximum Height* correspond to the size of the fixture that the generated container will house.

The *Longitudinal Buffer* and *Lateral Buffer* correspond to the additional space added to either side of the *Maximum Length* and *Maximum Width*, respectively. Extra space is useful for accommodating 3D printed parts and your hands for taking a fixture out of its container.

The *Vertical Buffer* corresponds to the space added above the fixture, assuming the fixture rests on the base.

The *Layout Spacing* corresponds to the distance between the parts in the acrylic layout assembly.

The *Optional Custom Instance Prefix* corresponds to a custom prefix, in front of the time stamp, for the generated instance folder.

### Fig. 3. The interface after initializing.
![interface1](https://github.com/lancefeig/velcro-self-assembling-container/blob/main/img/interface1.jpg?raw=true)

### Fig. 4. An instance is successfully generated.
![interface4.jpg](https://github.com/lancefeig/velcro-self-assembling-container/blob/main/img/interface4.jpg?raw=true)

### Fig. 5. A diagram noting the spatial representation of six variables.
![inputvisual.png](https://github.com/lancefeig/velcro-self-assembling-container/blob/main/img/inputvisual.png?raw=true) 

Once the *Submit* button on the interface is clicked, the numerical data is processed by an algorithm to calculate the custom container dimensions.

Some calculations are simple:
```Python
#Base Width [2] is the maximum width, plus twice the width of the acrylic, plus twice the lateral buffer
self.calculatedDimensions[2] = (2*self.floatEntryVars[0]) + self.floatEntryVars[2] + (2*self.floatEntryVars[5])
```
Some calculations are less intuitive:
```Python
#Lid Long Side Outer Cutout [4], Lid Long Side Overhang [5], Lid Long Side Inner Cutout [6]
#Generates 2 long side lid notches if they're at least 0.5" wide. The 2 notches and 3 cutouts should be equal distance
if((self.calculatedDimensions[1]/5) >= 0.5):
	self.calculatedDimensions[4] = self.calculatedDimensions[5] = self.calculatedDimensions[1]/5
	self.calculatedDimensions[6] = self.calculatedDimensions[1]/10
#Otherwise, forces both lid notches to be equal to 0.5"
else:
	self.calculatedDimensions[5] = 0.5
	self.calculatedDimensions[4] = (self.calculatedDimensions[1] - 1)/3
	self.calculatedDimensions[6] = (self.calculatedDimensions[1] - 1)/6
```
Next, the program overwrites two text files that store the dimension data. These are external equation files, which are read by the SolidWorks assemblies. Dimensions that appear in multiple parts are each defined as equation variables, which are modified as SolidWorks reads the updated external equation files. 

The OS module is used to capture the computer directory location of the equation files.

The script edits the files located in the `SolidWorks Parts & Assemblies` folder, which serves as a template for generated instances. The template folder contains the SolidWorks part files for the long side, short side, base, and lid of the containers. It also contains the main container assembly file (where the container appears like a container) and the laser cutting layout (where every piece is positioned flat on a plane).

Finally, the Shutil module is used to copy the edited template folder into a new timestamped folder inside the `Instance Saves` folder.

## Installation 
Download the provided `PackedSelfAssemblingContainer.zip` in the repository and extract all files to a chosen folder. Ensure all three files (`SolidWorks Parts & Assemblies`, `Instance Saves`, and `SelfAssemblingContainer.py`) are kept in the same directory, otherwise, the program will be unable to locate them. Run the Python file when ready.

## Notes
The way SolidWorks behaves, assemblies link to external equation files by remembering their file location. Once generated, the instance assembly files still read the template equation files in the `SolidWorks Parts & Assemblies` folder---and not the equation files within their `Instance Saves` sub-folder. The SolidWorks assemblies must be opened, and the locations of the equation files must be changed in the *Equations Interface*.