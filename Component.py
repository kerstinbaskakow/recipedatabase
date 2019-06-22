#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 10:32:43 2019

@author: kerstin
"""

class Component():
    #Klassenvariablen:
    num_of_component = 0
    #Instanzvariablen
    #ingredientslist = []
    def __init__(self,name,ingredients=None,preparation='Text missing'):
        self.name = name
        self.ingredients = ingredients
        self.preparation = preparation
        Component.num_of_component += 1  

#    def appendIngredient(self,ingredient):  
#        self.ingredients.append(ingredient)
#        
#    def appendPreparation(self,preparation):
#        self.preparation = preparation
        
    def componentAsJsonStructure(self):
        ingredientAsJson = list(map(lambda x:x.ingredientAsJsonStructure(),self.ingredients))
        jsonObject = {self.name:ingredientAsJson}
        return jsonObject

        