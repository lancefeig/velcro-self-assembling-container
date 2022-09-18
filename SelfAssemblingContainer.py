import os
import shutil
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk

class Interface(tk.Tk):
    
    #Stores the directory of this .py file
    PROJECT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    
    def __init__(self):
        super().__init__()

        self.title("Self-Assembling Container")
        self.geometry("645x200")
        self.resizable(False,False)

        self.rowconfigure(0,weight=2)

        #Initializes the string variables for the dimension entry widgets
        self.acrylicThicknessVar = tk.StringVar(self,"0.0")
        self.maxLengthVar = tk.StringVar(self,"0.0")
        self.maxWidthVar = tk.StringVar(self,"0.0")
        self.maxHeightVar = tk.StringVar(self,"0.0")
        self.longBufferVar = tk.StringVar(self,"0.0")
        self.lateralBufferVar = tk.StringVar(self,"0.0")
        self.verticalBufferVar = tk.StringVar(self,"0.0")
        self.layoutSpaceVar = tk.StringVar(self,"0.0")

        #Places the dimension entry labels left of the dimension entry widgets
        ttk.Label(self,text="Acrylic Thickness (in.) : ",anchor="w").grid(row=1,column=0,sticky="nsew",padx=3,pady=3)
        ttk.Label(self,text="Maximum Length (in.) : ",anchor="w").grid(row=2,column=0,sticky="nsew",padx=3,pady=3)
        ttk.Label(self,text="Maximum Width (in.) : ",anchor="w").grid(row=3,column=0,sticky="nsew",padx=3,pady=3)
        ttk.Label(self,text="Maximum Height (in.) : ",anchor="w").grid(row=4,column=0,sticky="nsew",padx=3,pady=3)
        ttk.Label(self,text="Longitudinal Buffer (Per Side) (in.) : ",anchor="w").grid(row=1,column=2,sticky="nsew",padx=3,pady=3)
        ttk.Label(self,text="Lateral Buffer (Per Side) (in.) : ",anchor="w").grid(row=2,column=2,sticky="nsew",padx=3,pady=3)
        ttk.Label(self,text="Vertical Buffer (Top Only) (in.) : ",anchor="w").grid(row=3,column=2,sticky="nsew",padx=3,pady=3)
        ttk.Label(self,text="Layout Spacing (in.) : ",anchor="w").grid(row=4,column=2,sticky="nsew",padx=3,pady=3)

        #Places the dimension entry widgets
        ttk.Entry(self,textvariable=self.acrylicThicknessVar).grid(row=1,column=1,padx=3,pady=3)
        ttk.Entry(self,textvariable=self.maxLengthVar).grid(row=2,column=1,padx=3,pady=3)
        ttk.Entry(self,textvariable=self.maxWidthVar).grid(row=3,column=1,padx=3,pady=3)
        ttk.Entry(self,textvariable=self.maxHeightVar).grid(row=4,column=1,padx=3,pady=3)
        ttk.Entry(self,textvariable=self.longBufferVar).grid(row=1,column=3,padx=3,pady=3)
        ttk.Entry(self,textvariable=self.lateralBufferVar).grid(row=2,column=3,padx=3,pady=3)
        ttk.Entry(self,textvariable=self.verticalBufferVar).grid(row=3,column=3,padx=3,pady=3)
        ttk.Entry(self,textvariable=self.layoutSpaceVar).grid(row=4,column=3,padx=3,pady=3)

        #Places the custom instance prefix label widget and custom instance prefix entry widget
        self.instanceFileNameVar = tk.StringVar(self,"")
        ttk.Entry(self,textvariable=self.instanceFileNameVar).grid(row=5,column=1,columnspan=2,sticky="nsew",padx=3,pady=8)
        ttk.Label(self,text="Optional Custom Instance Prefix : ",anchor="w").grid(row=5,column=0,sticky="nsew",pady=8)

        #Places the submit button, which calls button_press() when activated
        ttk.Button(self,text="Submit",command=self.button_press).grid(row=5,column=3,sticky="nsew",padx=3,pady=8)

        #Places an empty label used to communicate with the user
        self.messageLabel = ttk.Label(self,text=None,background="#e1e1e1",anchor="center")
        self.messageLabel.grid(row=0,column=0,columnspan=4,pady=8,stick="nsew")
        

    def button_press(self):
        """Variables indexes in self.stringEntryVars[] are given:
        Acrylic Thickness [0], Max Length [1], Max Width [2], Max Height [3], 
        Longitudinal Buffer [4],Lateral Buffer [5], Vertical Buffer [6], Layout Spacing [7]"""
        
        #Captures user entries for a new instances
        self.stringEntryVars = [self.acrylicThicknessVar.get(),self.maxLengthVar.get(),self.maxWidthVar.get(),self.maxHeightVar.get(),
        self.longBufferVar.get(),self.lateralBufferVar.get(),self.verticalBufferVar.get(),self.layoutSpaceVar.get()]
        self.floatEntryVars  = []
        numericalEntryCondition = True

        #Converts user dimension entries to floats from strings
        currentVarIndex = 0
        for currentVar in self.stringEntryVars:
            try:
                #If conversion is sucessful, and the value is non-zero and non-negative, or a non-negative buffer entry, append float to floatEntryVars[]
                if (float(currentVar) > 0) or (4 <= currentVarIndex <= 6 and float(currentVar) >= 0):
                    self.floatEntryVars.append(float(currentVar))
                    currentVarIndex += 1
                else:
                    numericalEntryCondition = False
                    break
            #If conversion is unsucessful, the error is caught
            except ValueError:
                numericalEntryCondition = False
                break

        #Call calculations() if all user entries are valid, otherwise, notify the user
        if numericalEntryCondition:
            self.calculations()
        else:
            self.messageLabel.config(text="Enter Non-Zero (Excluding Buffers) Positive Decimals Only.",foreground="#e0142f")

    def calculations(self):
        """Variables indexes in self.calculatedDimensions[] are given:
        Acrylic Thickness [0], Base Length [1], Base Width [2], Side Height [3],
        Lid Long Side Outer Cutout [4], Lid Long Side Overhang [5], Lid Long Side Inner Cutout [6],
        Short Side Width [7], Short Side Finger Hole [8], Lid Short Side Outer Cutout [9], Lid Short Side Outer Overhang [10],
        Lid Short Side Middle Cutout [11], Lid Short Side Middle Overhang [12], Layout Spacing [13]"""
        self.calculatedDimensions = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        #Acrylic Thickness [0] is equal to the corresponding user entry
        self.calculatedDimensions[0] = self.floatEntryVars[0]

        #Base Length [1] is the maxmimum length, plus twice the width of the acrylic, plus twice the longitudinal buffer
        self.calculatedDimensions[1] = (2*self.floatEntryVars[0]) + self.floatEntryVars[1] + (2*self.floatEntryVars[4])

        #Base Width [2] is the maximum width, plus twice the width of the acrylic, plus twice the lateral buffer
        self.calculatedDimensions[2] = (2*self.floatEntryVars[0]) + self.floatEntryVars[2] + (2*self.floatEntryVars[5])

        #Side Height [3] is the maximum height, plus the vertical buffer, plus the width of the acrylic (to account for the lid),
        self.calculatedDimensions[3] = self.floatEntryVars[0] + self.floatEntryVars[3] + self.floatEntryVars[6]

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

        #Short Side Width [7] is the maximum width plus twice the lateral buffer.
        self.calculatedDimensions[7] = self.floatEntryVars[2] + (2*(self.floatEntryVars[5]))

        #Short Side Finger Hole [8]
        #Generates a finger hole 0.825" in height if at leat 1.25" of material remains beneath on the short side wall, excluding the lid cutout
        if((self.calculatedDimensions[3] - 0.825 - self.floatEntryVars[0]) >= 1.25):
            self.calculatedDimensions[8] = 0.825 + self.floatEntryVars[0]
        #Otherwise, generates a finger hole that is 40% of the side height, excluding the lid cutout
        else: 
            self.calculatedDimensions[8] = ((self.calculatedDimensions[3] - self.floatEntryVars[0])*0.4) + self.floatEntryVars[0]
    
        #Lid Short Side Outer Cutout [9], Lid Short Side Outer Overhang [10], Lid Short Side Middle Cutout [11], Lid Short Side Middle Overhang [12]
        #Generates 2 overhangs, one twice the length of the other, if the smallest is at least 0.3"
        if((self.calculatedDimensions[7]/8) >= 0.3):  
            self.calculatedDimensions[9] = self.calculatedDimensions[10] = self.calculatedDimensions[11] = self.calculatedDimensions[12] = self.calculatedDimensions[7]/8
        #Otherwise, generates a 0.3" outer overhang and a 0.75" total middle overhang
        else: 
            self.calculatedDimensions[12] = 0.375
            self.calculatedDimensions[10] = 0.3
            self.calculatedDimensions[9] = self.calculatedDimensions[11] = ((self.calculatedDimensions[7]/2) - 0.675)/2

        #Layout Spacing [13] is equal to the corresponding user entry
        self.calculatedDimensions[13] = self.floatEntryVars[7]

        self.file_rewrite()
        
    def file_rewrite(self):
        #Stores the path of the Container Assembly Equations.txt and Acrylic Laser Cutting Equations.txt files
        containerAssemblyEquationsPath = os.path.join(Interface.PROJECT_DIRECTORY,"SolidWorks Parts & Assemblies","Container Assembly Equations.txt")
        acrylicLayoutEquationsPath = os.path.join(Interface.PROJECT_DIRECTORY,"SolidWorks Parts & Assemblies","Acrylic Laser Cutting Equations.txt")

        #List of equation names in the externally referenced equation file for the SolidWorks container assembly file
        containerAssemblyEquationNames = ["Acrylic Thickness","Base Length","Base Width","Side Height","Lid Long Side Outer Cutout",
                     "Lid Long Side Overhang","Lid Long Side Inner Cutout","Short Side Width","Short Side Finger Hole",
                     "Lid Short Side Outer Cutout","Lid Short Side Outer Overhang","Lid Short Side Middle Cutout",
                     "Lid Short Side Middle Overhang"]

        #Opens the Container Assembly Equations.txt file and rewrites the required equation entries
        with open(containerAssemblyEquationsPath,"w") as containerAssemblyEquationsFile:
            for currentEquation in containerAssemblyEquationNames:
                containerAssemblyEquationsFile.writelines([(f"\"{currentEquation}\"= {self.calculatedDimensions[containerAssemblyEquationNames.index(currentEquation)]}in\n"),"\n"])

        #Opens the Acrylic Laser Cutting Equations.txt and rewrites the part spacing equation
        with open(acrylicLayoutEquationsPath,"w") as acrylicLayoutEquationsFile:
            acrylicLayoutEquationsFile.write(f"\"Spacing\"= {self.calculatedDimensions[13]}in")

        self.save_instance()


    def save_instance(self):
        #Stores the current time stamp, numbers only
        timeStamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

        try:
            #Adds a custom prefix to the time stamp if enters anything in the custom instance prefix entry widget; otherwises, only uses time stamp
            if not self.instanceFileNameVar.get():
                fileName = timeStamp
            else:
                fileName = fr"{self.instanceFileNameVar.get()} - {timeStamp}"

            #Copies all files in the "SolidWorks Parts & Assemblies" folder to a new instance folder
            sourceDirectoryPath = os.path.join(Interface.PROJECT_DIRECTORY,"SolidWorks Parts & Assemblies")
            newInstanceDirectoryPath = os.path.join(Interface.PROJECT_DIRECTORY,"Instance Saves",fileName)
            shutil.copytree(sourceDirectoryPath,newInstanceDirectoryPath,copy_function=shutil.copy)

            #Notifies the user that the instance creation was successful
            self.messageLabel.config(text=f"Instance \'{fileName}\' Successfully Generated.\nPlease Update Equation File References.",foreground="#08871d")
        #Notifies the user if the custom file prefix contains illegal characters
        except OSError:
            self.messageLabel.config(text="Enter Acceptable Filename Characters.",foreground="#e0142f")

if __name__ == "__main__":
    interface = Interface()
    interface.mainloop()
