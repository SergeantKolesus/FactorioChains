from appJar import gui

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

    def __addItemButtonOnClickSub(self, btn):
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

        requirements = self.base.CalcualteMultipleRequest(requests)

        for key in requirements.keys():
            self.app.addListItem("Crafting requirements list box", str(key) + str(requirements[key]))

        # print()

        # self.app.updateListBox("Crafting requirements list box", requirements)

        # for requrement in requirements:
        #     self.app.addListItem("Crafting requirements list box", requrement.)


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
            res += str(product[1]) + " " + product[0] + " "

        res += "\nfrom "

        for component in recipe.component:
            res += str(component[1]) + " " + component[0] + " "

        if len(recipe.requirements) == 0:
            res += "\nand has no special requirements"
        else:
            res += "\nbut requires "

            for requirement in recipe.requirements:
                res += requirement[0] + " "

        if recipe.perMinute:
            res += "\nwith frequency " + str(recipe.frequency) + " item per minute"

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

        recipe = self.base.GetRecipe(self.app.getOptionBox("Recipes"))
        self.app.setLabel("Recipe view label", self.__createdMultistringRecipeDescription(recipe))

        self.app.setOptionBoxChangeFunction("Recipes", self.__updateRecipesInfoMain)
        pass

    def __createInputField(self):
        self.app.addListBox("Input recipes", [], 2, 0)
        # self.app.addButton("Add craft button", "Add item", 2, 0)
        self.app.addButton("Add", self.__addItemButtonOnClick, 1, 0)
        self.app.addButton("Calculate", self.__calculateButtonOnClick, 4, 0, 2, 1)

    def __createAddItemSubwindow(self):
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

    def __createResultsField(self):
        self.app.addListBox("Crafting requirements list box", [], 5, 0, 2, 1)

    def __init__(self, base):
        self.base = base
        self.app = gui("Calculator", "1280x1024")
        # self.app.setSticky("news")
        # self.app.setExpand("both")
        countInfo = "Total amount of recipeces parsed " + str(base.RecipesCount())
        self.app.addLabel("l1", countInfo)
        # self.app.addLabelOptionBox("Recipes", [], 1, 1)
        # self.app.addLabel("Selected recipe lbl", "", 1, 1)
        self.__createAllowedFactoriesCheckBox()
        self.__createInformationField()
        self.__createRecipeLookingField()
        self.__createInputField()
        self.__createAddItemSubwindow()
        self.__createResultsField()

        # self.app.addCheckBox()

    def Run(self):
        self.app.go()
