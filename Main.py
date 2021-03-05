import FactorioChains as fc
import appJar
import RecipesBase as rb
import CalculatorGUI as cgui
import numpy as np

def MainMain():
    base = rb.Base()

    base.CreateRecipesBase("Infos/Recipes.txt")

    # base.PrintAllRecipes()

    base.CreateRawSourcesBase("Infos/RawSources.txt")
    base.CreateFactoriesBase("Infos/Factories.txt")

    # base.PrintAllKnownSources()

    print(base.CalculateRequest("processing unit", 30))
    # print(base.FactoriesCount())

    app = cgui.RecipesApp(base)
    app.Run()


    # controlApp = cgui.CreateApp(base)
    # controlApp.go()

def TestMain():
    base = rb.Base()
    base.CreateRecipesBase("Infos/Recipes.txt")
    # print(base.GetRecipeByName("advanced oil processing"))
    # base.CreateFactoriesBase("Infos/Factories.txt")
    # base.PrintAllFactories()

    pass

# TestMain()
MainMain()
