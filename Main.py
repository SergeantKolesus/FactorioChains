import FactorioChains as fc
import appJar
import RecipesBase as rb
import CalculatorGUI as cgui
import numpy as np

def MainMain():
    with open("Infos/Recipes.txt") as reader:
        base = rb.Base()

        while True:
            line = reader.readline()

            if (line == '') | (line == "stop\n"):
                print("break")
                break

            rec = base.CreateRecipe(line)

    base.PrintAllRecipes()

    base.CreateRawSourcesBase("Infos/RawSources.txt")

    base.PrintAllKnownSources()

    print(base.CalculateRequest("microcircuit", 30))

    # controlApp = cgui.CreateApp(base)
    # controlApp.go()

def TestMain():
    base = rb.Base()
    base.CreateFactoriesBase("Infos/Factories.txt")
    base.PrintAllFactories()

    pass

TestMain()
# MainMain()
