from appJar import gui

class RecipesApp:
    base = []

    def __createAllowedFactoriesCheckBox(self):
        factories = self.base.GetAllFactories()
        # print(factories)
        props = {}

        for factory in factories:
            # print(factory)
            props[factory] = True

        self.app.addProperties("Factories", props, 0, 1)

    def __createInformationField(self):
        # self.app.addScrolledTextArea("Info text area", 0, 0)
        infostr = "Known recipes count: " + str(self.base.RecipesCount())
        infostr += '\n' + "Known factories count: " + str(self.base.FactoriesCount())
        infostr += '\n' + "Known raw sources count: " + str(self.base.RawSourceCount())
        self.app.addLabel("info l1", infostr, 0, 0)
        # self.app.addLabel("info l2", "Known recipes: " + str(self.base.RecipesCount() + 5), 0, 0)

    def __createRecipeLookingField(self):
        pass

    def __init__(self, base):
        self.base = base
        self.app = gui("Calculator", "640x480")
        # self.app.setSticky("news")
        # self.app.setExpand("both")
        countInfo = "Total amount of recipeces parsed " + str(base.RecipesCount())
        self.app.addLabel("l1", countInfo)
        self.app.addLabelOptionBox("Recipes", [], 1, 1)
        self.app.addLabel("Selected recipe lbl", "", 1, 1)
        self.__createAllowedFactoriesCheckBox()
        self.__createInformationField()
        # self.app.addCheckBox()

    def Run(self):
        self.app.go()
