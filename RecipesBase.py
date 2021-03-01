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
    print(val)

    perMinute = False

    if ("per" in val) and ("minute" in val):
        count = int([x for x in val if x.isnumeric()][0])
        perMinute = [True, count]
        del words[-3:]
        print(count)
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
    _factories = []
    _components = []

    def __init__(self):
        pass

    def FactoriesCount(self):
        return len(self._factories)

    def RecipesCount(self):
        return len(self._recipes)

    def AddRecipe(self, recipe):
        self._recipes.append(recipe)

    def AddComponent(self, component):
        if not component in self._components:
            self._components.append(component)

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

    def PrintAllRecipes(self):
        print("Contains ", self.RecipesCount(), " recipes:")
        for recipe in self._recipes:
            PrintRecipe(recipe)

    def _GetRecipe(self, item):
        # print(item)
        recipe = list(filter(lambda x: item == x.product[0][0], self._recipes))
        # recipe = [recipe for recipe in self._recipes if item in recipe.product[:]]
        if len(recipe) != 0:
            recipe = recipe[0]
        # print(recipe)
        # print(len(recipe[0].product[0]), recipe[0].product[0[0]])

    def CalculateRequest(self, item, count):
        recipe = self._GetRecipe(item)
