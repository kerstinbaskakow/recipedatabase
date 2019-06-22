#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 10:10:01 2019

@author: kerstin
"""

class Ingredient():
    #Klassenvariablen:
    num_of_ingredient = 0
    #Instanzvariablen
    def __init__(self,name,amount,unity,component=None):
        self.name = name
        self.amount = amount
        self.unity = unity
        self.component = component
        #zählt die gernierten Instanzen
        Ingredient.num_of_ingredient += 1 
        
#    def setComponent(self,component):
#        self.component = component
#        
#    def listFromIngredients(self):
#        return [self.name,self.amount,self.unity,self.component]

    def ingredientAsJsonStructure(self):
        jsonObject = {"Ingredient":self.name,"Amount":self.amount,"Unity":self.unity}
        return jsonObject