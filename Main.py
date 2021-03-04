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

            if line[0] != '#':
                rec = base.CreateRecipe(line)

    base.PrintAllRecipes()

    base.CreateRawSourcesBase("Infos/RawSources.txt")
    base.CreateFactoriesBase("Infos/Factories.txt")

    base.PrintAllKnownSources()

    print(base.CalculateRequest("processing unit", 30))
    # print(base.FactoriesCount())

    app = cgui.RecipesApp(base)
    app.Run()


    # controlApp = cgui.CreateApp(base)
    # controlApp.go()

def TestMain():
    # base = rb.Base()
    # base.CreateFactoriesBase("Infos/Factories.txt")
    # base.PrintAllFactories()

    app = cgui.gui("Test gui")
    columns = 1
    rows = 30
    components = 5

    for column in range(columns):
        print(column, column * components)
        for row in range(rows):
            string = "Test text" + str(column) + ":" + str(row)
            app.addLabel(string + "Label", "Name", row, column * components)
            app.addEntry(string + "Entry", row, column * components + 1)
            app.setEntryDefault(string + "Entry", "0")
            app.addNamedCheckBox("Per minute", string + "Check box", row, column * components + 2)
            app.setCheckBox(string + "Check box", True)
            app.addOptionBox(string + "Option box", ["No acceleration", "Allow acceleration"], row, column * components + 3)
            app.addOptionBox(string + "Option box 2", ["Ignore remains", "Minimize remains", "Craft remains"], row, column * components + 4)


    app.go()

    pass

# TestMain()
MainMain()
