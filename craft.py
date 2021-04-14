# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:18:36 2021

@author: aduhamel
"""
from enum import Enum
import math
import copy
import json


globalDict = {}
prefered = {}
speed=1

def load():
    fObj = open('dsp.json',)
    jdata = json.loads(fObj.read())
    
    for key, value in jdata.items():
        print(key, value)
        Craft(jData = value)
    
def addComponent(component):
    print(component in globalDict)
    if component in globalDict:
        globalDict[component.name].append(component)
    else:
        globalDict[component.name] = [component]

    prefered[component.name] = 0
    
class Crafter(Enum):
    Mining = 0
    Pump = 1
    Extractor = 2
    Smelter = 3
    Assembler = 4
    Chemical = 5
    Collider = 6
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
                    
    def __init__(self, name = None, crafter = None, inputs = None, outputs = None, time = None, jData = None):
        if jData is None:
            self.name = name
            self.crafter = crafter
            self.inputs = inputs
            self.outputs = outputs
            self.time = time
        else: 
            self.name = jData["Name"]
            self.crafter = jData["Crafter"]
            self.inputs = jData["Input"]
            self.outputs = jData["Output"]
            self.time = jData["Time"]

        print(jData, self.name, self.inputs, self.outputs)
        for o in self.outputs:
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
        #print("Calculate", self.name)
        sins = self.singleInputsStream()
        ret = [self]
        for ik, iv in sins.items():
         #   print("Input stream", ik, iv*self.facilities, "/min", "facilities: ", self.facilities, self.crafter)
            if self.crafter not in [0,1,2]:
                temp = copy.deepcopy(globalDict[ik][0])
                temp.setTargetOutput({ik: iv*self.facilities})
                #ret.append(temp)
                ret.append(temp.calculate())
        return ret
            
                
if __name__ == "__main__":
    load()
    #c = Craft("Iron ore", Crafter.Mining, {"iron": 1}, {"Iron ore": 30}, 60)
    #c2 = Craft("Iron lingot", Crafter.Smelter, {"Iron ore": 1}, {"Iron lingot": 1}, 1)
    #c3 = Craft("Steel", Crafter.Smelter, {"Iron lingot": 3}, {"Steel": 1}, 3)

    c2 = copy.deepcopy(globalDict["Iron lingot"][0])
    c3 = copy.deepcopy(globalDict["Steel"][0])
    for i in range(1, 10):
        c2.setFacilities(i)
        print("Iron Lingot " +str(i)+ " facilities:" + str(c2.outputsStream["Iron lingot"]))

    for i in range(1, 100):
        #print("--------------------------")
        c3.setTargetOutput({"Steel": i * 100})
        #print("Steel ", str(i*100), "Facilities:", str(c3.facilities), "Output stream", c3.outputsStream["Steel"], "/min")
        calc = c3.calculate()
        #print(calc)                
    for it in globalDict:
        print(it)
    