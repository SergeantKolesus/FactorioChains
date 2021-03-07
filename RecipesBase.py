import FactorioChains as fc
import math
import FactorioChains as fc

class CraftData:
    _recipes = []
    _factories = []
    _rawSources = []
    _components = []

    def __init__(self, files = []):
        if files == []:
            pass

    def RecipesCount(self):
        return len(self._recipes)

    def FactoriesCount(self):
        return len(self._factories)

    def RawSourcesCount(self):
        return len(self._rawSources)

    def ComponentsCount(self):
        return len(self._components)

    def PrintRecipes(self):
        for recipe in self._recipes:
            recipe.Print()

    def PrintFactories(self):
        for factory in self._factories:
            factory.Print()

    def PrintRawSources(self):
        for source in self._rawSources:
            source.Print()

    def PrintComponents(self):
        for component in self._components:
            component.Print()

    def AddRecipesFromFile(self, filename):
        with open(filename) as reader:
            while True:
                line = reader.readline()

                if (line == '') | (line == "stop\n"):
                    print("break")
                    break

                if line[0] == '#':
                    continue

                line = line[:-1]

                recipe = fc.Recipe()
                recipe.ParseFromLine(line)

                self._recipes.append(recipe)

    def AddFactoriesFromFile(self, filename):
        with open(filename) as reader:
            while True:
                line = reader.readline()

                if (line == '') | (line == "stop\n"):
                    print("break")
                    break

                if line[0] == '#':
                    continue

                line = line[:-1]

                factory = fc.Factory()
                factory.ParseFromLine(line)

                self. _factories.append(factory)

    def AddRawSourcesFromFile(self, filename):
        with open(filename) as reader:
            while True:
                line = reader.readline()

                if (line == '') | (line == "stop\n"):
                    print("break")
                    break

                if line[0] == '#':
                    continue

                if not line[-1].isprintable():
                    line = line[:-1]

                source = fc.RawSource()
                source.ParseFromLine(line)
                self._rawSources.append(source)

    def RenewComponentsList(self):
        for recipe in self._recipes:
            for component in recipe.components:
                comp = fc.Component(component[0])

                if not (comp in self._components):
                    self._components.append(comp)

            for product in recipe.products:
                comp = fc.Component(product[0])

                if not (comp in self._components):
                    self._components.append(comp)

    def GetAllRecipes(self):
        return self._recipes

    def GetAllRecipesNames(self):
        res = list()

        for recipe in self._recipes:
            res.append(recipe.name)

        return res

    def GetAllFactories(self):
        return self._factories

    def GetAllRawSources(self):
        return self._rawSources

    def GetAllComponentsNames(self):
        res = list()

        for component in self._components:
            res.append(component.name)

        return res

    def FillFromFile(self, files):
        self.AddRecipesFromFile(files["recipes"])
        self.AddFactoriesFromFile(files["factories"])
        self.AddRawSourcesFromFile(files["raw sources"])
        self.RenewComponentsList()

    def GetRecipeByName(self, name):
        recipe = list(filter(lambda x: name == x.name, self._recipes))
        if len(recipe) != 0:
            recipe = recipe[0]

        return recipe

    def GetRecipesByProduct(self, product):
        recipes = list()

        for recipe in self._recipes:
            for prod in recipe.products:
                if product == prod[0]:
                    recipes.append(recipe)
                    break

        if recipes == []:
            return recipes

        return recipes

    def __selectProperRecipe(self, recipe):
        return recipe[0]

    def __isRaw(self, component):
        source = fc.RawSource(component.name)

        return source in self._rawSources

    def __CalculateSubrecipe(self, item, count):

        if self.__isRaw(fc.Component(item)):
            return
        # if item in self._rawSources:
        #     return

        recipe = self.GetRecipesByProduct(item)

        print("Item: ", item, " recipe: ", recipe)

        if recipe == []:
            print("Recipe not found")
            return

        recipe = self.__selectProperRecipe(recipe)
        prodIndex = recipe.GetProductIndex(item)

        recipe.Print()

        requiredEfficiency = count / (recipe.perMinuteOperations * recipe.products[prodIndex][1])

        print("Efficiency: ", requiredEfficiency)

        print(recipe.products[prodIndex][0])

        if recipe.products[prodIndex][0] in self.productionSummary:
            print("Old one: ", recipe.products[prodIndex][0])
            # temp = self.productionSummary[recipe.products[prodIndex][0]]
            # self.productionSummary[recipe.products[prodIndex][0]] = [temp[0] + count, temp[1] + requiredEfficiency, recipe.requirements]
            self.productionSummary[recipe.products[prodIndex][0]].Append(requiredEfficiency)
        else:
            print("New one: ", recipe.products[prodIndex][0])
            self.productionSummary[recipe.products[prodIndex][0]] = fc.CraftRequirement(recipe.products[prodIndex], count, recipe.components, requiredEfficiency, recipe.requirements)
            print("Added one: ", self.productionSummary[recipe.products[prodIndex][0]])
            # self.productionSummary[recipe.products[prodIndex][0]] = [count, requiredEfficiency, recipe.requirements, recipe.components, recipe.products]

        for component in recipe.components:
            if not (fc.Component(component[0]) in self._rawSources):
                self.__CalculateSubrecipe(component[0], component[1] * requiredEfficiency)

    def __getProperFactories(self, request):
        print("Searching factory for ", request)

        matchingfactories = self._factories.copy()
        print("Matching factories: ", matchingfactories)

        for requirement in request.requirements:
            print("Req: ", requirement)
            matchingfactories[0].Print()
            matchingfactories = list(filter(lambda x: requirement in x.allowances, matchingfactories))
            print("Tmatch: ", matchingfactories)

        print("Matching factories: ", matchingfactories)

        request.GiveFactories(matchingfactories)
        request.FindFactoryCount()

        # print("match: ", matchingfactories)

        return matchingfactories

    def __refactorProductionSummary(self):
        for propkey in self.productionSummary.keys():
            prop = self.productionSummary[propkey]
            print("Prop: ", prop)
            self.__getProperFactories(prop)

            prop.Print()


    def CalculateMultipleRequest(self, data):
        self.productionSummary = {}

        print("Data: ", data)

        for pair in data:
            # print("pair:", pair)
            # recipe = self.GetRecipeByName(pair[0])
            # print(recipe)
            # requiredEfficiency = pair[1] / recipe.frequency
            self.__CalculateSubrecipe(pair[0], pair[1])

        # print("Total collected data length: ", len(self.productionSummary))

        self.__refactorProductionSummary()

        # for propkey in self.productionSummary.keys():
        #     prop = self.productionSummary[propkey]
        #     factories = self.__getProperFactories(prop)
        #
        #     if (factories == []):
        #         print("Error: no factory found")
        #         continue
        #
        #     efficiency = -1
        #     selectedFactory = []
        #
        #     for factory in factories:
        #         if factory[2] > efficiency:
        #             efficiency = factory[2]
        #             selectedFactory = factory
        #
        #     # print(selectedFactory)
        #
        #     factoriesCount = math.ceil(prop[1] / selectedFactory[2])
        #     self.productionSummary[propkey] = [selectedFactory[0], factoriesCount]
        #
        #     # key = self.productionSummary.
        #
        #     # print(factory[0], ": ", factoriesCount, ": ", data[0])
        #
        # print(self.productionSummary)

        return self.productionSummary
