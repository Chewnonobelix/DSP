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
    
    for value in jdata:
        Craft(jData = value)
    
def addComponent(oname, component):
    if component in globalDict:
        globalDict[oname].append(component)
    else:
        globalDict[oname] = [component]

    prefered[component.name] = 0
    
class Crafter(Enum):
    Mining = "mining"
    Pump = "pump"
    Extractor = "extractor"
    Smelter = "smelter"
    Assembler = "assembler"
    Chemical = "chemical"
    Collider = "collider"
    Raffinery = "raffinery"
    
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
            self.inputsStream = {}
            self.outputsStream = {}
        else: 
            self.name = jData["name"]
            self.crafter = Crafter(jData["crafter"])
            self.inputs = jData["input"]
            self.outputs = jData["output"]
            self.time = jData["time"]
            self.inputsStream = {}
            self.outputsStream = {}

        for o in self.outputs:
            addComponent(o, self)
    
        
    def singleoutputsStream(self):
        rets = {}
        for ok, ov in self.outputs.items():
            rets[ok] = ov / self.time * 60
        return rets
      
    def singleinputsStream(self):
        rets = {}
        if self.inputs is not None:
            for ik, iv in self.inputs.items():
                rets[ik] = iv / self.time * 60
        return rets
    
    def setFacilities(self, facilities):
        self.facilities = facilities
        os = self.singleoutputsStream()
        for ok, ov in os.items():
            self.outputsStream[ok] = ov * self.facilities

    def setTargetoutput(self, target):
        os = self.singleoutputsStream()
        for on, o in target.items():
            self.facilities = math.ceil(o / os[on])

        for on, of in os.items():
            self.outputsStream[on] = of * self.facilities
            
    def calculate(self):
        sins = self.singleinputsStream()
        ret = [self]
        for ik, iv in sins.items():
            if self.crafter not in [Crafter.Mining, Crafter.Extractor, Crafter.Pump]:
                if ik not in globalDict:
                    Craft(name=ik, outputs={ik: 1}, time=1)
                temp = copy.deepcopy(globalDict[ik][0])
                temp.setTargetoutput({ik: iv*self.facilities})
                ret.append(temp.calculate())
        return ret
            
def display(result, stage):
    print("For (",stage, ") : " , result[0].facilities,  result[0].name, "facilities")
    for ok, ov in result[0].outputsStream.items():
        print(ok, ov, "/min")
       

    if len(result) > 1:        
        print("(", stage, ") need:")
    else:
        print('#####')
    for it in result[1:]:
        display(it, stage +1)
        
                
if __name__ == "__main__":
    load()

    c2 = copy.deepcopy(globalDict["iron lingot"][0])
    c3 = copy.deepcopy(globalDict["energetic graphite"][0])
    for i in range(1, 10):
        c2.setFacilities(i)
        print("iron Lingot " +str(i)+ " facilities:" + str(c2.outputsStream["iron lingot"]))

    for i in range(1, 10):
        print("--------------------------")
        c3.setTargetoutput({"energetic graphite": i * 100})
        calc = c3.calculate()
        display(calc, 0)
    