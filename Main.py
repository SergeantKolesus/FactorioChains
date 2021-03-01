import FactorioChains as fc
import appJar
import RecipesBase as rb
import CalculatorGUI as cgui
import numpy as np

def MainMain():
    with open("Infos/Recipes.txt") as reader:
        base = rb.Base()


        # rb.AlternativeParse("test line")

        while True:
            recipe = fc.Recipe()
            line = reader.readline()
            # line.rstrip('\n')
            # print(int(line[-1]))
            # print(line[-1].isprintable())

            if (line == '') | (line == "stop\n"):
                print("break")
                break

            rec = base.CreateRecipe(line)
            # if '\n' in line:
            #     print(line, end="")
            # else:
            #     print(line)
            # rb.PrintRecipe(rec)
            # print()

        # print(base.RecipesCount())
    base.PrintAllRecipes()

    base.CalculateRequest("iron plate", 10)

    # controlApp = cgui.CreateApp(base)
    # controlApp.go()

def TestMain():
    with open("Infos/Recipes.txt") as reader:
        base = rb.Base()

        # rb.AlternativeParse("test line")

        while True:
            line = reader.readline()

            if (line == '') | (line == "stop\n"):
                print("break")
                break

            rec = base.CreateRecipe(line)

    base.PrintAllRecipes()

TestMain()
# MainMain()
