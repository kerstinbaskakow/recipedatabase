#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 18:43:33 2019

@author: kerstin
"""

class Recipe():
    #Klassenvariablen:
    num_of_recipe = 0
    
    def __init__(self,name,date,components,equipment=None,preparation='Text missing',keywords=None):
        self.name = name
        self.date = date
        self.components = components
        self.equipment = equipment
        self.preparation = preparation
        self.keywords = keywords
        Recipe.num_of_recipe += 1      
        
#    def appendComponent(self,component): 
#        self.components.append(component)
        
    def appendEquipment(self,equipment):
        self.equipmentlist.append(equipment)
        
    def appendPreparation(self,preparation):
        self.preparation = preparation
    
    def appendKeyword(self,keyword):
        self.keywords.append(keyword)  
        
#    def get_ingredientFromComponent():
#        pass
        
    def recipeAsJsonStructure(self):
        jsonObject = {"Recipename":self.name,
                      "Date":self.date,
                      "Preparation":self.preparation,
                      "Keywords":self.keywords,
                      "Component":list(map(lambda comp:comp.componentAsJsonStructure(),self.components)),             
                      "Equipment":self.equipment
                      }
        return jsonObject