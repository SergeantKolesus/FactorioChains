from appJar import gui

class RecipesApp:
    def __createAllowedFactoriesCheckBox(self, base):
        factories = base.GetAllFactories()
        print(factories)
        n = len(factories)
        props = {}
        i = 0
        for factory in factories:
            print(factory)
            props[factory] = False
            # self.app.addNamedCheckBox(factory, i, 0, 3, 1, n)
            i += 1

        self.app.addProperties("Factories", props, 0, 1)
        pass

    def __init__(self, base):
        self.app = gui("Calculator", "640x480")
        # self.app.setSticky("news")
        # self.app.setExpand("both")
        countInfo = "Total amount of recipeces parsed " + str(base.RecipesCount())
        self.app.addLabel("l1", countInfo)
        self.app.addLabelOptionBox("Recipes", [], 1, 1)
        self.__createAllowedFactoriesCheckBox(base)
        # self.app.addCheckBox()

    def Run(self):
        self.app.go()
