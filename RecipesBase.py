import FactorioChains as fc
import math
# def FirstIndexOf(array, element):
#     i = 0
#
#     for val in array:
#         if val == element:
#             return i
#         i += 1
#
#     return -1
#
#
# def DivideEnumeration(words):
#     res = list()
#     # print("In divide ", words)
#
#     while "and" in words:
#         block = words[:FirstIndexOf(words, "and")]
#         del words[:len(block) + 1]
#         if block[0].isnumeric():
#             compCount = int(block[0])
#             del block[0]
#         else:
#             compCount = 1
#
#         block = " ".join(block)
#
#         res.append([block, compCount])
#
#     if words[0].isnumeric():
#         compCount = int(words[0])
#         del words[0]
#     else:
#         compCount = 1
#
#     words = " ".join(words[:])
#
#     res.append([words, compCount])
#
#     return res
#
# def DivideEnumerationCountless(words):
#     res = []
#
#     if len(words) == 0:
#         return res
#
#     while "and" in words:
#         block = words[:FirstIndexOf(words, "and")]
#         del words[:len(block) + 1]
#
#         block = " ".join(block[:])
#         res.append(block)
#
#     words = " ".join(words[:])
#     res.append(words)
#
#     return res
#
# def ParseRecipe(string):
#     words = string.split()
#
#     if "per minute" in string:
#         # print("Per minute detected")
#         perMinuteCount = int(words[-1])
#         del words[-1]
#         del words[-1]
#         del words[-1]
#         perMinute = [True, perMinuteCount]
#     else:
#         perMinute = [False, 60]
#
#     if "recipe:" in words:
#         name = words[:FirstIndexOf(words, "recipe:")]
#         # if len(name) > 1:
#         # print(words)
#         del words[:len(name) + 1]
#         name = " ".join(name)
#     else:
#         name = "unnamed"
#
#     lastProduct = FirstIndexOf(words, "from")
#     products = DivideEnumeration(words[:lastProduct])
#     del words[:lastProduct + 1]
#     if "requires" in words:
#         lastComponent = FirstIndexOf(words, "requires")
#     else:
#         lastComponent = len(words)
#
#     components = words[:lastComponent].copy()
#     del words[:len(components)]
#
#     components = DivideEnumeration(components)
#
#     if len(words) != 0:
#         del words[0]
#
#     requirements = DivideEnumerationCountless(words)
#
#     return name, products, components, requirements, perMinute
#
#
# def PrintRecipe(recipe):
#     print(recipe)
#
#
# def IsSpecific(word):
#     specific = "and", "from", "recipe:", "requires"
#     return word in specific
#
#
# def ParseRecipes(line):
#     words = line.split()
#     stack = []
#     length = len(words)
#     perMinute = []
#     name = "recipe"
#     components = list()
#     products = list()
#     requirements = list()
#
#     val = words[-3:]
#     # print(val)
#
#     perMinute = False
#
#     if ("per" in val) and ("minute" in val):
#         try:
#             count = float(val[0])
#         except Exception:
#             try:
#                 count = float(val[2])
#             except Exception:
#                 count = 60
#         # count = int([x for x in val if x.isnumeric()][0])
#         perMinute = [True, count]
#         del words[-3:]
#         # print(count)
#     else:
#         perMinute = [False, 60]
#
#     length = len(words)
#
#     package = list()
#     packageComponent = []
#     count = 1
#     phrase = ""
#
#     while length > 0:
#         length -= 1
#         val = words.pop()
#
#         # print(val)
#
#         if IsSpecific(val):
#             # print("Specific val ", val)
#             if phrase[-1] == ' ':
#                 phrase = phrase[:-1]
#             packageComponent = [phrase, count]
#             count = 1
#             phrase = ""
#             package.append(packageComponent)
#             packageComponent = list()
#             if val == "from":
#                 components.append(package)
#                 package = list()
#             if val == "requires":
#                 requirements.append(package)
#                 package = list()
#             if val == "recipe:":
#                 products.append(package)
#                 package = list()
#         else:
#             if val.isnumeric():
#                 count = int(val)
#             else:
#                 phrase = val + " " + phrase
#
#     if len(products) != 0:
#         name = phrase[:-1]
#     else:
#         products.append(package)
#
#     products = products[0]
#     components = components[0]
#
#     if len(requirements) != 0:
#         requirements = requirements[0]
#
#     return name, products, components, requirements, perMinute

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


