#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 10:10:01 2019

@author: kerstin
"""

#import json
#import datetime as dt
from Ingredient import Ingredient
from Component import Component
from Recipe import Recipe
import pandas as pd
import datetime as dt
#import os
import json

def dfAddIng(df):
    df['Ingredient']=None
    l=[]
    for row in df.itertuples(name='Ingredient',index=False):
        l.append(Ingredient(row[0],row[1],row[2]))
    df['Ingredient']=l
    df['Ingredient_Json'] = df['Ingredient'].apply(lambda x:x.ingredientAsJsonStructure())
    return df

def turnIngtoComp(ing_dict):
    l=[]
    for item in ing_dict:
        ing_dict[item] = dfAddIng(ing_dict[item])
        l.append(Component(name=item,ingredients=ing_dict[item]['Ingredient']))
    return l

def recipe_formatter(dict_ing_comp,recipename):
    #------------------------- Generate Recipe -------------------------------------------
    recipe = Recipe(name = recipename,date = str(dt.date.today()),components=turnIngtoComp(dict_ing_comp))
    recipeReadyToStore = json.dumps(recipe.recipeAsJsonStructure())
    return recipeReadyToStore


if __name__ == "__main__":
    dict_ing_comp = {'karamellsosse':pd.read_csv('Karamellsosse_Zutaten.csv'),
          'kaiserschmarrn':pd.read_csv('Karamellsosse_Zutaten.csv'),
          'nocheinekOmp':pd.read_csv('Karamellsosse_Zutaten.csv')
          }
    recipename = 'Kaiserschmarrn mit Karamellsosse'
    recipeReadyToStore = recipe_formatter(dict_ing_comp=dict_ing_comp,recipename=recipename)
    print(recipeReadyToStore) 

 
