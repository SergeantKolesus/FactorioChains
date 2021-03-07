import math

def IsSpecific(word, type):
    specificWords = {
        "recipe": ["and", "from", "recipe:", "requires"],
        "factory": ["consumes", "efficiency", "allow", "and"]
    }
    return word in specificWords[type]

class Recipe:
    products = []
    components = []
    requirements = []
    name = []
    perMinuteOperations = 60

    def __init__(self):
        pass

    def GetProductIndex(self, product):
        for i in range(len(self.products)):
            if self.products[i][0] == product:
                return i

        return -1

    def Print(self):
        print(self.name, " recipe: crafts ",
              self.products, " from ",
              self.components, end='')

        if self.requirements == []:
            print(" and has no requirements ")
        else:
            print(" and requires ", self.requirements)

    def ParseFromLine(self, line):
        words = line.split()
        self.name = "recipe"
        self.components = list()
        self.products = list()
        self.requirements = list()

        val = words[-3:]

        # print(val)

        if ("per" in val) and ("minute" in val):
            try:
                self.perMinuteOperations = float(val[0])
            except Exception:
                try:
                    self.perMinuteOperations = float(val[2])
                except Exception:
                    self.perMinuteOperations = 1
            del words[-3:]
        else:
            self.perMinuteOperations = 1

        length = len(words)

        package = list()
        packageComponent = []
        count = 1
        phrase = ""

        while length > 0:
            length -= 1
            val = words.pop()

            if IsSpecific(val, "recipe"):
                if phrase[-1] == ' ':
                    phrase = phrase[:-1]
                packageComponent = [phrase, count]
                count = 1
                phrase = ""
                package.append(packageComponent)
                packageComponent = list()
                if val == "from":
                    self.components.append(package)
                    package = list()
                if val == "requires":
                    for requirement in package:
                        self.requirements.append(requirement[0])
                    package = list()
                if val == "recipe:":
                    self.products.append(package)
                    package = list()
            else:
                if val.isnumeric():
                    count = int(val)
                else:
                    phrase = val + " " + phrase

        if len(self.products) != 0:
            self.name = phrase[:-1]
        else:
            self.products.append(package)

        self.products = self.products[0]
        self.components = self.components[0]

        if len(self.requirements) != 0:
            requirements = self.requirements[0]
        else:
            self.requirements = ["crafting"]

    def GetMultistringDescription(self):
        res = "Creates "

        for product in self.products:
            res += str(product[1]) + " " + product[0] + " and "

        res = res[:-4]
        res += "\nfrom "

        for component in self.components:
            res += str(component[1]) + " " + component[0] + " and "

        res = res[:-4]

        if len(self.requirements) == 0:
            res += "\nand has no special requirements"
        else:
            res += "\nbut requires "

            for requirement in self.requirements:
                res += requirement[0] + " "

        res += "\nwith frequency " + str(self.perMinuteOperations) + " operations per minute"

        return res

class Factory:
    name = "Factory"
    efficiency = 1
    allowances = []
    consumption = []

    def Print(self):
        print(self.name, " works with efficiency ", self.efficiency,
              " consuming ", self.consumption,
              " and allows ", self.allowances)

    def ParseFromLine(self, line):
        words = line.split()
        length = len(words)
        phrase = ""
        self.allowances = []
        self.consumption = []
        self.efficiency = 1
        value = 1
        valSet = False
        phraseBlock = []

        while length > 0:
            length -= 1
            val = words.pop()

            try:
                value = float(val)
                valSet = True
                continue
            except ValueError:
                pass

            if IsSpecific(val, "factory"):
                if phrase != "":
                    if phrase[-1] == ' ':
                        phrase = phrase[:-1]

                if val == "consumes":
                    phraseBlock.append([phrase, value])
                    self.consumption = phraseBlock.copy()
                    phrase = ""
                    valSet = False
                    phraseBlock = []

                if val == "efficiency":
                    self.efficiency = value
                    phrase = ""
                    valSet = False

                if val == "allow":
                    phraseBlock.append(phrase)

                    for i in range(len(phraseBlock)):
                        if type(phraseBlock[i]) != str:
                            phraseBlock[i] = phraseBlock[i][0]

                    self.allowances = phraseBlock.copy()
                    phraseBlock = []
                    phrase = ""
                    valSet = False

                if val == "and":
                    phraseBlock.append([phrase, value])
                    phrase = ""
            else:
                phrase = val + " " + phrase

        if phrase[-1] == ' ':
            phrase = phrase[:-1]

        if valSet:
            if int(value) == value:
                value = int(value)
            phrase += " " + str(value)

        self.name = phrase

    def __init__(self, name="Factory", efficiency=1):
        self.name = name
        self.efficiency = efficiency

    def __lt__(self, other):
        return self.name < other.name

class RawSource:
    name = "Source"

    def __init__(self, name = "Source"):
        pass

    def ParseFromLine(self, line):
        self.name = line

    def Print(self):
        print("Raw source: ", self.name)

    def __eq__(self, other):
        return self.name == other.name

class Component:
    name = "component"

    def __init__(self, name = "component"):
        self.name = name

    def Print(self):
        print("Component: ", self.name)

    def __eq__(self, other):
        return self.name == other.name

class CraftRequirement:
    factories = None
    factoriesCount = 0
    optimalFactories = None

    product = None
    productCount = 0

    components = []
    craftsPerMinute = 0

    requirements = []

    def __init__(self, product, productCount, components, craftsPerMinute, requirements):
        # self.factory = factory
        # self.factoriesCount = factoriesCount
        self.product = product
        self.productCount = productCount
        self.components = components
        self.craftsPerMinute = craftsPerMinute
        self.requirements = requirements

    def ToString(self):
        line = "To craft " + str(self.productCount) + " " + str(self.product[0])  # + " you will need "
        line += " you will need " + str(self.factoriesCount) + " " + str(self.factories)

        for component in self.components:
            line += str(component[1]) + " " + str(component[0]) + " and "

        line = line[:-5]

        return line

    def GetInfoString(self):
        line = "To craft " + str(self.productCount) + " " + str(self.product[0]) + " you will need "
        if type(self.optimalFactories) == Factory:
            line += str(self.factoriesCount) + " of " + str(self.optimalFactories.name) + " consumping "

        for component in self.components:
            line += " " + str(component[1] * self.factoriesCount) + " " + component[0] + " and "

        line = line[:-4]

        return line

    def Print(self):
        print(self.ToString())

    def Append(self, craftsPerMinute):
        self.craftsPerMinute += craftsPerMinute
        pass

    def GiveFactories(self, factories):
        self.factories = factories

    def FindFactoryCount(self):
        factory = None
        maxProd = 0

        for fac in self.factories:
            if fac.efficiency > maxProd:
                factory = fac
                maxProd = fac.efficiency

        self.factoriesCount = math.ceil(self.craftsPerMinute / maxProd)
        self.optimalFactories = factory
