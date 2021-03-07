from appJar import gui

class FactorioCalculatorApp:
    base = None
    app = None

    def __updateRecipesInfoMain(self):
        self.__updateRecipeInfoField("Recipes", "Recipe view label")

    def __updateRecipeInfoField(self, optionBox, label):
        recipe = self.base.GetRecipeByName(self.app.getOptionBox(optionBox))

        self.app.setLabel(label, recipe.GetMultistringDescription())

    def __calculateButtonOnClick(self, btn):
        requests = list()

        for line in self.app.getListBox("Input recipes"):
            words = line.split()
            count = float(words[0])
            del words[0]
            name = ""
            for word in words:
                if word == "per":
                    break
                name += word + " "

            name = name[:-1]
            requests.append([name, count])

        requirements = self.base.CalculateMultipleRequest(requests)

        for key in requirements.keys():
            self.app.addListItem("Crafting requirements list box", str(requirements[key].GetInfoString()))

    def __addItemButtonOnClick(self, btn):
        self.app.showSubWindow("Add item")

    def __addItemButtonOnClickSub(self, btn):
        for entry in self.app.getAllEntries():
            text = self.app.getEntry(entry)

            if text == "":
                continue

            if text == "0":
                continue

            try:
                count = float(text)
            except:
                count = 60

            groupName = entry[:-5]
            item = self.app.getLabel(groupName + "Label")
            print(item)

            addingItemName = str(count) + " " + item

            if self.app.getCheckBox(groupName + "Check box"):
                addingItemName += " per minute"

            self.app.addListItem("Input recipes", addingItemName)
            self.app.hideSubWindow("Add item")

    def __createInformationWindow(self):
        infostr = "Known recipes count: " + str(self.base.RecipesCount())
        infostr += '\n' + "Known factories count: " + str(self.base.FactoriesCount())
        infostr += '\n' + "Known raw sources count: " + str(self.base.RawSourcesCount())
        self.app.addLabel("info l1", infostr, 0, 0)

    def __createAllowedFactoriesCheckBox(self):
        factories = self.base.GetAllFactories()
        props = {}

        for factory in factories:
            props[factory.name] = True

        self.app.addProperties("Factories", props, 0, 1)

    def __createRecipeLookingField(self):
        recipes = self.base.GetAllRecipesNames()

        self.app.addLabelOptionBox("Recipes", recipes, 1, 1)
        self.app.addLabel("Recipe view label", "", 2, 1)

        recipe = self.base.GetRecipeByName(self.app.getOptionBox("Recipes"))
        self.app.setLabel("Recipe view label", recipe.GetMultistringDescription())

        self.app.setOptionBoxChangeFunction("Recipes", self.__updateRecipesInfoMain)
        pass

    def __createInputField(self):
        self.app.addListBox("Input recipes", [], 2, 0)
        self.app.addButton("Add", self.__addItemButtonOnClick, 1, 0)
        self.app.addButton("Calculate", self.__calculateButtonOnClick, 4, 0, 2, 1)

    def __createResultsField(self):
        self.app.addListBox("Crafting requirements list box", [], 5, 0, 2, 1)

    def __createMainWindown(self):
        self.__createInformationWindow()
        self.__createAllowedFactoriesCheckBox()
        self.__createRecipeLookingField()
        self.__createInputField()
        self.__createResultsField()

        pass

    def __calculateSubwindowGridSize(self, count):
        rows = 0
        columns = 0
        maxColumn = 30

        if count <= maxColumn:
            rows = count
            columns = 1
        else:
            columns = int(count / maxColumn)

            if (count % maxColumn) != 0:
                columns += 1

            rows = int(count / columns)

            if (count % columns) != 0:
                rows += 1

        print(columns, rows)
        return rows, columns

    def __createAddItemSubwindow(self):
        sub = self.app.startSubWindow("Add item", modal=True)
        count = self.base.ComponentsCount()
        components = 5
        i = 0

        componentslist = self.base.GetAllComponentsNames()
        print(componentslist)

        rows, columns = self.__calculateSubwindowGridSize(count)

        for column in range(columns):
            print(column, column * components)
            for row in range(rows):
                if i == count:
                    break

                string = "Test text" + str(column) + ":" + str(row)
                self.app.addLabel(string + "Label", componentslist[i], row, column * components)
                self.app.addEntry(string + "Entry", row, column * components + 1)
                self.app.setEntryDefault(string + "Entry", "0")
                self.app.addNamedCheckBox("Per minute", string + "Check box", row, column * components + 2)
                self.app.setCheckBox(string + "Check box", True)
                self.app.addOptionBox(string + "Option box", ["No acceleration", "Allow acceleration"], row,
                                 column * components + 3)
                self.app.addOptionBox(string + "Option box 2", ["Ignore remains", "Minimize remains", "Craft remains"], row,
                                 column * components + 4)
                i += 1

        self.app.addNamedButton("Add", "Add item sub button", self.__addItemButtonOnClickSub, rows, 0, components * columns)
        self.app.stopSubWindow()

    def Run(self):
        self.app.go()

    def __init__(self, base):
        self.base = base
        self.app = gui("Factorio calculator", "1280x1024")
        self.__createMainWindown()
        self.__createAddItemSubwindow()
