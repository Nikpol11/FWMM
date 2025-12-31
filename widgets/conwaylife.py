import util
from widget import Widget as WidgetBase
from widget_config_item import WidgetConfigItem as Config
from widget_config_item import ConfigItemType as ConfigType
from const import WIDTH, HEIGHT
import numpy as np
import time

class Widget(WidgetBase):
    name = "ConwayLife"
    desired_spf = -1
    allow_rotation = True
    
    seeds = {
        "None":False,
        "Random": True,
    }


    def __init__(self):
        super().__init__()
        self.configuration = {
            "Width": Config(ConfigType.integer, 5, 1, max(WIDTH, HEIGHT)),
            "Height": Config(ConfigType.integer, 5, 1, max(WIDTH, HEIGHT)),
            "Brightness": Config(ConfigType.integer, 255, 0, 255),
            "Time Between Updates (sec)": Config(ConfigType.integer, -1, -1, 30),
            "Death Timeout": Config(ConfigType.integer, 10, -1, 1000),
            "General Timeout": Config(ConfigType.integer, -1, -1, 10000),
            "Seed": Config(ConfigType.combo, "Random", options=list(self.seeds.keys()))

        }
        # print(self.configuration["Seed"].value)
        self.conwayLifeManager = self.conwayLife(self.configuration["Width"].value,self.configuration["Height"].value, self)

    def get_current_size(self):
        return [self.configuration["Width"].value, self.configuration["Height"].value]
    
    def get_desired_spf(self):
        return self.configuration["Time Between Updates (sec)"].value

    def get_frame(self):
        width = self.configuration["Width"].value
        height = self.configuration["Height"].value
        
        self.conwayLifeManager.checkDims(width, height)
        self.conwayLifeManager.updateArray()
        base = self.conwayLifeManager.convertArray(self.configuration["Brightness"].value) # type: ignore
        # print(base)
        return base
 
    class conwayLife():
        def __init__(self, width, height, widget):
            self.height = height
            self.width = width
            self.widget = widget
            self.reset()
            if widget.configuration["General Timeout"].value != 0: self.widget.configuration["General Timeout"].value = widget.configuration["General Timeout"].value 
            else: self.widget.configuration["General Timeout"].value = 1
            # self.printArray()
        
        def updateArray(self):
            for x in range(0, np.shape(self.modifiedArray)[0]):
                for y in range(0, np.shape(self.modifiedArray)[1]):
                    self.checkSurrounding(x, y)
            
            if np.array_equal(self.array, self.modifiedArray):
                self.stagnantIterations += 1
                # print("stagnant", self.stagnantIterations)
                if self.stagnantIterations >= self.widget.configuration["Death Timeout"].value:
                    if type(self.widget.seeds[self.widget.configuration["Seed"].value]) == bool and self.widget.seeds[self.widget.configuration["Seed"].value] == True:
                        self.array = np.random.choice((True, False), size=(self.height, self.width))
                    elif type(self.widget.seeds[self.widget.configuration["Seed"].value]) == bool and self.widget.seeds[self.widget.configuration["Seed"].value] == False:
                        self.array = np.full((self.height, self.width),False)
                    else:
                        self.array = np.resize(self.widget.seeds[self.widget.configuration["Seed"].value], (self.height, self.width))
                    self.stagnantIterations = 0
                    self.oscillatingIterations = 0
                    self.iterations = 0
                    self.oldArray = self.array.copy()
                    self.modifiedArray = self.array.copy()
                    return
            elif np.array_equal(self.modifiedArray, self.oldArray):
                self.oscillatingIterations += 1
                # print("oscillating", self.oscillatingIterations)
                if self.oscillatingIterations >= self.widget.configuration["Death Timeout"].value:
                    if type(self.widget.seeds[self.widget.configuration["Seed"].value]) == bool and self.widget.seeds[self.widget.configuration["Seed"].value] == True:
                        self.array = np.random.choice((True, False), size=(self.height, self.width))
                    elif type(self.widget.seeds[self.widget.configuration["Seed"].value]) == bool and self.widget.seeds[self.widget.configuration["Seed"].value] == False:
                        self.array = np.full((self.height, self.width),False)
                    else:
                        self.array = np.resize(self.widget.seeds[self.widget.configuration["Seed"].value], (self.height, self.width))
                    self.stagnantIterations = 0
                    self.oscillatingIterations = 0
                    self.iterations = 0
                    self.oldArray = self.array.copy()
                    self.modifiedArray = self.array.copy()
                    return
            self.iterations += 1
            if self.widget.configuration["General Timeout"].value != -1 and self.iterations >= self.widget.configuration["General Timeout"].value:
                self.reset()
                return
            self.oldArray = self.array.copy()
            self.array = self.modifiedArray.copy()
        
        def checkSurrounding(self, x, y):
            neighborCount = 0
            for i in range(max(0, x-1), min(np.shape(self.array)[0], x+2)):
                for j in range(max(0, y-1), min(np.shape(self.array)[1], y+2)):
                    if (i,j) != (x,y) and self.array[i][j]:
                        neighborCount += 1
            # print(neighborCount, self.modifiedArray[x][y])
            if neighborCount < 2 or neighborCount > 3:
                self.modifiedArray[x][y] = False
            elif neighborCount == 3:
                self.modifiedArray[x][y] = True
            # print(self.modifiedArray[x][y])
                
        def convertArray(self, brightness):
            return np.matrix(np.where(self.array, np.full(np.shape(self.array),brightness), np.zeros(np.shape(self.array))))

        def checkDims(self, width, height):
            if height != self.height or width != self.width:
                self.resize(width, height)
        
        def resize(self, width, height):
            self.array = np.resize(self.array, (height, width))
            self.height = height
            self.width = width
            self.modifiedArray = self.array.copy()
            self.oldArray = self.array.copy()
            
        def reset(self):
            if type(self.widget.seeds[self.widget.configuration["Seed"].value]) == bool and self.widget.seeds[self.widget.configuration["Seed"].value] == True:
                self.array = np.random.choice((True, False), size=(self.height, self.width))
            elif type(self.widget.seeds[self.widget.configuration["Seed"].value]) == bool and self.widget.seeds[self.widget.configuration["Seed"].value] == False:
                self.array = np.full((self.height, self.width),False)
            else:
                self.array = np.resize(self.widget.seeds[self.widget.configuration["Seed"].value], (self.height, self.width))
            self.stagnantIterations = 0
            self.oscillatingIterations = 0
            self.iterations = 0
            self.oldArray = self.array.copy()
            self.modifiedArray = self.array.copy()
        
        def printArray(self):
            for x in self.array:
                print(["@" if y else " " for y in x])
        
        def runLoop(self):
            timelist = []
            while True:
                startTime = time.time()
                self.updateArray()
                timelist.append(time.time()-startTime)
                print(sum(timelist)/len(timelist), " Seconds Average")
                # print(self.array)
                self.printArray()
                time.sleep(1)

# startArray = np.full((4,4), False)
# startArray[2,1] = True
# startArray[1,3] = True
# startArray[2,3] = True
# startArray[3,3] = True
# startArray[3,2] = True

# life = conwayLife(10,12,)
# life.runLoop()
# life.updateArray()
# life.checkSurrounding(3,2)

