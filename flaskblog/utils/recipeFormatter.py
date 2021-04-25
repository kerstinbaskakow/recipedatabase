#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 10:10:01 2019

@author: kerstin
"""

import pandas as pd
import datetime as dt
import json


class Ingredient():
    # Klassenvariablen:
    num_of_ingredient = 0

    # Instanzvariablen
    def __init__(self, name, amount, unity):
        self.name = name
        self.amount = amount
        self.unity = unity
        # zählt die gernierten Instanzen
        Ingredient.num_of_ingredient += 1

    def ingredientAsJsonStructure(self):
        jsonReadyObject = {"Ingredient": self.name, "Amount": self.amount, "Unity": self.unity}
        return jsonReadyObject


class Component():
    # Klassenvariablen:
    num_of_component = 0

    # Instanzvariablen
    # ingredientslist = []
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients
        Component.num_of_component += 1

    def componentAsJsonStructure(self):
        ingredientAsJson = list(map(lambda x: x.ingredientAsJsonStructure(), self.ingredients))
        jsonReadyObject = {self.name: ingredientAsJson}
        return jsonReadyObject


class Recipe():
    # Klassenvariablen:
    num_of_recipe = 0

    def __init__(self, name, date, components, equipment=None, preparation='Text missing', keywords=None):
        self.name = name
        self.date = date
        self.components = components
        if equipment is None:
            self.equipment = []
        else:
            self.equipment = equipment
        self.preparation = preparation
        if keywords is None:
            self.keywords = []
        else:
            self.keywords = keywords
        Recipe.num_of_recipe += 1

    def __repr__(self):
        return "Recipe({},{})".format(self.name, self.date)

    def __str__(self):
        return "Recipe({},{})".format(self.name, self.date)

    #    def appendComponent(self,component):
    #        self.components.append(component)

    def add_equ(self, equ):
        if equ not in self.equipment:
            self.equipment.append(equ)

    def remove_equ(self, equ):
        if equ in self.equipment:
            self.equipment.remove(equ)

    def add_prep(self, prep):
        self.preparation = prep

    def add_kw(self, kw):
        if kw not in self.keywords:
            self.keywords.append(kw)

    def remove_kw(self, kw):
        if kw in self.keywords:
            self.keywords.remove(kw)

    def add_comp(self, comp):
        if comp not in self.components:
            self.components.append(comp)

    def remove_comp(self, comp):
        if comp in self.components:
            self.components.remove(comp)

    def recipeAsJson(self):
        jsonReadyObject = {"Recipename": self.name,
                           "Date": self.date,
                           "Preparation": self.preparation,
                           "Keywords": self.keywords,
                           "Component": list(map(lambda comp: comp.componentAsJsonStructure(), self.components)),
                           "Equipment": self.equipment
                           }
        return json.dumps(jsonReadyObject)


class RecipeFormatter():
    def dfAddIng(df):
        # -------------- make Ingredients out of the elements ------------------------------
        # ingredients must be a dataframe with the columms name of ingredient,amount of ingredient, unity
        df['Ingredient'] = None  # initialize Ingredients column in dataframe
        l = []  # initialize a list for all ingredients as Ingredients class
        # go through all rows and make a list of Ingredients class
        for row in df.itertuples(name='Ingredient', index=False):
            l.append(Ingredient(row[0], row[1], row[2]))
        # add the list to the dataframe as column Ingredient
        df['Ingredient'] = l
        # df['Ingredient_Json'] = df['Ingredient'].apply(lambda x:x.ingredientAsJsonStructure())
        return df

    def turnIngtoComp(ing_dict):
        # --------------------- make components out of components-ingredients dictionary -----------------
        l = []  # initialize a list for all Components
        # components and Ingredients must come in as dictionary of component:dataframe(Ingredients)
        for key, value in ing_dict.items():
            # value is the dataframe of ingredient where the table was formated to Ingredients class
            value = RecipeFormatter.dfAddIng(value)
            l.append(Component(name=key, ingredients=value['Ingredient']))
        return l

    def read_recipe():
        # ----------------------- header -------------------------------------------------

        dict_ing_comp = {'karamellsosse': pd.read_csv('Karamellsosse_Zutaten.csv'),
                         'kaiserschmarrn': pd.read_csv('Karamellsosse_Zutaten.csv'),
                         'nocheinekOmp': pd.read_csv('Karamellsosse_Zutaten.csv')
                         }
        recipename = input('Name of the recipe: ')
        equipment = input('Equipment kommagetrennt eingeben: ')
        keyword = input('Keyword kommagetrennt eingeben: ')
        preparation = input('Zubereitung eingeben: ')
        # ------------------------ generate recipe --------------------------------------------
        recipe = Recipe(name=recipename, date=str(dt.date.today()),
                        components=RecipeFormatter.turnIngtoComp(dict_ing_comp))
        for item in equipment.split(','):
            recipe.add_equ(item)
        for item in keyword.split(','):
            recipe.add_kw(item)
        recipe.add_prep(preparation)
        recipeReadyToStore = recipe.recipeAsJson()
        print(recipeReadyToStore)
        return recipeReadyToStore


RecipeFormatter.read_recipe()
# RecipeFormatter.read_recipe()