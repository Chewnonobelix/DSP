# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:18:36 2021

@author: aduhamel
"""
from enum import Enum
import math
import copy

globalDict = {}
speed=1

def addComponent(component):
    print(component in globalDict)
    if component in globalDict:
        globalDict[component.name].append(component)
    else:
        globalDict[component.name] = [component]
    print("end", type(globalDict[component.name]))
    
class Crafter(Enum):
    Mining = 0
    Smelter = 1
    Assembler = 2
    Chemical = 3
    Collider = 4
    Pump = 5
    Extractor = 6
    Raffinery = 7
    
class Craft:
    inputs = {}
    outputs = {}
    inputsStream = {}
    outputsStream = {}
    name = "id1"
    crafter = Crafter.Assembler
    time = 1
    facilities = 1
    
    def __init__(self, name, crafter, inputs, outputs, time):
        self.name = name
        self.crafter = crafter
        self.inputs = inputs
        self.outputs = outputs
        self.time = time
            
        for o in outputs:
            addComponent(self)
    
        
    def singleOutputsStream(self):
        rets = {}
        for ok, ov in self.outputs.items():
            rets[ok] = ov / self.time * 60
        return rets
      
    def singleInputsStream(self):
        rets = {}
        for ik, iv in self.inputs.items():
            rets[ik] = iv / self.time * 60
        return rets
    
    def setFacilities(self, facilities):
        self.facilities = facilities
        os = self.singleOutputsStream()
        for ok, ov in os.items():
            self.outputsStream[ok] = ov * self.facilities

    def setTargetOutput(self, target):
        os = self.singleOutputsStream()
        for on, o in target.items():
            self.facilities = math.ceil(o / os[on])

        for on, of in os.items():
            self.outputsStream[on] = of * self.facilities
            
    def calculate(self):
        print("Calculate", self.name)
        sins = self.singleInputsStream()
        for ik, iv in sins.items():
            print("Input stream", ik, iv*self.facilities, "/min", "facilities: ", self.facilities)
            temp = copy.deepcopy(globalDict[ik][0])
            temp.setTargetOutput({ik: iv*self.facilities})
            if temp.crafter != Crafter.Mining:
                temp.calculate()
            
                
if __name__ == "__main__":
    c = Craft("Iron ore", Crafter.Mining, {"iron": 1}, {"Iron ore": 30}, 60)
    c2 = Craft("Iron lingot", Crafter.Smelter, {"Iron ore": 1}, {"Iron lingot": 1}, 1)
    c3 = Craft("Steel", Crafter.Smelter, {"Iron lingot": 3}, {"Steel": 1}, 3)

    for i in range(1, 10):
        c2.setFacilities(i)
        print("Iron Lingot " +str(i)+ " facilities:" + str(c2.outputsStream["Iron lingot"]))

    for i in range(1, 100):
        print("--------------------------")
        c3.setTargetOutput({"Steel": i * 100})
        print("Steel ", str(i*100), "Facilities:", str(c3.facilities), "Output stream", c3.outputsStream["Steel"], "/min")
        c3.calculate()
        
    for it in globalDict:
        print(it)
    