class Base:
    _recipes = []
    _components = []
    _rawSources = []
    _factories = []

    def __init__(self):
        pass

    def FillBase(self, files):
        pass

    def FactoriesCount(self):
        return len(self._factories)

    def RecipesCount(self):
        return len(self._recipes)

    def RawSourceCount(self):
        return len(self._rawSources)

    def AddRecipe(self, recipe):
        self._recipes.append(recipe)

    def AddComponent(self, component):
        if not component in self._components:
            self._components.append(component)

    def GetAllFactories(self):
        res = []

        for factory in self._factories:
            res.append(factory[0])

        return res

    def GetAllRecipes(self):
        res = []

        for recipe in self._recipes:
            if recipe.name != "recipe":
                res.append(recipe.name)
            else:
                res.append("Unnamed " + recipe.product[0])

        return res

    def GetSpecifiedRecipe(self, name):
        recipe = list(filter(lambda x: x.name == name, self._recipes))
        return recipe

    def GetSpecifiedFactory(self, name):
        return list(filter(lambda x: x.name == name, self._factories))

    def CreateRecipe(self, description):
        name, products, components, requirements, perMinute = ParseRecipes(description)

        recipe = fc.Recipe(name)

        if perMinute[0]:
            recipe.ChangeCountType(perMinute[1])

        for product in products:
            recipe.AddProduct(product[0], product[1])

        for component in components:
            recipe.AddComponent(component[0], component[1])

        for requirement in requirements:
            recipe.AddRequirement(requirement)

        self._recipes.append(recipe)

        return recipe

    def CreateRawSourcesBase(self, filename):
        with open(filename) as reader:
            while True:
                line = reader.readline()

                if (line == '') | (line == "stop\n"):
                    print("break")
                    break

                if line[0] == '#':
                    continue

                line = line[:-1]

                self._rawSources.append(line)

    def CreateRecipesBase(self, filename):
        with open(filename) as reader:

            while True:
                line = reader.readline()

                if (line == '') | (line == "stop\n"):
                    print("break")
                    break

                if line[0] != '#':
                    rec = self.CreateRecipe(line)

    def PrintAllKnownSources(self):
        print("Known raw sources: ")
        for source in self._rawSources:
            print(source, end=", ")
        print()

    def __ParseFactoryLine(self, line):
        words = line.split()
        length = len(words)
        specials = ["consumes", "efficiency", "allow", "and"]
        phrase = ""
        allowance = []
        consumption = []
        efficiency = 1
        value = 1
        valSet = False
        phraseBlock = list()

        while length > 0:
            length -= 1
            val = words.pop()

            # print(val)

            try:
                value = float(val)
                valSet = True
                # print(value)
                continue
            except ValueError:
                pass

            if val in specials:
                if val == "consumes":
                    if phrase[-1] == ' ':
                        phrase = phrase[:-1]
                    if len(phraseBlock) != 0:
                        phraseBlock.append([phrase, value])
                        consumption = phraseBlock.copy()
                    else:
                        consumption = [phrase, value]
                    phrase = ""
                    valSet = False
                    phraseBlock = list()

                if val == "efficiency":
                    efficiency = value
                    phrase = ""
                    valSet = False

                if val == "allow":
                    if phrase[-1] == ' ':
                        phrase = phrase[:-1]

                    if len(phraseBlock) != 0:
                        phraseBlock.append(phrase)
                        allowance = phraseBlock.copy()

                        phraseBlock = list()
                    else:
                        allowance = phrase
                    phrase = ""
                    valSet = False

                if val == "and":
                    if phrase[-1] == ' ':
                        phrase = phrase[:-1]

                    phraseBlock.append([phrase, value])
                    phrase = ""
                    # print(phraseBlock)

            else:
                phrase = val + " " + phrase

        # print(phrase)

        if phrase[-1] == ' ':
            phrase = phrase[:-1]

        if valSet:
            if int(value) == value:
                value = int(value)
            phrase += " " + str(value)

        # print(allowance)

        for i in range(len(allowance)):
            # print(allowance[i], i, len(allowance[i]))
            if not (type(allowance[i]) == str):
                allowance.append(allowance[i][0])
                del allowance[i]
                i -= 1

        return [phrase, consumption, efficiency, allowance]

    def CreateFactoriesBase(self, filename):
        with open(filename) as reader:
            while True:
                line = reader.readline()

                if (line == '') | (line == "stop\n"):
                    print("break")
                    break

                if line[0] == '#':
                    continue

                line = line[:-1]

                self._factories.append(self.__ParseFactoryLine(line))

    def PrintAllFactories(self):
        print("Usable factories are: ")
        for factory in self._factories:
            print(factory)

    def PrintAllRecipes(self):
        print("Contains ", self.RecipesCount(), " recipes:")
        for recipe in self._recipes:
            PrintRecipe(recipe)

    def GetRecipeByName(self, name):
        # for recipe in self._recipes:
        #     print(recipe.name)

        recipe = list(filter(lambda x: name == x.name, self._recipes))
        # print(recipe)
        if len(recipe) != 0:
            recipe = recipe[0]

        return recipe

    def GetFirstRecipeByProduct(self, product):
        recipe = list(filter(lambda x: product in x.product[0], self._recipes))
        if len(recipe) != 0:
            recipe = recipe[0]

        return recipe

    def GetRecipesByProduct(self, product):
        # recipe = list(filter(lambda x: product in x.product[0], self._recipes))
        # if len(recipe) != 0:
        #     recipe = recipe[0]

        recipes = list()

        for recipe in self._recipes:
            # print(recipe.product[:])
            t = list(filter(lambda x:  product == x[0], recipe.product))
            if t != []:
                recipes.append(recipe)

        if recipes == []:
            return recipes

        print(recipes)

        return recipes[0]
        # return list(filter(lambda x: product for product in x.product if product in product, self._recipes))

    productionSummary = {}

    def __CalculateSybrecipe(self, item, count):
        print("Item: ", item)

        if item in self._rawSources:
            return

        recipe = self.GetRecipesByProduct(item)

        if recipe == []:
            print("Recipe not found")
            return

        print(recipe)

        # recipe = recipe[0]

        print("Recipe: ", recipe)

        requiredEfficiency = count / recipe.frequency

        if recipe.product[0][0] in self.productionSummary:
            temp = self.productionSummary[recipe.product[0][0]]
            self.productionSummary[recipe.product[0][0]] = [temp[0] + count, temp[1] + requiredEfficiency, recipe.requirements]
        else:
            self.productionSummary[recipe.product[0][0]] = [count, requiredEfficiency, recipe.requirements, recipe.component, recipe.product]

        for component in recipe.component:
            # print(component)
            print("Component: ", component)
            if not (component[0] in self._rawSources):
                self.__CalculateSybrecipe(component[0], component[1] * requiredEfficiency)

    def __getProperFactories(self, request):
        # print("Require: ")
        #
        # for requirement in request[2]:
        #     print(requirement)
        # for factory in self._factories:
        #     print(factory)

        #
        # if request[2] == []:
        #     print("Crafting")

        matchingfactories = self._factories.copy()

        for reqirement in request[2]:
            # print("Req: ", reqirement)
            matchingfactories = list(filter(lambda x: reqirement[0] in x[3], matchingfactories))
            # print("Tmatch: ", matchingfactories)

        # print("match: ", matchingfactories)

        return matchingfactories

    def CalculateRequest(self, item, count):
        self.productionSummary = {}

        recipe = self.GetRecipeByName(item)
        print(recipe)

        if recipe != []:
            return 0

        requiredEfficiency = count / recipe.frequency

        self.__CalculateSybrecipe(item, count)

        return self.productionSummary

    def CalculateMultipleRequest(self, data):
        self.productionSummary = {}

        print("Data: ", data)

        for pair in data:
            print("pair:", pair)
            recipe = self.GetRecipeByName(pair[0])
            print(recipe)
            requiredEfficiency = pair[1] / recipe.frequency
            self.__CalculateSybrecipe(pair[0], pair[1])

        for propkey in self.productionSummary.keys():
            prop = self.productionSummary[propkey]
            factories = self.__getProperFactories(prop)

            if(factories == []):
                print("Error: no factory found")
                continue

            efficiency = -1
            selectedFactory = []

            for factory in factories:
                if factory[2] > efficiency:
                    efficiency = factory[2]
                    selectedFactory = factory

            # print(selectedFactory)

            factoriesCount = math.ceil(prop[1] / selectedFactory[2])
            self.productionSummary[propkey] = [selectedFactory[0], factoriesCount]

            # key = self.productionSummary.

            # print(factory[0], ": ", factoriesCount, ": ", data[0])

        print(self.productionSummary)

        return self.productionSummary
