import FactorioChains as fc
import appJar
import RecipesBase as rb
import CalculatorGUI as cgui
import numpy as np

def MainMain():
    base = rb.Base()

    base.CreateRecipesBase("Infos/Recipes.txt")
    base.CreateRawSourcesBase("Infos/RawSources.txt")
    base.CreateFactoriesBase("Infos/Factories.txt")

    # base.PrintAllRecipes()



    # base.PrintAllKnownSources()

    # print(base.CalculateMultipleRequest("processing unit"))

    # print(base.FactoriesCount())

    app = cgui.RecipesApp(base)
    app.Run()


    # controlApp = cgui.CreateApp(base)
    # controlApp.go()

def TestMain():
    base = rb.Base()
    base.CreateRecipesBase("Infos/Recipes.txt")
    print(base.GetRecipesByProduct("petroleum gas"))
    # print(base.GetRecipeByName("advanced oil processing"))
    # base.CreateFactoriesBase("Infos/Factories.txt")
    # base.PrintAllFactories()

    pass

# TestMain()
MainMain()
