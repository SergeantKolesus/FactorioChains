import FactorioChains as fc
import appJar
import RecipesBase as rb
import CalculatorGUI as cgui
import numpy as np

def MainMainOld():
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

def MainMain():
    base = rb.CraftData()
    base.FillFromFile({
        "factories": "Infos/Factories.txt",
        "recipes": "Infos/Recipes.txt",
        "raw sources": "Infos/RawSources.txt"
    })
    base.PrintRecipes()
    base.PrintFactories()
    base.PrintRawSources()
    base.PrintComponents()
    print(base.ComponentsCount())
    app = cgui.FactorioCalculatorApp(base)

    # base.CreateRecipesBase("Infos/Recipes.txt")
    # print(base.GetRecipesByProduct("petroleum gas"))
    # print(base.GetRecipeByName("advanced oil processing"))
    # base.CreateFactoriesBase("Infos/Factories.txt")
    # base.PrintAllFactories()

    pass

def TestMain():
    a = fc.Component("Test")

# TestMain()
MainMain()
