import FactorioChains as fc

def FirstIndexOf(array, element):
    i = 0

    for val in array:
        if val == element:
            return i
        i += 1

    return -1


def DivideEnumeration(words):
    res = list()
    # print("In divide ", words)

    while "and" in words:
        block = words[:FirstIndexOf(words, "and")]
        del words[:len(block) + 1]
        if block[0].isnumeric():
            compCount = int(block[0])
            del block[0]
        else:
            compCount = 1

        block = " ".join(block)

        res.append([block, compCount])

    if words[0].isnumeric():
        compCount = int(words[0])
        del words[0]
    else:
        compCount = 1

    words = " ".join(words[:])

    res.append([words, compCount])

    return res

def DivideEnumerationCountless(words):
    res = []

    if len(words) == 0:
        return res

    while "and" in words:
        block = words[:FirstIndexOf(words, "and")]
        del words[:len(block) + 1]

        block = " ".join(block[:])
        res.append(block)

    words = " ".join(words[:])
    res.append(words)

    return res

def ParseRecipe(string):
    words = string.split()

    if "per minute" in string:
        # print("Per minute detected")
        perMinuteCount = int(words[-1])
        del words[-1]
        del words[-1]
        del words[-1]
        perMinute = [True, perMinuteCount]
    else:
        perMinute = [False, 60]

    if "recipe:" in words:
        name = words[:FirstIndexOf(words, "recipe:")]
        # if len(name) > 1:
        # print(words)
        del words[:len(name) + 1]
        name = " ".join(name)
    else:
        name = "unnamed"

    lastProduct = FirstIndexOf(words, "from")
    products = DivideEnumeration(words[:lastProduct])
    del words[:lastProduct + 1]
    if "requires" in words:
        lastComponent = FirstIndexOf(words, "requires")
    else:
        lastComponent = len(words)

    components = words[:lastComponent].copy()
    del words[:len(components)]

    components = DivideEnumeration(components)

    if len(words) != 0:
        del words[0]

    requirements = DivideEnumerationCountless(words)

    return name, products, components, requirements, perMinute


def PrintRecipe(recipe):
    print(recipe)


def IsSpecific(word):
    specific = "and", "from", "recipe:", "requires"
    return word in specific


def ParseRecipes(line):
    words = line.split()
    stack = []
    length = len(words)
    perMinute = []
    name = "recipe"
    components = list()
    products = list()
    requirements = list()

    val = words[-3:]
    # print(val)

    perMinute = False

    if ("per" in val) and ("minute" in val):
        try:
            count = float(val[0])
        except Exception:
            try:
                count = float(val[2])
            except Exception:
                count = 60
        # count = int([x for x in val if x.isnumeric()][0])
        perMinute = [True, count]
        del words[-3:]
        # print(count)
    else:
        perMinute = [False, 60]

    length = len(words)

    package = list()
    packageComponent = []
    count = 1
    phrase = ""

    while length > 0:
        length -= 1
        val = words.pop()

        # print(val)

        if IsSpecific(val):
            # print("Specific val ", val)
            if phrase[-1] == ' ':
                phrase = phrase[:-1]
            packageComponent = [phrase, count]
            count = 1
            phrase = ""
            package.append(packageComponent)
            packageComponent = list()
            if val == "from":
                components.append(package)
                package = list()
            if val == "requires":
                requirements.append(package)
                package = list()
            if val == "recipe:":
                products.append(package)
                package = list()
        else:
            if val.isnumeric():
                count = int(val)
            else:
                phrase = val + " " + phrase

    if len(products) != 0:
        name = phrase[:-1]
    else:
        products.append(package)

    products = products[0]
    components = components[0]

    if len(requirements) != 0:
        requirements = requirements[0]

    return name, products, components, requirements, perMinute


class Base:
    _recipes = []
    _components = []
    _rawSources = []
    _factories = []

    def __init__(self):
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

    def GetRecipe(self, item):
        recipe = list(filter(lambda x: item == x.product[0][0], self._recipes))
        if len(recipe) != 0:
            recipe = recipe[0]

        return recipe

    productionSummary = {}

    def __CalculateSybrecipe(self, item, count):
        recipe = self.GetRecipe(item)

        if recipe == []:
            return

        # print(recipe)

        requiredEfficiency = count / recipe.frequency

        if recipe.product[0][0] in self.productionSummary:
            temp = self.productionSummary[recipe.product[0][0]]
            self.productionSummary[recipe.product[0][0]] = [temp[0] + count, temp[1] + requiredEfficiency]
        else:
            self.productionSummary[recipe.product[0][0]] = [count, requiredEfficiency]

        for component in recipe.component:
            # print(component)
            if not (component in self._rawSources):
                self.__CalculateSybrecipe(component[0], component[1] * count)

    def CalculateRequest(self, item, count):
        self.productionSummary = {}

        recipe = self.GetRecipe(item)
        print(recipe)

        if recipe != []:
            return 0

        requiredEfficiency = count / recipe.frequency

        self.__CalculateSybrecipe(item, count)

        return self.productionSummary

    def CalcualteMultipleRequest(self, data):
        self.productionSummary = {}

        for pair in data:
            # print(pair)
            recipe = self.GetRecipe(pair[0])
            # print(recipe)
            requiredEfficiency = pair[1] / recipe.frequency
            self.__CalculateSybrecipe(pair[0], pair[1])

        return self.productionSummary
