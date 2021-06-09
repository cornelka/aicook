# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 02:05:08 2021

@author: gebruiker
"""
import pandas as pd
import time

#test = AllFoods.sample(5)
#test =test.reset_index(drop=True)
#print(test)

#front-end interface
def getRecipeAndWine(ingredientList):
    tmpWine, tmpRecipe = GetPairings(ingredientList)
    return tmpRecipe, tmpWine
    
    
def GetPairings(ingredients):

    foods = ['apple', 'banana', 'beef', 'blueberries', 'bread', 'butter', 'carrot', 'cheese', 'chicken', 'chicken_breast', 'chocolate', 'corn', 'eggs', 'flour', 'goat_cheese', 'green_beans', 'ground_beef', 'ham', 'heavy_cream', 'lime', 'milk', 'mushrooms', 'onion', 'potato', 'shrimp', 'spinach', 'strawberries', 'sugar', 'sweet_potato', 'tomato']
    AllFoods= pd.DataFrame(foods,columns =['food'])
    
    basepath = 'app/home/backend/pair/'
        
    conversie= pd.DataFrame(pd.read_pickle(basepath + 'conversie.pkl'))
    wines = pd.DataFrame(pd.read_pickle(basepath + "WinesTest.pkl"))
    recipes = pd.DataFrame(pd.read_pickle(basepath + 'RecipeCleaned.pkl'))
    ingredients= pd.merge(ingredients,conversie , on=['food'])
    ingredients =ingredients.reset_index(drop=True)

    PairedRecipe=pd.DataFrame( columns=recipes.columns)
    
    run= True
    b=0
    try:
        while run==True and b< len(ingredients):
            start_time = time.time()
            seconds = 4
            for i in range(len(recipes)):
           
                current_time = time.time()
                elapsed_time = current_time - start_time
                if elapsed_time>seconds:
                    break
                #for a in range(len(recipes.ingredient_top_match[i])-1):
                #print(recipes.ingredient_top_match[i])   
                if ingredients.vertaal[b] in recipes.ingredient_top_match[i]:
                    #print(a)
                    PairedRecipe =PairedRecipe.append(recipes.iloc[i])
            if PairedRecipe.empty== False: 
                        run = False
                        break
            else:
                        b+=1

        recept= PairedRecipe.sample()
    except:
        recept = None

    #print("Let's make " +recept.title)
    #print("Here's the description")
    #print(recept.instructions)


    try:
        PairedWines=pd.DataFrame( columns=wines.columns)
    
        start_time = time.time()
        seconds = 4
        for i in range(len(wines)):
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time>seconds:
                break
            for a in range(len(wines.wineclass_list[i])):
            
                if wines.wineclass_list[i][a] in ingredients.wineclass[b]:
                    PairedWines =PairedWines.append(wines.iloc[i])
    
        wijn= PairedWines.sample()
    except:
        wijn = None

    
    
    #print("We've found this wine to go with the recipe")
    #print(wijn.title)
    #display(wijn,recept)
    return wijn, recept

#GetPairings(test)