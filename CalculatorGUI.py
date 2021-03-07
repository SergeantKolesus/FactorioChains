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

    def __init__(self, base):
        self.base = base
        self.app = gui("Factorio calculator", "1280x1024")
        self.__createMainWindown()
        self.__createAddItemSubwindow()
        self.app.go()

class RecipesApp:
    base = []

    def __updateRecipesInfoMain(self):
        self.__updateRecipeInfoField("Recipes", "Recipe view label")

    def __updateRecipesInfoSub(self):
        self.__updateRecipeInfoField("Add recipe ob", "Recipe info label sub")

    def __updateRecipeInfoField(self, optionBox, label):
        # print("Updated")
        recipe = self.base.GetSpecifiedRecipe(self.app.getOptionBox(optionBox))[0]

        # print(self.__createdMultistringRecipeDescription(recipe))
        self.app.setLabel(label, self.__createdMultistringRecipeDescription(recipe))
        pass

    def __addItemButtonOnClick(self, btn):
        self.app.showSubWindow("Add item")
        pass

    def __addItemButtonOnClickSubOld(self, btn):
        addingItemName = self.app.getOptionBox("Add recipe ob")
        print(addingItemName)
        try:
            count = float(self.app.getEntry("Per minute production entry sub"))
        except Exception:
            count = 60

        addingItemName = str(count) + " " + addingItemName + " per minute"
        # self.app.setListBoxRows("Input recipes", self.  app.getListBox("Input recipes"))
        self.app.addListItem("Input recipes", addingItemName)
        self.app.hideSubWindow("Add item")
        pass

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

        print(requirements)

        for key in requirements.keys():
            self.app.addListItem("Crafting requirements list box", str(key) + str(requirements[key]))

    def __createAllowedFactoriesCheckBox(self):
        factories = self.base.GetAllFactories()
        # print(factories)
        props = {}

        for factory in factories:
            # print(factory)
            props[factory] = True

        self.app.addProperties("Factories", props, 0, 1)

    def __createdMultistringRecipeDescription(self, recipe):
        res = "Creates "

        for product in recipe.product:
            res += str(product[1]) + " " + product[0] + " and "

        res = res[:-4]
        res += "\nfrom "

        for component in recipe.component:
            res += str(component[1]) + " " + component[0] + " and "

        res = res[:-4]

        if len(recipe.requirements) == 0:
            res += "\nand has no special requirements"
        else:
            res += "\nbut requires "

            for requirement in recipe.requirements:
                res += requirement[0] + " "

        if recipe.perMinute:
            res += "\nwith frequency " + str(recipe.frequency) + " operations per minute"

        return res

    def __createInformationField(self):
        # self.app.addScrolledTextArea("Info text area", 0, 0)
        infostr = "Known recipes count: " + str(self.base.RecipesCount())
        infostr += '\n' + "Known factories count: " + str(self.base.FactoriesCount())
        infostr += '\n' + "Known raw sources count: " + str(self.base.RawSourceCount())
        self.app.addLabel("info l1", infostr, 0, 0)
        # self.app.addLabel("info l2", "Known recipes: " + str(self.base.RecipesCount() + 5), 0, 0)

    def __createRecipeLookingField(self):
        recipes = self.base.GetAllRecipes()

        self.app.addLabelOptionBox("Recipes", recipes, 1, 1)
        self.app.addLabel("Recipe view label", "", 2, 1)

        recipe = self.base.GetRecipeByName(self.app.getOptionBox("Recipes"))
        self.app.setLabel("Recipe view label", self.__createdMultistringRecipeDescription(recipe))

        self.app.setOptionBoxChangeFunction("Recipes", self.__updateRecipesInfoMain)
        pass

    def __createInputField(self):
        self.app.addListBox("Input recipes", [], 2, 0)
        # self.app.addButton("Add craft button", "Add item", 2, 0)
        self.app.addButton("Add", self.__addItemButtonOnClick, 1, 0)
        self.app.addButton("Calculate", self.__calculateButtonOnClick, 4, 0, 2, 1)

    def __createResultsField(self):
        self.app.addListBox("Crafting requirements list box", [], 5, 0, 2, 1)

    def __createAddItemSubwindowOld(self):
        sub = self.app.startSubWindow("Add item", modal=True)
        self.app.addOptionBox("Add recipe ob", self.base.GetAllRecipes(), 0, 0, 2, 1)
        recipe = self.base.GetRecipe(self.app.getOptionBox("Add recipe ob"))
        self.app.addLabel("Recipe info label sub", self.__createdMultistringRecipeDescription(recipe), 1, 0, 2, 1)
        self.app.setOptionBoxChangeFunction("Add recipe ob", self.__updateRecipesInfoSub)
        # self.app.setSize(480, 480)
        self.app.addLabel("Per minute phrase label sub", "Production per minute:", 2, 0)
        self.app.addEntry("Per minute production entry sub", 2, 1)
        self.app.setEntry("Per minute production entry sub", "60")
        self.app.addNamedButton("Add", "Add item sub button", self.__addItemButtonOnClickSub, 3, 0, 2, 1)
        self.app.stopSubWindow()

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
        count = self.base.RecipesCount()
        components = 5
        i = 0
        recipes = self.base.GetAllRecipes()

        rows, columns = self.__calculateSubwindowGridSize(count)

        for column in range(columns):
            print(column, column * components)
            for row in range(rows):
                if i == count:
                    break

                string = "Test text" + str(column) + ":" + str(row)
                self.app.addLabel(string + "Label", recipes[i], row, column * components)
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

    def __init__(self, base):
        self.base = base
        self.app = gui("Calculator", "1280x1024")
        countInfo = "Total amount of recipeces parsed " + str(base.RecipesCount())
        self.app.addLabel("l1", countInfo)
        self.__createAllowedFactoriesCheckBox()
        self.__createInformationField()
        self.__createRecipeLookingField()
        self.__createInputField()
        self.__createAddItemSubwindow()
        self.__createResultsField()

        # self.app.addCheckBox()

    def Run(self):
        self.app.go()
